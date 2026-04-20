from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from kb_chunk_search import build_answer, search_chunks
from simulate_kb_eval import load_chunk_vectors
from vector_model import DEFAULT_DIMENSIONS


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TICKETS = ROOT / "data" / "real-ticket-list.json"
DEFAULT_INDEX = ROOT / "data" / "kb-index.json"
DEFAULT_CHUNKS = ROOT / "data" / "kb-chunks.json"
DEFAULT_CHUNK_VECTORS = ROOT / "data" / "kb-chunk-vector-index.json"
DEFAULT_OUTPUT = ROOT / "reports" / "real-ticket-eval.json"
DEFAULT_REPORT = ROOT / "reports" / "real-ticket-eval.md"


SENSITIVE_LABEL_KEYS = {
    "contact_name",
    "contact_phone",
    "contact_email",
    "phone",
    "mobile",
    "email",
    "external_no",
}

NOISY_CONTEXT_KEYS = {
    "asset_no",
    "device_info",
    "external_id",
    "external_system",
    "fault_type",
    "location",
}

ALERT_CONTEXT_KEYS = {
    "alertname",
    "rule_name",
    "severity",
    "job",
    "name",
    "service",
    "instance",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def redact(text: str) -> str:
    text = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "<手机号>", text or "")
    text = re.sub(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)", "<IP>", text)
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<邮箱>", text)
    text = re.sub(r"Bearer\s+[A-Za-z0-9._-]+", "Bearer <TOKEN>", text, flags=re.I)
    return text


def compact_text(*values) -> str:
    parts = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, (dict, list)):
            continue
        text = str(value).strip()
        if text:
            parts.append(text)
    return "\n".join(parts)


def flatten_context(data: dict, prefix: str = "", allow_keys: set[str] | None = None) -> list[str]:
    rows = []
    for key, value in (data or {}).items():
        key_text = f"{prefix}.{key}" if prefix else str(key)
        key_lower = str(key).lower()
        if key_text.lower() in SENSITIVE_LABEL_KEYS or key_lower in SENSITIVE_LABEL_KEYS:
            continue
        if key_lower in NOISY_CONTEXT_KEYS:
            continue
        if allow_keys is not None and key_lower not in allow_keys:
            continue
        if value in (None, "", [], {}):
            continue
        if isinstance(value, dict):
            rows.extend(flatten_context(value, key_text, allow_keys=allow_keys))
        elif isinstance(value, list):
            simple = [str(item) for item in value if not isinstance(item, (dict, list)) and str(item).strip()]
            if simple:
                rows.append(f"{key_text}: {' '.join(simple[:5])}")
        else:
            text = str(value).strip()
            if text and len(text) <= 200:
                rows.append(f"{key_text}: {text}")
    return rows


def build_query(ticket: dict) -> str:
    is_alert = any(
        str(ticket.get(field) or "").strip()
        for field in ["eventId", "ruleId", "alertRuleId", "alertFingerprint", "datasourceType"]
    )
    core = compact_text(
        ticket.get("title"),
        ticket.get("description"),
        ticket.get("rootCause"),
        ticket.get("solution"),
        ticket.get("faultCenterId"),
    )
    context_rows = []
    if is_alert:
        context_rows.append(compact_text(ticket.get("datasourceType"), ticket.get("targetIP")))
        context_rows.extend(flatten_context(ticket.get("labels") or {}, allow_keys=ALERT_CONTEXT_KEYS))
        context_rows.extend(flatten_context(ticket.get("customFields") or {}, allow_keys=ALERT_CONTEXT_KEYS))
    return compact_text(core, "\n".join(context_rows[:12]))[:1200]


def classify(ticket: dict, query: str) -> str:
    alert_fields = [
        ticket.get("eventId"),
        ticket.get("ruleId"),
        ticket.get("alertRuleId"),
        ticket.get("alertFingerprint"),
        ticket.get("datasourceType"),
    ]
    if any(str(value or "").strip() for value in alert_fields):
        return "server-alert"
    if re.search(r"下载|安装包|驱动.*(在哪|下载|路径)|软件库", query):
        return "software"
    return "manual-ticket"


def required_kind(category: str, query: str) -> str:
    if category == "software":
        return "references"
    if category == "server-alert":
        return "steps_or_commands"
    if re.search(r"命令|指令|脚本|服务器|告警|CPU|内存|磁盘|Kubernetes|MySQL|Oracle|Redis", query, re.I):
        return "steps_or_commands"
    return "steps"


def has_requirement(answer: dict, requirement: str) -> bool:
    steps = answer.get("suggested_steps") or []
    commands = answer.get("commands") or []
    references = answer.get("references") or []
    if requirement == "steps":
        return len(steps) >= 3
    if requirement == "references":
        return len(references) >= 1
    if requirement == "steps_or_commands":
        return len(steps) >= 3 or len(commands) >= 1
    return False


def is_usable(category: str, requirement_ok: bool, score: int, answer: dict, top_doc: str) -> bool:
    if not requirement_ok or not top_doc:
        return False
    is_software_doc = "软件库目录" in top_doc or "software catalog" in top_doc.lower()
    if category != "software" and is_software_doc:
        return False
    if score >= 35:
        return True
    if category == "manual-ticket" and score >= 27 and len(answer.get("suggested_steps") or []) >= 5:
        return True
    return False


def evaluate_ticket(
    ticket: dict,
    chunks: list[dict],
    vectors: list[dict],
    index: list[dict],
    top_k: int,
    mode: str,
    cache: dict[str, tuple[list[dict], dict]],
) -> dict:
    query = build_query(ticket)
    category = classify(ticket, query)
    requirement = required_kind(category, query)
    cached = cache.get(query)
    if cached:
        hits, answer = cached
    else:
        hits = search_chunks(
            chunks,
            query,
            top_k=top_k,
            mode=mode,
            vector_records=vectors,
            dimensions=DEFAULT_DIMENSIONS,
        )
        answer = build_answer(query, hits, index)
        cache[query] = (hits, answer)
    top_hit = hits[0] if hits else {}
    score = int(top_hit.get("score") or 0)
    requirement_ok = has_requirement(answer, requirement)
    usable = bool(hits) and is_usable(category, requirement_ok, score, answer, top_hit.get("doc_title", ""))
    sources = answer.get("sources") or []
    return {
        "ticket_id": ticket.get("ticketNo") or ticket.get("ticketId") or "",
        "status": ticket.get("status", ""),
        "type": ticket.get("type", ""),
        "source": ticket.get("source", ""),
        "category": category,
        "requirement": requirement,
        "matched": bool(hits),
        "usable": usable,
        "requirement_ok": requirement_ok,
        "top_score": score,
        "top_rule_score": top_hit.get("rule_score", 0),
        "top_vector_score": top_hit.get("vector_score", 0),
        "top_doc": top_hit.get("doc_title", ""),
        "top_chunk": top_hit.get("title", ""),
        "top_path": top_hit.get("path", ""),
        "steps_count": len(answer.get("suggested_steps") or []),
        "commands_count": len(answer.get("commands") or []),
        "references_count": len(answer.get("references") or []),
        "query_preview": redact(query.replace("\n", " "))[:220],
        "summary": redact(answer.get("summary", "")),
        "sample_steps": [redact(item) for item in (answer.get("suggested_steps") or [])[:3]],
        "sample_commands": answer.get("commands", [])[:3],
        "sample_references": [redact(item) for item in (answer.get("references") or [])[:3]],
        "sources": sources[:3],
    }


def summarize(results: list[dict]) -> dict:
    def pct(n: int, d: int) -> float:
        return round(n / max(d, 1) * 100, 2)

    by_category = defaultdict(list)
    by_status = defaultdict(list)
    for item in results:
        by_category[item["category"]].append(item)
        by_status[item["status"] or "unknown"].append(item)

    return {
        "total": len(results),
        "matched": sum(1 for item in results if item["matched"]),
        "usable": sum(1 for item in results if item["usable"]),
        "match_rate": pct(sum(1 for item in results if item["matched"]), len(results)),
        "usable_rate": pct(sum(1 for item in results if item["usable"]), len(results)),
        "avg_top_score": round(sum(item["top_score"] for item in results) / max(len(results), 1), 2),
        "category": {
            key: {
                "total": len(items),
                "match_rate": pct(sum(1 for item in items if item["matched"]), len(items)),
                "usable_rate": pct(sum(1 for item in items if item["usable"]), len(items)),
                "avg_top_score": round(sum(item["top_score"] for item in items) / max(len(items), 1), 2),
            }
            for key, items in sorted(by_category.items())
        },
        "status": {key: len(items) for key, items in sorted(by_status.items())},
        "top_docs": Counter(item["top_doc"] for item in results if item["top_doc"]).most_common(20),
        "weak_samples": [
            item
            for item in sorted(results, key=lambda row: (row["usable"], row["top_score"], row["ticket_id"]))
            if not item["usable"]
        ][:30],
    }


def write_report(summary: dict, results: list[dict], output: Path, report: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": summary,
        "results": results,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    output_label = output.resolve()
    try:
        output_label_text = output_label.relative_to(ROOT).as_posix()
    except ValueError:
        output_label_text = output.as_posix()

    lines = [
        "# 真实工单知识库评测报告",
        "",
        f"- 生成时间：{payload['generated_at']}",
        f"- 工单数量：{summary['total']}",
        f"- 检索命中率：{summary['match_rate']}%",
        f"- 答案可用率：{summary['usable_rate']}%",
        f"- 平均最高分：{summary['avg_top_score']}",
        f"- 明细数据：`{output_label_text}`（本地忽略，不提交）",
        "",
        "## 分类结果",
        "",
        "| 分类 | 数量 | 命中率 | 可用率 | 平均最高分 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for key, item in summary["category"].items():
        lines.append(f"| {key} | {item['total']} | {item['match_rate']}% | {item['usable_rate']}% | {item['avg_top_score']} |")

    lines.extend(["", "## 状态分布", ""])
    for key, count in summary["status"].items():
        lines.append(f"- {key}: {count}")

    lines.extend(["", "## 常见首位命中文档", ""])
    for title, count in summary["top_docs"][:15]:
        lines.append(f"- {title}: {count}")

    lines.extend(["", "## 未达可用样本", ""])
    if not summary["weak_samples"]:
        lines.append("- 无")
    for item in summary["weak_samples"][:20]:
        lines.extend(
            [
                f"### {item['ticket_id']}",
                "",
                f"- 分类：{item['category']}",
                f"- 状态：{item['status']}",
                f"- 问题摘要：{item['query_preview']}",
                f"- 首位文档：{item['top_doc'] or '未命中'}",
                f"- 分数：{item['top_score']}",
                f"- 步骤/命令/引用数量：{item['steps_count']} / {item['commands_count']} / {item['references_count']}",
                "",
            ]
        )
    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate current KB against real fetched tickets.")
    parser.add_argument("--tickets", type=Path, default=DEFAULT_TICKETS)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--chunk-vectors", type=Path, default=DEFAULT_CHUNK_VECTORS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--mode", choices=["rules", "hybrid", "vector"], default="rules")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    tickets_payload = load_json(args.tickets)
    tickets = tickets_payload.get("tickets") or []
    if args.limit > 0:
        tickets = tickets[: args.limit]
    index = load_json(args.index)
    chunks = load_json(args.chunks)
    vectors = [] if args.mode == "rules" else load_chunk_vectors(args.chunk_vectors)
    cache: dict[str, tuple[list[dict], dict]] = {}
    results = [evaluate_ticket(ticket, chunks, vectors, index, args.top_k, args.mode, cache) for ticket in tickets]
    summary = summarize(results)
    write_report(summary, results, args.output, args.report)
    print(json.dumps({k: summary[k] for k in ["total", "match_rate", "usable_rate", "avg_top_score", "category", "status"]}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
