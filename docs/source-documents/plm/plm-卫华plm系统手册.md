# 卫华PLM系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [plm]
issue_types: [reference]
tags: [engineer-doc, imported, plm]
source_path: "D:\新建文件夹\业务维护清单\PLM\卫华PLM系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华PLM系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\PLM
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华PLM系统 运维手册

摘要

该文档详细阐述了卫华WMS系统的维护、使用以及操作注意事项。

作者：李军

日期：2024年8月14日星期三

版本：v1.0

。

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

PLM为离散制造业提供机、电、软协同设计管理平台，支持异构CAD并存设计,支持集团异地协同设计，支持设计、工艺一体化管理，实现质量体系与信息系统完全一体化。供应商为思普软件（上海）有限公司。

服务器基本信息

联系方式

- 系统管理员：李军，电话：<手机号已脱敏>，邮件：lijun@craneweihua.com

- 厂家技术支持：

报修平台地址：bestplm.com

账号:15012

密码=<已脱敏>

硬件信息

| 配置 | 应用/扫描服务器/web-api | 文件/签名/AutoVUE | 数据库 |

| 固定资产编号 | 51020140068 | 51020140067 | 51020140072 |

| 机架编号 | CY081617 (长垣机房08机柜161-7U) | CY082021 (长垣机房08机柜20-21U) | CY082627(长垣机房08机柜26-27U) |

| 服务器型号 | DELL PowerEdge R740 | DELL PowerEdge R740 | DELL PowerEdge R740 |

| 出厂序列号 | 6HJ7LV2 | 6HD3LV2 | 6J5ZKV2 |

| IDRAC: | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> |

| CPU | Intel(R) Xeon(R) Gold 5117 CPU @ 2.00GHz / cpu28*2 | Intel(R) Xeon(R) Gold 5117 CPU @ 2.00GHz / cpu28*3 | Intel(R) Xeon(R) Gold 5117 CPU @ 2.00GHz / cpu28*2 |

| 内存 | DDR4128G | 32G | 64G |

| 硬盘 | SSD480G 组RAID1 | SSD:480G+18.1T | SSD:480G+5.5T |

| 网络接口 | <IP地址已脱敏>XGigabitEthernet0/0/19 | <IP地址已脱敏>XGigabitEthernet0/0/17 | <IP地址已脱敏>XGigabitEthernet0/0/18 |

| VLAN ID | 222 | 222 | 222 |

| 操作系统 | Windows2012R2 | Windows2012R2 | CentOS 6.10 |

应用信息

<IP地址已脱敏> 文件、签名、AutoVue服务器

| 文件服务器：<IP地址已脱敏>:8089应用目录：D:\WHPLM\fileserver启停：D:\WHPLM\fileserver\bin\standalone.bat配置文件：D:\WHPLM\fileserver\standalone\configuration\standalone.xml日志目录：D:\WHPLM\fileserver\standalone\log\ |

| 签名服务器：<IP地址已脱敏>:8091应用目录：D:\WHPLM\fileappserver启停：D:\WHPLM\fileappserver\bin\standalone.bat配置文件：D:\WHPLM\fileappserverr\standalone\configuration\standalone.xml日志目录：D:\WHPLM\fileappserver\standalone\log\ |

| AutoVue服务器：<IP地址已脱敏>:5099应用目录：C:\Oracle\AutoVue启停：C:\Oracle\AutoVue\bin\jvueserver.bat配置文件：C:\Oracle\AutoVue\bin\jvueserver.properties日志目录：C:\Oracle\AutoVue\bin\Logs |

<IP地址已脱敏> 应用、扫描、Web-api

| 应用服务器：<IP地址已脱敏>:8088应用目录：D:\WHPLM\bcfserver启停：D:\WHPLM\bcfserver\bin\standalone.bat配置文件：D:\WHPLM\bcfserver\standalone\configuration\standalone.xml日志目录：D:\WHPLM\bcfserver\standalone\log\ |

| 扫描服务器：<IP地址已脱敏>:8090应用目录：D:\WHPLM\scanserver启停：D:\WHPLM\scanserver\bin\standalone.bat配置文件：D:\WHPLM\scanserver\standalone\configuration\standalone.xml日志目录：D:\WHPLM\scanserver\standalone\log\ |

| web-api服务器：<IP地址已脱敏>:8090应用目录：D:\WHPLM\web-api启停：D:\WHPLM\web-api\bin\startup.bat配置文件：D:\WHPLM\web-api\conf\server.xml日志目录：D:\WHPLM\web-api\logs\ |

<IP地址已脱敏> 数据库服务器

| 版本：<IP地址已脱敏>.0SERVICE_NAME = plmORACLE_SID = plmORACLE_BASE = /home/oracle/appORACLE_HOME = /home/oracle/app/product/11.2.0spfile = /home/oracle/app/product/11.2.0/dbs/spfileplm.ora归档日志目录 = /WH_data/archivelog数据文件目录 =/WH_data/oradata |

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

|  | 限制登录配置 |  |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐整机备份，30天 | 是 |

| <IP地址已脱敏> | 科力锐整机备份，30天 | 是 |

| <IP地址已脱敏> | Networker备份每天备份，备份文件保留7天 | 是 |

运维手册

服务点检

停机维护

常见问题处理

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |
