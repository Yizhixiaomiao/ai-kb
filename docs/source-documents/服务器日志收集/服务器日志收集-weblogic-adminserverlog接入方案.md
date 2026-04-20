# Weblogic AdminServerLog接入方案

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [服务器日志收集]
issue_types: [reference]
tags: [engineer-doc, imported]
source_path: "D:\新建文件夹\业务维护清单\服务器日志收集\Weblogic AdminServerLog接入方案.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：Weblogic AdminServerLog接入方案.docx
- 原始路径：D:\新建文件夹\业务维护清单\服务器日志收集
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

Weblogic AdminServerLog接入方案

杭州安恒信息技术股份有限公司

二〇一八年八月

目录

1 文档说明1

2 LINUX-AGENT1

2.1 程序下载1

2.2 程序安装1

2.3 配置说明1

2.3.1 配置textAgent.xml文件1

2.3.2 日志接收服务器IP的配置文件2

2.4 程序重启3

2.5 SOC接收日志效果3

文档说明

此文档用于收集weblogic的文本型adminserverLog日志配置操作手册，文档搭配的客户端安装包名称为socAgent_linux_x86_64.tar.gz。

LINUX-AGENT

Linux操作系统上也有对应版本的日志采集代理，主要可以采集文本型日志、以及数据库表中的数据。

程序下载

说明：

（1）如果现场是S05版本的综合日志审计平台，则客户端安装包下载地址如下：

链接:https://pan.baidu.com/s/1BJKB-OegIHv_hE101lK7Tw  密码=<已脱敏>

（2）如果现场是S06版本的综合日志审计平台，请登录明御综合日志审计平台，到 [系统/系统管理/软件下载]页面，单击LINUX-AGENT蓝色字体进行下载。

程序安装

（1）将下载的LINUX-AGENT安装包上传到weblogic日志所在的服务器上。

（2）将LINUX-AGENT解压到任一英文目录下，解压后有一个名为socAgent_linux_x86_64的文件夹。该文件夹下有以下内容。

图表 21  linuxAgent安装目录下的文件内容

（3）到bin目录 下执行install.sh，会将linuxAgent注册成系统服务并在后台运行。

配置说明

配置textAgent.xml文件

严格按照如下内容修改agent/conf/textAgent.xml文件。

<?xml version="1.0" encoding="UTF-8"?>

<trigger>

<config>

<logPath device="weblogic_37" lineMergeRegex="####" lineMergeMaxSize="1024" >/home/weblogic/Oracle/Middleware/user_projects/domains/base_domain/servers/AdminServer/logs/AdminServer.log</logPath>

<sendOldLogSwitch>on</sendOldLogSwitch>

<sendOldLogLineCount>1</sendOldLogLineCount>

</config>

<logFilter status="off">

<filter target="/var/log/secure" rule="localhost" mode="false" status="on"/>

</logFilter>

<logAttackCheck status="off">

<items target="/root/123/*.txt" mode="false" status="on"/>

</logAttackCheck>

</trigger>

说明：

device

资产别名：需要用到资产重识别时添加此字段，如果不用不需要添加此字段。

lineMergeRegex

多行日志合并正则表达式：通过样例看出DB2 DiagLog为多行事件，事件以2015-09-25-00.39.57.683446+480此类时间头部开始，定义正则对日志进行合并。

正则：####

logPath

weblogic AdminserverLog日志文件：需要监控的weblogic AdminserverLog 日志文件，如：/home/weblogic/Oracle/Middleware/user_projects/domains/base_domain/servers/AdminServer/logs/AdminServer.log

日志接收服务器IP的配置文件

指定linuxAgent采集的日志发送到哪台服务器上，这时需要配置agent.conf，修改agent.conf文件中的agentServer.ip和apmServer.ip(若不需要监控性能，则默认即可)地址为日志审计平台地址，文件中其他内容可以默认。

文件中各个配置项的说明见表格 21。

表格 21  agent.conf配置项说明

| 配置项 | 说明 |

| agentServer=true | 日志发送开关 |

| apmServer=true | 性能采集开关 |

| agentServer.ip=<IP地址已脱敏> | 采集器 IP地址 |

| agentServer.syslogPort=514 | 采集器 syslog协议接收端口，一般为 514 |

| agentServer.logSendCharSet=utf8 | 日志发送编码，当收集的日志是乱码时，可以修改成gbk |

| agentServer.logReaderCharSet=utf8 | 日志读取编码，当收集的日志是乱码时，可以修改成gbk |

| agentServer.sendLogInterval=60 | 每条日志发送的时间间隔，单位毫秒 |

| agentServer.logDetectInterval=5 | 文件型日志监视间隔，单位秒 |

| agentServer.systemStatusDetectInterval=120 | Agent 自身的心跳事件发送间隔，单位秒 |

| agentServer.sendSignalInterval=300 | Agent 自身的心跳事件发送间隔，单位秒 |

| agentServer.limitResourceMode=on | CPU 占用模式开关 |

| apmServer.ip=<IP地址已脱敏> | 性能采集接收地址 |

| apmServer.ssl.enable=on | 当采集器界面以 https方式访问时，这里设置成 on；当采集器界面以 http方式访问时，这里设置成off |

| apmServer.port=443 | 采集器 http协议接收端口：当采集器端没有特别配置时，使用采集器界面访问端口。界面以 https方式访问时，这里设置成 443；界面以http方式访问时，这里设置成 80 |

| window.event.log.enable=false(如果是true，则改成false) | Windows 事件采集相关（无需配置） |

| window.event.log.sleep=10 |  |

| window.event.log.types=Application,System,Security,DNS Server,Directory Service,File Replication Service,HardwareEvents,Internet Explorer,Key Management Service,Windows PowerShell |  |

| agentServer.updatePort=443 | Agent 在线升级配置项，默认即可 |

| agentServer.updateSSLEnable=on |  |

| agentServer.updateInterval=3 |  |

| agentServer.updateUserName=abc |  |

| agentServer.updatePassword=<已脱敏> |  |

程序重启

当各个配置文件有改动时，需要重启agent，修改项才会生效。

到linuxAgent安装目录的bin目录下，执行sh restart.sh或./restart.sh文件，即完成重启操作。

SOC接收日志效果

（1）通过正则表达式对weblogic AdminserverLog日志进行合并后的效果如下：

（2）对weblogic AdminserverLog 日志解析后效果：
