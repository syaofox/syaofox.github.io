---
title: "利用fastgit加速aur软件安装下载速度"
date: 2022-03-31 14:57:59+08:00
description: ""
image: ""
categories: [Tips]
tags: [linux,archlinux]
---
## 安装多线程下载工具

```shell
sudo pacman -S axel
```
## 创建脚本

```shell
sudo vi /usr/local/bin/fake_axel_for_makepkg
```

```shell
#! /bin/bash
# 该脚本用于处理yay安装软件时，由github下载缓慢甚至无法下载的问题
# 检测域名是不是github，如果是，则替换为镜像网站，依旧使用curl下载
# 如果不是github则采用axel代替curl进行15线程下载

domin=`echo $2 | cut -f3 -d'/'`;
others=`echo $2 | cut -f4- -d'/'`;
case "$domin" in
    "github.com")
    url="https://download.fastgit.org/"$others;
    echo "download from github mirror $url";
    /usr/bin/curl -gqb "" -fLC - --retry 3 --retry-delay 3 -o $1 $url;
    ;;
    *)
    url=$2;
    /usr/bin/axel -n 15 -a -o $1 $url;
    ;;
esac

```
赋予权限
```shell
sudo chmod +x /usr/local/bin/fake_axel_for_makepkg

```

## 编辑makepkg.conf

将htts协议修改为自定义脚本接管

```shell
sudo vi /etc/makepkg.conf
```
修改https协议部分
```shell
#-- The download utilities that makepkg should use to acquire sources
#  Format: 'protocol::agent'
DLAGENTS=('file::/usr/bin/curl -qgC - -o %o %u'
          'ftp::/usr/bin/curl -qgfC - --ftp-pasv --retry 3 --retry-delay 3 -o %o %u'
          'http::/usr/bin/curl -qgb "" -fLC - --retry 3 --retry-delay 3 -o %o %u'
          'https::/usr/local/bin/fake_axel_for_makepkg %o %u'
          'rsync::/usr/bin/rsync --no-motd -z %u %o'
          'scp::/usr/bin/scp -C %u %o')

```