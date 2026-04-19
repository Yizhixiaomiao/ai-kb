# 知识推荐离线回测报告

本报告由本地脚本根据历史工单和 Markdown 知识库生成，未连接任何服务器、接口或外部服务。

## 总体结果

- 工单总数：2491
- 有推荐命中：1950
- 无推荐命中：541
- 命中率：78.3%

## Top 推荐知识

- desktop/network-authentication-unavailable：259
- desktop/pc-boot-failed：220
- desktop/account-login-failed：106
- business-systems/oa-upload-or-print-slow：78
- desktop/printer-not-working：77
- design-software/cad-plm-interface-failed：77
- desktop/pc-performance-slow：75
- hardware/monitor-no-display-or-flicker：68
- desktop/black-screen-desktop-not-shown：66
- printer/shared-printer-connect-failed：65
- design-software/cad-install-uninstall-failed：59
- desktop/windows-system-reinstall-or-cache-reset：55
- desktop/printer-paper-jam：53
- network-security/network-cable-port-switch-fault：52
- desktop/office-wps-document-open-failed：51
- desktop/software-client-installation：42
- hardware/blue-screen-dump-or-driver：40
- printer/print-quality-faded-streaks-head-wear：39
- hardware/keyboard-mouse-usb-peripheral-failed：35
- desktop/shared-file-cloud-drive-access：30

## 未命中高频词

- 测试：21
- 加急：6
- 电脑：4
- 打不开：4
- word：4
- 柱子：4
- 盘已满：3
- 军品车间：3
- 路北：3
- 无法使用：3
- 连接不上：2
- 主机异响：2
- wifi：2
- 加密老掉线：2
- 显示：2
- 磁盘损坏：2
- 主机打不开：2
- 无法正常使用：2
- 无法保存：2
- 打印机连不上电脑：2
- 电脑运行卡：2
- 开机异常：2
- 微信登陆不上：2
- 电脑无法上网：2
- 电脑运行慢：2
- 习惯性死机：2
- 打开文件司机：2
- 需处理：2
- 无法连接外网：2
- 登陆软件没有了：2

## 下一步建议

- 对未命中高频词补充关键词或新增细分知识。
- 检查高频推荐是否过于泛化，必要时继续拆分场景。
- 将 `reports/recommendation-dry-run.csv` 中的推荐结果抽样给工程师确认，优化关键词权重。
