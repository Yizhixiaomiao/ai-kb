# 工单系统集成说明

本目录用于描述知识库与工单系统的联动方式。

## 文档清单

- [api-contract.md](api-contract.md)：推荐接口、反馈接口、错误码和请求响应字段。
- [data-flow.md](data-flow.md)：从 Markdown 知识到工单推荐结果的数据流。
- [feedback-loop.md](feedback-loop.md)：工程师采纳、拒绝、解决等反馈闭环。
- [deployment-options.md](deployment-options.md)：从本地脚本到 HTTP 服务、数据库、混合检索、RAG 的部署阶段。
- [local-debugging.md](local-debugging.md)：本地 9001 工单后端与 9100 知识推荐服务的联调方式。

## 第一阶段目标

把当前本地推荐原型包装成工单系统可调用的轻量服务：

```text
工单系统详情页
  ↓
POST /api/kb/recommend
  ↓
知识推荐服务
  ↓
返回 Top 3 工程师参考知识
```

第一阶段只需要：

- 加载 `data/kb-index.json`。
- 根据工单标题和描述推荐知识。
- 返回推荐原因。
- 记录工程师反馈。

暂不需要：

- 连接生产服务器。
- 调用业务系统接口。
- 接入大模型。
- 引入向量数据库。
