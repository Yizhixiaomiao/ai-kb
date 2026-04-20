# 奇秦PI&PO教材-Adapter使用-实例4 proxy2proxy

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [po]
issue_types: [reference]
tags: [engineer-doc, imported, po]
source_path: "D:\新建文件夹\业务维护清单\PO\奇秦PI&PO教材-Adapter使用-实例4 proxy2proxy.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：奇秦PI&PO教材-Adapter使用-实例4 proxy2proxy.docx
- 原始路径：D:\新建文件夹\业务维护清单\PO
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

1、功能说明

第三方系统（实例用BS_SHD_165）同步调用ERP系统（实例用BS_SHD_165），实现方式proxy2proxy；在ERP系统生成的服务类中实现功能。

2、操作步骤

IR所需组件

2.1 创建Data Type

创建发送方Request Data Type；

创建发送方Response Data Type

创建接收方Request Data Type

创建接收方Response Data Type

2.2 创建Message Type

创建发送方Request Message Type

创建发送方Response Message Type

创建接收方Request Message Type

创建接收方Response Message Type

2.3 创建Service Interface

创建发送方SI，同步模式调用，关联发送方Request MT & Response MT

创建接收方SI，同步模式调用，关联接收方Request MT & Response MT

2.4 创建Message Mapping

创建Request MM，关联发送方Request MT & 接收方Request MT

创建Response MM，关联接收方Response MT & 发送方Response MT

2.5 创建Operation Mapping

流方向从发送方SI到接收方SI，请求方向选Request MM

流方向从发送方SI到接收方SI，响应方向选Response MM

ID所需组件：

2.6 创建Communication Channel

创建发送方CC

创建接收方CC，输入登录目标系统信息

端口：8000

可以通过测试ERP-SICF上的节点得到该地址

2.7 创建Integrated Configuration

输入发送方BS & SI，选择发送方CC

选择接收方BS

选择接收方SI

选择接收方CC

保存激活。

3、调用

执行此步骤前请先参考《汉得PI&PO教材-基础配置-ERP系统配置PROXY连接PO.docx》配置好ERP系统。

保存激活后，在ERP系统运行事务SPROXY，双击SI生成类

在服务类中写代码实现功能

调用消费类
