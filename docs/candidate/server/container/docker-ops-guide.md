# Docker 运维参考手册

```yaml
status: usable
type: reference
risk_level: high
review_required: true
source: imported-manual
source_path: D:/Work/工作文档/知识库构建/服务器运维相关/docker-ops-guide.md
asset_types: [server, container]
systems: [docker, linux]
issue_types: [container-runtime, deployment, troubleshooting]
tags: [docker, container, image, compose, registry, network]
```

## 适用范围

- 适用于 Docker Engine、Docker Compose、镜像构建、容器运行、网络、存储、私有仓库和常见故障排查。
- 适合作为服务器容器运行环境维护、部署检查和问题定位参考。

## 常见现象

- 容器启动失败、异常退出或无法访问。
- 镜像构建失败、拉取失败或版本不一致。
- 容器网络、端口映射、卷挂载或日志异常。
- Docker 服务启动失败或资源占用异常。

## 处理步骤

1. 确认变更对象、影响范围、维护窗口和回退方案。
2. 先查看 Docker 服务状态、容器状态、镜像版本、端口映射、日志和资源占用。
3. 按故障现象选择原始手册中的安装配置、镜像构建、Compose、网络、存储、安全或故障案例章节。
4. 涉及删除容器、清理镜像、修改 daemon.json、开放远程 API 或重建服务前，必须确认备份和回滚路径。
5. 处理后记录实际命令、影响容器、验证结果和是否需要沉淀为更细知识。

## 验证方式

- Docker 服务状态正常。
- 目标容器处于期望状态，业务端口和日志正常。
- 重启 Docker 或容器后配置仍符合预期。

## 注意事项

- 本文属于服务器、数据库或网络设备高风险运维参考，生产环境操作前必须完成审批、备份、维护窗口和回退方案确认。
- 本文中的命令和参数来自通用手册，执行前必须替换为本公司实际环境，并先在测试环境验证。
- 涉及删除、覆盖、重启、恢复、扩缩容、路由/ACL 变更、证书/密钥、数据库恢复等动作时，不允许直接照抄执行。
- 手册中的示例密码、Token 和密钥已做脱敏处理；不得在知识库中保存真实凭据。

## 原始手册

以下内容为导入的原始手册正文，供工程师查阅细节。

# Docker 运维完全指南

> 📝 版本：Docker 24+ / Docker Engine 2026  
> ⚠️ 生产环境操作前请先在测试环境验证！

---

## 📚 目录

1. [Docker 架构概览](#1-docker-架构概览)
2. [安装与配置](#2-安装与配置)
3. [镜像管理](#3-镜像管理)
4. [容器管理](#4-容器管理)
5. [数据卷管理](#5-数据卷管理)
6. [网络管理](#6-网络管理)
7. [Docker Compose](#7-docker-compose)
8. [Dockerfile 编写](#8-dockerfile-编写)
9. [私有仓库](#9-私有仓库)
10. [安全配置](#10-安全配置)
11. [监控与日志](#11-监控与日志)
12. [故障排查（30 例）](#12-故障排查 30 例)
13. [最佳实践](#13-最佳实践)

---

## 1. Docker 架构概览

### 1.1 核心组件

| 组件 | 作用 | 说明 |
|------|------|------|
| **Docker Daemon** | 守护进程 | 监听 API 请求，管理镜像/容器/网络/卷 |
| **Docker Client** | 命令行工具 | 用户与 Docker 交互的 CLI |
| **Docker Registry** | 镜像仓库 | 存储和分发镜像（Docker Hub/私有仓库） |
| **Containerd** | 容器运行时 | 管理容器生命周期（Docker 底层） |
| **runc** | 低级运行时 | 实际创建和运行容器 |

### 1.2 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **镜像（Image）** | 只读模板，包含应用和依赖 | 光盘镜像 |
| **容器（Container）** | 镜像的运行实例 | 运行中的虚拟机 |
| **仓库（Registry）** | 存放镜像的地方 | 应用商店 |
| **数据卷（Volume）** | 持久化存储 | 共享文件夹 |
| **网络（Network）** | 容器间通信 | 虚拟交换机 |

### 1.3 架构图

```
┌─────────────────────────────────────────────────┐
│              Docker Client                       │
│              (docker CLI)                        │
└────────────────────┬────────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────────┐
│              Docker Daemon                       │
│              (dockerd)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Images  │  │Containers│  │ Networks │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│  ┌──────────┐  ┌──────────┐                     │
│  │ Volumes  │  │  Plugins │                     │
│  └──────────┘  └──────────┘                     │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│              Containerd                          │
│  ┌──────────────────────────────────────────┐   │
│  │              runc                         │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐        │   │
│  │  │Container│ │Container│ │Container│      │   │
│  │  └────────┘ └────────┘ └────────┘        │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 2. 安装与配置

### 2.1 Ubuntu/Debian 安装

```bash
# 卸载旧版本
apt-get remove docker docker-engine docker.io containerd runc

# 安装依赖
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release

# 添加 GPG 密钥
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# 添加仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 验证安装
docker --version
docker run --rm hello-world
```

### 2.2 CentOS/RHEL 安装

```bash
# 卸载旧版本
yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# 安装依赖
yum install -y yum-utils

# 添加仓库
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker Engine
yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动 Docker
systemctl start docker
systemctl enable docker
```

### 2.3 配置镜像加速器

```bash
# 编辑 daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live",
    "https://hub.rat.dev",
    "https://dhub.kubesre.xyz"
  ],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true
}
EOF

# 重启 Docker
systemctl daemon-reload
systemctl restart docker

# 验证
docker info | grep -A 5 "Registry Mirrors"
```

### 2.4 配置非 root 用户

```bash
# 创建 docker 组
groupadd docker

# 添加用户到 docker 组
usermod -aG docker $USER

# 重新登录或执行
newgrp docker

# 验证
docker run --rm hello-world
```

### 2.5 配置远程访问

```bash
# 编辑 systemd 配置
systemctl edit docker

# 添加以下内容
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375

# 重启 Docker
systemctl daemon-reload
systemctl restart docker

# 验证
docker -H tcp://<server-ip>:2375 info

# 配置 TLS（生产环境推荐）
# 生成证书
mkdir -p /etc/docker/certs
cd /etc/docker/certs
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
openssl genrsa -out server-key.pem 4096
openssl req -subj "/CN=$(hostname)" -sha256 -new -key server-key.pem -out server.csr
openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem
openssl genrsa -out key.pem 4096
openssl req -subj '/CN=client' -new -key key.pem -out client.csr
openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out cert.pem

# 配置 daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/etc/docker/certs/ca.pem",
  "tlscert": "/etc/docker/certs/server-cert.pem",
  "tlskey": "/etc/docker/certs/server-key.pem",
  "hosts": ["tcp://0.0.0.0:2376", "unix:///var/run/docker.sock"]
}
EOF
```

---

## 3. 镜像管理

### 3.1 拉取镜像

```bash
# 拉取最新镜像
docker pull nginx

# 拉取指定版本
docker pull nginx:1.21

# 拉取特定架构
docker pull --platform linux/amd64 nginx

# 拉取所有标签
docker pull --all-tags nginx

# 从私有仓库拉取
docker pull registry.example.com/myapp:latest

# 登录后拉取（私有仓库）
docker login registry.example.com
docker pull registry.example.com/myapp:latest
```

### 3.2 构建镜像

```bash
# 基础构建
docker build -t myapp:latest .

# 指定 Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# 使用构建参数
docker build --build-arg VERSION=1.0 -t myapp:1.0 .

# 多阶段构建
docker build --target production -t myapp:prod .

# 无缓存构建
docker build --no-cache -t myapp:latest .

# 构建并推送
docker build -t registry.example.com/myapp:1.0 .
docker push registry.example.com/myapp:1.0
```

### 3.3 查看镜像

```bash
# 列出镜像
docker images
docker image ls

# 查看镜像详情
docker image inspect nginx:1.21

# 查看镜像历史
docker history nginx:1.21

# 查看镜像树
docker image ls --tree  # 需要插件

# 搜索镜像
docker search nginx
docker search --filter is-official=true nginx
docker search --filter stars=100 nginx
```

### 3.4 镜像操作

```bash
# 打标签
docker tag nginx:1.21 my-nginx:1.21
docker tag nginx:1.21 registry.example.com/nginx:1.21

# 删除镜像
docker rmi nginx:1.21
docker image rm nginx:1.21

# 强制删除
docker rmi -f nginx:1.21

# 删除悬空镜像
docker image prune

# 删除所有未使用镜像
docker image prune -a

# 导出镜像
docker save -o nginx.tar nginx:1.21
docker save nginx:1.21 | gzip > nginx.tar.gz

# 导入镜像
docker load -i nginx.tar
docker load < nginx.tar.gz

# 复制镜像到另一台机器
docker save nginx:1.21 | ssh user@remote "docker load"
```

### 3.5 多阶段构建示例

```dockerfile
# Dockerfile
# 第一阶段：构建
FROM golang:1.21 AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# 第二阶段：运行
FROM alpine:3.18

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/
COPY --from=builder /app/myapp .
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 8080
CMD ["./myapp"]
```

### 3.6 镜像优化技巧

```dockerfile
# ✅ 好的实践
FROM alpine:3.18

# 合并 RUN 指令减少层数
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir flask && \
    rm -rf /root/.cache

# 使用 .dockerignore
# .dockerignore
.git
*.md
__pycache__
*.pyc
node_modules

# 使用多阶段构建
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# ❌ 避免的做法
FROM ubuntu:latest  # 使用具体版本
RUN apt-get update  # 单独执行
RUN apt-get install -y nginx  # 单独执行
RUN apt-get clean  # 单独执行
```

---

## 4. 容器管理

### 4.1 创建和启动容器

```bash
# 基础启动
docker run nginx

# 后台运行
docker run -d nginx

# 命名容器
docker run -d --name web-server nginx

# 端口映射
docker run -d -p 8080:80 nginx
docker run -d -p 127.0.0.1:8080:80 nginx  # 只监听本地
docker run -d -p 8080:80 -p 8443:443 nginx

# 环境变量
docker run -d -e MYSQL_ROOT_PASSWORD=<示例密码> mysql:8.0
docker run -d --env-file .env myapp

# 挂载数据卷
docker run -d -v /host/data:/container/data nginx
docker run -d --mount type=volume,source=myvol,target=/data nginx

# 挂载主机目录
docker run -d -v /var/log/nginx:/var/log/nginx:ro nginx

# 网络配置
docker run -d --network host nginx  # 主机网络
docker run -d --network none nginx  # 无网络
docker run -d --network mynet nginx  # 自定义网络

# 资源限制
docker run -d --memory=512m --cpus=1.0 nginx
docker run -d --memory=512m --memory-swap=1g nginx

# 重启策略
docker run -d --restart=no nginx  # 不自动重启
docker run -d --restart=on-failure nginx  # 失败时重启
docker run -d --restart=always nginx  # 总是重启
docker run -d --restart=unless-stopped nginx  # 除非手动停止

# 交互式容器
docker run -it ubuntu bash
docker run -it --rm python:3.11 python

# 指定用户
docker run -d --user 1000:1000 nginx
```

### 4.2 查看容器

```bash
# 列出容器
docker ps
docker ps -a  # 所有容器
docker ps -q  # 只显示 ID

# 查看容器详情
docker inspect web-server
docker inspect --format='{{.NetworkSettings.IPAddress}}' web-server

# 查看容器日志
docker logs web-server
docker logs -f web-server  # 跟随输出
docker logs --tail 100 web-server  # 最后 100 行
docker logs --since 1h web-server  # 最近 1 小时
docker logs --timestamps web-server  # 显示时间戳

# 查看容器进程
docker top web-server

# 查看容器资源使用
docker stats
docker stats web-server

# 查看容器变更
docker diff web-server
```

### 4.3 容器操作

```bash
# 启动/停止/重启
docker start web-server
docker stop web-server
docker restart web-server
docker pause web-server
docker unpause web-server

# 强制停止
docker kill web-server

# 删除容器
docker rm web-server
docker rm -f web-server  # 强制删除运行中的

# 进入容器
docker exec -it web-server bash
docker exec -it web-server sh  # 如果没有 bash
docker exec -it web-server /bin/sh

# 执行命令
docker exec web-server ls -la
docker exec web-server cat /etc/os-release

# 复制文件
docker cp file.txt web-server:/tmp/
docker cp web-server:/var/log/app.log ./app.log

# 更新容器
docker update --memory=1g web-server
docker update --restart=always web-server

# 重命名容器
docker rename web-server nginx-web

# 提交容器为镜像
docker commit web-server my-nginx:custom
```

### 4.4 批量操作

```bash
# 停止所有容器
docker stop $(docker ps -q)

# 删除所有容器
docker rm $(docker ps -aq)

# 删除所有退出状态的容器
docker container prune

# 批量启动
docker start $(docker ps -a -q --filter "status=exited")

# 批量重启
docker restart $(docker ps -q)

# 批量删除镜像
docker rmi $(docker images -q -f dangling=true)
```

---

## 5. 数据卷管理

### 5.1 数据卷类型

| 类型 | 命令 | 存储位置 | 用途 |
|------|------|----------|------|
| **命名卷** | `-v myvol:/data` | `/var/lib/docker/volumes/` | 持久化数据 |
| **匿名卷** | `-v /data` | `/var/lib/docker/volumes/` | 临时数据 |
| **绑定挂载** | `-v /host/path:/data` | 主机任意位置 | 共享主机文件 |
| **tmpfs** | `--tmpfs /data` | 内存 | 敏感临时数据 |

### 5.2 创建和管理卷

```bash
# 创建卷
docker volume create myvol
docker volume create --driver local --opt type=tmpfs mytmpfs

# 列出卷
docker volume ls

# 查看卷详情
docker volume inspect myvol

# 使用卷
docker run -d -v myvol:/data nginx

# 删除卷
docker volume rm myvol

# 删除未使用卷
docker volume prune

# 备份卷
docker run --rm -v myvol:/data -v $(pwd):/backup alpine tar cvf /backup/backup.tar /data

# 恢复卷
docker run --rm -v myvol:/data -v $(pwd):/backup alpine tar xvf /backup/backup.tar -C /
```

### 5.3 绑定挂载

```bash
# 挂载主机目录
docker run -d -v /host/data:/container/data nginx

# 只读挂载
docker run -d -v /host/config:/container/config:ro nginx

# 挂载单个文件
docker run -d -v /host/nginx.conf:/etc/nginx/nginx.conf:ro nginx

# SELinux 上下文
docker run -d -v /host/data:/container/data:z nginx
```

### 5.4 数据持久化最佳实践

```yaml
# docker-compose.yml 示例
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
      - ./conf.d:/etc/mysql/conf.d:ro
      - ./backups:/backups
    environment:
      MYSQL_ROOT_PASSWORD: secret

  redis:
    image: redis:7
    volumes:
      - redis-data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf:ro
    command: redis-server /usr/local/etc/redis/redis.conf

  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - ./logs:/var/log/nginx
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

volumes:
  mysql-data:
  redis-data:
```

---

## 6. 网络管理

### 6.1 网络类型

| 类型 | 命令 | 说明 |
|------|------|------|
| **bridge** | 默认 | 容器间通过网桥通信 |
| **host** | `--network host` | 使用主机网络（无隔离） |
| **none** | `--network none` | 无网络 |
| **overlay** | Docker Swarm | 跨主机网络 |
| **macvlan** | 高级 | 直接连接物理网络 |

### 6.2 创建和管理网络

```bash
# 创建网络
docker network create mynet
docker network create --driver bridge --subnet 172.20.0.0/16 mynet

# 列出网络
docker network ls

# 查看网络详情
docker network inspect mynet

# 连接容器到网络
docker network connect mynet web-server
docker network connect --ip 172.20.0.10 mynet db-server

# 断开网络
docker network disconnect mynet web-server

# 删除网络
docker network rm mynet

# 删除未使用网络
docker network prune
```

### 6.3 容器间通信

```bash
# 创建网络
docker network create app-network

# 启动容器加入网络
docker run -d --name web --network app-network nginx
docker run -d --name db --network app-network mysql

# 容器间通过名称访问
docker exec web ping db
docker exec web curl http://db:3306

# 使用 docker-compose
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend
      - backend
  db:
    image: mysql
    networks:
      - backend

networks:
  frontend:
  backend:
```

### 6.4 端口映射

```bash
# 映射到主机所有接口
docker run -d -p 8080:80 nginx

# 映射到特定 IP
docker run -d -p 192.168.1.100:8080:80 nginx

# 映射多个端口
docker run -d -p 80:80 -p 443:443 -p 8080:8080 nginx

# 动态端口映射
docker run -d -P nginx  # 随机映射所有暴露端口

# 查看端口映射
docker port web-server
```

### 6.5 网络故障排查

```bash
# 查看容器 IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web-server

# 测试连通性
docker run --rm --network container:web-server nicolaka/netshoot curl localhost

# 抓包
docker run --rm --cap-add=NET_ADMIN --network container:web-server nicolaka/netshoot tcpdump -i eth0

# DNS 测试
docker run --rm busybox nslookup db-server
```

---

## 7. Docker Compose

### 7.1 安装

```bash
# Docker 已包含 compose 插件
docker compose version

# 或独立安装
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 7.2 基础使用

```bash
# 启动服务
docker compose up
docker compose up -d  # 后台运行

# 停止服务
docker compose down
docker compose down -v  # 删除卷

# 查看状态
docker compose ps
docker compose logs
docker compose logs -f web

# 重启服务
docker compose restart
docker compose restart web

# 构建镜像
docker compose build
docker compose build --no-cache

# 执行命令
docker compose exec web bash
docker compose run --rm web python manage.py migrate

# 查看配置
docker compose config

# 扩缩容
docker compose up -d --scale web=3
```

### 7.3 Compose 文件示例

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Web 服务
  nginx:
    image: nginx:alpine
    container_name: web-server
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./logs:/var/log/nginx
    networks:
      - frontend
    depends_on:
      - app
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 应用服务
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        - VERSION=1.0
    container_name: myapp
    environment:
      - DATABASE_URL=mysql://user:pass@db:3306/mydb
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./app:/app
      - app-data:/app/data
    networks:
      - frontend
      - backend
    depends_on:
      - db
      - redis
    restart: always

  # 数据库
  db:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db-data:/var/lib/mysql
      - ./mysql/conf.d:/etc/mysql/conf.d:ro
      - ./mysql/backups:/backups
    networks:
      - backend
    restart: always
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 30s
      timeout: 10s
      retries: 5

  # 缓存
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    command: redis-server /usr/local/etc/redis/redis.conf
    volumes:
      - redis-data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    networks:
      - backend
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 监控
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - backend
    restart: always

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    ports:
      - "3000:3000"
    networks:
      - backend
    depends_on:
      - prometheus
    restart: always

networks:
  frontend:
  backend:
    driver: bridge

volumes:
  app-data:
  db-data:
  redis-data:
  prometheus-data:
  grafana-data:
```

### 7.4 多环境配置

```yaml
# docker-compose.override.yml (开发环境)
version: '3.8'
services:
  app:
    build:
      context: ./app
      target: development
    volumes:
      - ./app:/app
    environment:
      - DEBUG=true

# docker-compose.prod.yml (生产环境)
version: '3.8'
services:
  app:
    image: registry.example.com/myapp:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    environment:
      - DEBUG=false

# 使用不同配置
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d  # 开发
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d  # 生产
```

### 7.5 环境变量管理

```bash
# .env 文件
DB_ROOT_PASSWORD=SecretRoot@2026
DB_PASSWORD=Secret<示例密码>
GRAFANA_PASSWORD=Grafana@2026
APP_ENV=production

# 在 compose 中使用
# docker-compose.yml
services:
  db:
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
```

---

## 8. Dockerfile 编写

### 8.1 指令说明

| 指令 | 作用 | 示例 |
|------|------|------|
| FROM | 基础镜像 | `FROM ubuntu:22.04` |
| RUN | 执行命令 | `RUN apt-get update` |
| CMD | 默认命令 | `CMD ["nginx", "-g", "daemon off;"]` |
| ENTRYPOINT | 入口点 | `ENTRYPOINT ["python"]` |
| COPY | 复制文件 | `COPY . /app` |
| ADD | 复制 + 解压 | `ADD app.tar.gz /app` |
| WORKDIR | 工作目录 | `WORKDIR /app` |
| ENV | 环境变量 | `ENV NODE_ENV=production` |
| ARG | 构建参数 | `ARG VERSION=1.0` |
| EXPOSE | 暴露端口 | `EXPOSE 8080` |
| VOLUME | 数据卷 | `VOLUME ["/data"]` |
| USER | 运行用户 | `USER nobody` |
| HEALTHCHECK | 健康检查 | `HEALTHCHECK CMD curl -f http://localhost/` |

### 8.2 Python 应用示例

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### 8.3 Node.js 应用示例

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 生产阶段
FROM node:18-alpine

# 安装 dumb-init 处理信号
RUN apk add --no-cache dumb-init

WORKDIR /app

# 从构建阶段复制
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json .

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# 使用 dumb-init 启动
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

### 8.4 Java 应用示例

```dockerfile
# Dockerfile
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# 复制 pom.xml
COPY pom.xml .

# 下载依赖（利用缓存）
RUN mvn dependency:go-offline -B

# 复制源代码
COPY src ./src

# 构建
RUN mvn clean package -DskipTests -B

# 运行阶段
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# 创建非 root 用户
RUN addgroup -g 1001 -S java && \
    adduser -S java -u 1001

# 复制构建产物
COPY --from=builder /app/target/*.jar app.jar

# JVM 优化
ENV JAVA_OPTS="-Xms512m -Xmx512m -XX:+UseG1GC"

USER java

EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### 8.5 多阶段构建优化

```dockerfile
# Dockerfile
# 第一阶段：构建前端
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# 第二阶段：构建后端
FROM golang:1.21-alpine AS backend-builder

WORKDIR /app/backend
COPY backend/go.mod backend/go.sum ./
RUN go mod download
COPY backend/ .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# 第三阶段：运行
FROM alpine:3.18

# 安装运行时依赖
RUN apk --no-cache add ca-certificates tzdata nginx

# 设置时区
ENV TZ=Asia/Shanghai

WORKDIR /app

# 复制后端
COPY --from=backend-builder /app/backend/myapp .

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist ./static

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 创建非 root 用户
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 80

# 启动脚本
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

---

## 9. 私有仓库

### 9.1 部署 Registry

```bash
# 快速部署
docker run -d \
  --name registry \
  -p 5000:5000 \
  -v registry-data:/var/lib/registry \
  -e REGISTRY_STORAGE_DELETE_ENABLED=true \
  --restart=always \
  registry:2

# 配置 TLS 的 Registry
docker run -d \
  --name registry \
  -p 5000:5000 \
  -v registry-data:/var/lib/registry \
  -v /etc/docker/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_REALM="Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/certs/htpasswd \
  --restart=always \
  registry:2
```

### 9.2 配置客户端

```bash
# 配置信任私有仓库（HTTP）
cat > /etc/docker/daemon.json << EOF
{
  "insecure-registries": ["registry.example.com:5000"]
}
EOF
systemctl restart docker

# 配置 TLS（推荐）
mkdir -p /etc/docker/certs.d/registry.example.com:5000
cp ca.crt /etc/docker/certs.d/registry.example.com:5000/ca.crt
systemctl restart docker

# 登录
docker login registry.example.com:5000
```

### 9.3 推送和拉取

```bash
# 打标签
docker tag nginx:latest registry.example.com:5000/nginx:latest

# 推送
docker push registry.example.com:5000/nginx:latest

# 拉取
docker pull registry.example.com:5000/nginx:latest

# 列出仓库
curl -X GET https://registry.example.com:5000/v2/_catalog

# 列出标签
curl -X GET https://registry.example.com:5000/v2/nginx/tags/list

# 删除镜像
curl -X DELETE https://registry.example.com:5000/v2/nginx/manifests/sha256:xxx
```

### 9.4 Harbor 部署

```yaml
# docker-compose.yml for Harbor
version: '3'
services:
  proxy:
    image: goharbor/nginx-photon:v2.8.0
    container_name: nginx
    restart: always
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl

  registry:
    image: goharbor/registry-photon:v2.8.0
    container_name: registry
    restart: always
    volumes:
      - registry-data:/var/lib/registry
      - ./registry/config.yml:/etc/registry/config.yml

  core:
    image: goharbor/core-photon:v2.8.0
    container_name: core
    restart: always
    environment:
      - CORE_SECRET=<示例密钥>
      - REGISTRY_URL=http://registry:5000
      - TOKEN_SERVICE_URL=http://core:8080/service/token

  database:
    image: goharbor/harbor-db:v2.8.0
    container_name: harbor-db
    restart: always
    environment:
      - POSTGRES_PASSWORD=<示例密码>
    volumes:
      - database-data:/var/lib/postgresql/data

  redis:
    image: goharbor/redis-photon:v2.8.0
    container_name: redis
    restart: always
    volumes:
      - redis-data:/var/lib/redis

volumes:
  registry-data:
  database-data:
  redis-data:
```

---

## 10. 安全配置

### 10.1 守护进程安全

```bash
# 配置 daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/etc/docker/certs/ca.pem",
  "tlscert": "/etc/docker/certs/server-cert.pem",
  "tlskey": "/etc/docker/certs/server-key.pem",
  "hosts": ["tcp://0.0.0.0:2376", "unix:///var/run/docker.sock"],
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
EOF
```

### 10.2 容器安全

```bash
# 使用只读根文件系统
docker run --read-only nginx

# 禁止提权
docker run --security-opt=no-new-privileges:true nginx

# 删除_capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx

# 指定用户
docker run --user 1000:1000 nginx

# 限制资源
docker run --memory=512m --cpus=1.0 --pids-limit=100 nginx

# 使用 seccomp 配置文件
docker run --security-opt seccomp=/path/to/seccomp/profile.json nginx

# 使用 AppArmor
docker run --security-opt apparmor=/path/to/apparmor/profile nginx
```

### 10.3 镜像安全

```bash
# 扫描镜像漏洞
docker scan nginx:latest

# 使用可信基础镜像
FROM alpine:3.18  # 使用具体版本
FROM ubuntu:22.04  # 使用 LTS 版本

# 定期更新基础镜像
# 在 CI/CD 中自动更新

# 使用多阶段构建减少攻击面
FROM golang:1.21 AS builder
# ... 构建 ...
FROM alpine:3.18
COPY --from=builder /app/myapp .
```

### 10.4 网络安全

```bash
# 使用自定义网络隔离
docker network create --driver bridge isolated-net
docker run --network isolated-net app

# 禁止容器间通信
docker network create --opt com.docker.network.bridge.enable_icc=false isolated-net

# 限制端口暴露
docker run -p 127.0.0.1:8080:80 app  # 只监听本地
```

### 10.5 审计日志

```bash
# 配置审计
cat > /etc/audit/rules.d/docker.rules << EOF
-w /usr/bin/docker -k docker
-w /var/run/docker.sock -k docker
-w /etc/docker/daemon.json -k docker
EOF

# 查看审计日志
ausearch -k docker
```

---

## 11. 监控与日志

### 11.1 日志驱动

```bash
# 配置日志驱动
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3",
    "compress": "true"
  }
}
EOF

# 其他日志驱动
# syslog
"log-driver": "syslog",
"log-opts": {
  "syslog-address": "udp://192.168.1.100:514"
}

# journald
"log-driver": "journald"

# fluentd
"log-driver": "fluentd",
"log-opts": {
  "fluentd-address": "localhost:24224"
}

# splunk
"log-driver": "splunk",
"log-opts": {
  "splunk-token": "<示例Token>",
  "splunk-url": "https://splunk.example.com:8088"
}
```

### 11.2 查看日志

```bash
# 查看容器日志
docker logs web-server
docker logs -f web-server
docker logs --tail 100 --since 1h web-server

# 查看 Docker 守护进程日志
journalctl -u docker -f

# 查看容器日志文件
cat /var/lib/docker/containers/<container-id>/<container-id>-json.log

# 使用 docker-compose
docker compose logs
docker compose logs -f web
docker compose logs --tail=100
```

### 11.3 监控指标

```bash
# 查看资源使用
docker stats
docker stats --no-stream

# 查看容器详情
docker inspect web-server

# 查看事件
docker events
docker events --since 1h
docker events --filter type=container

# 使用 cAdvisor
docker run -d \
  --name=cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  gcr.io/cadvisor/cadvisor:latest
```

### 11.4 Prometheus 监控

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'docker'
    static_configs:
      - targets: ['localhost:9323']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

```bash
# 运行 Docker Exporter
docker run -d \
  --name docker-exporter \
  -p 9323:9323 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  prom/docker-exporter
```

### 11.5 日志收集（Fluentd）

```yaml
# docker-compose.yml
version: '3'
services:
  fluentd:
    image: fluent/fluentd:v1.16
    volumes:
      - ./fluentd/conf:/fluentd/etc
      - fluentd-log:/fluentd/log
    ports:
      - "24224:24224"

  app:
    image: myapp
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: app

volumes:
  fluentd-log:
```

---

## 12. 故障排查（30 例）

### 案例 1：Docker 服务无法启动

**现象：** `systemctl start docker` 失败

**排查步骤：**
```bash
# 1. 查看服务状态
systemctl status docker

# 2. 查看日志
journalctl -u docker -f

# 3. 检查配置文件
cat /etc/docker/daemon.json

# 4. 检查存储驱动
docker info | grep "Storage Driver"

# 5. 检查容器运行时
systemctl status containerd
```

**常见原因与解决：**
| 原因 | 解决方案 |
|------|----------|
| daemon.json 格式错误 | 修复 JSON 语法 |
| 存储驱动问题 | 清理 /var/lib/docker |
| containerd 未启动 | systemctl start containerd |
| 端口冲突 | 修改监听端口 |

---

### 案例 2：容器无法启动

**现象：** `docker run` 后容器立即退出

**排查步骤：**
```bash
# 1. 查看容器状态
docker ps -a

# 2. 查看日志
docker logs <container-id>

# 3. 查看容器详情
docker inspect <container-id>

# 4. 交互式调试
docker run -it --entrypoint /bin/sh <image>

# 5. 检查资源限制
docker inspect <container-id> | grep -A 5 "HostConfig"
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| 应用启动失败 | 查看日志修复应用 |
| CMD/ENTRYPOINT 错误 | 修正 Dockerfile |
| 资源不足 | 增加资源限制 |
| 端口冲突 | 修改映射端口 |

---

### 案例 3：镜像拉取失败

**现象：** `docker pull` 超时或失败

**排查步骤：**
```bash
# 1. 检查网络
ping registry-1.docker.io

# 2. 检查 DNS
nslookup registry-1.docker.io

# 3. 测试连接
curl -I https://registry-1.docker.io/v2/

# 4. 查看镜像加速器
docker info | grep -A 5 "Registry Mirrors"

# 5. 检查代理
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

**解决：**
```bash
# 配置镜像加速器
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live"
  ]
}
EOF
systemctl restart docker

# 或配置代理
mkdir -p /etc/systemd/system/docker.service.d
cat > /etc/systemd/system/docker.service.d/http-proxy.conf << EOF
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
EOF
systemctl daemon-reload
systemctl restart docker
```

---

### 案例 4：磁盘空间不足

**现象：** `No space left on device`

**排查步骤：**
```bash
# 1. 检查磁盘使用
df -h

# 2. 检查 Docker 占用
docker system df

# 3. 查看大文件
du -sh /var/lib/docker/*

# 4. 查看容器日志大小
du -sh /var/lib/docker/containers/*/*-json.log
```

**解决：**
```bash
# 清理未使用资源
docker system prune -a --volumes

# 清理悬空镜像
docker image prune

# 清理日志
find /var/lib/docker/containers -name "*-json.log" -size +100M -exec truncate -s 0 {} \;

# 配置日志轮转
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
EOF
systemctl restart docker
```

---

### 案例 5：容器无法访问网络

**现象：** 容器内无法访问外网

**排查步骤：**
```bash
# 1. 测试容器内网络
docker run --rm busybox ping -c 3 8.8.8.8
docker run --rm busybox nslookup google.com

# 2. 检查 Docker 网络
docker network ls
docker network inspect bridge

# 3. 检查 iptables
iptables -L -n | grep docker

# 4. 检查 DNS
cat /etc/docker/daemon.json | grep dns
```

**解决：**
```bash
# 重启 Docker 网络
systemctl restart docker

# 配置 DNS
cat > /etc/docker/daemon.json << EOF
{
  "dns": ["8.8.8.8", "114.114.114.114"]
}
EOF
systemctl restart docker

# 重建 bridge 网络
docker network rm bridge
systemctl restart docker
```

---

### 案例 6：端口映射不生效

**现象：** 主机无法访问容器端口

**排查步骤：**
```bash
# 1. 检查端口映射
docker port <container>

# 2. 检查容器监听
docker exec <container> netstat -tlnp

# 3. 检查防火墙
iptables -L -n | grep <port>

# 4. 测试本地访问
curl localhost:<port>
```

**解决：**
```bash
# 检查容器绑定地址
# 确保应用监听 0.0.0.0 而不是 127.0.0.1

# 开放防火墙
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# 或使用 firewalld
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload
```

---

### 案例 7：数据卷权限问题

**现象：** 容器内无法写入挂载目录

**排查步骤：**
```bash
# 1. 检查主机目录权限
ls -la /host/data

# 2. 检查容器内用户
docker exec <container> id

# 3. 测试写入
docker exec <container> touch /data/test
```

**解决：**
```bash
# 修改主机目录权限
chown -R 1000:1000 /host/data
chmod -R 755 /host/data

# 或使用相同 UID 运行容器
docker run -u $(id -u):$(id -g) -v /host/data:/data app

# 或修改容器内用户
docker run --user 0 -v /host/data:/data app chown -R 1000:1000 /data
```

---

### 案例 8：容器间无法通信

**现象：** 同一网络的容器无法互访

**排查步骤：**
```bash
# 1. 检查网络
docker network inspect <network>

# 2. 检查容器 IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

# 3. 测试连通性
docker exec web ping db

# 4. 检查防火墙
iptables -L -n | grep docker
```

**解决：**
```bash
# 确保容器在同一网络
docker network connect <network> <container>

# 启用 ICC（容器间通信）
docker network create --opt com.docker.network.bridge.enable_icc=true mynet

# 重启 Docker
systemctl restart docker
```

---

### 案例 9：Docker Compose 启动失败

**现象：** `docker compose up` 报错

**排查步骤：**
```bash
# 1. 验证配置文件
docker compose config

# 2. 查看详细错误
docker compose up --debug

# 3. 检查服务依赖
docker compose config --services

# 4. 查看已创建的资源
docker compose ps -a
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| YAML 语法错误 | 使用 `docker compose config` 验证 |
| 端口冲突 | 修改端口映射 |
| 卷已存在 | `docker volume rm` |
| 网络冲突 | `docker network prune` |

---

### 案例 10：构建镜像失败

**现象：** `docker build` 失败

**排查步骤：**
```bash
# 1. 查看详细错误
docker build --progress=plain .

# 2. 检查 Dockerfile 语法
hadolint Dockerfile

# 3. 检查上下文
ls -la .

# 4. 无缓存构建
docker build --no-cache .
```

**常见原因：**
| 原因 | 解决方案 |
|------|----------|
| 基础镜像不存在 | 检查 FROM 指令 |
| 文件不存在 | 检查 COPY/ADD 路径 |
| 命令执行失败 | 检查 RUN 指令 |
| 网络问题 | 配置镜像加速器 |

---

### 案例 11：容器 OOM

**现象：** 容器被杀死，状态为 OOMKilled

**排查步骤：**
```bash
# 1. 查看容器状态
docker inspect <container> | grep -A 5 "OOMKilled"

# 2. 查看内存使用
docker stats <container>

# 3. 查看系统日志
dmesg | grep -i "killed process"

# 4. 检查限制
docker inspect <container> | grep Memory
```

**解决：**
```bash
# 增加内存限制
docker update --memory=1g <container>

# 或修改 compose 文件
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
```

---

### 案例 12：Docker 守护进程响应慢

**现象：** docker 命令执行缓慢

**排查步骤：**
```bash
# 1. 检查守护进程状态
systemctl status docker

# 2. 查看日志
journalctl -u docker -f

# 3. 检查容器数量
docker ps -a | wc -l

# 4. 检查磁盘 IO
iostat -x 1
```

**解决：**
```bash
# 清理未使用资源
docker system prune -a

# 重启 Docker
systemctl restart docker

# 限制日志大小
# 配置 daemon.json log-opts
```

---

### 案例 13：容器时间不正确

**现象：** 容器内时间与主机不一致

**排查步骤：**
```bash
# 1. 检查主机时间
date

# 2. 检查容器时间
docker exec <container> date

# 3. 检查时区
docker exec <container> cat /etc/localtime
```

**解决：**
```bash
# 挂载时区文件
docker run -v /etc/localtime:/etc/localtime:ro app

# 或设置环境变量
docker run -e TZ=Asia/Shanghai app

# 或在 Dockerfile 中
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

---

### 案例 14：Registry 认证失败

**现象：** `docker login` 或 `docker push` 失败

**排查步骤：**
```bash
# 1. 检查凭据
cat ~/.docker/config.json

# 2. 重新登录
docker logout registry.example.com
docker login registry.example.com

# 3. 检查 Registry 状态
curl -I https://registry.example.com:5000/v2/

# 4. 查看 Registry 日志
docker logs registry
```

**解决：**
```bash
# 使用访问令牌
docker login -u admin -p Secret registry.example.com

# 或配置凭据存储
apt-get install pass
# Docker 会自动使用 pass 存储凭据
```

---

### 案例 15：容器健康检查失败

**现象：** 容器状态为 unhealthy

**排查步骤：**
```bash
# 1. 查看健康状态
docker inspect <container> | grep -A 10 "Health"

# 2. 查看健康检查日志
docker inspect <container> --format='{{json .State.Health.Log}}' | jq

# 3. 手动执行健康检查
docker exec <container> <healthcheck-command>
```

**解决：**
```bash
# 调整健康检查参数
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost/

# 或禁用健康检查
docker run --health-cmd="none" app
```

---

### 案例 16：多阶段构建失败

**现象：** 多阶段构建时找不到构建产物

**排查步骤：**
```bash
# 1. 检查阶段名称
docker build --progress=plain .

# 2. 验证文件存在
docker build --target builder .
docker run --rm -it <builder-image> ls -la /app

# 3. 检查路径
# 确保 COPY --from= 路径正确
```

**解决：**
```dockerfile
# 确保使用正确的阶段名称
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp .

FROM alpine:3.18
# 使用阶段名称或索引
COPY --from=builder /app/myapp /myapp
# 或 COPY --from=0 /app/myapp /myapp
```

---

### 案例 17：容器无法解析 DNS

**现象：** 容器内 nslookup 失败

**排查步骤：**
```bash
# 1. 测试 DNS
docker run --rm busybox nslookup google.com

# 2. 检查 Docker DNS
cat /etc/docker/daemon.json | grep dns

# 3. 检查容器 DNS 配置
docker exec <container> cat /etc/resolv.conf
```

**解决：**
```bash
# 配置 Docker DNS
cat > /etc/docker/daemon.json << EOF
{
  "dns": ["8.8.8.8", "114.114.114.114"]
}
EOF
systemctl restart docker

# 或运行时指定
docker run --dns 8.8.8.8 --dns 114.114.114.114 app
```

---

### 案例 18：绑定挂载不生效

**现象：** 主机文件修改容器内看不到

**排查步骤：**
```bash
# 1. 检查挂载
docker inspect <container> | grep -A 10 "Mounts"

# 2. 检查主机路径
ls -la /host/path

# 3. 检查容器内路径
docker exec <container> ls -la /container/path

# 4. 检查 SELinux
getenforce
```

**解决：**
```bash
# SELinux 上下文
docker run -v /host/path:/container/path:z app

# 或使用命名卷
docker volume create myvol
docker run -v myvol:/container/path app
```

---

### 案例 19：容器重启循环

**现象：** 容器反复重启

**排查步骤：**
```bash
# 1. 查看重启次数
docker inspect <container> | grep RestartCount

# 2. 查看日志
docker logs <container>
docker logs <container> --previous

# 3. 检查退出码
docker inspect <container> | grep ExitCode

# 4. 禁用重启测试
docker update --restart=no <container>
```

**常见退出码：**
| 退出码 | 含义 |
|--------|------|
| 0 | 正常退出 |
| 1 | 应用错误 |
| 125 | Docker 错误 |
| 126 | 命令不可执行 |
| 127 | 命令未找到 |
| 137 | OOMKilled |
| 143 | SIGTERM |

---

### 案例 20：网络冲突

**现象：** 创建网络或启动容器时 IP 冲突

**排查步骤：**
```bash
# 1. 查看网络配置
docker network ls
docker network inspect <network>

# 2. 检查 IP 分配
docker network inspect <network> | grep IPAddress

# 3. 查看冲突
docker network inspect <network> | grep -A 20 "Containers"
```

**解决：**
```bash
# 删除冲突网络
docker network rm <network>

# 创建新网络指定子网
docker network create --subnet=172.30.0.0/16 mynet

# 清理未使用网络
docker network prune
```

---

### 案例 21：Docker Build 缓存问题

**现象：** 构建使用了过期的缓存

**排查步骤：**
```bash
# 1. 查看构建缓存
docker build --progress=plain .

# 2. 检查 Dockerfile 顺序
# 确保频繁变化的文件放在后面

# 3. 无缓存构建
docker build --no-cache .
```

**解决：**
```dockerfile
# 优化 Dockerfile 顺序
# 先复制不频繁变化的文件
COPY package*.json ./
RUN npm install

# 再复制频繁变化的文件
COPY . .
```

---

### 案例 22：容器 CPU 使用率高

**现象：** 容器占用大量 CPU

**排查步骤：**
```bash
# 1. 查看资源使用
docker stats

# 2. 查看容器进程
docker top <container>

# 3. 进入容器排查
docker exec -it <container> top
```

**解决：**
```bash
# 限制 CPU
docker update --cpus=1.0 <container>

# 或启动时限制
docker run --cpus=1.0 app

# 优化应用
# 检查应用是否有死循环或资源泄漏
```

---

### 案例 23：Volume 无法删除

**现象：** `docker volume rm` 失败

**排查步骤：**
```bash
# 1. 查看卷使用情况
docker volume inspect <volume>

# 2. 查找使用卷的容器
docker ps -a --filter volume=<volume>

# 3. 检查匿名卷
docker volume ls --filter dangling=true
```

**解决：**
```bash
# 停止并删除使用卷的容器
docker stop <container>
docker rm <container>
docker volume rm <volume>

# 强制删除
docker volume rm -f <volume>

# 清理悬空卷
docker volume prune
```

---

### 案例 24：Docker Socket 权限问题

**现象：** 无法访问 /var/run/docker.sock

**排查步骤：**
```bash
# 1. 检查权限
ls -la /var/run/docker.sock

# 2. 检查用户组
groups $USER

# 3. 测试访问
docker info
```

**解决：**
```bash
# 添加用户到 docker 组
usermod -aG docker $USER
newgrp docker

# 或修改权限（不推荐）
chmod 666 /var/run/docker.sock
```

---

### 案例 25：Compose 网络不通

**现象：** Compose 服务间无法通信

**排查步骤：**
```bash
# 1. 查看网络
docker compose config

# 2. 检查服务网络
docker network inspect <project>_default

# 3. 测试连通性
docker compose exec web ping db

# 4. 查看容器 IP
docker compose exec web hostname -i
```

**解决：**
```yaml
# 确保服务在同一网络
services:
  web:
    networks:
      - default
  db:
    networks:
      - default

# 或使用服务名访问
# 在 web 容器内访问 http://db:3306
```

---

### 案例 26：镜像层数过多

**现象：** 构建警告层数过多

**排查步骤：**
```bash
# 1. 查看镜像历史
docker history <image>

# 2. 检查 Dockerfile
# 统计 RUN 指令数量
```

**解决：**
```dockerfile
# 合并 RUN 指令
RUN apt-get update && \
    apt-get install -y pkg1 pkg2 pkg3 && \
    rm -rf /var/lib/apt/lists/*

# 使用多阶段构建
FROM builder AS build
# ...
FROM runtime
COPY --from=build ...
```

---

### 案例 27：容器日志丢失

**现象：** `docker logs` 无输出

**排查步骤：**
```bash
# 1. 检查日志驱动
docker inspect <container> | grep LogPath

# 2. 查看日志文件
cat /var/lib/docker/containers/<id>/<id>-json.log

# 3. 检查应用输出
docker exec <container> cat /app/logs/app.log
```

**解决：**
```bash
# 确保应用输出到 stdout/stderr
# 不要输出到文件

# 修改日志驱动
docker run --log-driver=syslog app
```

---

### 案例 28：Docker 更新后不兼容

**现象：** Docker 升级后容器异常

**排查步骤：**
```bash
# 1. 查看 Docker 版本
docker --version

# 2. 查看容器状态
docker ps -a

# 3. 查看日志
journalctl -u docker -f
```

**解决：**
```bash
# 回滚 Docker 版本
apt-get install docker-ce=<previous-version>

# 或更新容器配置
docker update <container>

# 重建容器
docker rm <container>
docker run ...
```

---

### 案例 29：生产环境镜像过大

**现象：** 镜像超过 1GB

**排查步骤：**
```bash
# 1. 查看镜像大小
docker images

# 2. 分析镜像
docker history <image>

# 3. 使用工具分析
docker-slim build <image>
```

**解决：**
```dockerfile
# 使用更小的基础镜像
FROM alpine:3.18  # 5MB
# 或
FROM debian:bullseye-slim  # 80MB

# 多阶段构建
FROM golang:1.21 AS builder
# ...
FROM alpine:3.18
COPY --from=builder /app/myapp .

# 清理缓存
RUN apt-get clean && rm -rf /var/cache/apt/*
```

---

### 案例 30：安全漏洞扫描告警

**现象：** 镜像扫描发现漏洞

**排查步骤：**
```bash
# 1. 扫描镜像
docker scan <image>

# 2. 查看详情
docker scan --json <image> | jq

# 3. 检查基础镜像
docker history <image>
```

**解决：**
```bash
# 更新基础镜像
docker pull alpine:latest

# 更新包
RUN apt-get update && apt-get upgrade -y

# 使用安全基础镜像
FROM alpine:3.18  # 使用最新安全版本

# 或忽略特定漏洞（评估后）
# docker scan --severity=high <image>
```

---

## 13. 最佳实践

### ✅ 镜像构建

1. **使用具体版本标签**
   ```dockerfile
   FROM alpine:3.18  # ✅
   FROM alpine:latest  # ❌
   ```

2. **多阶段构建**
   ```dockerfile
   FROM golang:1.21 AS builder
   # ... 构建 ...
   FROM alpine:3.18
   COPY --from=builder /app/myapp .
   ```

3. **减少镜像层数**
   ```dockerfile
   RUN apt-get update && apt-get install -y pkg1 pkg2 && rm -rf /var/cache/apt/*
   ```

4. **使用 .dockerignore**
   ```
   .git
   node_modules
   *.md
   __pycache__
   ```

### ✅ 容器运行

1. **设置资源限制**
   ```bash
   docker run --memory=512m --cpus=1.0 app
   ```

2. **使用健康检查**
   ```dockerfile
   HEALTHCHECK --interval=30s CMD curl -f http://localhost/
   ```

3. **非 root 用户运行**
   ```dockerfile
   USER appuser
   ```

4. **只读根文件系统**
   ```bash
   docker run --read-only app
   ```

### ✅ 数据持久化

1. **使用命名卷**
   ```bash
   docker run -v myvol:/data app
   ```

2. **定期备份**
   ```bash
   docker run --rm -v myvol:/data -v $(pwd):/backup alpine tar cvf /backup/backup.tar /data
   ```

3. **避免绑定挂载敏感数据**
   ```bash
   # 使用 Docker Secret
   ```

### ✅ 网络安全

1. **使用自定义网络**
   ```bash
   docker network create isolated
   ```

2. **限制端口暴露**
   ```bash
   docker run -p 127.0.0.1:8080:80 app
   ```

3. **启用 TLS**
   ```bash
   # 配置 daemon.json tls 选项
   ```

### ✅ 监控日志

1. **配置日志轮转**
   ```json
   {
     "log-driver": "json-file",
     "log-opts": {"max-size": "100m", "max-file": "3"}
   }
   ```

2. **集中日志收集**
   ```bash
   docker run --log-driver=fluentd app
   ```

3. **设置告警**
   - 容器重启 > 5 次/小时
   - 磁盘使用率 > 80%
   - 内存使用率 > 90%

### ✅ CI/CD 集成

```yaml
# GitHub Actions 示例
name: Docker Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker Image
      run: docker build -t myapp:${{ github.sha }} .
    - name: Scan for vulnerabilities
      run: docker scan myapp:${{ github.sha }}
    - name: Push to Registry
      run: |
        docker login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PASS }}
        docker push myapp:${{ github.sha }}
```

---

## 📋 快速参考卡片

```bash
# ===== 镜像管理 =====
docker pull nginx:latest
docker build -t myapp:1.0 .
docker images
docker rmi <image>
docker save -o backup.tar <image>
docker load -i backup.tar

# ===== 容器管理 =====
docker run -d -p 8080:80 --name web nginx
docker ps -a
docker stop/start/restart <container>
docker logs -f <container>
docker exec -it <container> bash
docker rm <container>

# ===== 数据卷 =====
docker volume create myvol
docker volume ls
docker run -v myvol:/data app
docker volume rm myvol

# ===== 网络 =====
docker network create mynet
docker network ls
docker run --network mynet app
docker network connect/disconnect

# ===== Docker Compose =====
docker compose up -d
docker compose down
docker compose ps
docker compose logs -f
docker compose build

# ===== 清理 =====
docker system prune -a --volumes
docker image prune
docker container prune
docker volume prune
docker network prune

# ===== 故障排查 =====
docker inspect <container>      # 查看详情
docker logs <container>         # 查看日志
docker stats                    # 查看资源
docker events                   # 查看事件
journalctl -u docker -f         # 守护进程日志
```

---

## 🔗 相关资源

- **官方文档：** https://docs.docker.com/
- **Docker Hub：** https://hub.docker.com/
- **Docker GitHub：** https://github.com/docker
- **最佳实践：** https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- **安全指南：** https://docs.docker.com/engine/security/

---

> 💡 **刺刺提醒：**
> 1. 生产环境别用 latest 标签！用具体版本号！😈
> 2. 所有容器必须设置资源限制！
> 3. 定期清理未使用资源！
> 4. 敏感数据用 Secret 管理！
> 5. 文档里的 30 个案例都是常见坑，务必熟悉！
> 6. 备份卷比恢复卷容易一万倍！
## 常用指令

- systemctl status docker
- journalctl -u docker --since "30 min ago"
- docker ps -a
- docker logs <container-name> --tail=200
- docker inspect <container-name>
- docker stats --no-stream
- docker images
- docker system df
- docker network ls
- docker volume ls
- docker compose ps
- docker compose logs --tail=200

