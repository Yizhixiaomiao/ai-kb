# JVM GC、线程数量或 Java 运行时异常告警处理指南

```yaml
status: usable
type: troubleshooting
risk_level: high
review_required: true
asset_types: [server, business-system]
systems: [java, jvm]
issue_types: [jvm-gc, thread-high, performance]
tags: [jvm, gc, java, thread, heap, performance]
```

## 适用范围

- 适用于 GC 吞吐率低、GC 暂停时间过长、活跃守护线程数过多等 Java 应用运行时告警。
- 适用于规则名称包含“GC吞吐率”“GC暂停总时长”“守护线程数量”等场景。

## 常见现象

- GC 频繁或暂停时间变长。
- 应用响应慢、接口超时或实例重启。
- 线程数异常增长，可能伴随连接池、任务线程或死循环问题。

## 判断依据

- 结合 JVM 指标、应用日志、发布变更、流量变化和依赖状态判断。
- 区分短时流量高峰、内存泄漏、线程泄漏和外部依赖阻塞。

## 处理步骤

1. 确认应用、实例、告警指标、持续时间和业务影响。
2. 查看 JVM heap、GC 次数、GC 暂停、线程数、CPU、内存和应用日志。
3. 对比告警前后的发布、配置、流量和依赖服务状态。
4. 如果影响业务，按预案扩容、摘除异常实例、重启实例或回滚发布。
5. 保留 GC 日志、线程栈、堆信息和应用错误日志，交由应用负责人分析根因。
6. 记录处理动作、恢复时间和是否需要优化 JVM 参数或代码。

## 常用指令

- jps -lv -- ?? Java ?????????????
- jstat -gcutil <pid> 1000 10 -- ?? JVM GC ????????????
- jcmd <pid> VM.flags -- ?? JVM ??????????
- jcmd <pid> GC.heap_info -- ?????????????
- jcmd <pid> Thread.print > thread-dump-$(date +%F-%H%M%S).txt -- ?????????????????????
- jstack <pid> > jstack-$(date +%F-%H%M%S).txt -- ?? Java ?????????
- top -H -p <pid> -- ?? Java ????? CPU ????????
- ps -L -p <pid> -o pid,tid,pcpu,pmem,comm -- ??????????????????
- grep -i -E "Full GC|OutOfMemory|GC overhead" <app-log-file> | tail -50 -- ???????? GC ? OOM ????????
- kubectl logs <pod-name> -n <namespace> --tail=300 -- ?? Java ?? Pod ??????????

## 验证方式

- GC 指标、线程数和接口耗时恢复正常。
- 应用实例健康检查通过。
- 告警不再持续触发。

## 注意事项

- 不要在没有保留现场信息的情况下直接重启所有实例。
- 采集 heap dump、线程栈等操作可能影响性能，应在授权和维护窗口内执行。
- JVM 参数调整应经过测试验证，不应临时猜测修改。
