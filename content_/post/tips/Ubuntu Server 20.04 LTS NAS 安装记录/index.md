---
title: "Ubuntu Server 20.04 LTS NAS 安装记录"
date: 2020-06-01T11:15:54+08:00
description: "「Nas 安装 Ubuntu Server 20.04 LTS 系统，基于 zfs on linux」"
tags: [ubuntu, nas]
categories:
    - Tips
---

## 安装 Ubuntu

注意选中安装ssh,否则安装完成无法远程连接

## 更新系统

```bash
sudo apt update
sudo apt upgrade
```

## 设置时区

```bash
# 查看当前时区
timedatectl
```

```bash
# 列出所有时区
timedatectl list-timezones
# 显示亚洲时区
timedatectl list-timezones | grep Asia
```

```bash
# 设置时区为上海
sudo timedatectl set-timezone Asia/Shanghai
```

## 修改 root 用户登录权限

```bash
# 编辑 '/etc/ssh/sshd_config'
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# 重启SSH服务
sudo systemctl restart ssh

# 设置root账号密码
sudo passwd root
初始化硬盘
```

```bash
# 查看分区情况
lsblk
# 使用 gdisk 初始化硬盘
```

## 添加账号

```bash
adduser wife 
```

## 使用 ZFS 系统

```bash
# 安装 zfs
apt update
apt install zfsutils-linux

# 重启

# 创建 RAIDZ2 存储池 /dev/disk/by-id
zpool create pool raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde 

# 查看存储池状态
zpool status -v

# 查看存储池空间
df -h | grep pool

# 创建数据集并设置开启lz4压缩
zfs create -o compression=lz4 pool/share
zfs create -o compression=lz4 pool/media
zfs create -o compression=lz4 pool/work 
zfs create -o compression=lz4 pool/me

# 修改各数据集挂载点权限
chmod -R 777 /pool/share
chmod -R 777 /pool/media
chmod -R 777 /pool/work
chmod -R 777 /pool/me
```

## 安装 samba 并设置 samba 共享

```bash
# 安装 samba
apt install samba

# 备份配置文件
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak 

# 修改配置文件 添加共享文件夹配置
nano /etc/samba/smb.conf

# 所有人可以访问
[share]
 path = /pool/share
 browseable = yes
 read only = no
 public = yes

# syaofox 可读写 wife 可读
[media]
 path = /pool/media
 browseable = yes
 read only = no
 valid users = syaofox wife
 read list = syaofox wife
 write list = syaofox

# syaofox 可读写 wife 可读
[work]
 path = /pool/work
 browseable = yes
 read only = no
 valid users = syaofox wife
 read list = syaofox wife
 write list = syaofox

# syaofox可读写
[me]
 path = /pool/me
 browseable = yes
 read only = no
 valid users = syaofox

# 创建 samba 用户
smbpasswd -a syaofox
smbpasswd -a wife

# 重启 samba 服务
service smbd restart
```

## 安装 docker

```bash
# 安装依赖包
apt update
apt install apt-transport-https ca-certificates curl software-properties-common

# 添加GPG
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 添加源,注意版本 这里对应20.04 focal
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt update

# 查看 apt 缓存,确保源生效
apt-cache policy docker-ce

# 安装 docker
apt install docker-ce

# 安装 Docker Compose 注意更新版本
curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 安装 portainer
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

通过服务器`ip:9000`访问`portainer`后台

添加国内镜像加快docker镜像拉取速度

- 科大 https://docker.mirrors.ustc.edu.cn
- 七牛云 https://reg-mirror.qiniu.com

