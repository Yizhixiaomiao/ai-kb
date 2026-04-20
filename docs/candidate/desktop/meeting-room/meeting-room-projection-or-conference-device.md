# 会议室投屏、亿联或腾讯会议设备异常

```yaml
status: usable
type: troubleshooting
asset_types: [meeting-room-device, pc]
systems: [meeting-room]
issue_types: [network-unavailable, software-install, hardware-fault]
tags: [projection, yealink, tencent-meeting, wireless, meeting-room, 会议室, 投屏, 会议摄像头, 麦克风, 腾讯会议]
source: ticket-history
```

## 常见现象

- 笔记本无法使用会议室腾讯会议投屏。
- 有线投屏不同步。
- 平板不能投屏到电视。
- 亿联设备存储满。
- 会议室设备需要调整、搬迁或重新配置。

## 处理步骤

1. 确认会议室、设备型号和投屏方式。
2. 检查有线投屏线缆、网口、无线投屏网络和输入源。
3. 检查终端是否被桌管或安全策略限制无线设备。
4. 对亿联等会议终端，检查存储空间、账号和网络状态。
5. 设备搬迁或调整后，重新测试音视频、投屏、麦克风和网络。
6. 会议前保障时，优先恢复可用方案，再记录根因。

## 验证方式

- 笔记本或平板能成功投屏。
- 腾讯会议音视频正常。
- 亿联设备无存储或网络告警。

## 常用指令

- `mmsys.cpl`：打开 Windows 声音设置，检查默认麦克风和扬声器设备。
- `desk.cpl`：打开显示设置，检查投影、复制、扩展和分辨率配置。
- `displayswitch.exe`：打开投影切换界面，用于快速切换复制、扩展或仅第二屏。
- `devmgmt.msc`：打开设备管理器，检查摄像头、麦克风、声卡和 USB 设备是否异常。
- `ncpa.cpl`：打开网络连接界面，检查会议终端或无线投屏网络连接状态。
- `ping <会议终端地址或网关>`：验证会议终端到网络的基础连通性。

## 升级条件

- 桌管策略影响无线投屏。
- 会议终端固件、账号或平台异常。
- 重要会议保障。
