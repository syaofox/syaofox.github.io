---
title: "Rsync 命令比对文件及增量同步"
date: 2020-06-18T11:56:31+08:00
description: ""
tags: [Linux命令, Rsync]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

rsync基于ssh协议实现高效率远程或本地文件复制，传输速度比scp快。复制文件时会比对本地文件与远程主机的文件，仅复制有差异的文件。

## 常用选项：

```shell
-q,--quiet：suppress non-error messages 静默模式
-v,--verbose：increase verbosity
-a,--archive：archive mode; equals -rlptgoD (no -H,-A,-X) 归档模式，相当于-rlptgoD,不包括(no -H,-A,-X);最常用的参数
-H,--hard-links：preserve hard links 保留硬链接
-A,--acls：preserve ACLs (implies --perms) 保留ACL权限
-X,--xattrs：preserve extended attributes 保留扩展属性
-c, --checksum：skip based on checksum, not mod-time & size
-r,--recursive：recurse into directories 递归
-l,--links：copy symlinks as symlinks 保留软链接,而不跟踪原文件
-p,--perms：preserve permissions 保留权限
-t,--times：preserve modification times 保留mtime
-g,--group：preserve group 保留属组
-o,--owner：preserve owner (super-user only) 保留属主
-D：same as --devices,--specials 保留设备文件和特殊文件
--devices：preserve device files (super-user only)
--specials：preserve special files

-z,--compress：compress file data during the transfer 输过程中压缩文件数据
-n, --dry-run：perform a trial run with no changes made 干跑测试
-u,--update：skip files that are newer on the receiver 增量同步，跳过比本地较新的文件
--delete：delete extraneous files from destination dirs 删除目标目录多余文件
--progress：show progress during transfer 显示传输进度
```

## 本地复制

```shell
rsync -av ansible_auto/public/uy-s-192-v01.cfg objects/ansible_auto/public/uy-s-192-v01.cfg
```

## 比对文件

```shell
cd /usr/local/nagios/etc/
rsync -acvn ansible_auto/ objects/ansible_auto/ > diff
```

## 增量同步（合并目录文件，最终与目标目录一致）

```shell
rsync -avzu --progress /opt/* devops@11.0.10.8:/opt/
```

## 删除同步（删除目标目录多余文件，最终与源目录一致）

```shell
rsync -avzu --delete --progress /opt/* devops@11.0.10.8:/opt/
```

## 另外，可以设置计划任务实时同步和备份文件

```shell
crontab -e
*/1 * * * * rsync -avzu /opt/media/* 192.168.201.123:/opt/media
```