from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from kb_chunk_search import build_answer, search_chunks
from vector_model import DEFAULT_DIMENSIONS


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "data" / "kb-index.json"
DEFAULT_CHUNKS = ROOT / "data" / "kb-chunks.json"
DEFAULT_CHUNK_VECTORS = ROOT / "data" / "kb-chunk-vector-index.json"
DEFAULT_ALERT_RULES = ROOT / "data" / "alert-rules.json"
DEFAULT_OUTPUT = ROOT / "reports" / "simulated-ticket-eval.json"
DEFAULT_REPORT = ROOT / "reports" / "simulated-ticket-eval.md"


DESKTOP_CASES = [
    {
        "category": "desktop",
        "topic": "电脑无法开机",
        "queries": [
            "用户反馈办公电脑无法开机，按电源键没有反应",
            "工位电脑开不了机，主机不通电，显示器也没亮",
            "台式机无法启动，风扇不转，用户着急处理",
        ],
        "must_have": ["steps"],
    },
    {
        "category": "desktop",
        "topic": "打印机脱机",
        "queries": [
            "用户打印文件时提示打印机脱机，无法打印",
            "共享打印机显示脱机，打印任务一直卡在队列",
            "办公室打印机不出纸，电脑上显示已暂停或脱机",
        ],
        "must_have": ["steps", "commands"],
    },
    {
        "category": "desktop",
        "topic": "打印不清楚",
        "queries": [
            "用户反馈打印出来颜色很淡，打印不清楚",
            "标签打印机打印有空白间隔，怀疑打印头磨损",
            "打印文件有横纹，字迹模糊，影响发货单",
        ],
        "must_have": ["steps"],
    },
    {
        "category": "desktop",
        "topic": "网络认证",
        "queries": [
            "电脑连不上内网，网络认证客户端提示异常",
            "用户说 MES 打不开，认证助手登录后还是没网",
            "工位电脑上不了网，怀疑网络认证失败",
        ],
        "must_have": ["steps", "commands"],
    },
    {
        "category": "desktop",
        "topic": "CAD",
        "queries": [
            "CAD 打开后卡死无响应，用户无法编辑图纸",
            "AutoCAD 安装失败，卸载后重新安装还是报错",
            "CAD 保存到 PLM 管理系统失败，无法传图",
        ],
        "must_have": ["steps"],
    },
    {
        "category": "desktop",
        "topic": "SolidWorks",
        "queries": [
            "SolidWorks 打开提示无法获得许可，软件进不去",
            "solidworks 重装时提示缺少 solidworks.msi",
            "SolidWorks 菜单栏和工具栏图标不见了",
        ],
        "must_have": ["steps"],
    },
    {
        "category": "desktop",
        "topic": "业务系统登录",
        "queries": [
            "用户反馈 PLM 客户端无法登录，账号密码确认没错",
            "OA 附件上传很慢，浏览器兼容性可能有问题",
            "SAP GUI 登录失败，提示连接异常",
        ],
        "must_have": ["steps"],
    },
    {
        "category": "software",
        "topic": "软件下载路径",
        "queries": [
            "需要下载 SAP GUI 安装包，给我软件库路径",
            "网络认证客户端怎么下载，给下载路径",
            "Ricoh 打印机驱动在哪里下载",
            "MES 客户端安装包在哪里",
            "PLM 客户端安装包下载路径",
        ],
        "must_have": ["references"],
    },
    {
        "category": "desktop",
        "topic": "安防设备",
        "queries": [
            "摄像头无视频信号，监控画面黑屏",
            "道闸无法抬杆，车辆无法通过",
            "门禁刷卡没有反应，员工进不去",
        ],
        "must_have": ["steps"],
    },
    {
        "category": "desktop",
        "topic": "会议室设备",
        "queries": [
            "会议室投屏失败，电脑连接后没有画面",
            "会议摄像头没有图像，线上会议无法使用",
            "会议室麦克风没有声音，需要排查设备",
        ],
        "must_have": ["steps"],
    },
]


SERVER_FALLBACK_RULES = [
    "CPU使用率达到95%",
    "内存使用率达到95%",
    "磁盘空间使用率达到90%",
    "磁盘 inode 使用率过高",
    "主机不可达",
    "MySQL 连接数过高",
    "Oracle 表空间使用率过高",
    "Nginx 5xx 错误率过高",
    "JVM Full GC 频繁",
    "Kubernetes Pod CrashLoopBackOff",
    "vSphere 虚拟化主机告警",
    "Data Domain 空间不足",
    "NetWorker 备份失败",
    "HANA HA 状态异常",
    "MES 服务异常",
]


SERVER_CONTEXTS = [
    "生产环境服务器 {host} 触发告警：{rule}，请给出排查步骤和常用命令",
    "告警平台收到 {system} 的 {rule}，实例 {host}，需要工程师快速处理",
    "{rule} 告警持续 10 分钟，labels: job={system}, name={host}",
    "服务器告警工单：{rule}，影响对象 {host}，请按知识库生成处理建议",
]


HOSTS = ["app-01", "db-02", "mes-prod-03", "sap-if-01", "k8s-node-05", "backup-01", "vsphere-host-02"]
SYSTEMS = ["MES", "PLM", "SAP", "OA", "WMS", "backup", "kubernetes", "database", "node"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunk_vectors(path: Path) -> list[dict]:
    payload = load_json(path)
    if isinstance(payload, dict):
        return payload.get("chunks") or payload.get("records") or []
    return payload


def load_alert_rule_names(path: Path) -> list[str]:
    if not path.exists():
        return SERVER_FALLBACK_RULES
    payload = load_json(path)
    names = []
    for group in payload.get("groups", []):
        for rule in group.get("rules", []):
            name = str(rule.get("ruleName") or "").strip()
            if name:
                names.append(name)
    return names or SERVER_FALLBACK_RULES


def simulate_tickets(count: int, alert_rules: list[str], seed: int) -> list[dict]:
    rng = random.Random(seed)
    tickets = []
    desktop_count = count // 2
    alert_count = count - desktop_count

    for idx in range(1, desktop_count + 1):
        case = rng.choice(DESKTOP_CASES)
        query = rng.choice(case["queries"])
        if rng.random() < 0.25:
            query += "，用户描述比较简单：帮忙看一下"
        tickets.append(
            {
                "ticket_id": f"SIM-D-{idx:04d}",
                "category": case["category"],
                "topic": case["topic"],
                "query": query,
                "must_have": case["must_have"],
            }
        )

    for idx in range(1, alert_count + 1):
        rule = rng.choice(alert_rules)
        template = rng.choice(SERVER_CONTEXTS)
        query = template.format(rule=rule, host=rng.choice(HOSTS), system=rng.choice(SYSTEMS))
        tickets.append(
            {
                "ticket_id": f"SIM-A-{idx:04d}",
                "category": "server-alert",
                "topic": rule,
                "query": query,
                "must_have": ["steps_or_commands"],
            }
        )

    rng.shuffle(tickets)
    return tickets


def has_requirement(answer: dict, requirement: str) -> bool:
    steps = answer.get("suggested_steps") or []
    commands = answer.get("commands") or []
    references = answer.get("references") or []
    if requirement == "steps":
        return len(steps) >= 3
    if requirement == "commands":
        return len(commands) >= 1
    if requirement == "references":
        return len(references) >= 1
    if requirement == "steps_or_commands":
        return len(steps) >= 3 or len(commands) >= 1
    return False


def evaluate_ticket(
    ticket: dict,
    chunks: list[dict],
    vectors: list[dict],
    index: list[dict],
    top_k: int,
    answer_cache: dict[str, tuple[list[dict], dict]],
) -> dict:
    cache_key = ticket["query"]
    if ticket.get("category") == "server-alert":
        cache_key = f"server-alert::{ticket.get('topic')}"
    cached = answer_cache.get(cache_key)
    if cached:
        hits, answer = cached
    else:
        hits = search_chunks(
            chunks,
            ticket["query"],
            top_k=top_k,
            mode="hybrid",
            vector_records=vectors,
            dimensions=DEFAULT_DIMENSIONS,
        )
        answer = build_answer(ticket["query"], hits, index)
        answer_cache[cache_key] = (hits, answer)
    requirements = ticket.get("must_have", [])
    passed_requirements = [req for req in requirements if has_requirement(answer, req)]
    top_hit = hits[0] if hits else {}
    top_source = (answer.get("sources") or [{}])[0]
    score = int(top_hit.get("score") or 0)
    has_good_score = score >= 35
    matched = bool(hits)
    passed = matched and has_good_score and len(passed_requirements) == len(requirements)

    return {
        "ticket_id": ticket["ticket_id"],
        "category": ticket["category"],
        "topic": ticket["topic"],
        "query": ticket["query"],
        "matched": matched,
        "passed": passed,
        "top_score": score,
        "top_doc": top_hit.get("doc_title", ""),
        "top_chunk": top_hit.get("title", ""),
        "top_path": top_hit.get("path", ""),
        "top_rule_score": top_hit.get("rule_score", 0),
        "top_vector_score": top_hit.get("vector_score", 0),
        "source_doc": top_source.get("title", ""),
        "source_path": top_source.get("path", ""),
        "steps_count": len(answer.get("suggested_steps") or []),
        "commands_count": len(answer.get("commands") or []),
        "references_count": len(answer.get("references") or []),
        "requirements": requirements,
        "passed_requirements": passed_requirements,
        "summary": answer.get("summary", ""),
        "sample_steps": (answer.get("suggested_steps") or [])[:3],
        "sample_commands": (answer.get("commands") or [])[:3],
        "sample_references": (answer.get("references") or [])[:3],
    }


def summarize(results: list[dict]) -> dict:
    total = len(results)
    by_category = defaultdict(list)
    by_topic = defaultdict(list)
    for item in results:
        by_category[item["category"]].append(item)
        by_topic[item["topic"]].append(item)

    def rate(items: list[dict], key: str) -> float:
        return round(sum(1 for item in items if item.get(key)) / max(len(items), 1) * 100, 2)

    return {
        "total": total,
        "matched": sum(1 for item in results if item["matched"]),
        "passed": sum(1 for item in results if item["passed"]),
        "match_rate": rate(results, "matched"),
        "pass_rate": rate(results, "passed"),
        "avg_top_score": round(sum(item["top_score"] for item in results) / max(total, 1), 2),
        "category": {
            category: {
                "total": len(items),
                "match_rate": rate(items, "matched"),
                "pass_rate": rate(items, "passed"),
                "avg_top_score": round(sum(item["top_score"] for item in items) / max(len(items), 1), 2),
            }
            for category, items in sorted(by_category.items())
        },
        "weak_topics": [
            {
                "topic": topic,
                "total": len(items),
                "pass_rate": rate(items, "passed"),
                "match_rate": rate(items, "matched"),
                "avg_top_score": round(sum(item["top_score"] for item in items) / max(len(items), 1), 2),
            }
            for topic, items in sorted(
                by_topic.items(),
                key=lambda pair: (rate(pair[1], "passed"), -len(pair[1]), pair[0]),
            )[:20]
        ],
        "top_docs": Counter(item["top_doc"] for item in results if item["top_doc"]).most_common(20),
    }


def write_report(summary: dict, results: list[dict], output: Path, report: Path, seed: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "seed": seed,
        "summary": summary,
        "results": results,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    failed = [item for item in results if not item["passed"]]
    lines = [
        "# 模拟工单知识库评测报告",
        "",
        f"- 生成时间：{payload['generated_at']}",
        f"- 随机种子：{seed}",
        f"- 工单总数：{summary['total']}",
        f"- 检索命中率：{summary['match_rate']}%",
        f"- 答案达标率：{summary['pass_rate']}%",
        f"- 平均最高分：{summary['avg_top_score']}",
        f"- 明细数据：`{output.relative_to(ROOT).as_posix()}`",
        "",
        "## 分类结果",
        "",
        "| 分类 | 数量 | 命中率 | 达标率 | 平均最高分 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for category, item in summary["category"].items():
        lines.append(
            f"| {category} | {item['total']} | {item['match_rate']}% | {item['pass_rate']}% | {item['avg_top_score']} |"
        )

    lines.extend(["", "## 薄弱主题", ""])
    lines.extend(["| 主题 | 数量 | 命中率 | 达标率 | 平均最高分 |", "| --- | ---: | ---: | ---: | ---: |"])
    for item in summary["weak_topics"]:
        lines.append(
            f"| {item['topic']} | {item['total']} | {item['match_rate']}% | {item['pass_rate']}% | {item['avg_top_score']} |"
        )

    lines.extend(["", "## 常见首位命中文档", ""])
    for title, count in summary["top_docs"][:10]:
        lines.append(f"- {title}: {count}")

    lines.extend(["", "## 未达标样本", ""])
    for item in failed[:20]:
        missing = sorted(set(item["requirements"]) - set(item["passed_requirements"]))
        lines.extend(
            [
                f"### {item['ticket_id']} {item['topic']}",
                "",
                f"- 分类：{item['category']}",
                f"- 问题：{item['query']}",
                f"- 首位文档：{item['top_doc'] or '未命中'}",
                f"- 分数：{item['top_score']}",
                f"- 缺失项：{', '.join(missing) if missing else '分数不足或未命中'}",
                "",
            ]
        )

    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate tickets and evaluate KB answer assembly quality.")
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260420)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--chunk-vectors", type=Path, default=DEFAULT_CHUNK_VECTORS)
    parser.add_argument("--alert-rules", type=Path, default=DEFAULT_ALERT_RULES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    index = load_json(args.index)
    chunks = load_json(args.chunks)
    vectors = load_chunk_vectors(args.chunk_vectors)
    alert_rules = load_alert_rule_names(args.alert_rules)
    tickets = simulate_tickets(args.count, alert_rules, args.seed)
    answer_cache: dict[str, tuple[list[dict], dict]] = {}
    results = [evaluate_ticket(ticket, chunks, vectors, index, args.top_k, answer_cache) for ticket in tickets]
    summary = summarize(results)
    write_report(summary, results, args.output, args.report, args.seed)
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
