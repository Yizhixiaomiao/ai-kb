# 应用 5xx、4xx 或后端不可用告警处理指南

```yaml
status: usable
type: troubleshooting
risk_level: high
review_required: true
asset_types: [server, business-system]
systems: [application, nginx, gateway, nacos]
issue_types: [service-unavailable, http-error]
tags: [5xx, 4xx, backend, application, nacos, gateway]
```

## 适用范围

- 适用于业务后端不可用、HTTP 5xx/4xx 错误突增、域名错误率超阈值、Nacos 注册掉线等应用可用性告警。
- 适用于规则名称包含“业务后端不可用”“5xx 告警”“4xx 错误”“nacos 注册掉线”等场景。

## 常见现象

- 网关、Nginx、Ingress 或应用监控出现 5xx/4xx 告警。
- 用户访问失败、接口超时或业务后端不可用。
- 服务实例从注册中心掉线。

## 判断依据

- 区分客户端请求错误、网关错误、后端应用错误和依赖服务异常。
- 结合错误率、请求量、发布变更、实例健康和日志判断。

## 处理步骤

1. 确认告警域名、接口、业务系统、错误码、时间窗口和影响范围。
2. 查看网关或入口层状态、后端实例健康、注册中心实例数和最近发布记录。
3. 查看应用日志、错误堆栈、依赖数据库/缓存/第三方接口状态。
4. 如果是发布后异常，按预案回滚或切换流量。
5. 如果是单实例异常，优先摘除异常实例或重启实例，并保留日志供分析。
6. 如果是流量突增，按限流、扩容或降级预案处理。
7. 记录错误码、影响接口、根因、恢复动作和是否需要补充业务知识。

## 常用指令

- curl -I https://<domain>/<path> -- ?????? HTTP ?????????????
- curl -s -o /dev/null -w "%{http_code} %{time_total}\n" https://<domain>/<path> -- ????????????????
- tail -n 200 /var/log/nginx/error.log -- ?? Nginx ????????????
- tail -n 200 /var/log/nginx/access.log -- ?? Nginx ????????????
- grep " 5[0-9][0-9] " /var/log/nginx/access.log | tail -50 -- ???? 5xx ????????
- systemctl status nginx -- ?? Nginx ??????????
- systemctl status <app-service> -- ??????????????
- journalctl -u <app-service> --since "30 min ago" -- ????????????????
- kubectl get pod -n <namespace> -o wide -- ???? Pod ?????????????
- kubectl describe ingress <ingress-name> -n <namespace> -- ?? Ingress ???????????
- kubectl logs <pod-name> -n <namespace> --tail=200 -- ???? Pod ??????????
- kubectl rollout history deployment/<deployment-name> -n <namespace> -- ?????????????????????????

## 验证方式

- 5xx/4xx 错误率回落到正常范围。
- 业务接口健康检查和用户访问恢复。
- 注册中心实例数、网关后端状态和应用日志正常。

## 注意事项

- 不要只看错误码，必须结合请求量和影响范围判断严重程度。
- 重启、回滚、限流、扩容属于生产变更，应按业务预案执行。
- 涉及数据一致性问题时应升级给业务系统负责人和数据库工程师。
