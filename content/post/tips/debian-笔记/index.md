---
title: "Debian 笔记"
date: 2022-01-21T16:10:23+08:00
draft: false
categories: [Tips]
tags: [temp,linux,debian]
---

## 添加sudo权限

```shell
usermod -aG sudo username
```

## MacBook Broadcom 4360 无线网卡驱动
首先，启用非免费存储库。通过将`non-free` 添加到您的`/etc/apt/sources.list`文件中。
```shell
sudo apt-get update
sudo apt-get install broadcom-sta-*
sudo modprobe wl
echo "wl" | sudo tee -a /etc/modules
```
不要忘记tee命令中的-a，否则您将覆盖整个文件！
如果无法立即使用，请重新启动，应该没问题。