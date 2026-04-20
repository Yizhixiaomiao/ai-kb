# 卫华 HANA  HA维护文档

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [hana]
issue_types: [reference]
tags: [engineer-doc, imported, hana]
source_path: "D:\新建文件夹\业务维护清单\HANA\卫华 HANA  HA维护文档.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华 HANA  HA维护文档.docx
- 原始路径：D:\新建文件夹\业务维护清单\HANA
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华

HANA SR HA维护手册

Dell IDS

联系人

| 联系人 | 职务 | 邮箱 |

| Yang, Ji | FE | Ji_Y@dell.com |

版本

| 版本 | 日期 | 作者 | 职务 |

| V1.0 | 2020-07-15 | Yang, Ji | FE |

系统架构及原理

Scale-up HANA的HA通过HANA的system replication及SUSE 的HA extension for SAP HANA來完成，HANA SR复制数据的复制（从primary到secondary），SUSE HA负责virtual IP的切换以及HANA节点角色的提升（secondary to primary）

正常运行状态时，一个节点为Primary，另一个节点为Secondary，同时将virtual IP挂在primary节点上让应用服务器访问

当Primary发生故障时，SUSE HAE自动将vIP切换至Secondary，同時也将Secondary的HANA DB 提升成Primary

在node 1（此时为备节点）故障修复后，可将其注册成node 2（此时为主节点）的secondary，并重新回到正常系统复制的状态

日常维护操作

注意事项:

HANA system Replication 已经处于Suse HAE cluster的管理之下，日常的维护通过HAE来进行，不要在HANA DB层面执行stop和start的动作,会造成切换的集群的切换

如果需要执行HANA启停的日常维护，首先将HANA resource改为维护状态：

在root下执行crm resource maintenance rsc_SAPHana_GHP_HDB00

调整完成后恢复HANA原有的复制状态

在root下执行crm resource maintenance rsc_SAPHana_GHP_HDB00 off

关闭集群

关闭HANA 资源：root下命令行执行 crm resource stop rsc_SAPHana_GHP_HDB00

同时监控状态:crm_mon -r，直至rsc_SAPHana_GHP_HDB00显示为stop

关闭HANA拓扑资源：root下命令行执行crm resource stop rsc_SAPHanaTopology_GHP_HDB00

确认HANA相关资源关闭：root下执行crm resource list

关闭集群服务：systemctl stop pacemaker(两个节点root账户分别执行)

关闭操作系统：shutdown -h now

开启集群

服务器开机：电源接通，打开服务器电源

开启集群服务：systemctl start pacemaker(两个节点root账户分别执行)

开启HANA 拓扑资源：root下命令行执行crm resource start rsc_SAPHanaTopology_GHP_HDB00

开启HANA资源：root下命令行执行: crm resource start rsc_SAPHana_GHP_HDB00

确认启动完成：root下命令行执行:crm_mon -r

HANAPRD01 HANA Crash修复 (此时HANAPRD02已经被集群自动提升为主)

HANAPRD01向HANAPRD02注册复制关系

ghpadm@hanaprd01:/usr/sap/GHP/HDB00> hdbnsutil -sr_register --remoteHost=hanaprd02 --remoteInstance=00 --replicationMode=sync --operationMode=logreplay --name=SITEA

adding site ...

nameserver hanaprd01:30001 not responding.

collecting information ...

registered at <IP地址已脱敏> (hanaprd02)

updating local ini files ...

done.

cleanup HANAPRD01节点的hana资源

root下执行:crm resource cleanup rsc_SAPHana_GHP_HDB00 hanaprd01

HANAPRD01 Server Crash修复 (此时HANAPRD02已经被集群自动提升为主)

HANAPRD01向HANAPRD02注册复制关系

ghpadm@hanaprd01:/usr/sap/GHP/HDB00> hdbnsutil -sr_register --remoteHost=hanaprd02 --remoteInstance=00 --replicationMode=sync --operationMode=logreplay --name=SITEA

adding site ...

nameserver hanaprd01:30001 not responding.

collecting information ...

registered at <IP地址已脱敏> (hanaprd02)

updating local ini files ...

done.

HANAPRD01开启集群

root下执行:systemctl start pacemaker

HANAPRD02  HANA Crash修复 (此时HANAPRD01已经被集群自动提升为主)

HANAPRD02向HANAPRD01注册复制关系

ghpadm@hanaprd02:/usr/sap/GHP/HDB00> hdbnsutil -sr_register --remoteHost=hanaprd01 --remoteInstance=00 --replicationMode=sync --operationMode=logreplay --name=SITEB

adding site ...

nameserver hanaprd02:30001 not responding.

collecting information ...

registered at <IP地址已脱敏> (hanaprd01)

updating local ini files ...

done.

cleanup HANAPRD02节点的hana资源

root下执行:crm resource cleanup rsc_SAPHana_GHP_HDB00 HANAPRD02

HANAPRD02  Server Crash修复 (此时HANAPRD01已经被集群自动提升为主)

HANAPRD02向HANAPRD01注册复制关系

ghpadm@hanaprd02:/usr/sap/GHP/HDB00> hdbnsutil -sr_register --remoteHost=hanaprd01 --remoteInstance=00 --replicationMode=sync --operationMode=logreplay --name=SITEB

adding site ...

nameserver hanaprd02:30001 not responding.

collecting information ...

registered at <IP地址已脱敏> (hanaprd01)

updating local ini files ...

done.

HANAPRD02开启集群

root下执行:systemctl start pacemaker

手动迁移HANA到第二节点

Hana资源更改为维护模式：crm resource maintenance rsc_SAPHana_GHP_HDB00

停止HANA（ghpadm账号）：HDB stop

第二节点HANA手动执行takeover(ghpadm账号): hdbnsutil -sr_takeover

第一节点手动注册复制关系到第二节点(ghpadm账户):

hdbnsutil -sr_register --remoteHost=hanaprd02 --remoteInstance=00 --replicationMode=sync --operationMode=logreplay --name=SITEA

第一节点启动HANA，复制关系恢复（ghpadm账号）:HDB start

Cleanup HANA资源:crm resource cleanup rsc_SAPHana_GHP_HDB00

HANA资源退出维护模式: crm resource maintenance rsc_SAPHana_GHP_HDB00 off

HANA升级，集群操作步骤

Hana资源更改为维护模式: crm resource maintenance rsc_SAPHana_GHP_HDB00

节点设置为维护模式:

crm node maintenance hanaprd01

crm node maintenance hanaprd02

执行HANA升级

节点设置为ready:

crm node ready hanaprd01

crm node ready hanaprd02

cleanup HANA资源:crm resource cleanup rsc_SAPHana_GHP_HDB00

HANA资源退出维护模式: crm resource maintenance rsc_SAPHana_GHP_HDB00 off

其他常用维护命令

集群状态检查

crm_mon -r

HANA SR状态检查 :ghpadm账号下执行：

python $DIR_INSTANCE/exe/python_support/systemReplicationStatus.py

HANA状态检查：:Prdadm账号下执行：

sapcontrol -nr 00 -function GetProcessList

参考资料

SAP HANA System Replication on SLES for SAP Applications Setup Guide (SUSE)

High Availability and Disaster Recovery for SAP HANA with SUSE Linux Enterprise Server for SAP Applications (SUSE)

SUSE Linux Enterprise High Availability Extension - High Availability Guide (SUSE)

SAP HANA Administration Guide (SAP)

Automate SAP HANA System Replication with SLES for SAP Applications (SAP, http://scn.sap.com/docs/DOC-56278)
