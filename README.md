# 运维知识库

本仓库用于沉淀软硬件运维知识，并为工单系统提供可检索、可推荐、可反馈的知识来源。

当前阶段的重点不是直接建设完整 AI 推荐系统，而是先把历史工单中的口语化处理记录整理成结构化知识，供工程师处理工单时快速参考。

## 当前数据来源

- 原始文件：`工单报修历史记录.csv`
- 字段：`工单号`、`问题描述`、`解决步骤`
- 数据量：2491 条
- 数据特点：有完整字段，但大量解决步骤较短，例如“已处理”“完成”“网络认证问题”，需要结合工程师经验持续补充。

## 知识状态

- `candidate`：由历史工单归纳生成，信息不足或暂不适合推荐。
- `usable`：已整理成工程师可参考的知识，可进入工单系统推荐。
- `verified`：系统负责人或专业工程师确认过，可高权重推荐。
- `deprecated`：已过期或不再适用。

工单系统联动时，默认可推荐 `usable` 和 `verified` 知识。`candidate` 只作为低权重参考或提示后续补全文档。

## 目录结构

```text
docs/
  candidate/desktop/     从历史工单整理出的桌面运维参考知识
  business/              业务系统和维护资料整理
templates/               文档模板
taxonomy/                标签、资产类型、问题类型规范
reports/                 数据分析和整理报告
```

## 工单系统集成

对接工单系统时，优先阅读：

- `docs/integration/api-contract.md`
- `docs/integration/data-flow.md`
- `docs/integration/feedback-loop.md`
- `docs/integration/deployment-options.md`

第一阶段建议把当前离线推荐逻辑包装成内网 HTTP 服务，由工单系统详情页调用 `/api/kb/recommend` 获取推荐知识，并通过 `/api/kb/feedback` 记录工程师反馈。

## 推荐落地流程

1. 每周导出已解决工单。
2. 按问题描述和解决步骤聚类。
3. 合并相似问题，生成工程师参考知识。
4. 补充风险点、验证方式和升级条件。
5. 标记为 `usable` 后接入工单系统推荐；关键系统可进一步确认为 `verified`。
6. 工单关闭时记录知识是否有用，并持续调整排序。

## 本地推荐原型

当前仓库已包含一个离线推荐原型，不连接服务器、接口或外部服务。

生成知识索引：

```powershell
python scripts\build_kb_index.py
```

使用历史工单离线回测：

```powershell
python scripts\recommend_from_ticket.py
```

主要输出：

- `data/kb-index.json`：从 Markdown 文档生成的结构化知识索引。
- `reports/recommendation-dry-run.csv`：每条历史工单的 Top 3 推荐结果。
- `reports/recommendation-summary.md`：命中率、Top 推荐知识和未命中高频词。
