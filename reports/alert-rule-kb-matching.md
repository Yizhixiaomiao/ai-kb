# 告警规则与知识库匹配报告

本报告根据告警规则 `ruleName`、规则组名称、描述、表达式和标签，在本地知识库中做混合推荐匹配。

## 总览

- 告警规则数：37
- 有推荐结果：37
- 无推荐结果：0
- 匹配率：100.0%

## Top 匹配样例

- `MySQL宕机` -> `database-status-tablespace-alert`，综合 130，规则 114，向量 0.202
- `WMS 项目 Mysql  宕机` -> `database-status-tablespace-alert`，综合 130，规则 114，向量 0.202
- `KubernetesPod不健康` -> `kubernetes-ops-guide`，综合 127，规则 112，向量 0.1978
- `nacos 注册掉线告警` -> `application-http-5xx-or-unavailable-alert`，综合 112，规则 94，向量 0.2339
- `WMS业务机器CPU使用率` -> `linux-cpu-high-usage-alert`，综合 99，规则 80，向量 0.2415
- `CPU使用率达到95%` -> `linux-cpu-high-usage-alert`，综合 97，规则 80，向量 0.2188
- `Kubernetes节点网络不可用` -> `kubernetes-ops-guide`，综合 96，规则 80，向量 0.2002
- `KubernetesNode内存压力过大` -> `kubernetes-ops-guide`，综合 96，规则 80，向量 0.2073
- `CPU使用率超过95%` -> `linux-cpu-high-usage-alert`，综合 96，规则 80，向量 0.2088
- `5分钟内GC暂停总时长大于1秒` -> `jvm-gc-thread-alert`，综合 93，规则 80，向量 0.1692
- `域名三分钟内超过 300次 4xx 错误，请注意相关业务使用状态` -> `application-http-5xx-or-unavailable-alert`，综合 85，规则 70，向量 0.1916
- `JVM内存使用率大于 80%` -> `jvm-gc-thread-alert`，综合 83，规则 72，向量 0.1401
- `GC吞吐率<90%,程序异常` -> `jvm-gc-thread-alert`，综合 72，规则 60，向量 0.1576
- `Windows_磁盘空间使用率超过95%` -> `linux-disk-space-high-alert`，综合 62，规则 42，向量 0.2533
- `WMS 后端应用 5xx 告警` -> `application-http-5xx-or-unavailable-alert`，综合 62，规则 50，向量 0.1624
- `磁盘空间使用率超过97%` -> `linux-disk-space-high-alert`，综合 61，规则 42，向量 0.2498
- `磁盘空间使用率达到90%以上` -> `linux-disk-space-high-alert`，综合 58，规则 42，向量 0.2057
- `WMS业务机器内存使用率` -> `linux-memory-high-usage-alert`，综合 58，规则 42，向量 0.2041
- `内存使用率超过95%` -> `linux-memory-high-usage-alert`，综合 58，规则 42，向量 0.2118
- `内存使用率达到97%` -> `linux-memory-high-usage-alert`，综合 57，规则 42，向量 0.1952
- `活跃的守护线程数量 > 500 告警` -> `jvm-gc-thread-alert`，综合 57，规则 42，向量 0.1939
- `内存使用率达到95%` -> `linux-memory-high-usage-alert`，综合 56，规则 42，向量 0.1813
- `卫华MES数据库表空间监控` -> `database-status-tablespace-alert`，综合 50，规则 34，向量 0.2044
- `江苏MES数据库表空间监控` -> `database-status-tablespace-alert`，综合 50，规则 34，向量 0.2044
- `卫华MES数据库状态监控` -> `database-status-tablespace-alert`，综合 45，规则 28，向量 0.2159
- `江苏MES数据库状态监控` -> `database-status-tablespace-alert`，综合 45，规则 28，向量 0.2159
- `Pod 内存使用率过高` -> `kubernetes-ops-guide`，综合 40，规则 34，向量 0.0803
- `PLM应用磁盘空间剩余小于8G` -> `linux-disk-space-high-alert`，综合 38，规则 22，向量 0.2102
- `AI 项目 业务后端不可用` -> `application-http-5xx-or-unavailable-alert`，综合 36，规则 22，向量 0.1823
- `业务后端不可用` -> `application-http-5xx-or-unavailable-alert`，综合 36，规则 22，向量 0.1823

## 未匹配规则样例

