# 标签打印机纸张识别或连续出空白

```yaml
status: usable
type: troubleshooting
asset_types: [printer]
systems: [wms]
issue_types: [printer-not-working]
tags: [label-printer, barcode, wms, paper]
source: ticket-history
```

## 常见现象

- 标签机换纸后不识别纸张。
- 打一个标签出来多张空白。
- 库位码、标签、标识卡无法打印。
- 纸张规格不匹配。

## 处理步骤

1. 确认标签纸规格和装纸方向。
2. 检查打印机纸张传感器。
3. 重新校准标签纸。
4. 检查 WMS 或标签打印插件配置。
5. 重新连接标签打印机并测试打印。

## 升级条件

- 传感器无法识别纸张。
- WMS 打印组件异常。
- 涉及生产标签，影响发货或入库。


