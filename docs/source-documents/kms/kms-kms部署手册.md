# KMS部署手册

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [kms]
issue_types: [reference]
tags: [engineer-doc, imported, kms]
source_path: "D:\新建文件夹\业务维护清单\KMS\KMS部署手册.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：KMS部署手册.docx
- 原始路径：D:\新建文件夹\业务维护清单\KMS
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

配置KMS服务器

vlmcsd从github下载https://github.com/Wind4/vlmcsd/releases下载最新版，以2020-03-28 (svn1113)版本为例进行配置实现自启动。

配置前先更新一下centos系统，执行命令：

yum update

因为服务端配置为的系统为centos 64位，确定一下你这台机器的CPU架构执行命令：

cat /proc/cpuinfo

系统硬件为intel的64位cpu，所以下载成功后，解压出来binaries\Linux\intel\static\vlmcsd-x64-musl-static，将vlmcsd-x64-musl-static文件重命名为vlmcsd，

文件下载：vlmcsd1113

使用winscp软件上传vlmcsd文件到centos系统的/usr/bin/目录下，请设置0755的权限，执行命令：

chmod 755 /usr/bin/vlmcsd

新建vlmcsd.service文件执行命令：

vi /lib/systemd/system/vlmcsd.service

在新建vlmcsd.service的文件中，输入以下内容：

以上内容输入完毕，esc键，再输入:wq保存即可

[Unit]

Description=KMS Server By vlmcsd

After=network.target

[Service]

Type=forking

PIDFile=/var/run/vlmcsd.pid

ExecStart=/usr/bin/vlmcsd -p /var/run/vlmcsd.pid

ExecStop=/bin/kill -HUP $MAINPID

PrivateTmp=true

[Install]

WantedBy=multi-user.target

重载服务：

systemctl daemon-reload

启动VLMCSD：

systemctl start vlmcsd

查看VLMCSD的运行状态：

systemctl status vlmcsd

若出现类似如下显示，则表示已经运行

systemctl enable vlmcsd

systemctl start vlmcsd

systemctl status vlmcsd

reboot重启后，putty右键重启会话，再试下查看VLMCSD的运行状态：

systemctl status vlmcsd

显示在运行，可以正常激活，说明自启动部署成功
