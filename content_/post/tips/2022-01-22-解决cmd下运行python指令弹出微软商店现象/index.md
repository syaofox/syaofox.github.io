---
title: "解决cmd下运行python指令弹出微软商店现象"
date: 2022-01-22T10:51:35+08:00
description: ""
image: ""
categories: [Tips]
tags: [windows]
draft: false
---

## 问题
win10系统下下载了python之后每次使用cmd执行python指令都会自动弹出微软商店
解决方案:
在查询菜单栏中搜索“管理应用执行别名” ,将应用安装程序的两项关掉可以解决

## 设置执行别名
### 创建新别名
```shell
New-Alias "word" "C:\Windows\System32\notepad.exe"
```
### 修改别名
```shell
set-Alias "wd" "C:\Windows\System32\notepad.exe"
```