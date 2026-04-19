# Percona XtraBackup 备份恢复参考手册

```yaml
status: usable
type: reference
risk_level: high
review_required: true
source: imported-manual
source_path: D:/Work/工作文档/知识库构建/服务器运维相关/xtrabackup-guide.md
asset_types: [database, server]
systems: [mysql, percona-xtrabackup]
issue_types: [backup, restore, data-recovery]
tags: [xtrabackup, mysql, physical-backup, incremental-backup, restore]
```

## 适用范围

- 适用于 MySQL/Percona 使用 XtraBackup 执行物理热备、增量备份、压缩加密、恢复和验证。
- 适合作为较大数据库备份恢复和备份自动化参考。

## 常见现象

- 需要执行全量或增量物理备份。
- 需要准备备份、恢复数据目录或验证备份可恢复性。
- XtraBackup 权限、版本、redo 日志或恢复过程异常。

## 处理步骤

1. 确认 MySQL 版本、XtraBackup 版本、备份用户权限、备份目录和磁盘空间。
2. 备份前确认业务影响、保留策略、加密方式和监控告警。
3. 按场景参考原始手册中的全量备份、增量备份、prepare、恢复、验证和常见错误章节。
4. 恢复前必须停止目标实例、备份原数据目录，并优先在测试环境验证。
5. 记录备份链、LSN、prepare 日志、恢复命令和业务验证结果。

## 验证方式

- xtrabackup prepare 成功，无关键错误。
- 恢复后 MySQL 可正常启动。
- 关键库表、主从状态或业务查询正常。

## 注意事项

- 本文属于服务器、数据库或网络设备高风险运维参考，生产环境操作前必须完成审批、备份、维护窗口和回退方案确认。
- 本文中的命令和参数来自通用手册，执行前必须替换为本公司实际环境，并先在测试环境验证。
- 涉及删除、覆盖、重启、恢复、扩缩容、路由/ACL 变更、证书/密钥、数据库恢复等动作时，不允许直接照抄执行。
- 手册中的示例密码、Token 和密钥已做脱敏处理；不得在知识库中保存真实凭据。

## 原始手册

以下内容为导入的原始手册正文，供工程师查阅细节。

# Percona XtraBackup 完全指南

> 📝 版本：XtraBackup 8.0 (MySQL 8.0) / XtraBackup 2.4 (MySQL 5.7)  
> ⚠️ 生产环境操作前请先在测试环境验证！

---

## 📚 目录

1. [XtraBackup 简介](#1-xtrabackup-简介)
2. [安装与配置](#2-安装与配置)
3. [全量备份](#3-全量备份)
4. [增量备份](#4-增量备份)
5. [差异备份](#5-差异备份)
6. [备份恢复](#6-备份恢复)
7. [部分备份](#7-部分备份)
8. [流式备份与压缩](#8-流式备份与压缩)
9. [定时备份脚本](#9-定时备份脚本)
10. [备份验证与监控](#10-备份验证与监控)
11. [常见错误与解决方案](#11-常见错误与解决方案)
12. [最佳实践](#12-最佳实践)

---

## 1. XtraBackup 简介

### 1.1 什么是 XtraBackup？

Percona XtraBackup 是**开源的 MySQL 热备份工具**，支持：
- ✅ **InnoDB** 引擎（主要支持）
- ✅ **XtraDB** 引擎
- ✅ **MyISAM** 引擎（有限支持）
- ✅ **热备份**（不停机）
- ✅ **增量备份**
- ✅ **压缩备份**
- ✅ **流式备份**

### 1.2 版本对应关系

| XtraBackup 版本 | MySQL 版本 |
|----------------|------------|
| XtraBackup 8.0 | MySQL 8.0 |
| XtraBackup 2.4 | MySQL 5.7 / 5.6 |
| XtraBackup 2.3 | MySQL 5.6 / 5.5 |

### 1.3 核心概念

| 术语 | 说明 |
|------|------|
| **全量备份** | 备份所有数据文件 |
| **增量备份** | 只备份自上次备份后变化的数据（基于 LSN） |
| **差异备份** | 只备份自上次全量备份后变化的数据 |
| **Prepare** | 应用日志使备份一致（必须步骤） |
| **LSN** | Log Sequence Number，日志序列号 |

---

## 2. 安装与配置

### 2.1 Ubuntu/Debian 安装

```bash
# 添加 Percona 仓库
wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb

# 更新并安装
apt-get update
apt-get install percona-xtrabackup-80

# 验证安装
xbstream --version
xtrabackup --version
```

### 2.2 CentOS/RHEL 安装

```bash
# 添加 Percona 仓库
yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm

# 安装
yum install percona-xtrabackup-80

# 验证
xtrabackup --version
```

### 2.3 创建备份用户

```sql
-- 创建专用备份用户
CREATE USER 'backup'@'localhost' IDENTIFIED BY '<示例密码>';

-- 授予必要权限
GRANT BACKUP_ADMIN, SESSION_VARIABLES_ADMIN ON *.* TO 'backup'@'localhost';
GRANT RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT ON *.* TO 'backup'@'localhost';
GRANT SELECT ON performance_schema.* TO 'backup'@'localhost';
GRANT SELECT ON mysql.* TO 'backup'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 验证权限
SHOW GRANTS FOR 'backup'@'localhost';
```

### 2.4 MySQL 配置要求

编辑 `/etc/mysql/mysql.conf.d/mysqld.cnf`：

```ini
[mysqld]
# 必须配置（MySQL 8.0）
server-id = 1
log_bin = mysql-bin
binlog_format = ROW

# 推荐配置
innodb_file_per_table = 1
innodb_flush_method = O_DIRECT
innodb_flush_log_at_trx_commit = 2

# 如果使用压缩备份
innodb_checksum_algorithm = crc32
```

重启 MySQL：
```bash
systemctl restart mysql
```

### 2.5 创建备份目录

```bash
# 创建备份目录结构
mkdir -p /backup/mysql/{full,incremental,diff,logs}
mkdir -p /backup/mysql/{daily,weekly,monthly}

# 设置权限
chown -R mysql:mysql /backup/mysql
chmod -R 750 /backup/mysql

# 创建备份配置文件
cat > /etc/xtrabackup.cnf << EOF
[client]
user = backup
password = <示例密码>

[xtrabackup]
target-dir = /backup/mysql/full
backup-dir = /backup/mysql/incremental
EOF

chmod 600 /etc/xtrabackup.cnf
```

---

## 3. 全量备份

### 3.1 基本全量备份

```bash
# 使用配置文件
xtrabackup --backup --target-dir=/backup/mysql/full

# 或命令行指定参数
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full
```

### 3.2 全量备份（推荐参数）

```bash
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full_$(date +%F) \
  --parallel=4 \
  --compress \
  --compress-threads=4 \
  --checksum \
  --safe-slave-backup
```

**参数说明：**
| 参数 | 作用 |
|------|------|
| `--parallel` | 并行线程数 |
| `--compress` | 启用压缩 |
| `--compress-threads` | 压缩线程数 |
| `--checksum` | 校验和检查 |
| `--safe-slave-backup` | 确保从库安全 |

### 3.3 全量备份（流式输出）

```bash
# 流式备份到文件
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=xbstream \
  > /backup/mysql/full_$(date +%F).xbstream

# 流式备份并压缩
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=xbstream \
  | gzip > /backup/mysql/full_$(date +%F).xbstream.gz
```

### 3.4 全量备份（加密）

```bash
# 生成加密密钥
openssl rand -base64 24 > /backup/mysql/keyfile
chmod 600 /backup/mysql/keyfile

# 加密备份
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full_encrypted \
  --encrypt=AES256 \
  --encrypt-key-file=/backup/mysql/keyfile \
  --encrypt-threads=4
```

### 3.5 查看备份信息

```bash
# 查看备份元数据
cat /backup/mysql/full/backup-my.cnf
cat /backup/mysql/full/xtrabackup_checkpoints

# 查看 LSN 信息
cat /backup/mysql/full/xtrabackup_checkpoints | grep lsn

# 查看备份大小
du -sh /backup/mysql/full
```

---

## 4. 增量备份

### 4.1 增量备份原理

XtraBackup 通过比较 **LSN（Log Sequence Number）** 来实现增量备份：
- 全量备份后记录 LSN
- 增量备份只复制 LSN 之后的变化数据
- 基于 `xtrabackup_checkpoints` 文件

### 4.2 创建增量备份链

```bash
# 第 1 步：全量备份（周日）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full_sun \
  --parallel=4

# 第 2 步：增量备份（周一）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/incr_mon \
  --incremental-basedir=/backup/mysql/full_sun \
  --parallel=4

# 第 3 步：增量备份（周二）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/incr_tue \
  --incremental-basedir=/backup/mysql/incr_mon \
  --parallel=4

# 第 4 步：增量备份（周三）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/incr_wed \
  --incremental-basedir=/backup/mysql/incr_tue \
  --parallel=4
```

### 4.3 增量备份策略（推荐）

```bash
#!/bin/bash
# /usr/local/bin/xtrabackup_incremental.sh

DATE=$(date +%F)
WEEKDAY=$(date +%u)  # 1=周一，7=周日
FULL_DIR=/backup/mysql/full
INCR_DIR=/backup/mysql/incremental

if [ $WEEKDAY -eq 7 ]; then
  # 周日：全量备份
  echo "[$(date)] 执行全量备份" | tee -a /var/log/xtrabackup.log
  xtrabackup --user=backup --password=<示例密码> \
    --backup \
    --target-dir=$FULL_DIR/$DATE \
    --parallel=4 \
    --compress \
    2>&1 | tee -a /var/log/xtrabackup.log
else
  # 周一至周六：增量备份
  LATEST_FULL=$(ls -td $FULL_DIR/*/ | head -1)
  LATEST_INCR=$(ls -td $INCR_DIR/*/ 2>/dev/null | head -1)
  
  if [ -z "$LATEST_INCR" ]; then
    BASE_DIR=$LATEST_FULL
  else
    BASE_DIR=$LATEST_INCR
  fi
  
  echo "[$(date)] 执行增量备份，基于：$BASE_DIR" | tee -a /var/log/xtrabackup.log
  xtrabackup --user=backup --password=<示例密码> \
    --backup \
    --target-dir=$INCR_DIR/$DATE \
    --incremental-basedir=$BASE_DIR \
    --parallel=4 \
    --compress \
    2>&1 | tee -a /var/log/xtrabackup.log
fi

# 检查备份状态
if [ $? -eq 0 ]; then
  echo "[$(date)] 备份成功" | tee -a /var/log/xtrabackup.log
else
  echo "[$(date)] 备份失败！" | tee -a /var/log/xtrabackup.log
  exit 1
fi
```

### 4.4 查看增量备份信息

```bash
# 查看增量备份链
cat /backup/mysql/incr_mon/xtrabackup_checkpoints

# 输出示例：
# backup_type = incremental
# from_lsn = 1234567
# to_lsn = 2345678
# last_lsn = 2345678
# compact = 0
# recover_binlog_info = 0
# flushed_lsn = 2345678
```

---

## 5. 差异备份

### 5.1 差异备份 vs 增量备份

| 类型 | 基于 | 大小 | 恢复速度 |
|------|------|------|----------|
| **增量备份** | 上次备份（全量或增量） | 小 | 慢（需要应用所有增量） |
| **差异备份** | 上次全量备份 | 较大 | 快（只需全量 + 最后一次差异） |

### 5.2 创建差异备份

```bash
# 全量备份
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full \
  --parallel=4

# 差异备份 1（基于全量）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/diff_1 \
  --incremental-basedir=/backup/mysql/full \
  --parallel=4

# 差异备份 2（仍然基于全量，不是 diff_1）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/diff_2 \
  --incremental-basedir=/backup/mysql/full \
  --parallel=4

# 差异备份 3（仍然基于全量）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/diff_3 \
  --incremental-basedir=/backup/mysql/full \
  --parallel=4
```

### 5.3 差异备份策略

```bash
#!/bin/bash
# /usr/local/bin/xtrabackup_differential.sh

DATE=$(date +%F)
FULL_DIR=/backup/mysql/full
DIFF_DIR=/backup/mysql/differential

# 获取最新全量备份
LATEST_FULL=$(ls -td $FULL_DIR/*/ | head -1)

if [ -z "$LATEST_FULL" ]; then
  echo "[$(date)] 错误：未找到全量备份" | tee -a /var/log/xtrabackup.log
  exit 1
fi

echo "[$(date)] 执行差异备份，基于：$LATEST_FULL" | tee -a /var/log/xtrabackup.log

xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=$DIFF_DIR/$DATE \
  --incremental-basedir=$LATEST_FULL \
  --parallel=4 \
  --compress \
  2>&1 | tee -a /var/log/xtrabackup.log

if [ $? -eq 0 ]; then
  echo "[$(date)] 差异备份成功" | tee -a /var/log/xtrabackup.log
else
  echo "[$(date)] 差异备份失败！" | tee -a /var/log/xtrabackup.log
  exit 1
fi
```

---

## 6. 备份恢复

### 6.1 Prepare 备份（必须步骤）

**⚠️ 重要：** 恢复前必须先 Prepare，使备份数据一致！

```bash
# Prepare 全量备份
xtrabackup --prepare --target-dir=/backup/mysql/full

# Prepare 全量 + 增量备份链
# 第 1 步：Prepare 全量备份（应用日志，但不回滚未提交事务）
xtrabackup --prepare --apply-log-only --target-dir=/backup/mysql/full

# 第 2 步：应用增量备份 1
xtrabackup --prepare --apply-log-only --target-dir=/backup/mysql/full \
  --incremental-dir=/backup/mysql/incr_mon

# 第 3 步：应用增量备份 2
xtrabackup --prepare --apply-log-only --target-dir=/backup/mysql/full \
  --incremental-dir=/backup/mysql/incr_tue

# 第 4 步：应用最后一个增量备份（不用 --apply-log-only）
xtrabackup --prepare --target-dir=/backup/mysql/full \
  --incremental-dir=/backup/mysql/incr_wed
```

### 6.2 Prepare 差异备份

```bash
# Prepare 全量备份
xtrabackup --prepare --apply-log-only --target-dir=/backup/mysql/full

# 应用最后一次差异备份
xtrabackup --prepare --target-dir=/backup/mysql/full \
  --incremental-dir=/backup/mysql/diff_3
```

### 6.3 恢复备份（停机恢复）

```bash
# 第 1 步：停止 MySQL
systemctl stop mysql

# 第 2 步：备份原数据目录（以防万一）
mv /var/lib/mysql /var/lib/mysql.bak.$(date +%F)

# 第 3 步：创建新数据目录
mkdir -p /var/lib/mysql
chown mysql:mysql /var/lib/mysql

# 第 4 步：复制备份数据
xtrabackup --copy-back --target-dir=/backup/mysql/full

# 或手动复制
# cp -r /backup/mysql/full/* /var/lib/mysql/

# 第 5 步：修复权限
chown -R mysql:mysql /var/lib/mysql
chmod -R 750 /var/lib/mysql

# 第 6 步：启动 MySQL
systemctl start mysql

# 第 7 步：检查状态
systemctl status mysql
mysql -e "SHOW DATABASES;"
```

### 6.4 恢复到新位置（不停机）

```bash
# 准备新数据目录
mkdir -p /var/lib/mysql_new
chown mysql:mysql /var/lib/mysql_new

# 复制备份
xtrabackup --copy-back --target-dir=/backup/mysql/full \
  --datadir=/var/lib/mysql_new

# 修改 MySQL 配置
cat >> /etc/mysql/mysql.conf.d/mysqld.cnf << EOF
[mysqld]
datadir=/var/lib/mysql_new
EOF

# 重启 MySQL
systemctl restart mysql
```

### 6.5 使用 xbstream 恢复

```bash
# 解压 xbstream 文件
xbstream -x -C /backup/mysql/restore < /backup/mysql/full.xbstream

# Prepare
xtrabackup --prepare --target-dir=/backup/mysql/restore

# 恢复
xtrabackup --copy-back --target-dir=/backup/mysql/restore
```

### 6.6 使用压缩备份恢复

```bash
# 解压并恢复
xtrabackup --decompress --target-dir=/backup/mysql/full

# 或解压到指定目录
xtrabackup --decompress --decompress-dir=/backup/mysql/decompressed \
  --target-dir=/backup/mysql/full

# Prepare
xtrabackup --prepare --target-dir=/backup/mysql/full

# 恢复
xtrabackup --copy-back --target-dir=/backup/mysql/full
```

### 6.7 使用加密备份恢复

```bash
# 解密备份
xtrabackup --decrypt=AES256 --encrypt-key-file=/backup/mysql/keyfile \
  --target-dir=/backup/mysql/full_decrypted \
  --source-dir=/backup/mysql/full_encrypted

# Prepare
xtrabackup --prepare --target-dir=/backup/mysql/full_decrypted

# 恢复
xtrabackup --copy-back --target-dir=/backup/mysql/full_decrypted
```

---

## 7. 部分备份

### 7.1 备份指定表空间

```bash
# 获取表空间列表
mysql -e "SELECT tablespace_name FROM information_schema.files WHERE file_type='TABLESPACE';"

# 备份指定表空间
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/partial \
  --include="^mysql/.*" \
  --parallel=4
```

### 7.2 备份指定数据库

```bash
# 备份单个数据库
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/mydb \
  --databases="mydb" \
  --parallel=4

# 备份多个数据库
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/multi \
  --databases="mydb1 mydb2 mydb3" \
  --parallel=4

# 使用文件指定数据库列表
echo -e "mydb1\nmydb2\nmydb3" > /tmp/db_list.txt
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/multi \
  --databases-file=/tmp/db_list.txt
```

### 7.3 备份指定表

```bash
# 备份指定表
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/tables \
  --databases="mydb.users mydb.orders" \
  --parallel=4
```

### 7.4 恢复部分备份

```bash
# Prepare 部分备份
xtrabackup --prepare --target-dir=/backup/mysql/mydb \
  --export

# 生成可传输表空间
# 会在目录下生成 .cfg 文件

# 在目标数据库中导入
mysql -e "CREATE TABLE mydb.users (...); "
mysql -e "ALTER TABLE mydb.users DISCARD TABLESPACE;"

# 复制 .ibd 和 .cfg 文件
cp /backup/mysql/mydb/mydb/users.{ibd,cfg} /var/lib/mysql/mydb/
chown mysql:mysql /var/lib/mysql/mydb/users.*

# 导入表空间
mysql -e "ALTER TABLE mydb.users IMPORT TABLESPACE;"
```

---

## 8. 流式备份与压缩

### 8.1 xbstream 格式（推荐）

```bash
# 流式备份
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=xbstream \
  > /backup/mysql/full.xbstream

# 解压
xbstream -x -C /backup/mysql/restore < /backup/mysql/full.xbstream
```

### 8.2 流式备份到远程服务器

```bash
# 通过 SSH 传输到远程服务器
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=xbstream \
  | ssh user@remote "xbstream -x -C /backup/mysql/remote"

# 压缩后传输
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=xbstream \
  | gzip | ssh user@remote "cat > /backup/mysql/remote.xbstream.gz"

# 远程解压
ssh user@remote "gunzip -c /backup/mysql/remote.xbstream.gz | xbstream -x -C /backup/mysql/restore"
```

### 8.3 tar 格式流式备份

```bash
# tar 格式流式备份
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=tar \
  > /backup/mysql/full.tar

# 解压
tar -xf /backup/mysql/full.tar -C /backup/mysql/restore
```

### 8.4 压缩选项对比

| 压缩方式 | 参数 | 压缩比 | 速度 |
|----------|------|--------|------|
| **lz4** | `--compress=lz4` | 中 | 最快 |
| **lzo** | `--compress=lzo` | 中 | 快 |
| **zlib** | `--compress=zlib` | 高 | 中 |
| **zstd** | `--compress=zstd` | 最高 | 慢 |

```bash
# lz4 压缩（推荐，速度快）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full \
  --compress=lz4 \
  --compress-threads=4

# zstd 压缩（最高压缩比）
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/backup/mysql/full \
  --compress=zstd \
  --compress-threads=4
```

---

## 9. 定时备份脚本

### 9.1 完整备份脚本（含增量链）

```bash
#!/bin/bash
# /usr/local/bin/xtrabackup_full.sh

# ===== 配置 =====
DB_USER="backup"
DB_PASS="<示例密码>"
BACKUP_ROOT="/backup/mysql"
FULL_DIR="$BACKUP_ROOT/full"
INCR_DIR="$BACKUP_ROOT/incremental"
LOG_DIR="$BACKUP_ROOT/logs"
RETENTION_DAYS=30
DATE=$(date +%F)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ===== 初始化 =====
mkdir -p $FULL_DIR $INCR_DIR $LOG_DIR
LOG_FILE="$LOG_DIR/xtrabackup_$TIMESTAMP.log"

log() {
  echo "[$(date '+%F %T')] $1" | tee -a $LOG_FILE
}

# ===== 备份函数 =====
do_backup() {
  local backup_type=$1
  local target_dir=$2
  local base_dir=$3
  
  if [ "$backup_type" == "full" ]; then
    log "开始全量备份：$target_dir"
    xtrabackup --user=$DB_USER --password=$DB_PASS \
      --backup \
      --target-dir=$target_dir \
      --parallel=4 \
      --compress=lz4 \
      --compress-threads=4 \
      --checksum \
      2>&1 | tee -a $LOG_FILE
  else
    log "开始增量备份：$target_dir (基于：$base_dir)"
    xtrabackup --user=$DB_USER --password=$DB_PASS \
      --backup \
      --target-dir=$target_dir \
      --incremental-basedir=$base_dir \
      --parallel=4 \
      --compress=lz4 \
      --compress-threads=4 \
      --checksum \
      2>&1 | tee -a $LOG_FILE
  fi
  
  return $?
}

# ===== 主逻辑 =====
log "===== 备份开始 ====="

# 获取最新备份
LATEST_FULL=$(ls -td $FULL_DIR/*/ 2>/dev/null | head -1)
LATEST_INCR=$(ls -td $INCR_DIR/*/ 2>/dev/null | head -1)

# 判断备份类型（每周日全量，其他时间增量）
WEEKDAY=$(date +%u)
if [ $WEEKDAY -eq 7 ] || [ -z "$LATEST_FULL" ]; then
  # 周日或无全量备份：执行全量
  TARGET_DIR="$FULL_DIR/$DATE"
  do_backup "full" "$TARGET_DIR" ""
  BACKUP_RESULT=$?
else
  # 其他时间：执行增量
  if [ -z "$LATEST_INCR" ]; then
    BASE_DIR="$LATEST_FULL"
  else
    BASE_DIR="$LATEST_INCR"
  fi
  TARGET_DIR="$INCR_DIR/$DATE"
  do_backup "incremental" "$TARGET_DIR" "$BASE_DIR"
  BACKUP_RESULT=$?
fi

# ===== 结果处理 =====
if [ $BACKUP_RESULT -eq 0 ]; then
  log "备份成功：$TARGET_DIR"
  log "备份大小：$(du -sh $TARGET_DIR | cut -f1)"
else
  log "备份失败！退出码：$BACKUP_RESULT"
  exit 1
fi

# ===== 清理旧备份 =====
log "清理 $RETENTION_DAYS 天前的备份"
find $FULL_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null
find $INCR_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null
find $LOG_DIR -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null

log "===== 备份完成 ====="

# ===== 发送告警（可选） =====
# if [ $BACKUP_RESULT -ne 0 ]; then
#   mail -s "XtraBackup Failed on $(hostname)" admin@example.com < $LOG_FILE
# fi
```

### 9.2 添加定时任务

```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点备份
0 2 * * * /usr/local/bin/xtrabackup_full.sh

# 或使用系统 cron 目录
cp /usr/local/bin/xtrabackup_full.sh /etc/cron.daily/xtrabackup
chmod +x /etc/cron.daily/xtrabackup
```

### 9.3 备份到云存储

```bash
#!/bin/bash
# /usr/local/bin/xtrabackup_s3.sh

DATE=$(date +%F)
BACKUP_DIR=/backup/mysql/stream
S3_BUCKET=s3://my-backup-bucket/mysql

# 流式备份到 S3
xtrabackup --user=backup --password=<示例密码> \
  --backup \
  --target-dir=/tmp/backup \
  --stream=xbstream \
  | gzip \
  | aws s3 cp - $S3_BUCKET/full_$DATE.xbstream.gz

# 检查上传结果
if [ $? -eq 0 ]; then
  echo "[$(date)] S3 备份成功" >> /var/log/xtrabackup_s3.log
  # 清理本地临时文件
  rm -rf /tmp/backup
else
  echo "[$(date)] S3 备份失败" >> /var/log/xtrabackup_s3.log
  exit 1
fi
```

---

## 10. 备份验证与监控

### 10.1 验证备份完整性

```bash
# 检查备份目录
ls -la /backup/mysql/full/

# 查看备份元数据
cat /backup/mysql/full/backup-my.cnf
cat /backup/mysql/full/xtrabackup_checkpoints
cat /backup/mysql/full/xtrabackup_info.json

# 检查 LSN 连续性
grep lsn /backup/mysql/full/xtrabackup_checkpoints
grep lsn /backup/mysql/incr_mon/xtrabackup_checkpoints
```

### 10.2 验证备份可恢复性

```bash
# 定期测试恢复（建议每月）
TEST_DIR=/backup/mysql/test_restore

# Prepare 备份
xtrabackup --prepare --target-dir=/backup/mysql/full

# 复制到测试目录
mkdir -p $TEST_DIR
xtrabackup --copy-back --target-dir=/backup/mysql/full --datadir=$TEST_DIR

# 检查文件
ls -la $TEST_DIR/

# 清理
rm -rf $TEST_DIR
```

### 10.3 监控脚本

```bash
#!/bin/bash
# /usr/local/bin/xtrabackup_monitor.sh

BACKUP_ROOT="/backup/mysql"
ALERT_EMAIL="admin@example.com"

# 检查最新备份时间
LATEST_BACKUP=$(ls -td $BACKUP_ROOT/full/*/ $BACKUP_ROOT/incremental/*/ 2>/dev/null | head -1)
if [ -z "$LATEST_BACKUP" ]; then
  echo "ERROR: 未找到任何备份" | mail -s "XtraBackup 告警" $ALERT_EMAIL
  exit 1
fi

# 检查备份是否超过 24 小时
BACKUP_TIME=$(stat -c %Y $LATEST_BACKUP)
CURRENT_TIME=$(date +%s)
AGE_HOURS=$(( (CURRENT_TIME - BACKUP_TIME) / 3600 ))

if [ $AGE_HOURS -gt 24 ]; then
  echo "WARNING: 备份已超过 $AGE_HOURS 小时" | mail -s "XtraBackup 告警" $ALERT_EMAIL
  exit 1
fi

# 检查备份大小
BACKUP_SIZE=$(du -s $LATEST_BACKUP | cut -f1)
if [ $BACKUP_SIZE -lt 1000 ]; then  # 小于 1MB 可能有问题
  echo "WARNING: 备份大小异常：$BACKUP_SIZE KB" | mail -s "XtraBackup 告警" $ALERT_EMAIL
  exit 1
fi

# 检查磁盘空间
DISK_USAGE=$(df /backup | tail -1 | awk '{print $5}' | tr -d '%')
if [ $DISK_USAGE -gt 90 ]; then
  echo "WARNING: 备份磁盘使用率：$DISK_USAGE%" | mail -s "XtraBackup 告警" $ALERT_EMAIL
  exit 1
fi

echo "[$(date)] 备份检查正常" >> /var/log/xtrabackup_monitor.log
```

### 10.4 查看备份历史

```bash
# 查看备份日志
tail -50 /backup/mysql/logs/xtrabackup_*.log

# 查看备份统计
grep -h "备份成功\|备份失败" /backup/mysql/logs/*.log | sort | uniq -c

# 生成备份报告
cat << EOF
===== 备份报告 =====
最新全量备份：$(ls -td /backup/mysql/full/*/ | head -1)
最新增量备份：$(ls -td /backup/mysql/incremental/*/ | head -1)
备份总数：$(ls -d /backup/mysql/full/*/ /backup/mysql/incremental/*/ 2>/dev/null | wc -l)
总大小：$(du -sh /backup/mysql | cut -f1)
磁盘使用：$(df -h /backup | tail -1 | awk '{print $5}')
EOF
```

---

## 11. 常见错误与解决方案

### ❌ 错误 1：xtrabackup: Command not found

```
bash: xtrabackup: command not found
```

**原因：** 未安装或 PATH 未配置

**解决：**
```bash
# 检查安装
which xtrabackup
dpkg -l | grep xtrabackup

# 重新安装
apt-get install percona-xtrabackup-80

# 或添加 PATH
export PATH=$PATH:/usr/bin
```

---

### ❌ 错误 2：Access denied for user

```
xtrabackup: error while loading shared libraries
xtrabackup: [ERROR] Access denied for user 'backup'@'localhost'
```

**原因：** 用户名/密码错误或权限不足

**解决：**
```bash
# 测试连接
mysql -u backup -p<示例密码> -e "SELECT 1;"

# 检查权限
mysql -e "SHOW GRANTS FOR 'backup'@'localhost';"

# 重新授权
GRANT BACKUP_ADMIN, SESSION_VARIABLES_ADMIN ON *.* TO 'backup'@'localhost';
GRANT RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT ON *.* TO 'backup'@'localhost';
FLUSH PRIVILEGES;
```

---

### ❌ 错误 3：Missing or unknown parameter

```
xtrabackup: [ERROR] Unknown option --compress
```

**原因：** 版本不匹配（XtraBackup 2.4 不支持某些 8.0 参数）

**解决：**
```bash
# 检查版本
xtrabackup --version

# MySQL 8.0 使用 XtraBackup 8.0
# MySQL 5.7 使用 XtraBackup 2.4

# 或使用兼容参数
# XtraBackup 2.4 使用 --compress，8.0 使用 --compress=lz4
```

---

### ❌ 错误 4：Directory /path/to/backup is not empty

```
xtrabackup: [ERROR] Directory '/backup/mysql/full' is not empty
```

**原因：** 目标目录已有文件

**解决：**
```bash
# 使用空目录或带时间戳
xtrabackup --backup --target-dir=/backup/mysql/full_$(date +%F)

# 或清空目录
rm -rf /backup/mysql/full/*
xtrabackup --backup --target-dir=/backup/mysql/full
```

---

### ❌ 错误 5：Can't create/write to file: Permission denied

```
xtrabackup: [ERROR] Can't create/write to file '/backup/mysql/full/ibdata1': Permission denied
```

**原因：** 目录权限问题

**解决：**
```bash
# 修复权限
chown -R mysql:mysql /backup/mysql
chmod -R 750 /backup/mysql

# 或使用 root 运行
sudo xtrabackup --backup --target-dir=/backup/mysql/full
```

---

### ❌ 错误 6：Unsupported redo log format

```
xtrabackup: [ERROR] Unsupported redo log format.
```

**原因：** XtraBackup 版本与 MySQL 版本不匹配

**解决：**
```bash
# 检查版本兼容性
mysql --version
xtrabackup --version

# MySQL 8.0 必须用 XtraBackup 8.0
# 卸载旧版本，安装正确版本
apt-get remove percona-xtrabackup-24
apt-get install percona-xtrabackup-80
```

---

### ❌ 错误 7：The --incremental-basedir option requires a valid directory

```
xtrabackup: [ERROR] The --incremental-basedir option requires a valid directory
```

**原因：** 增量备份基于的目录无效或不存在

**解决：**
```bash
# 检查基础备份目录
ls -la /backup/mysql/full/
cat /backup/mysql/full/xtrabackup_checkpoints

# 确保基础备份已完成 Prepare
xtrabackup --prepare --target-dir=/backup/mysql/full

# 使用正确的路径
xtrabackup --backup --incremental-basedir=/backup/mysql/full --target-dir=/backup/mysql/incr
```

---

### ❌ 错误 8：Missing xtrabackup_checkpoints file

```
xtrabackup: [ERROR] Missing xtrabackup_checkpoints file
```

**原因：** 备份不完整或损坏

**解决：**
```bash
# 检查备份完整性
ls -la /backup/mysql/full/

# 重新执行全量备份
xtrabackup --backup --target-dir=/backup/mysql/full_new

# 如果增量链断裂，重新从全量开始
```

---

### ❌ 错误 9：Protocol mismatch

```
xtrabackup: [ERROR] Protocol mismatch between server and client
```

**原因：** MySQL 8.0 认证插件问题

**解决：**
```bash
# 修改用户认证方式
mysql -e "ALTER USER 'backup'@'localhost' IDENTIFIED WITH mysql_native_password BY '<示例密码>';"
FLUSH PRIVILEGES;

# 或在 my.cnf 中添加
# [client]
# default-authentication-plugin=mysql_native_password
```

---

### ❌ 错误 10：Out of disk space during backup

```
xtrabackup: [ERROR] Write failed: No space left on device
```

**原因：** 磁盘空间不足

**解决：**
```bash
# 检查磁盘空间
df -h /backup

# 清理旧备份
find /backup/mysql -type d -mtime +30 -exec rm -rf {} \;

# 使用压缩备份
xtrabackup --backup --target-dir=/backup/mysql/full --compress=lz4

# 或备份到其他磁盘
xtrabackup --backup --target-dir=/mnt/external/mysql_backup
```

---

### ❌ 错误 11：Prepare failed: InnoDB: Invalid page

```
xtrabackup: [ERROR] Prepare failed: InnoDB: Invalid page
```

**原因：** 备份文件损坏或不完整

**解决：**
```bash
# 检查备份文件
ls -la /backup/mysql/full/

# 尝试重新 Prepare
xtrabackup --prepare --target-dir=/backup/mysql/full --use-memory=2G

# 如果仍然失败，重新备份
xtrabackup --backup --target-dir=/backup/mysql/full_new
```

---

### ❌ 错误 12：MySQL server has gone away

```
xtrabackup: [ERROR] MySQL server has gone away
```

**原因：** 连接超时或 MySQL 重启

**解决：**
```bash
# 增加超时时间
xtrabackup --backup --target-dir=/backup/mysql/full --lock-wait-timeout=300

# 检查 MySQL 状态
systemctl status mysql

# 增加 MySQL 超时配置
# /etc/mysql/mysql.conf.d/mysqld.cnf
wait_timeout = 28800
interactive_timeout = 28800
```

---

## 12. 最佳实践

### ✅ 备份策略

| 数据库大小 | 推荐策略 | 频率 |
|------------|----------|------|
| < 50GB | 全量备份 | 每天 |
| 50GB-500GB | 周日全量 + 每日增量 | 周日全量，周一至周六增量 |
| > 500GB | 周日全量 + 每日差异 | 周日全量，每日差异 |

### ✅ 3-2-1 备份原则

- **3** 份数据副本
- **2** 种不同介质
- **1** 份异地备份

### ✅ 推荐配置

```bash
# 全量备份（周日）
xtrabackup --backup \
  --target-dir=/backup/mysql/full_$(date +%F) \
  --parallel=4 \
  --compress=lz4 \
  --compress-threads=4 \
  --checksum

# 增量备份（周一至周六）
xtrabackup --backup \
  --target-dir=/backup/mysql/incr_$(date +%F) \
  --incremental-basedir=/path/to/latest_backup \
  --parallel=4 \
  --compress=lz4
```

### ✅ 恢复测试

```bash
# 每月至少做一次完整恢复测试
# 记录 RTO（恢复时间目标）
time xtrabackup --prepare --target-dir=/backup/mysql/full
time xtrabackup --copy-back --target-dir=/backup/mysql/full
```

### ✅ 监控告警

```bash
# 监控项
- 备份是否按时完成
- 备份大小是否异常
- 磁盘空间使用率
- 备份链是否连续

# 告警阈值
- 备份延迟 > 2 小时
- 磁盘使用率 > 90%
- 备份大小变化 > 50%
```

### ✅ 安全建议

1. **备份加密**：敏感数据使用 AES256 加密
2. **权限控制**：备份目录只允许 mysql/root 访问
3. **网络传输加密**：远程备份使用 SSH
4. **审计日志**：记录所有备份和恢复操作
5. **定期轮换密码**：备份用户密码定期更换

---

## 📋 快速参考卡片

```bash
# ===== 全量备份 =====
xtrabackup --backup --target-dir=/backup/mysql/full --compress=lz4

# ===== 增量备份 =====
xtrabackup --backup --target-dir=/backup/mysql/incr --incremental-basedir=/backup/mysql/full

# ===== Prepare 全量 =====
xtrabackup --prepare --target-dir=/backup/mysql/full

# ===== Prepare 全量 + 增量 =====
xtrabackup --prepare --apply-log-only --target-dir=/backup/mysql/full
xtrabackup --prepare --target-dir=/backup/mysql/full --incremental-dir=/backup/mysql/incr

# ===== 恢复 =====
systemctl stop mysql
mv /var/lib/mysql /var/lib/mysql.bak
xtrabackup --copy-back --target-dir=/backup/mysql/full
systemctl start mysql

# ===== 流式备份 =====
xtrabackup --backup --target-dir=/tmp --stream=xbstream > backup.xbstream

# ===== 解压 =====
xbstream -x -C /backup/mysql/restore < backup.xbstream

# ===== 检查备份 =====
cat /backup/mysql/full/xtrabackup_checkpoints
cat /backup/mysql/full/xtrabackup_info.json
```

---

## 🔗 相关资源

- **官方文档：** https://www.percona.com/doc/percona-xtrabackup/
- **GitHub：** https://github.com/percona/percona-xtrabackup
- **下载：** https://www.percona.com/downloads/Percona-XtraBackup-8.0/

---

> 💡 **刺刺提醒：** 
> 1. 备份不测试 = 没有备份！定期做恢复演练！
> 2. 增量备份链断裂 = 灾难！定期检查 xtrabackup_checkpoints！
> 3. Prepare 是必须步骤！不要跳过！😈
## 常用指令

- xtrabackup --backup --target-dir=/backup/full --user=<user> --password=<password>
- xtrabackup --prepare --target-dir=/backup/full
- systemctl stop mysqld
- xtrabackup --copy-back --target-dir=/backup/full
- chown -R mysql:mysql /var/lib/mysql
- systemctl start mysqld
- xtrabackup --backup --target-dir=/backup/inc1 --incremental-basedir=/backup/full --user=<user> --password=<password>
- cat /backup/full/xtrabackup_checkpoints

