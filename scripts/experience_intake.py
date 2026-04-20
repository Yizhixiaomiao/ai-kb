from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIENCE_LOG = ROOT / "data" / "ticket-experiences.jsonl"
DEFAULT_CANDIDATES = ROOT / "data" / "kb-candidates.json"


VAGUE_RESOLUTIONS = {
    "已处理",
    "处理完成",
    "已解决",
    "好了",
    "正常",
    "恢复",
    "已恢复",
    "重启好了",
    "重启后正常",
}

ACTION_TERMS = [
    "检查",
    "重启",
    "重新",
    "清理",
    "清除",
    "取消",
    "安装",
    "卸载",
    "更换",
    "替换",
    "修复",
    "配置",
    "删除",
    "添加",
    "更新",
    "恢复",
    "认证",
    "登录",
    "授权",
    "扩容",
    "释放",
    "重建",
    "执行",
    "同步",
    "调整",
]

OBJECT_TERMS = [
    "电脑",
    "主机",
    "打印机",
    "驱动",
    "服务",
    "缓存",
    "浏览器",
    "网络",
    "网线",
    "交换机",
    "摄像头",
    "门禁",
    "道闸",
    "会议",
    "服务器",
    "数据库",
    "CPU",
    "内存",
    "磁盘",
    "容器",
    "Pod",
    "MES",
    "OA",
    "PLM",
    "SAP",
    "WMS",
]

VERIFY_TERMS = ["恢复", "正常", "验证", "可以", "能够", "成功", "无告警", "不再", "完成", "生效"]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def compact(value: str) -> str:
    return re.sub(r"[\s,，。.!！?？:：;；、/\\|_-]+", "", normalize_text(value))


def has_any(text: str, terms: list[str]) -> bool:
    text_lower = text.lower()
    return any(term.lower() in text_lower for term in terms)


def has_command(text: str) -> bool:
    patterns = [
        r"\b(systemctl|service|journalctl|top|ps|df|du|free|vmstat|iostat|pidstat|kubectl|docker|netstat|ss|ping|tracert|ipconfig)\b",
        r"\b(control printers|services\.msc|devmgmt\.msc|eventvwr\.msc|gpupdate|chkdsk|sfc|dism)\b",
    ]
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)


def assess_experience(payload: dict) -> dict:
    title = normalize_text(payload.get("title"))
    description = normalize_text(payload.get("description"))
    resolution = normalize_text(payload.get("resolution"))
    full_text = "\n".join(part for part in [title, description, resolution] if part)
    resolution_compact = compact(resolution)

    points = 0
    missing_fields: list[str] = []
    signals: list[str] = []

    if len(resolution_compact) >= 8 and resolution_compact not in VAGUE_RESOLUTIONS:
        points += 2
        signals.append("处理记录不是单纯的已处理/已恢复")
    else:
        missing_fields.append("具体处理动作")

    if len(resolution_compact) >= 20:
        points += 1
        signals.append("处理记录包含较多上下文")

    if has_any(full_text, OBJECT_TERMS):
        points += 2
        signals.append("包含故障对象或系统名称")
    else:
        missing_fields.append("故障对象或系统名称")

    if has_any(resolution, ACTION_TERMS):
        points += 2
        signals.append("包含可复用处理动作")
    else:
        missing_fields.append("可复用处理动作")

    if has_any(resolution, VERIFY_TERMS):
        points += 1
        signals.append("包含恢复或验证描述")
    else:
        missing_fields.append("验证结果")

    if has_command(resolution):
        points += 2
        signals.append("包含可执行命令或系统工具")

    if title and description:
        points += 1
        signals.append("包含标题和问题描述")

    if points >= 7:
        quality = "high"
    elif points >= 4:
        quality = "medium"
    else:
        quality = "low"

    questions = []
    if "故障对象或系统名称" in missing_fields:
        questions.append("具体处理的是哪个设备、系统、服务或业务模块？")
    if "具体处理动作" in missing_fields or "可复用处理动作" in missing_fields:
        questions.append("实际执行了什么操作、命令、配置修改或替换动作？")
    if "验证结果" in missing_fields:
        questions.append("如何确认问题已经恢复，是否有验证截图、日志或业务操作结果？")

    return {
        "quality": quality,
        "quality_score": points,
        "signals": signals,
        "missing_fields": list(dict.fromkeys(missing_fields)),
        "suggested_questions": questions,
    }


def split_resolution_steps(resolution: str) -> list[str]:
    resolution = normalize_text(resolution)
    if not resolution:
        return []
    parts = re.split(r"[；;。.\n]+|(?:\d+[、.])", resolution)
    steps = [part.strip(" ，,") for part in parts if len(compact(part)) >= 3]
    if not steps and resolution:
        steps = [resolution]
    return steps[:8]


def infer_title(payload: dict, matched_doc: dict | None) -> str:
    if matched_doc:
        return f"{matched_doc.get('title', '')}补充经验"
    title = normalize_text(payload.get("title"))
    if title:
        return f"{title}处理指南"
    return "待整理运维问题处理指南"


def build_candidate(payload: dict, assessment: dict, matched_doc: dict | None = None) -> dict:
    ticket_id = normalize_text(payload.get("ticket_id")) or f"ticket-{int(time.time())}"
    title = infer_title(payload, matched_doc)
    description = normalize_text(payload.get("description"))
    resolution = normalize_text(payload.get("resolution"))
    steps = split_resolution_steps(resolution)

    candidate = {
        "candidate_id": f"cand-{int(time.time())}-{uuid.uuid4().hex[:8]}",
        "title": title,
        "status": "needs_review",
        "quality": assessment["quality"],
        "source_ticket_ids": [ticket_id],
        "matched_doc_id": matched_doc.get("doc_id") if matched_doc else "",
        "problem": normalize_text(payload.get("title")) or description,
        "symptoms": [description] if description else [],
        "steps": steps,
        "commands": [],
        "verification": ["待工程师补充验证方式。"] if "验证结果" in assessment["missing_fields"] else [],
        "notes": [
            "本条由工单处理记录自动生成，不能直接发布为正式知识。",
            "发布前需要确认适用范围、处理步骤、风险和验证方式。",
        ],
        "missing_fields": assessment["missing_fields"],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    return candidate


def load_candidates(path: Path = DEFAULT_CANDIDATES) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8") or "[]")


def save_candidates(candidates: list[dict], path: Path = DEFAULT_CANDIDATES) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")


def append_experience(record: dict, path: Path = DEFAULT_EXPERIENCE_LOG) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def count_jsonl(path: Path = DEFAULT_EXPERIENCE_LOG) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def recent_experiences(path: Path = DEFAULT_EXPERIENCE_LOG, limit: int = 50) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows[-limit:]
