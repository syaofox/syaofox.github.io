---
title: "Openwrt自动更新bt Tracker"
date: 2022-01-30T16:57:49+08:00
description: ""
image: ""
categories: [Tips]
tags: [openwrt]
toc: true
---

## 创建脚本

```shell
#!/bin/bash

list=`wget -qO- https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt|awk NF|sed ":a;N;s/\n/,/g;ta"`

uci set aria2.main.bt_tracker=${list}
uci commit aria2
/etc/init.d/aria2 restart

```

## 定时执行更新脚本
系统-计划任务-添加任务
```shell
# 每天凌晨1点执行
0 1 * * * /etc/config/auto_sync_aria2c_tracker.sh >/dev/null 2>&1
```