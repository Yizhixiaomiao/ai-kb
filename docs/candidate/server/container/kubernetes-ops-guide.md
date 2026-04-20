# Kubernetes 运维参考手册

```yaml
status: usable
type: reference
risk_level: high
review_required: true
source: imported-manual
source_path: D:/Work/工作文档/知识库构建/服务器运维相关/kubernetes-ops-guide.md
asset_types: [server, container, cluster]
systems: [kubernetes, containerd, linux]
issue_types: [cluster-ops, pod-failed, deployment, troubleshooting]
tags: [kubernetes, k8s, pod, deployment, service, ingress, helm, KubernetesPod不健康, Pod不健康, CrashLoopBackOff, ImagePullBackOff, NotReady]
```

## 适用范围

- 适用于 Kubernetes 集群部署、节点维护、Pod/Deployment/Service/Ingress/Helm 等资源运维和常见故障排查。
- 适合作为集群级问题定位和变更前检查参考。

## 常见现象

- Pod Pending、CrashLoopBackOff、ImagePullBackOff 或调度失败。
- Service、Ingress、DNS、存储或网络访问异常。
- 节点 NotReady、资源不足、证书或权限异常。
- Helm 发布失败或回滚异常。

## 处理步骤

1. 确认集群、命名空间、业务影响范围和操作权限。
2. 优先执行只读检查：查看节点、Pod、事件、日志、资源配额和最近变更。
3. 按故障类型进入原始手册中的资源管理、网络、存储、配置、Helm 或故障排查章节。
4. 涉及重启组件、删除资源、扩缩容、升级、证书和 etcd 操作前，必须先备份并在维护窗口执行。
5. 记录命名空间、资源名、关键事件、处理动作和验证结果。

## 验证方式

- 目标 Pod、Deployment、Service 或 Ingress 状态恢复。
- 业务健康检查、日志和访问路径正常。
- 集群节点和关键系统组件无新增异常事件。

## 注意事项

- 本文属于服务器、数据库或网络设备高风险运维参考，生产环境操作前必须完成审批、备份、维护窗口和回退方案确认。
- 本文中的命令和参数来自通用手册，执行前必须替换为本公司实际环境，并先在测试环境验证。
- 涉及删除、覆盖、重启、恢复、扩缩容、路由/ACL 变更、证书/密钥、数据库恢复等动作时，不允许直接照抄执行。
- 手册中的示例密码、Token 和密钥已做脱敏处理；不得在知识库中保存真实凭据。

## 原始手册

以下内容为导入的原始手册正文，供工程师查阅细节。

# Kubernetes 运维完全指南

> 📝 版本：Kubernetes 1.28+  
> ⚠️ 生产环境操作前请先在测试环境验证！

---

## 📚 目录

1. [Kubernetes 架构概览](#1-kubernetes-架构概览)
2. [集群部署（手动）](#2-集群部署手动)
3. [集群部署（kubeadm）](#3-集群部署 kubeadm)
4. [kubectl 基础命令](#4-kubectl-基础命令)
5. [工作负载管理](#5-工作负载管理)
6. [网络与服务](#6-网络与服务)
7. [存储管理](#7-存储管理)
8. [配置与密钥](#8-配置与密钥)
9. [Helm 包管理](#9-helm-包管理)
10. [监控与日志](#10-监控与日志)
11. [故障排查（30 例）](#11-故障排查 30 例)
12. [最佳实践](#12-最佳实践)

---

## 1. Kubernetes 架构概览

### 1.1 核心组件

| 组件 | 作用 | 端口 |
|------|------|------|
| **kube-apiserver** | API 入口，所有请求的网关 | 6443 |
| **etcd** | 分布式键值存储，保存集群状态 | 2379-2380 |
| **kube-scheduler** | 调度 Pod 到节点 | - |
| **kube-controller-manager** | 运行各种控制器 | - |
| **kubelet** | 节点代理，管理 Pod 生命周期 | 10250 |
| **kube-proxy** | 网络代理，实现 Service | - |
| **coredns** | 集群内部 DNS 服务 | 53 |

### 1.2 核心资源

| 资源类型 | 作用 | 示例 |
|----------|------|------|
| **Pod** | 最小调度单元 | 一个或多个容器 |
| **Deployment** | 无状态应用部署 | Web 服务、API |
| **StatefulSet** | 有状态应用部署 | 数据库、缓存 |
| **DaemonSet** | 每个节点运行一个 Pod | 日志收集、监控 |
| **Service** | 服务发现与负载均衡 | ClusterIP、NodePort |
| **Ingress** | 七层路由 | HTTP/HTTPS 路由 |
| **ConfigMap** | 配置管理 | 环境变量、配置文件 |
| **Secret** | 敏感信息管理 | 密码、证书、Token |
| **PV/PVC** | 持久化存储 | 数据卷 |
| **Namespace** | 资源隔离 | 开发、测试、生产 |

### 1.3 网络模型

```
┌─────────────────────────────────────────────────┐
│                    Cluster                       │
│  ┌─────────────┐  ┌─────────────┐               │
│  │    Node 1   │  │    Node 2   │               │
│  │  ┌────────┐ │  │  ┌────────┐ │               │
│  │  │  Pod 1 │ │  │  │  Pod 3 │ │               │
│  │  │ 10.0.0.2│ │  │  │10.0.1.2│ │               │
│  │  └────────┘ │  │  └────────┘ │               │
│  │  ┌────────┐ │  │  ┌────────┐ │               │
│  │  │  Pod 2 │ │  │  │  Pod 4 │ │               │
│  │  │10.0.0.3│ │  │  │10.0.1.3│ │               │
│  │  └────────┘ │  │  └────────┘ │               │
│  └─────────────┘  └─────────────┘               │
│         │                │                       │
│         └───────┬────────┘                       │
│                 │                                │
│          ┌──────▼──────┐                         │
│          │   Service   │                         │
│          │ 10.96.0.100 │                         │
│          └──────┬──────┘                         │
│                 │                                │
└─────────────────┼────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │    Ingress      │
         │  example.com    │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │   外部用户       │
         └─────────────────┘
```

---

## 2. 集群部署（手动）

### 2.1 环境准备

```bash
# 所有节点执行
# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

# 关闭 SELinux
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# 关闭 Swap
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# 配置内核参数
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
sysctl --system

# 安装 containerd
apt-get update
apt-get install -y containerd
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml

# 修改 containerd 配置（使用 systemd cgroup）
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd
```

### 2.2 安装 Kubernetes 组件

```bash
# 添加 Kubernetes 仓库
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list

# 安装 kubelet、kubeadm、kubectl
apt-get update
apt-get install -y kubelet kubeadm kubectl
systemctl enable --now kubelet
```

### 2.3 初始化 Master 节点

```bash
# 初始化集群
kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --service-cidr=10.96.0.0/12 \
  --apiserver-advertise-address=192.168.1.10 \
  --control-plane-endpoint=192.168.1.10 \
  --upload-certs

# 配置 kubectl
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

# 保存 join 命令（用于 Worker 节点加入）
kubeadm token create --print-join-command
```

### 2.4 安装网络插件（Calico）

```bash
# 下载 Calico 配置
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml -O

# 修改 POD 网段
sed -i 's/CIDR=192.168.0.0\/16/CIDR=10.244.0.0\/16/' calico.yaml

# 应用配置
kubectl apply -f calico.yaml

# 验证
kubectl get pods -n calico-system
```

### 2.5 加入 Worker 节点

```bash
# 在 Worker 节点执行（使用 Master 生成的 join 命令）
kubeadm join 192.168.1.10:6443 --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>

# 在 Master 节点验证
kubectl get nodes
```

---

## 3. 集群部署（kubeadm）

### 3.1 快速部署脚本

```bash
#!/bin/bash
# deploy-k8s.sh

# 节点角色：master 或 worker
ROLE=$1
MASTER_IP=$2

# 基础配置
configure_node() {
  # 关闭防火墙、SELinux、Swap
  systemctl stop firewalld && systemctl disable firewalld
  setenforce 0
  sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
  swapoff -a
  sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
  
  # 内核参数
  cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
  sysctl --system
  
  # 安装 containerd
  apt-get update && apt-get install -y containerd
  mkdir -p /etc/containerd
  containerd config default > /etc/containerd/config.toml
  sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
  systemctl restart containerd
  
  # 安装 Kubernetes
  curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
  echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
  apt-get update && apt-get install -y kubelet kubeadm kubectl
  systemctl enable --now kubelet
}

# 初始化 Master
init_master() {
  kubeadm init \
    --pod-network-cidr=10.244.0.0/16 \
    --service-cidr=10.96.0.0/12 \
    --apiserver-advertise-address=$(hostname -I | awk '{print $1}')
  
  mkdir -p $HOME/.kube
  cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  chown $(id -u):$(id -g) $HOME/.kube/config
  
  # 安装 Calico
  kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml
  kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml
  
  echo "Master 初始化完成！"
  echo "Worker 节点加入命令："
  kubeadm token create --print-join-command
}

# 加入集群
join_cluster() {
  $MASTER_IP
}

# 主逻辑
configure_node
if [ "$ROLE" == "master" ]; then
  init_master
else
  join_cluster
fi
```

### 3.2 高可用集群部署

```bash
# 使用 Keepalived + HAProxy 实现高可用

# HAProxy 配置
cat > /etc/haproxy/haproxy.cfg << EOF
global
  log /dev/log local0
  maxconn 4096

defaults
  log global
  mode tcp
  timeout connect 5s
  timeout client 50s
  timeout server 50s

listen kubernetes-apiserver
  bind 0.0.0.0:6443
  balance roundrobin
  server master1 192.168.1.10:6443 check
  server master2 192.168.1.11:6443 check
  server master3 192.168.1.12:6443 check
EOF

# 初始化第一个 Master
kubeadm init \
  --control-plane-endpoint=192.168.1.100:6443 \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16

# 添加其他 Master
kubeadm join 192.168.1.100:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <key>

# 添加 Worker
kubeadm join 192.168.1.100:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>
```

### 3.3 验证集群状态

```bash
# 查看节点
kubectl get nodes -o wide

# 查看组件状态
kubectl get pods -n kube-system

# 查看集群信息
kubectl cluster-info

# 查看 etcd 状态
kubectl get pods -n kube-system -l component=etcd

# 运行测试 Pod
kubectl run test --image=nginx --rm -it -- bash
```

---

## 4. kubectl 基础命令

### 4.1 配置管理

```bash
# 查看配置
kubectl config view

# 切换集群
kubectl config use-context <context-name>

# 查看当前上下文
kubectl config current-context

# 设置命名空间
kubectl config set-context --current --namespace=<namespace>

# 配置自动补全
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

### 4.2 资源查看

```bash
# 查看所有资源
kubectl get all

# 查看特定资源
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get configmaps
kubectl get secrets
kubectl get pv
kubectl get pvc
kubectl get ingress

# 查看所有命名空间
kubectl get namespaces

# 查看详细信息
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl get pods -o json

# 查看标签
kubectl get pods --show-labels

# 按标签筛选
kubectl get pods -l app=nginx
kubectl get pods -l env=prod,tier=frontend

# 查看资源使用
kubectl top pods
kubectl top nodes
```

### 4.3 资源操作

```bash
# 创建资源
kubectl apply -f deployment.yaml
kubectl create -f deployment.yaml
kubectl create deployment nginx --image=nginx

# 删除资源
kubectl delete -f deployment.yaml
kubectl delete pod nginx-pod
kubectl delete deployment nginx
kubectl delete namespace test

# 编辑资源
kubectl edit deployment nginx
kubectl edit svc nginx

# 扩缩容
kubectl scale deployment nginx --replicas=5
kubectl scale deployment nginx --replicas=0

# 滚动更新
kubectl set image deployment/nginx nginx=nginx:1.21
kubectl rollout status deployment/nginx
kubectl rollout undo deployment/nginx
kubectl rollout history deployment/nginx

# 进入 Pod
kubectl exec -it nginx-pod -- bash
kubectl exec -it nginx-pod -c container-name -- bash

# 查看日志
kubectl logs nginx-pod
kubectl logs -f nginx-pod
kubectl logs nginx-pod -c container-name
kubectl logs nginx-pod --previous

# 端口转发
kubectl port-forward svc/nginx 8080:80
kubectl port-forward pod/nginx-pod 8080:80
```

### 4.4 调试命令

```bash
# 描述资源（查看详细信息和事件）
kubectl describe pod nginx-pod
kubectl describe deployment nginx
kubectl describe svc nginx

# 查看事件
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -n kube-system

# 临时调试容器
kubectl debug -it nginx-pod --image=busybox
kubectl debug -it nginx-pod --image=nicolaka/netshoot --target=nginx

# 复制文件
kubectl cp nginx-pod:/var/log/app.log ./app.log
kubectl cp ./config.json nginx-pod:/etc/app/config.json
```

---

## 5. 工作负载管理

### 5.1 Deployment（无状态应用）

```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: default
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        version: v1.0
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config-volume
          mountPath: /etc/nginx/conf.d
      volumes:
      - name: config-volume
        configMap:
          name: nginx-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: nginx
              topologyKey: kubernetes.io/hostname
```

```bash
# 部署
kubectl apply -f nginx-deployment.yaml

# 查看状态
kubectl get deployment nginx-deployment
kubectl get pods -l app=nginx

# 滚动更新
kubectl set image deployment/nginx-deployment nginx=nginx:1.22
kubectl rollout status deployment/nginx-deployment

# 回滚
kubectl rollout undo deployment/nginx-deployment
kubectl rollout undo deployment/nginx-deployment --to-revision=1

# 查看历史
kubectl rollout history deployment/nginx-deployment
```

### 5.2 StatefulSet（有状态应用）

```yaml
# mysql-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: root-password
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: standard
      resources:
        requests:
          storage: 10Gi
```

```bash
# 部署
kubectl apply -f mysql-statefulset.yaml

# 查看状态（按顺序启动）
kubectl get pods -l app=mysql
kubectl get pvc -l app=mysql

# 删除 StatefulSet（保留 PVC）
kubectl delete statefulset mysql
```

### 5.3 DaemonSet（节点级应用）

```yaml
# node-exporter-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      hostNetwork: true
      hostPID: true
      containers:
      - name: node-exporter
        image: prom/node-exporter:latest
        ports:
        - containerPort: 9100
          hostPort: 9100
        volumeMounts:
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: sys
          mountPath: /host/sys
          readOnly: true
      volumes:
      - name: proc
        hostPath:
          path: /proc
      - name: sys
        hostPath:
          path: /sys
      tolerations:
      - operator: Exists
```

### 5.4 Job/CronJob（批处理任务）

```yaml
# backup-job.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
spec:
  schedule: "0 2 * * *"  # 每天凌晨 2 点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: mysql:8.0
            command:
            - /bin/sh
            - -c
            - |
              mysqldump -h mysql -u root -p$MYSQL_ROOT_PASSWORD --all-databases | \
              gzip > /backup/backup-$(date +%F).sql.gz
            env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: root-password
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
          volumes:
          - name: backup-volume
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

```bash
# 查看 Job
kubectl get jobs
kubectl get cronjobs

# 手动触发 CronJob
kubectl create job --from=cronjob/database-backup manual-backup

# 查看 Job 日志
kubectl logs job/database-backup-xxxxx
```

---

## 6. 网络与服务

### 6.1 Service 类型

```yaml
# ClusterIP（默认，集群内部访问）
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP

---
# NodePort（节点端口暴露）
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080  # 30000-32767
  type: NodePort

---
# LoadBalancer（云负载均衡）
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer

---
# ExternalName（外部服务）
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: rds.example.com
  ports:
  - port: 3306
```

### 6.2 Headless Service

```yaml
# 用于 StatefulSet，直接访问 Pod IP
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
spec:
  selector:
    app: mysql
  clusterIP: None  # 关键配置
  ports:
  - port: 3306
    targetPort: 3306
```

### 6.3 Ingress 配置

```yaml
# nginx-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - example.com
    secretName: example-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

```bash
# 安装 NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml

# 查看 Ingress
kubectl get ingress
kubectl describe ingress nginx-ingress
```

### 6.4 Network Policy

```yaml
# 只允许特定 Pod 访问
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080

---
# 拒绝所有入站流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

### 6.5 网络故障排查

```bash
# 测试 DNS 解析
kubectl run -it --rm dns-test --image=busybox:1.28 --restart=Never -- nslookup kubernetes.default

# 测试服务连通性
kubectl run -it --rm net-test --image=nicolaka/netshoot --restart=Never -- bash
# 在 Pod 内执行
curl nginx-service.default.svc.cluster.local

# 查看 Service Endpoints
kubectl get endpoints nginx-service
kubectl describe svc nginx-service

# 查看网络策略
kubectl get networkpolicy
kubectl describe networkpolicy allow-frontend

# 抓包调试
kubectl debug -it nginx-pod --image=nicolaka/netshoot --target=nginx
# 在调试容器内
tcpdump -i any port 80
```

---

## 7. 存储管理

### 7.1 PV/PVC

```yaml
# storage-class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-data
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  hostPath:
    path: /mnt/data

---
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard

---
# 使用 PVC 的 Pod
apiVersion: v1
kind: Pod
metadata:
  name: data-pod
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: data-volume
      mountPath: /usr/share/nginx/html
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: pvc-data
```

### 7.2 动态存储（NFS）

```yaml
# nfs-storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-storage
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
parameters:
  server: 192.168.1.100
  path: /srv/nfs/k8s
  archiveOnDelete: "false"

---
# 使用动态存储的 PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs-storage
  resources:
    requests:
      storage: 5Gi
```

```bash
# 安装 NFS 动态存储
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
  --set nfs.server=192.168.1.100 \
  --set nfs.path=/srv/nfs/k8s \
  --set storageClass.name=nfs-storage
```

### 7.3 ConfigMap 和 Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    server.port=8080
    database.url=jdbc:mysql://mysql:3306/app
  log.level: INFO

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  username: admin
  password: <示例密码>
  api-key: sk-xxxxxxxxxxxx

---
# 在 Pod 中使用
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: password
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: log.level
    volumeMounts:
    - name: config-volume
      mountPath: /etc/app/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

---

## 8. Helm 包管理

### 8.1 Helm 安装与配置

```bash
# 安装 Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 验证安装
helm version

# 添加仓库
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# 更新仓库
helm repo update

# 搜索 Chart
helm search repo nginx
helm search repo mysql
helm search repo prometheus

# 查看 Chart 信息
helm show values bitnami/mysql
helm show chart bitnami/mysql
```

### 8.2 安装应用

```bash
# 安装 MySQL
helm install my-mysql bitnami/mysql \
  --namespace database \
  --create-namespace \
  --set auth.rootPassword=Root@2026 \
  --set auth.database=myapp \
  --set auth.username=appuser \
  --set auth.password=<示例密码> \
  --set primary.persistence.size=10Gi

# 安装 NGINX Ingress
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=30080

# 安装 Prometheus
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --create-namespace \
  --set alertmanager.persistentVolume.size=5Gi \
  --set server.persistentVolume.size=10Gi

# 自定义 values 文件安装
helm install my-app ./my-chart -f custom-values.yaml

# 干运行（测试安装）
helm install my-test bitnami/mysql --dry-run --debug
```

### 8.3 管理 Release

```bash
# 查看已安装的 Release
helm list
helm list -A  # 所有命名空间
helm list -n database

# 查看 Release 详情
helm status my-mysql
helm history my-mysql

# 升级 Release
helm upgrade my-mysql bitnami/mysql \
  --set primary.persistence.size=20Gi \
  --set image.tag=8.0.32

# 回滚 Release
helm rollback my-mysql 1
helm rollback my-mysql --revision 2

# 查看历史版本
helm history my-mysql

# 卸载 Release
helm uninstall my-mysql
helm uninstall my-mysql -n database

# 清理卸载残留
helm uninstall my-mysql --keep-history
```

### 8.4 创建自定义 Chart

```bash
# 创建 Chart 骨架
helm create my-app

# 目录结构
my-app/
├── Chart.yaml          # Chart 元数据
├── values.yaml         # 默认配置值
├── charts/             # 依赖的 Chart
├── templates/          # Kubernetes 模板
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── _helpers.tpl    # 模板辅助函数
│   └── NOTES.txt       # 安装后提示信息
└── .helmignore

# Chart.yaml 示例
apiVersion: v2
name: my-app
description: My Application Helm Chart
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"

# 模板示例（templates/deployment.yaml）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: {{ .Values.service.port }}

# 打包 Chart
helm package my-app

# 推送 Chart 到仓库
helm push my-app-0.1.0.tgz oci://registry.example.com/charts
```

### 8.5 常用 Helm Charts

```bash
# 监控栈（Prometheus + Grafana）
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# ELK 日志栈
helm install elasticsearch bitnami/elasticsearch \
  --namespace logging \
  --create-namespace
helm install kibana bitnami/kibana \
  --namespace logging

# Redis 集群
helm install redis bitnami/redis-cluster \
  --namespace database \
  --set cluster.nodes=6

# RabbitMQ
helm install rabbitmq bitnami/rabbitmq \
  --namespace messaging \
  --set auth.password=<示例密码>

# Kafka
helm install kafka bitnami/kafka \
  --namespace messaging \
  --set listeners=PLAINTEXT://:9092
```

---

## 9. 监控与日志

### 9.1 Prometheus + Grafana

```yaml
# prometheus-values.yaml
server:
  persistentVolume:
    enabled: true
    size: 10Gi
  retention: 15d

alertmanager:
  enabled: true
  persistentVolume:
    enabled: true
    size: 5Gi

grafana:
  enabled: true
  adminPassword: Grafana@2026
  persistence:
    enabled: true
    size: 5Gi

nodeExporter:
  enabled: true

kubeStateMetrics:
  enabled: true
```

```bash
# 安装
helm install prometheus prometheus-community/prometheus \
  -f prometheus-values.yaml \
  --namespace monitoring \
  --create-namespace

# 端口转发访问
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```

### 9.2 自定义监控规则

```yaml
# custom-alerts.yaml
groups:
- name: k8s-alerts
  rules:
  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 5 > 0
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Pod 频繁重启"
      description: "Pod {{ $labels.pod }} 在 5 分钟内重启 {{ $value }} 次"

  - alert: NodeNotReady
    expr: kube_node_status_condition{condition="Ready",status="true"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "节点不可用"
      description: "节点 {{ $labels.node }} 已离线 5 分钟"

  - alert: PVUsageHigh
    expr: (kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes) * 100 > 80
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "存储使用率过高"
      description: "PV {{ $labels.persistentvolumeclaim }} 使用率 {{ $value }}%"
```

### 9.3 日志收集（EFK/ELK）

```yaml
# fluentbit-values.yaml
config:
  inputs: |
    [INPUT]
        Name tail
        Path /var/log/containers/*.log
        Parser docker
        Tag kube.*
        Mem_Buf_Limit 5MB
        Skip_Long_Lines On
  filters: |
    [FILTER]
        Name kubernetes
        Match kube.*
        Merge_Log On
        K8S-Logging.Parser On
        K8S-Logging.Exclude On
  outputs: |
    [OUTPUT]
        Name es
        Match *
        Host elasticsearch-master.logging.svc
        Port 9200
        Logstash_Format On
        Logstash_Prefix k8s-logs
        Replace_Dots On
```

```bash
# 安装 Fluent Bit
helm install fluent-bit fluent/fluent-bit \
  -f fluentbit-values.yaml \
  --namespace logging \
  --create-namespace

# 查看日志
kubectl logs -f fluent-bit-xxxxx -n logging
```

### 9.4 常用监控命令

```bash
# 查看节点资源
kubectl top nodes

# 查看 Pod 资源
kubectl top pods
kubectl top pods -n kube-system

# 查看资源历史（需要 metrics-server）
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory

# 查看 Pod 事件
kubectl get events --sort-by='.lastTimestamp'

# 查看 Pod 状态
kubectl get pods -o wide
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName

# 查看资源配额
kubectl describe quota -n default
kubectl describe limitrange -n default
```

---

## 10. 故障排查（30 例）

### 案例 1：Pod 一直 Pending

**现象：** `kubectl get pods` 显示 Pending 状态

**排查步骤：**
```bash
# 1. 查看 Pod 详情
kubectl describe pod <pod-name>

# 2. 查看事件
kubectl get events --sort-by='.lastTimestamp'

# 3. 查看节点资源
kubectl describe nodes | grep -A 5 "Allocated resources"

# 4. 查看调度器日志
kubectl logs -n kube-system -l component=kube-scheduler

# 5. 检查资源请求
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].resources.requests}'
```

**常见原因与解决：**
| 原因 | 解决方案 |
|------|----------|
| 资源不足 | 扩容节点或减少资源请求 |
| 节点选择器不匹配 | 检查 nodeSelector/affinity |
| PV 未绑定 | 检查 StorageClass 和 PV |
| 污点容忍 | 添加 tolerations |
| Pod 反亲和性 | 调整 podAntiAffinity |

---

### 案例 2：Pod CrashLoopBackOff

**现象：** Pod 反复重启

**排查步骤：**
```bash
# 1. 查看 Pod 状态
kubectl describe pod <pod-name>

# 2. 查看日志
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # 查看上一次运行的日志

# 3. 进入调试
kubectl debug -it <pod-name> --image=busybox

# 4. 检查健康检查
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].livenessProbe}'
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].readinessProbe}'

# 5. 检查配置
kubectl get pod <pod-name> -o yaml | grep -A 10 "env:"
```

**常见原因与解决：**
| 原因 | 解决方案 |
|------|----------|
| 应用启动失败 | 检查日志，修复应用 |
| 配置错误 | 检查 ConfigMap/Secret |
| 健康检查失败 | 调整 probe 参数 |
| 内存不足 OOM | 增加内存限制 |
| 端口冲突 | 检查端口配置 |

---

### 案例 3：ImagePullBackOff

**现象：** 无法拉取镜像

**排查步骤：**
```bash
# 1. 查看事件
kubectl describe pod <pod-name>

# 2. 检查镜像名称
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].image}'

# 3. 测试拉取
docker pull <image-name>

# 4. 检查 Secret
kubectl get secrets
kubectl describe secret <registry-secret>

# 5. 查看 kubelet 日志
journalctl -u kubelet | grep -i pull
```

**解决：**
```yaml
# 创建镜像拉取 Secret
kubectl create secret docker-registry reg-secret \
  --docker-server=registry.example.com \
  --docker-username=admin \
  --docker-password=<示例密码> \
  --docker-email=admin@example.com

# 在 Pod 中使用
spec:
  imagePullSecrets:
  - name: reg-secret
```

---

### 案例 4：ErrImageNeverPull

**现象：** 配置了 ImagePullPolicy: Never 但镜像不存在

**排查步骤：**
```bash
# 1. 检查本地镜像
crictl images | grep <image-name>
docker images | grep <image-name>

# 2. 检查 PullPolicy
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].imagePullPolicy}'

# 3. 手动拉取
crictl pull <image-name>
```

**解决：** 修改 PullPolicy 或预加载镜像到节点

---

### 案例 5：Pod OOMKilled

**现象：** Pod 因内存不足被杀死

**排查步骤：**
```bash
# 1. 查看 Pod 状态
kubectl describe pod <pod-name> | grep -A 5 "Last State"

# 2. 查看 OOM 事件
kubectl get events | grep -i oom

# 3. 查看内存使用
kubectl top pod <pod-name>

# 4. 检查限制配置
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].resources}'
```

**解决：**
```yaml
# 增加内存限制
resources:
  requests:
    memory: "256Mi"
  limits:
    memory: "512Mi"
```

---

### 案例 6：Service 无法访问

**现象：** Service 无法连通

**排查步骤：**
```bash
# 1. 检查 Service
kubectl get svc <svc-name>
kubectl describe svc <svc-name>

# 2. 检查 Endpoints
kubectl get endpoints <svc-name>
kubectl describe endpoints <svc-name>

# 3. 检查 Pod 标签
kubectl get pods --show-labels
kubectl get pods -l <label-selector>

# 4. 测试连通性
kubectl run test --image=busybox --rm -it -- wget <svc-name>:<port>

# 5. 检查 kube-proxy
kubectl get pods -n kube-system -l k8s-app=kube-proxy
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| 标签不匹配 | 修正 selector |
| Pod 未就绪 | 检查 readinessProbe |
| kube-proxy 异常 | 重启 kube-proxy Pod |
| NetworkPolicy 阻止 | 检查网络策略 |

---

### 案例 7：DNS 解析失败

**现象：** Pod 内无法解析服务名

**排查步骤：**
```bash
# 1. 测试 DNS
kubectl run -it --rm dns-test --image=busybox:1.28 --restart=Never -- nslookup kubernetes.default

# 2. 检查 CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns

# 3. 检查 CoreDNS 配置
kubectl get cm coredns -n kube-system -o yaml

# 4. 检查 Pod DNS 配置
kubectl get pod <pod-name> -o jsonpath='{.spec.dnsPolicy}'
kubectl get pod <pod-name> -o jsonpath='{.spec.dnsConfig}'
```

**解决：**
```yaml
# 修复 CoreDNS
kubectl edit cm coredns -n kube-system

# 或重启 CoreDNS
kubectl rollout restart deployment/coredns -n kube-system
```

---

### 案例 8：Ingress 404/503

**现象：** Ingress 返回 404 或 503 错误

**排查步骤：**
```bash
# 1. 检查 Ingress
kubectl get ingress
kubectl describe ingress <ingress-name>

# 2. 检查后端 Service
kubectl get svc <backend-svc>
kubectl get endpoints <backend-svc>

# 3. 检查 Ingress Controller
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 4. 测试后端
kubectl run test --image=busybox --rm -it -- wget <svc-name>:<port>

# 5. 检查 TLS Secret
kubectl get secret <tls-secret>
kubectl describe secret <tls-secret>
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| 后端 Service 不存在 | 创建 Service |
| Endpoints 为空 | 检查 Pod 标签 |
| Ingress Class 不匹配 | 设置正确的 ingressClassName |
| TLS 证书问题 | 更新 Secret |

---

### 案例 9：PV/PVC 无法绑定

**现象：** PVC 一直 Pending

**排查步骤：**
```bash
# 1. 查看 PVC 状态
kubectl get pvc
kubectl describe pvc <pvc-name>

# 2. 查看 PV 状态
kubectl get pv
kubectl describe pv <pv-name>

# 3. 检查 StorageClass
kubectl get storageclass
kubectl describe storageclass <sc-name>

# 4. 查看事件
kubectl get events | grep -i pvc
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| 没有匹配 PV | 创建 PV 或启用动态供应 |
| StorageClass 不存在 | 创建 StorageClass |
| 访问模式不匹配 | 修改 accessModes |
| 容量不足 | 增加 PV 容量 |

---

### 案例 10：节点 NotReady

**现象：** `kubectl get nodes` 显示 NotReady

**排查步骤：**
```bash
# 1. 查看节点详情
kubectl describe node <node-name>

# 2. 查看节点条件
kubectl get node <node-name> -o jsonpath='{.status.conditions}'

# 3. SSH 到节点检查
systemctl status kubelet
journalctl -u kubelet -f

# 4. 检查容器运行时
systemctl status containerd
crictl info

# 5. 检查网络插件
kubectl get pods -n calico-system
```

**常见解决：**
```bash
# 重启 kubelet
systemctl restart kubelet

# 重启容器运行时
systemctl restart containerd

# 重启网络插件
kubectl rollout restart daemonset/calico-node -n calico-system

# 驱逐节点
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

---

### 案例 11：etcd 故障

**现象：** etcd 集群异常

**排查步骤：**
```bash
# 1. 查看 etcd Pod
kubectl get pods -n kube-system -l component=etcd
kubectl logs -n kube-system -l component=etcd

# 2. 检查 etcd 健康
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key \
  endpoint health

# 3. 查看 etcd 成员
ETCDCTL_API=3 etcdctl member list

# 4. 查看 etcd 指标
curl -L http://localhost:2379/metrics | grep etcd
```

**备份与恢复：**
```bash
# 备份
ETCDCTL_API=3 etcdctl snapshot save backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/backup-client.crt \
  --key=/etc/kubernetes/pki/etcd/backup-client.key

# 恢复
ETCDCTL_API=3 etcdctl snapshot restore backup.db \
  --data-dir=/var/lib/etcd-backup
```

---

### 案例 12：kube-apiserver 无法访问

**现象：** kubectl 命令超时

**排查步骤：**
```bash
# 1. 检查 apiserver Pod
kubectl get pods -n kube-system -l component=kube-apiserver

# 2. 查看日志
kubectl logs -n kube-system -l component=kube-apiserver

# 3. 检查证书
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

# 4. 检查 etcd 连接
kubectl logs -n kube-system -l component=kube-apiserver | grep etcd

# 5. 测试 API
curl -k https://localhost:6443/healthz
```

**常见解决：**
```bash
# 重启 apiserver
kubectl delete pod -n kube-system -l component=kube-apiserver

# 更新证书
kubeadm certs renew apiserver
kubeadm certs renew apiserver-kubelet-client
systemctl restart kubelet
```

---

### 案例 13：Deployment 滚动更新卡住

**现象：** 更新时新 Pod 不启动

**排查步骤：**
```bash
# 1. 查看滚动更新状态
kubectl rollout status deployment/<name>

# 2. 查看新 Pod
kubectl get pods -l app=<name> --show-labels

# 3. 查看事件
kubectl describe deployment <name>

# 4. 检查资源配额
kubectl describe quota -n <namespace>
kubectl describe limitrange -n <namespace>
```

**解决：**
```bash
# 回滚
kubectl rollout undo deployment/<name>

# 跳过健康检查（不推荐）
kubectl set image deployment/<name> <container>=<image>
kubectl edit deployment/<name>
# 修改 strategy.rollingUpdate.maxUnavailable: 100%
```

---

### 案例 14：StatefulSet Pod 无法启动

**现象：** StatefulSet Pod 卡在 ContainerCreating

**排查步骤：**
```bash
# 1. 查看 Pod 详情
kubectl describe pod <pod-name>

# 2. 检查 PVC
kubectl get pvc -l app=<app-name>
kubectl describe pvc <pvc-name>

# 3. 检查 PV
kubectl get pv
kubectl describe pv <pv-name>

# 4. 查看 Headless Service
kubectl get svc <statefulset-name>-headless
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| PVC 未绑定 | 检查 StorageClass |
| 顺序启动等待 | 等待前一个 Pod Ready |
| 域名解析失败 | 检查 Headless Service |

---

### 案例 15：DaemonSet Pod 调度失败

**现象：** 部分节点没有 DaemonSet Pod

**排查步骤：**
```bash
# 1. 查看 DaemonSet 状态
kubectl get daemonset -n <namespace>

# 2. 查看未调度节点
kubectl get daemonset <name> -o jsonpath='{.status.numberMisscheduled}'

# 3. 检查节点污点
kubectl describe node <node-name> | grep Taint

# 4. 检查容忍配置
kubectl get daemonset <name> -o yaml | grep -A 10 tolerations
```

**解决：**
```yaml
# 添加容忍
spec:
  template:
    spec:
      tolerations:
      - operator: Exists
```

---

### 案例 16：ConfigMap/Secret 更新不生效

**现象：** 修改 ConfigMap/Secret 后 Pod 未更新

**排查步骤：**
```bash
# 1. 检查挂载方式
kubectl get pod <pod-name> -o yaml | grep -A 10 volumes

# 2. 查看 ConfigMap 内容
kubectl get configmap <name> -o yaml

# 3. 检查 Pod 内文件
kubectl exec <pod-name> -- cat /etc/config/file.conf
```

**解决：**
```bash
# 重启 Pod（ConfigMap 作为环境变量时）
kubectl rollout restart deployment/<name>

# 等待自动更新（ConfigMap 作为卷挂载时，约 1-2 分钟）
```

---

### 案例 17：网络策略阻止流量

**现象：** Pod 间无法通信

**排查步骤：**
```bash
# 1. 查看 NetworkPolicy
kubectl get networkpolicy
kubectl describe networkpolicy <name>

# 2. 检查 Pod 标签
kubectl get pods --show-labels

# 3. 测试连通性
kubectl run test --image=busybox --rm -it -- wget <target-pod-ip>

# 4. 查看 CNI 日志
kubectl logs -n calico-system -l k8s-app=calico-node
```

**解决：**
```yaml
# 添加允许的 NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-traffic
spec:
  podSelector:
    matchLabels:
      app: target
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: source
```

---

### 案例 18：Helm 升级失败

**现象：** `helm upgrade` 失败

**排查步骤：**
```bash
# 1. 查看 Release 状态
helm status <release-name>
helm history <release-name>

# 2. 查看详细错误
helm upgrade <release-name> <chart> --debug

# 3. 查看 Kubernetes 事件
kubectl get events --sort-by='.lastTimestamp'

# 4. 回滚
helm rollback <release-name> <revision>
```

**常见解决：**
```bash
# 强制回滚
helm rollback <release-name> 1 --force

# 清理 hooks
kubectl delete job -l release=<release-name>

# 重新安装
helm uninstall <release-name>
helm install <release-name> <chart>
```

---

### 案例 19：资源配额不足

**现象：** Pod 创建失败，提示超出配额

**排查步骤：**
```bash
# 1. 查看配额
kubectl describe quota -n <namespace>

# 2. 查看 LimitRange
kubectl describe limitrange -n <namespace>

# 3. 查看资源使用
kubectl top pods -n <namespace>
kubectl top nodes

# 4. 查看事件
kubectl get events -n <namespace> | grep -i quota
```

**解决：**
```yaml
# 增加配额
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
```

---

### 案例 20：证书过期

**现象：** kubectl 提示证书过期

**排查步骤：**
```bash
# 1. 检查证书有效期
kubeadm certs check-expiration

# 2. 查看证书详情
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout | grep -A 2 Validity
```

**解决：**
```bash
# 续订证书
kubeadm certs renew apiserver
kubeadm certs renew apiserver-kubelet-client
kubeadm certs renew front-proxy-apiserver-client
kubeadm certs renew etcd-server
kubeadm certs renew etcd-peer
kubeadm certs renew etcd-healthcheck-client
kubeadm certs renew kubelet-api-client

# 重启相关组件
kubectl delete pod -n kube-system -l component=kube-apiserver
kubectl delete pod -n kube-system -l component=etcd
systemctl restart kubelet
```

---

### 案例 21：Pod 无法删除（Terminating）

**现象：** Pod 一直卡在 Terminating 状态

**排查步骤：**
```bash
# 1. 查看 Pod 详情
kubectl describe pod <pod-name>

# 2. 查看最终器
kubectl get pod <pod-name> -o jsonpath='{.metadata.finalizers}'

# 3. 查看节点状态
kubectl get nodes

# 4. 检查 kubelet 日志
journalctl -u kubelet | grep <pod-name>
```

**解决：**
```bash
# 强制删除
kubectl delete pod <pod-name> --grace-period=0 --force

# 移除最终器
kubectl edit pod <pod-name>
# 删除 finalizers 字段

# 或
kubectl patch pod <pod-name> -p '{"metadata":{"finalizers":null}}'
```

---

### 案例 22：HPA 不工作

**现象：** HPA 无法自动扩缩容

**排查步骤：**
```bash
# 1. 查看 HPA 状态
kubectl get hpa
kubectl describe hpa <hpa-name>

# 2. 检查 metrics-server
kubectl get pods -n kube-system -l k8s-app=metrics-server
kubectl top pods

# 3. 检查资源请求
kubectl get deployment <name> -o jsonpath='{.spec.template.spec.containers[*].resources.requests}'

# 4. 查看自定义指标
kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods
```

**解决：**
```bash
# 安装 metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# 确保 Pod 有资源请求
kubectl edit deployment <name>
# 添加 resources.requests.cpu 和 memory
```

---

### 案例 23：CronJob 不执行

**现象：** CronJob 未按时触发

**排查步骤：**
```bash
# 1. 查看 CronJob
kubectl get cronjob
kubectl describe cronjob <name>

# 2. 查看历史 Job
kubectl get jobs --selector=cronjob=<name>

# 3. 检查控制器日志
kubectl logs -n kube-system -l controller-manager

# 4. 检查时间同步
kubectl exec -it <pod> -- date
```

**解决：**
```yaml
# 检查时区配置
spec:
  timeZone: Asia/Shanghai
  schedule: "0 2 * * *"  # 每天凌晨 2 点
```

---

### 案例 24：Service Account 权限不足

**现象：** Pod 内访问 API 被拒绝

**排查步骤：**
```bash
# 1. 查看 ServiceAccount
kubectl get sa <name>

# 2. 查看 RBAC
kubectl get role,rolebinding -n <namespace>
kubectl get clusterrole,clusterrolebinding

# 3. 检查 Pod 使用的 SA
kubectl get pod <pod-name> -o jsonpath='{.spec.serviceAccountName}'

# 4. 测试权限
kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>
```

**解决：**
```yaml
# 创建 Role 和 RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
- kind: ServiceAccount
  name: my-sa
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

### 案例 25：Ingress Controller 异常

**现象：** Ingress Controller Pod 异常

**排查步骤：**
```bash
# 1. 查看 Pod 状态
kubectl get pods -n ingress-nginx
kubectl describe pod -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 2. 查看日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 3. 检查 Service
kubectl get svc -n ingress-nginx
kubectl describe svc -n ingress-nginx

# 4. 检查配置
kubectl get cm -n ingress-nginx ingress-nginx-controller -o yaml
```

**解决：**
```bash
# 重启 Ingress Controller
kubectl rollout restart deployment/ingress-nginx-controller -n ingress-nginx

# 重新安装
helm uninstall nginx-ingress -n ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx -n ingress-nginx
```

---

### 案例 26：节点磁盘压力

**现象：** 节点 DiskPressure，Pod 被驱逐

**排查步骤：**
```bash
# 1. 查看节点条件
kubectl describe node <node-name> | grep -A 5 DiskPressure

# 2. SSH 检查磁盘
df -h
du -sh /var/lib/docker/*
du -sh /var/log/*

# 3. 查看被驱逐的 Pod
kubectl get events | grep -i evict
```

**解决：**
```bash
# 清理镜像
crictl rmi --prune
docker system prune -a

# 清理日志
journalctl --vacuum-time=1d
find /var/log -name "*.log" -size +100M -exec truncate -s 0 {} \;

# 配置日志轮转
cat > /etc/logrotate.d/docker-containers << EOF
/var/log/containers/*.log {
  daily
  rotate 7
  compress
  copytruncate
}
EOF
```

---

### 案例 27：Pod 间延迟高

**现象：** Pod 间通信延迟高

**排查步骤：**
```bash
# 1. 测试延迟
kubectl run test --image=nicolaka/netshoot --rm -it -- \
  ping <target-pod-ip>

# 2. 检查节点位置
kubectl get pods -o wide

# 3. 检查网络插件
kubectl get pods -n calico-system
kubectl logs -n calico-system -l k8s-app=calico-node

# 4. 抓包分析
kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container>
# 在调试容器内
tcpdump -i any -n host <target-ip>
```

**解决：**
- 确保 Pod 在同一节点或同一机架
- 检查 CNI 配置
- 优化网络策略

---

### 案例 28：kubelet 内存泄漏

**现象：** kubelet 内存持续增长

**排查步骤：**
```bash
# 1. 查看 kubelet 内存
systemctl status kubelet
ps aux | grep kubelet

# 2. 查看 kubelet 日志
journalctl -u kubelet | grep -i leak

# 3. 检查 Pod 数量
kubectl get pods --field-selector spec.nodeName=<node-name>
```

**解决：**
```bash
# 重启 kubelet
systemctl restart kubelet

# 限制 kubelet 内存
cat > /etc/systemd/system/kubelet.service.d/limit.conf << EOF
[Service]
MemoryLimit=2G
EOF
systemctl daemon-reload
systemctl restart kubelet

# 升级 kubelet 版本
```

---

### 案例 29：Helm Release 状态不一致

**现象：** Helm 显示的状态与实际不符

**排查步骤：**
```bash
# 1. 查看 Release 状态
helm list
helm status <release-name>

# 2. 查看 Kubernetes 资源
kubectl get all -l app.kubernetes.io/instance=<release-name>

# 3. 查看 Helm 存储
kubectl get secrets -n <namespace> | grep <release-name>
kubectl get configmaps -n <namespace> | grep <release-name>
```

**解决：**
```bash
# 修复 Release 状态
helm rollback <release-name> <revision>

# 清理孤儿资源
kubectl delete secret -n <namespace> -l app.kubernetes.io/instance=<release-name>

# 重新同步
helm upgrade <release-name> <chart> --force
```

---

### 案例 30：集群升级失败

**现象：** kubeadm upgrade 失败

**排查步骤：**
```bash
# 1. 查看可用版本
kubeadm upgrade plan

# 2. 检查前置条件
kubeadm upgrade plan --print-config

# 3. 查看错误日志
journalctl -u kubelet | grep -i upgrade

# 4. 检查组件状态
kubectl get pods -n kube-system
```

**解决：**
```bash
# 升级控制平面
kubeadm upgrade apply v1.28.0

# 升级 kubelet 和 kubectl
apt-get update
apt-get install -y kubelet=1.28.0-00 kubectl=1.28.0-00
systemctl restart kubelet

# 升级 Worker 节点
kubeadm upgrade node

# 验证
kubectl get nodes
kubectl version
```

---

## 11. 最佳实践

### ✅ 集群设计

1. **高可用架构**
   - 至少 3 个 Master 节点
   - etcd 独立部署（大型集群）
   - 使用负载均衡器

2. **节点规划**
   - Master 专用，不跑业务
   - 按业务类型划分节点池
   - 预留 20% 资源缓冲

3. **网络规划**
   - Pod 网段：/16 或更大
   - Service 网段：/12 或 /16
   - 避免与现有网络冲突

### ✅ 应用部署

1. **资源管理**
   - 所有 Pod 必须设置 requests/limits
   - 使用 LimitRange 设置默认值
   - 使用 ResourceQuota 控制总量

2. **健康检查**
   - 配置 livenessProbe（重启）
   - 配置 readinessProbe（流量）
   - 配置 startupProbe（慢启动）

3. **高可用部署**
   - 至少 2 个副本
   - 配置 podAntiAffinity
   - 使用 PDB（PodDisruptionBudget）

### ✅ 安全配置

1. **访问控制**
   - 启用 RBAC
   - 最小权限原则
   - 定期审计权限

2. **网络安全**
   - 使用 NetworkPolicy
   - 启用 PodSecurityPolicy/Standards
   - 限制 Service 暴露

3. **镜像安全**
   - 使用私有仓库
   - 扫描镜像漏洞
   - 使用固定版本标签

### ✅ 监控告警

1. **监控指标**
   - 节点：CPU、内存、磁盘、网络
   - Pod：资源使用、重启次数
   - 应用：QPS、延迟、错误率

2. **告警规则**
   - 节点 NotReady > 5 分钟
   - Pod 重启 > 5 次/小时
   - 磁盘使用率 > 80%
   - API 延迟 > 1 秒

3. **日志管理**
   - 集中收集日志
   - 设置日志保留期
   - 敏感信息脱敏

### ✅ 备份恢复

1. **etcd 备份**
   ```bash
   # 每天备份
   0 2 * * * /usr/local/bin/etcd-backup.sh
   ```

2. **资源配置备份**
   ```bash
   kubectl get all -A -o yaml > backup-$(date +%F).yaml
   ```

3. **恢复演练**
   - 每季度做一次恢复演练
   - 记录 RTO/RPO

---

## 📋 快速参考卡片

```bash
# ===== 集群管理 =====
kubeadm init --pod-network-cidr=10.244.0.0/16
kubeadm join <master>:6443 --token <token>
kubeadm upgrade plan
kubeadm certs check-expiration

# ===== 资源操作 =====
kubectl apply -f file.yaml
kubectl delete -f file.yaml
kubectl edit deployment/<name>
kubectl scale deployment/<name> --replicas=5

# ===== 查看资源 =====
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs -f <pod-name>
kubectl top pods/nodes

# ===== 故障排查 =====
kubectl describe pod <name>         # 查看 Pod 详情
kubectl get events --sort-by='.lastTimestamp'  # 查看事件
kubectl debug -it <pod> --image=busybox  # 调试 Pod
kubectl rollout status deployment/<name>  # 查看滚动更新

# ===== Helm 操作 =====
helm install <name> <chart>
helm upgrade <name> <chart>
helm rollback <name> <revision>
helm uninstall <name>

# ===== 常用诊断 =====
kubectl auth can-i <verb> <resource>  # 检查权限
kubectl api-resources                    # 查看 API 资源
kubectl explain pod.spec                # 查看资源说明
```

---

## 🔗 相关资源

- **官方文档：** https://kubernetes.io/docs/
- **Kubernetes GitHub：** https://github.com/kubernetes/kubernetes
- **Helm Charts：** https://artifacthub.io/
- **故障排查指南：** https://kubernetes.io/docs/tasks/debug/

---

> 💡 **刺刺提醒：**
> 1. 生产环境变更前先备份 etcd！😈
> 2. 所有 Pod 必须设置资源限制！
> 3. 定期检查证书有效期！
> 4. 监控告警比故障排查更重要！
> 5. 文档里的 30 个案例都是血泪教训，务必熟悉！
## 常用指令

- kubectl get node -o wide
- kubectl describe node <node-name>
- kubectl get pod -A -o wide
- kubectl describe pod <pod-name> -n <namespace>
- kubectl logs <pod-name> -n <namespace> --tail=200
- kubectl get events -A --sort-by=.lastTimestamp
- kubectl top node
- kubectl top pod -A
- kubectl get svc,ingress -A
- kubectl rollout status deployment/<deployment-name> -n <namespace>
- kubectl rollout history deployment/<deployment-name> -n <namespace>

