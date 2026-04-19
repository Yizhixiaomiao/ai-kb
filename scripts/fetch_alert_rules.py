from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from recommend_from_ticket import DEFAULT_INDEX, recommend
from vector_model import build_vector_records


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://whops.craneweihua.com"
DEFAULT_OUTPUT_JSON = ROOT / "data" / "alert-rules.json"
DEFAULT_OUTPUT_CSV = ROOT / "reports" / "alert-rule-kb-matching.csv"
DEFAULT_OUTPUT_MD = ROOT / "reports" / "alert-rule-kb-matching.md"


def request_json(base_url: str, path: str, params: dict, token: str, tenant_id: str) -> dict:
    url = f"{base_url.rstrip('/')}{path}?{urlencode(params)}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "TenantID": tenant_id,
            "User-Agent": "ops-kb-alert-rule-import/1.0",
        },
        method="GET",
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_items(body: dict) -> list[dict]:
    candidates = [
        body.get("data", {}).get("list") if isinstance(body.get("data"), dict) else None,
        body.get("data", {}).get("items") if isinstance(body.get("data"), dict) else None,
        body.get("data") if isinstance(body.get("data"), list) else None,
        body.get("list"),
        body.get("items"),
    ]
    for candidate in candidates:
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, dict)]
    return []


def extract_total(body: dict, fallback: int) -> int:
    if isinstance(body.get("data"), dict):
        for key in ["total", "count"]:
            value = body["data"].get(key)
            if isinstance(value, int):
                return value
    for key in ["total", "count"]:
        value = body.get(key)
        if isinstance(value, int):
            return value
    return fallback


def first_value(item: dict, keys: list[str]) -> str:
    for key in keys:
        value = item.get(key)
        if value is not None:
            return str(value)
    return ""


def clean_alert_rule_name(name: str) -> str:
    text = name or ""
    text = text.replace("_", " ")
    for token in ["WMS", "MES", "PLM", "NC", "AI", "卫华", "江苏", "项目", "应用"]:
        text = text.replace(token, " ")
    return " ".join(text.split())


def fetch_paginated(base_url: str, path: str, params: dict, token: str, tenant_id: str, page_size: int) -> list[dict]:
    all_items: list[dict] = []
    page = 1
    while True:
        page_params = dict(params)
        page_params["index"] = page
        page_params["size"] = page_size
        body = request_json(base_url, path, page_params, token, tenant_id)
        items = extract_items(body)
        all_items.extend(items)
        total = extract_total(body, len(all_items))
        if not items or len(all_items) >= total or len(items) < page_size:
            break
        page += 1
    return all_items


def fetch_alert_rules(base_url: str, token: str, tenant_id: str, page_size: int) -> dict:
    groups = fetch_paginated(
        base_url,
        "/api/w8t/ruleGroup/ruleGroupList",
        {},
        token,
        tenant_id,
        page_size,
    )

    result_groups = []
    for group in groups:
        group_id = first_value(group, ["ruleGroupId", "id", "groupId"])
        group_name = first_value(group, ["ruleGroupName", "name", "groupName"])
        if not group_id:
            continue
        rules = fetch_paginated(
            base_url,
            "/api/w8t/rule/ruleList",
            {"status": "all", "ruleGroupId": group_id},
            token,
            tenant_id,
            page_size,
        )
        result_groups.append(
            {
                "ruleGroupId": group_id,
                "ruleGroupName": group_name,
                "raw": group,
                "rules": rules,
            }
        )

    return {"groups": result_groups}


def rule_text(rule: dict, group_name: str) -> str:
    rule_name = first_value(rule, ["ruleName", "name", "alertName"])
    parts = [
        clean_alert_rule_name(rule_name),
        first_value(rule, ["description", "remark", "summary"]),
        first_value(rule, ["expr", "promQL", "query", "promql"]),
        first_value(rule, ["severity", "level", "priority"]),
    ]
    labels = rule.get("labels")
    if isinstance(labels, dict):
        parts.extend(f"{key}:{value}" for key, value in labels.items())
    return "\n".join(part for part in parts if part)


def match_rules(alert_rules: dict, index: list[dict], top_k: int, mode: str) -> list[dict]:
    vector_records = build_vector_records(index) if mode in {"vector", "hybrid"} else None
    rows = []
    for group in alert_rules["groups"]:
        group_name = group["ruleGroupName"]
        for rule in group["rules"]:
            rule_id = first_value(rule, ["ruleId", "id"])
            rule_name = first_value(rule, ["ruleName", "name", "alertName"])
            text = rule_text(rule, group_name)
            recommendations = recommend(index, text, top_k=top_k, mode=mode, vector_records=vector_records)
            top = recommendations[0] if recommendations else {}
            rows.append(
                {
                    "ruleGroupId": group["ruleGroupId"],
                    "ruleGroupName": group_name,
                    "ruleId": rule_id,
                    "ruleName": rule_name,
                    "matched": "yes" if recommendations else "no",
                    "topDocId": top.get("doc_id", ""),
                    "topTitle": top.get("title", ""),
                    "score": top.get("score", ""),
                    "ruleScore": top.get("rule_score", ""),
                    "vectorScore": top.get("vector_score", ""),
                    "reason": "；".join(top.get("reason", [])),
                    "recommendations": recommendations,
                }
            )
    return rows


def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "ruleGroupId",
        "ruleGroupName",
        "ruleId",
        "ruleName",
        "matched",
        "topDocId",
        "topTitle",
        "score",
        "ruleScore",
        "vectorScore",
        "reason",
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_summary(rows: list[dict], output: Path) -> None:
    matched = [row for row in rows if row["matched"] == "yes"]
    lines = [
        "# 告警规则与知识库匹配报告",
        "",
        "本报告根据告警规则 `ruleName`、规则组名称、描述、表达式和标签，在本地知识库中做混合推荐匹配。",
        "",
        "## 总览",
        "",
        f"- 告警规则数：{len(rows)}",
        f"- 有推荐结果：{len(matched)}",
        f"- 无推荐结果：{len(rows) - len(matched)}",
        f"- 匹配率：{(len(matched) / len(rows) * 100):.1f}%" if rows else "- 匹配率：0.0%",
        "",
        "## Top 匹配样例",
        "",
    ]
    for row in sorted(matched, key=lambda item: int(item["score"] or 0), reverse=True)[:30]:
        lines.append(
            f"- `{row['ruleName']}` -> `{row['topDocId']}`，综合 {row['score']}，规则 {row['ruleScore']}，向量 {row['vectorScore']}"
        )
    lines.extend(["", "## 未匹配规则样例", ""])
    for row in [row for row in rows if row["matched"] != "yes"][:30]:
        lines.append(f"- `{row['ruleName']}`（规则组：{row['ruleGroupName']}）")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch WatchAlert rules and match them to local KB documents.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--tenant-id", default=os.environ.get("WHOPS_TENANT_ID", "default"))
    parser.add_argument("--token-env", default="WHOPS_TOKEN")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--mode", choices=["rules", "vector", "hybrid"], default="hybrid")
    parser.add_argument("--skip-fetch", action="store_true", help="Use existing output-json instead of calling remote APIs.")
    args = parser.parse_args()

    token = os.environ.get(args.token_env)
    if not token and not args.skip_fetch:
        print(f"Missing token. Set ${args.token_env} before running this script.", file=sys.stderr)
        return 2

    if args.skip_fetch:
        alert_rules = json.loads(args.output_json.read_text(encoding="utf-8"))
    else:
        alert_rules = fetch_alert_rules(args.base_url, token or "", args.tenant_id, args.page_size)
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(alert_rules, ensure_ascii=False, indent=2), encoding="utf-8")

    index = json.loads(args.index.read_text(encoding="utf-8"))
    rows = match_rules(alert_rules, index, top_k=args.top_k, mode=args.mode)
    write_csv(rows, args.output_csv)
    write_summary(rows, args.output_md)
    print(f"Groups: {len(alert_rules['groups'])}")
    print(f"Rules: {len(rows)}")
    print(f"CSV: {args.output_csv}")
    print(f"Summary: {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
