---
title: "Ubuntu 配置 ZFS Event Daemon"
date: 2020-06-18T12:09:42+08:00
description: ""
tags: [Ubuntu, ZED]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

## 一、安装软件

zed是zfs的一个事件服务，需要安装zfs-zed来使用，同时，为了能邮件通知，还需要安装`mailutils msmtp msmtp-mta s-nail`

```c
apt-get install mailutils msmtp msmtp-mta s-nail zfs-zed
```

## 二、配置msmtp

修改或新建/etc/msmtprc

```c
defaults
auth           login
#tls_starttls   off
tls            off
#tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        ~/.msmtp.log

account alerts
host smtp.qq.com
port 25
from 地址@qq.com
user 地址@qq.com
password xxxx       #这里的密码是smtp的验证密码，不是邮箱登录密码

# Set a default account
account default : alerts
```

配置完后`echo "test mail" | mail -s "test" 地址@qq.com`测试是否能收到邮件。

## 三、配置zed

```
vi /etc/zfs/zed.d/zed.rc
```

```c
ZED_EMAIL_ADDR="地址@qq.com"
ZED_EMAIL_PROG="mail"
ZED_EMAIL_OPTS="-s '@SUBJECT@' @ADDRESS@ -r 地址@qq.com"
ZED_NOTIFY_INTERVAL_SECS="3600"
ZED_NOTIFY_VERBOSE=1
ZED_DEBUG_LOG="/tmp/zed.debug.log"
ZED_SYSLOG_PRIORITY="daemon.notice"
ZED_SYSLOG_TAG="zed"
```

Restart zfs-zed

```css
systemctl restart zfs-zed.service
```

/etc/aliases file:



```css
root: brismuth
brismuth: brismuth@gmail.com
```

You’ll want to replace “brismuth” with your username and you’ll want to use your own email address at the end. This file tells your computer that all email intended for the “root” user should be sent to the “brismuth” user, and that all email intended for the “brismuth” user should be sent to “[brismuth@gmail.com]

## 四、测试验证

```
zpool scrub pool
```

## 五、计划任务



```ruby
# zpool scrub every month
0 2 1 * * /sbin/zpool scrub pool
0 13 1 * * /sbin/zpool status
```
