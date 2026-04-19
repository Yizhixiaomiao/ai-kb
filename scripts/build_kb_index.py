from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS_DIR = ROOT / "docs"
DEFAULT_OUTPUT = ROOT / "data" / "kb-index.json"


CURATED_KEYWORDS: dict[str, list[str]] = {
    "network-authentication-unavailable": [
        "没网",
        "没有网络",
        "没有网",
        "无网络",
        "连不上网",
        "无法联网",
        "网络不通",
        "连接不上网络",
        "无法连接网络",
        "上不上网",
        "网络认证",
        "认证问题",
        "重新认证",
        "认证过多",
        "认证助手",
        "mes登不上",
        "mes登录不上",
        "上不去网",
    ],
    "printer-not-working": ["无法打印", "打印不了", "无法正常打印", "连接不上打印机", "无法连接打印机", "打印机连接不上", "打印机没反应"],
    "printer-paper-jam": ["打印机卡纸", "卡纸", "取不出来", "进纸口卡纸"],
    "pc-boot-failed": ["无法开机", "开不了机", "打不开机", "不开机", "不通电", "主机开不开机"],
    "black-screen-desktop-not-shown": ["黑屏", "鼠标光标可见", "桌面不显示", "explorer.exe"],
    "pc-performance-slow": ["电脑卡顿", "电脑卡", "电脑很慢", "反应慢", "卡顿", "卡死", "配置低", "cpu占用"],
    "disk-c-drive-full": ["c盘空间不足", "c盘可用空间过小", "c盘储存满", "c盘满", "c盘爆满", "系统盘满", "磁盘空间不足", "硬盘满"],
    "account-login-failed": ["无法登录", "登录异常", "登录不上", "登不上", "密码错误", "权限不足", "账号问题", "账户问题", "加域", "脱域", "域账户", "重置域账户"],
    "office-wps-document-open-failed": ["word打不开", "excel打不开", "ppt打不开", "office打不开", "wps打不开", "文档打不开", "文件打不开", "文件损坏"],
    "software-client-installation": ["安装软件", "安装客户端", "需要安装", "已安装", "重装软件", "重新安装", "软件安装"],
    "shared-file-cloud-drive-access": ["共享文件", "共享文件夹", "云盘", "上传不了", "下载不了", "文件找不到"],
    "shared-printer-connect-failed": ["共享打印机", "连接不上打印机", "无法连接打印机", "重新连接打印机", "连接打印机", "共享路径不通", "换办公室打印"],
    "printer-driver-install-failed": ["打印机驱动", "驱动故障", "驱动丢失", "安装驱动", "找不到驱动"],
    "printer-offline-or-paused": ["打印机脱机", "显示脱机", "打印机暂停", "打印机不打印", "队列", "接收到打印任务但是不打印"],
    "printer-paper-jam-feed-failed": ["卡纸", "进纸失败", "不出纸", "搓纸轮", "定影卡纸", "碎纸片"],
    "label-printer-paper-recognition": ["标签机", "标签打印", "库位码", "标识卡", "条码", "纸张不识别", "空白标签"],
    "scanner-preview-failed": ["扫描", "扫描后无法预览", "扫描件无法预览", "扫描仪驱动"],
    "print-port-deleted-by-security-software": ["打印端口", "端口被删除", "360删除打印端口", "安全软件打印"],
    "print-template-or-paper-size-error": ["打印模板", "纸张规格", "三联纸", "a4纸", "sap纸张", "发车清单", "打印格式"],
    "print-quality-faded-streaks-head-wear": [
        "打印不清楚",
        "打印机打印不清楚",
        "打印头磨损",
        "打印头",
        "针头磨损",
        "针头坏",
        "打印有空白间隔",
        "跑空白",
        "黑印",
        "横纹",
        "断续横纹",
        "硒鼓",
        "粉盒",
        "定影膜",
        "打印字体",
    ],
    "cad-install-uninstall-failed": ["cad装不上", "cad安装", "cad卸载", "cad重装", "autocad安装", "注册表"],
    "cad-crash-or-hang": ["cad卡死", "cad崩溃", "cad无响应", "cad打开后卡死", "cad报错"],
    "cad-plm-interface-failed": ["cad与plm", "cad保存到管理系统", "plm接口", "无法传图", "传图失败"],
    "cad-drawing-open-failed-encryption": ["dwg打不开", "cad图纸打不开", "图纸损坏", "加密图纸", "文件损坏"],
    "solidworks-license-activation-failed": ["solidworks许可", "solidworks激活", "无法获得许可", "重新激活", "许可证丢失", "证书丢失"],
    "solidworks-install-source-missing": ["solidworks.msi", "solidworks无法卸载", "solidworks安装源", "sw无法安装", "solidworks重装"],
    "solidworks-ui-layout-missing": ["solidworks图标缺失", "菜单栏缺失", "功能区按钮", "窗口布局"],
    "oa-upload-or-print-slow": ["oa上传", "oa附件", "oa发协同", "oa打印", "发车清单", "浏览器版本"],
    "plm-client-or-login-failed": ["plm打不开", "plm无法登录", "plm客户端", "plm卡顿", "plm传图"],
    "mes-login-network-related": ["mes登不上", "mes无法登录", "mes登录失败", "车间终端", "mes没网"],
    "cloud-drive-install-sync-access": ["云盘安装", "云盘同步", "云盘扩容", "云盘共享", "投标文件"],
    "encryption-client-offline": ["加密掉线", "加密频繁掉", "没有加密", "加密软件登不上", "手动上线失败", "加密客户端"],
    "ip-conflict-or-static-ip-error": ["ip冲突", "dhcp", "静态ip", "换办公室没网", "ip地址"],
    "vpn-or-remote-access-failed": ["vpn", "远程访问", "远程进不了", "未连接到互联网"],
    "blue-screen-dump-or-driver": ["蓝屏", "blue screen", "驱动蓝屏"],
    "memory-fault-or-insufficient": ["内存不足", "内存问题", "内存坏", "内存条", "运行内存", "内存报警", "内存缓存"],
    "disk-fault-not-just-c-drive-full": ["硬盘坏", "机械硬盘有坏道", "硬盘有坏道", "磁盘读取", "硬盘故障", "读取困难", "硬盘异响"],
    "wps-feature-missing-or-calculation-slow": ["wps功能缺失", "wps计算慢", "表格计算", "wps线程"],
    "browser-compatibility-control-certificate": ["浏览器兼容", "ie兼容", "兼容性视图", "控件", "证书到期", "网址运行不了"],
    "monitor-no-display-or-flicker": [
        "屏幕不亮",
        "显示屏不亮",
        "显示器不显示",
        "显示器坏",
        "显示屏坏",
        "显示屏损坏",
        "显示屏花屏",
        "花屏",
        "闪屏",
        "信号线松",
        "字体模糊",
        "屏幕打不开",
    ],
    "keyboard-mouse-usb-peripheral-failed": [
        "键盘坏",
        "鼠标坏",
        "鼠标断点",
        "按键失灵",
        "usb",
        "usb网卡",
        "usb无法识别",
        "外设",
    ],
    "pdf-reader-open-print-failed": [
        "pdf",
        "pdf打不开",
        "pdf文件不能打开",
        "pdf阅读器",
        "搜狗pdf",
        "adobe",
        "并行配置不正确",
        "扁平化",
        "pdf打印",
    ],
    "sap-client-login-print-failed": [
        "sap",
        "sap登录不了",
        "sap登录不上",
        "sap异常",
        "sap打印",
        "sap无法正常报货",
        "sap纸张",
        "zfi039",
    ],
    "network-cable-port-switch-fault": [
        "网络不通",
        "网线不通",
        "网线松动",
        "网线接触不良",
        "墙上网口",
        "墙插模块",
        "交换机",
        "以太网打叉",
        "网口接触不好",
        "连接网线没有网",
    ],
    "windows-system-reinstall-or-cache-reset": [
        "重装系统",
        "需要重装系统",
        "系统崩溃",
        "无法启动",
        "垃圾软件太多",
        "清空缓存",
        "缓存没清空",
        "系统问题",
        "系统更新问题",
        "软件闪退",
    ],
    "kms-windows-office-activation": [
        "windows系统过期",
        "windows激活",
        "office激活",
        "kms",
        "重新连接kms",
        "系统过期",
    ],
    "camera-no-signal-or-offline": [
        "摄像头",
        "摄像头不通",
        "摄像头无信号",
        "摄像头不亮",
        "无视频信号",
        "监控不通",
        "监控掉线",
        "监控办公楼",
        "监控画面",
        "光衰",
        "保密区域",
    ],
    "barrier-gate-abnormal": [
        "道闸",
        "道闸维修",
        "无法关闭",
        "自动开闭",
        "落杆不到位",
        "车辆道闸",
        "非固定车辆禁止放行",
        "摆闸",
        "红外",
        "限位",
    ],
    "access-control-offline-or-reboot": [
        "门禁",
        "门禁系统",
        "门禁离线",
        "门禁总是重启",
        "门禁一体机",
        "ap离线",
        "访客认证",
        "环保门禁",
    ],
    "meeting-room-display-or-led-screen": [
        "会议室屏幕",
        "会议室",
        "大屏",
        "led大屏",
        "屏幕闪烁",
        "屏幕不显示",
        "maxhub",
        "apk",
        "接收卡",
        "拼接屏",
    ],
    "meeting-room-projection-or-conference-device": [
        "会议室投屏",
        "投屏",
        "腾讯会议投屏",
        "有线投屏",
        "无线投屏",
        "亿联",
        "会议终端",
        "存储满",
        "会议室设备",
    ],
}


CURATED_KEYWORDS.update(
    {
        "linux-cpu-high-usage-alert": [
            "CPU使用率达到95%",
            "CPU使用率超过95%",
            "CPU使用率",
            "cpu使用率",
            "CPU过高",
            "cpu high",
            "node告警",
            "业务机器CPU使用率",
            "服务器CPU",
            "load average",
            "top",
            "pidstat",
        ],
        "linux-memory-high-usage-alert": [
            "WMS业务机器内存使用率",
            "内存使用率超过95%",
            "内存使用率达到97%",
            "内存使用率达到95%",
            "内存使用率",
            "内存压力过大",
            "memory pressure",
            "oom",
            "free -h",
            "vmstat",
            "业务机器内存使用率",
        ],
        "linux-disk-space-high-alert": [
            "PLM应用磁盘空间剩余小于8G",
            "Windows_磁盘空间使用率超过95%",
            "磁盘空间使用率超过97%",
            "磁盘空间使用率达到90%",
            "磁盘空间使用率",
            "磁盘空间剩余小于",
            "磁盘满",
            "磁盘空间不足",
            "df -h",
            "du -sh",
            "inode",
        ],
        "application-http-5xx-or-unavailable-alert": [
            "5xx",
            "4xx",
            "业务后端不可用",
            "后端应用 5xx 告警",
            "域名三分钟内超过",
            "服务不可用",
            "http error",
            "接口错误",
            "应用宕机",
            "nacos 注册掉线告警",
            "nacos",
        ],
        "jvm-gc-thread-alert": [
            "GC吞吐率",
            "GC暂停",
            "GC暂停总时长",
            "活跃的守护线程数量",
            "守护线程",
            "jvm",
            "java",
            "gc",
            "daemon thread",
        ],
        "database-status-tablespace-alert": [
            "卫华MES数据库状态监控",
            "江苏MES数据库状态监控",
            "卫华MES数据库表空间监控",
            "江苏MES数据库表空间监控",
            "NC数据库宕机",
            "NC数据库表空间超过98%",
            "数据库状态监控",
            "数据库表空间监控",
            "表空间",
            "tablespace",
            "数据库宕机",
            "MySQL宕机",
            "Mysql 宕机",
            "Oracle",
            "MySQL",
            "数据库连接",
        ],
    }
)


def slugify(path: Path) -> str:
    return path.stem.lower().replace("_", "-")


def parse_scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value.strip("\"'")


def parse_metadata(text: str) -> dict:
    header = text[:2000]
    next_section = re.search(r"^##\s+", header, re.M)
    if next_section:
        header = header[: next_section.start()]
    match = re.search(r"```yaml\s*(.*?)```", header, re.S | re.I)
    if not match:
        return {}
    metadata = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(value)
    return metadata


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def visible_text(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*]\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]+]\([^)]*\)", " ", text)
    text = re.sub(r"[#>*_`|\\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_section_line(line: str) -> str:
    line = re.sub(r"^\s*[-*+]\s+", "", line)
    line = re.sub(r"^\s*\d+[.、)]\s*", "", line)
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
    line = re.sub(r"`([^`]*)`", r"\1", line)
    return line.strip()


def extract_section_lines(text: str, heading_names: list[str], limit: int = 8) -> list[str]:
    names = "|".join(re.escape(name) for name in heading_names)
    match = re.search(rf"^#+\s*({names})\s*$", text, re.M)
    if not match:
        return []

    start = match.end()
    next_heading = re.search(r"^#+\s+", text[start:], re.M)
    section = text[start : start + next_heading.start()] if next_heading else text[start:]

    lines = []
    for raw_line in section.splitlines():
        line = clean_section_line(raw_line)
        if not line or line.startswith("```"):
            continue
        if re.match(r"^[-=]{3,}$", line):
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def parse_command_line(line: str) -> dict:
    line = re.sub(r"^\s*[-*+]\s+", "", line).strip()
    line = re.sub(r"^\s*\d+[.、)]\s*", "", line).strip()
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
    line = re.sub(r"`([^`]*)`", r"\1", line)
    risk = ""
    purpose = ""
    command = line

    risk_match = re.search(r"\s*[（(]风险[:：]\s*([^）)]+)[）)]\s*$", command)
    if risk_match:
        risk = risk_match.group(1).strip()
        command = command[: risk_match.start()].strip()

    for separator in [" -- ", " —— ", " - "]:
        if separator in command:
            left, right = command.split(separator, 1)
            command = left.strip()
            purpose = right.strip()
            break

    if not purpose and "： " in command:
        left, right = command.split("： ", 1)
        command = left.strip()
        purpose = right.strip()

    fallback_purpose = command_purpose(command)
    if fallback_purpose and (not purpose or "?" in purpose):
        purpose = fallback_purpose

    return {
        "command": command,
        "purpose": purpose,
        "risk": risk or "低",
    }


def command_purpose(command: str) -> str:
    exact = {
        "uptime": "查看系统运行时间和平均负载，判断 CPU 压力是否持续。",
        "top -c": "实时查看 CPU、内存占用最高的进程及完整命令行。",
        "pidstat -u 1 5": "按进程采样 CPU 使用率，观察是否持续占用。",
        "vmstat 1 5": "查看 CPU、内存、运行队列、IO 和系统整体压力。",
        "mpstat -P ALL 1 5": "查看各 CPU 核心使用率，判断是否单核打满。",
        "free -h": "查看内存、缓存和 swap 使用情况。",
        "top -o %MEM": "实时查看内存占用最高的进程。",
        "swapon --show": "查看 swap 是否启用及使用情况。",
        "df -hT": "查看各挂载点容量、使用率和文件系统类型。",
        "df -ih": "查看 inode 使用率，排查小文件过多。",
        "lsblk -f": "查看磁盘、分区、挂载点和文件系统。",
        "mount | column -t": "查看当前挂载信息。",
        "lsof +L1": "查找已删除但仍被进程占用的文件。",
        "journalctl --disk-usage": "查看 systemd journal 日志占用。",
        "docker stats --no-stream": "查看容器 CPU 和内存占用快照。",
        "docker system df": "查看 Docker 镜像、容器、卷占用。",
        "docker image prune -a --dry-run": "预览 Docker 镜像清理影响，不实际删除。",
        "kubectl top pod -A --sort-by=cpu": "查看 Kubernetes Pod CPU 占用排序。",
        "kubectl top pod -A --sort-by=memory": "查看 Kubernetes Pod 内存占用排序。",
        "kubectl get pvc -A": "查看 Kubernetes PVC 列表和容量。",
        "kubectl get pod -n <namespace> -o wide": "查看业务 Pod 状态、IP 和所在节点。",
        "jps -lv": "列出 Java 进程及启动参数。",
        "jstat -gcutil <pid> 1000 10": "采样 JVM GC 使用率和频率。",
        "jcmd <pid> VM.flags": "查看 JVM 启动参数。",
        "jcmd <pid> GC.heap_info": "查看 JVM 堆内存信息。",
        "top -H -p <pid>": "查看指定进程内线程 CPU 占用。",
        "systemctl status mysqld": "查看 MySQL 服务状态。",
        "systemctl status mysql": "查看 MySQL 服务状态，适用于部分发行版服务名。",
        "lsnrctl status": "查看 Oracle 监听状态。",
        "sqlplus / as sysdba": "本机以 SYSDBA 登录 Oracle，需授权。",
        "select status from v$instance;": "查看 Oracle 实例状态。",
        "control printers": "打开 Windows 打印机列表。",
        "services.msc": "打开 Windows 服务管理器。",
        "printmanagement.msc": "打开打印管理，查看驱动、端口和队列。",
        "net stop spooler": "停止打印后台处理服务，常用于清理队列前置操作。",
        "net start spooler": "启动打印后台处理服务。",
        "Get-Printer": "PowerShell 查看本机打印机列表。",
        "taskmgr": "打开任务管理器，查看进程和资源占用。",
        "resmon": "打开资源监视器，查看进程级 CPU、磁盘、网络占用。",
        "perfmon": "打开性能监视器，做较长时间性能观察。",
        "msconfig": "查看系统启动配置和服务，排查异常启动项。",
        "appwiz.cpl": "打开程序和功能，卸载异常或无用软件。",
        "cleanmgr": "启动磁盘清理工具。",
        "%temp%": "打开当前用户临时目录，人工清理临时文件。",
        "eventvwr.msc": "打开事件查看器，检查系统、应用和驱动错误。",
        "devmgmt.msc": "打开设备管理器，检查硬件和驱动异常。",
        "msinfo32": "查看系统型号、BIOS、内存和硬件摘要。",
        "diskmgmt.msc": "打开磁盘管理，检查硬盘和分区是否识别。",
        "chkdsk C: /scan": "在线扫描 C 盘文件系统错误，不立即修复。",
        "sfc /scannow": "扫描并修复 Windows 系统文件。",
        "dism /online /cleanup-image /restorehealth": "修复 Windows 组件存储。",
        "bcdedit": "查看启动配置，排查引导项异常。",
        "shutdown /r /t 0": "立即重启电脑，用于验证重启后是否恢复。",
        "explorer.exe": "重新启动 Windows 桌面外壳，恢复桌面和任务栏。",
        "Ctrl + Shift + Esc": "键盘快捷键打开任务管理器。",
        "ipconfig /all": "查看 IP、网关、DNS、MAC 和 DHCP 状态。",
        "ipconfig /release": "释放 DHCP 地址。",
        "ipconfig /renew": "重新获取 DHCP 地址。",
        "route print": "查看本机路由表。",
        "ncpa.cpl": "打开网络连接界面，检查网卡状态。",
        "netsh interface show interface": "查看网卡接口启用状态。",
        "netsh winsock reset": "重置 Winsock，可能影响网络配置，需重启。",
        "netsh int ip reset": "重置 TCP/IP 协议栈，需重启。",
        "Win + P": "切换投影、扩展或复制显示模式。",
        "desk.cpl": "打开显示设置，检查分辨率和多屏模式。",
        "dxdiag": "查看 DirectX 和显卡信息。",
        "displayswitch.exe": "打开显示切换界面。",
    }
    if command in exact:
        return exact[command]
    prefixes = [
        ("ps -eo ", "按指定字段列出进程并排序，用于定位资源占用最高的进程。"),
        ("dmesg -T", "查看内核日志，常用于排查 OOM、磁盘、驱动等系统级异常。"),
        ("journalctl ", "查看 systemd 日志，按服务或时间窗口定位异常。"),
        ("du -", "统计目录空间占用，用于定位大目录。"),
        ("find ", "按条件查找文件，用于定位大文件、日志或异常文件。"),
        ("curl ", "发起 HTTP 请求，验证状态码、响应头或耗时。"),
        ("tail ", "查看日志文件末尾内容。"),
        ("grep ", "筛选日志或文本中的关键错误。"),
        ("systemctl status ", "查看指定 Linux 服务状态。"),
        ("kubectl describe ", "查看 Kubernetes 资源详情、事件和配置。"),
        ("kubectl logs ", "查看 Kubernetes Pod 日志。"),
        ("kubectl rollout ", "查看或确认 Kubernetes 发布状态和历史。"),
        ("mysql ", "连接 MySQL 执行检查 SQL。"),
        ("mysqladmin ping", "测试 MySQL 实例是否可连接。"),
        ("rundll32 printui.dll", "打开 Windows 打印机管理相关界面。"),
        ("pnputil /enum-drivers", "枚举 Windows 驱动包。"),
        ("pnputil /delete-driver", "卸载指定 Windows 驱动包，需确认驱动归属。"),
        ("ping ", "测试网络连通性。"),
        ("tracert ", "查看到目标地址的路由路径。"),
        ("wmic ", "查询 Windows 系统硬件、磁盘或配置字段。"),
        ("vssadmin ", "查看或管理 Windows 卷影副本。"),
        ("powercfg ", "查看或调整 Windows 电源相关配置。"),
    ]
    for prefix, purpose in prefixes:
        if command.startswith(prefix):
            return purpose
    return ""


def extract_commands(text: str, limit: int = 12) -> list[dict]:
    return [parse_command_line(line) for line in extract_section_lines(text, ["常用指令", "常用命令", "检查命令", "参考命令", "排查命令"], limit=limit)]


def unique_keep_order(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        value = value.strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def build_index(docs_dir: Path) -> list[dict]:
    docs = []
    for path in sorted(docs_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata = parse_metadata(text)
        if not metadata:
            continue
        doc_id = slugify(path)
        title = title_from_markdown(text, doc_id)
        tags = metadata.get("tags", [])
        systems = metadata.get("systems", [])
        issue_types = metadata.get("issue_types", [])
        asset_types = metadata.get("asset_types", [])
        if isinstance(tags, str):
            tags = [tags]
        if isinstance(systems, str):
            systems = [systems]
        if isinstance(issue_types, str):
            issue_types = [issue_types]
        if isinstance(asset_types, str):
            asset_types = [asset_types]

        keywords = []
        keywords.extend(CURATED_KEYWORDS.get(doc_id, []))
        keywords.extend([title])
        keywords.extend(tags)
        keywords.extend(systems)
        keywords.extend(issue_types)
        keywords.extend(asset_types)

        docs.append(
            {
                "doc_id": doc_id,
                "title": title,
                "status": metadata.get("status", "candidate"),
                "type": metadata.get("type", ""),
                "asset_types": asset_types,
                "systems": systems,
                "issue_types": issue_types,
                "tags": tags,
                "keywords": unique_keep_order(keywords),
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "content_preview": visible_text(text)[:300],
                "applicability": extract_section_lines(text, ["适用范围", "适用场景"], limit=3),
                "symptoms": extract_section_lines(text, ["常见现象", "故障现象", "问题现象"], limit=5),
                "steps": extract_section_lines(text, ["处理步骤", "解决步骤", "操作步骤"], limit=10),
                "commands": extract_commands(text, limit=12),
                "verification": extract_section_lines(text, ["验证方式", "验证方法", "验证结果"], limit=5),
                "notes": extract_section_lines(text, ["注意事项", "风险提示", "升级条件"], limit=5),
                "search_text": visible_text(text)[:2000],
            }
        )
    return docs


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a structured index from Markdown knowledge articles.")
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    docs = build_index(args.docs_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Indexed {len(docs)} documents -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
