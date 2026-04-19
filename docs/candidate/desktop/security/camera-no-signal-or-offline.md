# 摄像头无信号、离线或画面异常

```yaml
status: usable
type: troubleshooting
asset_types: [security-device, network]
systems: [camera, monitoring]
issue_types: [network-unavailable, hardware-fault]
tags: [camera, cctv, no-signal, offline, power, switch]
source: ticket-history
```

## 常见现象

- 摄像头不通、无视频信号。
- 多个摄像头同时不亮。
- 监控画面掉线。
- 摄像头位置偏移、画面角度异常。
- 下雨、施工、供电或交换机异常后摄像头离线。

## 处理步骤

1. 确认是单个摄像头异常还是同区域多个摄像头异常。
2. 检查摄像头供电、电源适配器、插排和 PoE 交换机状态。
3. 检查网线、光纤、交换机端口和链路指示灯。
4. 在监控平台查看设备在线状态、码流和最近离线时间。
5. 对单个摄像头，现场检查设备、镜头、支架和接线。
6. 对施工导致角度偏移的摄像头，重新调整角度并确认覆盖范围。
7. 涉及光纤、交换机或设备损坏时升级网络或安防维护。

## 验证方式

- 监控平台显示设备在线。
- 实时画面正常。
- 录像回放正常。

## 升级条件

- 同区域多个摄像头同时离线。
- 摄像头、交换机、光纤或供电设备损坏。
- 涉及保密区域、门岗、围墙等关键点位。

