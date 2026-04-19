# 门禁离线、反复重启或网络异常

```yaml
status: usable
type: troubleshooting
asset_types: [security-device, network]
systems: [access-control]
issue_types: [network-unavailable, hardware-fault]
tags: [access-control, door, ap, power, offline]
source: ticket-history
```

## 常见现象

- 门禁一体机反复重启。
- 门禁系统离线。
- 门禁处 AP 离线或无线网络不通。
- 后台提示认证或网络异常。

## 处理步骤

1. 确认门禁位置和影响范围。
2. 检查门禁设备供电和电源适配器。
3. 长 ping 门禁设备，观察是否间歇性中断。
4. 检查门禁使用的网络、AP、交换机和认证状态。
5. 检查后台平台是否能看到设备在线。
6. 如电源、AP 或设备硬件异常，记录现象并升级维护。

## 验证方式

- 门禁设备稳定在线。
- 刷卡、人脸或访客认证功能正常。
- 后台无离线告警。

## 升级条件

- 门禁电源、AP 或一体机损坏。
- 门禁影响生产、环保或安全通行。
- 多个门禁点位同时异常。

