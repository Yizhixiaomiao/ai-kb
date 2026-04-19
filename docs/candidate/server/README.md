# 服务器运维参考知识清单

本目录收录服务器、容器、数据库、网络设备相关的高风险运维参考手册。当前资料来自：

```text
D:\Work\工作文档\知识库构建\服务器运维相关
```

导入时已统一补充知识库元数据、适用范围、常见现象、处理步骤、验证方式和注意事项，并对明显示例密码做了脱敏处理。

## 分类

| 分类 | 文档 | 说明 |
| --- | --- | --- |
| 容器 | `container/docker-ops-guide.md` | Docker Engine、Compose、镜像、容器、网络、存储和常见故障 |
| 容器 | `container/kubernetes-ops-guide.md` | Kubernetes 集群、Pod、Service、Ingress、Helm 和常见故障 |
| 数据库 | `database/mysql-backup-restore-guide.md` | MySQL mysqldump 逻辑备份和恢复 |
| 数据库 | `database/oracle-backup-restore-guide.md` | Oracle RMAN、Data Pump、冷备和恢复 |
| 数据库 | `database/xtrabackup-guide.md` | Percona XtraBackup 物理热备、增量备份和恢复 |
| 网络 | `network/huawei-switch-config-guide.md` | 华为交换机 VRP、VLAN、接口、路由、ACL、监控和排障 |

## 使用准则

- 这些文档属于服务器、数据库和网络设备高风险运维知识，推荐结果只作为工程师参考。
- 生产环境操作前必须确认审批、备份、维护窗口、影响范围和回退方案。
- 涉及删除、覆盖、恢复、重启、扩缩容、路由/ACL 变更、证书/密钥等动作时，不允许直接照抄执行。
- 如果推荐结果只是第二或第三候选，需要结合工单对象、系统、资产类型和现象人工判断。

## 推荐关键词示例

- Docker 容器启动失败、容器异常退出、镜像构建失败、Docker 服务异常。
- Kubernetes Pod CrashLoopBackOff、ImagePullBackOff、节点 NotReady、Ingress 访问异常。
- MySQL 备份失败、mysqldump 恢复、binlog 恢复、备份压缩加密。
- Oracle RMAN 备份、Data Pump 导入导出、表空间恢复、归档日志。
- XtraBackup 全量备份、增量备份、prepare 失败、物理恢复。
- 华为交换机端口不通、VLAN 配置、ACL、SSH 登录、配置保存。
