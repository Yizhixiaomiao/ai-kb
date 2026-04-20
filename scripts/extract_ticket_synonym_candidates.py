from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from recommend_from_ticket import compact, keyword_hit, normalize


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TICKETS = ROOT / "工单报修历史记录.csv"
DEFAULT_SYNONYMS = ROOT / "taxonomy" / "query-synonyms.json"
DEFAULT_REPORT = ROOT / "reports" / "ticket-synonym-candidates.md"


STOP_PHRASES = {
    "处理",
    "问题",
    "用户",
    "办公室",
    "车间",
    "电脑",
    "报修",
    "小程序",
    "default",
    "已解决",
    "正常",
    "进行",
    "无法",
    "需要",
    "重新",
}


def read_tickets(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_synonyms(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def ticket_text(row: dict) -> str:
    return "\n".join(str(row.get(key) or "") for key in ["问题描述", "解决步骤"])


def count_synonym_hits(rows: list[dict], groups: list[dict]) -> tuple[dict[str, int], dict[str, Counter]]:
    group_hits: dict[str, int] = defaultdict(int)
    alias_hits: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        text = ticket_text(row)
        text_norm = normalize(text)
        text_compact = compact(text)
        for group in groups:
            group_id = group.get("id") or group.get("canonical") or "unknown"
            terms = [group.get("canonical", "")]
            terms.extend(group.get("aliases", []))
            matched_group = False
            for term in terms:
                if keyword_hit(str(term), text_norm, text_compact):
                    alias_hits[group_id][str(term)] += 1
                    matched_group = True
            if matched_group:
                group_hits[group_id] += 1
    return dict(group_hits), alias_hits


def extract_frequent_phrases(rows: list[dict], limit: int = 120) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for row in rows:
        text = re.sub(r"[A-Za-z0-9_@./:-]+", " ", ticket_text(row))
        text = re.sub(r"[^\u4e00-\u9fff]+", " ", text)
        for segment in text.split():
            if len(segment) < 2:
                continue
            max_len = min(6, len(segment))
            for size in range(2, max_len + 1):
                for idx in range(0, len(segment) - size + 1):
                    phrase = segment[idx : idx + size]
                    if phrase in STOP_PHRASES:
                        continue
                    if any(stop in phrase for stop in ["车间", "办公室", "厂区", "用户"]):
                        continue
                    counter[phrase] += 1
    return [(phrase, count) for phrase, count in counter.most_common(limit) if count >= 3]


def write_report(rows: list[dict], groups: list[dict], report: Path) -> None:
    group_hits, alias_hits = count_synonym_hits(rows, groups)
    frequent = extract_frequent_phrases(rows)
    matched_ticket_count = 0
    for row in rows:
        text = ticket_text(row)
        text_norm = normalize(text)
        text_compact = compact(text)
        if any(
            keyword_hit(str(term), text_norm, text_compact)
            for group in groups
            for term in [group.get("canonical", ""), *group.get("aliases", [])]
        ):
            matched_ticket_count += 1

    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 历史工单口语词候选报告",
        "",
        f"- 历史工单数：{len(rows)}",
        f"- 同义词组数：{len(groups)}",
        f"- 至少命中一个同义词组的工单：{matched_ticket_count}",
        f"- 同义词覆盖率：{matched_ticket_count / max(len(rows), 1) * 100:.2f}%",
        "",
        "## 同义词组命中统计",
        "",
        "| 同义词组 | 命中工单数 | 高频别名 |",
        "| --- | ---: | --- |",
    ]
    group_by_id = {group.get("id") or group.get("canonical") or "unknown": group for group in groups}
    for group_id, count in sorted(group_hits.items(), key=lambda item: (-item[1], item[0])):
        top_aliases = "、".join(f"{alias}({num})" for alias, num in alias_hits[group_id].most_common(8))
        label = group_by_id.get(group_id, {}).get("canonical", group_id)
        lines.append(f"| {label} | {count} | {top_aliases} |")

    lines.extend(["", "## 高频短语候选", ""])
    lines.extend(["| 短语 | 出现次数 |", "| --- | ---: |"])
    for phrase, count in frequent:
        lines.append(f"| {phrase} | {count} |")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract synonym coverage and frequent phrase candidates from ticket history.")
    parser.add_argument("--tickets", type=Path, default=DEFAULT_TICKETS)
    parser.add_argument("--synonyms", type=Path, default=DEFAULT_SYNONYMS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = read_tickets(args.tickets)
    groups = load_synonyms(args.synonyms)
    write_report(rows, groups, args.report)
    print(f"Wrote synonym candidate report -> {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
