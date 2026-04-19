# wh-ops-alert 接口映射

更新时间：2026-04-17

## 本地服务

- 工单系统后端：`http://127.0.0.1:9001`
- 知识库推荐服务：`http://127.0.0.1:9100`

已验证：

- `GET http://127.0.0.1:9001/hello` 返回 `200`
- `GET http://127.0.0.1:9001/api/w8t/ticket/list` 未带登录态时返回 `401`
- `GET http://127.0.0.1:9001/api/w8t/knowledge/list` 未带登录态时返回 `401`
- `GET http://127.0.0.1:9100/health` 返回 `200`
- `POST http://127.0.0.1:9100/api/kb/recommend` 可返回推荐知识

## 后端路由入口

源码位置：

- `D:\Workspace\wh-ops-alert\WatchAlert\internal\routers\v1\api.go`
- `D:\Workspace\wh-ops-alert\WatchAlert\internal\routers\health.go`

后端使用 Gin。业务 API 挂在：

- `/api/system`
- `/api/w8t`
- `/api/oidc`
- `/ws`

工单与知识库相关控制器已注册在 `/api/w8t`：

- `api.TicketController.API(w8t)`
- `api.KnowledgeController.API(w8t)`
- `api.WorkHoursController.API(w8t)`
- `api.TicketReviewController.API(w8t)`

## 工单接口

前端集中配置位置：

- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\api\factory.js`
- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\api\ticket.jsx`

可复用接口：

| 用途 | 方法 | 路径 |
| --- | --- | --- |
| 工单列表 | GET | `/api/w8t/ticket/list` |
| 工单详情 | GET | `/api/w8t/ticket/get` |
| 创建工单 | POST | `/api/w8t/ticket/create` |
| 更新工单 | POST | `/api/w8t/ticket/update` |
| 删除工单 | POST | `/api/w8t/ticket/delete` |
| 指派 | POST | `/api/w8t/ticket/assign` |
| 领取 | POST | `/api/w8t/ticket/claim` |
| 转派 | POST | `/api/w8t/ticket/transfer` |
| 升级 | POST | `/api/w8t/ticket/escalate` |
| 解决 | POST | `/api/w8t/ticket/resolve` |
| 关闭 | POST | `/api/w8t/ticket/close` |
| 重开 | POST | `/api/w8t/ticket/reopen` |
| 评论 | POST | `/api/w8t/ticket/comment` |
| 评论列表 | GET | `/api/w8t/ticket/comments` |
| 工时记录 | GET | `/api/w8t/ticket/worklog` |
| 统计 | GET | `/api/w8t/ticket/statistics` |
| 步骤列表 | GET | `/api/w8t/ticket/steps` |
| 新增步骤 | POST | `/api/w8t/ticket/step/add` |
| 更新步骤 | POST | `/api/w8t/ticket/step/update` |
| 删除步骤 | POST | `/api/w8t/ticket/step/delete` |
| 步骤排序 | POST | `/api/w8t/ticket/step/reorder` |

## 知识库接口

前端集中配置位置：

- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\api\factory.js`
- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\api\knowledge.jsx`

可复用接口：

| 用途 | 方法 | 路径 |
| --- | --- | --- |
| 创建知识 | POST | `/api/w8t/knowledge/create` |
| 更新知识 | POST | `/api/w8t/knowledge/update` |
| 删除知识 | POST | `/api/w8t/knowledge/delete` |
| 知识详情 | GET | `/api/w8t/knowledge/get` |
| 知识列表 | GET | `/api/w8t/knowledge/list` |
| 点赞 | POST | `/api/w8t/knowledge/like` |
| 关联到工单 | POST | `/api/w8t/knowledge/save-to-ticket` |
| 分类创建 | POST | `/api/w8t/knowledge/category/create` |
| 分类更新 | POST | `/api/w8t/knowledge/category/update` |
| 分类删除 | POST | `/api/w8t/knowledge/category/delete` |
| 分类详情 | GET | `/api/w8t/knowledge/category/get` |
| 分类列表 | GET | `/api/w8t/knowledge/category/list` |

## 前端接入点

源码位置：

- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\setupProxy.js`
- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\utils\http.jsx`
- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\pages\ticket\detail.jsx`
- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\pages\ticket\hooks\useTicketDetail.js`
- `D:\Workspace\wh-ops-alert\WatchAlert-web\src\pages\ticket\components\TicketStepsEditor.jsx`

现有前端已经具备：

- `/api` 代理到 `http://127.0.0.1:9001`
- axios 自动携带 `TenantID` 与 `Authorization`
- 工单详情页加载工单、步骤、评论、工时、评分、知识列表
- 步骤编辑器里已有知识库选择弹窗

最自然的入口是工单详情页：

1. 工单详情加载完成后，用工单 `title`、`description`、`type`、`priority`、`labels` 调用推荐服务。
2. 在工单详情或步骤编辑器旁边展示“推荐知识”。
3. 工程师点开推荐知识，只作为参考，不自动写入处理步骤。
4. 工程师采纳或忽略时，调用推荐服务的 feedback 接口沉淀效果数据。

## 推荐接入方案

### 方案 A：前端直连推荐服务

适合本地快速联调。

前端直接请求：

```http
POST http://127.0.0.1:9100/api/kb/recommend
Content-Type: application/json
```

请求体示例：

```json
{
  "ticket_id": "TICKET-001",
  "title": "打印机无法打印",
  "description": "共享打印机连接失败，提示脱机",
  "top_k": 5
}
```

优点：

- 改动小，不需要动 Go 后端。
- 当前推荐服务已开启 CORS，本地浏览器可直接访问。

限制：

- 生产环境不建议前端直连内部推荐服务。
- 鉴权、审计、租户隔离不走工单系统后端。

### 方案 B：Go 后端做代理

适合正式集成。

建议新增：

```http
POST /api/w8t/knowledge/recommend
```

由工单系统后端读取当前登录态、租户、工单信息，再转发到：

```http
POST http://127.0.0.1:9100/api/kb/recommend
```

优点：

- 前端仍然只访问 `/api/w8t/*`，不增加跨域和端口暴露。
- 可以沿用现有 `Authorization`、`TenantID`、审计日志和权限体系。
- 后续可以把推荐结果与工单操作、知识库采纳记录统一入库。

限制：

- 需要修改 `D:\Workspace\wh-ops-alert` 后端源码。
- 需要确定推荐服务地址配置项，例如 `kb_recommend_url`。

## 与现有知识库的关系

当前 `ops-kb` 生成的是 Markdown 知识库，推荐结果的 `id` 是文档 ID，不等同于 `wh-ops-alert` 数据库里的 `knowledgeId`。

因此第一阶段不要直接调用：

```http
POST /api/w8t/knowledge/save-to-ticket
```

更稳妥的做法是：

1. 先展示外部推荐知识，只读参考。
2. 采纳、忽略、打开详情等行为写入 `ops-kb` 的 feedback。
3. 等推荐效果稳定后，再做 Markdown 知识导入 `wh-ops-alert` 知识库表。
4. 导入后建立 `kb_doc_id -> knowledgeId` 映射，再使用 `/api/w8t/knowledge/save-to-ticket` 做正式关联。

## 下一步

建议先做方案 A 的最小联调：

1. 在 `wh-ops-alert` 前端新增一个 `kbRecommend` API 方法。
2. 在工单详情页读取当前工单信息后调用推荐服务。
3. 展示 Top 5 推荐知识、匹配分、分类、适用场景和处理步骤。
4. 增加“有用 / 无用 / 已参考”反馈按钮，调用 `http://127.0.0.1:9100/api/kb/feedback`。

如果要开始改 `wh-ops-alert` 源码，需要授权写入该目录。
