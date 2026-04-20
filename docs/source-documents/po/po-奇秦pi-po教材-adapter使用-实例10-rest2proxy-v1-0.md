# 奇秦PI&PO教材-Adapter使用-实例10 rest2proxy V1.0

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [po]
issue_types: [reference]
tags: [engineer-doc, imported, po]
source_path: "D:\新建文件夹\业务维护清单\PO\奇秦PI&PO教材-Adapter使用-实例10 rest2proxy V1.0.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：奇秦PI&PO教材-Adapter使用-实例10 rest2proxy V1.0.docx
- 原始路径：D:\新建文件夹\业务维护清单\PO
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

| 汉得PI&PO教材系列 |  |

|  | Adapter使用-实例10：Rest2Proxy APO |

| 仅限汉得内部使用 | 作者：汉得顾问版本：1.0日期：2017-02-25 |

图标

| 图标 | 含义 |

|  | 警告 |

|  | 示例 |

|  | 注释 |

|  | 建议 |

|  | 语法 |

|  | 外部处理 |

|  | 可选业务处理或决定 |

排版惯例

| 字体风格 | 描述 |

| Example text | 出现在屏幕上的单字或字符。包括字段名、屏幕标题、按钮以及菜单名、路径和选项。到其它文档的交叉引用。 |

| Example text | 正文文本中强调的字或词组，图形和表格的标题。 |

| EXAMPLE TEXT | 系统中元素的名称。包括报表名、程序名、事务代码、表名和正文文本中嵌入的编程语言关键字，如 SELECT 和 INCLUDE。 |

| Example text | 屏幕输出。包括文件和目录的名称及其路径、消息、源代码、变量和参数的名称以及安装工具、更新工具和数据库工具的名称。 |

| EXAMPLE TEXT | 键盘上的按键。例如，功能键（如F2）或ENTER键。 |

| Example text | 用户输入原文。完全如文档所示输入这些单字或字符至系统中。 |

| <Example text> | 可变用户输入。尖括号表示应使用适当的输入替换括号中的单字和字符。 |

1、文档说明

本文档目的在于提供一个REST2PROXY场景的接口案例，用于说明REST适配器如何使用，以及使用REST适配器的注意事项以及最佳使用实践。

2、文档历史

| 版本 | 修订时间 | 修订人 | 备注 |

| 0.1 | 2017年02月25日 | 黄照家 | 根据培训案例整理出该文档 |

3、功能说明

本案例中发送方系统为第三方系统BS_FTP_DEV，接收方系统为ERP系统BS_ED1_300，即发送方和接收方为不同系统。实际使用，则根据实际系统来配置不同的业务系统作为数据发送方和接收方。

注意：REST适配器无论Request还是Response方向，其报文格式都是JSON格式的消息报文，但是他和仅仅传输JSON格式报文的接口有本质区别，例如一个SOAP适配器的webservice接口，可以将传入传出参数组织为JSON格式数据输入输出，但是其调用方式却不能以HTTP或REST方式来调用，而应该使用webservice的方式(SOAP协议)调用，而HTTP或REST的接口却不能使用SOAP的方式调用，而应该采用HTTP特性的GET、POST、PUT、DELETE等方法调用。

发送方REST请求消息为JSON报文格式，示例报文如下；

发送方请求的JSON报文，经REST转换为如下XML格式，此报文格式可以与PROXY对应的XML报文做映射关系转换(Message Mapping):

发送方发出的JSON报文经REST转换后与PROXY接收报文做映射转换，接收方PROXY接收到的的XML报文格式示例如下：

接收方PROXY，响应报文为XML格式，示例如下：

接收方返回的PROXY报文为XML格式，经映射转换后转换为发出方应接收的XML报文字段，（此报文经REST转换后即可输出为发送方所需接收的JSON格式报文）:

发送方所需接收的XML字段报文，经REST转换后，转换为JSON格式，通过REST适配器返回给发送方，发送方接收到的响应报文格式示例如下：

本案例发送的为简单的测试数据。

4、操作步骤-定义IR对象

异步方式发送，所需IR对象如下图：

4.1 定义Data Type

在安装的发送方软件组件 （SC_FTP） 分别创建Request和Response方向的Data Type。

SC_FTP下定义发送方发出格式的Data Type

SC_FTP下定义发出方接收格式的Data Type

在安装的接收方软件组件 （SC_ERP） 分别创建Request和Response方向的Data Type。

SC_ERP下定义接收方接收格式的Data Type

SC_ERP下定义接收方返回格式的Data Type

4.2 定义Message Type

在安装的发送方软件组件 （SC_FTP） 分别创建Request和Response方向的Message Type。

定义发送方发出格式的Message Type(MT_000_REST2PROXY_001_Req)，关联发送方发出格式的Data Type，即SC_FTP下的DT_000_REST2PROXY_001_Req

定义发出方接收格式的Message Type(MT_000_REST2PROXY_001_Res)，关联发出方接收格式的Data Type，即SC_FTP下的DT_000_REST2PROXY_001_Res

在安装的接收方软件组件 （SC_ERP） 分别创建Request和Response方向的Message Type。

定义接收方接收格式的Message Type(MT_000_REST2PROXY_001_Req)，关联接收方接收格式的Data Type，即SC_ERP下的DT_000_REST2PROXY_001_Req

定义接收方返回格式的Message Type(MT_000_REST2PROXY_001_Res)，关联发出方接收格式的Data Type，即SC_ERP下的DT_000_REST2PROXY_001_Res

4.3 定义Service Interface

定义发送方Service Interface，属性是Outbound，选择同步方式，关联发送方Message Type，即SC_FTP下的MT_000_REST2PROXY_001_Req以及MT_000_REST2PROXY_001_Res

定义接收方Service Interface，属性是Inbound，选择同步方式，关联接收方Message Type，即SC_ERP下的MT_000_REST2PROXY_001_Req以及MT_000_REST2PROXY_001_Res

4.4 定义Message Mapping

在安装的接收方ERP系统的软件组件（SC_ERP）下创建Request Message Mapping，发送Message Type为SC_FTP下的DT_000_REST2PROXY_001_Req，接收Message Type为SC_ERP下的 MT_000_REST2PROXY_001_Req，维护对应关系

同步方式下有两个MM，选择发送方Message Type，接收方Message Type，匹配字段对应关系。

创建Request方向的 Message Mapping，发送Message Type

为SC_FTP下的DT_000_REST2PROXY_001_Req，接收Message Type为SC_ERP下的 MT_000_REST2PROXY_001_Req

创建Response 方向的Message Mapping，发送Message Type

为SC_ERP下的MT_000_REST2PROXY_001_Res，接收Message Type为SC_FTP下的MT_000_REST2PROXY_001_Res，维护对应关系

4.5 定义Operation Mapping

在安装的接收方ERP系统的软件组件（SC_ERP）下创建Operation Mapping，源Service Interface为SC_FTP下的SI_000_REST2PROXY_001_Outbound，目标Service Interface为SC_ERP下的SI_000_REST2PROXY_001_Inbound。

选择发送方Service Interface，接收方Service Interface，选择Request Message Mapping

选择Response Message Mapping

5、 操作步骤-定义ID对象

所需ID对象如下图，可以先定义Configuration Scenario（可以理解为接口场景对象的容器，用于组织ID对象用，通常将构成一个接口的所有对象放到一个Configuration Scenario，同一个对象可以放到多个Configuration Scenario，便于组织构成接口的完整对象）。

5.1 定义发送方Communication Channel

定义发送方Communication Channel，选择发送方Business System（BS_FTP_DEV），选择REST适配器。

5.2 定义接收方Communication Channel

指定数据接收方业务系统（BS_ED1_300），选择PROXY适配器，输入登录ERP系统服务器及客户端信息（多个外围系统调用该接口，此CC可共用）。

5.3 定义Integrated Configuration

输入发送方业务系统（BS_FTP_DEV），输入发送方Service Interface，发送方Communication Channel

维护接收方业务系统（BS_ED1_300）

维护接收方Operation Mapping以及Service Interface

维护接收方Communication Channel

保存，激活，查看传输日志。

调用地址 http://<IP>:<Port>/RESTAdapter/<EndPoint>/

例如本例的调用地址为：http://IP:Port/RESTAdapter/TestRestService001/

提供此URL地址给第三方调用即可，实现REST2PROXY。

6、调用

保存激活后，在ERP系统运行事务SPROXY，双击SI生成类

实现功能代码，即可调用。

7、传输监控

SOAPUI测试。

返回结果

PI监控消息，调用成功。
