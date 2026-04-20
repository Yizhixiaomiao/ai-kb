from __future__ import annotations

import argparse
import html
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(r"D:\新建文件夹\业务维护清单")
DEFAULT_OUTPUT = ROOT / "docs" / "source-documents"
DEFAULT_REPORT = ROOT / "reports" / "source-document-import-report.md"


SUPPORTED_EXTENSIONS = {".docx", ".xlsx", ".txt", ".md"}
SENSITIVE_NAME_TERMS = [
    "账号密码",
    "密码",
    "访问信息",
    "服务器清单",
    "服务器IP",
    "部署信息",
    "环境部署信息",
    "license",
    "密钥",
    "key",
]

NS_WORD = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
NS_XLSX = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return value or "source-document"


def infer_domain(relative: Path) -> str:
    parts = list(relative.parts)
    if len(parts) > 1:
        return slugify(parts[0])
    name = relative.stem.lower()
    mapping = {
        "AD": ["ad", "域", "active"],
        "DLP": ["dlp", "防泄密"],
        "KMS": ["kms"],
        "MES": ["mes"],
        "NC": ["nc"],
        "OA": ["oa"],
        "PLM": ["plm"],
        "PO": ["po", "pi"],
        "S4": ["s4", "hana", "sap"],
        "SRM": ["srm"],
        "U8": ["u8"],
        "WMS": ["wms"],
        "vSphere": ["vsphere", "虚拟化"],
        "backup": ["备份", "networker"],
        "storage": ["存储", "data domain", "分布式"],
    }
    for domain, terms in mapping.items():
        if any(term.lower() in name for term in terms):
            return slugify(domain)
    return "business-system"


def infer_tags(relative: Path, title: str) -> list[str]:
    text = f"{relative.as_posix()} {title}".lower()
    path_parts = [part.lower() for part in relative.with_suffix("").parts]
    tags = ["engineer-doc", "imported"]
    candidates = [
        "ad",
        "dlp",
        "hana",
        "kms",
        "mes",
        "nexus",
        "nc",
        "oa",
        "plm",
        "po",
        "rtx",
        "s4",
        "sap",
        "srm",
        "u8",
        "vsphere",
        "wms",
        "networker",
        "backup",
        "data-domain",
        "storage",
        "docker",
        "mysql",
        "oracle",
        "cloud-drive",
    ]
    aliases = {
        "data-domain": ["data domain"],
        "cloud-drive": ["云盘"],
        "storage": ["存储"],
        "backup": ["备份"],
    }
    for tag in candidates:
        terms = aliases.get(tag, [tag])
        matched = False
        for term in terms:
            term_lower = term.lower()
            if term_lower in path_parts:
                matched = True
                break
            if re.fullmatch(r"[a-z0-9-]{1,3}", term_lower):
                if re.search(rf"(^|[^a-z0-9]){re.escape(term_lower)}([^a-z0-9]|$)", text):
                    matched = True
                    break
            elif term_lower in text:
                matched = True
                break
        if matched:
            tags.append(tag)
    return list(dict.fromkeys(tags))


def is_sensitive_path(path: Path) -> bool:
    text = path.as_posix().lower()
    return any(term.lower() in text for term in SENSITIVE_NAME_TERMS)


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def redact(text: str) -> str:
    text = re.sub(r"(?i)(password|passwd|pwd|密码)\s*[:=：]\s*([^\s,，;；]+)", r"\1=<已脱敏>", text)
    text = re.sub(r"(?i)(token|secret|密钥)\s*[:=：]\s*([^\s,，;；]+)", r"\1=<已脱敏>", text)
    text = re.sub(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)", "<IP地址已脱敏>", text)
    text = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "<手机号已脱敏>", text)
    return text


def read_docx(path: Path, max_chars: int) -> str:
    lines: list[str] = []
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
        for node in root.findall(".//w:body/*", NS_WORD):
            tag = node.tag.rsplit("}", 1)[-1]
            if tag == "p":
                text = "".join(t.text or "" for t in node.findall(".//w:t", NS_WORD)).strip()
                if text:
                    lines.append(text)
            elif tag == "tbl":
                for row in node.findall(".//w:tr", NS_WORD):
                    cells = []
                    for cell in row.findall("./w:tc", NS_WORD):
                        value = "".join(t.text or "" for t in cell.findall(".//w:t", NS_WORD)).strip()
                        cells.append(clean_cell(value))
                    if any(cells):
                        lines.append("| " + " | ".join(cells) + " |")
            if sum(len(line) for line in lines) >= max_chars:
                lines.append("（内容较长，已按导入长度限制截断。）")
                break
    return "\n\n".join(lines)


def xlsx_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    values = []
    for si in root.findall("a:si", NS_XLSX):
        values.append("".join(t.text or "" for t in si.findall(".//a:t", NS_XLSX)))
    return values


def xlsx_sheet_names(zf: zipfile.ZipFile) -> list[str]:
    if "xl/workbook.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/workbook.xml"))
    return [node.attrib.get("name", "") for node in root.findall(".//a:sheet", NS_XLSX)]


def read_xlsx(path: Path, max_rows_per_sheet: int, max_chars: int) -> str:
    lines = []
    with zipfile.ZipFile(path) as zf:
        shared = xlsx_shared_strings(zf)
        names = xlsx_sheet_names(zf)
        sheet_paths = sorted(name for name in zf.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name))
        for sheet_idx, sheet_path in enumerate(sheet_paths, start=1):
            sheet_name = names[sheet_idx - 1] if sheet_idx - 1 < len(names) else f"Sheet{sheet_idx}"
            lines.append(f"## {sheet_name}")
            root = ET.fromstring(zf.read(sheet_path))
            count = 0
            for row in root.findall(".//a:row", NS_XLSX):
                cells = []
                for cell in row.findall("a:c", NS_XLSX):
                    value_node = cell.find("a:v", NS_XLSX)
                    value = value_node.text if value_node is not None and value_node.text else ""
                    if cell.attrib.get("t") == "s" and value.isdigit():
                        idx = int(value)
                        value = shared[idx] if idx < len(shared) else value
                    cells.append(clean_cell(value))
                if any(cells):
                    lines.append("| " + " | ".join(cells) + " |")
                    count += 1
                if count >= max_rows_per_sheet:
                    lines.append("（表格较长，已按导入行数限制截断。）")
                    break
            if sum(len(line) for line in lines) >= max_chars:
                lines.append("（内容较长，已按导入长度限制截断。）")
                break
    return "\n\n".join(lines)


def read_text_file(path: Path, max_chars: int) -> str:
    for encoding in ["utf-8-sig", "utf-8", "gb18030"]:
        try:
            text = path.read_text(encoding=encoding)
            return text[:max_chars]
        except UnicodeDecodeError:
            continue
    return ""


def title_from_path(path: Path) -> str:
    return path.stem.strip() or "正式文档"


def write_imported_doc(source_root: Path, output_root: Path, source: Path, content: str) -> Path:
    relative = source.relative_to(source_root)
    title = title_from_path(source)
    domain = infer_domain(relative)
    tags = infer_tags(relative, title)
    target_dir = output_root / domain
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{slugify(relative.with_suffix('').as_posix())}.md"
    body = f"""# {title}

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [{domain}]
issue_types: [reference]
tags: [{", ".join(tags)}]
source_path: "{redact(str(source))}"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：{redact(str(source.name))}
- 原始路径：{redact(str(source.parent))}
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

{redact(content).strip()}
"""
    target.write_text(body, encoding="utf-8")
    return target


def import_documents(
    source_root: Path,
    output_root: Path,
    max_file_mb: int,
    max_chars: int,
    max_rows_per_sheet: int,
) -> tuple[list[dict], list[dict]]:
    imported = []
    skipped = []
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        relative = path.relative_to(source_root)
        if ext not in SUPPORTED_EXTENSIONS:
            skipped.append({"path": str(relative), "reason": f"unsupported extension {ext or '<none>'}"})
            continue
        if is_sensitive_path(relative):
            skipped.append({"path": str(relative), "reason": "sensitive filename"})
            continue
        size_mb = path.stat().st_size / 1024 / 1024
        if size_mb > max_file_mb:
            skipped.append({"path": str(relative), "reason": f"too large {size_mb:.1f}MB"})
            continue
        try:
            if ext == ".docx":
                content = read_docx(path, max_chars=max_chars)
            elif ext == ".xlsx":
                content = read_xlsx(path, max_rows_per_sheet=max_rows_per_sheet, max_chars=max_chars)
            else:
                content = read_text_file(path, max_chars=max_chars)
        except Exception as exc:
            skipped.append({"path": str(relative), "reason": f"parse failed: {exc}"})
            continue
        if len(compact_text(content)) < 20:
            skipped.append({"path": str(relative), "reason": "no useful text"})
            continue
        target = write_imported_doc(source_root, output_root, path, content)
        imported.append({"source": str(relative), "target": str(target.relative_to(ROOT)).replace("\\", "/"), "chars": len(content)})
    return imported, skipped


def compact_text(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def write_report(imported: list[dict], skipped: list[dict], report: Path) -> None:
    lines = [
        "# 正式文档导入报告",
        "",
        f"- 已导入：{len(imported)}",
        f"- 已跳过：{len(skipped)}",
        "",
        "## 已导入",
        "",
    ]
    for item in imported:
        lines.append(f"- {item['source']} -> `{item['target']}`（{item['chars']} 字符）")
    lines.extend(["", "## 已跳过", ""])
    for item in skipped:
        lines.append(f"- {item['path']}：{item['reason']}")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import engineer source documents into searchable Markdown records.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--max-file-mb", type=int, default=30)
    parser.add_argument("--max-chars", type=int, default=60000)
    parser.add_argument("--max-rows-per-sheet", type=int, default=80)
    args = parser.parse_args()

    imported, skipped = import_documents(
        args.source,
        args.output,
        max_file_mb=args.max_file_mb,
        max_chars=args.max_chars,
        max_rows_per_sheet=args.max_rows_per_sheet,
    )
    write_report(imported, skipped, args.report)
    print(json.dumps({"imported": len(imported), "skipped": len(skipped), "report": str(args.report)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
