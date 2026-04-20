from __future__ import annotations

import argparse
import json
from pathlib import Path

from recommend_from_ticket import DEFAULT_INDEX


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "kb-chunks.json"


SECTION_TITLES = {
    "overview": "适用范围与现象",
    "step": "处理步骤",
    "command": "常用指令",
    "verification": "验证方式",
    "note": "注意事项",
}


def clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def command_text(item: dict | str) -> tuple[str, str, str]:
    if isinstance(item, dict):
        return (
            clean_text(item.get("command")),
            clean_text(item.get("purpose")),
            clean_text(item.get("risk") or "低"),
        )
    return clean_text(item), "", "低"


def base_chunk(doc: dict, chunk_type: str, ordinal: int) -> dict:
    chunk_id = f"{doc['doc_id']}#{chunk_type}-{ordinal:03d}"
    return {
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "doc_title": doc.get("title", ""),
        "title": SECTION_TITLES.get(chunk_type, chunk_type),
        "type": chunk_type,
        "ordinal": ordinal,
        "status": doc.get("status", ""),
        "path": doc.get("path", ""),
        "asset_types": doc.get("asset_types", []),
        "systems": doc.get("systems", []),
        "issue_types": doc.get("issue_types", []),
        "tags": doc.get("tags", []),
        "keywords": doc.get("keywords", []),
        "risk_level": doc.get("risk_level", ""),
        "review_required": bool(doc.get("review_required", False)),
    }


def chunk_search_text(doc: dict, title: str, content: str, extra: str = "") -> str:
    parts = [
        doc.get("title", ""),
        title,
        " ".join(doc.get("keywords", [])),
        " ".join(doc.get("asset_types", [])),
        " ".join(doc.get("systems", [])),
        " ".join(doc.get("issue_types", [])),
        " ".join(doc.get("tags", [])),
        content,
        extra,
    ]
    return "\n".join(part for part in parts if part)


def build_chunks_for_doc(doc: dict) -> list[dict]:
    chunks: list[dict] = []

    overview_items = []
    overview_items.extend(clean_text(item) for item in doc.get("applicability", []))
    overview_items.extend(clean_text(item) for item in doc.get("symptoms", []))
    overview_items = [item for item in overview_items if item]
    if overview_items:
        chunk = base_chunk(doc, "overview", 1)
        content = "\n".join(f"- {item}" for item in overview_items)
        chunk.update(
            {
                "title": f"{doc.get('title', '')} - 适用范围与现象",
                "content": content,
                "items": overview_items,
                "search_text": chunk_search_text(doc, chunk["title"], content),
            }
        )
        chunks.append(chunk)

    for idx, step in enumerate(doc.get("steps", []), start=1):
        step = clean_text(step)
        if not step:
            continue
        chunk = base_chunk(doc, "step", idx)
        title = f"{doc.get('title', '')} - 第 {idx} 步"
        content = f"{idx}. {step}"
        chunk.update(
            {
                "title": title,
                "content": content,
                "items": [step],
                "search_text": chunk_search_text(doc, title, content),
            }
        )
        chunks.append(chunk)

    for idx, item in enumerate(doc.get("commands", []), start=1):
        command, purpose, risk = command_text(item)
        if not command:
            continue
        chunk = base_chunk(doc, "command", idx)
        title = f"{doc.get('title', '')} - 指令 {idx}"
        parts = [command]
        if purpose:
            parts.append(f"用途：{purpose}")
        if risk:
            parts.append(f"风险：{risk}")
        content = "\n".join(parts)
        chunk.update(
            {
                "title": title,
                "content": content,
                "command": command,
                "purpose": purpose,
                "risk": risk,
                "items": [command],
                "search_text": chunk_search_text(doc, title, content, purpose),
            }
        )
        chunks.append(chunk)

    for idx, item in enumerate(doc.get("verification", []), start=1):
        item = clean_text(item)
        if not item:
            continue
        chunk = base_chunk(doc, "verification", idx)
        title = f"{doc.get('title', '')} - 验证 {idx}"
        content = f"- {item}"
        chunk.update(
            {
                "title": title,
                "content": content,
                "items": [item],
                "search_text": chunk_search_text(doc, title, content),
            }
        )
        chunks.append(chunk)

    for idx, item in enumerate(doc.get("notes", []), start=1):
        item = clean_text(item)
        if not item:
            continue
        chunk = base_chunk(doc, "note", idx)
        title = f"{doc.get('title', '')} - 注意事项 {idx}"
        content = f"- {item}"
        chunk.update(
            {
                "title": title,
                "content": content,
                "items": [item],
                "search_text": chunk_search_text(doc, title, content),
            }
        )
        chunks.append(chunk)

    if not chunks and doc.get("content_preview"):
        chunk = base_chunk(doc, "overview", 1)
        content = clean_text(doc.get("content_preview"))
        chunk.update(
            {
                "title": f"{doc.get('title', '')} - 摘要",
                "content": content,
                "items": [content],
                "search_text": chunk_search_text(doc, chunk["title"], content),
            }
        )
        chunks.append(chunk)

    return chunks


def build_chunks(index: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    for doc in index:
        chunks.extend(build_chunks_for_doc(doc))
    return chunks


def main() -> int:
    parser = argparse.ArgumentParser(description="Build chunk-level KB records from the document index.")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    index = json.loads(args.index.read_text(encoding="utf-8"))
    chunks = build_chunks(index)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Chunked {len(index)} documents into {len(chunks)} chunks -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
