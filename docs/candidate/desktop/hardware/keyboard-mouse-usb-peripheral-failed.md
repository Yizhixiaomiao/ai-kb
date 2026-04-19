# 键盘、鼠标或 USB 外设异常

```yaml
status: usable
type: troubleshooting
asset_types: [pc, hardware]
systems: [windows]
issue_types: [hardware-fault]
tags: [keyboard, mouse, usb, peripheral]
source: ticket-history
```

## 常见现象

- 键盘按键失灵。
- 鼠标断点、左键失灵。
- USB 插口损坏或设备无法识别。
- 插入 USB 有提示音，但设备管理器找不到设备。

## 处理步骤

1. 重新插拔键盘、鼠标或 USB 设备。
2. 更换 USB 接口测试。
3. 使用其他电脑交叉验证外设是否损坏。
4. 检查设备管理器中是否有异常驱动。
5. 如涉及 USB 网卡或受控设备，检查桌管 / 加密策略是否禁用。
6. 必要时更换外设或维修接口。

## 升级条件

- USB 端口物理损坏。
- 桌管或加密策略禁用设备。
- 多台设备同时无法识别同类外设。

