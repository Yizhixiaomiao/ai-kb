# 卫华MES系统手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [mes]
issue_types: [reference]
tags: [engineer-doc, imported, mes]
source_path: "D:\新建文件夹\业务维护清单\MES\卫华MES系统手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：卫华MES系统手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\MES
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

卫华MES系统 操作手册

摘要

该文档详细阐述了卫华MES系统的维护、使用以及操作注意事项。

作者：常帅

日期：2024年8月16日星期五

版本：v1.0

。

卫华集团数字科技中心-运维技术部

文档保证声明

非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

系统概述

MES(Manufacturing Execution System)即制造企业生产过程执行系统，是一套面向制造企业车间执行层的生产信息化管理系统。MES 可以为企业提供包括制造数据管理、计划排产管理、生产调度管理、库存管理、质量管理、人力资源管理、工作中心/设备管理、工具工装管理、采购管理、成本管理、项目看板管理、生产过程控制、底层数据集成分析、上层数据集成分解等管理模块，为企业打造一个扎实、可靠、全面、可行的制造协同管理平台。

服务器基本信息

联系方式

- 系统管理员：常帅，电话：<手机号已脱敏>，邮件：changshuai@craneweihua.com

- 厂家技术支持：

无

硬件信息

卫华MES应用服务器

| 服务器 | 卫华MES应用服务器 | 纽科伦MES应用服务器 | 蒲瑞MES应用服务器 | 江苏MES应用服务器 |

| 系统信息 |  |  |  |  |

| 操作系统 | Microsoft Windows Server 2016 | Microsoft Windows Server 2012 | Microsoft Windows Server 2012 | Microsoft Windows Server 2016 |

| 主机名 |  | WIN-S2E14VIG6EQ | WIN-S2E14VIG6EQ | DSM |

| IP | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 | <IP地址已脱敏>/24 |

| GATEWAY | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> |

| 硬件信息 |  |  |  |  |

| vCPU | 16 | 16 | 16 | 8 |

| 内存 | 64G | 24G | 24G | 16G |

| 硬盘 | 600G | 500G | 500G | 100G+500G |

| VLAN | 1 | 198 | 198 | 198 |

| 宿主信息 |  |  |  |  |

| vCenter | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> | <IP地址已脱敏> |

| 群集 | WH-cluster | WH-cluster | WH-cluster | WH-cluster |

| 服务器 | 江苏卫华数据库服务器 |

| 系统信息 |  |

| 操作系统 | CentOS Linux release 7.9.2009 (Core) |

| 主机名 | mes_js |

| IP | <IP地址已脱敏>/24 |

| GATEWAY | <IP地址已脱敏> |

| 硬件信息 |  |

| vCPU | 28 |

| 内存 | 128G |

| 硬盘 | 200G+1.95T |

| VLAN | 198 |

| 宿主信息 |  |

| vCenter | <IP地址已脱敏> |

| 群集 | Production |

| 配置 | 数据库 |

| 固定资产编号 | 51020140084 |

| 机架编号 | CYA092728(长垣机房行政楼机房09机柜27-28U) |

| 服务器型号 | DELL PowerEdge R740 |

| 出厂序列号 | 5W6D7Z2 |

| IDRAC: | <IP地址已脱敏> |

| CPU | Intel(R) Xeon(R) Gold 5218 CPU @ 2.30GHz / cpu16*2 |

| 内存 | 128G |

| 硬盘 | SSD:480G*2 1.2T*3 |

| 网络接口 | <IP地址已脱敏>XGigabitEthernet0/0/18 |

| VLAN ID | 1 |

| IP | <IP地址已脱敏> |

| 操作系统 | Microsoft Windows Server 2016 Standard |

应用信息

<IP地址已脱敏> 卫华MES服务器

| 业务日志：F:\Mestar_Home-7415-final\prj-hnwh\logs\Unimax应用连接数据库：F:\Mestar_Home-7415-final\prj-hnwh\application.properties图纸路径：F:\Mestar_Home-7415-final\standalone\tmp\vfs\temp\tempb2aa2e68a457ad9c\prj-hnwh.war-9c1345fec1880982\pdf\web部署：nginx版本: 1.9.15端口：80启动命令：F:\Mestar_Home-7415-final\bats\start_nginx_1启动Nginx.bat配置路径：F:\Mestar_Home-7415-final\nginx\conf\nginx.conf日志路径：F:\Mestar_Home-7415-final\nginx\logs部署：redis版本:3.2.100端口：6379启动命令：F:\Redis-x64-3.2.100\startup.bat部署：Jboss版本:1.8.0端口：4449 8082 8789 9992 10001 1499 1799 4447 8080 8787 9990 9999 64481启动命令：F:\Mestar_Home-7415-final\bats\start_single_3-启动单机服务.bat配置路径：F:\Mestar_Home-7415-final\config\conf日志路径：F:\Mestar_Home-7415-final\config\logs部署：帆软端口：8082启动命令：F:\finereport\bats\start_single_3-启动帆软服务.bat配置路径：F:\finereport\config |

<IP地址已脱敏> 纽科伦MES服务器

| 业务日志：D:\mestar_home\prj-nkl\logs应用连接数据库：D:\mestar_home\prj-nkl\application.properties图纸路径：D:\apache-tomcat-8.5.60\webapps\prj-nkl\pdf\web部署：nginx版本: 1.9.15端口：80 8000启动命令：D:\Nginx.bat配置路径：D:\nginx\conf\nginx.conf日志路径：D:\nginx\logs部署：redis版本:3.2.100端口：6379启动命令：D:\Redis-x64-3.2.100\startup.bat部署：tomcat版本:8.5.60端口：4449 8082 8788 9992 10001 1499 1799 8080 64188 8005启动命令：D:\apache-tomcat-8.5.60\bin\startup.bat配置路径：D:\apache-tomcat-8.5.60\conf日志路径：D:\apache-tomcat-8.5.60\logs部署：帆软（停用）端口：8082启动命令：D:\finereport\bats\start_single_3-启动帆软服务.bat |

<IP地址已脱敏> 蒲瑞MES服务器

| 业务日志：D:\mestar_home\prj-pr\logs应用连接数据库：D:\mestar_home\prj-pr\application.properties图纸路径：D:\apache-tomcat-8.5.60\webapps\prj-pr\pdf\web部署：nginx版本: 1.9.15端口：80 8000启动命令：D:\Nginx.bat配置路径：D:\nginx\conf\nginx.conf日志路径：D:\nginx\logs部署：redis版本:3.2.100端口：6379启动命令：D:\Redis-x64-3.2.100\startup.bat部署：tomcat版本:8.5.60端口：4449 8082 8788 9992 10001 1499 1799 8080 65530 8005启动命令：D:\apache-tomcat-8.5.60\bin\startup.bat配置路径：D:\apache-tomcat-8.5.60\conf日志路径：D:\apache-tomcat-8.5.60\logs部署：帆软（停用）端口：启动命令：D:\finereport\bats\start_single_3-启动帆软服务.bat |

<IP地址已脱敏> 江苏MES服务器

| 业务日志：D:\master_home\prj-hnwh\logs应用连接数据库：D:\mestar_home\prj-hnwh\application.properties图纸路径：D:\apache-tomcat-8.5.60\webapps\prj-jswh\pdf\web部署：nginx版本: 1.9.15端口：80启动命令：D:\Nginx.bat配置路径：D:\nginx\conf\nginx.conf日志路径：D:\nginx\logs部署：redis版本:3.2.100端口：6379启动命令：D:\Redis-x64-3.2.100\startup.bat部署：tomcat版本:8.5.60端口：1499 1799 8000 49587 8005启动命令：D:\apache-tomcat-8.5.60\bin\startup.bat配置路径：D:\apache-tomcat-8.5.60\conf日志路径：D:\apache-tomcat-8.5.60\logs |

<IP地址已脱敏>  MES数据库服务器

| 部署：oracle 版本:<IP地址已脱敏>.0端口：1521数据文件路径：G:\oracleTablespace;H:\MESdatafile归档日志路径：H:\archivelogservername:orclsid:orcloracle_base:G:\oracleoracle_home:G\oracle\product\11.2.0\dbhome_1spfile:G:\oracle\product\11.2.0\dbhome_1\database\SPFILEORCL.ORA |

<IP地址已脱敏> 江苏MES数据库服务器

| 部署：oracle 版本:<IP地址已脱敏>.0端口：1521数据文件路径：/ordata/data/ORACLETABLESPACE；/ordata/data/MESDATAFILE归档日志路径：/oradata/log/servername:orclsid:orcloracle_base:/u01/oracleoracle_home:/u01/oracle/product/11.2.0/dbhome_1spfile:/u01/oracle/product/11.2.0/dbhome_1/dbs/spfileorcl.ora |

系统优化配置

| 服务器IP | 系统优化项 | 是否优化 |

| <IP地址已脱敏> | 安装杀毒客户端 | 是 |

|  | 安装蓝鲸客户端， | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 |  |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 |  |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 |  |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 |  |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 |  |

|  | 端口封堵 |  |

| <IP地址已脱敏> | 杀毒客户端 | 是 |

|  | 蓝鲸客户端 | 是 |

|  | 配置进程监控 | 是 |

|  | 限制登录配置 | 是 |

|  | 本地yum源配置 | 是 |

|  | 端口封堵 |  |

4.备份和恢复

| 服务器IP | 备份策略 | 是否开启 |

| <IP地址已脱敏> | 整机备份，第一次全备之后每天增量备份，备份文件保留30天 | 是 |

| <IP地址已脱敏> | 整机备份，第一次全备之后每天增量备份，备份文件保留30天 | 是 |

| <IP地址已脱敏> | 整机备份，第一次全备之后每天增量备份，备份文件保留30天 | 是 |

| <IP地址已脱敏> | 整机备份，第一次全备之后每天增量备份，备份文件保留30天 | 是 |

| <IP地址已脱敏> | VMWARE免代理备份，第一次全备之后每天增量备份，备份文件保留7天 | 是 |

| <IP地址已脱敏> | networker数据库备份，每日全量备份，备份文件保留7天 | 是 |

5.运维手册

5.1服务信息

<IP地址已脱敏> 卫华MES服务器

| 部署业务 | Nginx、weblogic、redis、帆软 |

| 启停命令 | 停止：关闭窗口启动Nginx:F:\Mestar_Home-7415-final\bats\start_nginx_1启动Nginx.batredis:F:\Redis-x64-3.2.100\startup.bat|java:F:\Mestar_Home-7415-final\bats\start_single_3-启动单机服务.bat帆软：F:\finereport\bats\start_single_3-启动帆软服务.bat |

<IP地址已脱敏> 纽科伦MES服务器

| 部署业务 | Nginx、tomcat、redis |

| 启停命令 | 停止：关闭窗口启动Nginx:D:\Nginx.batredis:D:\Redis-x64-3.2.100\startup.battomcat:D:\apache-tomcat-8.5.60\bin\startup.bat |

<IP地址已脱敏> 蒲瑞MES服务器

| 部署业务 | Nginx、tomcat、redis |

| 启停命令 | 停止：关闭窗口启动Nginx:D:\Nginx.batredis:D:\Redis-x64-3.2.100\startup.battomcat:D:\apache-tomcat-8.5.60\bin\startup.bat |

<IP地址已脱敏> 江苏卫华MES服务器

| 部署业务 | Nginx、tomcat、redis |

| 启停命令 | 停止：关闭窗口启动Nginx:D:\Nginx.batredis:D:\Redis-x64-3.2.100\startup.battomcat:D:\apache-tomcat-8.5.60\bin\startup.bat |

<IP地址已脱敏>  MES数据库服务器

| 部署业务 | Oracle <IP地址已脱敏>.0 |

| 启停命令 | 停止实例:shutdown immediate;启动实例:startup启动监听:lsnrctl start |

<IP地址已脱敏>  江苏卫华MES数据库服务器

| 部署业务 | Oracle <IP地址已脱敏>.0 |

| 启停命令 | 停止实例:shutdown immediate;启动实例:startup启动监听:lsnrctl start |

5.2停机维护

当遇到需要停机维护的时候，服务的关闭顺序如下

应用：应用服务tomcat（JBoss）->帆软服务->nginx->redis--> 数据库Oracle

业务恢复启动服务顺序：数据库Oracle-->应用：redis->nginx->应用服务tomcat（JBoss）->帆软服务

5.3日常点检

| 点检内容 | 点检业务正常标准 |

| 备份 | 应用虚拟机在科力锐备份状态成功数据库在networker备份状态成功 |

| 业务状态 | 应用服务nginx、redis、tomca、jboss、帆软正常运行，业务正常访问数据库服务oracle正常运行访问 |

| 硬件状态正常 | 电源、内存、cpu、存储使用状态正常 |

5.4关联业务

| 业务 | 接口调用 |

| <IP地址已脱敏> | 套料发送数据地址：http://<IP地址已脱敏>/api/wh/whpushNestplan |

| 帆软 | http://report.craneweihua.com/webroot/decision |

| PLM | 图纸下载：http://<IP地址已脱敏>:8080/sipmweb/web/download? |

| 加密 | 加密文件下载：http://<IP地址已脱敏>:8090/sipmweb/web/download? |

| WMS | http://<IP地址已脱敏>:9091/newGids |

MES程序更新

| 业务 | 更新操作 |

| 卫华MES更新<IP地址已脱敏> | 1、先关闭启动单机服务窗口2、删除F:\Mestar_Home-7415-final\standalone\tmp\vfs\temp文件夹(剪切temp文件夹到F盘目录下删除，不然删不掉)3、删除F:\Mestar_Home-7415-final\standalone\deployments\prj-hnwh.war.deployed文件4、将需要更新的文件更新到F:\Mestar_Home-7415-final\standalone\deployments\prj-hnwh.war压缩包内5、双击桌面“单机服务”启动服务6、卫华MES App更新：先备份F:\Mestar_Home-7415-final\prj-hnwh目录下的WeiHuaApp_0.0.78.apk文件，将新的apk文件放到该目录下 |

| 纽科伦MES更新<IP地址已脱敏> | 1、先关闭tomcat窗口2、删除D:\apache-tomcat-8.5.60\temp文件夹下的文件3、删除:D:\apache-tomcat-8.5.60\work文件夹下的文件4、将需要更新的文件更新到D:\apache-tomcat-8.5.60\webapps\prj-nkl目录下5、双击桌面“启动服务”启动服务6、纽科伦MES App更新：D:\mestar_home\prj-nkl目录下的 WeiHuaApp_0.0.96.apk文件，将新的apk文件放到该目录下 |

| 蒲瑞MES更新<IP地址已脱敏> | 1、先关闭tomcat窗口2、删除D:\apache-tomcat-8.5.60\temp文件夹下的文件3、删除:D:\apache-tomcat-8.5.60\work文件夹下的文件4、将需要更新的文件更新到D:\apache-tomcat-8.5.60\webapps\prj-pr目录下5、双击桌面“启动服务”启动服务6、纽科伦MES App更新：D:\mestar_home\prj-pr目录下的 WeiHuaApp_0.0.82.apk文件，将新的apk文件放到该目录下 |

| 江苏卫华MES更新<IP地址已脱敏> | 1、先关闭tomcat窗口2、删除D:\apache-tomcat-8.5.60\temp文件夹下的文件3、删除:D:\apache-tomcat-8.5.60\work文件夹下的文件4、将需要更新的文件更新到D:\apache-tomcat-8.5.60\webapps\prj-jswh目录下5、双击桌面“startup.bat”启动服务6、纽科伦MES App更新：D:\master_home\prj-hnwh目录下的WeiHuaApp_0.0.1.apk文件，将新的apk文件放到该目录下 |
