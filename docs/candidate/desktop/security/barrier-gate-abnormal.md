# 道闸无法关闭、自动开闭或离线

```yaml
status: usable
type: troubleshooting
asset_types: [security-device]
systems: [barrier-gate]
issue_types: [hardware-fault, network-unavailable]
tags: [barrier-gate, motor, infrared, limit, power, 道闸, 抬杆, 落杆, 车辆通行, 离线]
source: ticket-history
```

## 常见现象

- 道闸打开后无法关闭。
- 道闸不会回位，处于常开状态。
- 道闸自动开闭或落杆不到位。
- 道闸提示离线，车辆无法放行。
- 数码管报错、电机无法运行。

## 处理步骤

1. 确认故障道闸位置、方向和通道编号。
2. 检查供电、接地和设备电源状态。
3. 检查红外对射、限位、弹簧、主板和电机状态。
4. 检查设备与平台通讯是否正常。
5. 清理红外灰尘或重新固定红外对射。
6. 需要更换主板、电机或道闸主机时，记录型号并升级维护。
7. 修复后测试进出方向开关、落杆、反弹和平台记录。

## 验证方式

- 道闸能正常开关。
- 车辆通行记录能同步到平台。
- 离线告警消失。

## 升级条件

- 电机、主板、限位或道闸主机损坏。
- 涉及车辆通行、门岗或收费系统。
- 需要供应商重新配置程序。
