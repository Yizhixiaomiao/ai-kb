# 会议室屏幕、大屏或 LED 显示异常

```yaml
status: usable
type: troubleshooting
asset_types: [meeting-room-device, display]
systems: [meeting-room]
issue_types: [hardware-fault]
tags: [meeting-room, led-screen, display, maxhub, signal, 会议室, 大屏, LED, 黑屏, 投屏]
source: ticket-history
```

## 常见现象

- 会议室屏幕闪烁、晃眼。
- 大屏不显示或部分屏幕不亮。
- LED 屏不定时黑屏。
- 显示颜色异常、横纹或接触不良。
- MaxHub 或会议大屏无法安装 APK。

## 处理步骤

1. 确认会议室、屏幕编号和故障区域。
2. 检查大屏电源、信号线、HDMI 输入源和控制设备。
3. 对拼接屏或 LED 屏，检查单块屏幕、接收卡和配置线。
4. 如需调试软件，使用公司指定工具读取和保存配置后再操作。
5. 对 APK 安装问题，确认设备安装权限和软件来源。
6. 硬件损坏或需要拆屏时升级会议设备维护或供应商。

## 验证方式

- 大屏显示完整。
- 投屏、会议画面或演示内容正常。
- 设备重启后配置仍正常。

## 常用指令

- `desk.cpl`：打开显示设置，检查分辨率、多屏模式和主副屏配置。
- `displayswitch.exe`：打开投影切换界面，确认当前是复制、扩展还是仅第二屏。
- `dxdiag`：查看显卡、显示输出和 DirectX 信息，辅助判断电脑端显示能力。
- `devmgmt.msc`：打开设备管理器，检查显卡、显示器和 USB 转接设备是否异常。
- `ping <控制器或大屏设备地址>`：检查大屏控制器或会议终端网络连通性。

## 升级条件

- LED 屏、背板、接收卡或控制器损坏。
- 涉及拆屏、重新配置屏参。
- 会议保障窗口紧急。
