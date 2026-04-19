# 工单系统知识推荐 MVP

本文件保留第一阶段推荐思路。正式对接工单系统时，以以下文档为准：

- [integration/api-contract.md](integration/api-contract.md)
- [integration/data-flow.md](integration/data-flow.md)
- [integration/feedback-loop.md](integration/feedback-loop.md)
- [integration/deployment-options.md](integration/deployment-options.md)

## 目标

在工单详情页根据当前工单内容自动推荐相关知识，减少工程师手动查找和重复处理。

## 第一阶段推荐策略

先使用低成本、可解释的规则和关键词推荐，不直接依赖大模型。

输入字段：

- 工单号
- 问题描述
- 解决步骤
- 资产类型
- 系统 / 软件
- 问题类型

推荐逻辑：

1. 从工单标题和描述中提取关键词。
2. 匹配知识文档的 `asset_types`、`systems`、`issue_types` 和 `tags`。
3. 优先推荐 `status: verified` 的文档，其次推荐 `status: usable` 的文档。
4. 无 verified / usable 命中时，显示 candidate 文档并标注“信息待补全”。
5. 记录工程师是否采纳推荐。

细分类要求：

- 优先推荐细场景文档，不优先推荐“大类汇总文档”。
- 对“打印机无法打印”“CAD 异常”“无法联网”这类泛化描述，应先根据关键词或追问拆到具体场景。
- 如果只命中大类，应返回多个候选场景，让工程师选择。

## 推荐 API 草案

```http
POST /api/kb/recommend
```

请求示例：

```json
{
  "ticket_id": "51021860098",
  "title": "没网，mes登不上",
  "description": "轻型车间北二跨 K17 柱子，MES 无法登录",
  "asset_type": "pc",
  "system": "mes",
  "issue_type": "network-unavailable"
}
```

响应示例：

```json
{
  "recommendations": [
    {
      "doc_id": "network-authentication-unavailable",
      "title": "网络认证或 MES 无法访问处理指南",
      "status": "usable",
      "score": 0.86,
      "reason": [
        "命中关键词：没网、MES",
        "匹配系统：mes",
        "匹配问题类型：network-unavailable"
      ]
    }
  ]
}
```

## 工单关闭时反馈

建议新增以下反馈字段：

- 是否推荐了知识
- 工程师是否采纳
- 采纳的知识 ID
- 推荐是否有效
- 是否需要生成新知识
- 是否需要更新旧知识

这些反馈后续可用于排序：

- 被采纳次数多的文档加权。
- 同系统、同资产、同问题类型的历史有效文档加权。
- 多次标记无用的文档降权。
- 长期未补全的 candidate 文档降权。
