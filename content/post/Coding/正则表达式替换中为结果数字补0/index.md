---
title: "正则表达式替换中为结果数字补0"
date: 2022-02-12T17:16:24+08:00
description: ""
image: ""
categories: [Coding]
tags: [正则]
toc: true
---

分两步实现
1. **先为数字添加多个0**
   
   查找
   `第(\d+)话`
   替换为
   `000000$1`
2. **第二次替换,去掉多余的0**
   
   查找`第0*([0-9]{3})话`替换为`$1`
   
   `{3}`表示匹配最长3个字符,达到补0到三位数的目的