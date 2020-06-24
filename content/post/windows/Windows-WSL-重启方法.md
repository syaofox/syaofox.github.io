---
title: "Windows WSL 重启方法"
date: 2020-06-18T10:24:18+08:00
description: ""
tags: [WSL]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---

Windows 10 子系统 wsl 的重启方法

以管理员权限运行`cmd`或者`PowerShell`执行以下命令

```bash
net stop LxssManager	//停止
net start LxssManager	//启动
```
