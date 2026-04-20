# 卫华PO系统运维手册v1

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [po]
issue_types: [reference]
tags: [engineer-doc, imported, po]
source_path: "D:\新建文件夹\业务维护清单\PO\卫华PO系统运维手册v1.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华PO系统运维手册v1.docx
- 原始路径：D:\新建文件夹\业务维护清单\PO
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华PO系统运维手册

摘要

该文档详细阐述了卫华SAP系统的维护、使用以及操作注意事项。

。

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

SAP PO(Process Orchestration)系统基于SAP NetWeaver平台（SOA框架的平台）的中间件产品，为企业提供一套支持SAP系统间、SAP系统与Non-SAP系统间及Non-SAP系统间进行数据交换(XI/PI)和业务流程管理(BPM)的平台，业务流程可以根据预定义的规则(BRM)流转，数据集成可以是A2A或B2B，支持同步和异步的数据交互方式。

服务器基本信息

系统架构

硬件信息

SAP:400-620-2008

应用服务器

IP：<IP地址已脱敏>

操作系统：SUSE Linux Enterprise Server 15 SP1

内核版本：4.12.14-195-default.x86_64

| 服务器 | 应用 |  |  |

| 系统信息 |

| 操作系统 | SLES 15 SP1 | IP | <IP地址已脱敏>/24 |

| 主机名 | sappoprd | GATEWAY | <IP地址已脱敏> |

| 硬件信息 |

| vCPU | 16 | 硬盘 | 280 |

| 内存 | 128 | VLAN | 198 |

| 宿主信息 |

| vCenter | <IP地址已脱敏> | 群集 | Production |

数据库服务器

IP：<IP地址已脱敏>-13

操作系统：SUSE Linux Enterprise Server 15 SP1

内核版本：4.12.14-195-default.x86_64

| 配置 | 数据库 | 数据库 |

| 固定资产编号 | 51020140089 | 51020140090 |

| 机架编号 | CYA061012 (长垣机房06机柜10-12U) | CYA061719(长垣机房06机柜17-19U) |

| 服务器型号 | DELL PowerEdge R940 | DELL PowerEdge R940 |

| 出厂序列号 | 8FS8D53 | 8FRBD53 |

| IDRAC: | <IP地址已脱敏> | <IP地址已脱敏> |

| CPU | Intel(R) Xeon(R) Platinum 8276 CPU @ 2.20GHz / cpu28*2 | Intel(R) Xeon(R) Platinum 8276 CPU @ 2.20GHz / cpu28*2 |

| 内存 | ECC DDR4 2304G | ECC DDR4 2304G |

| 硬盘 | SSD480G 组RAID1 SSD1.92T组RAID5 HHD1.8T组RAID5 | SSD480G 组RAID1 SSD1.92T组RAID5 HHD1.8T组RAID5 |

| 网络接口 | <IP地址已脱敏>XGigabitEthernet0/0/1XGigabitEthernet1/0/1 | <IP地址已脱敏>XGigabitEthernet0/0/2XGigabitEthernet1/0/2 |

| VLAN ID | 198 | 198 |

| 操作系统 | SLES 15 SP1 | SLES 15 SP1 |

应用信息

<IP地址已脱敏> 数据库服务器

| 部署：SAP HANA 2.00.048端口：30013 30015启动命令：HDB start数据路径：/hana/data配置路径：/hana/shared日志路径：/hana/log数据库账号：SYSTEM数据库密码=<已脱敏> |

<IP地址已脱敏> 数据库服务器

| 部署：SAP HANA 2.00.048端口：30013 30015启动命令：HDB start数据路径：/hana/data配置路径：/hana/shared日志路径：/hana/log数据库账号：SYSTEM数据库密码=<已脱敏> |

<IP地址已脱敏> 应用服务器

| 部署：SAP POSAP端口：3301,50000SAP启动重启停止：startsap R3/stopsap R3SAP参数配置路径：/usr/sap/POP/SYS/profileSAP日志路径：/usr/sap/POP/J00 /j2ee/cluster/server0 |

安全配置

| 服务器IP | 安全加固项 | 是否加固 |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 卸载zabbix_agent | 是 |

|  | 限制登录配置 |  |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

系统优化配置

无

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐整机备份，30天 | 是 |

| <IP地址已脱敏> | Networker备份每天备份，备份文件保留10天 | 是 |

变更管理

变更记录

运维手册

更新

<IP地址已脱敏> 数据库服务器

| 启停命令 | HDB start |启动 HDB stop|停止 |

| 查看进程 | sapcontrol -nr 00 -function GetProcessList |

| 配置文件 | /hana/shared/GHP/global/hdb/custom/config/DB_GHP |

| 进程端口 | 30015 |

| 用户名密码 | su - ghpadm |

<IP地址已脱敏> 数据库服务器

| 启停命令 | HDB start |启动 HDB stop|停止 |

| 查看进程 | sapcontrol -nr 00 -function GetProcessList |

| 配置文件 | /hana/shared/GHP/global/hdb/custom/config/DB_GHP |

| 进程端口 | 30015 |

| 用户名密码 | su - ghpadm |

<IP地址已脱敏> PO应用服务器

| 部署业务 | SAP PO |

| 启停命令 | systemctl start|stop pacemaker |

| 查看日志 | /usr/sap/POP/J00/j2ee/cluset/server0 |

| web界面 | http://<IP地址已脱敏>:50000 |

| 配置文件 | /usr/sap/PPO/SYS/profile/POP_J00_sappoprd |

| 进程端口 |  |

停机维护

当遇到需要停机维护的时候，服务的关闭顺序如下

PO-->HANA从-->HANA主

点检

常见问题处理

1、

2、

3、
