# 向量检索层

当前知识库已加入本地向量检索层，用于补充原有关键词规则推荐。

## 当前模型

模型名：

```text
local-char-ngram-hash-v1
```

它不是外部大模型 embedding，也不依赖网络或第三方服务。实现方式是：

1. 对知识文档和工单文本做中文字符 n-gram 切分。
2. 使用稳定哈希映射到固定维度稀疏向量。
3. 使用余弦相似度计算工单和知识文档的语义近似度。
4. 与原有规则分数合并排序。

当前维度：

```text
2048
```

索引文件：

```text
data/kb-vector-index.json
```

## 构建命令

先构建结构化知识索引：

```powershell
python scripts\build_kb_index.py
```

再构建向量索引：

```powershell
python scripts\build_kb_vector_index.py
```

启动推荐服务：

```powershell
python scripts\kb_http_service.py --host 127.0.0.1 --port 9100
```

健康检查会显示向量状态：

```http
GET http://127.0.0.1:9100/health
```

示例返回字段：

```json
{
  "vector_model": "local-char-ngram-hash-v1",
  "vector_documents": 51,
  "vector_dimensions": 2048
}
```

## 推荐模式

推荐接口支持三种模式：

```http
POST /api/kb/recommend
```

请求参数：

```json
{
  "title": "会议室投屏没有画面",
  "description": "无线投屏失败，大屏无信号",
  "mode": "hybrid",
  "top_k": 5
}
```

模式说明：

| mode | 说明 |
| --- | --- |
| `rules` | 只使用关键词、系统、标签、问题类型等规则打分 |
| `vector` | 只使用本地向量相似度 |
| `hybrid` | 规则分 + 向量分混合排序，默认模式 |

返回结果包含：

```json
{
  "score": 75,
  "rule_score": 60,
  "vector_score": 0.1988,
  "reason": [
    "问题描述关键词:会议室投屏",
    "语义相似度:0.20"
  ]
}
```

## 当前定位

当前向量层的目标是先补齐工程能力：

- 让推荐服务具备向量召回接口。
- 支持规则、向量、混合三种模式对比。
- 在不联网、不引入外部依赖的情况下验证流程。
- 为后续替换成真正 embedding 模型预留接口。

它不等同于大模型 embedding。对同义表达有一定帮助，但理解能力有限。

## 后续替换路径

后续如果接入正式 embedding 模型，只需要替换：

```text
scripts/vector_model.py
```

保留这些接口即可：

- `vectorize_text`
- `build_vector_records`
- `vector_search`

推荐服务、前端展示和反馈闭环可以继续沿用。

建议升级顺序：

1. 继续保留 `hybrid`，不要直接切到纯向量。
2. 用历史工单离线回测比较 `rules`、`vector`、`hybrid`。
3. 确认向量召回稳定后，再接入企业可控的 embedding 模型。
4. 使用工程师反馈调整混合排序权重。
