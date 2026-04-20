# 卫华RTX系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [rtx]
issue_types: [reference]
tags: [engineer-doc, imported, rtx]
source_path: "D:\新建文件夹\业务维护清单\RTX\卫华RTX系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华RTX系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\RTX
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华RTX系统 系统手册

摘要

该文档详细阐述了卫华RTX系统的维护、使用以及操作注意事项。

作者：孟庆洋

日期：2024年8月26日

版本：v1.0

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

RTX是腾讯公司推出的企业级即时通信平台。该平台定位于降低企业通信费用，增强企业内部沟通能力，改善企业与客户之间的沟通渠道，创造新兴的企业沟通文化，提高企业生产力。RTX平台的主要功能，包括企业内部实时信息交互、视频语音、企业短信中心等等。RTX平台具有很高的实用性、易用性、可管理性和安全性。除了底层采用128位对称加密技术之外，在实际应用中，RTX可以通过员工实名制、记录对外交互信息等措施，确保企业应用的通信安全。RTX可以利用SDK和API接口扩展第三方应用，如可以开发第三方短信网关、IM监控功能、用户数据同步等功能，为企业、ISV合作伙伴提供参考的整体解决方案。

服务器基本信息

联系方式

- 系统管理员：孟庆洋，电话：<手机号已脱敏>，邮件：mengqingyang@cranewh.com

- 厂家技术支持：无

报修平台地址：无

账号：无

密码=<已脱敏>

服务器信息

| 服务器 | <IP地址已脱敏>-RTX |  |  |

| 系统信息 |  |  |  |

| 操作系统 | Windows 2016 STD |  |  |

| 主机名 | RTX |  |  |

| IP | <IP地址已脱敏>/24 |  |  |

| GATEWAY | <IP地址已脱敏> |  |  |

| 硬件信息 |  |  |  |

| vCPU | 8 |  |  |

| 内存 | 16G |  |  |

| 硬盘 | 100G+100G |  |  |

| VLAN | 198 |  |  |

| 宿主信息 |  |  |  |

| vCenter | <IP地址已脱敏> |  |  |

| 群集 | WH-cluster |  |  |

应用信息

<IP地址已脱敏>-RTXServer

| RTX连接服务器：<IP地址已脱敏>:8000应用目录：D:\Tencent\RTXServer启停：D:\Tencent\RTXServer\bin\UserManager.exe配置文件：D:\Tencent\RTXServer\Config\目录下3个xml文件：ConfigCenter.xml、MultiLoginIP.xml、rtxserver.xml日志目录：D:\Tencent\RTXServer\Logs数据库路径：D:\Tencent\RTXServer\db |

| Tomcat服务：RTX注册申请与审核注册页面：代理地址：https://rtxapply.cranewh.com/rtx/user/userReg.jsp真实地址：http://<IP地址已脱敏>:9090/rtx/user/userReg.jsp（无访问路径不能加载组织架构）审核页面：代理地址：https://rtxapply.cranewh.com/rtx/user/user.jsp真实地址：http:// <IP地址已脱敏>:9090/rtx/user/user.jsp（登录：admin，密码=<已脱敏> |

系统优化配置

| 服务器 | 安装杀毒客户端 | 安装蓝鲸客户端 | 配置进程监控 | 限制登录配置 | 本地yum源配置 | 端口封堵 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | — | 无 |

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐整机备份，30天 | 是 |

运维手册

服务点检

| 服务器 | 业务状态 | 备份状态 | 系统资源使用率 |

| <IP地址已脱敏> | RTXServe（8000）和Tomcat（9090） | 科力锐整机备份状态 | 利用蓝鲸监控查看负载 |

停机维护

RTX Server

D:\Tencent\RTXServer\bin\UserManager.exe

Tomcat

启动：D:\tomcat-32\bin\startup.bat

停止：D:\tomcat-32\bin\shutdown.bat

常见问题处理

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |
