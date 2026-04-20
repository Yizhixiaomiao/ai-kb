from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_API_URL = "http://soft.craneweihua.com/api/fs/list"
DEFAULT_PORTAL_URL = "http://soft.craneweihua.com/"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "source-documents" / "software"
DEFAULT_DATA = ROOT / "data" / "software-catalog.json"
DEFAULT_REPORT = ROOT / "reports" / "software-catalog-import-report.md"


CATEGORY_TAGS = {
    "浏览器": ["browser", "desktop-software", "浏览器", "浏览器安装包"],
    "输入法": ["input-method", "desktop-software", "输入法", "输入法安装包"],
    "打印机": ["printer", "driver", "打印机", "打印机驱动", "驱动下载"],
    "远程": ["remote-tool", "远程工具", "远程软件"],
    "即时通讯": ["im", "desktop-software", "即时通讯", "通讯工具"],
    "办公": ["office", "desktop-software", "办公软件", "Office", "WPS"],
    "系统镜像": ["os-image", "windows", "系统镜像", "Windows镜像"],
    "镜像": ["os-image", "镜像"],
    "SAP": ["sap", "sap-gui", "SAP GUI", "SAP客户端", "SAP安装包"],
    "激活": ["activation", "kms", "激活工具", "KMS"],
    "加域": ["domain-join", "ad", "加域工具", "域工具"],
    "加密": ["encryption-client", "dlp", "加密客户端", "加密软件"],
    "PLM": ["plm", "PLM客户端", "PLM安装包"],
    "保密": ["dlp", "保密软件"],
    "解压缩": ["archive-tool", "解压缩", "压缩软件"],
    "财务": ["finance-software", "财务软件"],
    "无线网卡": ["network-driver", "无线网卡驱动", "网卡驱动"],
    "Server": ["server", "服务器软件", "Server"],
    "MES": ["mes", "MES客户端", "MES安装包"],
    "网络认证": ["network-authentication", "网络认证客户端", "认证客户端"],
    "企业云盘": ["cloud-drive", "企业云盘", "云盘客户端"],
    "WMS": ["wms", "WMS客户端", "WMS安装包"],
    "群晖": ["nas", "synology", "群晖", "NAS"],
    "devops": ["devops"],
    "zabbix": ["zabbix", "monitoring"],
    "开发工具": ["developer-tool"],
    "脚本": ["script"],
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return value or "software"


def join_path(parent: str, name: str) -> str:
    if parent == "/":
        return "/" + name.strip("/")
    return parent.rstrip("/") + "/" + name.strip("/")


def parent_path(path: str) -> str:
    path = path.rstrip("/")
    if not path or path == "/":
        return "/"
    parent = path.rsplit("/", 1)[0]
    return parent or "/"


def top_category(path: str) -> str:
    parts = [part for part in path.strip("/").split("/") if part]
    return parts[0] if parts else "_root"


def format_size(size: int | str | None) -> str:
    try:
        value = int(size or 0)
    except (TypeError, ValueError):
        return ""
    if value <= 0:
        return ""
    units = ["B", "KB", "MB", "GB", "TB"]
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(amount)} {unit}"
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return str(value)


def list_dir(api_url: str, path: str, timeout: int) -> list[dict]:
    body = json.dumps(
        {"path": path, "password": "", "page": 1, "per_page": 0, "refresh": False},
        ensure_ascii=False,
    ).encode("utf-8")
    req = request.Request(
        api_url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": DEFAULT_PORTAL_URL.rstrip("/"),
            "Referer": DEFAULT_PORTAL_URL,
            "User-Agent": "ops-kb-software-catalog-importer/1.0",
        },
    )
    with request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("code") not in (200, "200", None):
        raise RuntimeError(f"API returned code={payload.get('code')} message={payload.get('message')}")
    data = payload.get("data") or {}
    content = data.get("content")
    if content is None:
        return []
    if not isinstance(content, list):
        raise RuntimeError(f"Unexpected content for {path}: {type(content).__name__}")
    return content


def fetch_catalog(api_url: str, max_dirs: int, max_depth: int, timeout: int) -> tuple[list[dict], list[dict], list[str]]:
    directories: list[dict] = []
    files: list[dict] = []
    errors: list[str] = []
    queue: deque[tuple[str, int]] = deque([("/", 0)])
    visited: set[str] = set()

    while queue:
        current, depth = queue.popleft()
        if current in visited:
            continue
        if len(visited) >= max_dirs:
            errors.append(f"达到目录数量上限 {max_dirs}，后续目录未继续读取。")
            break
        visited.add(current)
        try:
            items = list_dir(api_url, current, timeout)
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            errors.append(f"{current}: {exc}")
            continue

        for item in items:
            name = str(item.get("name") or "").strip()
            if not name:
                continue
            full_path = join_path(current, name)
            is_dir = bool(item.get("is_dir"))
            normalized = {
                "name": name,
                "path": full_path,
                "parent": current,
                "top_category": top_category(full_path) if is_dir or current != "/" else "_root",
                "size": item.get("size") or 0,
                "size_text": format_size(item.get("size")),
                "modified": item.get("modified") or "",
                "created": item.get("created") or "",
                "type": item.get("type") or "",
                "is_dir": is_dir,
            }
            if normalized["is_dir"]:
                directories.append(normalized)
                if depth < max_depth:
                    queue.append((full_path, depth + 1))
                else:
                    errors.append(f"{full_path}: 达到递归深度上限 {max_depth}，未继续读取。")
            else:
                files.append(normalized)

    directories.sort(key=lambda x: x["path"].lower())
    files.sort(key=lambda x: x["path"].lower())
    return directories, files, errors


def tags_for_category(category: str) -> list[str]:
    tags = ["software", "software-catalog", "installer", "软件下载", "安装包", "下载路径", "软件库路径"]
    if category != "_root":
        tags.append(category)
    text = category.lower()
    for key, values in CATEGORY_TAGS.items():
        if key.lower() in text:
            tags.extend(values)
    return list(dict.fromkeys(tags))


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def build_doc(category: str, files: list[dict], directories: list[dict], portal_url: str) -> str:
    title = "常用软件库目录" if category == "_root" else f"常用软件库目录 - {category}"
    tags = tags_for_category(category)
    systems = ["software-repository"]
    if "sap-gui" in tags:
        systems.append("sap")
    for system in ["plm", "mes", "wms", "zabbix"]:
        if system in tags:
            systems.append(system)

    lines = [
        f"# {title}",
        "",
        "```yaml",
        "status: imported",
        "type: software-catalog",
        "source: software-repository",
        "asset_types: [software, desktop, server]",
        f"systems: {yaml_list(list(dict.fromkeys(systems)))}",
        "issue_types: [software-installation, driver-installation, client-installation, download-reference]",
        f"tags: {yaml_list(tags)}",
        f'source_path: "{portal_url}"',
        'import_note: "只导入软件库目录元数据：文件名、路径、大小和更新时间；未下载文件，未解析压缩包或镜像内容。"',
        "```",
        "",
        "## 适用范围",
        "",
        "- 工程师处理软件安装、客户端重装、驱动安装、系统镜像、工具下载等工单时，快速定位公司常用软件库中的参考路径。",
        "- 本文档只提供软件库路径参考，不代表该安装包一定适用于所有电脑或服务器；安装前仍需确认系统版本、授权和业务影响。",
        "",
        "## 使用方式",
        "",
        f"- 页面入口：{portal_url}",
        "- 软件库路径：按下方条目中的路径进入对应目录下载。",
        "- 不确定版本时，优先选择目录中更新时间较新的版本，并结合工单场景确认。",
        "",
        "## 目录概览",
        "",
    ]

    child_dirs = [d for d in directories if d["top_category"] == category]
    if child_dirs:
        for item in child_dirs[:200]:
            lines.append(f"- `{item['path']}`")
        if len(child_dirs) > 200:
            lines.append(f"- 其余 {len(child_dirs) - 200} 个目录见结构化目录数据。")
    else:
        lines.append("- 无子目录。")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in files:
        grouped[parent_path(item["path"])].append(item)

    lines.extend(["", "## 文件路径清单", ""])
    if not files:
        lines.append("- 未发现文件。")
    for folder in sorted(grouped, key=str.lower):
        section_title = folder if folder != "/" else "根目录"
        lines.extend(["", f"### {section_title}", ""])
        for item in grouped[folder]:
            detail = [f"软件库路径：`{item['path']}`", f"页面入口：{portal_url}"]
            if item.get("size_text"):
                detail.append(f"大小：{item['size_text']}")
            if item.get("modified"):
                detail.append(f"更新时间：{item['modified']}")
            lines.append(f"- {item['name']}。{'；'.join(detail)}。")

    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    directories: list[dict],
    files: list[dict],
    errors: list[str],
    output_dir: Path,
    data_path: Path,
    report_path: Path,
    portal_url: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("software-*.md"):
        stale.unlink()

    catalog = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "portal_url": portal_url,
        "directory_count": len(directories),
        "file_count": len(files),
        "directories": directories,
        "files": files,
        "errors": errors,
    }
    data_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

    grouped_files: dict[str, list[dict]] = defaultdict(list)
    grouped_dirs: dict[str, list[dict]] = defaultdict(list)
    for item in files:
        grouped_files[item["top_category"]].append(item)
    for item in directories:
        grouped_dirs[item["top_category"]].append(item)

    categories = sorted(set(grouped_files) | set(grouped_dirs), key=str.lower)
    written_docs = []
    for category in categories:
        filename = "software-root.md" if category == "_root" else f"software-{slugify(category)}.md"
        path = output_dir / filename
        path.write_text(
            build_doc(category, grouped_files.get(category, []), grouped_dirs.get(category, []), portal_url),
            encoding="utf-8",
        )
        written_docs.append(path)

    report_lines = [
        "# 软件目录导入报告",
        "",
        f"- 生成时间：{catalog['generated_at']}",
        f"- 页面入口：{portal_url}",
        f"- 目录数：{len(directories)}",
        f"- 文件数：{len(files)}",
        f"- 生成 Markdown：{len(written_docs)} 篇",
        f"- 结构化数据：`{data_path.relative_to(ROOT).as_posix()}`",
        "",
        "## 分类统计",
        "",
    ]
    for category in categories:
        report_lines.append(
            f"- {category}: {len(grouped_dirs.get(category, []))} 个目录，{len(grouped_files.get(category, []))} 个文件"
        )
    if errors:
        report_lines.extend(["", "## 读取异常", ""])
        report_lines.extend(f"- {item}" for item in errors)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Fetched {len(directories)} directories and {len(files)} files.")
    print(f"Wrote {len(written_docs)} Markdown documents -> {output_dir}")
    print(f"Wrote catalog data -> {data_path}")
    print(f"Wrote report -> {report_path}")
    if errors:
        print(f"Warnings: {len(errors)}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import software repository file list into the KB.")
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--portal-url", default=DEFAULT_PORTAL_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--max-dirs", type=int, default=2000)
    parser.add_argument("--max-depth", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    directories, files, errors = fetch_catalog(args.api_url, args.max_dirs, args.max_depth, args.timeout)
    write_outputs(directories, files, errors, args.output_dir, args.data, args.report, args.portal_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
