# Linux下IBM HTTP SERVER访问日志接入方案

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [服务器日志收集]
issue_types: [reference]
tags: [engineer-doc, imported]
source_path: "D:\新建文件夹\业务维护清单\服务器日志收集\Linux下IBM HTTP SERVER访问日志接入方案.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：Linux下IBM HTTP SERVER访问日志接入方案.docx
- 原始路径：D:\新建文件夹\业务维护清单\服务器日志收集
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

Linux 下IBM HTTP SERVER访问日志接入方案

杭州安恒信息技术股份有限公司

二〇一八年八月

目录

1 使用logger发送web访问日志1

2 Linux syslog/rsyslog配置1

3 SOC接收IBM HTTP SERVER Access Log日志2

使用logger发送web访问日志

IBM HTTP SERVER配置文件修改

修改http.conf配置文件，注释原来CustomLog配置，新增新的CustomLog配置如下（注意：加上-t root选项，如果没加会误匹配到其它使用logger进行syslog发送的日志的解析规则）

CustomLog "| /usr/bin/logger -p LOCAL1.info -t root" combined

重新加载IBM HTTPSERVER配置文件

执行：/opt/IBM/HTTPServer/bin/apachectl graceful

Linux syslog/rsyslog配置

新增配置

#Save IBM HTTP SERVER ACCESS LOG

LOCAL1.info                                             /var/log/zane/accessLog.txt

重启syslog/rsyslog

执行：service rsyslog restart

SOC接收IBM HTTP SERVER Access Log日志

解析后数据
