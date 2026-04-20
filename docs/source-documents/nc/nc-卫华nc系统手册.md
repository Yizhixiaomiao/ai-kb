# 卫华NC系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [nc]
issue_types: [reference]
tags: [engineer-doc, imported, nc]
source_path: "D:\新建文件夹\业务维护清单\NC\卫华NC系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华NC系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\NC
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华NC系统 操作手册

摘要

该文档详细阐述了卫华NC系统的维护、使用以及操作注意事项。

作者：常帅

日期：2024年9月11日星期三

版本：v1.0

。

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

用友NC涵盖了财务核算、成本控制、预算管理、资产管理等核心功能，通过自动化的财务流程和智能化的数据分析，提高企业的财务管理效率和决策能力。

服务器基本信息

联系方式

- 系统管理员：常帅，电话：<手机号已脱敏>，邮件：changshuai@craneweihua.com

- 厂家技术支持：

无

硬件信息

卫华MES应用服务器

| 服务器 | 卫华NC应用服务器 | 集团NC应用服务器 |

| 系统信息 |  |  |

| 操作系统 | CentOS release 6.10 | CentOS release 6.10 |

| 主机名 | gfncweb | jtncweb |

| IP | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 |

| GATEWAY | <IP地址已脱敏> | <IP地址已脱敏> |

| 硬件信息 |  |  |

| vCPU | 16 | 16 |

| 内存 | 40G | 32G |

| 硬盘 | 632G | 632G |

| VLAN | 1 | 1 |

| 宿主信息 |  |  |

| vCenter | <IP地址已脱敏> | <IP地址已脱敏> |

| 群集 | WH-cluster | WH-cluster |

| 配置 | NC数据库 |

| 固定资产编号 | 51020140195 |

| 机架编号 | CYA092021(长垣机房行政楼机房09机柜20-21U) |

| 服务器型号 | DELL PowerEdge R750 |

| 出厂序列号 | 1T8JJM3 |

| IDRAC: | <IP地址已脱敏> |

| CPU | Intel(R) Xeon(R) Gold 5318 CPU @ 2.10GHz / cpu24*2 |

| 内存 | 64G |

| 硬盘 | Raid-1:480G*2;Raid-5:2.4T*4 |

| 网络接口 | <IP地址已脱敏>XGigabitEthernet0/0/18 |

| VLAN ID | 1 |

| IP | <IP地址已脱敏> |

| 操作系统 | Centos Linux release 7.9.2009 (Core) |

应用信息

<IP地址已脱敏> 集团NC应用服务器

| 部署：IBM websphere端口：9000部署：NC启动命令：su - weblogiccd app/ sh ncstart.sh部署：weblogic端口：9632 9060 9352 9100 7277 8879 9809 9043 9626 2810 7272 9354 9101 8878 9643 2811 9444 42757 9355 8881 9091 9636 9083 2813 9446 9357 8883 44472 9637 9084 2814 944746442 9358 8884 9638 9085 2815 37154 9448 9359 8885 9635 9082 2812 9445 9356 40145 8882 |

<IP地址已脱敏> 股份NC应用服务器

| 部署：IBM websphere端口：9000部署：NC启动命令：su - weblogiccd app/ sh ncstart.sh部署：java端口：9632 9060 9352 9100 7277 8879 9809 9043 9626 2810 7272 9354 9101 8878 9643 2811 9444 33993 9355 8881 9081 9636 9083 2813 9446 33096 9357 8883 9637 9084 2814 9447 41470 9358 8884 9638 9085 2815 34322 9448 9359 8885 9635 9082 2812 9445 9356 38067 8882 |

<IP地址已脱敏> NC数据库服务器

| 部署：oracle 版本:<IP地址已脱敏>.0端口：1521数据文件路径：/oradata/NCDB归档日志路径：/oradata/archive_logservername:NCDB2sid:NCDB2oracle_base:/u01/oracle/oracle_home:/u01/oracle/product/11.2.0/dbhome_1spfile:/u01/oracle/product/11.2.0/dbhome_1/dbs/spfileNCDB2.ora |

系统优化配置

| 服务器IP | 系统优化项 | 是否优化 |

| <IP地址已脱敏> | 安装杀毒客户端 | 是 |

|  | 安装蓝鲸客户端， | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

4.备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 整机备份，第一次全备之后每天增量备份，备份文件保留30天 | 是 |

| <IP地址已脱敏> | 整机备份，第一次全备之后每天增量备份，备份文件保留30天 | 是 |

| <IP地址已脱敏> | networker数据库备份，每日全量备份，备份文件保留7天 | 是 |

5.运维手册

服务信息

<IP地址已脱敏> 集团NC服务器

| 部署业务 | java、IBM websphere |

| 启停命令 | 停止su - weblogiccd app/ sh ncstop.sh启动su - weblogiccd app/ sh ncstart.sh |

<IP地址已脱敏> 股份NC服务器

| 部署业务 | java、IBM websphere |

| 启停命令 | 停止su - weblogiccd app/ sh ncstop.sh启动su - weblogiccd app/ sh ncstart.sh |

<IP地址已脱敏>  MES数据库服务器

| 部署业务 | Oracle <IP地址已脱敏>.0 |

| 启停命令 | 停止实例:shutdown immediate;启动实例:startup启动监听:lsnrctl start |

5.2停机维护

当遇到需要停机维护的时候，服务的关闭顺序如下

应用：应用服务NC-> 数据库Oracle

业务恢复启动服务顺序：数据库Oracle-->应用：NC

5.3日常点检

| 点检内容 | 点检业务正常标准 |

| 备份 | 应用虚拟机在科力锐备份状态成功数据库在networker备份状态成功 |

| 业务状态 | 应用服务java正常运行，业务正常访问数据库服务oracle正常运行访问 |

| 硬件状态正常 | 电源、内存、cpu、存储使用状态正常 |
