---
title: "UPS 通过 ping 实现 NAS 断电自动关机"
date: 2020-06-18T11:00:48+08:00
description: ""
tags: [UPS, NAS]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

没有数据通讯的UPS，只有电源接口，无法判断断电后自动关机,保护数据安全,这里通过ping简单实现

思路，ups只接NAS，路由接市电，通过每隔一定时间通过NAS ping路由IP地址来确认是否停电，如果ping没有问题，就是有电，如果突然断电，ping不通了，就认为断电，执行关机命令。


TG500-1.sh脚本如下:
```bash
#!/bin/sh

ping -c 1 192.168.1.1 > /dev/null
ret=$?
if [ $ret -eq 0 ]
then
echo ' AC Power OK ! '
else
echo ' AC Power maybe off, checking again after 4 minutes ! '
sleep 240
/usr/sbin/TG500-2.sh
fi
```

TG500-2.sh脚本如下:
```bash
#!/bin/sh

ping -c 1 192.168.1.1 > /dev/null
ret=$?
if [ $ret -eq 0 ]
then
echo ' AC Power OK ! '
else
echo ' AC Power off, shut down NAS ! '
/sbin/poweroff
fi
```
然后修改/etc/config/crontab文件，5分钟执行一次TG500-1.sh
```bash
*/5 * * * * /usr/sbin/TG500-1.sh
```
通过以上的脚本，得到的效果是如果断电，那么在9-14分钟内NAS就会自动关闭，如果路由只是重启，4分钟内不会关闭NAS
