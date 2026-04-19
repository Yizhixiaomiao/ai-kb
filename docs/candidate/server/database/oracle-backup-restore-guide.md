# Oracle 数据库备份与恢复参考手册

```yaml
status: usable
type: reference
risk_level: high
review_required: true
source: imported-manual
source_path: D:/Work/工作文档/知识库构建/服务器运维相关/oracle-backup-restore-guide.md
asset_types: [database, server]
systems: [oracle, rman]
issue_types: [backup, restore, data-recovery]
tags: [oracle, rman, expdp, impdp, backup, restore]
```

## 适用范围

- 适用于 Oracle RMAN、Data Pump、冷备、恢复验证和常见错误处理。
- 适合作为 Oracle 备份恢复、迁移和对象级恢复前的操作参考。

## 常见现象

- 需要执行全量、增量、归档日志或对象级备份。
- 需要恢复数据库、表空间、Schema、表或导入导出数据。
- RMAN、expdp、impdp 或归档日志相关错误。

## 处理步骤

1. 确认数据库版本、实例名、归档模式、备份策略、恢复目标和停机窗口。
2. 恢复前检查数据库状态、备份可用性、归档完整性和剩余空间。
3. 按场景参考原始手册中的 RMAN、Data Pump、冷备、恢复和常见错误章节。
4. 生产恢复必须先在测试环境验证，涉及覆盖数据前必须取得业务确认。
5. 记录备份片、SCN/时间点、恢复命令、日志和验证结果。

## 验证方式

- RMAN validate 或恢复验证通过。
- 目标对象、表空间或数据库状态正常。
- 应用连接和关键业务 SQL 验证正常。

## 注意事项

- 本文属于服务器、数据库或网络设备高风险运维参考，生产环境操作前必须完成审批、备份、维护窗口和回退方案确认。
- 本文中的命令和参数来自通用手册，执行前必须替换为本公司实际环境，并先在测试环境验证。
- 涉及删除、覆盖、重启、恢复、扩缩容、路由/ACL 变更、证书/密钥、数据库恢复等动作时，不允许直接照抄执行。
- 手册中的示例密码、Token 和密钥已做脱敏处理；不得在知识库中保存真实凭据。

## 原始手册

以下内容为导入的原始手册正文，供工程师查阅细节。

# Oracle 数据库备份与恢复完全指南

> 📝 版本：Oracle 12c/18c/19c/21c  
> ⚠️ 生产环境操作前请先在测试环境验证！

---

## 📚 目录

1. [备份方式概览](#1-备份方式概览)
2. [RMAN 备份（推荐）](#2-rman-备份推荐)
3. [RMAN 恢复](#3-rman-恢复)
4. [数据泵 expdp/impdp](#4-数据泵-expdpimpdp)
5. [传统导出导入 exp/imp](#5-传统导出导入-expimp)
6. [冷备份（脱机备份）](#6-冷备份脱机备份)
7. [热备份（联机备份）](#7-热备份联机备份)
8. [Flashback 闪回技术](#8-flashback-闪回技术)
9. [定时备份脚本](#9-定时备份脚本)
10. [常见错误与解决方案](#10-常见错误与解决方案)
11. [最佳实践](#11-最佳实践)

---

## 1. 备份方式概览

| 方式 | 工具 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **RMAN** | rman | 增量、并行、自动管理 | 需要学习 | **生产环境首选** |
| **数据泵** | expdp/impdp | 灵活、可跨平台 | 逻辑备份、慢 | 迁移、部分导出 |
| **传统导出** | exp/imp | 兼容旧版本 | 已淘汰 | 老系统维护 |
| **冷备份** | cp/os 命令 | 简单可靠 | 需停机 | 小库、维护窗口 |
| **热备份** | ALTER TABLESPACE | 不停机 | 复杂、需归档 | 7x24 系统 |
| **闪回** | FLASHBACK | 秒级恢复 | 有限制 | 误操作恢复 |

---

## 2. RMAN 备份（推荐）

### 2.1 连接 RMAN

```bash
# 本地连接
rman target /

# 远程连接
rman target sys/<password>@orcl

# 带恢复目录
rman target sys/<password>@orcl catalog rman_user/password@catdb
```

### 2.2 查看数据库信息

```sql
RMAN> SHOW ALL;                    -- 显示所有配置
RMAN> REPORT SCHEMA;               -- 报告数据库结构
RMAN> LIST BACKUP;                 -- 列出所有备份
RMAN> LIST BACKUP SUMMARY;         -- 备份摘要
RMAN> LIST ARCHIVELOG ALL;         -- 列出归档日志
RMAN> CROSSCHECK BACKUP;           -- 交叉检查备份
RMAN> DELETE EXPIRED BACKUP;       -- 删除过期备份记录
```

### 2.3 全量备份

```sql
-- 备份整个数据库
RMAN> BACKUP DATABASE;

-- 备份数据库 + 归档日志
RMAN> BACKUP DATABASE PLUS ARCHIVELOG;

-- 备份到指定位置
RMAN> BACKUP DATABASE FORMAT '/backup/oracle/%U.bkp';

-- 备份为镜像副本（类似物理拷贝）
RMAN> BACKUP AS COPY DATABASE;

-- 压缩备份
RMAN> BACKUP DATABASE COMPRESS;

-- 并行备份（4 通道）
RMAN> CONFIGURE DEVICE TYPE DISK PARALLELISM 4;
RMAN> BACKUP DATABASE;
```

### 2.4 增量备份

```sql
-- 0 级增量（相当于全量）
RMAN> BACKUP INCREMENTAL LEVEL 0 DATABASE;

-- 1 级增量（差异增量，默认）
RMAN> BACKUP INCREMENTAL LEVEL 1 DATABASE;

-- 1 级累积增量（基于 0 级）
RMAN> BACKUP INCREMENTAL LEVEL 1 CUMULATIVE DATABASE;

-- 常用策略：周日 0 级，周一到周六 1 级
-- 周日
RMAN> BACKUP INCREMENTAL LEVEL 0 DATABASE PLUS ARCHIVELOG;
-- 周一至周六
RMAN> BACKUP INCREMENTAL LEVEL 1 DATABASE PLUS ARCHIVELOG;
```

### 2.5 备份特定对象

```sql
-- 备份表空间
RMAN> BACKUP TABLESPACE SYSTEM;
RMAN> BACKUP TABLESPACE USERS;

-- 备份数据文件
RMAN> BACKUP DATAFILE 1;
RMAN> BACKUP DATAFILE '/u01/app/oracle/oradata/orcl/users01.dbf';

-- 备份控制文件
RMAN> BACKUP CURRENT CONTROLFILE;

-- 备份 SPFILE
RMAN> BACKUP SPFILE;

-- 备份归档日志
RMAN> BACKUP ARCHIVELOG ALL;

-- 备份最近 1 小时的归档日志
RMAN> BACKUP ARCHIVELOG FROM TIME 'SYSDATE-1/24';
```

### 2.6 配置保留策略

```sql
-- 保留最近 7 天的备份
RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;

-- 保留每个数据文件的 2 份备份
RMAN> CONFIGURE RETENTION POLICY TO REDUNDANCY 2;

-- 查看保留策略
RMAN> SHOW RETENTION POLICY;

-- 删除不再需要的备份
RMAN> DELETE OBSOLETE;

-- 删除指定时间之前的备份
RMAN> DELETE BACKUP COMPLETED BEFORE 'SYSDATE-7';
```

### 2.7 配置归档日志删除策略

```sql
-- 备份后删除归档日志
RMAN> CONFIGURE ARCHIVELOG DELETION POLICY TO BACKED UP 1 TIMES TO DEVICE TYPE DISK;

-- 手动删除已备份的归档日志
RMAN> BACKUP ARCHIVELOG ALL DELETE INPUT;
```

### 2.8 备份验证

```sql
-- 验证数据库是否可备份
RMAN> BACKUP VALIDATE DATABASE;

-- 检查逻辑损坏
RMAN> BACKUP VALIDATE CHECK LOGICAL DATABASE;

-- 验证特定数据文件
RMAN> BACKUP VALIDATE DATAFILE 1;
```

---

## 3. RMAN 恢复

### 3.1 恢复前准备

```bash
# 检查数据库状态
sqlplus / as sysdba
SQL> SELECT status FROM v$instance;

# 查看可恢复的备份
RMAN> LIST BACKUP SUMMARY;
RMAN> REPORT NEED BACKUP;
```

### 3.2 完全恢复（数据库关闭）

```sql
-- 启动到 mount 状态
RMAN> STARTUP MOUNT;

-- 恢复数据库
RMAN> RESTORE DATABASE;

-- 应用归档日志恢复
RMAN> RECOVER DATABASE;

-- 打开数据库
RMAN> ALTER DATABASE OPEN;
```

### 3.3 完全恢复（表空间级别）

```sql
-- 离线表空间
RMAN> SQL 'ALTER TABLESPACE users OFFLINE IMMEDIATE';

-- 恢复表空间
RMAN> RESTORE TABLESPACE users;
RMAN> RECOVER TABLESPACE users;

-- 在线表空间
RMAN> SQL 'ALTER TABLESPACE users ONLINE';
```

### 3.4 不完全恢复（时间点恢复）

```sql
-- 恢复到指定时间
RMAN> STARTUP MOUNT;
RMAN> SET UNTIL TIME "TO_DATE('2026-03-10 11:00:00','YYYY-MM-DD HH24:MI:SS')";
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN RESETLOGS;

-- 恢复到指定 SCN
RMAN> STARTUP MOUNT;
RMAN> SET UNTIL SCN 1234567;
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN RESETLOGS;

-- 恢复到指定日志序列
RMAN> STARTUP MOUNT;
RMAN> SET UNTIL SEQUENCE 100 THREAD 1;
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN RESETLOGS;
```

⚠️ **注意：** `RESETLOGS` 会重置日志序列，之后需要重新做全量备份！

### 3.5 恢复控制文件

```sql
-- 从自动备份恢复
RMAN> STARTUP NOMOUNT;
RMAN> SET DBID=1234567890;  -- 如果不知道，从备份文件名找
RMAN> RESTORE CONTROLFILE FROM AUTOBACKUP;

-- 从指定文件恢复
RMAN> RESTORE CONTROLFILE FROM '/backup/oracle/controlfile_backup.bkp';

-- 挂载并恢复数据库
RMAN> ALTER DATABASE MOUNT;
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN RESETLOGS;
```

### 3.6 恢复 SPFILE

```sql
-- 从自动备份恢复
RMAN> STARTUP NOMOUNT FORCE;
RMAN> RESTORE SPFILE FROM AUTOBACKUP;

-- 从指定文件恢复
RMAN> RESTORE SPFILE FROM '/backup/oracle/spfile_backup.bkp';

-- 重启使配置生效
RMAN> SHUTDOWN IMMEDIATE;
RMAN> STARTUP;
```

### 3.7 恢复单个数据文件

```sql
-- 离线数据文件
RMAN> SQL 'ALTER DATABASE DATAFILE 4 OFFLINE';

-- 恢复数据文件
RMAN> RESTORE DATAFILE 4;
RMAN> RECOVER DATAFILE 4;

-- 在线数据文件
RMAN> SQL 'ALTER DATABASE DATAFILE 4 ONLINE';
```

### 3.8 块级别恢复（最小化停机）

```sql
-- 恢复损坏的块
RMAN> BLOCKRECOVER DATAFILE 4 BLOCK 123,456;

-- 从备用数据库恢复块
RMAN> BLOCKRECOVER DATAFILE 4 BLOCK 123 FROM SERVICE standby_db;
```

---

## 4. 数据泵 expdp/impdp

### 4.1 创建目录对象

```sql
-- 以 sysdba 登录
sqlplus / as sysdba

-- 创建目录
CREATE DIRECTORY backup_dir AS '/backup/oracle/dump';

-- 授权
GRANT READ, WRITE ON DIRECTORY backup_dir TO system;

-- 查看目录
SELECT * FROM dba_directories WHERE directory_name = 'BACKUP_DIR';
```

### 4.2 导出（expdp）

```bash
# 导出整个数据库
expdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full_%U.dmp LOGFILE=full.log

# 导出特定用户（Schema）
expdp system/<password> SCHEMAS=hr,oe DIRECTORY=backup_dir DUMPFILE=schema_%U.dmp LOGFILE=schema.log

# 导出特定表
expdp system/<password> TABLES=hr.employees,hr.departments DIRECTORY=backup_dir DUMPFILE=tables.dmp

# 导出表空间
expdp system/<password> TABLESPACES=users,tools DIRECTORY=backup_dir DUMPFILE=tbs.dmp

# 按查询条件导出
expdp system/<password> TABLES=hr.employees QUERY=hr.employees:"WHERE department_id=10" DIRECTORY=backup_dir DUMPFILE=query.dmp

# 并行导出（4 进程）
expdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full_%U.dmp PARALLEL=4

# 压缩导出
expdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full.dmp COMPRESSION=ALL

# 只导出元数据（结构）
expdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=metadata.dmp CONTENT=METADATA_ONLY

# 只导出数据
expdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=data.dmp CONTENT=DATA_ONLY

# 排除特定对象
expdp system/<password> SCHEMAS=hr DIRECTORY=backup_dir DUMPFILE=hr.dmp EXCLUDE=STATISTICS

# 只导出特定对象
expdp system/<password> SCHEMAS=hr DIRECTORY=backup_dir DUMPFILE=hr.dmp INCLUDE=TABLE:"IN ('EMPLOYEES','DEPARTMENTS')"
```

### 4.3 导入（impdp）

```bash
# 导入整个数据库
impdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full_%U.dmp LOGFILE=import.log

# 导入特定用户
impdp system/<password> SCHEMAS=hr DIRECTORY=backup_dir DUMPFILE=schema.dmp LOGFILE=import.log

# 导入到不同用户（重映射）
impdp system/<password> REMAP_SCHEMA=hr:hr_new DIRECTORY=backup_dir DUMPFILE=schema.dmp

# 导入到不同表空间
impdp system/<password> REMAP_TABLESPACE=users:users_new DIRECTORY=backup_dir DUMPFILE=schema.dmp

# 重命名表
impdp system/<password> REMAP_TABLE=hr.emp:hr.employees DIRECTORY=backup_dir DUMPFILE=tables.dmp

# 只导入表结构
impdp system/<password> TABLES=hr.employees DIRECTORY=backup_dir DUMPFILE=tables.dmp CONTENT=METADATA_ONLY

# 只导入数据
impdp system/<password> TABLES=hr.employees DIRECTORY=backup_dir DUMPFILE=tables.dmp CONTENT=DATA_ONLY

# 并行导入
impdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full_%U.dmp PARALLEL=4

# 跳过已存在的表
impdp system/<password> TABLES=hr.employees DIRECTORY=backup_dir DUMPFILE=tables.dmp TABLE_EXISTS_ACTION=SKIP

# 追加数据
impdp system/<password> TABLES=hr.employees DIRECTORY=backup_dir DUMPFILE=tables.dmp TABLE_EXISTS_ACTION=APPEND

# 替换表（先 DROP 再创建）
impdp system/<password> TABLES=hr.employees DIRECTORY=backup_dir DUMPFILE=tables.dmp TABLE_EXISTS_ACTION=REPLACE

# 从多个文件导入
impdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full_%U.dmp LOGFILE=import.log
```

### 4.4 网络导入导出（不生成文件）

```bash
# 从远程数据库直接导入
impdp system/<password> NETWORK_LINK=remote_db SCHEMAS=hr DIRECTORY=backup_dir DUMPFILE=network.dmp

# 导出到远程数据库
expdp system/<password> SCHEMAS=hr NETWORK_LINK=remote_db DIRECTORY=backup_dir DUMPFILE=network.dmp
```

### 4.5 查看作业状态

```sql
-- 查看正在运行的数据泵作业
SELECT * FROM dba_datapump_jobs;

-- 查看作业进度
SELECT sid, serial#, username, opname,sofar,totalwork FROM v$session_longops WHERE opname LIKE '%Data Pump%';
```

---

## 5. 传统导出导入 exp/imp

⚠️ **注意：** 已淘汰，仅用于兼容旧版本

```bash
# 导出
exp system/<password> FILE=/backup/exp.dmp FULL=Y LOG=/backup/exp.log

# 导入
imp system/<password> FILE=/backup/exp.dmp FULL=Y LOG=/backup/imp.log IGNORE=Y

# 导出特定用户
exp system/<password> FILE=hr.dmp OWNER=hr

# 导入到不同用户
imp system/<password> FILE=hr.dmp FROMUSER=hr TOUSER=hr_new
```

---

## 6. 冷备份（脱机备份）

### 6.1 备份步骤

```sql
-- 1. 正常关闭数据库
sqlplus / as sysdba
SQL> SHUTDOWN IMMEDIATE;

-- 2. 复制所有相关文件（操作系统命令）
-- 数据文件
cp /u01/app/oracle/oradata/orcl/*.dbf /backup/oracle/cold/

-- 控制文件
cp /u01/app/oracle/oradata/orcl/control*.ctl /backup/oracle/cold/

-- 重做日志
cp /u01/app/oracle/oradata/orcl/redo*.log /backup/oracle/cold/

-- 参数文件
cp /u01/app/oracle/product/19c/dbhome_1/dbs/spfileorcl.ora /backup/oracle/cold/

-- 密码文件
cp /u01/app/oracle/product/19c/dbhome_1/dbs/orapworcl /backup/oracle/cold/

-- 3. 启动数据库
SQL> STARTUP;
```

### 6.2 恢复步骤

```sql
-- 1. 关闭数据库
SQL> SHUTDOWN IMMEDIATE;

-- 2. 复制备份文件回原位置
cp /backup/oracle/cold/*.dbf /u01/app/oracle/oradata/orcl/
cp /backup/oracle/cold/*.ctl /u01/app/oracle/oradata/orcl/
cp /backup/oracle/cold/*.log /u01/app/oracle/oradata/orcl/

-- 3. 启动数据库
SQL> STARTUP;
```

---

## 7. 热备份（联机备份）

⚠️ **前提：** 数据库必须处于归档模式

### 7.1 检查归档模式

```sql
SQL> ARCHIVE LOG LIST;
SQL> SELECT log_mode FROM v$database;
```

### 7.2 启用归档模式

```sql
SQL> SHUTDOWN IMMEDIATE;
SQL> STARTUP MOUNT;
SQL> ALTER DATABASE ARCHIVELOG;
SQL> ALTER DATABASE OPEN;
SQL> ARCHIVE LOG LIST;
```

### 7.3 表空间级别热备份

```sql
-- 1. 开始备份表空间
SQL> ALTER TABLESPACE users BEGIN BACKUP;

-- 2. 复制数据文件（操作系统命令）
cp /u01/app/oracle/oradata/orcl/users01.dbf /backup/oracle/hot/

-- 3. 结束备份
SQL> ALTER TABLESPACE users END BACKUP;

-- 4. 切换日志（可选）
SQL> ALTER SYSTEM SWITCH LOGFILE;
```

### 7.4 数据库级别热备份（10g+）

```sql
-- 1. 开始备份
SQL> ALTER DATABASE BEGIN BACKUP;

-- 2. 复制所有数据文件
cp /u01/app/oracle/oradata/orcl/*.dbf /backup/oracle/hot/

-- 3. 结束备份
SQL> ALTER DATABASE END BACKUP;

-- 4. 备份控制文件
SQL> ALTER DATABASE BACKUP CONTROLFILE TO '/backup/oracle/control_backup.ctl';
SQL> ALTER DATABASE BACKUP CONTROLFILE TO TRACE AS '/backup/oracle/control_trace.trc';

-- 5. 切换日志
SQL> ALTER SYSTEM SWITCH LOGFILE;
```

### 7.5 热备份恢复

```sql
-- 1. 挂载数据库
SQL> STARTUP MOUNT;

-- 2. 恢复数据文件
SQL> RESTORE DATAFILE '/u01/app/oracle/oradata/orcl/users01.dbf';
SQL> RECOVER DATAFILE '/u01/app/oracle/oradata/orcl/users01.dbf';

-- 3. 打开数据库
SQL> ALTER DATABASE OPEN;
```

---

## 8. Flashback 闪回技术

### 8.1 启用闪回

```sql
-- 检查闪回状态
SQL> SELECT flashback_on FROM v$database;

-- 配置闪回区
SQL> ALTER SYSTEM SET db_recovery_file_dest_size=10G;
SQL> ALTER SYSTEM SET db_recovery_file_dest='/u01/app/oracle/flash_recovery_area';

-- 启用闪回
SQL> SHUTDOWN IMMEDIATE;
SQL> STARTUP MOUNT;
SQL> ALTER DATABASE FLASHBACK ON;
SQL> ALTER DATABASE OPEN;
```

### 8.2 闪回查询

```sql
-- 查询过去某一时刻的数据
SELECT * FROM hr.employees AS OF TIMESTAMP TO_TIMESTAMP('2026-03-10 10:00:00','YYYY-MM-DD HH24:MI:SS');

-- 查询过去某一 SCN 的数据
SELECT * FROM hr.employees AS OF SCN 1234567;

-- 查看历史数据
SELECT VERSIONS_STARTTIME, VERSIONS_ENDTIME, VERSIONS_XID, *
FROM hr.employees VERSIONS BETWEEN TIMESTAMP MINVALUE AND MAXVALUE
WHERE employee_id = 100;
```

### 8.3 闪回表

```sql
-- 恢复误删除的表
FLASHBACK TABLE hr.employees TO TIMESTAMP TO_TIMESTAMP('2026-03-10 10:00:00','YYYY-MM-DD HH24:MI:SS');

-- 恢复到指定 SCN
FLASHBACK TABLE hr.employees TO SCN 1234567;

-- 闪回删除的表（回收站）
FLASHBACK TABLE hr.employees TO BEFORE DROP;

-- 查看回收站
SELECT * FROM dba_recyclebin;

-- 清空回收站
PURGE RECYCLEBIN;
PURGE TABLE hr.employees;
```

### 8.4 闪回数据库

```sql
-- 闪回到指定时间
SQL> SHUTDOWN IMMEDIATE;
SQL> STARTUP MOUNT;
SQL> FLASHBACK DATABASE TO TIMESTAMP TO_TIMESTAMP('2026-03-10 10:00:00','YYYY-MM-DD HH24:MI:SS');
SQL> ALTER DATABASE OPEN RESETLOGS;

-- 闪回到指定 SCN
SQL> FLASHBACK DATABASE TO SCN 1234567;
SQL> ALTER DATABASE OPEN RESETLOGS;

-- 闪回到还原点
SQL> FLASHBACK DATABASE TO RESTORE POINT before_upgrade;
SQL> ALTER DATABASE OPEN RESETLOGS;
```

### 8.5 创建还原点

```sql
-- 创建普通还原点
SQL> CREATE RESTORE POINT before_upgrade;

-- 创建担保还原点（保证可闪回）
SQL> CREATE RESTORE POINT before_upgrade GUARANTEE FLASHBACK DATABASE;

-- 查看还原点
SELECT * FROM v$restore_point;

-- 删除还原点
SQL> DROP RESTORE POINT before_upgrade;
```

---

## 9. 定时备份脚本

### 9.1 RMAN 全备脚本

```bash
#!/bin/bash
# /u01/scripts/rman_full_backup.sh

# 环境变量
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/19c/dbhome_1
export ORACLE_SID=orcl
export PATH=$ORACLE_HOME/bin:$PATH
export DATE=$(date +%Y%m%d_%H%M%S)
export BACKUP_DIR=/backup/oracle/rman
export LOG_DIR=/backup/oracle/log

# 创建目录
mkdir -p $BACKUP_DIR $LOG_DIR

# RMAN 备份脚本
rman target / log=$LOG_DIR/rman_full_$DATE.log << EOF
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
CONFIGURE DEVICE TYPE DISK PARALLELISM 4;
CONFIGURE DEFAULT DEVICE TYPE TO DISK;
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '$BACKUP_DIR/control_%F';

BACKUP INCREMENTAL LEVEL 0 DATABASE FORMAT '$BACKUP_DIR/full_%U.bkp' PLUS ARCHIVELOG FORMAT '$BACKUP_DIR/arch_%U.bkp' DELETE INPUT;
BACKUP CURRENT CONTROLFILE FORMAT '$BACKUP_DIR/control_$DATE.bkp';
BACKUP SPFILE FORMAT '$BACKUP_DIR/spfile_$DATE.bkp';

DELETE OBSOLETE;
DELETE ARCHIVELOG ALL COMPLETED BEFORE 'SYSDATE-7';

CROSSCHECK BACKUP;
DELETE EXPIRED BACKUP;

EXIT;
EOF

# 检查备份状态
if [ $? -eq 0 ]; then
  echo "[$(date)] RMAN 备份成功" >> $LOG_DIR/backup_status.log
else
  echo "[$(date)] RMAN 备份失败！" >> $LOG_DIR/backup_status.log
  # 发送邮件告警（可选）
  # mail -s "Oracle Backup Failed" admin@example.com < $LOG_DIR/rman_full_$DATE.log
fi
```

### 9.2 数据泵备份脚本

```bash
#!/bin/bash
# /u01/scripts/expdp_backup.sh

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/19c/dbhome_1
export ORACLE_SID=orcl
export PATH=$ORACLE_HOME/bin:$PATH
export DATE=$(date +%Y%m%d_%H%M%S)
export DUMP_DIR=/backup/oracle/dump
export LOG_DIR=/backup/oracle/log

mkdir -p $DUMP_DIR $LOG_DIR

# 导出全库
expdp system/<password> FULL=Y \
  DIRECTORY=backup_dir \
  DUMPFILE=full_$DATE_%U.dmp \
  LOGFILE=full_$DATE.log \
  PARALLEL=4 \
  COMPRESSION=ALL \
  EXCLUDE=STATISTICS

# 检查导出状态
if [ $? -eq 0 ]; then
  echo "[$(date)] 数据泵备份成功" >> $LOG_DIR/expdp_status.log
  # 清理 7 天前的备份
  find $DUMP_DIR -name "*.dmp" -mtime +7 -delete
  find $LOG_DIR -name "*.log" -mtime +7 -delete
else
  echo "[$(date)] 数据泵备份失败！" >> $LOG_DIR/expdp_status.log
fi
```

### 9.3 添加定时任务

```bash
# 编辑 crontab
crontab -e

# 每周日凌晨 2 点 RMAN 全备
0 2 * * 0 /u01/scripts/rman_full_backup.sh

# 每天凌晨 3 点数据泵备份
0 3 * * * /u01/scripts/expdp_backup.sh

# 每小时备份归档日志
0 * * * * /u01/scripts/archive_backup.sh
```

---

## 10. 常见错误与解决方案

### ❌ 错误 1：ORA-01034: ORACLE not available

```
ERROR:
ORA-01034: ORACLE not available
ORA-27101: shared memory realm does not exist
```

**原因：** 数据库未启动或环境变量错误

**解决：**
```bash
# 检查实例状态
sqlplus / as sysdba
SQL> SELECT status FROM v$instance;

# 启动数据库
SQL> STARTUP;

# 检查环境变量
echo $ORACLE_SID
echo $ORACLE_HOME
```

---

### ❌ 错误 2：ORA-01555: snapshot too old

```
ORA-01555: snapshot too old: rollback segment number 9 with name "_SYSSMU9_..." too small
```

**原因：** 回滚段太小，长时间查询被覆盖

**解决：**
```sql
-- 增加 undo 表空间
ALTER DATABASE DATAFILE '/u01/app/oracle/oradata/orcl/undotbs01.dbf' RESIZE 2G;
ALTER TABLESPACE undotbs1 ADD DATAFILE '/u01/app/oracle/oradata/orcl/undotbs02.dbf' SIZE 1G AUTOEXTEND ON;

-- 增加 undo_retention
ALTER SYSTEM SET undo_retention=10800 SCOPE=BOTH;  -- 3 小时
```

---

### ❌ 错误 3：ORA-00257: Archiver error

```
ORA-00257: archiver error. Connect internal only, until freed
```

**原因：** 归档日志满了

**解决：**
```bash
# 检查闪回区使用率
sqlplus / as sysdba
SQL> SELECT * FROM v$flash_recovery_area_usage;

# 删除旧归档日志（RMAN）
rman target /
RMAN> DELETE ARCHIVELOG ALL COMPLETED BEFORE 'SYSDATE-7';
RMAN> DELETE OBSOLETE;

# 或增加闪回区大小
SQL> ALTER SYSTEM SET db_recovery_file_dest_size=20G SCOPE=BOTH;
```

---

### ❌ 错误 4：ORA-19504: failed to create file

```
ORA-19504: failed to create file '/backup/oracle/full_01.bkp'
ORA-27038: created file already exists
```

**原因：** 备份文件已存在或目录权限问题

**解决：**
```bash
# 检查目录权限
ls -la /backup/oracle/
chown oracle:oinstall /backup/oracle
chmod 755 /backup/oracle

# 或使用 %U 生成唯一文件名
BACKUP DATABASE FORMAT '/backup/oracle/full_%U.bkp';
```

---

### ❌ 错误 5：ORA-01157: cannot identify/lock data file

```
ORA-01157: cannot identify/lock data file 4 - see DBWR trace file
ORA-01110: data file 4: '/u01/app/oracle/oradata/orcl/users01.dbf'
```

**原因：** 数据文件丢失或损坏

**解决：**
```sql
-- 离线数据文件
SQL> ALTER DATABASE DATAFILE 4 OFFLINE;

-- 恢复数据文件
RMAN> RESTORE DATAFILE 4;
RMAN> RECOVER DATAFILE 4;

-- 在线数据文件
SQL> ALTER DATABASE DATAFILE 4 ONLINE;

-- 如果文件无法恢复，创建新文件
SQL> ALTER DATABASE CREATE DATAFILE '/u01/app/oracle/oradata/orcl/users01.dbf' AS NEW;
SQL> RECOVER DATAFILE 4;
```

---

### ❌ 错误 6：ORA-00205: error in identifying control file

```
ORA-00205: error in identifying control file, check alert log for more info
```

**原因：** 控制文件损坏或丢失

**解决：**
```sql
-- 从备份恢复控制文件
RMAN> STARTUP NOMOUNT;
RMAN> RESTORE CONTROLFILE FROM AUTOBACKUP;
RMAN> ALTER DATABASE MOUNT;
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN RESETLOGS;

-- 或从镜像副本恢复
cp /backup/oracle/control_backup.ctl /u01/app/oracle/oradata/orcl/control01.ctl
SQL> STARTUP;
```

---

### ❌ 错误 7：ORA-01589: must use RESETLOGS or NORESETLOGS

```
ORA-01589: must use RESETLOGS or NORESETLOGS option for database open
```

**原因：** 不完全恢复后必须用 RESETLOGS 打开

**解决：**
```sql
SQL> ALTER DATABASE OPEN RESETLOGS;
```

---

### ❌ 错误 8：expdp ORA-39002: invalid operation

```
ORA-39002: invalid operation
ORA-39070: Unable to open the log file
```

**原因：** 目录对象不存在或权限不足

**解决：**
```sql
-- 创建目录
CREATE DIRECTORY backup_dir AS '/backup/oracle/dump';

-- 授权
GRANT READ, WRITE ON DIRECTORY backup_dir TO system;

-- 检查目录
SELECT * FROM dba_directories WHERE directory_name = 'BACKUP_DIR';
```

---

### ❌ 错误 9：ORA-01113: file 4 needs media recovery

```
ORA-01113: file 4 needs media recovery
ORA-01110: data file 4: '/u01/app/oracle/oradata/orcl/users01.dbf'
```

**原因：** 数据文件需要恢复

**解决：**
```sql
-- 开始恢复
SQL> RECOVER DATAFILE 4;

-- 或自动恢复
SQL> RECOVER AUTOMATIC DATAFILE 4;

-- 完成后打开
SQL> ALTER DATABASE OPEN;
```

---

### ❌ 错误 10：RMAN-06023: no backup or copy of datafile found

```
RMAN-06023: no backup or copy of datafile 4 found to restore
```

**原因：** 没有可用的备份

**解决：**
```bash
# 查看可用备份
RMAN> LIST BACKUP OF DATAFILE 4;

# 交叉检查
RMAN> CROSSCHECK BACKUP;

# 如果没有备份，只能从其他副本恢复或重建
# 检查是否有物理副本
ls -la /backup/oracle/

# 或从 standby 数据库恢复
```

---

## 11. 最佳实践

### ✅ 备份策略

| 数据库大小 | 推荐策略 | 频率 |
|------------|----------|------|
| < 100GB | RMAN 全量 | 每天 |
| 100GB-1TB | RMAN 0 级 +1 级增量 | 周日 0 级，每天 1 级 |
| > 1TB | RMAN 增量 + 数据泵 | 周日 0 级，每天增量，每月数据泵 |

### ✅ 3-2-1 备份原则

- **3** 份数据副本
- **2** 种不同介质（磁盘 + 磁带/云）
- **1** 份异地备份

### ✅ RMAN 配置建议

```sql
-- 启用控制文件自动备份
CONFIGURE CONTROLFILE AUTOBACKUP ON;

-- 设置保留策略
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;

-- 设置并行度
CONFIGURE DEVICE TYPE DISK PARALLELISM 4;

-- 启用压缩
CONFIGURE DEVICE TYPE DISK BACKUP TYPE TO COMPRESSED BACKUPSET;
```

### ✅ 监控备份

```sql
-- 查看备份进度
SELECT * FROM v$session_longops WHERE opname LIKE '%RMAN%';

-- 查看备份历史
SELECT * FROM v$rman_status ORDER BY start_time DESC;

-- 查看闪回区使用率
SELECT * FROM v$flash_recovery_area_usage;

-- 检查备份是否成功
RMAN> REPORT NEED BACKUP;
RMAN> REPORT OBSOLETE;
```

### ✅ 恢复测试

```bash
# 每季度做一次完整恢复测试
# 记录 RTO（恢复时间目标）和 RPO（恢复点目标）
# 验证备份可用性
```

### ✅ 安全建议

1. **备份加密**：使用 RMAN 加密备份集
2. **权限控制**：备份目录只允许 oracle 用户访问
3. **网络传输加密**：远程备份使用 SSL
4. **审计日志**：记录所有备份和恢复操作
5. **定期轮换密码**：备份用户密码定期更换

---

## 📋 快速参考卡片

```bash
# ===== RMAN 备份 =====
rman target /
RMAN> BACKUP DATABASE PLUS ARCHIVELOG;
RMAN> BACKUP INCREMENTAL LEVEL 1 DATABASE;
RMAN> DELETE OBSOLETE;

# ===== RMAN 恢复 =====
RMAN> STARTUP MOUNT;
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN;

# ===== 数据泵导出 =====
expdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full.dmp

# ===== 数据泵导入 =====
impdp system/<password> FULL=Y DIRECTORY=backup_dir DUMPFILE=full.dmp

# ===== 闪回表 =====
FLASHBACK TABLE hr.employees TO TIMESTAMP TO_TIMESTAMP('2026-03-10 10:00:00','YYYY-MM-DD HH24:MI:SS');

# ===== 检查状态 =====
SQL> SELECT flashback_on FROM v$database;
SQL> ARCHIVE LOG LIST;
RMAN> LIST BACKUP SUMMARY;
```

---

> 💡 **刺刺提醒：** 备份不测试 = 没有备份！定期做恢复演练！😈
> 
> ⚠️ **重要：** 生产环境执行恢复前，务必先在测试环境验证！
## 常用指令

- rman target /
- list backup summary;
- crosscheck backup;
- report obsolete;
- backup database plus archivelog;
- restore database;
- recover database;
- expdp system/<password> FULL=Y DIRECTORY=<dir> DUMPFILE=<file>.dmp LOGFILE=<file>.log
- impdp system/<password> FULL=Y DIRECTORY=<dir> DUMPFILE=<file>.dmp LOGFILE=<file>.log
- sqlplus / as sysdba
- select status from v$instance;

