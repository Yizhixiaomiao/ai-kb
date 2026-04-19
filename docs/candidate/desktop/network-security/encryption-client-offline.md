# 加密客户端掉线或手动上线失败

```yaml
status: usable
type: troubleshooting
asset_types: [pc]
systems: [windows]
issue_types: [network-authentication, file-access]
tags: [encryption-client, dlp, network]
source: ticket-history
```

## 常见现象

- 加密频繁掉线。
- 加密软件登不上。
- 手动上线失败。
- 加密客户端导致 CAD 卡顿或图纸打不开。

## 处理步骤

1. 检查网络是否正常。
2. 检查加密客户端服务状态。
3. 重新登录或重新上线。
4. 检查客户端版本是否过旧。
5. 如影响 CAD / PLM，记录版本和报错后升级给安全或厂商。

## 升级条件

- 批量用户加密客户端离线。
- 涉及图纸加密、解密或权限策略。


