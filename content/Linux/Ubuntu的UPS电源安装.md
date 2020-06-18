---
title: "Ubuntu 的 UPS 电源安装"
date: 2020-06-18T11:02:01+08:00
description: ""
tags: [UPS, Ubuntu]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

跑程序，网络不是最重要，但是长时间的稳定电源还是非常重要的，所以加一个UPS可以避免一些短时间的断电。

首先看看usb有没有成功连接到ups电源,一般会出现下面信息
```bash
$ lsusb Bus 002 Device 004: ID 051d:0002 American Power Conversion Uninterruptible Power Supply
```

安装很简单，就是一句命令
```bash
sudo apt-get -y install apcupsd
```
备份文件
```bash
sudo cp /etc/apcupsd/apcupsd.conf /etc/apcupsd/apcupsd.conf.bak
```
编辑下面文件

sudo nano /etc/apcupsd/apcupsd.conf

```bash
UPSNAME smartups750
UPSCABLE usb
UPSTYPE usb
DEVICE 
POLLTIME 60
```

另外一个文件

```bash
sudo cp /etc/default/apcupsd /etc/default/apcupsd.bak
sudo nano /etc/default/apcupsd
```

内容为
```bash
ISCONFIGURED=yes
```
重启服务
```bash
sudo systemctl restart apcupsd.service
```

然后可以运行下面命令看ups电源的状态

```bash
$ apcaccess status
APC      : 001,037,0923
DATE     : 2017-02-05 04:57:23 +0800  
HOSTNAME : gtx1080
VERSION  : 3.14.12 (29 March 2014) debian
UPSNAME  : gtx1080
CABLE    : USB Cable
DRIVER   : USB UPS Driver
UPSMODE  : Stand Alone
STARTTIME: 2017-02-05 02:45:22 +0800  
MODEL    : Back-UPS XS 1400U  
STATUS   : ONLINE 
LINEV    : 230.0 Volts
LOADPCT  : 7.0 Percent
BCHARGE  : 100.0 Percent
TIMELEFT : 83.1 Minutes
MBATTCHG : 5 Percent
MINTIMEL : 3 Minutes
MAXTIME  : 0 Seconds
SENSE    : Medium
LOTRANS  : 155.0 Volts
HITRANS  : 280.0 Volts
ALARMDEL : No alarm
BATTV    : 28.1 Volts
LASTXFER : Low line voltage
NUMXFERS : 1
XONBATT  : 2017-02-05 03:09:35 +0800  
TONBATT  : 0 Seconds
CUMONBATT: 672 Seconds
XOFFBATT : 2017-02-05 03:20:47 +0800  
SELFTEST : NO
STATFLAG : 0x05000008
SERIALNO : 3B1644X34934  
BATTDATE : 2016-11-05
NOMINV   : 230 Volts
NOMBATTV : 24.0 Volts
NOMPOWER : 700 Watts
FIRMWARE : 926.T2 .I USB FW:T2
END APC  : 2017-02-05 04:57:28 +0800 
```
在空载的情况下可以运行
```bash
TIMELEFT : 83.1 Minutes
````