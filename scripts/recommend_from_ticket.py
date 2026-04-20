from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

from vector_model import build_vector_records, vector_search


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "data" / "kb-index.json"
DEFAULT_TICKETS = ROOT / "工单报修历史记录.csv"
DEFAULT_OUTPUT = ROOT / "reports" / "recommendation-dry-run.csv"
DEFAULT_SUMMARY = ROOT / "reports" / "recommendation-summary.md"
DEFAULT_SYNONYMS = ROOT / "taxonomy" / "query-synonyms.json"


STOP_WORDS = {
    "the",
    "and",
    "with",
    "status",
    "type",
    "source",
    "ticket",
    "history",
    "windows",
}


def normalize(text: str) -> str:
    text = (text or "").lower()
    text = text.replace("，", ",").replace("。", ".").replace("：", ":")
    return re.sub(r"\s+", " ", text).strip()


def compact(text: str) -> str:
    return re.sub(r"[\s,，。.!！?？:：;；、/\\|_-]+", "", normalize(text))


@lru_cache(maxsize=1)
def load_query_synonyms(path: str = str(DEFAULT_SYNONYMS)) -> tuple[tuple[str, ...], ...]:
    source = Path(path)
    if not source.exists():
        return ()
    groups = json.loads(source.read_text(encoding="utf-8"))
    result = []
    for group in groups:
        terms = [group.get("canonical", "")]
        terms.extend(group.get("aliases", []))
        cleaned = []
        seen = set()
        for term in terms:
            term = normalize(str(term))
            key = compact(term)
            if not term or not key or key in seen:
                continue
            seen.add(key)
            cleaned.append(term)
        if cleaned:
            result.append(tuple(cleaned))
    return tuple(result)


def expand_query_terms(text: str) -> str:
    text = text or ""
    text_norm = normalize(text)
    text_compact = compact(text)
    additions = []
    seen = set()
    for terms in load_query_synonyms():
        matched = False
        for term in terms:
            if keyword_hit(term, text_norm, text_compact):
                matched = True
                break
        if not matched:
            continue
        for term in terms:
            key = compact(term)
            if key and key not in seen and key not in text_compact:
                seen.add(key)
                additions.append(term)
    if not additions:
        return text
    return text + "\n" + " ".join(additions)


def split_terms(values) -> list[str]:
    terms = []
    for value in values:
        if not value:
            continue
        if isinstance(value, list):
            terms.extend(split_terms(value))
            continue
        value = str(value)
        terms.append(value)
        terms.extend(re.findall(r"[a-zA-Z][a-zA-Z0-9.+#-]{1,}", value.lower()))
    return [term for term in terms if term and term not in STOP_WORDS]


def keyword_hit(keyword: str, text_norm: str, text_compact: str) -> bool:
    key = normalize(keyword)
    if not key or key in STOP_WORDS:
        return False
    if len(key) <= 1:
        return False
    if re.fullmatch(r"[a-z0-9+#.-]+", key):
        variants = {re.escape(key)}
        if "-" in key:
            variants.add(re.escape(key).replace(r"\-", r"[\s-]+"))
        pattern = r"(?<![a-z0-9])(?:" + "|".join(sorted(variants)) + r")(?![a-z0-9])"
        return bool(re.search(pattern, text_norm))
    if key in text_norm:
        return True
    key_compact = compact(key)
    return len(key_compact) >= 2 and key_compact in text_compact


def score_doc(doc: dict, description: str, resolution: str = "", expand: bool = True) -> tuple[int, list[str]]:
    if expand:
        description = expand_query_terms(description)
        resolution = expand_query_terms(resolution)
    desc_norm = normalize(description)
    desc_compact = compact(description)
    text_norm = normalize(f"{description}\n{resolution}")
    text_compact = compact(f"{description}\n{resolution}")
    score = 0
    reasons = []

    for keyword in doc.get("keywords", []):
        if keyword_hit(keyword, desc_norm, desc_compact):
            weight = 20 if len(compact(keyword)) >= 4 else 12
            score += weight
            reasons.append(f"问题描述关键词:{keyword}")
        elif keyword_hit(keyword, text_norm, text_compact):
            weight = 8 if len(compact(keyword)) >= 4 else 4
            score += weight
            reasons.append(f"处理记录关键词:{keyword}")

    for field, weight in [
        ("systems", 8),
        ("tags", 5),
        ("issue_types", 4),
        ("asset_types", 3),
    ]:
        for term in split_terms(doc.get(field, [])):
            if keyword_hit(term, desc_norm, desc_compact):
                score += weight * 2
                reasons.append(f"问题描述{field}:{term}")
            elif keyword_hit(term, text_norm, text_compact):
                score += weight
                reasons.append(f"处理记录{field}:{term}")

    title = doc.get("title", "")
    for token in re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]{2,}", title):
        if keyword_hit(token, desc_norm, desc_compact):
            score += 6
            reasons.append(f"问题描述标题:{token}")
        elif keyword_hit(token, text_norm, text_compact):
            score += 3
            reasons.append(f"处理记录标题:{token}")

    if reasons:
        status = doc.get("status")
        if status == "verified":
            score += 3
        elif status == "usable":
            score += 2
        elif status == "candidate":
            score -= 3

    return score, list(dict.fromkeys(reasons))[:8]


def recommendation_payload(doc: dict, score: int, reasons: list[str], vector_score: float = 0.0) -> dict:
    return {
        "doc_id": doc["doc_id"],
        "title": doc["title"],
        "status": doc.get("status", ""),
        "path": doc["path"],
        "score": score,
        "rule_score": score,
        "vector_score": round(vector_score, 4),
        "reason": reasons,
        "applicability": doc.get("applicability", []),
        "symptoms": doc.get("symptoms", []),
        "steps": doc.get("steps", []),
        "commands": doc.get("commands", []),
        "verification": doc.get("verification", []),
        "notes": doc.get("notes", []),
        "content_preview": doc.get("content_preview", ""),
    }


def recommend_rules(index: list[dict], description: str, resolution: str = "", top_k: int = 3) -> list[dict]:
    expanded_description = expand_query_terms(description)
    expanded_resolution = expand_query_terms(resolution)
    scored = []
    for doc in index:
        score, reasons = score_doc(doc, expanded_description, expanded_resolution, expand=False)
        if score > 0 and reasons:
            scored.append(recommendation_payload(doc, score, reasons))
    scored.sort(key=lambda item: (-item["score"], item["title"]))
    return scored[:top_k]


def recommend(
    index: list[dict],
    description: str,
    resolution: str = "",
    top_k: int = 3,
    mode: str = "hybrid",
    vector_records: list[dict] | None = None,
) -> list[dict]:
    mode = (mode or "hybrid").lower()
    if mode == "rules":
        return recommend_rules(index, description, resolution, top_k)

    by_doc_id = {doc["doc_id"]: doc for doc in index}
    scored: dict[str, dict] = {}
    expanded_description = expand_query_terms(description)
    expanded_resolution = expand_query_terms(resolution)

    for doc in index:
        rule_score, reasons = score_doc(doc, expanded_description, expanded_resolution, expand=False)
        if rule_score > 0 and reasons:
            scored[doc["doc_id"]] = recommendation_payload(doc, rule_score, reasons)

    if mode in {"hybrid", "vector"}:
        query = f"{description}\n{resolution}".strip()
        vectors = vector_records if vector_records is not None else build_vector_records(index)
        for item in vector_search(index, query, vector_records=vectors, top_k=max(top_k * 4, 10)):
            doc = by_doc_id[item["doc_id"]]
            vector_score = item["vector_score"]
            vector_points = int(vector_score * 80)
            if mode == "vector" or item["doc_id"] not in scored:
                if vector_score < 0.08:
                    continue
                scored[item["doc_id"]] = recommendation_payload(
                    doc,
                    vector_points,
                    [f"语义相似度:{vector_score:.2f}"],
                    vector_score=vector_score,
                )
                scored[item["doc_id"]]["rule_score"] = 0
            else:
                scored[item["doc_id"]]["vector_score"] = vector_score
                scored[item["doc_id"]]["score"] += vector_points
                scored[item["doc_id"]]["reason"].append(f"语义相似度:{vector_score:.2f}")

    results = list(scored.values())
    results.sort(key=lambda item: (-item["score"], -item.get("vector_score", 0), item["title"]))
    return results[:top_k]


def read_tickets(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_results(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "工单号",
        "问题描述",
        "解决步骤",
        "推荐1",
        "推荐1分数",
        "推荐1原因",
        "推荐2",
        "推荐2分数",
        "推荐2原因",
        "推荐3",
        "推荐3分数",
        "推荐3原因",
        "是否命中",
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict], summary: Path) -> None:
    total = len(rows)
    hit_rows = [row for row in rows if row["是否命中"] == "是"]
    miss_rows = [row for row in rows if row["是否命中"] != "是"]
    top_docs = Counter(row["推荐1"] for row in hit_rows if row["推荐1"])
    miss_terms = Counter()
    for row in miss_rows:
        desc = row["问题描述"]
        cleaned = re.sub(r"\d+", "", desc)
        for token in re.findall(r"[A-Za-z][A-Za-z0-9.+#-]{1,}|[\u4e00-\u9fff]{2,}", cleaned):
            if token.lower() not in STOP_WORDS:
                miss_terms[token] += 1

    category_counts = defaultdict(int)
    for row in hit_rows:
        doc = row["推荐1"]
        if "/" in doc:
            category_counts[doc.split("/")[0]] += 1

    hit_rate = (len(hit_rows) / total * 100) if total else 0
    lines = [
        "# 知识推荐离线回测报告",
        "",
        "本报告由本地脚本根据历史工单和 Markdown 知识库生成，未连接任何服务器、接口或外部服务。",
        "",
        "## 总体结果",
        "",
        f"- 工单总数：{total}",
        f"- 有推荐命中：{len(hit_rows)}",
        f"- 无推荐命中：{len(miss_rows)}",
        f"- 命中率：{hit_rate:.1f}%",
        "",
        "## Top 推荐知识",
        "",
    ]
    if top_docs:
        for doc, count in top_docs.most_common(20):
            lines.append(f"- {doc}：{count}")
    else:
        lines.append("- 暂无命中。")

    lines.extend(["", "## 未命中高频词", ""])
    if miss_terms:
        for term, count in miss_terms.most_common(30):
            lines.append(f"- {term}：{count}")
    else:
        lines.append("- 暂无未命中词。")

    lines.extend(
        [
            "",
            "## 下一步建议",
            "",
            "- 对未命中高频词补充关键词或新增细分知识。",
            "- 检查高频推荐是否过于泛化，必要时继续拆分场景。",
            "- 将 `reports/recommendation-dry-run.csv` 中的推荐结果抽样给工程师确认，优化关键词权重。",
        ]
    )

    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run offline knowledge recommendations for historical tickets.")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--tickets", type=Path, default=DEFAULT_TICKETS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--mode", choices=["rules", "vector", "hybrid"], default="hybrid")
    args = parser.parse_args()

    index = json.loads(args.index.read_text(encoding="utf-8"))
    vector_records = build_vector_records(index) if args.mode in {"vector", "hybrid"} else None
    tickets = read_tickets(args.tickets)
    rows = []
    for ticket in tickets:
        ticket_id = (ticket.get("工单号") or "").strip()
        description = (ticket.get("问题描述") or "").strip()
        resolution = (ticket.get("解决步骤") or "").strip()
        recs = recommend(index, description, resolution, top_k=args.top_k, mode=args.mode, vector_records=vector_records)
        row = {
            "工单号": ticket_id,
            "问题描述": description,
            "解决步骤": resolution,
            "推荐1": "",
            "推荐1分数": "",
            "推荐1原因": "",
            "推荐2": "",
            "推荐2分数": "",
            "推荐2原因": "",
            "推荐3": "",
            "推荐3分数": "",
            "推荐3原因": "",
            "是否命中": "是" if recs else "否",
        }
        for idx, rec in enumerate(recs[:3], start=1):
            row[f"推荐{idx}"] = f"{Path(rec['path']).parent.name}/{rec['doc_id']}"
            row[f"推荐{idx}分数"] = rec["score"]
            row[f"推荐{idx}原因"] = "；".join(rec["reason"])
        rows.append(row)

    write_results(rows, args.output)
    write_summary(rows, args.summary)
    print(f"Processed {len(rows)} tickets -> {args.output}")
    print(f"Summary -> {args.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
