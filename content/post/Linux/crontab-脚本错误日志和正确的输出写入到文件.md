---
title: "Crontab 脚本错误日志和正确的输出写入到文件"
date: 2020-06-18T12:08:17+08:00
description: ""
tags: [Linux, Crontab]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

crontab 脚本运行时,需要把运行日志写入到日志中方便查阅,本文介绍一下如果控制输出内容

- 如果crontab不重定向输出，并且crontab所执行的命令有输出内容的话，是一件非常危险的事情。因为该输出内容会以邮件的形式发送给用户，内容存储在邮件文件

```bash
/var/spool/mail/$user
```

> 如果命令执行比较频繁（如每分钟一次），或者命令输出内容较多，会使这个邮件文件不断追加内容，文件越来越大。而邮件文件一般存放在根分区，根分区一般相对较小，所以会造成根分区写满而无法登录服务器。
>

- 不输出内容

```bash
*/5 * * * * /root/XXXX.sh &>/dev/null 2>&1 
```

- 将正确和错误日志都输出到 /tmp/load.log

```bash
*/1 * * * * /root/XXXX.sh > /tmp/load.log 2>&1 &
```

- 只输出正确日志到 /tmp/load.log

```bash
*/1 * * * * /root/XXXX.sh > /tmp/load.log &  等同于   */1 * * * * /root/XXXX.sh 1>/tmp/load.log &
```

- 只输出错误日志到 /tmp/load.log

```bash
*/1 * * * * /root/XXXX.sh 2> /tmp/load.log & 
```

> 名词解释
>
> 在shell中，每个进程都和三个系统文件相关联：标准输入stdin，标准输出stdout和标准错误stderr，三个系统文件的文件描述符分别为0，1和2。所以这里2>&1的意思就是将标准错误也输出到标准输出当中。
>

> \> 就相当于 1> 也就是重定向标准输出，不包括标准错误。通过2>&1，就将标准错误重定向到标准输出了（stderr已作为stdout的副本），那么再使用>重定向就会将标准输出和标准错误信息一同重定向了。如果只想重定向标准错误到文件中，则可以使用2> file。