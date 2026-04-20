# 卫华AD系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [ad]
issue_types: [reference]
tags: [engineer-doc, imported, ad]
source_path: "D:\新建文件夹\业务维护清单\AD\卫华AD系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华AD系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\AD
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华AD系统 系统手册

摘要

该文档详细阐述了卫华AD系统的维护、使用以及操作注意事项。

作者：孟庆洋

日期：2024年8月16日

版本：v1.0

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

目录是一种分层结构，用于存储网络上的对象的相关信息。诸如 Active Directory 域服务 (AD DS) 之类的目录服务提供用于存储目录数据并使此数据可供网络用户和管理员使用的方法。例如，AD DS 存储有关用户帐户的信息，如名称、密码、电话号码等，并使同一网络上的其他授权用户能够访问这些信息。

Active Directory 存储有关网络上对象的信息，并让管理员和用户可以更容易地使用这些信息。 Active Directory 使用结构化数据存储作为目录信息的逻辑层次组织的基础。

此数据存储也称为目录，包含有关 Active Directory 对象的信息。这些对象通常包括共享资源，如服务器、卷、打印机以及网络用户和计算机帐户。

安全性通过登录身份验证以及对目录中对象的访问控制与 Active Directory 集成。通过单一网络登录，管理员可以管理其整个网络中的目录数据和组织，获得授权的网络用户可以访问该网络上的任何资源。基于策略的管理简化了即使最复杂的网络的管理。

Active Directory 还包括：

一组规则，即架构，它定义包含在目录中的对象和属性的类别、这些对象的实例的约束和限制及其名称的格式。

全局编录，包含有关目录中每个对象的信息。这允许用户和管理员查找目录信息，而无论目录中的哪个域实际包含数据。

一种查询和索引机制，以便对象及其属性可由网络用户或应用程序发布和发现。

一种复制服务，可在整个网络中分发目录数据。域中所有域控制器均参与复制，并包含其域的所有目录信息的完整副本。对目录数据的任何更改均复制到域中的所有域控制器。

服务器基本信息

联系方式

- 系统管理员：孟庆洋，电话：<手机号已脱敏>，邮件：mengqingyang@cranewh.com

- 厂家技术支持：无

报修平台地址：无

账号：无

密码=<已脱敏>

服务器信息

服务器信息-表1

| 服务器 | DC59 | DC58 | DC56 |

| 系统信息 |  |  |  |

| 操作系统 | Windows 2022 STD | Windows 2022 STD | Windows 2022 STD |

| 主机名 | DC59 | DC58 | DC56 |

| IP | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 |

| GATEWAY | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> |

| 硬件信息 |  |  |  |

| vCPU | 8 | 16 | 2 |

| 内存 | 8G | 16G | 8G |

| 硬盘 | 100G+100G | 100G+100G | 100G+100G |

| VLAN | 1 | 1 | 198 |

| 宿主信息 |  |  |  |

| vCenter | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> |

| 群集 | WH-cluster | Production | Production |

服务器信息-表2

| 服务器 | RODC-DC11 | DNS100 |  |

| 系统信息 |  |  |  |

| 操作系统 | Windows 2022 STD | Windows 2022 STD |  |

| 主机名 | DC11 | DNS100 |  |

| IP | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 |  |

| GATEWAY | <IP地址已脱敏> | <IP地址已脱敏> |  |

| 硬件信息 |  |  |  |

| vCPU | 4 | 2 |  |

| 内存 | 8G | 8G |  |

| 硬盘 | 60G + 100G | 100G + 200G |  |

| VLAN | 1006 | 198 |  |

| 宿主信息 |  |  |  |

| vCenter | - | <IP地址已脱敏> |  |

| 群集 | <IP地址已脱敏> | Production |  |

应用信息

<IP地址已脱敏> AD/DNS/CA/IIS

| AD服务器：<IP地址已脱敏>:389服务名称：NTDS显示名称：Active Directory Domain Services可执行文件的路径：C:\WINDOWS\System32\lsass.exe启停：Services.msc配置文件：D:\Windows\NTDS\ ntds.dit日志目录：D:\Windows\NTDS\ |

| DNS服务器：<IP地址已脱敏>:53服务名称：DNS显示名称：DNS Server可执行文件的路径：C:\WINDOWS\system32\dns.exe启停：Services.msc配置文件：Active Directory和注册表日志目录：C:\Windows\System32\dns |

| CA服务器：<IP地址已脱敏>:59175服务名称：CertSvc显示名称：Active Directory Certificate Services可执行文件的路径：C:\WINDOWS\system32\certsrv.exe启停：Services.msc配置文件：D:\Windows\CA\CertLog\ whjt-DC59-CA.edb日志目录：D:\Windows\CA\CertLog |

| IIS服务器：<IP地址已脱敏>:80/443服务名称：W3SVC显示名称：World Wide Web 发布服务可执行文件的路径：C:\WINDOWS\system32\svchost.exe -k iissvcs启停：Services.msc配置文件：C:\Windows\System32\inetsrv\config\applicationHost.config日志目录：C:\inetpub\logs |

<IP地址已脱敏> AD/DNS

| AD服务器：<IP地址已脱敏>:389服务名称：NTDS显示名称：Active Directory Domain Services可执行文件的路径：C:\WINDOWS\System32\lsass.exe启停：Services.msc配置文件：D:\Windows\NTDS\ ntds.dit日志目录：D:\Windows\NTDS\ |

| DNS服务器：<IP地址已脱敏>:53服务名称：DNS显示名称：DNS Server可执行文件的路径：C:\WINDOWS\system32\dns.exe启停：Services.msc配置文件：Active Directory和注册表日志目录：C:\Windows\System32\dns |

<IP地址已脱敏> AD/DNS

| AD服务器：<IP地址已脱敏>:389服务名称：NTDS显示名称：Active Directory Domain Services可执行文件的路径：C:\WINDOWS\System32\lsass.exe启停：Services.msc配置文件：D:\Windows\NTDS\ ntds.dit日志目录：D:\Windows\NTDS\ |

| DNS服务器：<IP地址已脱敏>:53服务名称：DNS显示名称：DNS Server可执行文件的路径：C:\WINDOWS\system32\dns.exe启停：Services.msc配置文件：Active Directory和注册表日志目录：C:\Windows\System32\dns |

<IP地址已脱敏> RODC/DNS

| AD服务器：<IP地址已脱敏>:389服务名称：NTDS显示名称：Active Directory Domain Services可执行文件的路径：C:\WINDOWS\System32\lsass.exe启停：Services.msc配置文件：D:\Windows\NTDS\ ntds.dit日志目录：D:\Windows\NTDS\ |

| DNS服务器：<IP地址已脱敏>:53服务名称：DNS显示名称：DNS Server可执行文件的路径：C:\WINDOWS\system32\dns.exe启停：Services.msc配置文件：Active Directory和注册表日志目录：C:\Windows\System32\dns |

<IP地址已脱敏> DNS

| DNS服务器：<IP地址已脱敏>:53服务名称：DNS显示名称：DNS Server可执行文件的路径：C:\WINDOWS\system32\dns.exe启停：Services.msc配置文件：C:\Windows\System32\dns日志目录：C:\Windows\System32\dns |

系统优化配置

| 服务器 | 安装杀毒客户端 | 安装蓝鲸客户端 | 配置进程监控 | 限制登录配置 | 本地yum源配置 | 端口封堵 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐整机备份，30天 | 是 |

| <IP地址已脱敏> | 科力锐免代理备份，7天 | 是 |

| <IP地址已脱敏> | 科力锐免代理备份，7天 | 是 |

| <IP地址已脱敏> | 无 | -- |

| <IP地址已脱敏> | 科力锐免代理备份，7天 | 是 |

运维手册

服务点检

| 服务器 | 业务状态 | 备份状态 | 系统资源使用率 |

| <IP地址已脱敏> | AD DS / DNS / AD CS / IIS | 科力锐整机备份状态 | 利用蓝鲸监控查看负载 |

| <IP地址已脱敏> | AD DS / DNS | 科力锐免代理备份状态 | 利用蓝鲸监控查看负载 |

| <IP地址已脱敏> | AD DS / DNS | 科力锐整机备份状态 | 利用蓝鲸监控查看负载 |

| <IP地址已脱敏> | AD DS / DNS | 科力锐免代理备份状态 | 利用蓝鲸监控查看负载 |

| <IP地址已脱敏> | DNS | 科力锐免代理备份状态 | 利用蓝鲸监控查看负载 |

停机维护

开机

目前环境中存在5台设备（3台主域控+1台只读域控+1台DNS），需要注意的是涉及服务对象及服务区域不同，没有强依赖的开关机顺序，建议开机顺序如下：

| 优先级 | IP | 服务 | 服务对象 | 服务区域 |

| 1 | <IP地址已脱敏> | AD/DNS/CA | 服务器、终端 | AD（所有），DNS（长垣、江苏） |

| 1 | <IP地址已脱敏> | AD/DNS | 服务器 | 长垣 |

| 1 | <IP地址已脱敏> | RODC/DNS | 终端 | 郑州 |

| 2 | <IP地址已脱敏> | AD/DNS | 终端 | 长垣、江苏 |

| 3 | <IP地址已脱敏> | DNS | 国际链路 | 长垣 |

关机

根据实际情况按需关机，关机顺序：

| 优先级 | IP | 服务 |  |

| 1 | <IP地址已脱敏> | DNS |  |

| 2 | <IP地址已脱敏> | AD/DNS |  |

| 3 | <IP地址已脱敏> | RODC/DNS | 分支机构 |

| 4 | <IP地址已脱敏> | AD/DNS |  |

| 5 | <IP地址已脱敏> | AD/DNS/CA |  |

常见问题处理

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |
