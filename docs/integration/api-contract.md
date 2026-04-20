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

## 知识块检索接口

文档级推荐用于回答“应该看哪篇知识”。知识块检索用于回答“当前问题最相关的步骤、指令、验证方式是哪几条”。

```http
POST /api/kb/search
```

### 请求示例

```json
{
  "ticket_id": "INC-CPU-001",
  "title": "CPU使用率达到95%",
  "description": "WMS业务机器CPU使用率持续告警",
  "mode": "hybrid",
  "top_k": 8
}
```

### 响应要点

- `chunks`：召回的知识块列表。
- `chunk_id`：知识块 ID，格式为 `doc_id#type-序号`。
- `type`：`overview`、`step`、`command`、`verification`、`note`。
- `score`：综合分。
- `rule_score`：规则分。
- `vector_score`：本地向量相似度。
- `content`：可直接展示给工程师的步骤、指令或说明。
- `command`、`purpose`、`risk`：当 `type=command` 时返回。

## 智能答案接口

当前版本不调用外部大模型，先基于知识块召回结果组装“处理建议”。后续接大模型时，应只允许模型基于 `retrieved_chunks` 和 `sources` 生成答案，不允许凭空补充生产操作。

```http
POST /api/kb/answer
```

### 请求示例

```json
{
  "ticket_id": "INC-BOOT-001",
  "title": "无法开机",
  "description": "用户反馈工位电脑按电源键后无法正常启动",
  "mode": "hybrid",
  "top_k": 12
}
```

### 响应结构

```json
{
  "matched": true,
  "answer": {
    "summary": "优先参考《电脑无法开机或不通电处理指南》中的适用范围与现象。",
    "suggested_steps": ["检查插座、电源线、插排和主机电源开关。"],
    "commands": [
      {
        "command": "eventvwr.msc",
        "purpose": "打开事件查看器，检查系统、应用和驱动错误。",
        "risk": "低",
        "source": "pc-boot-failed"
      }
    ],
    "verification": ["电脑能正常进入 Windows 桌面。"],
    "cautions": [],
    "sources": [
      {
        "doc_id": "pc-boot-failed",
        "title": "电脑无法开机或不通电处理指南",
        "path": "docs/candidate/desktop/pc-boot-failed.md"
      }
    ],
    "retrieved_chunks": []
  }
}
```

### 索引生成顺序

```powershell
python scripts\build_kb_index.py
python scripts\build_kb_vector_index.py
python scripts\build_kb_chunks.py
python scripts\build_kb_chunk_vector_index.py
```

服务运行时会优先读取：

- `data/kb-index.json`
- `data/kb-vector-index.json`
- `data/kb-chunks.json`
- `data/kb-chunk-vector-index.json`

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

## 工单经验沉淀接口

该接口用于工单系统在工程师关单后同步原始处理经验。同步内容不会直接进入正式知识库；系统会先做质量判断、匹配已有知识，并在必要时生成候选草稿。

```http
POST /api/kb/experience
```

### 请求示例

```json
{
  "ticket_id": "INC-20260420-001",
  "title": "打印机显示脱机无法打印",
  "description": "用户反馈共享打印机显示脱机，无法提交打印任务",
  "resolution": "取消脱机，清理打印队列，重启 Print Spooler 服务后恢复",
  "category": "printer",
  "engineer_id": "ops001",
  "closed_at": "2026-04-20 10:30:00"
}
```

### 响应动作

- `need_more_detail`：记录过于简单，只进入经验池，不生成候选知识。
- `attach_to_existing`：匹配到已有知识，作为该知识的案例素材和后续关键词来源。
- `create_candidate`：质量达到要求但未匹配到已有知识，生成候选草稿，等待人工复核。

### 响应示例

```json
{
  "saved": true,
  "quality": "medium",
  "quality_score": 6,
  "action": "attach_to_existing",
  "matched_doc": {
    "doc_id": "printer-offline-or-paused",
    "title": "打印机脱机或暂停处理指南",
    "score": 42
  },
  "missing_fields": [],
  "suggested_questions": [],
  "suggested_candidate": null
}
```

低质量记录示例：

```json
{
  "saved": true,
  "quality": "low",
  "action": "need_more_detail",
  "missing_fields": ["具体处理动作", "验证结果"],
  "suggested_questions": [
    "实际执行了什么操作、命令、配置修改或替换动作？",
    "如何确认问题已经恢复，是否有验证截图、日志或业务操作结果？"
  ]
}
```

查看最近经验和候选草稿：

```http
GET /api/kb/experiences
GET /api/kb/candidates
```

数据落地位置：

- `data/ticket-experiences.jsonl`
- `data/kb-candidates.json`

## 正式文档导入

工程师已经整理好的正式文档不走经验池，也不要求先改成标准知识模板。导入流程会将 `.docx`、`.xlsx`、`.txt`、`.md` 转成 `docs/source-documents/` 下的 Markdown，并标记为：

```yaml
status: imported
type: reference
source: engineer-doc
```

导入命令：

```powershell
python scripts\import_source_documents.py --source "D:\新建文件夹\业务维护清单"
python scripts\build_kb_index.py
python scripts\build_kb_vector_index.py
python scripts\build_kb_chunks.py
python scripts\build_kb_chunk_vector_index.py
```

导入策略：

- 导入 `.docx`、`.xlsx`、`.txt`、`.md`。
- 跳过安装包、压缩包、镜像、图片、PDF 等二进制或重复资料。
- 跳过文件名疑似账号密码、访问清单、服务器 IP 清单的资料。
- 对正文中的 IP、手机号、密码、Token、Secret 做脱敏。
- 正式文档作为 `imported/reference` 参与检索，但不等同于标准 SOP。

导入报告：

```text
reports/source-document-import-report.md
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
