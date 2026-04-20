# 按卷清理 Data Domain 空间的完整流程

```yaml
status: imported
type: reference
source: engineer-doc
asset_types: [business-system, server]
systems: [storage]
issue_types: [reference]
tags: [engineer-doc, imported, data-domain]
source_path: "D:\新建文件夹\业务维护清单\按卷清理 Data Domain 空间的完整流程.docx"
import_note: "由正式文档导入，原文格式可能未标准化；账号、密码、Token、IP 和手机号已尽量脱敏。"
```

## 文档说明

- 来源类型：工程师正式文档
- 原始文件：按卷清理 Data Domain 空间的完整流程.docx
- 原始路径：D:\新建文件夹\业务维护清单
- 导入策略：保留正文用于检索，不直接视为标准 SOP。

## 原始正文

🔹按卷清理 Data Domain 空间的完整流程

1. 查看卷状态（NetWorker）

在 NetWorker Server 上执行：

mminfo -av -r "volume,volid,percent,mode,volretent,clflags" | findstr nmc.dddefault

percent → 卷使用率

mode → appendable/full

volretent → 卷保留期限

clflags → 标志位（recyclable 等）

确认目标卷（如 .002~.007）确实不需要保留。

2. 确认卷里无要保留的 Save Set

（可选验证，不逐条审核，但至少看一眼）

mminfo -q volume=nmc.dddefault.002 -avot -r "ssid,ssretent,ssflags"

如果卷上全是过期或者你确定整卷不要，可以直接下一步。

3. 将卷标记为 recyclable

对每个要清理的卷：

nsrmm -o recyclable -y nmc.dddefault.002

nsrmm -o recyclable -y nmc.dddefault.003

nsrmm -o recyclable -y nmc.dddefault.004

nsrmm -o recyclable -y nmc.dddefault.005

nsrmm -o recyclable -y nmc.dddefault.006

nsrmm -o recyclable -y nmc.dddefault.007

这会告诉 NetWorker：卷内容可被覆盖/删除。

4. 同步媒体数据库

执行：

nsrim -X

确保 NetWorker 元数据与 Data Domain 一致。

5. 在 Data Domain 上执行清理

登录 Data Domain（SSH）：

filesys show space

filesys clean start

filesys clean status

等 Clean 完成，再验证：

filesys show space

预期：Cleanable GiB → 0，Available 空间增加。

6.清理完后如果卷不可写需要在管理界面手动修改卷状态为可追加
