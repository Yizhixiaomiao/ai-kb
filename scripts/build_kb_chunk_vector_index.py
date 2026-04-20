from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_kb_chunks import DEFAULT_OUTPUT as DEFAULT_CHUNKS
from vector_model import DEFAULT_DIMENSIONS, vectorize_text


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "kb-chunk-vector-index.json"


def build_chunk_vector_records(chunks: list[dict], dimensions: int = DEFAULT_DIMENSIONS) -> list[dict]:
    records = []
    for chunk in chunks:
        records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "doc_id": chunk["doc_id"],
                "vector": vectorize_text(chunk.get("search_text") or chunk.get("content", ""), dimensions=dimensions),
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local sparse vector index for KB chunks.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS)
    args = parser.parse_args()

    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    records = build_chunk_vector_records(chunks, dimensions=args.dimensions)
    body = {
        "model": "local-char-ngram-hash-v1",
        "dimensions": args.dimensions,
        "chunks": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Vector indexed {len(records)} chunks -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
