# 桌面运维参考知识清单

本目录中的文档由 `工单报修历史记录.csv` 归纳生成，状态统一调整为 `usable`。这些文档用于工程师处理工单时参考，不面向普通一线用户自助执行。

## 整理原则

第一版按大类合并，便于快速搭框架，但对工程师检索不够直观。当前版本改为“低聚合、细场景”：

- 打印机不再只合并为“无法打印”，拆成连接、驱动、脱机、卡纸、标签纸、扫描、端口、模板。
- 设计软件单独拆 CAD、SolidWorks、PLM 接口、图纸加密。
- 业务系统按 OA、PLM、MES、云盘拆分。
- 硬件问题区分蓝屏、内存、硬盘、无法开机、黑屏。
- 网络安全问题区分认证、加密客户端、IP 冲突、VPN。
- 安防问题单独拆摄像头、道闸、门禁。
- 会议室问题单独拆大屏显示和投屏 / 会议终端。

## 汇总类参考知识

| 文档 | 来源聚类 | 建议审核人 |
| --- | --- | --- |
| [network-authentication-unavailable.md](network-authentication-unavailable.md) | 网络认证 / MES / 无网 | 网络或桌面运维 |
| [printer-not-working.md](printer-not-working.md) | 打印机无法连接 / 无法打印 | 桌面运维 |
| [printer-paper-jam.md](printer-paper-jam.md) | 打印机卡纸 | 桌面运维或硬件维护 |
| [pc-boot-failed.md](pc-boot-failed.md) | 无法开机 / 不通电 | 桌面运维或硬件维护 |
| [black-screen-desktop-not-shown.md](black-screen-desktop-not-shown.md) | 黑屏 / 桌面不显示 | 桌面运维 |
| [pc-performance-slow.md](pc-performance-slow.md) | 电脑卡顿 / 性能慢 | 桌面运维 |
| [disk-c-drive-full.md](disk-c-drive-full.md) | C 盘 / 系统盘空间不足 | 桌面运维 |
| [account-login-failed.md](account-login-failed.md) | 账号 / 密码 / 权限 / 登录异常 | 账号或应用管理员 |
| [office-wps-document-open-failed.md](office-wps-document-open-failed.md) | Office / WPS / 文档打不开 | 桌面运维 |
| [software-client-installation.md](software-client-installation.md) | 软件 / 客户端安装 | 桌面运维 |
| [shared-file-cloud-drive-access.md](shared-file-cloud-drive-access.md) | 共享文件 / 云盘访问异常 | 桌面运维或存储管理员 |

## 细分参考知识

### 打印机

| 文档 | 场景 |
| --- | --- |
| [printer/shared-printer-connect-failed.md](printer/shared-printer-connect-failed.md) | 共享打印机连接失败 |
| [printer/printer-driver-install-failed.md](printer/printer-driver-install-failed.md) | 打印机驱动安装失败或驱动丢失 |
| [printer/printer-offline-or-paused.md](printer/printer-offline-or-paused.md) | 打印机脱机、暂停或接收任务但不打印 |
| [printer/printer-paper-jam-feed-failed.md](printer/printer-paper-jam-feed-failed.md) | 卡纸、进纸失败 |
| [printer/label-printer-paper-recognition.md](printer/label-printer-paper-recognition.md) | 标签打印机纸张识别、库位码、标识卡 |
| [printer/scanner-preview-failed.md](printer/scanner-preview-failed.md) | 扫描后无法预览或下载异常 |
| [printer/print-port-deleted-by-security-software.md](printer/print-port-deleted-by-security-software.md) | 安全软件删除打印端口 |
| [printer/print-template-or-paper-size-error.md](printer/print-template-or-paper-size-error.md) | 打印模板或纸张规格错误 |
| [printer/print-quality-faded-streaks-head-wear.md](printer/print-quality-faded-streaks-head-wear.md) | 打印不清楚、横纹、黑印或打印头磨损 |

### CAD / SolidWorks / PLM 接口

| 文档 | 场景 |
| --- | --- |
| [design-software/cad-install-uninstall-failed.md](design-software/cad-install-uninstall-failed.md) | CAD 安装、卸载或重装失败 |
| [design-software/cad-crash-or-hang.md](design-software/cad-crash-or-hang.md) | CAD 打开后卡死、崩溃或无响应 |
| [design-software/cad-plm-interface-failed.md](design-software/cad-plm-interface-failed.md) | CAD 与 PLM 接口异常 |
| [design-software/cad-drawing-open-failed-encryption.md](design-software/cad-drawing-open-failed-encryption.md) | CAD 图纸打不开或加密相关异常 |
| [design-software/solidworks-license-activation-failed.md](design-software/solidworks-license-activation-failed.md) | SolidWorks 许可或激活异常 |
| [design-software/solidworks-install-source-missing.md](design-software/solidworks-install-source-missing.md) | SolidWorks 安装源缺失或无法重装 |
| [design-software/solidworks-ui-layout-missing.md](design-software/solidworks-ui-layout-missing.md) | SolidWorks 菜单栏或功能区按钮缺失 |

### 业务系统客户端

| 文档 | 场景 |
| --- | --- |
| [business-systems/oa-upload-or-print-slow.md](business-systems/oa-upload-or-print-slow.md) | OA 附件上传失败或打印慢 |
| [business-systems/plm-client-or-login-failed.md](business-systems/plm-client-or-login-failed.md) | PLM 客户端、登录或接口异常 |
| [business-systems/mes-login-network-related.md](business-systems/mes-login-network-related.md) | MES 登录失败或疑似网络认证问题 |
| [business-systems/cloud-drive-install-sync-access.md](business-systems/cloud-drive-install-sync-access.md) | 云盘安装、同步或共享访问异常 |

### 网络与终端安全

| 文档 | 场景 |
| --- | --- |
| [network-security/encryption-client-offline.md](network-security/encryption-client-offline.md) | 加密客户端掉线或手动上线失败 |
| [network-security/ip-conflict-or-static-ip-error.md](network-security/ip-conflict-or-static-ip-error.md) | IP 冲突或静态地址配置异常 |
| [network-security/vpn-or-remote-access-failed.md](network-security/vpn-or-remote-access-failed.md) | VPN 或远程访问失败 |

### 硬件与系统

| 文档 | 场景 |
| --- | --- |
| [hardware/blue-screen-dump-or-driver.md](hardware/blue-screen-dump-or-driver.md) | Windows 蓝屏 |
| [hardware/memory-fault-or-insufficient.md](hardware/memory-fault-or-insufficient.md) | 内存故障或内存不足 |
| [hardware/disk-fault-not-just-c-drive-full.md](hardware/disk-fault-not-just-c-drive-full.md) | 硬盘故障或读取困难 |

### Office / 浏览器

| 文档 | 场景 |
| --- | --- |
| [office/wps-feature-missing-or-calculation-slow.md](office/wps-feature-missing-or-calculation-slow.md) | WPS 功能缺失或表格计算慢 |
| [office/browser-compatibility-control-certificate.md](office/browser-compatibility-control-certificate.md) | 浏览器兼容性、控件或证书异常 |

### 安防设备

| 文档 | 场景 |
| --- | --- |
| [security/camera-no-signal-or-offline.md](security/camera-no-signal-or-offline.md) | 摄像头无信号、离线或画面异常 |
| [security/barrier-gate-abnormal.md](security/barrier-gate-abnormal.md) | 道闸无法关闭、自动开闭或离线 |
| [security/access-control-offline-or-reboot.md](security/access-control-offline-or-reboot.md) | 门禁离线、反复重启或网络异常 |

### 会议室设备

| 文档 | 场景 |
| --- | --- |
| [meeting-room/meeting-room-display-or-led-screen.md](meeting-room/meeting-room-display-or-led-screen.md) | 会议室屏幕、大屏或 LED 显示异常 |
| [meeting-room/meeting-room-projection-or-conference-device.md](meeting-room/meeting-room-projection-or-conference-device.md) | 会议室投屏、亿联或腾讯会议设备异常 |

## 使用建议

这些文档可以直接进入工单推荐，使用时建议工程师关注：

- 具体系统名称、客户端名称、平台地址或打印服务器地址是否与现场一致。
- 是否需要管理员权限。
- 是否涉及账号、权限、授权、数据恢复、注册表、系统重装、硬件更换等高风险操作。
- 是否需要升级给网络、系统、应用、数据、硬件或供应商工程师。

关键系统或高频知识后续可进一步确认为 `status: verified`，并填写 `owner`、`reviewer` 和更新时间。
