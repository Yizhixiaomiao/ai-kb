from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_kb_index import DEFAULT_OUTPUT as DEFAULT_KB_INDEX
from vector_model import DEFAULT_DIMENSIONS, build_vector_records


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "kb-vector-index.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local sparse vector index for KB documents.")
    parser.add_argument("--index", type=Path, default=DEFAULT_KB_INDEX)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS)
    args = parser.parse_args()

    index = json.loads(args.index.read_text(encoding="utf-8"))
    records = build_vector_records(index, dimensions=args.dimensions)
    body = {
        "model": "local-char-ngram-hash-v1",
        "dimensions": args.dimensions,
        "documents": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Vector indexed {len(records)} documents -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
