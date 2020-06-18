---
title: "重新安装windows无法选择版本的问题"
date: 2020-06-18T10:50:46+08:00
description: ""
tags: [安装系统]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---

有些品牌机在重新安装系统时无法选择windows版本，默认安装家庭版，解决这个问题很简单

新建txt文档，复制粘贴下面几行字符，保存，修改文件名为ei.cfg(连同后缀名一块修改)。然后将这个文件添加到镜像中的sources文件夹内即可。如果想保存为ISO镜像，需要使用ISO编辑软件添加此文件。如果是通过U盘，硬盘安装，在制作好U盘启动盘或者解压后添加即可。

```ini
[EditionID]
[Channel]
Retail
[VL]
0
```