# MES 登录失败或疑似网络认证问题

```yaml
status: usable
type: troubleshooting
asset_types: [pc, network, business-system]
systems: [mes]
issue_types: [network-unavailable, login-failed]
tags: [mes, network, authentication]
source: ticket-history
```

## 常见现象

- MES 登不上。
- 车间终端没网。
- 认证过多或认证客户端异常。

## 处理步骤

1. 确认同区域其他 MES 终端是否正常。
2. 检查网络认证状态。
3. 检查 MES 访问地址是否正确。
4. 清理浏览器缓存或重新打开 MES。
5. 如同区域多台异常，升级网络或 MES 管理员。

## 升级条件

- 车间批量无法访问 MES。
- MES 系统本身异常。


