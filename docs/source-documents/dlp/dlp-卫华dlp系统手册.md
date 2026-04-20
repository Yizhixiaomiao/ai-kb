# 卫华DLP系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [dlp]
issue_types: [reference]
tags: [engineer-doc, imported, dlp]
source_path: "D:\新建文件夹\业务维护清单\DLP\卫华DLP系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华DLP系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\DLP
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华DLP系统 系统手册

摘要

该文档详细阐述了卫华DLP系统的维护、使用以及操作注意事项。

作者：孟庆洋

日期：2024年9月16日

版本：v1.0

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

亿赛通新一代电子文档安全管理系统（简称：CDG）是一款融合文档加密、数据分类分级、访问控制、关联分析、大数据分析、智能识别等核心技术的综合性数据智能安全产品。产品包括透明加密、智能加密、权限文档、数据分类分级、终端安全管理、文件外发管理、集团管控、数据安全网关、加解密接口中间件、U盘客户端十大核心组件，保护范围涵盖终端电脑（Windows、Mac和Linux系统平台）、智能终端（Android、IOS）以及各类应用系统（OA、知识管理、文档管理、项目管理、PDM等），能够对企业核心数据资产从生产、存储、流转、外发到销毁进行全生命周期保护。通过对“有意”、“无意”两种数据泄漏行为作统一防护，采用“事前主动防御，事中实时控制，事后及时追踪，全面防止泄密”的设计理念，配合身份鉴别、数据分类、密级标识、权限控制、应用集成、安全接入、风险预警以及行为审计等能力，全方位保障用户终端数据安全。

服务器基本信息

联系方式

- 系统管理员：孟庆洋，电话：<手机号已脱敏>，邮件：mengqingyang@cranewh.com

- 厂家技术支持：绿盟科技，400-818-6868 转接 0，<手机号已脱敏>

报修平台地址：无

账号：无

密码=<已脱敏>

服务器信息

| 服务器 | DLP |  |  |

| 系统信息 |  |  |  |

| 操作系统 | Windows 2016 STD |  |  |

| 主机名 | WIN-F5KBECDV5JD |  |  |

| IP | <IP地址已脱敏>/24 |  |  |

| GATEWAY | <IP地址已脱敏> |  |  |

| 硬件信息 |  |  |  |

| vCPU | 12 |  |  |

| 内存 | 80G |  |  |

| 硬盘 | 100G+1T |  |  |

| VLAN | 222 |  |  |

| 宿主信息 |  |  |  |

| vCenter | <IP地址已脱敏> |  |  |

| 群集 | WH-cluster |  |  |

应用信息

<IP地址已脱敏>-DLP

| 数据库服务器：<IP地址已脱敏>:1433版本：Microsoft SQL Server 2008 R2 (RTM) - 10.50.1600.1 (X64)应用目录：D:\MSSQL10_50.MSSQLSERVER\MSSQL数据库文件目录（默认）：D:\MSSQL10_50.MSSQLSERVER\MSSQL\DATA日志目录：D:\MSSQL10_50.MSSQLSERVER\MSSQL\DATA |

| DLP服务器：<IP地址已脱敏>:8090应用目录：C:\Program Files (x86)\ESAFENET\CDocGuard Server启停：Services.msc / CobraDG配置文件：C:\Program Files (x86)\ESAFENET\CDocGuard Server\tomcat64\conf\server.xml日志目录：C:\Program Files (x86)\ESAFENET\CDocGuard Server\tomcat64\webapps\CDGServer3\logs |

系统优化配置

| 服务器 | 安装杀毒客户端 | 安装蓝鲸客户端 | 配置进程监控 | 限制登录配置 | 本地yum源配置 | 端口封堵 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐免代理备份，7天 | 是 |

运维手册

服务点检

| 服务器 | 业务状态 | 备份状态 | 系统资源使用率 |

| <IP地址已脱敏> | SQL Server（1433）和CobraDG（8090） | 科力锐备份状态 | 利用蓝鲸监控查看负载 |

停机维护

单台应用，无特别注意事项。

常见问题处理

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |
