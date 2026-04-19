# 工单知识推荐数据流

本文描述从 Markdown 知识库到工单系统推荐结果的完整数据流。

## 离线知识构建流

```text
Markdown 知识文档
  ↓
scripts/build_kb_index.py
  ↓
data/kb-index.json
  ↓
知识推荐服务启动时加载
```

当前索引字段包括：

- `doc_id`
- `title`
- `status`
- `type`
- `asset_types`
- `systems`
- `issue_types`
- `tags`
- `keywords`
- `path`
- `content_preview`

## 在线推荐流

```text
工单系统
  ↓ POST /api/kb/recommend
知识推荐服务
  ↓ 加载 data/kb-index.json
规则匹配与排序
  ↓
返回 Top K 知识、分数、原因
  ↓
工单详情页展示推荐
```

## 推荐排序逻辑

第一阶段使用可解释规则：

1. 工单 `description` 命中关键词，权重最高。
2. 工单 `resolution` 命中关键词，作为辅助权重。
3. 命中 `systems`、`tags`、`issue_types`、`asset_types` 时加权。
4. `verified` 文档高于 `usable` 文档。
5. 细分文档优先于大类文档。

注意：历史工单回测可以使用 `resolution`，新工单实时推荐通常没有处理记录，因此主要依赖 `title` 和 `description`。

## 工单详情页展示建议

推荐区建议展示：

- 知识标题
- 文档状态：`usable` / `verified`
- 推荐分数和置信度
- 推荐原因
- 文档入口
- 反馈按钮：有用、无用、采纳、关联到工单

示例：

```text
推荐知识：共享打印机连接失败
状态：usable
推荐原因：问题描述命中“连接不上打印机”
操作：查看 / 采纳 / 无用
```

## 数据更新频率

建议第一阶段采用人工或定时构建：

```powershell
python scripts\build_kb_index.py
```

推荐频率：

- 知识文档有变更时手动执行。
- 每天定时执行一次。
- 后续接入 Git 或发布流水线后自动执行。

## 敏感信息处理

知识索引不应包含：

- 密码、Token、密钥。
- 服务器登录地址和账号。
- 数据库连接信息。
- 堡垒机、备份、存储等高权限系统凭据。

Markdown 文档中如需引用敏感资料，只记录受控资料位置和负责人，不写明文。

## 数据落库建议

第一阶段可以只使用文件：

- `data/kb-index.json`
- `reports/recommendation-dry-run.csv`
- 反馈日志文件或数据库表

正式接入后建议落库：

```text
kb_documents
kb_recommendation_log
kb_feedback
kb_unmatched_ticket
```

