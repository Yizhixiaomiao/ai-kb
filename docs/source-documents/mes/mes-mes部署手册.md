# Mes部署手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [mes]
issue_types: [reference]
tags: [engineer-doc, imported, mes]
source_path: "D:\新建文件夹\业务维护清单\MES\Mes部署手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：Mes部署手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\MES
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

MES系统部署手册

1.Redis

1.1 Redis路径

路径：D:\Redis-x64-3.2.100

1.2 Redis启动

双击桌面的Redis 快捷方式启动Redis服务

桌面出现如下窗口，并且任务管理器的详细信息中出现redis-server.exe服务即表示Redis服务启动成功，注意：将桌面弹出的Redis窗口隐藏即可，切勿关闭窗口（窗口关闭的话服务也会随之关闭）

1.3 Redis关闭

关闭Redis运行窗口即可停止Redis服务

2. Nginx

2.1Nginx路径

路径：   D:\nginx

2.2Nginx启动

双击桌面的Nginx快捷方式启动Nginx服务

桌面出现如下窗口，并且任务管理器的详细信息中出现三个nginx.exe服务即表示Nginx服务启动成功，Nginx窗口可以关闭

2.3Nginx关闭

在任务关闭器中结束这三个进程

3.web服务

3.1代码打包

在idea中打开项目

点击最右边的Maven栏目

打开Maven下的自定义工件（示例中为prj-nkl）下的Lifecycle

双击clean

出现如下语句，表示clean完成

而后双击install（静等打包完成）

出现如下语句，表示install完成（打包完成）

war包路径：mes\target\prj-pr.war (相对路径)，为工程的target目录下

3.2web服务发布

3.2.1Tomcat路径：D:\apache-tomcat-8.5.60

3.2.2 上传war包

将打好的war包上传至服务器（在本机电脑复制，然后到服务器上粘贴即可）

替换war包中的配置文件

打开war包将Tomcat下的webapps目录下的application.properties文件和interfacesAddress.properties文件替换war包中的WEB-INF\classes\目录下的application.properties文件和interfacesAddress.properties文件

3.2.3 Tomcat服务关闭

若服务正在运行，需先关闭服务再进行后面的操作

关闭Tomcat运行窗口即可

3.2.4备份

将原有的war备份至Tomcat目录下的bak目录下

删除现有的prj-nkl文件夹

3.2.5 web服务发布

将上传到服务器的新war包，放到Tomcat目录下的webapps目录

启动web服务

双击桌面的启动服务快捷方式启动Tomcat服务

桌面出现如下窗口，表示Tomcat正在启动，服务需要几分钟时间启动完成（切勿关闭Tomcat运行窗口，服务启动完成后隐藏即可）

当Tomcat窗口出现如下日志，表示服务启动成功，隐藏Tomcat窗口即可，切勿关闭，关闭的话服务也会随之关闭的

4. APP发布

4.1代码打包

登录apicloud

网址：https://www.apicloud.com/signin

打开项目

打开云编译页面

平台选中Android

类型选中正式版

拉到页面最下，点击云编译即可（静待打包完成）

打包完成在最下方会出现相应版本号的版本包，点击图示标志下载对应安装包

4.2APP服务发布

4.2.1 上传发布包

APP发布包路径：D:\mestar_home\prj-pr

将下载好的安装包上传至对应服务器（在本机电脑复制，然后到服务器上粘贴即可）

将上传到服务器的APP发布包的文件名修改为当前正在使用的APP包的版本号+1（如图示）

备份原有的APP包，将原来得APP包移动至bak文件夹下

4.2.2 发布APP服务

发布新包，将新的APP包移动至mestar_home\prj-pr文件夹下即可，发布完成

5.帆软服务启动

双击桌面的启动帆软服务快捷方式启动帆软服务

出现如图所示日志，即表示帆软服务启动成功，注意：将桌面弹出的帆软服务窗口隐藏即可，切勿关闭窗口（窗口关闭的话服务也会随之关闭）
