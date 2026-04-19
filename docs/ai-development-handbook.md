# 运维知识库 AI 开发手册与准则

本文面向后续参与本项目的其他大模型、编码助手或工程师。目标是让接手者先理解项目定位、数据边界、推荐链路和开发约束，再进行代码修改。

## 项目定位

本项目是企业软硬件运维知识库与工单系统联动原型，当前重点不是替代工程师自动处置工单，而是为工程师在处理工单时提供可追溯、可解释、可反馈的知识推荐。

当前知识来源包括：

- 历史工单清洗结果。
- 手工整理的 Markdown 知识文档。
- 安防、会议室、打印机、桌面软件、业务系统等分类知识。
- 后续可接入工单系统数据库中的正式知识库。

当前推荐结果应该被视为“工程师参考资料”，不是自动执行方案。

## 核心原则

1. 先保证知识可信，再追求智能生成。
2. 推荐必须尽量可解释，不能只给一个黑盒相似度。
3. 大模型优先用于知识整理、结构化、去重和质量评估，不应直接替代人工做高风险运维决策。
4. 对服务器、数据库、网络、安全设备等高风险场景，只给排查建议和来源知识，不主动生成破坏性操作命令。
5. 不连接生产服务器，不调用未授权接口，不做真实业务测试。
6. 不把账号、密码、Token、手机号、内网 IP、服务器名等敏感信息写入知识文档。
7. 不把低质量工单直接发布为正式知识，应先进入候选或待复核状态。

## 目录职责

```text
docs/
  candidate/              候选或已整理的知识文档
  business/               业务系统相关资料
  integration/            与工单系统、推荐服务、向量检索相关的设计文档

scripts/
  build_kb_index.py       从 Markdown 文档构建结构化知识索引
  build_kb_vector_index.py 构建本地向量索引
  vector_model.py         本地向量模型实现
  recommend_from_ticket.py 离线推荐与回测逻辑
  kb_http_service.py      本地 HTTP 推荐服务

data/
  kb-index.json           结构化知识索引
  kb-vector-index.json    本地向量索引
  kb-feedback.jsonl       工程师反馈日志

reports/
  recommendation-*.csv/md 离线回测和分析报告

templates/
  知识文档模板

taxonomy/
  标签、资产类型、问题类型规范
```

## 知识文档标准

知识文档必须优先使用 Markdown，并包含 YAML 元数据块。推荐结构如下：

```markdown
# 知识标题

```yaml
status: usable
type: troubleshooting
asset_types: [printer]
systems: [windows]
issue_types: [offline, print-failed]
tags: [printer, queue, driver]
```

## 适用范围

说明适用于什么系统、设备、场景。

## 常见现象

- 用户看到的现象。
- 系统提示。
- 影响范围。

## 判断依据

- 如何判断属于该类问题。
- 哪些情况不适用。

## 处理步骤

1. 先做低风险检查。
2. 再做配置或服务层操作。
3. 必要时升级给对应工程师。

## 验证方式

- 如何确认问题已经解决。

## 注意事项

- 风险点。
- 不允许执行的动作。
- 升级条件。
```

状态定义：

| 状态 | 含义 |
| --- | --- |
| `candidate` | 候选知识，可能来自工单沉淀，未充分整理 |
| `usable` | 工程师可参考使用 |
| `verified` | 已由专业人员确认，可高权重推荐 |
| `deprecated` | 过期或不再适用，不应推荐 |

## 推荐链路

当前推荐链路如下：

```text
Markdown 知识文档
  -> scripts/build_kb_index.py
  -> data/kb-index.json
  -> scripts/build_kb_vector_index.py
  -> data/kb-vector-index.json
  -> scripts/kb_http_service.py
  -> /api/kb/recommend
  -> 工单详情页推荐卡片
  -> /api/kb/feedback
```

推荐服务支持三种模式：

| mode | 说明 |
| --- | --- |
| `rules` | 只使用关键词、标签、系统、问题类型等规则打分 |
| `vector` | 只使用本地向量相似度 |
| `hybrid` | 规则分 + 向量分混合排序，当前默认模式 |

返回结果应包含：

- `score`：综合分。
- `rule_score`：规则分。
- `vector_score`：向量相似度。
- `reason`：命中原因。
- `steps`：处理步骤。
- `verification`：验证方式。
- `path`：来源文档路径。

不要移除 `reason`、`steps`、`path` 等可解释字段。

## 当前向量模型定位

当前向量模型是本地轻量实现：

```text
local-char-ngram-hash-v1
```

它使用中文字符 n-gram + 稳定哈希生成稀疏向量，不是外部 embedding 模型。

它的作用是：

- 先搭好向量召回接口。
- 支持 `rules / vector / hybrid` 对比。
- 在不联网、不引入外部依赖的情况下验证流程。
- 为后续替换正式 embedding 模型预留接口。

不要把当前向量模型描述成“大模型语义理解”。它只是轻量本地相似度模型。

后续替换正式 embedding 时，优先保持以下接口稳定：

- `vectorize_text`
- `build_vector_records`
- `vector_search`

## 与工单系统的关系

当前已联动 `D:\Workspace\wh-ops-alert` 前端：

- 新增 API 封装：`WatchAlert-web/src/api/ops_kb.jsx`
- 工单详情页：`WatchAlert-web/src/pages/ticket/detail.jsx`

前端推荐卡片只读展示知识，不应自动执行处理动作。

当前联调方式：

- 工单系统后端：`http://127.0.0.1:9001`
- 工单系统前端：`http://127.0.0.1:3000`
- 知识推荐服务：`http://127.0.0.1:9100`

前端直连推荐服务是本地联调方案。正式环境更推荐由工单系统后端代理，统一鉴权、审计、租户隔离和服务地址配置。

## 开发命令

构建结构化索引：

```powershell
python scripts\build_kb_index.py
```

构建向量索引：

```powershell
python scripts\build_kb_vector_index.py
```

离线回测：

```powershell
python scripts\recommend_from_ticket.py --mode hybrid
```

启动推荐服务：

```powershell
python scripts\kb_http_service.py --host 127.0.0.1 --port 9100
```

健康检查：

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:9100/health
```

推荐接口示例：

```powershell
$body = @{
  ticket_id = "debug-001"
  title = "会议室投屏没有画面"
  description = "无线投屏失败，大屏无信号"
  mode = "hybrid"
  top_k = 5
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:9100/api/kb/recommend `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## 修改推荐算法的准则

可以做：

- 增加同义词、负向关键词、领域权重。
- 增加知识质量分、反馈分、时效分。
- 调整 `rules / vector / hybrid` 的加权逻辑。
- 增加离线回测报告字段。
- 增加候选知识去重和相似知识合并建议。

不要做：

- 删除规则推荐，只保留纯向量。
- 删除推荐原因。
- 删除处理步骤展示。
- 将 `candidate` 知识无差别高权重推荐。
- 为了提高命中率合并过粗分类，例如把所有打印问题都合并成“打印机问题”。
- 在没有验证的情况下把模型生成内容标记为 `verified`。

## 使用大模型的准则

适合大模型做的事：

- 从工单记录中抽取故障对象、现象、原因、动作、验证结果。
- 把口语化处理步骤整理成标准知识格式。
- 判断工单是否值得沉淀。
- 发现重复知识或建议合并。
- 给知识文档做质量评分。
- 根据已有知识生成“受控建议”。

不适合大模型直接做的事：

- 编造内部系统流程。
- 编造服务器、账号、路径、审批人。
- 生成高风险执行命令并直接交给一线执行。
- 在没有来源知识的情况下输出确定性结论。
- 替代工程师确认数据库、网络、安全设备变更。

大模型生成的回答必须区分：

```text
内部知识依据
通用补充建议
需要人工确认的信息
高风险操作提示
```

## 知识治理方向

下一阶段优先做知识运营层，而不是单纯堆知识数量。

建议模块：

1. 知识质量评分：结构完整度、复用次数、反馈质量、时效性。
2. 值得沉淀识别：高频、超时、无命中、关键系统问题。
3. 去重和合并建议：新知识入库前先查相似知识。
4. 反馈学习：有用、无用、已参考、最终是否解决。
5. 缺口分析：高频但无有效知识的问题。
6. 工时联动：标准工时、历史平均、超时风险和知识缺口关联。

## 安全边界

后续开发必须遵守：

- 不主动连接任何生产服务器。
- 不主动调用真实业务写接口。
- 不在代码或文档中保存密钥、Token、密码。
- 不把敏感工单原文直接写进公开知识文档。
- 不对用户未授权的目录做批量修改。
- 不清理或覆盖不是当前任务产生的改动。

## 给后续 AI 助手的工作方式

接手任务时应先做：

1. 阅读本手册。
2. 阅读 `docs/integration/vector-retrieval.md`。
3. 阅读 `docs/integration/wh-ops-alert-interface-map.md`。
4. 确认当前服务端口和进程状态。
5. 查看 git 状态，区分已有改动和本次改动。

修改代码后至少做：

1. 运行 Python 编译检查：

```powershell
python -m py_compile scripts\vector_model.py scripts\build_kb_vector_index.py scripts\recommend_from_ticket.py scripts\kb_http_service.py scripts\build_kb_index.py
```

2. 重建索引：

```powershell
python scripts\build_kb_index.py
python scripts\build_kb_vector_index.py
```

3. 用一个样例请求验证推荐接口。

4. 如果修改前端，确认 `http://127.0.0.1:3000` 仍可访问。

## 当前已知限制

- 当前知识主要来自历史工单和手工 Markdown，覆盖范围仍不完整。
- 当前向量模型不是正式 embedding，语义理解能力有限。
- 当前前端直连 `9100` 是本地联调方案，生产环境需要后端代理。
- 当前反馈只落本地 `kb-feedback.jsonl`，尚未进入工单系统数据库。
- 当前推荐排序还没有使用工时标准、知识质量分和反馈学习。

后续优化应围绕“知识质量、反馈闭环、缺口分析、正式 embedding 替换、后端统一代理”推进。
