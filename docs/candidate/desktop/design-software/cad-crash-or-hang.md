# CAD 打开后卡死、崩溃或无响应

```yaml
status: usable
type: troubleshooting
asset_types: [pc]
systems: [windows]
issue_types: [performance-slow, software-install]
tags: [cad, crash, hang, authentication-client]
source: ticket-history
```

## 常见现象

- CAD 打开后卡死。
- 打开图纸后无响应。
- 频繁崩溃。
- 认证客户端或杀毒软件影响 CAD 程序文件。

## 处理步骤

1. 确认是打开 CAD 即卡死，还是打开特定图纸卡死。
2. 检查 CPU、内存、磁盘占用。
3. 检查认证客户端、加密客户端或杀毒软件是否拦截 CAD 文件。
4. 安装必要运行库。
5. 禁用异常插件或 Autodesk 相关非必要插件。
6. 必要时卸载重装 CAD。

## 升级条件

- 同版本 CAD 多人异常。
- 与加密客户端或认证客户端版本冲突。


