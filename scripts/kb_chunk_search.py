from __future__ import annotations

import re
from collections import defaultdict

from recommend_from_ticket import keyword_hit, normalize, compact, score_doc, split_terms, expand_query_terms
from vector_model import DEFAULT_DIMENSIONS, cosine_similarity, vectorize_text


TYPE_WEIGHTS = {
    "overview": 9,
    "section": 7,
    "step": 10,
    "command": 6,
    "verification": 4,
    "note": 2,
}


def is_software_catalog_chunk(chunk: dict) -> bool:
    return chunk.get("type") == "software-catalog" or "software-catalog" in chunk.get("tags", [])


def is_software_lookup_query(query: str) -> bool:
    return bool(
        re.search(
            r"下载|安装包|软件库|驱动.*(下载|路径|在哪)|客户端.*(下载|安装|升级)|升级.*客户端|重装.*客户端",
            query,
            re.I,
        )
    )


def score_chunk(chunk: dict, query: str, original_query: str | None = None) -> tuple[int, list[str]]:
    software_intent_query = original_query or query
    query_norm = normalize(query)
    query_compact = compact(query)
    score = 0
    reasons: list[str] = []

    for keyword in chunk.get("keywords", []):
        if keyword_hit(keyword, query_norm, query_compact):
            weight = 18 if len(compact(keyword)) >= 4 else 10
            score += weight
            reasons.append(f"关键词:{keyword}")

    for field, weight in [
        ("systems", 8),
        ("tags", 5),
        ("issue_types", 5),
        ("asset_types", 3),
    ]:
        for term in split_terms(chunk.get(field, [])):
            if keyword_hit(term, query_norm, query_compact):
                score += weight
                reasons.append(f"{field}:{term}")

    title = chunk.get("title", "")
    if title and keyword_hit(title, query_norm, query_compact):
        score += 12
        reasons.append("标题匹配")

    content = chunk.get("content", "")
    if content:
        content_norm = normalize(content)
        for term in split_terms([query]):
            if keyword_hit(term, content_norm, compact(content)):
                score += 2

    if score > 0:
        score += TYPE_WEIGHTS.get(chunk.get("type"), 0)
        if is_software_catalog_chunk(chunk) and not is_software_lookup_query(software_intent_query):
            score -= 60
        elif is_software_catalog_chunk(chunk) and is_software_lookup_query(software_intent_query):
            score += 60
        if chunk.get("status") == "verified":
            score += 3
        elif chunk.get("status") == "usable":
            score += 2
        elif chunk.get("status") == "candidate":
            score -= 2

    return score, list(dict.fromkeys(reasons))[:8]


def search_chunks(
    chunks: list[dict],
    query: str,
    top_k: int = 8,
    mode: str = "hybrid",
    vector_records: list[dict] | None = None,
    dimensions: int = DEFAULT_DIMENSIONS,
) -> list[dict]:
    mode = (mode or "hybrid").lower()
    top_k = max(1, min(int(top_k or 8), 30))
    scored: dict[str, dict] = {}
    expanded_query = expand_query_terms(query)

    if mode in {"rules", "hybrid"}:
        for chunk in chunks:
            rule_score, reasons = score_chunk(chunk, expanded_query, original_query=query)
            if rule_score > 0 and reasons:
                scored[chunk["chunk_id"]] = {
                    **chunk,
                    "score": rule_score,
                    "rule_score": rule_score,
                    "vector_score": 0.0,
                    "reason": reasons,
                }

    if mode in {"vector", "hybrid"}:
        query_vector = vectorize_text(query, dimensions=dimensions)
        if query_vector:
            records = vector_records or []
            by_chunk_id = {chunk["chunk_id"]: chunk for chunk in chunks}
            vector_hits = []
            for record in records:
                score = cosine_similarity(query_vector, record.get("vector", {}))
                if score <= 0:
                    continue
                chunk = by_chunk_id.get(record.get("chunk_id"))
                if not chunk:
                    continue
                vector_hits.append((score, chunk))
            vector_hits.sort(key=lambda item: (-item[0], item[1].get("title", "")))

            for vector_score, chunk in vector_hits[: max(top_k * 6, 30)]:
                if vector_score < 0.05:
                    continue
                vector_points = int(vector_score * 100)
                existing = scored.get(chunk["chunk_id"])
                if existing:
                    existing["vector_score"] = round(vector_score, 4)
                    existing["score"] += vector_points
                    existing["reason"].append(f"语义相似度:{vector_score:.2f}")
                else:
                    scored[chunk["chunk_id"]] = {
                        **chunk,
                        "score": vector_points,
                        "rule_score": 0,
                        "vector_score": round(vector_score, 4),
                        "reason": [f"语义相似度:{vector_score:.2f}"],
                    }

    results = list(scored.values())
    results.sort(
        key=lambda item: (
            -item["score"],
            -TYPE_WEIGHTS.get(item.get("type"), 0),
            item.get("doc_title", ""),
            item.get("ordinal", 0),
        )
    )
    return results[:top_k]


def build_answer(query: str, hits: list[dict], doc_index: list[dict]) -> dict:
    docs_by_id = {doc["doc_id"]: doc for doc in doc_index}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for hit in hits:
        grouped[hit["doc_id"]].append(hit)

    ordered_docs = sorted(
        grouped.items(),
        key=lambda item: (-sum(hit["score"] for hit in item[1]), item[1][0].get("doc_title", "")),
    )

    steps = []
    commands = []
    verification = []
    cautions = []
    references = []
    sources = []

    primary_doc_id = ordered_docs[0][0] if ordered_docs else ""

    for doc_id, doc_hits in ordered_docs[:3]:
        doc = docs_by_id.get(doc_id, {})
        sources.append(
            {
                "doc_id": doc_id,
                "title": doc.get("title") or doc_hits[0].get("doc_title", ""),
                "path": doc.get("path") or doc_hits[0].get("path", ""),
                "score": sum(hit["score"] for hit in doc_hits),
                "chunks": [hit["chunk_id"] for hit in doc_hits[:5]],
            }
        )

        # The final answer should stay anchored on the strongest matched document.
        # Secondary documents are kept as sources for traceability, but their
        # steps/commands should not be mixed into the main procedure.
        if doc_id != primary_doc_id:
            continue

        for hit in doc_hits:
            if hit.get("type") == "step":
                steps.extend(hit.get("items", []))
            elif hit.get("type") == "command":
                commands.append(
                    {
                        "command": hit.get("command", ""),
                        "purpose": hit.get("purpose", ""),
                        "risk": hit.get("risk", ""),
                        "source": hit.get("chunk_id", ""),
                    }
                )
            elif hit.get("type") == "verification":
                verification.extend(hit.get("items", []))
            elif hit.get("type") == "note":
                cautions.extend(hit.get("items", []))
            if "software-catalog" in hit.get("tags", []) or "软件库路径" in str(hit.get("content", "")):
                for line in str(hit.get("content", "")).splitlines():
                    line = line.strip()
                    if "软件库路径：" in line or "页面入口" in line:
                        references.append(line.lstrip("- ").strip())
        if doc:
            if len(steps) < 3:
                steps.extend(doc.get("steps", [])[:8])
            if len(verification) < 2:
                verification.extend(doc.get("verification", [])[:4])
            if len(cautions) < 2:
                cautions.extend(doc.get("notes", [])[:4])
            if len(commands) < 3:
                for item in doc.get("commands", [])[:6]:
                    if isinstance(item, dict):
                        commands.append(
                            {
                                "command": item.get("command", ""),
                                "purpose": item.get("purpose", ""),
                                "risk": item.get("risk", ""),
                                "source": doc_id,
                            }
                        )

    def unique(values: list[str], limit: int) -> list[str]:
        result = []
        seen = set()
        for value in values:
            value = str(value).strip()
            if value and value not in seen:
                seen.add(value)
                result.append(value)
            if len(result) >= limit:
                break
        return result

    unique_commands = []
    seen_commands = set()
    for item in commands:
        command = item.get("command", "").strip()
        if command and command not in seen_commands:
            seen_commands.add(command)
            unique_commands.append(item)
        if len(unique_commands) >= 8:
            break

    if not hits:
        summary = "未召回到足够相关的知识块，建议补充故障对象、报错文本、系统名称或告警规则名。"
    else:
        top = hits[0]
        summary = f"优先参考《{top.get('doc_title', '')}》中的{top.get('title', '相关步骤')}。"

    if hits and references:
        top = hits[0]
        summary = f"已召回软件库下载参考，优先查看《{top.get('doc_title', '')}》中的软件库路径。"

    return {
        "summary": summary,
        "suggested_steps": unique(references + steps, 10),
        "commands": unique_commands,
        "verification": unique(verification, 6),
        "cautions": unique(cautions, 6),
        "references": unique(references, 10),
        "sources": sources,
        "retrieved_chunks": hits,
    }
