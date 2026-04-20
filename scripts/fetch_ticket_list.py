from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from urllib import parse, request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://whops.craneweihua.com/api/w8t/ticket/list"
DEFAULT_OUTPUT = ROOT / "data" / "real-ticket-list.json"


def request_page(base_url: str, token: str, page: int, size: int, status: str, timeout: int) -> dict:
    query = parse.urlencode({"page": page, "size": size, "status": status})
    req = request.Request(
        f"{base_url}?{query}",
        method="GET",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "Referer": "https://whops.craneweihua.com/ticket",
            "TenantID": "default",
            "User-Agent": "ops-kb-real-ticket-eval/1.0",
        },
    )
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_items(payload: dict) -> list[dict]:
    candidates = [
        payload.get("data"),
        payload.get("result"),
        payload.get("rows"),
        payload.get("list"),
    ]
    for candidate in candidates:
        if isinstance(candidate, list):
            return candidate
        if not isinstance(candidate, dict):
            continue
        for key in ["list", "rows", "records", "items", "content", "data"]:
            value = candidate.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                nested = find_items(value)
                if nested:
                    return nested
    return []


def find_total(payload: dict) -> int | None:
    stack = [payload]
    while stack:
        item = stack.pop()
        if not isinstance(item, dict):
            continue
        for key in ["total", "count", "totalCount", "total_count"]:
            value = item.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, str) and value.isdigit():
                return int(value)
        stack.extend(value for value in item.values() if isinstance(value, dict))
    return None


def fetch_all(base_url: str, token: str, size: int, status: str, max_pages: int, timeout: int, sleep: float) -> dict:
    pages = []
    tickets = []
    total = None
    for page in range(1, max_pages + 1):
        payload = request_page(base_url, token, page, size, status, timeout)
        items = find_items(payload)
        if total is None:
            total = find_total(payload)
        pages.append({"page": page, "item_count": len(items), "raw": payload})
        tickets.extend(items)
        if not items:
            break
        if total is not None and len(tickets) >= total:
            break
        if len(items) < size and total is None:
            break
        if sleep > 0:
            time.sleep(sleep)
    return {
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "base_url": base_url,
        "status": status,
        "page_size": size,
        "reported_total": total,
        "ticket_count": len(tickets),
        "tickets": tickets,
        "pages": [{"page": p["page"], "item_count": p["item_count"]} for p in pages],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch ticket list pages from WatchAlert ticket API.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--status", default="")
    parser.add_argument("--max-pages", type=int, default=200)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--sleep", type=float, default=0.05)
    args = parser.parse_args()

    token = os.environ.get("WHOPS_TOKEN", "").strip()
    if not token:
        raise SystemExit("WHOPS_TOKEN environment variable is required.")

    result = fetch_all(args.base_url, token, args.size, args.status, args.max_pages, args.timeout, args.sleep)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["fetched_at", "reported_total", "ticket_count", "pages"]}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
