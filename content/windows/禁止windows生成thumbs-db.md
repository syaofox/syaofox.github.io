---
title: "禁止 windows 生成 thumbs.db"
date: 2020-06-18T10:31:40+08:00
description: ""
tags: [thumbs, 缩略图]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---

1. 按下 Win+R 打开“运行”，输入：gpedit.msc 回车;
   
    ![](/禁止windows生成thumbs-db/1569154295281.jpg)

2. 在打开的组策略窗口中，依次点开：
  
    用户配置>管理模版>Windows 组件

    找到右侧的“文件资料管理器”，双击打开;

    ![](/禁止windows生成thumbs-db/1569154318392.jpg)

3. 找到并双击打开“关闭隐藏的thumbs.db文件中的缩略图缓存”;

4. 勾选“已启用”并“应用”设置，下次开机之后thumbs.db就不见了。

    ![](/禁止windows生成thumbs-db/1569154337114.jpg)
