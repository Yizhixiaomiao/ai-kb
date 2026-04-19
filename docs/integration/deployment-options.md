# 知识推荐服务部署选项

本文给出从本地脚本到正式服务的分阶段部署建议。

## 阶段 0：本地离线原型

当前状态。

```text
Markdown 知识
  ↓
build_kb_index.py
  ↓
kb-index.json
  ↓
recommend_from_ticket.py
  ↓
dry-run 报告
```

适合：

- 验证知识结构。
- 验证关键词和规则。
- 用历史工单回测。

不适合：

- 被工单系统实时调用。
- 记录工程师反馈。

## 阶段 1：轻量 HTTP 服务

推荐方案。

```text
工单系统
  ↓ HTTP
知识推荐服务
  ↓
kb-index.json
```

技术可选：

- Python FastAPI
- Flask
- .NET Web API
- Java Spring Boot

第一阶段建议 FastAPI 或现有团队熟悉的后端框架。

核心能力：

- 启动时加载 `data/kb-index.json`。
- 提供 `/api/kb/recommend`。
- 提供 `/api/kb/feedback`。
- 本地文件或数据库记录反馈。

## 阶段 2：接入数据库

当推荐日志和反馈需要长期分析时，接入数据库。

建议表：

- `kb_documents`
- `kb_recommendation_log`
- `kb_feedback`
- `kb_unmatched_ticket`

知识正文仍可继续使用 Markdown + Git 管理，数据库只存索引、日志和反馈。

## 阶段 3：混合检索

当关键词规则覆盖不足时，再引入：

- Elasticsearch / OpenSearch BM25
- PostgreSQL `pg_trgm`
- 向量检索
- Rerank 模型

不建议在知识质量和反馈闭环未稳定前直接上复杂 AI。

## 阶段 4：RAG 助手

在检索结果稳定后，再接入大模型生成排查建议。

大模型只做：

- 总结推荐知识。
- 组织排查步骤。
- 提取相似历史工单经验。
- 生成候选知识草稿。

不建议让大模型直接决定生产操作。

## 部署建议

第一阶段服务可以部署在内网应用服务器：

```text
端口：由内部规范确定
访问方：工单系统后端
数据源：本地 kb-index.json
日志：推荐日志和反馈日志
权限：仅工单系统调用
```

## 发布流程

建议流程：

1. 修改 Markdown 知识。
2. 执行 `python scripts\build_kb_index.py`。
3. 执行 `python scripts\recommend_from_ticket.py` 做回测。
4. 检查 `reports/recommendation-summary.md`。
5. 发布新的 `kb-index.json`。
6. 推荐服务 reload 索引。

## 风险与控制

| 风险 | 控制方式 |
| --- | --- |
| 推荐错误 | 展示推荐原因，允许工程师反馈 |
| 知识过期 | 使用 `status`、`updated_at` 和定期治理 |
| 敏感信息泄露 | 索引不存密码、Token、账号 |
| 低质量工单影响推荐 | 强化工单字段和描述规范 |
| 规则过拟合历史数据 | 保留人工抽样和反馈闭环 |

