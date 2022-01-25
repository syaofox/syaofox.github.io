---
title: "Linux 笔记"
date: 2022-01-21T16:10:23+08:00
draft: false
categories: [Tips]
tags: [temp,linux,debian,ubuntu]
---


## Debian
### 添加sudo权限

```shell
usermod -aG sudo username
```

### MacBook Broadcom 4360 无线网卡驱动
首先，启用非免费存储库。通过将`non-free` 添加到您的`/etc/apt/sources.list`文件中。
```shell
sudo apt-get update
sudo apt-get install broadcom-sta-*
sudo modprobe wl
echo "wl" | sudo tee -a /etc/modules
```
不要忘记tee命令中的-a，否则您将覆盖整个文件！
如果无法立即使用，请重新启动，应该没问题。

### 查看当前debian版本
简单信息
```shell
cat /etc/issue
```
debian版本号
```shell
cat /etc/debian_version
```
debian详细信息
```shell
cat /etc/os-release
```

### 挂载ntfs格式
安装`ntfs-3g`
```shell
sudo apt install ntfs-3g
```
命令挂载
```shell
mount -t ntfs-3g /dev/sda1 /mnt/windows
```
/etc/fstab
```shell
/dev/sda1 /mnt/windows ntfs-3g rw,uid=1000,gid=1000,dmask=0002,fmask=0003 0 0
```

## Ubuntu

### 修改ip
18，0以后使用netplan
修改位于` /etc/netplan/`下的yaml文件
加载生效
```shell
sudo netplan apply
```
也可以使用shell界面配置
```shell
sudo nmtui
```