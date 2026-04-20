# 3_SRM-部署文档

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [srm]
issue_types: [reference]
tags: [engineer-doc, imported, srm]
source_path: "D:\新建文件夹\业务维护清单\SRM\3_SRM-部署文档.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：3_SRM-部署文档.docx
- 原始路径：D:\新建文件夹\业务维护清单\SRM
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

SRM本地化部署

环境架构图

服务器部署说明

| 服务器 | 部署应用 |

| 应用 | nginx、tomcat(interface)、JDK |

| 数据库 | MYSQL、boost、redis、mongodb |

软件版本介绍

1. 服务器系统版本： linux centos 系列

2. 代理服务： Nginx 1.20.0

3. 应用服务： JDK1.8、tomcat 7.0.104

4. 数据库服务： mysql 5.7.35 、  redis 4.0.14、mongodb4.0.17

目录介绍说明。创建！

/data/software/     ###软件包存放目录。

/data/script/     ##脚本存放目录。

/home/app/        ###SRM软件部署目录【非绝对，根据磁盘分区大小决定，可能是/data/app,或/mnt/local】

服务器设置及优化 【脚本一键执行。】（可脚本执行也可手动部署）

脚本一键执行

手动部署

关闭防火墙及selinux

systemctl stop firewalld

systemctl disable firewalld

sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config

setenforce 0

设置文件最大描述符

echo "* soft nofile 100001" >> /etc/security/limits.conf

echo "* hard nofile 100001" >> /etc/security/limits.conf

内核优化

cp /etc/sysctl.conf /etc/sysctl.conf.bak

cat > /etc/sysctl.conf <<EOF

net.ipv4.neigh.default.gc_stale_time=120

net.ipv4.conf.default.arp_announce = 2

net.ipv4.conf.all.arp_announce=2

net.ipv4.conf.lo.arp_announce=2

net.ipv4.icmp_echo_ignore_broadcasts = 1

net.ipv4.icmp_ignore_bogus_error_responses = 1

net.ipv4.ip_forward = 0

net.ipv4.conf.all.send_redirects = 0

net.ipv4.conf.default.send_redirects = 0

net.ipv4.conf.all.rp_filter = 1

net.ipv4.conf.default.rp_filter = 1

net.ipv4.conf.all.accept_source_route = 0

net.ipv4.conf.default.accept_source_route = 0

kernel.sysrq = 0

kernel.core_uses_pid = 1

net.ipv4.tcp_syncookies = 1

kernel.msgmnb = 65536

kernel.msgmax = 65536

kernel.shmmax = 68719476736

kernel.shmall = 4294967296

net.ipv4.tcp_max_tw_buckets = 6000

net.ipv4.tcp_sack = 1

net.ipv4.tcp_window_scaling = 1

net.ipv4.tcp_rmem = 4096        87380   4194304

net.ipv4.tcp_wmem = 4096        16384   4194304

net.core.wmem_default = 8388608

net.core.rmem_default = 8388608

net.core.rmem_max = 16777216

net.core.wmem_max = 16777216

net.core.netdev_max_backlog = 262144

net.ipv4.tcp_max_orphans = 3276800

net.ipv4.tcp_max_syn_backlog = 262144

net.ipv4.tcp_timestamps = 0

net.ipv4.tcp_synack_retries = 1

net.ipv4.tcp_syn_retries = 1

net.ipv4.tcp_tw_recycle = 1

net.ipv4.tcp_tw_reuse = 1

net.ipv4.tcp_mem = 94500000 915000000 927000000

net.ipv4.tcp_fin_timeout = 1

net.ipv4.tcp_keepalive_time = 1800

net.ipv4.tcp_keepalive_probes = 3

net.ipv4.tcp_keepalive_intvl = 15

net.ipv4.ip_local_port_range = 1024    65000

net.ipv4.conf.all.accept_redirects = 0

net.ipv4.conf.default.accept_redirects = 0

net.ipv4.conf.all.secure_redirects = 0

net.ipv4.conf.default.secure_redirects = 0

EOF

sysctl -p

安装nginx-1.20.0

安装服务相关依赖

yum install pcre pcre-devel openssl openssl-devel gcc-c++ gcc -y

创建服务的用户

useradd nginx -s /sbin/nologin -M

解压及初始化(安装位置视情况而变)

wget http://nginx.org/download/nginx-1.20.1.tar.gz

tar -zxvf nginx-1.20.1.tar.gz && cd nginx-1.20.1

./configure --user=nginx --group=nginx --prefix=/home/app/srm_nginx --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-http_stub_status_module --with-http_v2_module --with-stream

执行安装命令。

make && make install

将nginx添加到系统命令

ln -s /home/app/srm_nginx/sbin/nginx /usr/bin/

验证nginx安装

nginx -v

常用命令介绍

nginx   启动

nginx -t 检查语法

nginx -s reload  #重新加载

加入systemctl

2.加入systemctl

vim /usr/lib/systemd/system/nginx.service

[Unit]

Description=nginx-high performance web server

After=network.target remote-fs.target nss-lookup.target

[Service]

Type=forking

ExecStart=/home/app/srm_nginx/sbin/nginx

ExecReload=/home/app/srm_nginx/sbin/nginx -s reload

ExecStop=/home/app/srm_nginx/sbin/nginx -s stop

ExecStatus=/home/app/srm_nginx/sbin/nginx -t

[Install]

WantedBy=multi-user.target

-----------------------------------------------------------------------------------

chmod 754 /usr/lib/systemd/system/nginx.service

systemctl daemon-reload  #重新挂载

systemctl start nginx.service    #启动

systemctl enable nginx.service   #开机自启动

Nginx 默认配置文件。

user  root;

worker_processes  8;

events {

worker_connections  102400;

}

http {

include       mime.types;

default_type  application/octet-stream;

server_tokens off;

log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '

'$status $body_bytes_sent "$http_referer" '

'"$http_user_agent" "$http_x_forwarded_for"'

'$upstream_addr $upstream_response_time $request_time ';

access_log logs/access.log main;

error_log logs/error.log notice;

sendfile        on;

tcp_nopush on;

tcp_nodelay on;

keepalive_timeout  65;

send_timeout 360;

client_max_body_size 200M;

proxy_connect_timeout 6000;

proxy_send_timeout 6000;

proxy_read_timeout 6000;

proxy_buffer_size       16k;

proxy_buffers           4 64k;

proxy_busy_buffers_size 128k;

proxy_temp_file_write_size 128k;

gzip on;

gzip_min_length 1k;

gzip_buffers 4 32k;

gzip_http_version 1.0;

gzip_comp_level 5;

gzip_types text/plain application/x-javascript text/css application/xml text/javascript application/x-httpd-php;

gzip_vary off;

gzip_disable "MSIE [1-6].";

fastcgi_intercept_errors on;

include domain/*.conf;

}

srm服务配置文件https样式 (修改nginx代理端口，srm访问地址，srm应用所在服务器IP及端口，tomcat所在服务器IP端口，im应用所在服务器IP及端口，report所在服务器IP及端口)

server {

listen       80;  #nginx代理端口

server_name  <IP地址已脱敏>;  #srm访问地址

charset utf-8;

add_header X-Frame-Options "SAMEORIGIN";

add_header X-XSS-Protection "1; mode=block";

add_header X-Content-Type-Options "nosniff";

#access_log  /tmp/sit.log  main;

####前端访问配置

location / {

root   /opt/nfsshare/webpage/web-srm/dist/; #前端路径

index  index.html index.htm;

try_files $uri $uri/ /index.html;

}

####interface接口平台

location ^~/els-interface-base/ {

proxy_pass      http://<IP地址已脱敏>:9012/els-interface-base/;

proxy_redirect http:// https://;

proxy_set_header        X-Real-IP       $remote_addr;

proxy_set_header        Host            $host;

proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;

proxy_pass_request_headers      on;

}

#####移动前端访问配置##

location ^~/mobile {

if (-d $request_filename){

rewrite ^/(.*)([^/])$https://$host/$1$2/ permanent;

}

alias /opt/nfsshare/webpage/web-srm/app/mobile/; #移动前端路径

index  index.html index.htm;

try_files $uri $uri/ /index.html;

}

###客服前端配置###

location ^~/kefu {

if (-d $request_filename){

rewrite ^/(.*)([^/])$https://$host/$1$2/ permanent;

}

alias /opt/nfsshare/webpage/web-srm/im/dist/;

index  index.html index.htm;

try_files $uri $uri/ /kefu/index.html;

}

###opt前端挂载共享###

location ~ ^/(images|img|javascript|js|im|css|tinymce|flash|media|static)/

{

root /opt/nfsshare/webpage/web-srm/dist/;

gzip_static on;

autoindex off;

}

###srm-后端####

location ^~/els {

proxy_pass http://<IP地址已脱敏>:12381; #srm应用IP及启动端口

proxy_set_header X-Real-IP $remote_addr;

proxy_connect_timeout       3000;

proxy_send_timeout          3000;

proxy_read_timeout          3000;

send_timeout                3000;

}

###srm-websocket在srm后端###

location /els/websocket  {

proxy_pass http://<IP地址已脱敏>:12381; # srm应用IP及启动端口

proxy_http_version 1.1;

proxy_set_header Upgrade $http_upgrade;

proxy_set_header Connection "Upgrade";

proxy_set_header X-real-ip $remote_addr;

proxy_set_header X-Forwarded-For $remote_addr;

}

####im-###

location /els/im  {

proxy_pass http://<IP地址已脱敏>:8888; #im应用IP及启动端口

proxy_set_header X-real-ip $remote_addr;

proxy_set_header X-Forwarded-For $remote_addr;

}

####im-websocket在im- 后端-##

location /els/imChat  {

proxy_pass http://<IP地址已脱敏>:9326; #im应用IP及websocket启动端口

proxy_http_version 1.1;

proxy_set_header Upgrade $http_upgrade;

proxy_set_header Connection "Upgrade";

proxy_set_header X-real-ip $remote_addr;

proxy_set_header X-Forwarded-For $remote_addr;

}

####报表report###

location /els/report  {

proxy_pass http://<IP地址已脱敏>:8085; #report应用IP及启动端口

proxy_set_header X-real-ip $remote_addr;

proxy_set_header X-Forwarded-For $remote_addr;

}

###后端共享挂载js

location /opt/ {

alias /opt/nfsshare/webpage/web-srm/;

gzip_static on;

autoindex off;

}

}

安装JDK1.8

软件包默认存放在/data/software 下，如图所示： 支持jdk1.8.xx版本。

解压到安装目录。

tar -zxvf jdk1.8.0_141.tar.gz

mv jdk1.8.0_141 /home/app/srm_jdk

写入java配置至环境变量文件。

export JAVA_HOME=/home/app/srm_jdk

export PATH=$JAVA_HOME/bin:$PATH

export CLASSPATH=$JAVA_HOME/jre/lib/ext:$JAVA_HOME/lib/tools.jar

重新加载环境变量。

source /etc/profile

验证jdk是否安装成功。

java -version

安装MYSQL5.7.35

卸载默认mariadb

rpm -qa|grep mariadb

yum remove mariadb* -y

yum安装mysql服务相关依赖

yum -y install cmake bison ncurses ncurses-devel git gcc gcc-c++ ncurses-devel bison

本地安装boost依赖。

上传boost_1_59_0、mysql5.7.35源码包至/data/software目录下。

tar -zxf boost_1_59_0.tar.gz   ###解压至安装目录。

mv boost_1_59_0 /home/app/srm_boost   ###改文件名

创建mysql用户及相关目录

groupadd  -r mysql && useradd -r -g mysql -s /bin/false -M mysql

编译安装mysql5.7.35

cd mysql-5.7.35/

cmake . -DCMAKE_INSTALL_PREFIX=/home/app/srm_mysql -DMYSQL_DATADIR=/home/app/srm_mysql/data -DSYSCONFDIR=/etc -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DEXTRA_CHARSETS=all -DMYSQL_UNIX_ADDR=/home/app/srm_mysql/mysql.sock -DWITH_MYISAM_STORAGE_ENGINE=1 -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_PARTITION_STORAGE_ENGINE=1 -DWITH_SYSTEMD=1 -DWITH_BOOST=/home/app/srm_boost

make -j`nproc` && make -j`nproc` install

编译相关说明。

注解：

-DCMAKE_INSTALL_PREFIX=/app/mysql    #mysql安装的根目录

-DMYSQL_DATADIR=/app/mysql/data   #mysql数据库文件存放目录

-DSYSCONFDIR=/etc  #mysql配置文件所在目录

-DWITH_MYISAM_STORAGE_ENGINE=1  #添加MYISAM引擎支持

-DWITH_INNOBASE_STORAGE_ENGINE=1 #添加InnoDB引擎支持

-DWITH_ARCHIVE_STORAGE_ENGINE=1 #添加ARCHIVE引擎支持

-DMYSQL_UNIX_ADDR=/app/mysql/mysql.sock  #指定mysql.sock位置

-DWITH_PARTITION_STORAGE_ENGINE=1  #安装支持数据库分区

-DEXTRA_CHARSETS=all  #使mysql支持所有的扩展字符

-DDEFAULT_CHARSET=utf8 #设置mysql的默认字符集为utf8

-DDEFAULT_COLLATION=utf8_general_ci #设置默认字符集校对规则

-DWITH-SYSTEMD=1 #可以使用systemd控制mysql服务

-DWITH_BOOST=/home/app/boost  #指向boost库所在目录

设置MySQL环境变量

export MYSQL_HOME=/home/app/srm_mysql

export PATH=$PATH:$MYSQL_HOME/bin

设置mysql目录权限。

mkdir /home/app/srm_mysql/{mysqld,logs,data} -p

chown -R mysql. /home/app/srm_mysql

chmod  755  /home/app/srm_mysql/data/

初始化数据库

cd home/srm/srm_mysql/

mysqld --initialize --user=mysql --basedir=/home/app/srm_mysql --datadir=/home/app/srm_mysql/data

!!这里初始化后会出来mysql默认密码，需要记下来。

配置/etc/my.cnf文件

vim /etc/my.cnf    #内容根据实际情况修改 。

[mysqld]

skip_ssl

max_allowed_packet = 1024M

skip-name-resolve

max_connections=3000

default-storage-engine=InnoDB

innodb_buffer_pool_size = 16G

thread_cache_size = 16

innodb_thread_concurrency = 16

read_buffer_size = 32M

sort_buffer_size = 16M

query_cache_size = 1024M

wait_timeout = 100

read_buffer_size = 128M

read_rnd_buffer_size = 32M

slow_query_log = 1

long_query_time = 4

slow_query_log_file = /home/app/srm_mysql/logs/mysql.slow.log

datadir=/home/app/srm_mysql/data

socket=/home/app/srm_mysql/mysql.sock

port = 3306

character-set-server=utf8

collation-server=utf8_general_ci

symbolic-links=0

log-error=/home/app/srm_mysql/logs/error.log

pid-file=/home/app/srm_mysql/mysqld/mysqld.pid

server_id=1

log_bin = /home/app/srm_mysql/logs/mysql-bin

binlog_format = ROW

expire_logs_days = 15

设置mysql -  systemctl 启动关闭。

修改mysql服务文件的pid文件位置。

vim /home/app/srm_mysql/usr/lib/systemd/system/mysqld.service

复制修改好的mysqld.service  至系统system 目录下。

cp /home/app/srm_mysql/usr/lib/systemd/system/mysqld.service  /usr/lib/systemd/system/

systemctl daemon-reload    #重新加载systemcrl

systemctl  start mysqld    ##启动mysql

systemctl enable mysqld    ##加入开机自启动

修改初始化密码

mysql -uroot -p   输入上面记录的初始化密码登录mysql

alter user user( ) identified by 'newpassword';  修改密码

创建数据库及专用用户

create database srm_sit;

create database els_db_jiekou;

grant all on srm_sit.* to 'user'@'%' identified by 'password'；

grant all on els_db_jiekou.* to 'user'@'%' identified by 'password’

flush privileges;

安装redis-server

上传安装包至/data/software并解压

tar -zxf redis-4.0.14.tar.gz

cd redis-4.0.14

执行安装命令

make && make install

创建redis目录

mkdir /home/app/srm_redis/bin -p

cp /data/software/redis-4.0.14/redis.conf /home/srm/srm_redis/redis.conf

cp /data/software/redis-4.0.14/src/redis-server /home/srm/srm_redis/bin/

修改6379.conf配置文件

vim /data/srm/srm_redis/redis.conf  修改高亮处！

########6379.conf配置修改文件如下。####

bind <IP地址已脱敏>  #修改为本机IP

daemonize yes   #redis后台运行

requirepass Pass1q2w#e  #redis密码

设置开机自启

cp /data/software/redis-4.0.14/utils/redis_init_script /etc/init.d/redis6379

vim /etc/init.d/redis6379

修改redis配置文件路径

chmod a+x /etc/init.d/redis6379

chkconfig --add redis6379

启动

/etc/init.d/redis6379 start

验证安装成功

redis-server -v

部署mongodb。

下载mongodb安装包，解压到指定安装目录

yum -y install glibc  #下载mongodb依赖

设置环境变量

export MONGODB_HOME=/home/app/srm_mongodb

export PATH=$PATH:$MONGODB_HOME/bin

配置

在mongodb目录下新建data/db, logs两个目录

mkdir {data/db,logs} -p

在目录下新建mongodb.conf 文件,内容如下。

dbpath = /home/app/srm_mongodb/data/db

logpath = /home/app/srm_mongodb/logs/mongodb.log

port = 27017

fork = true

# 更改为mongodb所在服务器内网IP

bind_ip =

logappend = true

wiredTigerCacheSizeGB = 2

启动

启动方式 bin/mongod -f mongodb.conf

设置开机自启

开机自启动脚本：

#!/bin/bash

export MONGO_HOME=/home/app/srm_mongodb

#chkconfig:2345 20 90

#description:mongod

#processname:mongod

case $1 in

start)

$MONGO_HOME/bin/mongod --config $MONGO_HOME/mongodb.conf

;;

stop)

$MONGO_HOME/bin/mongod  --shutdown --config $MONGO_HOME/mongodb.conf

;;

status)

ps -ef | grep mongod

;;

restart)

$MONGO_HOME/bin/mongod  --shutdown --config $MONGO_HOME/mongodb.conf

$MONGO_HOME/bin/mongod --config $MONGO_HOME/mongodb.conf

;;

*)

echo "require start|stop|status|restart"

;;

esac

chmod a+x /etc/init.d/mongodb

chkconfig --add mongodb

登录及优化

登录方式  mongo --host ip

登录mongodb，创建库跟用户密码=<已脱敏> els_logs

db.createUser( {user: "qqt",pwd=<已脱敏> elsadmin#@!888888",roles: [ { role: "readWrite", db: "els_logs" } ]});

用户： qqt  密码=<已脱敏>   数据库：els_logs

执行优化命令

db.resend_value.createIndex({"id": -1},{background:true});

db.els_logs_input.createIndex({"id": -1},{background:true});

db.els_logs_output.createIndex({"id": -1},{background:true});

db.els_logs_actual_input.createIndex({"id": -1},{background:true});

db.els_logs_actual_output.createIndex({"id": -1},{background:true});

NFS服务端安装

yum 安装NFS-server

yum install -y nfs-utils rpcbind

启动并设置开机自启动

systemctl start rpcbind.service

systemctl enable rpcbind.service

systemctl start nfs-server.service

systemctl enable nfs-server.service

创建NFS存储目录，并修改配置

mkdir /opt/nfsshare

vim /etc/exports

/opt/nfsshare 192.168.0.*(rw,sync,all_squash)

设置指定端口[可略]

1.指定端口。

cat >> /etc/sysconfig/nfs <<EOF

RQUOTAD_PORT=30001

LOCKD_TCPPORT=30002

LOCKD_UDPPORT=30002

MOUNTD_PORT=30003

STATD_PORT=30004

EOF

2.重启rpc、nfs服务

systemctl restart rpcbind.service

systemctl restart nfs.service

3.指定端口

cat >> /etc/modprobe.d/lockd.conf <<EOF

options lockd nlm_tcpport=30002

options lockd nlm_udpport=30002

EOF

4.重新加载nfs配置服务。

systemctl restart nfs-config

systemctl restart nfs-idmap

systemctl restart nfs-lock

systemctl restart nfs-server

如果不生效。将参数增加到/etc/sysctl.conf 内

fs.nfs.nlm_tcpport=30002

fs.nfs.nlm_udpport=30002

5.查看端口使用情况

rpcinfo -p

安装nfs客户端

yum -y install nfs-utils

systemctl start nfs

systemctl enable nfs

showmount -e <IP地址已脱敏>

mkdir /opt/nfsshare

mount -t nfs <IP地址已脱敏>:/opt/nfsshare /opt/nfsshare

客户端写入开机自启动文件。

echo "mount -t nfs <IP地址已脱敏>:/opt/nfsshare /opt/nfsshare" >>/etc/rc.d/rc.local

chmod a+x /etc/rc.d/rc.local

验证

挂载成功。

Rocketmq安装

源码安装方式

解压rocketmq

unzip rocketmq-all-4.9.0-bin-release.zip

mv rocketmq-all-4.9.0-bin-release/ rocketmq

更改配置文件

cd rocketmq/conf ; cp broker.conf broker.conf.bak ;

vim broker.conf

brokerClusterName = test1

brokerName = broker-a

brokerId = 0

deleteWhen = 04

fileReservedTime = 48

brokerRole = ASYNC_MASTER

flushDiskType = ASYNC_FLUSH

autoCreateTopicEnable = true

brokerIP1=<IP地址已脱敏>

namesrvAddr=<IP地址已脱敏>:9876

defaultTopicQueueNums=4

autoCreateSubscriptionGroup=true

listenPort=10911

mapedFileSizeCommitLog=1073741824

mapedFileSizeConsumeQueue=300000

diskMaxUsedSpaceRatio=88

storePathRootDir=/mnt/local/app/rocketmq/store

storePathCommitLog=/mnt/local/app/rocketmq/store/commitlog

storePathConsumeQueue=/mnt/local/app/rocketmq/store/consumequeue

storePathIndex=/mnt/local/app/rocketmq/store/index

storeCheckpoint=/mnt/local/app/rocketmq/store/checkpoint

abortFile=/mnt/local/app/rocketmq/store/abort

maxMessageSize=4194304

#根据需要是否需要远程连接，设置外网地址

#brokerIP1=<IP地址已脱敏>

#namesrvAddr=<IP地址已脱敏>:9876

创建日志和存储文件等目录

### mkdir -p /home/app/srm_rocketmq/logs /home/app/srm_rocketmq/store\ /home/app/srm_rocketmq/store/commitlog /home/app/srm_rocketmq/store/config\ /home/app/srm_rocketmq/store/consumequeue /home/app/srm_rocketmq/store/index

mkdir {logs,store/commitlog,store/config,store/consumequeue,store/index} -p

启动nameserver和broker

（最好修改下JVM参数）

nohup sh /home/app/rocketmq/bin/mqnamesrv >> /home/app/rocketmq/logs/mqnamesrv_stdout.log 2>&1 &

nohup sh /home/app/rocketmq/bin/mqbroker -c /home/app/rocketmq/conf/broker.conf >> /home/app/rocketmq/logs/broker_stdout.log 2>&1 &

安装可视化界面

wget https://codeload.github.com/apache/rocketmq-externals/zip/master -O rocketmq-externals.zip

unzip rocketmq-externals.zip -d /home/app/

cd /home/app/rocketmq-externals-master/rocketmq-console/

vim src/main/resources/application.properties

#端口为web客户端访问端口

server.port=18018

#这个填写自己的nameserver的地址，默认是localhost:9876

rocketmq.config.namesrvAddr=<IP地址已脱敏>:9876

#rocketmq-console的数据目录，默认为 /tmp/rocketmq-console/data

rocketmq.config.dataPath=/mnt/local/app/rocketmq-console/data

#开启认证登录功能，默认为false，密码默认admin/admin

rocketmq.config.loginRequired=true

编译rocketmq-console

使用maven进行编译

cd /home/app/rocketmq-externals-master/rocketmq-console/

mvn clean package -Dmaven.test.skip=true

#新建目录用来存放rocketmq-console的文件

mkdir /home/app/srm_rocketmq-console

cp target/rocketmq-console-ng-2.0.0.jar /mnt/local/app/rocketmq-console/

运行jar包

cd /usr/local/rocketmq-console/

java -jar rocketmq-console-ng-2.0.0.jar &> log &

验证

检测能否正常消费消息队列：

### export NAMESRV_ADDR=localhost:9876

### sh bin/tools.sh org.apache.rocketmq.example.quickstart.Producer

### sh bin/tools.sh org.apache.rocketmq.example.quickstart.Consumer

浏览器登录 :  http://localhost:18018

Rocketmq容器安装方式

安装docker和docker-compose

默认脚本安装，网络不好时使用二进制安装

脚本安装

[root@VM-6-27-centos ~]# install -d /data/{script,software}

授权执行下载的脚本即可

[root@master script]# cd /data/script

[root@master script]# wget -c https://officebak.51qqt.com/download/v5wserver/init_docker_env.sh

[root@master script]# chmod 700 init_docker_env.sh

#①请注意执行脚本后面传的路径是docker的数据目录，请按照服务器容量最大的盘做调整

#②经测试download.docker.com做了全球cdn节点请求的ip会发生变化，所以如果脚本没法执行请参考二进制安装方式即可，如果srm服务器出口不限制即可忽略二进制安装

[root@master script]# sh init_docker_env.sh /data/docker

3丶验证安装

二进制安装（网络不好的时候使用）

| 1丶下载docker安装包[root@master software]# cd /data/software[root@master software]# wget -c https://officebak.51qqt.com/download/v5wserver/docker-19.03.9.tgz2丶解压并配置配置systemctl启动[root@master software]# tar xf docker-19.03.9.tgz [root@master software]# mv docker/* /usr/bin/[root@master software]# rm -rf docker[root@master software]#cat > /usr/lib/systemd/system/docker.service << EOF[Unit]Description=Docker Application Container EngineDocumentation=https://docs.docker.comAfter=network-online.target firewalld.serviceWants=network-online.target[Service]Type=notifyExecStart=/usr/bin/dockerdExecReload=/bin/kill -s HUP $MAINPIDLimitNOFILE=infinityLimitNPROC=infinityLimitCORE=infinityTimeoutStartSec=0Delegate=yesKillMode=processRestart=on-failureStartLimitBurst=3StartLimitInterval=60s[Install]WantedBy=multi-user.targetEOF3丶配置docker配置文件[root@master software]# tee /etc/docker/daemon.json<<EOF{"graph": "/data/docker","bip": "<IP地址已脱敏>/24","registry-mirrors":["http://harbor.51qqt.com","https://registry.docker-cn.com","http://hub-mirror.c.163.com","https://docker.mirrors.ustc.edu.cn"],"insecure-registries": ["registry.access.rehat.com","quay.io","harbor.com"],"exec-opts": ["native.cgroupdriver=systemd"]}EOF4丶启动docker并查看版本信息[root@master software]# systemctl daemon-reload [root@master software]# systemctl start docker[root@master software]# docker -v5丶设置开机自启动[root@master software]# systemctl enable docker |

Docker-compose安装

| 1丶下载docker-compose[root@master bin]# cd /usr/local/bin/[root@master bin]# wget -c https://officebak.51qqt.com/download/v5wserver/docker-compose[root@master bin]# chmod +x docker-compose2丶验证安装[root@master bin]# docker-compose -v |

安装Rocket MQ

| 1丶创建rockermq的日志及存储路径（根据实际磁盘容量选择路径）[root@master ~]# cd /app/srm/docker-compose/[root@master docker-compose]# install -d ./rocketmq/logs[root@master docker-compose]# install -d ./rocketmq/store2、将下面这个文件放到当前目录下面2丶启动rocketmq[root@master docker-compose]# docker-compose up -d3丶验证rocketmqhttp://IP:18018#①默认账户：admin#②默认密码=<已脱敏> |

接口部署(接口平台)

接口基础要求.

a.服务器必须部署JDK1.8

b.Tomcat版本7.0.104

c.最新的接口war包，存放到tomcat- webapps 目录下d.接口数据库脚本。 按编号顺序导入数据库。 库名推荐els_db_jiekou

安装cronolog日志切割

Cronolog 主要是针对tomcat应用按天切割日志，方便tomcat查询日志。

上传软件至/data/software目录

解压并安装

tar -zxf cronolog-1.6.2.tar.gz

cd cronolog-1.6.2

./configure

make && make install

验证是否安装成功。

which cronolog

部署Tomcat7.0.104（interface）

上传并解压

tar -zxf apache-tomcat-7.0.104.tar.gz

修改文件名，方便识别。

mv apache-tomcat-7.0.104  /home/app/srm_interface

启动及停止命令

cd /home/app/srm_interface/bin/

./catalina.sh start      #开始

cd /home/app/srm_interface/bin/

./shutdown.sh             #停止

获取接口平台war包至webapps路径下

https://officebak.51qqt.com/download/interface-new/els-interface-base.war

启动tomcat以解压war包 修改配置

1、srm_interface/webapps/els-interface-base /WEB-INF/classes/sysconfig.properties

同时，修改：

mail_host=smtp.exmail.qq.com

mail_post=465

mail_sender=srmservice@51qqt.com

mail_username=srmservice@51qqt.com

mail_password=<已脱敏>

2、srm_interface/webapps/els-interface-base /WEB-INF/classes/dbconfig.properties

！数据库密码需加密

3、srm_interface/webapps/els-interface-base /WEB-INF/classes/sso.properties

#sso.cookie.domain配置二级域名

4、srm_interface/webapps/els-interface-base /WEB-INF/classes/redis.properties

5、srm_interface/webapps/els-interface-base/META-INF/context.xml

ip或域名

6、发布完成之后lib下面sap*开头的包删除，并将以下两个包替换上去

7、替换此class文件

目录：/webapps/els-interface-base/WEB-INF/classes/com/els/util/MailSend.class

启动后，通过nginx代理端口访问。

####interface接口平台

location ^~/els-interface-base/{

proxy_pass      http://<IP地址已脱敏>:9012/els-interface-base/;

proxy_redirect http:// https://;

proxy_set_header        X-Real-IP       $remote_addr;

proxy_set_header        Host            $host;

proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;

proxy_pass_request_headers      on;

}

访问地址

http://<IP地址已脱敏>/els-interface-base/login/login.html

默认账户：251000/1001/qqt

服务启动

可通过/etc/rc.d/rc.loca 查看自启命令

Nginx

systemctl start nginx.service    #启动

systemctl enable nginx.service   #开机自启动

MYSQL

systemctl  start mysqld    ##启动mysql

systemctl enable mysqld    ##加入开机自启动

REDIS

/etc/init.d/redis6379 start   #脚本启动

/home/app/srm_redis/bin/redis-server /home/app/srm_redis/redis.conf    #命令启动

MONGODB

/etc/init.d/mongodb start    #脚本启动

/home/app/srm_mongodb/mongod -f /home/app/srm_mongodb/mongodb.conf     #命令启动

Rocketmq

systemctl start docker.service

cd /home/app/docker-compose

docker-compose up -d

NFS

服务端

systemctl start rpcbind.service    #启动

systemctl enable rpcbind.service   #加入开机自启

客户端

systemctl start nfs    #启动

systemctl enable nfs   #加入开机自启

interface(tomcat)

cd /home/app/srm_interface/bin/

./catalina.sh start      #开始

cd /home/app/srm_interface/bin/

./shutdown.sh             #停止

SRM/im/report

#SRM

cd /home/app/srm_v5/

./app.sh start

#im

cd /home/app/srm_v5/im/

./service_manager.sh start

#report

cd/home/app/srm_v5/report/

./service_manager.sh start
