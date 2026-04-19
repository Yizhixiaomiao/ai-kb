# 数据库状态、宕机或表空间告警处理指南

```yaml
status: usable
type: troubleshooting
risk_level: high
review_required: true
asset_types: [database, server]
systems: [mysql, oracle]
issue_types: [database-down, tablespace, connection-failed]
tags: [database, mysql, oracle, tablespace, availability]
```

## 适用范围

- 适用于 MySQL 宕机、Oracle 数据库状态监控、数据库连接异常、表空间监控等告警。
- 适用于规则名称包含“数据库状态监控”“数据库表空间监控”“MySQL宕机”“Mysql 宕机”等场景。

## 常见现象

- 数据库实例不可连接或连接数异常。
- 数据库状态监控失败。
- Oracle 表空间使用率过高。
- 应用报数据库连接失败、查询超时或写入失败。

## 判断依据

- 先区分数据库实例宕机、网络不可达、账号权限、连接池耗尽、磁盘空间或表空间问题。
- MySQL 备份恢复参考 MySQL 和 XtraBackup 手册；Oracle 备份恢复参考 Oracle 手册。

## 处理步骤

1. 确认数据库类型、实例、业务系统、告警指标和影响范围。
2. 查看数据库进程、端口、连接状态、错误日志、磁盘空间和最近变更。
3. Oracle 表空间告警需确认表空间使用率、数据文件自动扩展、剩余磁盘和增长趋势。
4. MySQL 宕机需确认服务状态、错误日志、磁盘、内存和是否存在崩溃恢复。
5. 涉及重启、扩容、恢复、删除数据文件、调整表空间前，必须确认备份和业务窗口。
6. 如涉及数据恢复，按对应数据库备份恢复手册执行，并先在测试环境验证。
7. 记录实例、根因、处理动作、恢复时间和后续容量或高可用优化建议。

## 常用指令

- systemctl status mysqld -- ?? MySQL ??????????
- systemctl status mysql -- ?? MySQL ??????????????????????
- mysqladmin ping -h <host> -P <port> -u <user> -p -- ?? MySQL ?????????????
- mysql -h <host> -P <port> -u <user> -p -e "show processlist;" -- ?? MySQL ????????? SQL??????
- tail -n 200 /var/log/mysqld.log -- ?? MySQL ????????????
- lsnrctl status -- ?? Oracle ??????????
- sqlplus / as sysdba -- ??? SYSDBA ?? Oracle??????????
- select status from v$instance; -- ?? Oracle ??????????
- select tablespace_name, round(used_percent,2) used_percent from dba_tablespace_usage_metrics order by used_percent desc; -- ?? Oracle ????????????
- df -hT -- ????????????????????

## 验证方式

- 数据库实例状态正常，应用可连接。
- 表空间、磁盘、连接数和错误日志恢复正常。
- 关键业务 SQL 或应用健康检查通过。

## 注意事项

- 数据库操作属于高风险操作，不允许直接照抄命令执行。
- 涉及数据文件、恢复、重启和扩容必须走审批、备份和回退流程。
- 表空间告警不能只扩容，还应分析增长来源和保留策略。
