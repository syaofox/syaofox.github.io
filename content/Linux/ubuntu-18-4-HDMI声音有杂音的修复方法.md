---
title: "Ubuntu 18 4 HDMI声音有杂音的修复方法"
date: 2020-06-18T11:19:25+08:00
description: ""
tags: [Ubuntu, 声音]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

显示器自带音箱，通过hdmi连接电脑，安装完ubuntu 18后声音出现比较大的杂音...

<!--more-->

google找到以下方法，亲测完美解决

```shell
sudo pico /etc/pulse/default.pa
```

在弹出的文本内查找以下字眼

```shell
load-module module-udev-detect
```

在后面添加`tsched=0` 完成后像这样

```shell
load-module module-udev-detect tsched=0
```

重启后世界清静了～～