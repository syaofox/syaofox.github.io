---
title: "查看当前linux mint 基于ubuntu哪个版本"
created_at: "2025-10-07 00:00:35"
updated_at: "2025-10-07 00:00:35"
issue_number: 19
state: open
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/19
---

# 查看当前linux mint 基于ubuntu哪个版本

```shell
cat /etc/upstream-release/lsb-release
```
显示类似消息:

```shell
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu Noble Numbat"
```

或者打开系统报告,查看系统信息

<img width="1015" height="648" alt="Image" src="https://github.com/user-attachments/assets/813c2100-99ef-4d13-9d21-3dd376052ec9" />

