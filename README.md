# 运维知识库

本仓库用于沉淀企业软硬件运维知识，并为工单系统提供可检索、可推荐、可反馈、可持续沉淀的知识来源。

当前项目已经从“Markdown 知识整理”推进到“轻量 RAG 原型”：知识来源包括历史工单、工程师正式文档、服务器告警规则、软件目录和人工维护的 Markdown 文档。工单系统可以通过 HTTP 接口获取推荐知识，工程师也可以在处理工单后把经验沉淀为候选知识。当前服务还额外提供 OpenAI 风格兼容接口，可直接把知识库当作“AI 服务”接入现有工单系统。

## 当前能力

- Markdown 知识库：桌面运维、打印机、网络、安全、安防、会议室、服务器和业务系统等知识。
- 正式文档入库：可将工程师已有文档转换为可检索知识块，保留原文来源。
- 告警规则入库：服务器类问题可用告警规则名称作为检索输入，例如 CPU、内存、磁盘、业务可用性和备份失败。
- 软件目录入库：只把软件名称、路径和下载入口作为参考知识，不关心压缩包、镜像等具体文件格式。
- 混合检索：规则关键词、同义词扩展、向量相似度和分块检索共同参与召回。
- 工单系统联动：提供推荐、RAG 组装、反馈、经验沉淀和候选知识入口。
- AI 兼容接口：提供 `GET /v1/models` 与 `POST /v1/chat/completions`，可按大模型接口方式接入。
- AI 服务配置页：可在 `/ui/` 中手动维护端口、URL、模型名称、接口路径和 API Key 默认值。
- 评测脚本：支持模拟工单评测、真实工单评测和历史工单同义词覆盖分析。

## 目录结构

```text
data/                  构建后的知识索引、分块索引和向量索引
docs/                  Markdown 知识库和集成文档
docs/business/         业务维护清单和正式文档转换结果
docs/candidate/        待确认或可参考的运维知识
docs/integration/      与工单系统联动的接口、流程和部署说明
reports/               推荐评测、模拟评测和同义词分析报告
scripts/               构建、导入、检索、评测和 HTTP 服务脚本
taxonomy/              分类、标签、同义词和知识库规范
templates/             知识库文档模板
web/                   本地知识库前端页面
```

## 快速运行

在仓库根目录执行：

```powershell
python scripts\kb_http_service.py --host 127.0.0.1 --port 9100
```

启动后访问：

```text
http://127.0.0.1:9100/ui/
```

常用接口：

```text
GET  /health
POST /api/kb/recommend
POST /api/kb/answer
POST /api/kb/feedback
POST /api/kb/experience
GET  /api/kb/candidates
GET  /v1/models
POST /v1/chat/completions
```

工单系统本地联调说明见：

- `docs/integration/api-contract.md`
- `docs/integration/data-flow.md`
- `docs/integration/feedback-loop.md`
- `docs/integration/local-debugging.md`

## AI 接口接入

如果你的工单系统当前已经是通过“大模型接口”获取处理建议，可以直接把本服务当成 AI 服务接入。

默认模型：

```text
ops-kb-rag
```

OpenAI 风格接口：

```text
GET  /v1/models
POST /v1/chat/completions
```

鉴权方式：

```text
Authorization: Bearer <api_key>
```

或：

```text
x-api-key: <api_key>
```

最小请求示例：

```json
{
  "model": "ops-kb-rag",
  "messages": [
    {
      "role": "user",
      "content": "工单标题：CPU使用率达到95%\n工单描述：WMS业务机器CPU使用率持续告警"
    }
  ]
}
```

工单系统通常直接取：

```text
choices[0].message.content
```

如果需要结构化展示，可读取：

```text
kb_answer
```

其中包含 `suggested_steps`、`commands`、`verification`、`cautions`、`sources`。

## AI 服务配置

工作台已内置“AI服务配置”页面：

```text
/ui/
```

可在页面中维护以下默认配置：

- 服务名称
- 模型名称
- 监听主机
- 监听端口
- 服务 URL
- API Key
- 模型列表接口路径
- 对话补全接口路径
- 健康检查接口路径

说明：

- `api_key` 保存后对 AI 兼容接口立即生效。
- `port` 保存后只会写入配置，需重启服务后才会实际改监听端口。
- 实际运行配置保存在 `data/ai-service-config.json`，该文件默认不提交到仓库。

## 构建索引

修改 Markdown、导入文档、调整同义词或更新软件目录后，需要重建索引：

```powershell
python scripts\build_kb_index.py
python scripts\build_kb_chunks.py
python scripts\build_kb_vector_index.py
python scripts\build_kb_chunk_vector_index.py
```

主要输出：

```text
data/kb-index.json
data/kb-chunks.json
data/kb-vector-index.json
data/kb-chunk-vector-index.json
```

## 检索逻辑

当前不是简单的 Markdown 字符串匹配，而是分层召回：

1. 输入清洗：去除无关字段、设备编号、过长位置和低价值描述。
2. 同义词扩展：使用 `taxonomy/query-synonyms.json` 补齐口语词、错别字、简称和标准表达。
3. 规则检索：基于标题、适用范围、标签、症状、步骤和命令打分。
4. 向量检索：使用本地向量模型计算语义相似度。
5. 分块检索：把长文档和正式文档拆成知识块，避免整篇文档召回不准。
6. RAG 组装：将命中的知识块、处理步骤、命令和注意事项组装成工程师可参考答案。

软件目录有独立意图判断：只有用户明显询问下载、安装包、驱动、客户端、升级包或路径时，软件目录才会被加权，避免故障类工单被软件下载链接误召回。

## 知识沉淀

知识来源分为三类：

- 人工维护 Markdown：适合稳定流程、标准操作、常见故障和高频问题。
- 正式工程师文档：适合直接作为检索内容入库，必要时再整理成标准知识。
- 工单处理经验：适合从工单关闭记录中提取候选知识，再由工程师确认是否转正。

工单处理经验不要求工程师一开始就写得很完整。系统会先做质量判断：过短、只有“已处理”、没有故障现象或没有处理动作的记录进入低质量经验；信息足够的记录进入候选知识，后续再由工程师补充适用范围、步骤、验证方式和风险点。

## 同义词补强

同义词维护在：

```text
taxonomy/query-synonyms.json
```

该文件覆盖历史工单中的口语表达，例如“联不上网”“重做系统”“清灰”“打印机换电脑”“掉加密”“业务可用性<95”“networekr 备份失败”等。

从历史工单分析同义词覆盖情况：

```powershell
python scripts\extract_ticket_synonym_candidates.py
```

输出报告：

```text
reports/ticket-synonym-candidates.md
```

## 评测

模拟 1000 条桌面、服务器告警和软件类工单：

```powershell
python scripts\simulate_kb_eval.py
```

使用真实工单列表评测：

```powershell
python scripts\evaluate_real_tickets.py --mode rules
```

真实工单接口拉取脚本：

```powershell
python scripts\fetch_ticket_list.py --size 100 --max-pages 200
```

真实工单数据可能包含内部系统信息、联系人、位置和处理记录，默认通过 `.gitignore` 排除，不应提交到远程仓库。

## 数据安全

以下内容不应提交：

- 原始工单 CSV
- 从生产接口拉取的真实工单 JSON
- 真实工单详细评测报告
- token、cookie、账号、密码和内部接口凭据
- 临时缓存、日志和 `__pycache__`

正式文档和知识库 Markdown 入库前，应去除账号密码、内网敏感地址和不可公开的客户信息。

## 分支

主分支为：

```text
main
```

历史 `master` 分支不再使用。
