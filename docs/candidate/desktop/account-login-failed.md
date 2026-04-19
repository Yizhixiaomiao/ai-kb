# 账号、密码或权限导致登录失败处理指南

```yaml
status: usable
type: troubleshooting
asset_types: [account, business-system]
systems: [mes, oa, plm, authentication-client]
issue_types: [login-failed, permission]
tags: [account, password, permission, login]
source: ticket-history
evidence_count: 227
owner: ""
reviewer: ""
updated_at: 2026-04-17
```

## 适用范围

适用于内部平台、MES、OA、PLM、认证助手等系统登录异常、密码错误、权限不足、账号异常问题。

## 常见现象

- 系统提示登录异常或无法登录。
- 认证助手密码报错。
- 内部平台账号问题。
- 调岗后无法访问原系统或新增系统。

## 处理步骤

1. 确认用户身份、工号和所属部门。
2. 确认登录系统名称和报错提示。
3. 判断是密码错误、账号锁定、权限缺失还是系统异常。
4. 对密码类问题按账号管理流程重置或指导用户自助处理。
5. 对权限类问题确认审批或权限申请记录。
6. 对单系统异常，联系对应系统管理员确认账号状态。

## 验证方式

- 用户能成功登录目标系统。
- 用户能访问所需功能菜单或业务页面。

## 风险点

- 不要绕过权限审批直接授权。
- 账号处理必须确认用户身份。

## 升级条件

- 批量用户无法登录。
- 账号状态正常但系统仍拒绝访问。
- 涉及生产权限、敏感数据或跨部门授权。


