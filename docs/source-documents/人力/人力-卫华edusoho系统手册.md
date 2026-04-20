# 卫华EduSoho系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [人力]
issue_types: [reference]
tags: [engineer-doc, imported]
source_path: "D:\新建文件夹\业务维护清单\人力\卫华EduSoho系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华EduSoho系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\人力
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华EduSoho系统 系统手册

摘要

该文档详细阐述了卫华EduSoho系统的维护、使用以及操作注意事项。

作者：孟庆洋

日期：2024年10月16日

版本：v1.0

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

EduSoho教培系统是一款专为学习场景研发的数字化培训解决方案，助力培训机构、企业、高校打造独立网校平台，提升教学效率和效果。EduSoho教培系统提供多种教学方式、运营工具、数据分析、AI能力，满足不同行业和场景的培训需求。

服务器基本信息

联系方式

- 系统管理员：孟庆洋，电话：<手机号已脱敏>，邮件：mengqingyang@cranewh.com

- 厂家技术支持：

报修平台地址：无

账号：无

密码=<已脱敏>

服务器信息

| 服务器 | <IP地址已脱敏> |  |  |

| 系统信息 |  |  |  |

| 操作系统 | CentOS Linux release 7.6.1810 |  |  |

| 主机名 | sh.craneweihua.com |  |  |

| IP | <IP地址已脱敏>/24 |  |  |

| GATEWAY | <IP地址已脱敏> |  |  |

| 硬件信息 |  |  |  |

| vCPU | 4 |  |  |

| 内存 | 8G |  |  |

| 硬盘 | 60G + 2T |  |  |

| VLAN | 198 |  |  |

| 宿主信息 |  |  |  |

| vCenter | <IP地址已脱敏> |  |  |

| 群集 | WH-cluster |  |  |

应用信息

<IP地址已脱敏>-EduSoho服务器

| MySQL服务：<IP地址已脱敏>:3306版本：MySQL 5.6.44 启停方式：systemctl mysqld [start | stop]应用目录：/usr/sbin/mysqld配置文件：/etc/my.cnf数据库目录：/var/lib/mysql日志目录：/var/log/mysqld.log |

| php-fpm服务：<IP地址已脱敏>:9000版本：PHP 7.0.33启停方式：systemctl php-fpm [start | stop]应用目录：/usr/sbin/mysqld配置文件：/etc/php-fpm.conf日志目录：/var/log/php-fpm/error.log |

| Nginx服务：<IP地址已脱敏>:80版本：Nginx 1.16.0启停方式：/usr/sbin/nginx [-s stop]应用目录：/usr/sbin/nginx配置文件：/etc/nginx/nginx.conf日志目录：/var/log/nginx/ |

系统优化配置

| 服务器 | 安装杀毒客户端 | 安装蓝鲸客户端 | 配置进程监控 | 限制登录配置 | 本地yum源配置 | 端口封堵 |

| <IP地址已脱敏> | 是 | 是 | 是 | 是 | 是 | 无 |

备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 科力锐整机备份，30天 | 是 |

运维手册

服务点检

| 服务器 | 业务状态 | 备份状态 | 系统资源使用率 |

| <IP地址已脱敏> | Nginx/php-fpm/MySQL | 科力锐备份状态 | 利用蓝鲸监控查看负载 |

停机维护

开机

单台应用无特别注意事项

关机

常见问题处理

变更管理

变更记录

| 服务器IP | 变更日期 | 变更说明 | 备注 |
