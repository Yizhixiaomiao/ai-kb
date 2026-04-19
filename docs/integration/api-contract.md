# 知识推荐服务 API 契约

本文定义工单系统与知识推荐服务之间的接口契约。当前契约面向第一阶段规则推荐，底层数据来自 `data/kb-index.json`，不依赖向量库或大模型。

## 基本约定

- 数据格式：JSON。
- 字符集：UTF-8。
- 推荐对象：工程师处理工单时参考的知识文档。
- 推荐范围：默认返回 `status` 为 `verified` 或 `usable` 的知识。
- 排序原则：`verified` 优先于 `usable`；问题描述命中优先于处理记录命中；细分场景文档优先于大类汇总文档。

## 推荐接口

```http
POST /api/kb/recommend
```

### 请求字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ticket_id` | string | 是 | 工单编号 |
| `title` | string | 否 | 工单标题。若工单系统没有标题，可与 `description` 相同 |
| `description` | string | 是 | 用户报修描述或问题描述 |
| `resolution` | string | 否 | 已有处理记录。新工单推荐时通常为空，历史回测时可传 |
| `category` | string | 否 | 工单大类，例如桌面运维、安防、会议室、业务系统 |
| `business_system` | string | 否 | 业务系统，例如 MES、OA、PLM、SAP |
| `asset_type` | string | 否 | 资产类型，例如 pc、printer、network、security-device |
| `issue_type` | string | 否 | 问题类型，例如 login-failed、printer-not-working |
| `location` | string | 否 | 位置，例如车间、办公室、门岗、会议室 |
| `top_k` | integer | 否 | 返回数量，默认 3，建议最大 5 |

### 请求示例

```json
{
  "ticket_id": "51020111960",
  "title": "连接不上打印机",
  "description": "用户反馈连接不上共享打印机，换办公室后无法打印",
  "category": "桌面运维",
  "business_system": "",
  "asset_type": "printer",
  "issue_type": "printer-not-working",
  "location": "综合办公楼",
  "top_k": 3
}
```

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `request_id` | string | 本次推荐请求 ID |
| `ticket_id` | string | 工单编号 |
| `matched` | boolean | 是否有推荐结果 |
| `recommendations` | array | 推荐知识列表 |
| `fallback` | object | 无命中或低置信度时的补充建议 |

### 推荐项字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `doc_id` | string | 知识文档 ID |
| `title` | string | 知识标题 |
| `status` | string | `usable` 或 `verified` |
| `type` | string | 文档类型，例如 troubleshooting、sop |
| `score` | number | 推荐分数 |
| `confidence` | string | `high`、`medium`、`low` |
| `path` | string | Markdown 文档路径 |
| `asset_types` | array | 资产类型 |
| `systems` | array | 系统 / 软件 |
| `issue_types` | array | 问题类型 |
| `tags` | array | 标签 |
| `reason` | array | 推荐原因，必须可解释 |

### 响应示例

```json
{
  "request_id": "rec-20260417-000001",
  "ticket_id": "51020111960",
  "matched": true,
  "recommendations": [
    {
      "doc_id": "shared-printer-connect-failed",
      "title": "共享打印机连接失败",
      "status": "usable",
      "type": "troubleshooting",
      "score": 22,
      "confidence": "high",
      "path": "docs/candidate/desktop/printer/shared-printer-connect-failed.md",
      "asset_types": ["pc", "printer"],
      "systems": ["windows"],
      "issue_types": ["printer-not-working"],
      "tags": ["printer", "shared-printer", "windows"],
      "reason": [
        "问题描述关键词:连接不上打印机"
      ]
    }
  ],
  "fallback": {
    "need_clarification": false,
    "questions": []
  }
}
```

## 无命中响应

当没有任何推荐结果时，服务不应返回空白页面，而应返回可操作提示。

```json
{
  "request_id": "rec-20260417-000002",
  "ticket_id": "INC-001",
  "matched": false,
  "recommendations": [],
  "fallback": {
    "need_clarification": true,
    "questions": [
      "请补充故障对象：电脑、打印机、业务系统、网络、安防设备或会议室设备。",
      "请补充具体现象，例如无法登录、无法打印、无信号、离线、卡纸、黑屏。"
    ],
    "suggested_action": "记录为未命中工单，后续用于补充知识库。"
  }
}
```

## 反馈接口

```http
POST /api/kb/feedback
```

### 请求字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ticket_id` | string | 是 | 工单编号 |
| `request_id` | string | 否 | 推荐请求 ID |
| `doc_id` | string | 是 | 被反馈的知识 ID |
| `action` | string | 是 | `viewed`、`accepted`、`rejected`、`copied`、`linked` |
| `helpful` | boolean | 否 | 工程师是否认为有用 |
| `resolved` | boolean | 否 | 是否帮助解决工单 |
| `engineer_id` | string | 否 | 工程师标识 |
| `comment` | string | 否 | 反馈说明 |

### 请求示例

```json
{
  "ticket_id": "51020111960",
  "request_id": "rec-20260417-000001",
  "doc_id": "shared-printer-connect-failed",
  "action": "accepted",
  "helpful": true,
  "resolved": true,
  "engineer_id": "ops001",
  "comment": "推荐准确，重新连接共享打印机后恢复。"
}
```

### 响应示例

```json
{
  "saved": true,
  "feedback_id": "fb-20260417-000001"
}
```

## 知识索引刷新接口

第一阶段可以不提供线上刷新接口，由定时任务或人工执行脚本生成 `data/kb-index.json`。

如后续需要服务端刷新，可定义：

```http
POST /api/kb/admin/reload-index
```

建议该接口只允许管理员或部署流水线调用。

## 错误码

| HTTP 状态 | code | 说明 |
| --- | --- | --- |
| 400 | `INVALID_REQUEST` | 请求字段缺失或格式错误 |
| 404 | `DOC_NOT_FOUND` | 反馈的文档 ID 不存在 |
| 422 | `EMPTY_DESCRIPTION` | 问题描述为空，无法推荐 |
| 500 | `INTERNAL_ERROR` | 服务内部错误 |
| 503 | `INDEX_NOT_READY` | 知识索引未加载 |

