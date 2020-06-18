---
title: "利用 Windows 自带的资源监视器查看文件占用"
date: 2020-06-18T10:35:52+08:00
description: ""
tags: [资源监视器]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---

经常当我们删除文件时，有时会提示【操作无法完成，因为文件已在另一个程序中打开，请关闭该文件并重试】，到底是哪些程序呢？

有时候一个一个找真不是办法，已经被这个问题折磨很久了，今天下决心要把它解决，找到办法了。如果系统是win7以上，可以这么做：

在开始菜单中的搜索框内输入“资源监视器”，回车，打开“资源监视器”。

看下图，在“资源监视器”界面中，点击第二个选项卡“CPU”。在“关联的句柄”右侧搜索框内输入文件名称，点击右侧下拉箭头，就可以查看该文件被那几个程序占用了。

![](/利用windows自带的资源监视器查看文件占用/20200618103858.jpg)

选中程序，右击选择结束进程。

![](/利用windows自带的资源监视器查看文件占用/20200618104345.jpg)