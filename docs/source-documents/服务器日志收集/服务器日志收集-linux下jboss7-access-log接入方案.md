# Linux下Jboss7 Access Log接入方案

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [服务器日志收集]
issue_types: [reference]
tags: [engineer-doc, imported]
source_path: "D:\新建文件夹\业务维护清单\服务器日志收集\Linux下Jboss7 Access Log接入方案.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：Linux下Jboss7 Access Log接入方案.docx
- 原始路径：D:\新建文件夹\业务维护清单\服务器日志收集
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

Linux下Jboss7 Access Log接入方案接入方案

杭州安恒信息技术股份有限公司

二〇一八年八月

目录

1 更改Jboss7配置文件1

2 日志发送1

3 SOC接收IBM HTTP SERVER Access Log日志2

更改Jboss7配置文件

(1)更改文件${JBOSS_HOME}/standalone/configuration/standalone.xml，在<virtual-server></virtual-server>内加入<access-log/>

原配置

修改后配置

(2) 重启Jboss

(3) 查看生成日志文件

日志发送

方案一：使用agent发送

使用默认agent发送文件配置发送Jboss7 Access Log日志文件，请参考agent发送文件配置

方案二：使用rsyslog发送${JBOSS_HOME}/standalone/log/default-host/*.log

（1）Rsyslog.conf配置

从文件中加载日志

# auditd audit.log

$InputFileName /usr/local/jboss-as-7.1.0.CR1b/standalone/log/default-host/*.log

$InputFileTag JbossAccessLog:

$InputFileStateFile /tmp/rsyslog_Jboss_Access.log

$InputFileSeverity info

$InputFileFacility local2

$InputRunFileMonitor

#load imfile module

#Note that the imfile module will need to have been loaded previously in the rsyslog configuration. This is the line responsible for that:

$ModLoad imfile

（2）配置远程log server

新增配置

#linux audit Log send to log server

Local0.info@<IP地址已脱敏>

（3）重启rsyslog

执行：service rsyslog restart

SOC接收IBM HTTP SERVER Access Log日志

解析后数据

原始日志：

| <150>May 10 18:00:11 localhost JbossAccessLog: <IP地址已脱敏> - - [10/五月/2016:10:00:07 +0000] "GET / HTTP/1.1" 304 0 |

| <150>May 10 18:00:11 localhost JbossAccessLog: <IP地址已脱敏> - - [10/五月/2016:10:00:07 +0000] "GET /jetty_banner.gif HTTP/1.1" 304 0 |

| <150>May 10 18:00:11 localhost JbossAccessLog: <IP地址已脱敏> - - [10/五月/2016:10:00:07 +0000] "GET / HTTP/1.1" 304 0 |

| <150>May 10 18:00:11 localhost JbossAccessLog: <IP地址已脱敏> - - [10/五月/2016:10:00:06 +0000] "GET /jetty_banner.gif HTTP/1.1" 304 0 |

| <150>May 10 18:00:11 localhost JbossAccessLog: <IP地址已脱敏> - - [10/五月/2016:10:00:06 +0000] "GET / HTTP/1.1" 304 0 |

| <150>May 10 18:00:11 localhost JbossAccessLog: <IP地址已脱敏> - - [10/五月/2016:10:00:06 +0000] "GET /jetty_banner.gif HTTP/1.1" 304 0 |
