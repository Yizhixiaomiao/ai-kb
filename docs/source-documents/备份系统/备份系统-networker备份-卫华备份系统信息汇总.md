# 卫华备份系统信息汇总

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [备份系统]
issue_types: [reference]
tags: [engineer-doc, imported, networker, backup]
source_path: "D:\新建文件夹\业务维护清单\备份系统\networker备份\卫华备份系统信息汇总.xlsx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华备份系统信息汇总.xlsx
- 原始路径：D:\新建文件夹\业务维护清单\备份系统\networker备份
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

## Sheet1

| nocatalog msglog '/nsr/logs/rman_Incr.log' append |

| 序列号 | 应用系统名称 | IP | oS | hostname |  | 数据库备份内容 | 数据库账号密码 | 备注 |

| 股份OA | <IP地址已脱敏> | linux | whgfora | whgf.com | oracle@dbserver | nwbak/whnwbak | 1-6 增量，7 full 1:00 |

| 集团OA | <IP地址已脱敏> | linux | whjtora | whjt.com | oracle@dbserver1 | nwbak/whnwbak | 1-6 增量，7 full 1:20 |

| crm | <IP地址已脱敏> | linux | crmdb | crmdb.com | oracle@orcl | nwbak/whnwbak | 1-6 增量，7 full 1:30 |

| erp | <IP地址已脱敏> | linux | ncdb2 | cranewh.com | oracle@NCdb2 | nwbak/whnwbak | 1-6 增量，7 full 2:00 | /u01/oracle/product/11.2.0/dbhome_1/network/admin |

| MySQL | <IP地址已脱敏> | linux | oa116 | oa116.com | /home/backup_mysql | nwbak/whnwbak | 1-6增量，7 Full 1:40 |

| SQLserver | <IP地址已脱敏> | win | WIN-RND47FJFTEL | MSSQL | administraor/A123456. | 1-6 增量，7 Full 5:00 |

| 11 | vcenter | whgf.com | <IP地址已脱敏> | administrator@whgf.com/P@ssw0rd |

| 12 | DD3300 | dd3300.whgf.com | 管理:<IP地址已脱敏>（ethMa） 业务:<IP地址已脱敏>. 41 （数据传输） iDRC:<IP地址已脱敏>--24--254 | DD3300:sysadmin/P@ssw0rd iDRC:root/P@ssw0rd |  |

| 13 | Networker NMC | nmc | <IP地址已脱敏>（备份服务器地址） | 服务器：administrator/P@ssw0rd NMC：administrator/Mima@1234 |  |

| 14 | AVE | ave | <IP地址已脱敏>（虚拟化备份服务器） | admin/Password_123 root/Password_123 | dpnctl stop/start | admin/Passw0rd.（末位小数点）Password_123 root/Passw0rd.（末位小数点 ） |  |

| 15 | AVEProxy | aveproxy | <IP地址已脱敏>（AVE 代理主机） | admin/avam@r root/avam@r |  |

## LAC

| LAC：YFNNJQBYTDN0LXYBXS62 |
