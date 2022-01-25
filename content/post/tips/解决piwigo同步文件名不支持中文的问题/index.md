---
title: "解决piwigo同步文件名不支持中文的问题"
date: 2022-02-11T09:09:22+08:00
description: ""
image: ""
categories: [Tips]
tags: [docker,piwigo,相册]
toc: true
---

## 开启LocalFiles Editor插件

工具 > 插件 > 打开LocalFiles Editor

## 修改同步文件名过滤规则

搜索`sync_chars_regex`
将整行修改为

```shell
$conf['sync_chars_regex'] = '/^[\x{2e80}-\x{fe4f}a-zA-Z0-9-_.\(\)\[\]\!@#×\s]+$/u';
```