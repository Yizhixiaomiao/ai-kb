# 本地联调说明

本文说明工单系统后端与知识推荐服务的本地联调方式。

## 当前端口规划

建议本地联调时分两个服务：

```text
工单系统后端：http://127.0.0.1:9001
知识推荐服务：http://127.0.0.1:9100
```

工单系统后端在处理工单详情页或创建工单时，调用知识推荐服务：

```http
POST http://127.0.0.1:9100/api/kb/recommend
```

## 启动知识推荐服务

先确保索引存在：

```powershell
python scripts\build_kb_index.py
```

启动推荐服务：

```powershell
python scripts\kb_http_service.py --host 127.0.0.1 --port 9100
```

健康检查：

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:9100/health" -UseBasicParsing
```

## 推荐接口测试

```powershell
$body = @{
  ticket_id = "LOCAL-001"
  title = "连接不上打印机"
  description = "用户反馈连接不上共享打印机，换办公室后无法打印"
  category = "桌面运维"
  asset_type = "printer"
  top_k = 3
} | ConvertTo-Json -Depth 5

Invoke-WebRequest `
  -Uri "http://127.0.0.1:9100/api/kb/recommend" `
  -Method POST `
  -ContentType "application/json; charset=utf-8" `
  -Body $body `
  -UseBasicParsing
```

## 反馈接口测试

```powershell
$feedback = @{
  ticket_id = "LOCAL-001"
  doc_id = "shared-printer-connect-failed"
  action = "accepted"
  helpful = $true
  resolved = $true
  engineer_id = "local-test"
  comment = "本地联调反馈"
} | ConvertTo-Json -Depth 5

Invoke-WebRequest `
  -Uri "http://127.0.0.1:9100/api/kb/feedback" `
  -Method POST `
  -ContentType "application/json; charset=utf-8" `
  -Body $feedback `
  -UseBasicParsing
```

反馈会写入：

```text
data/kb-feedback.jsonl
```

## 工单后端集成方式

工单后端可以在以下时机调用：

- 打开工单详情页时。
- 创建工单并填写问题描述后。
- 工程师点击“推荐知识”按钮时。

建议第一阶段采用按钮触发，便于观察结果和调试。

## 联调排查

如果 `9001` 或 `9100` 访问失败，检查：

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 9001
Test-NetConnection -ComputerName 127.0.0.1 -Port 9100
```

查看端口监听：

```powershell
netstat -ano | Select-String ":9100"
```

如果知识服务和工单后端不在同一个运行环境，不能使用 `127.0.0.1` 互相访问，需要把知识服务监听地址改为内网地址：

```powershell
python scripts\kb_http_service.py --host 0.0.0.0 --port 9100
```

再由工单后端访问：

```text
http://<知识服务所在机器IP>:9100/api/kb/recommend
```
