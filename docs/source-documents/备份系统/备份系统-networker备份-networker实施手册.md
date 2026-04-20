# networker实施手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [备份系统]
issue_types: [reference]
tags: [engineer-doc, imported, networker, backup]
source_path: "D:\新建文件夹\业务维护清单\备份系统\networker备份\networker实施手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：networker实施手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\备份系统\networker备份
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

2023.6

networker添加 6400设备

右键新建设备向导

选择Data Domain

添加DD，输入ddboost用户名和密码，选择存储单元（或者新建）

在存储单元下新建文件夹

创建新的池

输入DD里配置的字符串

确认信息

创建成功

备份测试

编辑networker自身服务器备份目标池

手动发起备份测试

备份成功

恢复测试

备份配置

配置VM备份

部署vproxy虚拟机

选择部署ovf，选择vproxy软件包

下一步

接受

命名

选择资源

选择存储

选择精简置备

选择网络

填写网络IP信息

完成

添加解析

在vproxy上添加networker，dd和vcenter的地址解析

在networker服务器上添加DD、vcenter、vproxy的解析

在networker界面里添加vcenter

添加hosts里的vcenter名称及用户名密码

在networker界面里添加vproxy

输入hosts里vproxy名称

选择vcenter，开启NBD，输入admin用户信息

看到版本信息创建成功

新建备份组

选择VMware备份类型，选择要备份的虚拟机

备份策略配置

添加policy

新建policy

添加workflow

添加workflow

添加action

选择保留周期和目标池

下一步

配置windows文件备份

备份服务器配置客户端hosts解析

vi /etc/hosts 添加客户端的解析

客户端配置服务器和DD的hosts解析

添加修改 C:\Windows\System32\drivers\etc\hosts 文件内容

安装备份软件

解压nw198_win_x64.zip

以管理员身份运行安装

先安装lgtoclnt-<IP地址已脱敏>.exe 再安装lgtoxtdclnt-<IP地址已脱敏>.exe

安装lgtoclnt-<IP地址已脱敏>.exe

一直下一步即可

安装lgtoxtdclnt-<IP地址已脱敏>.exe

添加客户端

用hostname去添加客户端

选择备份类型

下一步

选择要备份的文件或目录

配置信息

完成

备份策略配置

添加policy

添加workflow

设置启动时间和自动运行

添加关联组

选择之前创建的客户端

添加action

设置备份策略，FULL（全量）、incr（增量）、Cumulative incr（累积增量）

选择目标池和保留周期

信息摘要

配置Ubuntu系统文件备份

备份服务器添加客户端的hosts解析

客户端添加备份服务器和DD的hosts解析

安装备份软件

登录到root用户：sudo su -

tar -zxvf nw198_linux_x86_64.tar.gz 解压安装包

cd linux_86_64

安装软件

sudo dpkg -i lgtoclnt_<IP地址已脱敏>_amd64.deb lgtoxtdclnt_<IP地址已脱敏>_amd64.deb

启动服务

/opt/nsr/admin/networker.sh start

检查服务

ps -ef|grep nsr

添加客户端

用hostname去添加客户端

选择备份类型

下一步

选择要备份的文件或目录

配置信息摘要

完成

备份策略配置

添加policy

添加workflow

设置启动时间和自动运行

添加关联组

选择之前创建的客户端

添加action

设置备份策略，FULL（全量）、incr（增量）、Cumulative incr（累积增量）

选择目标池和保留周期

信息摘要

配置Linux系统文件备份

备份服务器添加客户端的hosts解析

客户端添加备份服务器和DD的hosts解析

安装备份软件

tar -zxvf nw198_linux_x86_64.tar.gz 解压安装包

cd linux_86_64

安装软件

rpm -ivh lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm

启动服务

/opt/nsr/admin/networker.sh start

检查服务

ps -ef|grep nsr

添加客户端

用hostname去添加客户端

选择备份类型

下一步

选择要备份的文件或目录

配置信息摘要

完成

备份策略配置

添加policy

添加workflow

设置启动时间和自动运行

添加关联组

选择之前创建的客户端

添加action

设置备份策略，FULL（全量）、incr（增量）、Cumulative incr（累积增量）

选择目标池和保留周期

信息摘要

配置Linux系统oracle备份

开启归档模式

备份服务器添加客户端的hosts解析

客户端添加备份服务器和DD的hosts解析

安装备份软件

tar -zxvf nw198_linux_x86_64.tar.gz 解压安装包

cd linux_86_64

安装软件

rpm -ivh lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm

启动服务

/opt/nsr/admin/networker.sh start

检查服务

ps -ef|grep nsr

安装nmda模块

yum install -y lgtonmda-<IP地址已脱敏>-1.x86_64.rpm

做软链接

以Oracle用户登录，在ORACLE_HOME的lib目录下检查：libobk.so是否指向/usr/lib/libnsrora.so

如果不存在，或者指向不对，需要在ORACLE_HOME的lib目录下重新执行链接命令：

ln –s /usr/lib/libnsrora.so  libobk.so

添加客户端

全量备份配置

用hostname去添加客户端

选择备份类型

下一步

自定义备份配置

下一步

选择ORACLE_HOME，TNS_ADMIN目录，数据库用户，ORACLE实例的SID

选择数据库备份

选择数据库

自定义备份

下一步

自定义备份日志

备份脚本查看（也可自定义）

自定义备份脚本

RUN {

ALLOCATE CHANNEL CH1 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH2 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH3 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH4 TYPE 'SBT_TAPE';

BACKUP

INCREMENTAL  LEVEL 0

filesperset 1

FORMAT 'full_%d_%U'

DATABASE

INCLUDE CURRENT CONTROLFILE;

BACKUP

not backed up 1 times

FORMAT 'arch_%d_%U'

ARCHIVELOG ALL  delete input;

BACKUP

FORMAT 'cntrl_%U'

CURRENT CONTROLFILE;

RELEASE CHANNEL CH1;

RELEASE CHANNEL CH2;

RELEASE CHANNEL CH3;

RELEASE CHANNEL CH4;

}

RUN {

ALLOCATE CHANNEL CH1 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH2 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH3 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH4 TYPE 'SBT_TAPE';

BACKUP

FULL

FORMAT '%d_%U'

DATABASE

INCLUDE CURRENT CONTROLFILE

PLUS ARCHIVELOG

;

DELETE

ARCHIVELOG UNTIL TIME "SYSDATE-14"

BACKED UP 1 TIMES TO DEVICE TYPE

sbt;

BACKUP

FORMAT 'cntrl_%U'

CURRENT CONTROLFILE;

RELEASE CHANNEL CH1;

RELEASE CHANNEL CH2;

RELEASE CHANNEL CH3;

RELEASE CHANNEL CH4;

}

下一步

配置信息摘要

完成

增量备份配置

用hostname去添加客户端

选择备份类型

下一步

自定义备份配置

下一步

选择ORACLE_HOME，TNS_ADMIN目录，数据库用户，ORACLE实例的SID

选择数据库备份

选择数据库

自定义备份（选择增量备份，level 1）

下一步

自定义备份日志

备份脚本查看（也可自定义）

自定义备份脚本

RUN {

ALLOCATE CHANNEL CH1 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH2 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH3 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH4 TYPE 'SBT_TAPE';

BACKUP

INCREMENTAL  LEVEL 1

filesperset 1

FORMAT 'incr_%d_%U'

DATABASE

INCLUDE CURRENT CONTROLFILE;

BACKUP

not backed up 1 times

FORMAT 'arch_%d_%U'

ARCHIVELOG ALL  delete input;

BACKUP

FORMAT 'cntrl_%U'

CURRENT CONTROLFILE;

RELEASE CHANNEL CH1;

RELEASE CHANNEL CH2;

RELEASE CHANNEL CH3;

RELEASE CHANNEL CH4;

}

下一步

配置信息摘要

完成

日志备份配置

用hostname去添加客户端

选择备份类型

下一步

自定义备份配置

下一步

选择ORACLE_HOME，TNS_ADMIN目录，数据库用户，ORACLE实例的SID

选择日志备份

自定义备份日志

下一步

备份脚本查看（也可自定义）

自定义备份脚本

RUN {

ALLOCATE CHANNEL CH1 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH2 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH3 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL CH4 TYPE 'SBT_TAPE';

BACKUP

not backed up 1 times

FORMAT 'arch_%d_%U'

ARCHIVELOG ALL  delete input;

BACKUP

FORMAT 'cntrl_%U'

CURRENT CONTROLFILE;

RELEASE CHANNEL CH1;

RELEASE CHANNEL CH2;

RELEASE CHANNEL CH3;

RELEASE CHANNEL CH4;

}

下一步

配置信息摘要

完成

备份策略配置

添加policy

添加workflow

全量、增量、日志各对应一个workflow

设置启动时间和自动运行

添加关联组

选择之前创建的客户端

添加action

设置备份策略，FULL（全量）、incr（增量）、Cumulative incr（累积增量）

Oracle备份选FULL或者跳过即可、日志备份选FULL即可，例如：周日全备其他时间增备

两个workflow：1，选择全备客户端，周日FULL，其他skip

2，选择增备客户端，周日skip，其他FULL

选择目标池和保留周期

信息摘要

配置sqlserver备份

备份服务器配置客户端hosts解析

vi /etc/hosts 添加客户端的解析

客户端配置服务器和DD的hosts解析

添加修改 C:\Windows\System32\drivers\etc\hosts 文件内容

安装备份软件

解压nw198_win_x64.zip和nmm198_win_x64.zip

以管理员身份运行安装

先安装lgtoclnt-<IP地址已脱敏>.exe 再安装lgtoxtdclnt-<IP地址已脱敏>.exe 最后安装NWVSS.exe

安装lgtoclnt-<IP地址已脱敏>.exe

一直下一步即可

安装lgtoxtdclnt-<IP地址已脱敏>.exe

安装nmm

管理员身份运行NWVSS.exe(SQL数据库插件)

一直下一步安装即可

\

添加客户端

用hostname去添加客户端

选择备份类型

下一步

选择要备份的数据库

输入操作系统用户名和密码

默认配置

配置摘要

完成

备份策略配置

添加policy

添加workflow

设置启动时间和自动运行

添加关联组

选择之前创建的客户端

添加action

设置备份策略

sqlserver 周日全量其他增量则设置周日为Full 其他为Cumulative incr

日志备份则设置为Logs Only

周日全量其他增量如下图

日志备份如下图

选择目标池和保留周期

信息摘要

配置windows下Oracle备份

Oracle需要开启归档模式

SQL>  archive log list;

SQL>  shutdown immediate;

SQL>  startup mount;

SQL>  alter database archivelog;

SQL>  alter system set log_archive_dest_1=’LOCATION=/data/arch’ scope=both; ##路径自定义

SQL>  alter database open;

SQL>  alter system switch logfile;    ###手工产生日志文件

创建Oracle备份用户并授权

create user backup identified by backup;

grant sysbackup to backup;

grant create session to backup;

备份服务器配置客户端hosts解析

vi /etc/hosts 添加客户端的解析

客户端配置服务器和DD的hosts解析

添加修改 C:\Windows\System32\drivers\etc\hosts 文件内容

安装备份软件

解压nw198_win_x64.zip和nmda198_win_x64.zip

以管理员身份运行安装

先安装lgtoclnt-<IP地址已脱敏>.exe 再安装lgtoxtdclnt-<IP地址已脱敏>.exe 最后安装NMDA.exe

安装lgtoclnt-<IP地址已脱敏>.exe

一直下一步即可

安装lgtoxtdclnt-<IP地址已脱敏>.exe

安装NMDA.exe

管理员身份运行NMDA.exe(数据库插件)

一直下一步安装即可

拷贝相应配置文件到指定目录

拷贝C:\Program Files\EMC NetWorker\nsr\bin\orasbt.dll和C:\Program Files\EMC NetWorker\nsr\bin\nsrsbtcn.exe文件到C:\Windows\System32下，并重启服务器操作系统

添加客户端

可参考linux的oracle添加客户端

用hostname去添加客户端

选择备份类型

下一步

自定义备份

下一步

选择ORACLE_HOME，TNS_ADMIN目录，数据库用户，ORACLE实例的SID

选择数据库备份

选择数据库

自定义备份

下一步

自定义备份日志

备份脚本查看（也可自定义）

下一步

配置信息摘要

完成

备份策略配置

添加policy

添加workflow

全量、增量、日志各对应一个workflow

设置启动时间和自动运行

添加关联组

选择之前创建的客户端

添加action

设置备份策略，FULL（全量）、incr（增量）、Cumulative incr（累积增量）

Oracle备份选FULL或者跳过即可、日志备份选FULL即可，例如：周日全备其他时间增备

两个workflow：1，选择全备客户端，周日FULL，其他skip

2，选择增备客户端，周日skil，其他FULL

选择目标池和保留周期

信息摘要

恢复验证

虚拟机恢复（12克隆_restore恢复测试）

点击Recover界面，右键New Recover

选择虚拟机恢复，选择源vcenter

选择要恢复的虚拟机

选择哪次备份

选择恢复类型（选择创建新的虚拟机）

配置恢复的虚拟机

选择从哪个备份存储设备上进行恢复

为此次恢复任务命名

查看恢复进度

虚拟机恢复（QMS恢复测试）

点击Recover界面，右键New Recover

选择虚拟机恢复，选择源vcenter

选择要恢复的虚拟机

选择哪次备份

选择恢复类型为创建新的虚拟机

配置恢复的虚拟机

选择从哪个备份存储设备上进行恢复

为此次恢复任务命名

查看恢复进度

文件恢复（EAM30）

点击Recover界面，右键New Recover

选择传统客户端恢复

选择源端和目标端

选择要恢复的时间和目录

选择要恢复的目标目录

下一步

为恢复任务命名

恢复完成

检查/home/user/recover20230613目录

文件异机恢复（PORTAL）

备份服务器配置目标客户端hosts解析

vi /etc/hosts 添加客户端的解析

目标客户端配置服务器和DD以及源机的hosts解析

添加修改 C:\Windows\System32\drivers\etc\hosts 文件内容

安装备份软件

解压nw198_win_x64.zip

以管理员身份运行安装

先安装lgtoclnt-<IP地址已脱敏>.exe 再安装lgtoxtdclnt-<IP地址已脱敏>.exe

安装lgtoclnt-<IP地址已脱敏>.exe

一直下一步即可

安装lgtoxtdclnt-<IP地址已脱敏>.exe

添加客户端

恢复目标机只要成功添加上客户端即可

用hostname去添加客户端

选择备份类型

下一步

选择要备份的文件或目录（随便选即可）

配置信息

完成

在源机客户端上添加远程访问

在源机客户端remote access 属性里添加*@*

开始恢复

点击Recover界面，右键New Recover

选择传统客户端恢复

选择源端和目标端

选择要恢复的时间和目录

选择要恢复的目标目录

路径不存在则会自动创建

下一步

为恢复任务命名

恢复完成

sqlserver恢复（PM系统）

运行恢复向导

配置恢复的数据库信息

重定向数据文件和日志文件目录

开始运行

确定

确定

正在恢复

恢复成功

Oracle恢复（PLM系统）

恢复前准备

备份服务器配置客户端hosts解析

vi /etc/hosts 添加客户端的解析

客户端配置服务器和DD以及源机的hosts解析

添加修改 C:\Windows\System32\drivers\etc\hosts 文件内容

安装备份软件

解压nw198_win_x64.zip和nmda198_win_x64.zip

以管理员身份运行安装

先安装lgtoclnt-<IP地址已脱敏>.exe 再安装lgtoxtdclnt-<IP地址已脱敏>.exe 最后安装NMDA.exe

安装lgtoclnt-<IP地址已脱敏>.exe

一直下一步即可

安装lgtoxtdclnt-<IP地址已脱敏>.exe

安装NMDA.exe

管理员身份运行NMDA.exe(数据库插件)

一直下一步安装即可

拷贝相应配置文件到指定目录

拷贝C:\Program Files\EMC NetWorker\nsr\bin\orasbt.dll和C:\Program Files\EMC NetWorker\nsr\bin\nsrsbtcn.exe文件到C:\Windows\System32下，并重启服务器操作系统

添加客户端

添加客户端

用hostname去添加客户端

选择备份类型

下一步

选择要备份的文件或目录(随便选即可，不做备份)

配置信息

完成

在源机客户端上添加远程访问

在源机客户端remote access 属性里添加*@*

开始恢复

查询备份记录

在备份服务器上查询控制文件备份记录，获取备份文件名及备份时间点(根据hostname查询备份记录)

mminfo -avr 'savetime(20),client,name' -q client=WINDOWS-A46CCHR -ot|grep cntrl

选择要恢复时间点往后最近的控制文件；假如要恢复到2023-06-14 16:00

选择控制文件cntrl_191umrgo_1_1

PLM_tn25l5ti_1_1

恢复控制文件

切换数据库到nomount模式；

sqlplus  / as sysdba

shutdown immediate;

startup nomount;

select instance_name from v$instance;

进入rman恢复控制文件

rman target /

修改备份服务器名称，源机名称，控制文件备份集

run{

ALLOCATE CHANNEL ch01 TYPE 'SBT_TAPE';

send 'NSR_ENV=(NSR_SERVER=nmc,NSR_CLIENT=plmdb1)';

restore controlfile from 'PLM_tn25l5ti_1_1';

RELEASE CHANNEL ch01;

}

恢复数据文件

将数据库启动至mount状态

alter database mount；

进入rman，恢复数据文件

使用et newname for database to 'D:\ptc_ocu\Windchill_11.0\ocu\oradata\wind\%U';重新定义数据文件名称路径

run{

set newname for database to 'D:\ptc_ocu\Windchill_11.0\ocu\oradata\wind\%U';

ALLOCATE CHANNEL ch01 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch02 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch03 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch04 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch05 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch06 TYPE 'SBT_TAPE';

send 'NSR_ENV=(NSR_SERVER=nmc,NSR_CLIENT=plmdb1)';

restore database until time "to_date('2023-06-14 02:00:00','YYYY-MM-DD HH24:MI:SS')";

switch datafile all;

RELEASE CHANNEL ch01;

RELEASE CHANNEL ch02;

RELEASE CHANNEL ch03;

RELEASE CHANNEL ch04;

RELEASE CHANNEL ch05;

RELEASE CHANNEL ch06;

}

run{

set newname for database to '/WH_data/oradata/plm/%U';

ALLOCATE CHANNEL ch01 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch02 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch03 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch04 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch05 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch06 TYPE 'SBT_TAPE';

send 'NSR_ENV=(NSR_SERVER=nmc,NSR_CLIENT=plmdb1,DDBOOST_COMPRESSED_RESTORE=TRUE#压缩恢复参数)';

restore database;

switch datafile all;

RELEASE CHANNEL ch01;

RELEASE CHANNEL ch02;

RELEASE CHANNEL ch03;

RELEASE CHANNEL ch04;

RELEASE CHANNEL ch05;

RELEASE CHANNEL ch06;

}

执行完成

使用归档日志对数据库进行recover

使用命令对数据库进行recover

run{

ALLOCATE CHANNEL ch01 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch02 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch03 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch04 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch05 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch06 TYPE 'SBT_TAPE';

send 'NSR_ENV=(NSR_SERVER=xa-networker,NSR_CLIENT=WINDOWS-A46CCHR)';

recover database until time "to_date('2023-06-14 16:00:00','YYYY-MM-DD HH24:MI:SS')";

RELEASE CHANNEL ch01;

RELEASE CHANNEL ch02;

RELEASE CHANNEL ch03;

RELEASE CHANNEL ch04;

RELEASE CHANNEL ch05;

RELEASE CHANNEL ch06;

run{

set  until time "to_date('2023-09-06 00:09:00','YYYY-MM-DD HH24:MI:SS')";

ALLOCATE CHANNEL ch01 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch02 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch03 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch04 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch05 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL ch06 TYPE 'SBT_TAPE';

send 'NSR_ENV=(NSR_SERVER=nmc,NSR_CLIENT=plmdb1)';

recover database;

RELEASE CHANNEL ch01;

RELEASE CHANNEL ch02;

RELEASE CHANNEL ch03;

RELEASE CHANNEL ch04;

RELEASE CHANNEL ch05;

RELEASE CHANNEL ch06;

}

}

重新定义日志文件位置

查询redolog文件位置（查的是备份的路径）

在恢复机上新建路径目录 或者   重定向redolog

alter  database rename file 'E:\PTC\WINDCHILL_11.0\OCU\ORADATA\WIND\WINDREDO01.log' to 'D:\ptc_ocu\Windchill_11.0\ocu\oradata\wind\WINDREDO01.log'

alter database rename file 'E:\PTC\WINDCHILL_11.0\OCU\ORADATA\WIND\WINDREDO01.log' to 'D:\ptc_ocu\Windchill_11.0\ocu\oradata\wind\WINDREDO01.log'

alter database rename file 'E:\PTC\WINDCHILL_11.0\OCU\ORADATA\WIND\WINDREDO02.log' to 'D:\ptc_ocu\Windchill_11.0\ocu\oradata\wind\WINDREDO02.log'

alter database rename file 'E:\PTC\WINDCHILL_11.0\OCU\ORADATA\WIND\WINDREDO03.log' to 'D:\ptc_ocu\Windchill_11.0\ocu\oradata\wind\WINDREDO03.log'

使用select group#,member from v$logfile;确认日志文件已重新定义

启动数据库

使用alter database open resetlogs命令启动数据库

至此数据库所有恢复操作结束
