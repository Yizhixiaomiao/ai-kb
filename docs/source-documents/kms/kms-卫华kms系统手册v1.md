# 卫华KMS系统手册v1

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [kms]
issue_types: [reference]
tags: [engineer-doc, imported, kms]
source_path: "D:\新建文件夹\业务维护清单\KMS\卫华KMS系统手册v1.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华KMS系统手册v1.docx
- 原始路径：D:\新建文件夹\业务维护清单\KMS
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华KMS系统 操作手册

摘要

该文档详细阐述了卫华KMS系统的维护、使用以及操作注意事项。

作者：孙万明

日期： 2024年10月22日星期二

版本：v1

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

‌KMS（Key Management Service）服务器是现代企业中不可或缺的一部分，它负责激活和验证软件许可证，确保软件的合法使用。

服务器基本信息

联系方式

-系统管理员：孙万明; 电话：<手机号已脱敏>；邮箱：swm000796@gmail.com

-厂家技术支持：无

硬件信息

| 服务器 | KMS |

| 系统信息 |  |

| 操作系统 | CentOS Linux release 7.5.1804 (Core) |

| 主机名 | kms-124 |

| IP | <IP地址已脱敏>/24 |

| GATEWAY | <IP地址已脱敏> |

| 硬件信息 |  |

| vCPU | 1 |

| 内存 | 4G |

| 硬盘 | 50G |

| VLAN | 198 |

| 宿主信息 |  |

| vCenter | <IP地址已脱敏> |

| 群集 | Production |

应用信息

<IP地址已脱敏> KMS服务器

| 部署vlmcsdvlmcsd端口：1688vlmcsd启动文件：/kmsdata/binaries/Linux/intel/static/vlmcsd-x64-musl-static |

系统优化配置

| 服务器IP | 系统优化项 | 是否优化 |

| <IP地址已脱敏> | 安装杀毒客户端 | 是 |

|  | 安装蓝鲸客户端， | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

运维手册

服务信息

<IP地址已脱敏> KMS服务器

| 启停命令 | systemctl start vlmcsd && systemctl stop vlmcsd |

| 查看日志 | tail -n 50 -f /root/kms.log |

| 配置文件 | /kmsdata/binaries/Linux/intel/static/ |

| 进程端口 | 1688 |

停机维护

当遇到需要停机维护的时候，相关业务启停顺序如下

关闭业务顺序：systemctl stop vlmcsd

启动业务顺序：systemctl start vlmcsd

日常点检

| 服务器IP | 点检项目 | 点检结果 |

| <IP地址已脱敏> | 备份状态 | 无需备份 |

|  | 服务状态(vlmcsd) | 正常 |

|  | 资源使用情况 | 正常 |

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |

| <IP地址已脱敏> | 2024/10/22 | 制作启动控制程序，将进程服务交给 systemctl 纳管 |  |
