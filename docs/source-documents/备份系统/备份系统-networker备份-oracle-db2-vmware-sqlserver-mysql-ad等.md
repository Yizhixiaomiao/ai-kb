# Oracle、DB2、vmware、sqlserver、mysql、ad等

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [备份系统]
issue_types: [reference]
tags: [engineer-doc, imported, ad, networker, backup, mysql, oracle]
source_path: "D:\新建文件夹\业务维护清单\备份系统\networker备份\Oracle、DB2、vmware、sqlserver、mysql、ad等.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：Oracle、DB2、vmware、sqlserver、mysql、ad等.docx
- 原始路径：D:\新建文件夹\业务维护清单\备份系统\networker备份
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

EMC Corporation Technical Solution GroupEMC Corporation Technical Solution Group

集中备份系统实施文档

| 送交： | 提供者： |

文档版本信息

| 版本信息 | 日期 | 文档作者 | 文档描述 |

networker软件安装

Linux服务器安装

需要加本机的地址解析

安装networker server：

[root@nwserver emcsoft]# tar zxvf nw182_linux_x86_64.tar.gz

[root@nwserver linux_x86_64]# rpm -ivh lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm lgtonode-<IP地址已脱敏>-1.x86_64.rpm lgtoserv-<IP地址已脱敏>-1.x86_64.rpm lgtoauthc-<IP地址已脱敏>-1.x86_64.rpm lgtoman-<IP地址已脱敏>-1.x86_64.rpm

配置networker默认用户名及密码=<已脱敏>

[root@nwserver linux_x86_64]# /opt/nsr/authc-server/scripts/authc_configure.sh

启动networker服务：

[root@nwserver linux_x86_64]# /opt/nsr/admin/networker.sh start

安装networker控制台软件：

[root@nwserver linux_x86_64]# rpm -ivh lgtonmc-<IP地址已脱敏>-1.x86_64.rpm

配置networker控制台：

[root@nwserver linux_x86_64]# /opt/lgtonmc/bin/nmc_config

然后打开浏览器，输入http://备份服务器IP：9000

输入networker服务器主机名

至此networker server配置完成。

Windows服务器安装

安装networker server

配置NMC：

Linux客户端安装

首先在备份服务和客户机中加入对方的主机名解析，或用DNS解释

在linux系统中安装networker需用一些依赖软件包，如果系统没有安装可以通过yum源来安装：

Linux客户端需要安装下面两个软件包

lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm和lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm

可以先在本地解压nw91_linux_x86_64.tar.gz，然后只上传上面两个文件到linux

[root@app02 emcsoft]# cd linux_x86_64/

# rpm -ivh lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm

或yum localinstall --nogpgcheck lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm

第一次安装后需要手动启动networker服务：

[root@db01 emcsoft]# /etc/init.d/networker start

或systemctl start networker

键入以下命令以确定是否启动了 NetWorker 服务：

#ps -ef | grep nsr

如果有数据库要备份，要安装NMDA模块(需要配置本地yum源)

# rpm –ivh lgtonmda-<IP地址已脱敏>-1.x86_64.rpm

Windows客户端安装

首先在备份服务和客户机中加入对方的主机名解析，或用DNS解释

如果是windows2008以上系统，需要运行Certmgr.msc导入证书，才能安装networker软件

2 备份客户机以管理员权限安装Networker客户端软件（先装lgtoclnt*，再装lgtoxtdclnt*），默认安装即可

如果有微软数据库，要安装NMM模块，默认安装即可

如果有非微软数据库，要安装NMDA模块，默认安装即可

Aix客户端的安装

首先在备份服务和客户机中加入对方的主机名解析，或用DNS解释

解压软件

#gunzip nw18.2_aixpower.tar.gz

#tar –xvf nw18.2_aixpower.tar

#cd /software/aixpower

安装软件

#installp –a –d /software/aixpower  LGTonw.clnt.rte

#installp –a –d /software/aixpower  LGTonw.xtdclnt.rte

或用#smit install

检查安装情况：

# lslpp -l |grep -i lgto

第一次安装后需要手动启动networker服务

#/etc/rc.nsr（起备份服务）

键入以下命令以确定是否启动了 NetWorker 服务：

#ps -ef | grep nsr

如果要停止networker服务，使用下面命令：

#/etc/rc.nsr stop

或#nsr_shutdown

如果有数据库要备份，要安装NMDA模块

# gunzip nmda182_aixpower_64.tar.gz

# tar xvf nmda182_aixpower_64.tar

# installp -a -d /dir_pathname LGTOnmda.rte

检查网络连通性

下面命令可以检查备份服务器与客户端之间的网络连通性

分别在备份服务器和客户机运行命令：nsrrpcinfo -p 对端主机名

DD6800安装

DD6800上架并做初始化。

使用向导做基础配置，配置IP等信息。

在DD上配置Ddboost

点create创建ddboost用户

输入用户名及密码

1.启用ddboost service

把前面创建的用户添加进来

在DD上配置VTL

打开DD的网页管理界面，然后进行如下配置

创建VTL Library

点击“VTL Service”下的“Libraries”，在右边框中点击“create”：

输入虚拟带库信息，如库名，驱动器数量，驱动器类型，槽位，机械手类型,Options默认不用改：

点击“OK”，完成虚拟带库的创建。

创建磁带并导入Library

首先创建用于存放磁带的存储池，点击More Taks下的Create Pool，如下图所示：

弹出创建存储池的窗口，输入Pool的名字：

在存储池中创建磁带，高亮选中存储池，然后点击Create Tapes

弹出磁带创建窗口，输入：

接下来需要导入磁带到对应的Library中，高亮选中被导入磁带的Library，然后点击import from Vault

点OK

设置VTL与主机连接

将DD6800的光纤口与需要连接主机的光纤口使用光纤线连接，做完zoning之后，DD的Physical Resourse上可以看到对应主机光纤口的WWPN号

为WWPN取个容易识别的别名

创建组配置VTL访问控制

创建访问控制，把VTL映射给主机：

点击“access group”，创建group：

在出现的“Group Name”中输入名称，然后勾选对应的主机initiator

弹出窗口中点击绿色的加号

选择驱动器及机械手，再选择使用的主端口及备选端口

选择完如下

点击下一步，确认配置，然后完成配置

分配好设备，就可以在主机上扫描设备了

networker配置备份设备

配置ddboost设备

在备份服务器上配置DDBOOST步骤如下：

在Data Domain System右键，选择添加“New Device wizard”，

然后输入DD的主机名及用户名、密码

点“New Folder”，新建一个文件夹。

选择建立的文件夹的名称，并点击“下一步”，进行设备介质池的配置。

选择“池类型”，如果这个pool用于备份就选择Backup，如果这个pool用于clone就选择Backup Clone，并输入一个新的池名，将介质标签到该池中；

创建设备后进行标记和装载：设备创建完成后，自动进行DDBoost设备中的介质的标签和加载到该驱动器中。

点否

点next

至此EMC Networker上创建DDBoost设备已经完成。

配置VTL设备

在下面存储节点点右键

输入存储节点的主机名：

点这 台存储节点右键，选san for all device 开始扫描设备。

点start scan

然后就可以在上面的带库中看到相对的带库了，此时带库因还没配置是红色的，然后再选配置带库

右键带库然后选重新配置带库，选中全部的主机，点start configuration

配置后，对磁带做label，指定到相应的pool，然后就可以用了

配置物理带库设备

配置前，首先要在系统上识别到带库设备，windows在设备管理器查看，linux用inquire命令查看

点这台存储节点右键，选san for all device 开始扫描设备。

点启动扫描

然后就可以在上面的带库中看到相对的带库了，此时带库因还没配置是红色的，然后再选配置带库

右键带库然后选重新配置带库，选中全部的主机，点start configuration

配置后，对磁带做label，指定到相应的pool，然后就可以用了

networker配置备份策略

创建client注意

加域的主机要用长名去创建networker client，没加域的主机用短名创建networker client，如果主机上一个IP对应多个别名，需要把这些别名都加到networker client的别名列表中

配置文件备份

安装networekr软件

参考前面章节

配置file备份策略

1、创建client

输入客户机的主机名

选择备份目录

以上完成客户端的创建，如果客户端有加域，还要做如下操作：

打开客户端属性，在Globals(1 of 2)里，确认添加有该客户机的长名

2、创建group，把上一步创建的client加进来

3、创建备份策略

点创建workflow，

输入name，并选择上面创建的group，并在actions点击add

输入action name和选择action type

选择目标池

点OK

备份策略创建完如下，然后就可以备份该策略了

File恢复

点新建

在name里选择要恢复哪台机器的数据，目标主机里可以选择恢复到源机或异机

选择要恢复的文件

选择恢复目录，可以在源路径或其它路径

默认，点下一步

Recovery name里随便输入一个名称，点开始恢复

配置Oracle备份与恢复

确认oracle处于归档日志模式

首先要确认oracle处于归档日志模式（如下面表示oracle没开启归档模式，做不了RMAN备份）

[root@oajavatest ~]# su - oracle

[oracle@oajavatest ~]$ sqlplus / as sysdba

SQL> archive log list

Database log mode              No Archive Mode

Automatic archival             Disabled

Archive destination            USE_DB_RECOVERY_FILE_DEST

Oldest online log sequence     10888

Current log sequence           10890

SQL>

安装networker软件

前提是安装了networker客户端软件，并启动networker服务，然后再安装下面的oracle模块软件。

AIx安装NMDA数据库模块：

# gunzip nmda182_aixpower_64.tar.gz

# tar xvf nmda182_aixpower_64.tar

# installp -a -d /dir_pathname LGTOnmda.rte

linux安装NMDA数据库模块：

# tar zxvf nmda182_linux_x86_64.tar.gz

# rpm -ivh lgtonmda-<IP地址已脱敏>-1.x86_64.rpm

安装完networker for oracle代理模块后要做库连接，命令如下：

(以下为各种类型的系统安装NMDA模块后的link方法)

例如Linux平台：

# su - oracle

$ cd $ORACLE_HOME/lib

$ ln -s /usr/lib/libnsrora.so libobk.so

配置oracle备份策略

1、首先创建client，点击新建

备份集：

Linux：RMAN:/nsr/apps/config/eamdb_full.sh

备份命令:

Linux：nsrdasv -z /nsr/apps/config/eamdb_full.cfg

/nsr/apps/config/eamdb_full.cfg文件内容如下

（建议复制一份/nsr/apps/config/nmda_oracle.cfg，然后编辑该文件，改下面4个参数）

linux样例：

ORACLE_HOME = /u01/db/oracle/<IP地址已脱敏>/db

ORACLE_SID = eamdb

ORACLE_USER =oracle

NSR_RMAN_ARGUMENTS = "nocatalog msglog '/nsr/applogs/eamdb_full.log' append"

eamdb_full.sh备份脚本内容如下（只需要修改NSR_CLIENT为实际的客户机名字）

connect target /;

CONFIGURE CONTROLFILE AUTOBACKUP ON;

run {

ALLOCATE CHANNEL c1 TYPE 'SBT_TAPE';

ALLOCATE CHANNEL c2 TYPE 'SBT_TAPE';

Send 'NSR_ENV=(NSR_CLIENT=VMPRDEAMAPPDATA)';

BACKUP

INCREMENTAL LEVEL=0

filesperset 1

FORMAT 'db_%s_%U_%T'

DATABASE;

sql 'alter system archive log current';

BACKUP

SKIP INACCESSIBLE

filesperset 20

format 'arch_%s_%U_%T'

archivelog all delete input;

#   archivelog ALL not backed up 1 times;

#   delete noprompt archivelog until time 'sysdate-1';

BACKUP

format 'cntrl_%s_%U_%T'

current controlfile;

RELEASE CHANNEL c1;

RELEASE CHANNEL c2;

}

2、创建group，把上一步创建的client加进来

3、创建备份策略

创建workflow，并在actions点击add

输入action name和选择action type

选择目标池

备份策略创建完如下，然后就可以备份该策略了

本机恢复

本恢复测试场景是删掉一个datafile，然后恢复这个datafile

1、删掉datafile文件hlb2.dbf

gz-ted01#[/oradata/testing/apps]ll

total 9294368

-rw-rw----   1 oracle     dba        1612931072 Aug 31 14:30 feras.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 13:51 hlb.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 14:30 hlb2.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 13:32 hlb_bak.dbf

gz-ted01#[/oradata/testing/apps]mv hlb2.dbf hlb2_bak.dbf

gz-ted01#[/oradata/testing/apps]ll

total 9294368

-rw-rw----   1 oracle     dba        1612931072 Aug 31 14:30 feras.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 13:51 hlb.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 14:55 hlb2_bak.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 13:32 hlb_bak.dbf

2、检查是否能查询到表

SQL>  select * from sys.testnw2;

select * from sys.testnw2

*

ERROR at line 1:

ORA-00376: file 59 cannot be read at this time

ORA-01110: data file 59: '/oradata/testing/apps/hlb2.dbf'

SQL>

3、开始RMAN恢复datafile

connect target /;

RMAN> run {

2> allocate channel t1 type 'SBT_TAPE';

3> send 'NSR_ENV=(NSR_SERVER=GZ-NKR01.gameco.com.cn,NSR_CLIENT=gz-ted01)';

4> restore datafile 59;

5> recover datafile 59;

6> release channel t1;

7> }

allocated channel: t1

channel t1: sid=542 devtype=SBT_TAPE

channel t1: NMDA Oracle v<IP地址已脱敏>

sent command to channel: t1

Starting restore at 31-AUG-18

channel t1: starting datafile backupset restore

channel t1: specifying datafile(s) to restore from backup set

restoring datafile 00059 to /oradata/testing/apps/hlb2.dbf

channel t1: reading from backup piece db_40809_r9tbuk5o_1_1_20180831

channel t1: restored backup piece 1

piece handle=db_40809_r9tbuk5o_1_1_20180831 tag=TAG20180831T141242

channel t1: restore complete, elapsed time: 00:00:25

Finished restore at 31-AUG-18

Starting recover at 31-AUG-18

starting media recovery

media recovery complete, elapsed time: 00:00:03

Finished recover at 31-AUG-18

released channel: t1

RMAN> exit

Recovery Manager complete.

$

4、检查hlb2.dbf是否恢复回来

gz-ted01#[/oradata/testing/apps]ll

total 11342400

-rw-rw----   1 oracle     dba        1612931072 Aug 31 14:30 feras.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 13:51 hlb.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 14:56 hlb2.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 14:55 hlb2_bak.dbf

-rw-r-----   1 oracle     dba        1048584192 Aug 31 13:32 hlb_bak.dbf

5、联机datafile文件

SQL> alter database datafile 59 online;

Database altered.

6、检查是否能查询到表

SQL> select * from sys.testnw2;

A

----------

1

SQL>

异机恢复

1、测试环境准备

要求恢复机器和原机相同的OS和DB版本，并且有足够的存储空间用于恢复

恢复前确认原生产机的数据，等一下恢复完验证恢复是否成功

在恢复目标机器上hosts加上备份服务器、DD、本机、源机主机名解释

在恢复目标机器上安装networker客户机软件和NMDA软件，并在NMC为恢复目标机器创建一个client

只在name输入恢复机器名称bfhfyl就行，其他不用填，点确定

查看源机orace 的DBID，并记下来

在NMC检查备份历史记录，找出最新的控制文件，如下面红框所示

2、恢复数据

建议在恢复测试机上新建一个与原机一样的数据库，然后把数据库shutdown，然后开始恢复oracle控制文件和数据文件

如果不新建这个数据库，就要手动新建一个pfile（最简单就是从原机复制一个过来，也可以从备份中恢复pfile文件，但步骤比较麻烦），然后用这个pfile去启动数据库，还要手动创建pfile中指定的相关目录以及数据库文件存放的目录

p750rRST:/dbdata/oradata/prodres$mkdir archive

p750rRST:/dbdata/oradata$mkdir adump

p750rRST:/dbdata/oradata$mkdir bdump

p750rRST:/dbdata/oradata$mkdir cdump

p750rRST:/dbdata/oradata$mkdir udump

下面恢复控制文件

$ rman target /

Recovery Manager: Release <IP地址已脱敏>.0 - Production on Tue Oct 30 16:26:27 2018

Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

connected to target database (not started)

RMAN> startup nomount pfile=/oracle/product/<IP地址已脱敏>/dbs/initprod.ora

Oracle instance started

Total System Global Area    4175568896 bytes

Fixed Size                     2212144 bytes

Variable Size               1023413968 bytes

Database Buffers            3137339392 bytes

Redo Buffers                  12603392 bytes

RMAN> set dbid 401112483

executing command: SET DBID

RMAN> run {

allocate channel t1 type 'sbt_tape';

send channel t1 'NSR_ENV=(NSR_SERVER=vmprdnetworker, NSR_CLIENT=YSX8)';

restore controlfile from 'c-401112483-20190220-02';

release channel t1;

}

控制文件恢复完成后，把数据库启动到mount状态

RMAN> alter database mount;

database mounted

RMAN>

然后恢复数据库文件

RMAN> run {

SET ARCHIVELOG DESTINATION TO '/dbdata/oradata/prodres/archive';

allocate channel t1 type 'SBT_TAPE';

allocate channel t2 type 'SBT_TAPE';

allocate channel t3 type 'SBT_TAPE';

send 'NSR_ENV=(NSR_SERVER=vmprdnetworker, NSR_CLIENT=YSX8)';

set newname for datafile 1   to '/dbdata/oradata/prodres/system01.dbf';

set newname for datafile 2   to '/dbdata/oradata/prodres/system02.dbf';

set newname for datafile 3   to '/dbdata/oradata/prodres/system03.dbf';

set newname for datafile 4   to '/dbdata/oradata/prodres/system04.dbf';

set newname for datafile 5   to '/dbdata/oradata/prodres/system05.dbf';

set newname for datafile 6   to '/dbdata/oradata/prodres/system06.dbf';

set newname for datafile 7   to '/dbdata/oradata/prodres/system07.dbf';

set newname for datafile 8   to '/dbdata/oradata/prodres/system08.dbf';

set newname for datafile 9   to '/dbdata/oradata/prodres/system09.dbf';

set newname for datafile 10  to '/dbdata/oradata/prodres/system10.dbf';

set newname for datafile 11  to '/dbdata/oradata/prodres/system11.dbf';

set newname for datafile 12  to '/dbdata/oradata/prodres/undo01.dbf';

set newname for datafile 13  to '/dbdata/oradata/prodres/a_archive01.dbf';

set newname for datafile 14  to '/dbdata/oradata/prodres/a_int01.dbf';

set newname for datafile 15  to '/dbdata/oradata/prodres/a_media01.dbf';

set newname for datafile 16  to '/dbdata/oradata/prodres/a_nolog01.dbf';

set newname for datafile 17  to '/dbdata/oradata/prodres/a_queue01.dbf';

set newname for datafile 18  to '/dbdata/oradata/prodres/a_queue02.dbf';

set newname for datafile 19  to '/dbdata/oradata/prodres/a_ref01.dbf';

set newname for datafile 20  to '/dbdata/oradata/prodres/a_ref02.dbf';

set newname for datafile 21  to '/dbdata/oradata/prodres/a_summ01.dbf';

set newname for datafile 22  to '/dbdata/oradata/prodres/a_txn_data01.dbf';

set newname for datafile 23  to '/dbdata/oradata/prodres/a_txn_data02.dbf';

set newname for datafile 24  to '/dbdata/oradata/prodres/a_txn_data03.dbf';

set newname for datafile 25  to '/dbdata/oradata/prodres/a_txn_ind01.dbf';

set newname for datafile 26  to '/dbdata/oradata/prodres/a_txn_ind02.dbf';

set newname for datafile 27  to '/dbdata/oradata/prodres/a_txn_ind03.dbf';

set newname for datafile 28  to '/dbdata/oradata/prodres/a_txn_ind04.dbf';

set newname for datafile 29  to '/dbdata/oradata/prodres/a_txn_ind05.dbf';

set newname for datafile 30  to '/dbdata/oradata/prodres/ctxd01.dbf';

set newname for datafile 31  to '/dbdata/oradata/prodres/odm.dbf';

set newname for datafile 32  to '/dbdata/oradata/prodres/olap.dbf';

set newname for datafile 33  to '/dbdata/oradata/prodres/owad01.dbf';

set newname for datafile 34  to '/dbdata/oradata/prodres/portal01.dbf';

set newname for datafile 35  to '/dbdata/oradata/prodres/sysaux01.dbf';

set newname for datafile 36  to '/dbdata/oradata/prodres/apps_ts_tools01.dbf';

set newname for datafile 37  to '/dbdata/oradata/prodres/a_txn_data4.dbf';

set newname for datafile 38  to '/dbdata/oradata/prodres/cuxd01.dbf';

set newname for datafile 39  to '/dbdata/oradata/prodres/cuxx01.dbf';

set newname for datafile 40  to '/dbdata/oradata/prodres/a_txn_data05.dbf';

set newname for datafile 41  to '/dbdata/oradata/prodres/a_txn_data06.dbf';

set newname for datafile 42  to '/dbdata/oradata/prodres/a_txn_data07.dbf';

set newname for datafile 43  to '/dbdata/oradata/prodres/a_txn_ind06.dbf';

set newname for datafile 44  to '/dbdata/oradata/prodres/a_txn_ind07.dbf';

set newname for datafile 45  to '/dbdata/oradata/prodres/undo02.dbf';

set newname for datafile 46  to '/dbdata/oradata/prodres/undo03.dbf';

set newname for datafile 47  to '/dbdata/oradata/prodres/sysaux02.dbf';

set newname for datafile 48  to '/dbdata/oradata/prodres/system12.dbf.dbf';

set newname for datafile 49  to '/dbdata/oradata/prodres/ctxd02.dbf';

set newname for datafile 50  to '/dbdata/oradata/prodres/system13.dbf';

set newname for datafile 51  to '/dbdata/oradata/prodres/cuxx02.dbf';

set newname for datafile 52  to '/dbdata/oradata/prodres/cuxd02.dbf';

set newname for datafile 53  to '/dbdata/oradata/prodres/a_ref03.dbf';

set newname for datafile 54  to '/dbdata/oradata/prodres/undo04.dbf';

set newname for datafile 55  to '/dbdata/oradata/prodres/cuxd03.dbf';

set newname for datafile 56  to '/dbdata/oradata/prodres/ctxd03.dbf';

set newname for datafile 57  to '/dbdata/oradata/prodres/undo05.dbf';

set newname for datafile 58  to '/dbdata/oradata/prodres/undo06.dbf';

set newname for datafile 59  to '/dbdata/oradata/prodres/cuxd04.dbf';

set newname for datafile 60  to '/dbdata/oradata/prodres/undo07.dbf';

set newname for datafile 61  to '/dbdata/oradata/prodres/cuxd05.dbf';

set newname for datafile 62  to '/dbdata/oradata/prodres/cuxx03.dbf';

set newname for datafile 63  to '/dbdata/oradata/prodres/a_media02.dbf';

set newname for datafile 64  to '/dbdata/oradata/prodres/undo08.dbf';

set newname for datafile 65  to '/dbdata/oradata/prodres/undo09.dbf';

set newname for datafile 66  to '/dbdata/oradata/prodres/cuxd06.dbf';

set newname for datafile 67  to '/dbdata/oradata/prodres/undo10.dbf';

set newname for datafile 68  to '/dbdata/oradata/prodres/undo11.dbf';

set newname for datafile 69  to '/dbdata/oradata/prodres/cuxx04.dbf';

set newname for datafile 70  to '/dbdata/oradata/prodres/cuxd07.dbf';

set newname for datafile 71  to '/dbdata/oradata/prodres/undo12.dbf';

set newname for datafile 72  to '/dbdata/oradata/prodres/cuxd08.dbf';

set newname for datafile 73  to '/dbdata/oradata/prodres/cuxd09.dbf';

set newname for datafile 74  to '/dbdata/oradata/prodres/cuxx05.dbf';

set newname for datafile 75  to '/dbdata/oradata/prodres/cuxd10.dbf';

set newname for datafile 76  to '/dbdata/oradata/prodres/cuxd11.dbf';

set newname for datafile 77  to '/dbdata/oradata/prodres/cuxx06.dbf';

set newname for datafile 78  to '/dbdata/oradata/prodres/cuxd12.dbf';

set newname for datafile 79  to '/dbdata/oradata/prodres/cuxd13.dbf';

set newname for datafile 80  to '/dbdata/oradata/prodres/cuxx07.dbf';

set newname for datafile 81  to '/dbdata/oradata/prodres/undo13.dbf';

set newname for datafile 82  to '/dbdata/oradata/prodres/cuxd14.dbf';

set newname for datafile 83  to '/dbdata/oradata/prodres/cuxx08.dbf';

set newname for datafile 84  to '/dbdata/oradata/prodres/cuxd15.dbf';

set newname for datafile 85  to '/dbdata/oradata/prodres/cuxd16.dbf';

set newname for datafile 86  to '/dbdata/oradata/prodres/cuxd17.dbf';

set newname for datafile 87  to '/dbdata/oradata/prodres/cuxx09.dbf';

set newname for datafile 88  to '/dbdata/oradata/prodres/a_media03.dbf';

set newname for datafile 89  to '/dbdata/oradata/prodres/cuxd18.dbf';

set newname for datafile 90  to '/dbdata/oradata/prodres/cuxx10.dbf';

set newname for datafile 91  to '/dbdata/oradata/prodres/cuxd19.dbf';

set newname for datafile 92  to '/dbdata/oradata/prodres/cuxd20.dbf';

set newname for datafile 93  to '/dbdata/oradata/prodres/cuxx11.dbf';

set newname for datafile 94  to '/dbdata/oradata/prodres/cuxd21.dbf';

set newname for datafile 95  to '/dbdata/oradata/prodres/cuxd22.dbf';

set newname for datafile 96  to '/dbdata/oradata/prodres/cuxx12.dbf';

set newname for datafile 97  to '/dbdata/oradata/prodres/cuxx13.dbf';

set newname for datafile 98  to '/dbdata/oradata/prodres/cuxd23.dbf';

set newname for datafile 99  to '/dbdata/oradata/prodres/cuxd24.dbf';

set newname for datafile 100 to '/dbdata/oradata/prodres/cuxd25.dbf';

set newname for datafile 101 to '/dbdata/oradata/prodres/cuxd26.dbf';

set newname for datafile 102 to '/dbdata/oradata/prodres/cuxx14.dbf';

set newname for datafile 103 to '/dbdata/oradata/prodres/a_media04.dbf';

set newname for datafile 104 to '/dbdata/oradata/prodres/cuxd27.dbf';

set newname for datafile 105 to '/dbdata/oradata/prodres/cuxd28.dbf';

set newname for datafile 106 to '/dbdata/oradata/prodres/cuxx15.dbf';

set newname for datafile 107 to '/dbdata/oradata/prodres/a_media05.dbf';

set newname for datafile 108 to '/dbdata/oradata/prodres/cuxd29.dbf';

set newname for datafile 109 to '/dbdata/oradata/prodres/cuxd30.dbf';

set newname for datafile 110 to '/dbdata/oradata/prodres/cuxx16.dbf';

set newname for datafile 111 to '/dbdata/oradata/prodres/cuxd31.dbf';

set newname for datafile 112 to '/dbdata/oradata/prodres/cuxd32.dbf';

set newname for datafile 113 to '/dbdata/oradata/prodres/cuxx17.dbf';

set newname for datafile 114 to '/dbdata/oradata/prodres/cuxd33.dbf';

set newname for datafile 115 to '/dbdata/oradata/prodres/cuxx18.dbf';

set newname for datafile 116 to '/dbdata/oradata/prodres/cuxd34.dbf';

set newname for datafile 117 to '/dbdata/oradata/prodres/cuxx19.dbf';

set newname for datafile 118 to '/dbdata/oradata/prodres/cuxx20.dbf';

set newname for datafile 119 to '/dbdata/oradata/prodres/cuxd35.dbf';

set newname for datafile 120 to '/dbdata/oradata/prodres/cuxd36.dbf';

set newname for datafile 121 to '/dbdata/oradata/prodres/cuxd37.dbf';

set newname for datafile 122 to '/dbdata/oradata/prodres/cuxd38.dbf';

set newname for datafile 123 to '/dbdata/oradata/prodres/cuxd39.dbf';

set newname for datafile 124 to '/dbdata/oradata/prodres/cuxd40.dbf';

set newname for datafile 125 to '/dbdata/oradata/prodres/cuxx21.dbf';

set newname for datafile 126 to '/dbdata/oradata/prodres/cuxx22.dbf';

set newname for datafile 127 to '/dbdata/oradata/prodres/a_media06.dbf';

set newname for datafile 128 to '/dbdata/oradata/prodres/cuxd41.dbf';

set newname for datafile 129 to '/dbdata/oradata/prodres/cuxd42.dbf';

set newname for datafile 130 to '/dbdata/oradata/prodres/cuxd43.dbf';

set newname for datafile 131 to '/dbdata/oradata/prodres/cuxd44.dbf';

set newname for datafile 132 to '/dbdata/oradata/prodres/cuxx23.dbf';

set newname for datafile 133 to '/dbdata/oradata/prodres/a_media07.dbf';

set newname for datafile 134 to '/dbdata/oradata/prodres/a_media08.dbf';

set newname for datafile 135 to '/dbdata/oradata/prodres/cuxx24.dbf';

set newname for datafile 136 to '/dbdata/oradata/prodres/cuxd45.dbf';

set newname for datafile 137 to '/dbdata/oradata/prodres/cuxd46.dbf';

set newname for datafile 138 to '/dbdata/oradata/prodres/cuxx25.dbf';

set newname for datafile 139 to '/dbdata/oradata/prodres/cuxd47.dbf';

set newname for datafile 140 to '/dbdata/oradata/prodres/cuxd48.dbf';

set newname for datafile 141 to '/dbdata/oradata/prodres/cuxd49.dbf';

set newname for datafile 142 to '/dbdata/oradata/prodres/cuxd50.dbf';

set newname for datafile 143 to '/dbdata/oradata/prodres/cuxd51.dbf';

set newname for datafile 144 to '/dbdata/oradata/prodres/cuxd52.dbf';

set newname for datafile 145 to '/dbdata/oradata/prodres/cuxd53.dbf';

set newname for datafile 146 to '/dbdata/oradata/prodres/cuxd54.dbf';

set newname for datafile 147 to '/dbdata/oradata/prodres/cuxd55.dbf';

set newname for datafile 148 to '/dbdata/oradata/prodres/cuxd56.dbf';

set newname for datafile 149 to '/dbdata/oradata/prodres/cuxd57.dbf';

set newname for datafile 150 to '/dbdata/oradata/prodres/cuxd58.dbf';

set newname for datafile 151 to '/dbdata/oradata/prodres/cuxd59.dbf';

set newname for datafile 152 to '/dbdata/oradata/prodres/cuxd60.dbf';

set newname for datafile 153 to '/dbdata/oradata/prodres/cuxx26.dbf';

set newname for datafile 154 to '/dbdata/oradata/prodres/cuxx27.dbf';

set newname for datafile 155 to '/dbdata/oradata/prodres/cuxx28.dbf';

set newname for datafile 156 to '/dbdata/oradata/prodres/cuxx29.dbf';

set newname for datafile 157 to '/dbdata/oradata/prodres/cuxx30.dbf';

set newname for datafile 158 to '/dbdata/oradata/prodres/cuxx31.dbf';

set newname for datafile 159 to '/dbdata/oradata/prodres/cuxx32.dbf';

set newname for datafile 160 to '/dbdata/oradata/prodres/cuxx33.dbf';

set newname for datafile 161 to '/dbdata/oradata/prodres/cuxx34.dbf';

set newname for datafile 162 to '/dbdata/oradata/prodres/cuxx35.dbf';

set newname for datafile 163 to '/dbdata/oradata/prodres/cuxx36.dbf';

set newname for datafile 164 to '/dbdata/oradata/prodres/a_media09.dbf';

set newname for datafile 165 to '/dbdata/oradata/prodres/a_media10.dbf';

set newname for datafile 166 to '/dbdata/oradata/prodres/a_txn_data08.dbf';

set newname for datafile 167 to '/dbdata/oradata/prodres/a_txn_ind08.dbf';

set newname for datafile 168 to '/dbdata/oradata/prodres/cuxd61.dbf';

set newname for datafile 169 to '/dbdata/oradata/prodres/cuxd62.dbf';

set newname for datafile 170 to '/dbdata/oradata/prodres/cuxd63.dbf';

set newname for datafile 171 to '/dbdata/oradata/prodres/a_txn_data09.dbf';

set newname for datafile 172 to '/dbdata/oradata/prodres/cuxd64.dbf';

set newname for datafile 173 to '/dbdata/oradata/prodres/cuxd65.dbf';

set newname for datafile 174 to '/dbdata/oradata/prodres/a_media11.dbf';

set newname for datafile 175 to '/dbdata/oradata/prodres/a_media12.dbf';

restore database;

switch datafile all;

recover database;

release channel t1;

release channel t2;

release channel t3;

}

数据文件恢复完成后，打开数据库，这里报错是因为redo log和原机不一样，要修改

SQL>

SQL> alter database open resetlogs

2  ;

alter database open resetlogs

*

ERROR at line 1:

ORA-00344: unable to re-create online log '/oradata/apps/redo01.log'

ORA-27040: file create error, unable to create file

HPUX-ia64 Error: 2: No such file or directory

Additional information: 1

查看当前redo log路径

SQL> select group#,member from v$logfile;

修改成正确的路径

alter database rename file '/oradata/prod/db/apps_st/data/log02a.dbf' to '/dbdata/oradata/prodres/log02a.dbf';

alter database rename file '/oradata/prod/db/apps_st/data/log02b.dbf' to '/dbdata/oradata/prodres/log02b.dbf';

alter database rename file '/oradata/prod/db/apps_st/data/log01a.dbf' to '/dbdata/oradata/prodres/log01a.dbf';

alter database rename file '/oradata/prod/db/apps_st/data/log01b.dbf' to '/dbdata/oradata/prodres/log01b.dbf';

然后再尝试打开数据库

SQL> alter database open resetlogs;

最后就可以正常打开数据库

SQL> alter database open upgrade;

Database altered.

SQL>

4.2、配置db2备份与恢复

db2恢复会先创建容器创建容器的过程数据存储会占用空间，但是看不到恢复进度

创建完容器后，存储空间不再变化，可以看到恢复进度

确认DB2处于归档日志模式

开启归档才能online备份

如果DB2系统的日志备份需要配置成为自动备份，则需要更新DB2实例中每一个数据库的配置，具体实例如下，以DB2用户登录：

1.进入db2用户环境

#su – db2inst3

Windows要用命令db2cmd

2.连接到db2实例

# db2 list db directory

#db2 connect to GDB

3.查看db2数据库的主日志归档方法

# db2 get db cfg |grep -i log

Windows要用命令db2 get db cfg | findstr –I log

查看LOGARCHMETH1是否有类似值'DISK:/archive_log'"

安装networker软件

请参考前面章节

配置DB2备份策略

在客户端点右键，选择新建客户端向导

输入备份主机名

选择DB2

选择自定义

默认点next

输入DB2参数，DB2实例的用户名和密码

选择备份对象

选择备份参数，如果DB2主机没有启用DAS，就把最下面的勾去掉（include system information in the backup）

默认点next

把前面的配置保存成一个新文件，输入文件完整路径

点创建，完成客户端创建

然后再创建组和备份策略，就可以备份该客户机了。

本机恢复

Networker准备工作

创建DB2_CFG文件/nsr/apps/config/nmda_db2_XSMEC_res.cfg如下：

DB2INSTANCE=db2inst8

DB2_NODE_NAME=db2inst8

NSR_CLIENT = p750rRST

NSR_SERVER=vmprdnetworker

把其它参数注释掉，也不用用户名及生成密码。

查找某个时间戳的数据库备份

# nsrinfo -s vmprdnetworker -n db2 -X all p750rRST | grep isfstdb

version=1,  DB2, objectname=/ISFSTDB/NODE0000 /DB_BACKUP.20190220090818.2, createtime=Wed Feb 20 09:08:19 2019, copytype=BSACopyType_BACKUP, copyId=1550624899.1550624900, restoreOrder=1550624899.1, objectsize=0.0, resourcetype=database,  BSAObjectType_DATABASE,  BSAObjectStatus_ACTIVE, description=NMDA_v92:DB2_v97B:FULL_BACKUP:ISFSTDB:TNE, objectinfo=db2inst8:2

version=1,  DB2, objectname=/ISFSTDB/NODE0000 /DB_BACKUP.20190220090818.1, createtime=Wed Feb 20 09:08:18 2019, copytype=BSACopyType_BACKUP, copyId=1550624898.1550624899, restoreOrder=1550624898.1, objectsize=0.0, resourcetype=database,  BSAObjectType_DATABASE,  BSAObjectStatus_ACTIVE, description=NMDA_v92:DB2_v97B:FULL_BACKUP:ISFSTDB:TEQ, objectinfo=db2inst8:2

或在源机器上查看历史备份情况，选择相应的版本进行恢复：

$ db2 list history backup all for p750rRST

开始恢复

如果dac数据库存在

> db2 restore db ISFSTDB load /usr/lib/libnsrdb2.so open 2 sessions options @/nsr/apps/config/db2_full_res.cfg taken at 20190220090818

如果dac数据库不存在

> db2 restore db ISFSTDB load /usr/lib/libnsrdb2.so open 2 sessions options @/nsr/apps/config/db2_full_res.cfg taken at 20190220090818 into ISFSTDB

查询恢复状态

$ db2 rollforward db ISFSTDB query status

前滚日志

$ db2 "rollforward db ISFSTDB to end of logs and stop”

至此恢复成功

异机恢复

原机：hnlcdb01_svc上db2inst2实例下的数据库XSMEC

恢复目标机：cdptest1上db2inst2实例下的数据库XSMVTL

Networker准备工作

1、需要在原机和目标机的host互相解释

2、在恢复目标机安装networker软件和nmda模块，并在networker创建客户端和配置设备

3、在目标机设置环境变量，即创建DB2_CFG文件/nsr/apps/config/nmda_db2_XSMEC_res.cfg如下：

DB2_NODE_NAME =db2inst2 （原机）

DB2INSTANCE =db2inst2  （原机）

NSR_CLIENT =hnlcdb01_svc （原机）

NSR_SERVER = nwserver

把其它参数注释掉，也不用用户名及生成密码。

3、如果是恢复到不同DB2实例，需要在nwserver修改原机hnlcdb01_svc属性

在应用程序信息里加上：DB2_R=XSMEC:db2inst2:db2inst2:

XSMEC表示要恢复的数据库，接着是原机数据库所在实例名，最后是目标机恢复实例名

查找某个时间戳的数据库备份

# nsrinfo -s NetWorker_server -n db2 -X all DB2_client | grep database_name

或在源机器上查看历史备份情况，选择相应的版本进行恢复：

$ db2 list history backup all for SAMPLE

开始异机恢复

1. 生成db2恢复脚本.

$ db2 restore db XSMEC load /usr/lib/libnsrdb2.o open 2 sessions options @/nsr/apps/config/nmda_db2_XSMEC_res.cfg taken at 201305251654 to  '/xsmrecdata/XSMVTL' into XSMVTL LOGTARGET '/xsmrecdata/XSMVTL' redirect generate script restore_XSMVTL.sql

注意上面时间戳格式是yyyymmddtttt

2．修改生成的脚本restore_XSMVTL.sql（注意恢复目录/xsmrecdata/XSMVTL要给足够权限，例如777）：

修改ON ‘/bigspace/home/db2inst2’

DEVICE改成FILE （也就是说，之前是用祼设备的表空间将变成文件形式）

表空间文件路径需要指向重定向文件夹：/xsmrecdata/XSMVTL

如：’ /dev/rMDM_20_001’改成’ /xsmrecdata/XSMVTL /rMDM_20_001’

4. 在目标机运行修改后的恢复脚本:

$ db2 -tvf restore_XSMVTL.sql

5. 前滚日志：

$ db2 rollforward db sample query status  查询恢复状态

$ db2 "rollforward db XSMVTL to end of logs and stop overflow log path (/xsmrecdata/XSMVTL)"

至此数据库处于一致性状态，检查数据是否恢复回来。

4.3、VMWARE备份与恢复

如果有其它vmware备份工具，需要先停用，再部署NVP。

配置备份策略

部署VPROXY ovf模板

在vSphere client中选择文件，选择部署ovf模板

选择ova文件位置。

设置部署VM的名称及清单位置：

选择datacenter位置：

选择datastore：

选择部署的网络：

输入需要配置的ip及主机名等信息：

设置Timezone(时区)，用户名及密码默认即可

VCenter注册

VCenter注册到备份软件中的过程为：

登录EMC Networker administration的管理界面，在“protection”选择“vmware view”，右键点击选择“add vCenter”：

输入vCenter名称，用户名及密码=<已脱敏>

在NMC中添加vProxy

首先在备份服务器添加vProxy的hosts解析

然后登陆vProxy，添加备份服务器、DD、Vcenter的hosts解释

登录EMC Networker administration的管理界面，在“设备”选择“VMware Proxies”，右键点击选择“新建”：

输入上一步中部署的vProxy虚拟机的名字：

选择已注册的vCenter：

如果所有VM都能hotadd，就不要改NBD session，输入user id 和password=<已脱敏>

创建VMware Proxy建完成：

虚拟机备份配置过程：

虚拟机备份policy过程与其它类型的备份配置过和类似：

先创建虚拟机的备份group，选中要加入到这个group的虚拟机：

创建policy过程如下：

创建workflow，然后点击“添加”：

目标池选择之前创建的ddboost pool

点配置

点确定

（以上过程就完成了虚拟机备份的配置）

恢复

Vm recovery

FLR文件级别恢复

打开恢复向导

在下面点Start Mount

选中要恢复的文件，点下一步

选中要恢复到目标机器的哪个目录，点下一步

为本次恢复起一下名字

4.4、MSSQL备份与恢复

备份

恢复

Normal就是覆盖恢复，Copy就是恢复一个新的数据库

4.5、NAS备份与恢复

创建备份策略

备份策略配置如下

输入主机名，选ndmp备份类型：

NAS恢复

在备份服务器打开networker user程序，点recover

选择要恢复哪台机器的备份

选择要把数据恢复到哪台机

选择要恢复的文件

点Recover Options

默认恢复到原来路径，可以在下面填入新的恢复路径

点下面红框图标

如下已经恢复完成

4.6、MYSQL备份与恢复

备份

检查兼容性

确保mysql主机安装了正确版本的MEB

安装networker

1、安装networker软件

# rpm -ivh lgtoclnt-<IP地址已脱敏>-1.x86_64.rpm

# rpm -ivh lgtoxtdclnt-<IP地址已脱敏>-1.x86_64.rpm

# /etc/init.d/networker start

# rpm -ivh lgtonmda-<IP地址已脱敏>-1.x86_64.rpm

2、Linking NMDA in a MySQL environment

# ln -s /usr/lib64/mysql/libmysqlclient.so.20 /usr/lib64/libmysqlclient.so

# ln –s /var/lib/mysql/mysql.sock /tmp/mysql.sock

3、编辑my.cnf

# cp /etc/my.cnf /etc/my.cnf.bak

# vi /etc/my.cnf

加上

[client]

port=3306

socket=/var/lib/mysql/mysql.sock

innodb_log_file_size=30M#mysql5.5以上一定要设置这个参数大于5M，不然备份出来的数据恢复不了

4、然后重启mysql服务

# service mysqld stop

# service mysqld status

# service mysqld start

开启bin-log日志

配置备份策略

在NMC用向导创建client

输入mysql的管理员用户和密码

创建完client后，再创建group和policy，然后就可以备份了

恢复mysql

在NMC点要恢复主机的右键，选择恢复

下面输入一个临时恢复目录（该目录要提前创建），用于存放恢复数据缓存

选择一个备份时间点

到此恢复完成

启动数据库：#service mysqld start

查数据库是否恢复回来

mysql> show databases;

+--------------------+

| Database           |

+--------------------+

| information_schema |

| db_amiagent        |

| mysql              |

| performance_schema |

| sys                |

| test03             |

+--------------------+

6 rows in set (0.00 sec)

4.7、AD备份与恢复

备份

点右键新建客户端

恢复

在恢复机器上打开networker user for micorsoft

选中要恢复的对象

恢复完成

networker备份软件日常维护

检查备份任务完成状态

当前备份状态

从EMC Networker的管理界面中可以直接监控到当天的状态：

“登录”“企业” “监控”：

选择一个备份策略，鼠标右击得到下拉菜单，选择Show Details按钮,如下图：

如果备份操作已经正常完成，所有的备份操作的历史记录将被显示在“Completed Successfully” 的信息框中,未完成备份的文件或文件系统将被显示在“Currently Running”的信息框中，出现错误的备份显示在“Failed”的信息框中，系统备份管理员可查明未完成原因后 ，继续完成此备份操作。

客户机组的备份失败可能是由于以下一种原因：

◆ NetWorker 服务器出现故障。

◆ NetWorker 客户机出现故障。

◆ 网络连接出现故障。

备份状态通过图标来表示。下表列出了每个图标并对其进行了说明。

| 图标 | 标记 | 说明 |

|  | 失败 | 组备份失败。 |

|  | 已中断 | 组备份已中断。 |

|  | 从未运行 | 组备份从未运行。 |

|  | 正在运行 | 组备份正在运行。 |

|  | 正在克隆 | 正在克隆组备份。 |

|  | 已成功 | 已成功完成组备份。 |

检查备份卷使用空间

从Networker主机上查看D盘的空间使用情况。

从Networker上可看到卷的大小

根据空间使用情况调整备份策略，延长或缩短保存期，以防止备份空间满。

磁带同样道理要检查磁带是否够，如果不够则标签磁带

查看备份历史信息

在NMC点Reports，可以查看各类数据的备份信息

配置邮件告警

在Action里输入smtpmail –h snmp主机 –s “Alert” 收件人邮箱

Networker活动日志

从Networker主界面“监视”“日志”可看到Networker的活动日志

Networker服务器上，Networker的活动日志为D:\EMC Networker\nsr\logs下的daemon.raw文件，要查看该文件的内容，可使用命令

#nsr_render_log daemon.raw>daemon.log

将daemon.raw转换成daemon.log，再查看daemon.log即可看到有活动时间的详细活动日志。

networker进程介绍及服务重启

下面networker开头的4个服务

下面EMC开头的服务也要启动

Networker常见命令

1、停止networker服务：

# nsr_shutdown -qf

2、networker服务：

# systemctl start networker

3、测试网络连通性：

# nsrrpcinfo –p 对方主机名

4、清除主机缓存信息：

在Networker server上:

>nsradmin -p nsrexec

>p type: NSR peer information; name: clientname

>delete

>yes

在client server上:

>nsradmin -p nsrexec

>p type: NSR peer information; name: servername

>delete

>yes

重启客户端networker service

>nsradmin

vi进入操作界面

ps -ef|grep nsr

ps -ef|grep -i gst

ps -ef|grep -i http

DD日常维护

查看DD告警信息

登陆DD之后，如果有alert信息，要注意查看

点alerts，可查看alerts详细信息

也可以在NMC查看

查看DD空间使用情况

点击Data Management可以看到DD2500空间的使用情况，包括实际使用大小

DD常见命令

查看ddboost备份速度

ddboost show stats interval 2

查看网卡速度

system show stats view net interval 2

查看IP信息

net show setting

提高DD消重比

1、对于oracle备份，可通过ＲＭＡＮ备份脚本中修改fileperset参数提高消重比率：

对于Oracle datafile的全备份，设置filesperset 1

对于oracle datafile的增量备份，或者archivelog备份，由于重复数据少，设置filesperset=1对消重没效果，可默认不设置，或者设置更大的fileperset数值以提高备份速度。

2、不要在备份软件或者数据源端启用消重、multiplex、compression、encryption等功能

配置邮件告警

在Subscribers点Configure，添加收件人邮件地址

EMC DD开关机

注意以下DD开关机顺序

关机指引：

首先，关闭备份软件服务

其次，关闭备份介质 DD

开机指引：

首先，开启备份介质 DD,

其次，开启备份软件服务

重启DD

重启DD可通过WEB图形界面或者命令行，下面分别介绍：

WEB方式重启

点下面的Reboot System

命令行方式重启

# system reboot

关闭DD

关闭DD只能通过命令行方式关闭

# system poweroff

The ‘system poweroff’ command shuts down the system and turns off the power. Continue? (yes|no|?) [no]:yes

开启DD

接通主柜电源就可开机

EMC技术支持

固定电话拨打8008190009 ，手机拨打4006700009， 听到提示音后选择3(软件)，再选择对应产品的序号，有人接听后需提供Site ID

Networker需要提供Site ID：14769549

DD需要提供序列号：CKM00184800811
