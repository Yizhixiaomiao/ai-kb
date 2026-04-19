# IP 冲突或静态地址配置异常

```yaml
status: usable
type: troubleshooting
asset_types: [pc, network]
systems: [windows]
issue_types: [network-unavailable]
tags: [ip-conflict, dhcp, network]
source: ticket-history
```

## 常见现象

- 连不上网。
- 换办公室后无网络。
- IP 冲突。
- 静态地址配置不正确。

## 处理步骤

1. 确认电脑是否应使用 DHCP。
2. 检查当前 IP、网关、DNS。
3. 如工位应使用 DHCP，改回自动获取。
4. 如需静态地址，确认地址未被占用。
5. 重新认证网络后测试访问。

## 风险点

- 不要随意配置未知静态 IP。


