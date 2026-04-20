# 打印不清楚、横纹、黑印或打印头磨损

```yaml
status: usable
type: troubleshooting
asset_types: [printer]
systems: []
issue_types: [printer-not-working, hardware-fault]
tags: [printer, print-quality, toner, print-head, streaks, 打印不清楚, 字迹模糊, 横纹, 黑印, 打印头磨损]
source: ticket-history
```

## 常见现象

- 打印不清楚。
- 字体断断续续、局部空白。
- 打印照片出现断续横纹。
- 纸张两边有黑印。
- 标签连续出空白或跑空白。
- 针式打印机针头、标签打印机打印头磨损。

## 处理步骤

1. 确认打印机类型：激光、针式、标签机或照片打印机。
2. 打印测试页，判断是所有内容异常还是特定文件异常。
3. 对激光打印机，检查粉盒、硒鼓和定影组件。
4. 对针式打印机，检查色带、针头和打印头磨损。
5. 对标签机，检查打印头、纸张传感器和标签纸校准。
6. 对 PDF 或图片打印异常，先排除软件打印设置。
7. 硬件磨损时记录型号并申请耗材或维修。

## 验证方式

- 测试页清晰，无横纹、黑印、空白间隔。
- 业务标签、单据或照片打印正常。

## 常用指令

- `control printers`：打开 Windows 打印机列表，用于进入打印首选项、打印测试页或检查默认打印机。
- `printmanagement.msc`：打开打印管理，查看打印驱动、端口和队列，适用于驱动或端口异常排查。
- `services.msc`：打开服务管理器，检查 Print Spooler 服务状态。
- `net stop spooler`：停止打印后台处理服务，常用于清理异常打印队列前置操作。
- `net start spooler`：启动打印后台处理服务，清理队列或重装驱动后用于恢复打印服务。
- `Get-Printer`：PowerShell 查看本机打印机列表，确认打印机名称、状态和驱动信息。

## 升级条件

- 打印头、针头、定影膜、硒鼓或粉盒需要更换。
- 生产标签或业务单据打印质量影响作业。
