---
title: "使用screen来实现多任务不断线操作命令"
date: 2020-06-18T10:59:04+08:00
description: ""
tags: [Linux命令, screen]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

## 前言

我们用`VPS`执行一个系统安装，就输入命令然后在那一直等。如果出现掉线或者断网死机的情况，我们还得重新安装。如果能使用上`screen`命令可以实现无人值守的效果。我们可以同时操作多个任务，也可以关机操作。所以说很方便。

## 方法

**1、安装方法：**

```shell
yum install screen  #CentOS
apt-get install screen  #Debian或者Ubuntu
```

**2、创建一个screen会话：**

```shell
screen -S xx  #xx为创建会话的名称
```

**3、隐藏并保留当前会话窗口：**

```shell
按Ctrl+A，再按"D"键
```

如果怕中途掉线或者要离开的话，可以使用。  
**4、恢复会话窗口：**

```shell
screen -r xx #恢复名字为xx的会话
```

如果在恢复会话的时候忘记了或者没有设定会话名称我们就要执行：

```shell
screen -ls
```

他会列出你所有的会话列表，然后使用：

```shell
screen -r 会话名称
```

来恢复会话窗口。  
**5、关闭会话窗口：**

```shell
exit
```

`screen`的好处就是不会因为远程的操作因网络问题中断掉。

