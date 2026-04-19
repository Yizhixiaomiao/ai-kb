# 推荐反馈闭环

知识推荐系统要长期有效，必须记录工程师的真实使用反馈。没有反馈闭环，推荐结果无法持续排序和优化。

## 需要记录的行为

| 行为 | 含义 | 用途 |
| --- | --- | --- |
| `viewed` | 工程师查看了推荐知识 | 判断曝光量 |
| `accepted` | 工程师采纳该知识 | 提升排序权重 |
| `rejected` | 工程师认为不相关 | 降低排序权重 |
| `linked` | 工程师将知识关联到工单 | 形成工单-知识关系 |
| `resolved` | 知识帮助解决工单 | 作为高价值正反馈 |

## 推荐反馈表

建议表结构：

```sql
CREATE TABLE kb_feedback (
  id BIGINT PRIMARY KEY,
  ticket_id VARCHAR(64) NOT NULL,
  request_id VARCHAR(64),
  doc_id VARCHAR(128) NOT NULL,
  action VARCHAR(32) NOT NULL,
  helpful BOOLEAN,
  resolved BOOLEAN,
  engineer_id VARCHAR(64),
  comment TEXT,
  created_at TIMESTAMP NOT NULL
);
```

## 推荐日志表

建议记录每次推荐请求，便于复盘。

```sql
CREATE TABLE kb_recommendation_log (
  id BIGINT PRIMARY KEY,
  request_id VARCHAR(64) NOT NULL,
  ticket_id VARCHAR(64) NOT NULL,
  request_text TEXT NOT NULL,
  recommended_docs JSON NOT NULL,
  matched BOOLEAN NOT NULL,
  created_at TIMESTAMP NOT NULL
);
```

## 未命中工单表

无命中或低置信度工单应进入待分析池。

```sql
CREATE TABLE kb_unmatched_ticket (
  id BIGINT PRIMARY KEY,
  ticket_id VARCHAR(64) NOT NULL,
  title TEXT,
  description TEXT,
  category VARCHAR(64),
  business_system VARCHAR(64),
  asset_type VARCHAR(64),
  issue_type VARCHAR(64),
  status VARCHAR(32) NOT NULL,
  created_at TIMESTAMP NOT NULL
);
```

## 排序权重建议

可以先使用简单权重：

| 信号 | 权重 |
| --- | ---: |
| `accepted` | +5 |
| `resolved=true` | +8 |
| `linked` | +3 |
| `viewed` | +1 |
| `rejected` | -5 |
| 多次无用 | 降权或进入复查 |

同系统、同资产、同问题类型的历史采纳结果应优先用于同类工单。

## 工单关闭时的动作

工单关闭时建议弹出或嵌入简短反馈：

```text
本次推荐是否有用？
- 有用，已采纳
- 有用，但需要补充
- 无用
- 没有合适知识
```

如果工程师填写了新的解决方案，可以提示：

```text
是否生成候选知识？
```

生成候选知识时，不要直接发布为 `usable`，先进入 `candidate` 或人工整理队列。

## 周期性治理

建议每周生成治理报告：

- 无命中 Top 关键词。
- 被采纳最多的知识。
- 被拒绝最多的知识。
- 长期无人使用的知识。
- 有用但缺步骤的知识。
- 需要新增的知识主题。

