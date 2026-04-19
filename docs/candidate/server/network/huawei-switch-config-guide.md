# 华为交换机配置与排障参考手册

```yaml
status: usable
type: reference
risk_level: high
review_required: true
source: imported-manual
source_path: D:/Work/工作文档/知识库构建/服务器运维相关/huawei-switch-config-guide.md
asset_types: [network-device, switch]
systems: [huawei-vrp, switch]
issue_types: [network-unavailable, switch-config, port-down]
tags: [huawei, switch, vrp, vlan, stp, acl, ssh]
```

## 适用范围

- 适用于华为交换机基础配置、VLAN、接口、路由、ACL、安全、监控维护和常见故障排查。
- 适合作为网络工程师变更前核对和故障定位参考。

## 常见现象

- 交换机端口 Down、VLAN 不通或网关不可达。
- SSH/Telnet 登录、管理 IP、NTP、日志或配置保存异常。
- ACL、路由、DHCP、STP、链路聚合或镜像配置异常。

## 处理步骤

1. 确认设备型号、VRP 版本、变更目标、影响范围和回退配置。
2. 优先执行只读检查：display current-configuration、display interface、display vlan、display ip routing-table、display logbuffer 等。
3. 按问题类型参考原始手册中的基础配置、VLAN、路由、ACL、安全或监控维护章节。
4. 涉及接口关闭、路由变更、ACL 变更、配置恢复和重启前，必须备份当前配置并在维护窗口操作。
5. 处理后保存配置，并记录变更前后关键状态。

## 验证方式

- 目标端口、VLAN、路由或管理访问恢复。
- 业务连通性测试正常。
- 配置保存成功，重启风险和回退方案已确认。

## 注意事项

- 本文属于服务器、数据库或网络设备高风险运维参考，生产环境操作前必须完成审批、备份、维护窗口和回退方案确认。
- 本文中的命令和参数来自通用手册，执行前必须替换为本公司实际环境，并先在测试环境验证。
- 涉及删除、覆盖、重启、恢复、扩缩容、路由/ACL 变更、证书/密钥、数据库恢复等动作时，不允许直接照抄执行。
- 手册中的示例密码、Token 和密钥已做脱敏处理；不得在知识库中保存真实凭据。

## 原始手册

以下内容为导入的原始手册正文，供工程师查阅细节。

# 华为交换机配置完全指南

> 📝 版本：VRP 5.x / VRP 8.x  
> ⚠️ 生产环境操作前请先在测试环境验证！

---

## 📚 目录

1. [华为交换机系列与版本](#1-华为交换机系列与版本)
2. [基础配置](#2-基础配置)
3. [VLAN 配置](#3-vlan-配置)
4. [链路聚合](#4-链路聚合)
5. [生成树协议](#5-生成树协议)
6. [路由配置](#6-路由配置)
7. [ACL 与安全](#7-acl-与安全)
8. [QoS 配置](#8-qos-配置)
9. [堆叠与集群](#9-堆叠与集群)
10. [监控与维护](#10-监控与维护)
11. [故障处理案例（25 例）](#11-故障处理案例 25 例)
12. [最佳实践](#12-最佳实践)

---

## 1. 华为交换机系列与版本

### 1.1 主要系列

| 系列 | 定位 | 典型型号 |
|------|------|----------|
| **S1700** | 入门级 | S1700-8G, S1700-24G |
| **S2700** | 二层接入 | S2700-26TP, S2700-52P |
| **S3700** | 三层接入 | S3700-28TP, S3700-52P |
| **S5700** | 企业接入/汇聚 | S5700-28X, S5700-52X |
| **S6700** | 万兆汇聚 | S6700-24X, S6700-48X |
| **S7700** | 核心交换机 | S7703, S7706, S7712 |
| **S9700** | 数据中心核心 | S9703, S9706, S9712 |
| **S12700** | 敏捷交换机 | S12704, S12708, S12712 |

### 1.2 VRP 版本区别

| VRP 版本 | 对应系统 | 特点 |
|----------|----------|------|
| **VRP 5.x** | V200R001-V200R011 | 传统命令行，配置方式较老 |
| **VRP 8.x** | V200R019+ | 新命令行，支持 Python 自动化，配置更灵活 |

### 1.3 VRP 5.x vs VRP 8.x 命令差异

| 功能 | VRP 5.x | VRP 8.x |
|------|---------|---------|
| 进入系统视图 | `system-view` | `system-view` |
| 查看配置 | `display current-configuration` | `display current-configuration` |
| 保存配置 | `save` | `save` |
| VLAN 批量创建 | `vlan batch 10 20 30` | `vlan batch 10 to 30` |
| 接口描述 | `description xxx` | `description xxx` |
| SSH 开启 | `stelnet server enable` | `ssh server enable` |

---

## 2. 基础配置

### 2.1 首次登录

```bash
# Console 登录（默认无密码）
<Quidway> system-view
[Quidway] sysname SW-Core

# Telnet 登录
<Quidway> system-view
[Quidway] telnet server enable
[Quidway] user-interface vty 0 4
[Quidway-ui-vty0-4] authentication-mode aaa
[Quidway-ui-vty0-4] protocol inbound telnet
[Quidway-ui-vty0-4] quit
[Quidway] aaa
[Quidway-aaa] local-user admin password cipher <示例密码>
[Quidway-aaa] local-user admin service-type telnet
[Quidway-aaa] local-user admin privilege level 15
```

### 2.2 SSH 配置（推荐）

```bash
# VRP 8.x
system-view
sysname SW-Core
ssh server enable
stelnet server enable

# 创建用户
aaa
 local-user admin password cipher <示例密码>
 local-user admin service-type ssh
 local-user admin privilege level 15
 quit

# 生成密钥
rsa local-key-pair create 2048

# 配置 VTY
user-interface vty 0 4
 authentication-mode aaa
 protocol inbound ssh
 quit

# 配置 SSH 用户
ssh user admin authentication-type password
ssh user admin service-type stelnet
```

### 2.3 接口基础配置

```bash
system-view

# 配置接口描述
interface GigabitEthernet 0/0/1
 description To-Server-Web01
 quit

# 配置接口速率和双工
interface GigabitEthernet 0/0/2
 speed 1000
 duplex full
 quit

# 关闭接口
interface GigabitEthernet 0/0/3
 shutdown
 quit

# 开启接口
interface GigabitEthernet 0/0/3
 undo shutdown
 quit

# 批量配置接口
port-group 1
 group-member GigabitEthernet 0/0/1 to 0/0/24
 description To-Access-Switch
 port link-type access
 quit
```

### 2.4 管理 IP 配置

```bash
# 配置 VLANIF 管理 IP
interface Vlanif 1
 ip address 192.168.1.10 255.255.255.0
 quit

# 配置默认网关
ip route-static 0.0.0.0 0.0.0.0 192.168.1.1

# 配置带外管理（如果有 MGMT 口）
interface MEth 0/0/1
 ip address 192.168.100.10 255.255.255.0
 quit
```

### 2.5 保存与恢复

```bash
# 保存配置
save
# 或
write

# 查看保存的配置
display saved-configuration

# 备份配置到 TFTP
tftp 192.168.1.100 put flash:/vrpcfg.zip

# 从 TFTP 恢复配置
tftp 192.168.1.100 get flash:/vrpcfg.zip

# 重启交换机
reboot

# 恢复出厂设置
reset saved-configuration
reboot
```

### 2.6 系统时间配置

```bash
# 手动设置时间
clock datetime 10:30:00 2026-03-10

# 配置 NTP
ntp-service unicast-server 192.168.1.100
ntp-service unicast-server 192.168.1.101

# 配置时区（东八区）
clock timezone Beijing add 08:00:00

# 查看时间
display clock
```

---

## 3. VLAN 配置

### 3.1 创建 VLAN

```bash
system-view

# 创建单个 VLAN
vlan 10
 description HR-Department
 quit

# 批量创建 VLAN
vlan batch 10 20 30
# 或
vlan batch 10 to 30

# 批量创建并命名
vlan batch 10 to 30
vlan 10
 description HR
 quit
vlan 20
 description Finance
 quit
```

### 3.2 Access 端口配置

```bash
# 将端口加入 VLAN
interface GigabitEthernet 0/0/1
 port link-type access
 port default vlan 10
 quit

# 批量配置 Access 端口
port-group access-ports
 group-member GigabitEthernet 0/0/1 to 0/0/24
 port link-type access
 port default vlan 10
 quit
```

### 3.3 Trunk 端口配置

```bash
# 配置 Trunk 端口
interface GigabitEthernet 0/0/24
 port link-type trunk
 port trunk allow-pass vlan 10 20 30
 # 或允许所有 VLAN
 # port trunk allow-pass vlan 1 to 4094
 quit

# 修改 Trunk 默认 VLAN（PVID）
interface GigabitEthernet 0/0/24
 port trunk pvid vlan 10
 quit
```

### 3.4 Hybrid 端口配置

```bash
# Hybrid 端口（灵活 tagging）
interface GigabitEthernet 0/0/1
 port link-type hybrid
 port hybrid tagged vlan 10 20
 port hybrid untagged vlan 30
 port hybrid pvid vlan 30
 quit

# Hybrid 端口应用场景
# - 连接 IP 电话：语音 VLAN tagged，数据 VLAN untagged
interface GigabitEthernet 0/0/2
 port link-type hybrid
 port hybrid tagged vlan 100  # 语音 VLAN
 port hybrid untagged vlan 10  # 数据 VLAN
 port hybrid pvid vlan 10
 quit
```

### 3.5 VLAN 间路由

```bash
# 创建 VLANIF 接口
interface Vlanif 10
 ip address 192.168.10.1 255.255.255.0
 quit

interface Vlanif 20
 ip address 192.168.20.1 255.255.255.0
 quit

interface Vlanif 30
 ip address 192.168.30.1 255.255.255.0
 quit

# 验证
display ip interface brief
ping 192.168.20.1
```

### 3.6 Super VLAN

```bash
# 创建 Super VLAN
vlan 100
 description Super-VLAN
 quit

interface Vlanif 100
 ip address 192.168.100.1 255.255.255.0
 quit

# 创建 Sub VLAN
vlan batch 101 102 103
vlan 101
 description Sub-VLAN-1
 quit
vlan 102
 description Sub-VLAN-2
 quit
vlan 103
 description Sub-VLAN-3
 quit

# 关联 Sub VLAN 到 Super VLAN
vlan 100
 aggregate-vlan
 access-vlan 101 to 103
 quit

# 启用 ARP 代理
interface Vlanif 100
 arp-proxy inter-sub-vlan-proxy enable
 quit
```

---

## 4. 链路聚合

### 4.1 手工负载分担

```bash
# 创建 Eth-Trunk
interface Eth-Trunk 1
 description To-Core-Switch
 port link-type trunk
 port trunk allow-pass vlan 10 20 30
 quit

# 添加成员端口
interface GigabitEthernet 0/0/23
 eth-trunk 1
 quit

interface GigabitEthernet 0/0/24
 eth-trunk 1
 quit

# 查看状态
display eth-trunk 1
```

### 4.2 LACP 模式

```bash
# 创建 LACP Eth-Trunk
interface Eth-Trunk 1
 mode lacp
 description To-Core-LACP
 port link-type trunk
 port trunk allow-pass vlan 10 20 30
 quit

# 添加成员端口
interface GigabitEthernet 0/0/23
 eth-trunk 1
 quit

interface GigabitEthernet 0/0/24
 eth-trunk 1
 quit

# 配置 LACP 优先级（可选）
interface Eth-Trunk 1
 lacp priority 100  # 值越小优先级越高
 quit

# 配置活动端口数量上限
interface Eth-Trunk 1
 max active-linknumber 2
 quit

# 查看 LACP 状态
display eth-trunk 1
display lacp statistics eth-trunk 1
```

### 4.3 跨设备链路聚合（M-LAG）

```bash
# 配置 M-LAG（需要两台交换机）
# 交换机 A
sysname SW-A
stack
 stack enable
 stack member 1 priority 150
 quit

# 配置 DFS 组
dfs-group 1
 quit

interface Eth-Trunk 10
 description M-LAG-Port
 mode lacp
 dfs-group 1 m-lag
 quit

# 交换机 B 配置类似
```

---

## 5. 生成树协议

### 5.1 STP 基础配置

```bash
# 启用 STP
stp enable

# 配置 STP 模式
stp mode stp      # 传统 STP
stp mode rstp     # 快速 STP（推荐）
stp mode mstp     # 多实例 STP

# 配置优先级（值越小优先级越高，4096 的倍数）
stp priority 0      # 根桥
stp priority 4096   # 备份根桥
stp priority 8192

# 查看 STP 状态
display stp
display stp brief
```

### 5.2 RSTP 配置

```bash
# 启用 RSTP
stp mode rstp
stp enable

# 配置边缘端口（连接终端）
interface GigabitEthernet 0/0/1
 stp edged-port enable
 quit

# 配置 BPDU 保护
stp bpdu-protection

# 配置根保护
interface GigabitEthernet 0/0/24
 stp root-protection
 quit

# 配置环路保护
interface GigabitEthernet 0/0/23
 stp loop-protection
 quit
```

### 5.3 MSTP 配置

```bash
# 配置 MSTP
stp mode mstp
stp enable

# 创建 MST 域
stp region-configuration
 region-name Huawei-MSTP
 instance 1 vlan 10 20
 instance 2 vlan 30 40
 active region-configuration
 quit

# 配置实例优先级
stp instance 1 priority 0
stp instance 2 priority 4096

# 查看 MSTP 状态
display stp region-configuration
display stp instance 1
display stp instance 2
```

### 5.4 STP 优化

```bash
# 配置 TC 保护
stp tc-protection

# 配置 TC 保护阈值
stp tc-protection threshold 10

# 禁用指定端口的 STP（慎用）
interface GigabitEthernet 0/0/1
 stp disable
 quit

# 配置 STP 计时器
stp timer hello 2
stp timer forward-delay 15
stp timer max-age 20
```

---

## 6. 路由配置

### 6.1 静态路由

```bash
# 配置静态路由
ip route-static 192.168.100.0 255.255.255.0 10.0.0.1
ip route-static 192.168.200.0 24 10.0.0.1

# 配置默认路由
ip route-static 0.0.0.0 0.0.0.0 10.0.0.1

# 配置浮动静态路由（备份路由）
ip route-static 0.0.0.0 0.0.0.0 10.0.0.1 preference 60
ip route-static 0.0.0.0 0.0.0.0 10.0.0.2 preference 100

# 查看路由表
display ip routing-table
display ip routing-table protocol static
```

### 6.2 OSPF 配置

```bash
# 启用 OSPF
ospf 1 router-id 1.1.1.1

# 配置区域
area 0
 network 192.168.1.0 0.0.0.255
 network 10.0.0.0 0.0.0.3
 quit

# 配置被动接口（不发送 OSPF 报文）
ospf 1
 silent-interface Vlanif 10
 quit

# 配置 OSPF 优先级
interface Vlanif 10
 ospf dr-priority 100
 quit

# 查看 OSPF 状态
display ospf peer
display ospf routing
display ospf lsdb
```

### 6.3 OSPF 多区域

```bash
ospf 1 router-id 1.1.1.1

# 骨干区域
area 0
 network 10.0.0.0 0.0.0.3
 quit

# 普通区域
area 1
 network 192.168.1.0 0.0.0.255
 network 192.168.2.0 0.0.0.255
 quit

# Stub 区域
area 2
 stub
 network 192.168.3.0 0.0.0.255
 quit

# NSSA 区域
area 3
 nssa
 network 192.168.4.0 0.0.0.255
 quit
```

### 6.4 BGP 配置

```bash
# 启用 BGP
bgp 65001
 router-id 1.1.1.1

# 配置对等体
peer 10.0.0.2 as-number 65001
peer 10.0.0.3 as-number 65002

# 配置网络宣告
network 192.168.0.0 255.255.0.0

# 查看 BGP 状态
display bgp peer
display bgp routing-table
```

---

## 7. ACL 与安全

### 7.1 基本 ACL（2000-2999）

```bash
# 创建基本 ACL
acl number 2000
 description Allow-Admin-Subnet
 rule 5 permit source 192.168.1.0 0.0.0.255
 rule 10 deny source any
 quit

# 应用 ACL
user-interface vty 0 4
 acl 2000 inbound
 quit
```

### 7.2 高级 ACL（3000-3999）

```bash
# 创建高级 ACL
acl number 3000
 description Web-Server-Access
 rule 5 permit tcp source any destination 192.168.10.100 0 destination-port eq 80
 rule 10 permit tcp source any destination 192.168.10.100 0 destination-port eq 443
 rule 15 deny ip source any destination any
 quit

# 应用 ACL 到接口
interface GigabitEthernet 0/0/1
 traffic-filter inbound acl 3000
 quit
```

### 7.3 二层 ACL（4000-4999）

```bash
# 创建二层 ACL
acl number 4000
 description Block-MAC
 rule 5 deny source-mac 00e0-fc12-3456 ffff-ffff-ffff
 rule 10 permit
 quit

# 应用二层 ACL
interface GigabitEthernet 0/0/1
 traffic-filter inbound acl 4000
 quit
```

### 7.4 端口安全

```bash
# 配置端口安全
interface GigabitEthernet 0/0/1
 port-security enable
 port-security max-mac-count 5
 port-security protect-action restrict
 quit

# 配置静态 MAC 绑定
interface GigabitEthernet 0/0/1
 mac-address static 00e0-fc12-3456 vlan 10
 quit

# 查看端口安全状态
display port-security
display mac-address
```

### 7.5 DHCP Snooping

```bash
# 启用 DHCP Snooping
dhcp snooping enable

# 配置信任端口（连接 DHCP 服务器）
interface GigabitEthernet 0/0/24
 dhcp snooping trusted
 quit

# 配置非信任端口（连接用户）
interface GigabitEthernet 0/0/1
 dhcp snooping untrusted
 quit

# 启用 DAI（动态 ARP 检测）
arp anti-attack check user-bind enable

# 查看 DHCP Snooping 状态
display dhcp snooping configuration
display dhcp snooping user-bind all
```

### 7.6 IP Source Guard

```bash
# 启用 IP Source Guard
interface GigabitEthernet 0/0/1
 ip source check user-bind enable
 quit

# 配置静态绑定
user-bind static ip-address 192.168.10.100 mac-address 00e0-fc12-3456 vlan 10 interface GigabitEthernet 0/0/1
```

---

## 8. QoS 配置

### 8.1 流量分类

```bash
# 创建 ACL
acl number 3001
 rule 5 permit tcp destination-port eq 80
 rule 10 permit tcp destination-port eq 443
 quit

# 创建流分类
traffic classifier WEB operator or
 if-match acl 3001
 quit

traffic classifier VOIP operator or
 if-match dscp ef
 quit
```

### 8.2 流量行为

```bash
# 创建流行为
traffic behavior WEB
 remark dscp af21
 queue af bandwidth pct 30
 quit

traffic behavior VOIP
 remark dscp ef
 queue ef bandwidth pct 20
 quit

traffic behavior DEFAULT
 queue be bandwidth pct 50
 quit
```

### 8.3 流量策略

```bash
# 创建流量策略
traffic policy QOS-POLICY
 classifier WEB behavior WEB
 classifier VOIP behavior VOIP
 classifier DEFAULT behavior DEFAULT
 quit

# 应用流量策略
interface GigabitEthernet 0/0/1
 traffic-policy QOS-POLICY inbound
 quit
```

### 8.4 端口限速

```bash
# 入方向限速
interface GigabitEthernet 0/0/1
 qos lr inbound cir 100000  # 100Mbps
 quit

# 出方向限速
interface GigabitEthernet 0/0/1
 qos lr outbound cir 100000
 quit

# 基于流的限速
traffic behavior LIMIT
 car cir 10000 cbs 2000000
 quit
```

---

## 9. 堆叠与集群

### 9.1 堆叠配置（S5700/S6700）

```bash
# 交换机 A（Master）
sysname SW-Stack-A
stack
 stack enable
 stack member 1 priority 150
 stack port 0/1 enable
 stack port 0/2 enable
 quit

# 交换机 B（Slave）
sysname SW-Stack-B
stack
 stack enable
 stack member 2 priority 100
 stack port 0/1 enable
 stack port 0/2 enable
 quit

# 配置堆叠域名（防止堆叠分裂）
stack
 stack domain 10
 quit

# 查看堆叠状态
display stack
display stack topology
display stack members
```

### 9.2 集群配置（S7700/S9700）

```bash
# 配置 CSS（集群交换机系统）
# 使用集群卡
set css mode css-card
css enable
css id 1
css priority 100
css port interface 40GE 1/0/0 1/0/1

# 重启生效
reboot

# 查看集群状态
display css status
display css topology
```

### 9.3 堆叠分裂检测

```bash
# 配置 MAD（多主检测）
# LACP 检测
interface Eth-Trunk 10
 mad enable
 quit

# 直连检测
interface GigabitEthernet 0/0/25
 mad direct enable
 quit

# 查看 MAD 状态
display mad verbose
```

---

## 10. 监控与维护

### 10.1 基本信息查看

```bash
# 查看设备信息
display device
display version
display elabel

# 查看接口状态
display interface brief
display interface GigabitEthernet 0/0/1

# 查看 VLAN 信息
display vlan
display vlan 10

# 查看 MAC 地址表
display mac-address
display mac-address vlan 10

# 查看 ARP 表
display arp
display arp vlan 10
```

### 10.2 日志与告警

```bash
# 查看日志
display logbuffer
display logbuffer reverse
display logbuffer level 6

# 配置日志主机
info-center enable
info-center loghost 192.168.1.100
info-center loghost level 6

# 配置告警
info-center trapbuffer size 1024
display trapbuffer

# 保存日志
save logbuffer
```

### 10.3 性能监控

```bash
# 查看 CPU 使用率
display cpu-usage
display cpu-usage history

# 查看内存使用率
display memory-usage
display memory-usage history

# 查看接口流量
display interface GigabitEthernet 0/0/1
display interface counters rate

# 查看温度与风扇
display environment
display fan
display power
```

### 10.4 诊断命令

```bash
# Ping 测试
ping 192.168.1.1
ping -a 192.168.1.10 192.168.2.1  # 指定源地址
ping -c 100 192.168.1.1  # 指定次数

# Tracert 测试
tracert 192.168.2.1

# 环回测试
interface GigabitEthernet 0/0/1
 loopback internal
 quit

# 电缆测试
cable-test interface GigabitEthernet 0/0/1
```

### 10.5 远程镜像

```bash
# 配置远程端口镜像
# 源交换机
observe-server 1 destination-ip 192.168.100.100 source-ip 192.168.1.10
interface GigabitEthernet 0/0/1
 port-mirroring to observe-server 1 inbound
 quit

# 目的交换机
observe-server 1
interface GigabitEthernet 0/0/24
 port-mirroring observe-server 1 inbound
 quit
```

---

## 11. 故障处理案例（25 例）

### 案例 1：端口无法 Up

**现象：** 端口显示 DOWN 状态

**排查步骤：**
```bash
# 1. 检查端口状态
display interface GigabitEthernet 0/0/1

# 2. 检查是否被 shutdown
display current-configuration interface GigabitEthernet 0/0/1

# 3. 检查对端设备
# 确认对端端口是否开启

# 4. 检查线缆
# 更换网线或光模块

# 5. 强制端口 Up
interface GigabitEthernet 0/0/1
 undo shutdown
 speed 1000
 duplex full
 quit
```

**解决：** 更换故障光模块后恢复正常

---

### 案例 2：VLAN 间无法通信

**现象：** 不同 VLAN 用户无法互访

**排查步骤：**
```bash
# 1. 检查 VLANIF 接口
display ip interface brief

# 2. 检查 VLANIF 状态
display interface Vlanif 10
display interface Vlanif 20

# 3. 检查路由表
display ip routing-table

# 4. 检查 ACL
display acl all

# 5. 测试连通性
ping -a 192.168.10.1 192.168.20.1
```

**解决：** VLANIF 接口被 shutdown，执行 undo shutdown 恢复

---

### 案例 3：DHCP 无法获取 IP

**现象：** 客户端无法获取 IP 地址

**排查步骤：**
```bash
# 1. 检查 DHCP 服务
display dhcp server statistics

# 2. 检查 DHCP Snooping
display dhcp snooping configuration

# 3. 检查信任端口
display dhcp snooping trusted

# 4. 检查地址池
display dhcp server ip-in-use all

# 5. 检查中继配置
display current-configuration | include dhcp relay
```

**解决：** DHCP 中继未配置，添加以下配置：
```bash
interface Vlanif 10
 dhcp select relay
 dhcp relay server-ip 192.168.100.10
 quit
```

---

### 案例 4：生成树环路

**现象：** 网络广播风暴，CPU 飙升

**排查步骤：**
```bash
# 1. 检查 STP 状态
display stp brief

# 2. 查看根桥
display stp root

# 3. 检查端口状态
display interface brief | include DOWN

# 4. 查看日志
display logbuffer | include STP

# 5. 临时关闭可疑端口
interface GigabitEthernet 0/0/10
 shutdown
 quit
```

**解决：** 发现非授权交换机接入，启用 BPDU 保护：
```bash
stp bpdu-protection
```

---

### 案例 5：Eth-Trunk 成员端口 Down

**现象：** Eth-Trunk 中部分成员端口 Down

**排查步骤：**
```bash
# 1. 检查 Eth-Trunk 状态
display eth-trunk 1

# 2. 检查成员端口
display interface GigabitEthernet 0/0/23
display interface GigabitEthernet 0/0/24

# 3. 检查 LACP 状态
display lacp statistics eth-trunk 1

# 4. 检查配置一致性
display current-configuration interface GigabitEthernet 0/0/23
display current-configuration interface GigabitEthernet 0/0/24
```

**解决：** 成员端口配置不一致，统一配置后恢复

---

### 案例 6：OSPF 邻居无法建立

**现象：** OSPF 邻居状态卡在 Init 或 2-Way

**排查步骤：**
```bash
# 1. 检查 OSPF 邻居
display ospf peer

# 2. 检查接口配置
display ospf interface

# 3. 检查 Hello 间隔
display current-configuration | include ospf timer

# 4. 检查区域 ID
display ospf brief

# 5. 检查认证
display current-configuration | include ospf authentication
```

**解决：** 两端 Hello 间隔不一致，统一为 10 秒：
```bash
interface Vlanif 10
 ospf timer hello 10
 quit
```

---

### 案例 7：ACL 导致业务中断

**现象：** 配置 ACL 后部分业务无法访问

**排查步骤：**
```bash
# 1. 查看 ACL 配置
display acl all

# 2. 查看 ACL 匹配统计
display acl 3000

# 3. 检查接口应用
display traffic-filter applied-record

# 4. 临时移除 ACL
interface GigabitEthernet 0/0/1
 undo traffic-filter inbound
 quit

# 5. 测试连通性
ping 192.168.10.100
```

**解决：** ACL 规则顺序错误，调整规则优先级：
```bash
acl number 3000
 undo rule 5
 rule 1 permit tcp destination 192.168.10.100 0 destination-port eq 443
 rule 2 permit tcp destination 192.168.10.100 0 destination-port eq 80
 rule 100 deny ip
 quit
```

---

### 案例 8：端口安全触发

**现象：** 端口突然无法使用，日志显示 port-security

**排查步骤：**
```bash
# 1. 查看端口安全状态
display port-security

# 2. 查看告警日志
display logbuffer | include port-security

# 3. 查看 MAC 地址表
display mac-address interface GigabitEthernet 0/0/1

# 4. 清除违规 MAC
reset port-security interface GigabitEthernet 0/0/1

# 5. 恢复端口
interface GigabitEthernet 0/0/1
 undo shutdown
 quit
```

**解决：** 调整最大 MAC 数量限制：
```bash
interface GigabitEthernet 0/0/1
 port-security max-mac-count 10
 quit
```

---

### 案例 9：CPU 使用率过高

**现象：** CPU 持续高于 80%

**排查步骤：**
```bash
# 1. 查看 CPU 使用率
display cpu-usage

# 2. 查看进程占用
display cpu-usage task

# 3. 查看日志
display logbuffer

# 4. 检查广播流量
display interface | include broadcast

# 5. 检查 ARP 攻击
display arp anti-attack statistics
```

**解决：** 发现 ARP 攻击，启用 ARP 限速：
```bash
interface GigabitEthernet 0/0/1
 arp rate-limit 100
 quit
```

---

### 案例 10：内存泄漏

**现象：** 内存使用率持续增长

**排查步骤：**
```bash
# 1. 查看内存使用率
display memory-usage

# 2. 查看内存历史
display memory-usage history

# 3. 查看进程内存
display memory-usage task

# 4. 收集诊断信息
display diagnostic-information

# 5. 重启设备（最后手段）
reboot
```

**解决：** 升级到最新 VRP 版本修复内存泄漏 Bug

---

### 案例 11：堆叠分裂

**现象：** 堆叠系统分裂，出现双主

**排查步骤：**
```bash
# 1. 查看堆叠状态
display stack

# 2. 查看堆叠拓扑
display stack topology

# 3. 检查 MAD 状态
display mad verbose

# 4. 查看日志
display logbuffer | include MAD

# 5. 检查堆叠线缆
# 确认堆叠线缆连接正常
```

**解决：** 修复堆叠线缆，重启备用交换机重新加入堆叠

---

### 案例 12：光模块不兼容

**现象：** 端口无法 Up，日志显示光模块告警

**排查步骤：**
```bash
# 1. 查看光模块信息
display transceiver interface GigabitEthernet 0/0/1

# 2. 查看告警
display alarm active

# 3. 查看日志
display logbuffer | include transceiver

# 4. 更换光模块
# 使用华为认证光模块

# 5. 强制端口 Up（临时）
interface GigabitEthernet 0/0/1
 undo transceiver phony-alarm-disable
 quit
```

**解决：** 更换为华为认证光模块

---

### 案例 13：PoE 供电不足

**现象：** IP 电话/AP 无法启动

**排查步骤：**
```bash
# 1. 查看 PoE 状态
display poe interface

# 2. 查看 PoE 功率
display poe power

# 3. 查看告警
display alarm active | include PoE

# 4. 调整供电优先级
interface GigabitEthernet 0/0/1
 poe priority critical
 quit

# 5. 关闭非关键端口 PoE
interface GigabitEthernet 0/0/24
 undo poe enable
 quit
```

**解决：** 增加 PoE 交换机或调整供电优先级

---

### 案例 14：镜像端口无法抓包

**现象：** 镜像端口无流量

**排查步骤：**
```bash
# 1. 查看镜像配置
display observe-server

# 2. 查看端口镜像
display port-mirroring

# 3. 检查镜像会话
display mirroring-group all

# 4. 检查目的端口
display interface GigabitEthernet 0/0/24

# 5. 重新配置镜像
undo observe-server 1
observe-server 1 destination-ip 192.168.100.100 source-ip 192.168.1.10
```

**解决：** 镜像配置错误，重新配置后正常

---

### 案例 15：NTP 时间不同步

**现象：** 交换机时间与 NTP 服务器不一致

**排查步骤：**
```bash
# 1. 查看 NTP 状态
display ntp-service status

# 2. 查看 NTP 会话
display ntp-service sessions

# 3. 检查 NTP 配置
display current-configuration | include ntp

# 4. 测试 NTP 服务器连通性
ping 192.168.1.100

# 5. 重新配置 NTP
undo ntp-service unicast-server 192.168.1.100
ntp-service unicast-server 192.168.1.100
```

**解决：** NTP 服务器防火墙阻止，开放 UDP 123 端口后正常

---

### 案例 16：SSH 无法登录

**现象：** SSH 连接被拒绝

**排查步骤：**
```bash
# 1. 检查 SSH 服务
display ssh server status

# 2. 检查 SSH 用户
display ssh user-information

# 3. 检查 VTY 配置
display current-configuration | include user-interface vty

# 4. 检查 ACL
display acl all

# 5. 重启 SSH 服务
undo ssh server enable
ssh server enable
```

**解决：** SSH 密钥损坏，重新生成：
```bash
undo rsa local-key-pair create
rsa local-key-pair create 2048
```

---

### 案例 17：VLAN 批量配置失败

**现象：** 批量创建 VLAN 时部分失败

**排查步骤：**
```bash
# 1. 查看已有 VLAN
display vlan

# 2. 查看 VLAN 资源
display vlan resource

# 3. 检查系统限制
display device

# 4. 逐个创建 VLAN
vlan 10
 quit
vlan 20
 quit

# 5. 检查 License
display license
```

**解决：** 超出 VLAN 数量限制，升级 License 后正常

---

### 案例 18：接口流量异常

**现象：** 某接口流量突增

**排查步骤：**
```bash
# 1. 查看接口流量
display interface GigabitEthernet 0/0/1

# 2. 查看流量统计
display interface counters rate

# 3. 查看 MAC 地址
display mac-address interface GigabitEthernet 0/0/1

# 4. 启用流量监控
traffic-statistic enable

# 5. 限速
interface GigabitEthernet 0/0/1
 qos lr inbound cir 50000
 quit
```

**解决：** 发现环路，启用 STP 后正常

---

### 案例 19：配置无法保存

**现象：** 重启后配置丢失

**排查步骤：**
```bash
# 1. 检查存储空间
dir

# 2. 检查配置文件
display saved-configuration

# 3. 手动保存
save

# 4. 检查存储设备
display device

# 5. 备份配置
tftp 192.168.1.100 put flash:/vrpcfg.zip
```

**解决：** Flash 空间不足，清理后重新保存

---

### 案例 20：BGP 路由震荡

**现象：** BGP 路由频繁变化

**排查步骤：**
```bash
# 1. 查看 BGP 邻居
display bgp peer

# 2. 查看 BGP 路由
display bgp routing-table

# 3. 查看日志
display logbuffer | include BGP

# 4. 启用路由阻尼
bgp 65001
 dampening
 quit

# 5. 调整 Keepalive
bgp 65001
 timer keepalive 30 hold 90
 quit
```

**解决：** 链路质量差，启用路由阻尼后稳定

---

### 案例 21：MSTP 区域不匹配

**现象：** MSTP 端口被阻塞

**排查步骤：**
```bash
# 1. 查看 MSTP 配置
display stp region-configuration

# 2. 查看 MSTP 状态
display stp brief

# 3. 对比两端配置
# 确认域名、修订级别、实例 VLAN 映射一致

# 4. 重新配置 MSTP
stp region-configuration
 region-name Huawei-MSTP
 revision-level 1
 instance 1 vlan 10 to 20
 active region-configuration
 quit
```

**解决：** 修订级别不一致，统一后正常

---

### 案例 22：DHCP 地址池耗尽

**现象：** 新设备无法获取 IP

**排查步骤：**
```bash
# 1. 查看地址池使用率
display dhcp server ip-in-use all

# 2. 查看地址池统计
display dhcp server statistics

# 3. 检查租期
display current-configuration | include dhcp server

# 4. 缩短租期
dhcp server ip-pool VLAN10
 network 192.168.10.0 mask 255.255.255.0
 gateway-list 192.168.10.1
 expired day 1
 quit

# 5. 扩大地址池
dhcp server ip-pool VLAN10
 network 192.168.10.0 mask 255.255.254.0
 quit
```

**解决：** 缩短租期并扩大地址池

---

### 案例 23：QoS 策略不生效

**现象：** 配置 QoS 后流量未限速

**排查步骤：**
```bash
# 1. 查看流量策略
display traffic policy

# 2. 查看应用记录
display traffic-policy applied-record

# 3. 查看流分类
display traffic classifier

# 4. 查看流行为
display traffic behavior

# 5. 检查硬件支持
display qos queue statistics
```

**解决：** 流分类匹配条件错误，修正 ACL 后正常

---

### 案例 24：链路聚合负载不均

**现象：** Eth-Trunk 中流量集中在单条链路

**排查步骤：**
```bash
# 1. 查看 Eth-Trunk 状态
display eth-trunk 1

# 2. 查看负载分担模式
display eth-trunk 1 load-balance

# 3. 查看流量统计
display interface Eth-Trunk 1 counters rate

# 4. 调整负载分担算法
load-balance dst-ip
# 或
load-balance src-dst-ip

# 5. 检查成员端口
display interface GigabitEthernet 0/0/23
display interface GigabitEthernet 0/0/24
```

**解决：** 调整负载分担算法为 src-dst-ip 后均衡

---

### 案例 25：设备无法启动

**现象：** 交换机启动失败

**排查步骤：**
```bash
# 1. 查看启动文件
display boot-loader

# 2. 查看存储文件
dir

# 3. 指定启动文件
boot-loader file flash:/V200R019C00SPC500.cc all

# 4. 检查配置文件
display saved-configuration

# 5. 恢复出厂设置
reset saved-configuration
reboot
```

**解决：** 启动文件损坏，从 TFTP 重新加载系统文件

---

## 12. 最佳实践

### ✅ 配置规范

1. **命名规范**
   - 设备命名：位置 - 角色 - 编号（如 BJ-Core-SW01）
   - 接口描述：对端设备 - 对端接口
   - VLAN 命名：部门/功能

2. **安全配置**
   - 禁用 Telnet，使用 SSH
   - 配置 AAA 认证
   - 启用端口安全
   - 配置 ACL 限制管理访问

3. **高可用配置**
   - 配置 STP/RSTP/MSTP
   - 配置 Eth-Trunk 链路聚合
   - 配置堆叠/集群
   - 配置 VRRP 网关冗余

4. **监控配置**
   - 配置 NTP 时间同步
   - 配置日志服务器
   - 配置 SNMP 监控
   - 配置告警通知

### ✅ 维护规范

1. **变更前**
   - 备份当前配置
   - 评估变更风险
   - 准备回退方案

2. **变更中**
   - 逐条执行命令
   - 实时验证结果
   - 记录变更过程

3. **变更后**
   - 保存配置
   - 验证业务正常
   - 更新文档

### ✅ 巡检清单

```bash
# 每日巡检
display device
display interface brief
display logbuffer
display cpu-usage
display memory-usage

# 每周巡检
display vlan
display stp brief
display eth-trunk
display ip routing-table
display arp

# 每月巡检
display version
display license
display environment
display fan
display power
```

---

## 📋 快速参考卡片

```bash
# ===== 基础命令 =====
system-view                 # 进入配置模式
save                        # 保存配置
display current-configuration  # 查看当前配置
display saved-configuration    # 查看保存的配置

# ===== 接口配置 =====
interface GigabitEthernet 0/0/1
 description To-Server
 port link-type access
 port default vlan 10
 quit

# ===== VLAN 配置 =====
vlan batch 10 to 30
interface Vlanif 10
 ip address 192.168.10.1 24
 quit

# ===== 路由配置 =====
ip route-static 0.0.0.0 0.0.0.0 192.168.1.1
ospf 1 router-id 1.1.1.1
 area 0
  network 192.168.0.0 0.0.255.255

# ===== SSH 配置 =====
ssh server enable
rsa local-key-pair create 2048
aaa
 local-user admin service-type ssh
 quit

# ===== 故障排查 =====
display interface brief       # 查看接口状态
display vlan                  # 查看 VLAN
display stp brief            # 查看 STP
display ip routing-table     # 查看路由表
display logbuffer            # 查看日志
display cpu-usage            # 查看 CPU
display memory-usage         # 查看内存
```

---

## 🔗 相关资源

- **华为官方文档：** https://support.huawei.com/enterprise/zh/doc/EDOC1100064896
- **VRP 命令参考：** https://support.huawei.com/hedex/hdx.do?docid=EDOC1100064896
- **华为企业支持：** https://support.huawei.com/enterprise/

---

> 💡 **刺刺提醒：** 
> 1. 配置前先保存！配置前先保存！配置前先保存！😈
> 2. 生产环境变更请在维护窗口进行！
> 3. 遇到环路先拔线，再查 STP！
> 4. 备份配置比恢复配置容易一万倍！
## 常用指令

- display current-configuration
- display interface brief
- display interface GigabitEthernet 0/0/1
- display vlan
- display ip interface brief
- display ip routing-table
- display logbuffer
- display stp brief
- display mac-address
- display arp
- ping <target-ip>
- tracert <target-ip>
- save

