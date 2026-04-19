# VPN 或远程访问失败

```yaml
status: usable
type: troubleshooting
asset_types: [pc, network]
systems: [vpn]
issue_types: [network-unavailable, login-failed]
tags: [vpn, remote-access]
source: ticket-history
```

## 常见现象

- OA、WMS 等提示未连接到互联网。
- VPN 连接不上。
- 远程访问进不去。

## 处理步骤

1. 确认本地网络是否正常。
2. 检查 VPN 客户端登录状态。
3. 确认账号权限和密码是否正常。
4. 重启 VPN 客户端后重试。
5. 如仍失败，记录错误提示并升级网络管理员。

## 升级条件

- 多人 VPN 同时不可用。
- 外部访问策略或账号权限异常。


