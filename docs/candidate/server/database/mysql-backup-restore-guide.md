# MySQL 备份与恢复参考手册

```yaml
status: usable
type: reference
risk_level: high
review_required: true
source: imported-manual
source_path: D:/Work/工作文档/知识库构建/服务器运维相关/mysql-backup-restore-guide.md
asset_types: [database, server]
systems: [mysql]
issue_types: [backup, restore, data-recovery]
tags: [mysql, mysqldump, backup, restore, binlog]
```

## 适用范围

- 适用于 MySQL 逻辑备份、恢复、压缩、加密、定时备份和常见恢复问题。
- 适合作为数据库备份恢复操作前的流程检查参考。

## 常见现象

- 需要备份单库、多库、全库或单表。
- 需要从 SQL、压缩备份或历史备份恢复数据。
- 备份失败、恢复失败、权限不足或字符集异常。

## 处理步骤

1. 确认数据库实例、库表范围、备份时间点、保留策略和恢复目标。
2. 恢复前必须确认现有数据备份、业务停机窗口和回退方案。
3. 按场景参考原始手册中的 mysqldump、mysql 恢复、压缩加密、自动备份或常见错误章节。
4. 恢复操作优先在测试环境验证，再进入生产维护窗口。
5. 记录备份文件路径、校验结果、恢复命令、耗时和验证结果。

## 验证方式

- 备份文件存在且可读，大小和校验结果符合预期。
- 恢复后目标库表、行数、关键业务查询和应用连接正常。
- 备份任务后续调度和告警正常。

## 注意事项

- 本文属于服务器、数据库或网络设备高风险运维参考，生产环境操作前必须完成审批、备份、维护窗口和回退方案确认。
- 本文中的命令和参数来自通用手册，执行前必须替换为本公司实际环境，并先在测试环境验证。
- 涉及删除、覆盖、重启、恢复、扩缩容、路由/ACL 变更、证书/密钥、数据库恢复等动作时，不允许直接照抄执行。
- 手册中的示例密码、Token 和密钥已做脱敏处理；不得在知识库中保存真实凭据。

## 原始手册

以下内容为导入的原始手册正文，供工程师查阅细节。

# MySQL 备份与恢复完全指南

> 📝 版本：MySQL 8.0+  
> ⚠️ 生产环境操作前请先测试！

---

## 📚 目录

1. [备份方式概览](#1-备份方式概览)
2. [mysqldump 逻辑备份](#2-mysqldump-逻辑备份)
3. [mysql 命令恢复](#3-mysql-命令恢复)
4. [物理备份](#4-物理备份)
5. [增量备份](#5-增量备份)
6. [定时备份脚本](#6-定时备份脚本)
7. [常见错误与解决方案](#7-常见错误与解决方案)
8. [最佳实践](#8-最佳实践)

---

## 1. 备份方式概览

| 方式 | 工具 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **逻辑备份** | mysqldump | 灵活、可读、跨版本 | 慢、大库耗时 | 小中型数据库 |
| **物理备份** | xtrabackup / cp | 快、支持增量 | 占用空间、版本依赖 | 大型数据库 |
| **二进制日志** | mysqlbinlog | 支持时间点恢复 | 配置复杂 | 精确恢复 |
| **云厂商快照** | 控制台 | 一键操作 | 厂商锁定 | 云数据库 |

---

## 2. mysqldump 逻辑备份

### 2.1 基本语法

```bash
mysqldump [选项] [数据库名] [表名]
```

### 2.2 常用备份场景

#### 🔹 备份单个数据库
```bash
mysqldump -u admin -p mydb > mydb_backup.sql
```

#### 🔹 备份多个数据库
```bash
mysqldump -u admin -p --databases db1 db2 db3 > multi_db_backup.sql
```

#### 🔹 备份所有数据库
```bash
mysqldump -u admin -p --all-databases > all_databases_backup.sql
```

#### 🔹 备份单张表
```bash
mysqldump -u admin -p mydb users > users_backup.sql
```

#### 🔹 备份多张表
```bash
mysqldump -u admin -p mydb users orders products > tables_backup.sql
```

#### 🔹 只备份表结构（无数据）
```bash
mysqldump -u admin -p --no-data mydb > mydb_structure.sql
```

#### 🔹 只备份数据（无结构）
```bash
mysqldump -u admin -p --no-create-info mydb > mydb_data.sql
```

#### 🔹 备份存储过程和函数
```bash
mysqldump -u admin -p --routines --triggers mydb > mydb_full.sql
```

#### 🔹 备份事件（Event）
```bash
mysqldump -u admin -p --events mydb > mydb_with_events.sql
```

### 2.3 推荐的生产环境备份参数

```bash
mysqldump -u admin -p \
  --single-transaction \
  --quick \
  --lock-tables=false \
  --routines \
  --triggers \
  --events \
  --set-gtid-purged=OFF \
  mydb > mydb_production.sql
```

**参数说明：**
| 参数 | 作用 |
|------|------|
| `--single-transaction` | InnoDB 一致性快照，不锁表 |
| `--quick` | 逐行读取，不缓存全部结果 |
| `--lock-tables=false` | 不锁定表（配合 single-transaction） |
| `--routines` | 包含存储过程和函数 |
| `--triggers` | 包含触发器 |
| `--events` | 包含事件调度器 |
| `--set-gtid-purged=OFF` | 不写入 GTID 信息（避免恢复时冲突） |

### 2.4 压缩备份（节省空间）

```bash
# 备份并压缩
mysqldump -u admin -p mydb | gzip > mydb_backup.sql.gz

# 备份并压缩（推荐，更快）
mysqldump -u admin -p mydb | pigz > mydb_backup.sql.gz

# 解压查看
zcat mydb_backup.sql.gz | head -50
```

### 2.5 加密备份（敏感数据）

```bash
# 使用 GPG 加密
mysqldump -u admin -p mydb | gpg -c > mydb_backup.sql.gpg

# 解密恢复
gpg -d mydb_backup.sql.gpg | mysql -u admin -p mydb
```

---

## 3. mysql 命令恢复

### 3.1 基本恢复

```bash
# 恢复单个数据库
mysql -u admin -p mydb < mydb_backup.sql

# 恢复所有数据库（需要 --all-databases 备份）
mysql -u admin -p < all_databases_backup.sql
```

### 3.2 恢复压缩备份

```bash
# gzip 压缩
gunzip < mydb_backup.sql.gz | mysql -u admin -p mydb

# 或
zcat mydb_backup.sql.gz | mysql -u admin -p mydb

# pigz 压缩
pigz -dc mydb_backup.sql.gz | mysql -u admin -p mydb
```

### 3.3 恢复时跳过错误

```bash
# 继续执行即使遇到错误
mysql -u admin -p --force mydb < mydb_backup.sql
```

### 3.4 恢复前清空数据库

```bash
# 先删除再创建
mysql -u admin -p -e "DROP DATABASE IF EXISTS mydb; CREATE DATABASE mydb;"
mysql -u admin -p mydb < mydb_backup.sql
```

### 3.5 使用 source 命令在 MySQL 内恢复

```bash
mysql -u admin -p
mysql> USE mydb;
mysql> SOURCE /path/to/mydb_backup.sql;
```

---

## 4. 物理备份

### 4.1 直接复制数据文件（需停服）

```bash
# 停止 MySQL
systemctl stop mysql

# 复制数据目录
cp -r /var/lib/mysql /backup/mysql_backup_$(date +%F)

# 启动 MySQL
systemctl start mysql
```

⚠️ **注意：**
- 必须停止 MySQL 服务
- 需要复制整个 `/var/lib/mysql` 目录
- 恢复时也需要停服

### 4.2 使用 XtraBackup（热备份）

```bash
# 安装
apt-get install percona-xtrabackup-80

# 全量备份
xtrabackup --backup --target-dir=/backup/xtrabackup_full

# 准备备份（应用日志）
xtrabackup --prepare --target-dir=/backup/xtrabackup_full

# 恢复（停服后）
systemctl stop mysql
rm -rf /var/lib/mysql/*
xtrabackup --copy-back --target-dir=/backup/xtrabackup_full
chown -R mysql:mysql /var/lib/mysql
systemctl start mysql
```

---

## 5. 增量备份

### 5.1 启用二进制日志

编辑 `/etc/mysql/mysql.conf.d/mysqld.cnf`：

```ini
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_format = ROW
expire_logs_days = 7
max_binlog_size = 100M
```

重启 MySQL：
```bash
systemctl restart mysql
```

### 5.2 全量 + 增量备份策略

```bash
# 周日：全量备份
mysqldump -u admin -p --all-databases > /backup/sunday_full.sql

# 周一至周六：增量备份（复制 binlog）
cp /var/log/mysql/mysql-bin.* /backup/binlog_$(date +%F)/
```

### 5.3 使用 binlog 恢复

```bash
# 查看 binlog 文件
mysql -u admin -p -e "SHOW BINARY LOGS;"

# 查看 binlog 内容
mysqlbinlog /var/log/mysql/mysql-bin.000001 | head -50

# 按时间点恢复
mysqlbinlog --stop-datetime="2026-03-10 11:00:00" \
  /var/log/mysql/mysql-bin.000001 | mysql -u admin -p

# 按位置恢复
mysqlbinlog --start-position=1000 --stop-position=2000 \
  /var/log/mysql/mysql-bin.000001 | mysql -u admin -p
```

---

## 6. 定时备份脚本

### 6.1 完整备份脚本

```bash
#!/bin/bash
# /usr/local/bin/mysql_backup.sh

# 配置
DB_USER="admin"
DB_PASS="OpenClaw@2026"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份所有数据库
mysqldump -u $DB_USER -p$DB_PASS \
  --single-transaction \
  --quick \
  --lock-tables=false \
  --routines \
  --triggers \
  --events \
  --all-databases | gzip > $BACKUP_DIR/all_databases_$DATE.sql.gz

# 检查备份是否成功
if [ $? -eq 0 ]; then
  echo "[$(date)] 备份成功：all_databases_$DATE.sql.gz" >> $BACKUP_DIR/backup.log
else
  echo "[$(date)] 备份失败！" >> $BACKUP_DIR/backup.log
  exit 1
fi

# 清理旧备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] 清理完成，保留最近 $RETENTION_DAYS 天的备份" >> $BACKUP_DIR/backup.log
```

### 6.2 添加定时任务

```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点备份
0 2 * * * /usr/local/bin/mysql_backup.sh

# 或每周日凌晨 3 点
0 3 * * 0 /usr/local/bin/mysql_backup.sh
```

### 6.3 备份到远程服务器

```bash
# 追加到备份脚本
scp $BACKUP_DIR/all_databases_$DATE.sql.gz user@remote:/backup/mysql/

# 或使用 rsync（支持断点续传）
rsync -avz $BACKUP_DIR/all_databases_$DATE.sql.gz user@remote:/backup/mysql/
```

---

## 7. 常见错误与解决方案

### ❌ 错误 1：Access denied

```
mysqldump: Got error: 1045: Access denied for user 'admin'@'localhost'
```

**原因：** 用户名或密码错误

**解决：**
```bash
# 检查密码
mysql -u admin -p

# 重置密码
mysql -u root -e "ALTER USER 'admin'@'%' IDENTIFIED BY '新密码';"
```

---

### ❌ 错误 2：Got error: 2006: MySQL server has gone away

```
mysqldump: Got error: 2006: MySQL server has gone away when using 'SHOW TRIGGER STATUS'
```

**原因：** 数据包太大或超时

**解决：**
```bash
# 增加 max_allowed_packet
mysqldump -u admin -p --max_allowed_packet=1G mydb > backup.sql

# 或在 MySQL 配置中增加
# /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
max_allowed_packet = 1G
wait_timeout = 28800
```

---

### ❌ 错误 3：Got error: 1044: Access denied when using LOCK TABLES

```
mysqldump: Got error: 1044: Access denied when using LOCK TABLES
```

**原因：** 用户没有 LOCK TABLES 权限

**解决：**
```bash
# 使用 --single-transaction 避免锁表
mysqldump -u admin -p --single-transaction mydb > backup.sql

# 或授予权限
mysql -u root -e "GRANT LOCK TABLES ON *.* TO 'admin'@'%';"
```

---

### ❌ 错误 4：Unknown table 'COLUMN_STATISTICS'

```
mysqldump: Couldn't execute 'SELECT COLUMN_NAME...': Unknown table 'COLUMN_STATISTICS'
```

**原因：** MySQL 8.0.21+ 的默认行为与旧版本不兼容

**解决：**
```bash
# 添加 --column-statistics=0
mysqldump -u admin -p --column-statistics=0 mydb > backup.sql
```

---

### ❌ 错误 5：Duplicate entry when restoring

```
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
```

**原因：** 数据库中已有相同数据

**解决：**
```bash
# 方法 1：恢复前清空数据库
mysql -u admin -p -e "DROP DATABASE IF EXISTS mydb; CREATE DATABASE mydb;"
mysql -u admin -p mydb < backup.sql

# 方法 2：使用 --force 继续执行
mysql -u admin -p --force mydb < backup.sql

# 方法 3：备份时添加 DROP 语句
mysqldump -u admin -p --add-drop-database mydb > backup.sql
```

---

### ❌ 错误 6：Character set mismatch

```
ERROR 1366 (HY000): Incorrect string value
```

**原因：** 字符集不匹配

**解决：**
```bash
# 备份时指定字符集
mysqldump -u admin -p --default-character-set=utf8mb4 mydb > backup.sql

# 恢复时指定字符集
mysql -u admin -p --default-character-set=utf8mb4 mydb < backup.sql
```

---

### ❌ 错误 7：Backup file is empty

```bash
-rw-r--r-- 1 root root 0 backup.sql
```

**原因：** 备份命令失败但创建了空文件

**解决：**
```bash
# 检查 MySQL 服务状态
systemctl status mysql

# 检查磁盘空间
df -h

# 检查用户权限
mysql -u admin -p -e "SHOW GRANTS;"

# 重新备份并检查
mysqldump -u admin -p mydb > backup.sql
wc -l backup.sql  # 检查行数
```

---

### ❌ 错误 8：Restore timeout

```
ERROR 2013 (HY000): Lost connection to MySQL server during query
```

**原因：** 恢复时间太长导致超时

**解决：**
```bash
# 增加超时时间
mysql -u admin -p --connect-timeout=3600 --net-read-timeout=3600 mydb < backup.sql

# 或分批恢复大表
```

---

### ❌ 错误 9：GTID 冲突

```
ERROR 1840 (HY000): GTID_NEXT cannot be changed
```

**原因：** 备份中包含 GTID 信息

**解决：**
```bash
# 备份时禁用 GTID
mysqldump -u admin -p --set-gtid-purged=OFF mydb > backup.sql

# 或恢复时跳过 GTID
mysql -u admin -p -e "SET @@GLOBAL.GTID_PURGED='';"
mysql -u admin -p mydb < backup.sql
```

---

### ❌ 错误 10：Disk full during backup

```
No space left on device
```

**原因：** 磁盘空间不足

**解决：**
```bash
# 检查空间
df -h

# 清理空间
rm -rf /tmp/*
journalctl --vacuum-time=1d

# 备份到外部存储
mysqldump -u admin -p mydb | gzip > /mnt/external/backup.sql.gz

# 或边备份边压缩边传输到远程
mysqldump -u admin -p mydb | gzip | ssh user@remote "cat > /backup/backup.sql.gz"
```

---

## 8. 最佳实践

### ✅ 备份策略

| 数据库大小 | 推荐方式 | 频率 |
|------------|----------|------|
| < 1GB | mysqldump | 每天 |
| 1-10GB | mysqldump + binlog | 每天全量 + 每小时增量 |
| > 10GB | XtraBackup + binlog | 每周全量 + 每天增量 |

### ✅ 3-2-1 备份原则

- **3** 份数据副本（1 份生产 + 2 份备份）
- **2** 种不同介质（本地磁盘 + 云存储/磁带）
- **1** 份异地备份（不同地理位置）

### ✅ 恢复测试

```bash
# 每月至少做一次恢复测试
# 记录恢复时间，评估 RTO（恢复时间目标）
time mysql -u admin -p testdb < backup.sql
```

### ✅ 监控备份

```bash
# 检查最新备份时间
ls -lt /backup/mysql/*.sql.gz | head -1

# 检查备份文件大小（异常小可能失败）
du -h /backup/mysql/*.sql.gz

# 检查备份日志
tail -20 /backup/mysql/backup.log
```

### ✅ 安全建议

1. **备份文件加密**：敏感数据使用 GPG 加密
2. **权限控制**：备份目录只允许 root/mysql 用户访问
3. **网络传输加密**：远程备份使用 SSH/SSL
4. **定期轮换密码**：备份用户密码定期更换
5. **审计日志**：记录所有备份和恢复操作

---

## 📋 快速参考卡片

```bash
# ===== 备份 =====
# 单库
mysqldump -u admin -p mydb > backup.sql

# 全库
mysqldump -u admin -p --all-databases > all.sql

# 压缩
mysqldump -u admin -p mydb | gzip > backup.sql.gz

# 仅结构
mysqldump -u admin -p --no-data mydb > structure.sql

# ===== 恢复 =====
# 单库
mysql -u admin -p mydb < backup.sql

# 全库
mysql -u admin -p < all.sql

# 解压恢复
gunzip < backup.sql.gz | mysql -u admin -p mydb

# ===== 检查 =====
# 备份文件内容
head -50 backup.sql

# 备份文件大小
du -h backup.sql.gz

# MySQL 服务状态
systemctl status mysql
```

---

> 💡 **刺刺提醒：** 备份不测试 = 没有备份！定期做恢复演练！😈
## 常用指令

- mysqldump -h <host> -P <port> -u <user> -p --single-transaction --routines --triggers --events <database> > <database>.sql
- mysql -h <host> -P <port> -u <user> -p <database> < <database>.sql
- mysqladmin ping -h <host> -P <port> -u <user> -p
- mysql -h <host> -P <port> -u <user> -p -e "show databases;"
- mysql -h <host> -P <port> -u <user> -p -e "show processlist;"
- gzip <database>.sql
- gunzip <database>.sql.gz

