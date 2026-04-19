from __future__ import annotations

import hashlib
import math
import re
from collections import Counter


DEFAULT_DIMENSIONS = 2048
DEFAULT_NGRAM_RANGE = (2, 4)


def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize_for_vector(text: str, ngram_range: tuple[int, int] = DEFAULT_NGRAM_RANGE) -> list[str]:
    text = normalize_text(text)
    compact_cn = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9+#.]+", "", text)
    tokens: list[str] = []

    for token in re.findall(r"[A-Za-z][A-Za-z0-9+#.]{1,}", text):
        tokens.append(token)

    min_n, max_n = ngram_range
    for n in range(min_n, max_n + 1):
        if len(compact_cn) < n:
            continue
        tokens.extend(compact_cn[i : i + n] for i in range(len(compact_cn) - n + 1))

    return tokens


def stable_hash(value: str) -> int:
    digest = hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big", signed=False)


def vectorize_text(text: str, dimensions: int = DEFAULT_DIMENSIONS) -> dict[str, float]:
    counts = Counter(tokenize_for_vector(text))
    if not counts:
        return {}

    vector: dict[int, float] = {}
    for token, count in counts.items():
        bucket = stable_hash(token) % dimensions
        weight = 1.0 + math.log(count)
        vector[bucket] = vector.get(bucket, 0.0) + weight

    norm = math.sqrt(sum(value * value for value in vector.values()))
    if norm == 0:
        return {}
    return {str(bucket): round(value / norm, 8) for bucket, value in vector.items()}


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0

    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(key, 0.0) for key, value in left.items())


def join_doc_text(doc: dict) -> str:
    command_text = []
    for item in doc.get("commands", []):
        if isinstance(item, dict):
            command_text.append(" ".join(str(item.get(key, "")) for key in ["command", "purpose", "risk"]))
        else:
            command_text.append(str(item))

    parts = [
        doc.get("title", ""),
        " ".join(str(item) for item in doc.get("keywords", [])),
        " ".join(str(item) for item in doc.get("asset_types", [])),
        " ".join(str(item) for item in doc.get("systems", [])),
        " ".join(str(item) for item in doc.get("issue_types", [])),
        " ".join(str(item) for item in doc.get("tags", [])),
        " ".join(str(item) for item in doc.get("applicability", [])),
        " ".join(str(item) for item in doc.get("symptoms", [])),
        " ".join(str(item) for item in doc.get("steps", [])),
        " ".join(command_text),
        " ".join(str(item) for item in doc.get("verification", [])),
        " ".join(str(item) for item in doc.get("notes", [])),
        doc.get("content_preview", ""),
        doc.get("search_text", ""),
    ]
    return "\n".join(part for part in parts if part)


def build_vector_records(index: list[dict], dimensions: int = DEFAULT_DIMENSIONS) -> list[dict]:
    records = []
    for doc in index:
        records.append(
            {
                "doc_id": doc["doc_id"],
                "vector": vectorize_text(join_doc_text(doc), dimensions=dimensions),
            }
        )
    return records


def vector_search(
    index: list[dict],
    query: str,
    vector_records: list[dict] | None = None,
    top_k: int = 5,
    dimensions: int = DEFAULT_DIMENSIONS,
) -> list[dict]:
    query_vector = vectorize_text(query, dimensions=dimensions)
    if not query_vector:
        return []

    records = vector_records or build_vector_records(index, dimensions=dimensions)
    by_doc_id = {doc["doc_id"]: doc for doc in index}
    scored = []
    for record in records:
        score = cosine_similarity(query_vector, record.get("vector", {}))
        if score <= 0:
            continue
        doc = by_doc_id.get(record["doc_id"])
        if not doc:
            continue
        scored.append(
            {
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "status": doc.get("status", ""),
                "path": doc["path"],
                "vector_score": round(score, 4),
            }
        )

    scored.sort(key=lambda item: (-item["vector_score"], item["title"]))
    return scored[:top_k]
