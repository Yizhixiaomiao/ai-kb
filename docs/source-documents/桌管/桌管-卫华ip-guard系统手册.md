# 卫华IP-Guard系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [桌管]
issue_types: [reference]
tags: [engineer-doc, imported]
source_path: "D:\新建文件夹\业务维护清单\桌管\卫华IP-Guard系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华IP-Guard系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\桌管
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华IP-Guard系统 系统手册

摘要

该文档详细阐述了卫华IP-Guard系统的维护、使用以及操作注意事项。

作者：孟庆洋

日期：2024年8月16日

版本：v1.0

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

IP-guard企业信息监管系统是一款高性价比的网络监管系统。IP-guard可以详细记录网络环境下的计算机的屏幕、使用的应用程序、浏览的网站、文件操作等活动，并能提供程序使用控制、网站使用控制、设备禁用、远程控制、软件分发、资产管理等管理功能，从而让企业管理者清楚了解内部和控制的计算机使用者如何使用企业的信息资源，为企业的业务提供保障。

服务器基本信息

联系方式

系统管理员：孟庆洋，电话：<手机号已脱敏>，邮件：mengqingyang@cranewh.com

厂家技术支持：河南信之服信息技术有限公司，电话：0371-86017811

报修平台地址：无

账号：无

密码=<已脱敏>

服务器信息

服务器信息-表1

| 服务器 | IP-Guard |  |  |

| 系统信息 |  |  |  |

| 操作系统 | Windows 2016 STD |  |  |

| 主机名 | DSM |  |  |

| IP | <IP地址已脱敏>/24 |  |  |

| GATEWAY | <IP地址已脱敏> |  |  |

| 硬件信息 |  |  |  |

| vCPU | 8 |  |  |

| 内存 | 16G |  |  |

| 硬盘 | 100G+4T |  |  |

| VLAN | 1 |  |  |

| 宿主信息 |  |  |  |

| vCenter | <IP地址已脱敏> |  |  |

| 群集 | Production |  |  |

应用信息

IP-Guard产品包括多种服务器角色：

数据库 SQL Server (SQLEXPRESS)

服务器 OCULAR V3 SERVER

中继器 OCULAR V3 MIDTIER SERVER

客户端 WINDOWS HELPER SERVICE

报表 OCULAR V3 REPORT SERVER

web服务器 Ocular web server ,OCULAR Console Web Service

云备份服务器 OCULAR File Cloud Backup Server, OCULAR File Cloud Backup Helper, OCULAR File Cloud Backup Cacher

加密备份服务器 OCULAR V3 BACKUP SERVER

备用服务器 OCULAR V3 STANDBY SERVER

邮件服务器 OCULAR V3 MAILREPORT

补丁 OCULAR V3 UPDATE

申请文档存储服务器 OCULAR Approval Backup Server, OCULAR Approval Backup Cacher

LDAP服务器OpenLDAP slapd server

webservice接口 OCULAR Console Web Service

<IP地址已脱敏> SQLServer 2008R2 / IP-Guard

| SQLServer服务器：<IP地址已脱敏>服务名称：MSSQL$IPG显示名称：SQL Server (IPG)可执行文件的路径："C:\Program Files\Microsoft SQL Server\MSSQL10_50.IPG\MSSQL\Binn\sqlservr.exe" -sIPG启停：Services.msc‬‬配置文件：D:\IPguard3\日志目录：D:\IPguard3 |

| IP-Guard服务器：<IP地址已脱敏>服务名称：OSERVER3显示名称：OCULAR V3 SERVER可执行文件的路径："D:\IPguard3\oserver3_x64.exe" -service启停：Services.msc‬‬配置文件：D:\IPguard3\OServer3.ini |

系统优化配置

| 服务器 | 安装杀毒客户端 | 安装蓝鲸客户端 | 配置进程监控 | 限制登录配置 | 本地yum源配置 | 端口封堵 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐免代理备份，7天 | 是 |

运维手册

服务点检

| 服务器 | 业务状态 | 备份状态 | 系统资源使用率 |

| <IP地址已脱敏> | SQL Server (IPG) / OCULAR V3 SERVER | 科力锐整机备份状态 | 利用蓝鲸监控查看负载 |

停机维护

开机

单台应用，无特别注意事项

关机

单台应用，无特别注意事项

常见问题处理

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |
