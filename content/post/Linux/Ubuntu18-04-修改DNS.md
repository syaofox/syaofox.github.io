---
title: "Ubuntu18 04 修改DNS"
date: 2020-06-18T11:20:07+08:00
description: ""
tags: []
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

最近使用了最新版的ubuntu 18.04运行一些服务，发现服务器经常出现无法解析域名的情况。

<!--more-->

检查/etc/resolv.conf文件，发现里面nameserver是127.0.0.53，修改以后过了段时间，又被修改回去，查找资料原来18.04版本DNS是由systemd-resolved管理的。

```shell
netstat -tnpl| grep systemd-resolved
```

通过以上命令查看到这个服务是监听在53号端口上。

/etc/systemd/resolved.conf大致内容如下：

```shell
[Resolve]
DNS=223.5.5.5 8.8.8.8
#FallbackDNS=
#Domains=
LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#Cache=yes
#DNSStubListener=yes
```

修改这里面的内容，然后重启systemd-resolved服务即可。

```shell
systemctl restart systemd-resolved.service
```

如果想要用/etc/resolve.conf控制，直接将systemd-resolved服务停止并禁用。

```shell
systemctl stop systemd-resolved.service
systemctl disable systemd-resolved.service
```

这样世界就清净了。