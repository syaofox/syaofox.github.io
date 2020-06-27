---
title: "基于 ZFS 文件系统的 OpenMediaVault 安装记录"
date: 2020-06-01T11:12:00+08:00
description: "「记录安装基于 ZFS 文件系统的 OpenMediaVault 安装过程。本篇不是教程，部分步骤略过不表」"
tags: [ZFS, NAS, OMV, OpenMediaVault]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

## 安装系统

注意事项：

- 镜像选清华镜像 [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn/)

- 修改引导防止挂载路径变化后无法引导

  获得磁盘UUID

  ```bash
  blkid
  
  /dev/sda1: UUID="8305-3011" TYPE="vfat" PARTUUID="2b972aa5-f2fd-475a-8353-77594dc8a1e1"
  /dev/sda2: UUID="f4add2f3-efd0-42df-b23d-e453ab285aa3" TYPE="ext4" PARTUUID="f120845a-5b97-4eb3-884d-43fb45b41720"
  /dev/sda3: UUID="9fcacfa0-cb8d-45be-9efc-3f8d8222f03e" TYPE="swap" PARTUUID="acf58c24-4829-41b5-b326-6d295e3d720a"
  ```

  修改引导文件`/boot/grub/grub.cfg`

  把`boot=/dev/sda2` 改成 `boot=UUID=f4add2f3-efd0-42df-b23d-e453ab285aa3`

  重启测试

  ```bash
  update-grub
  ```

- 修改时区

- 修改密码

- 修改后台登出时间

- 修改网络DHCP -> 静态IP

- 更新系统

- 安装`OMV-EXTRAS`

  ```bash
  wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash
  ```

  

## 安装并配置 ZFS 文件系统

- 更换`Proxmox`内核

  - 重启

  - 删除`non-Proxmox`内核

  - 安装 zfs 插件

  - 重启

  - 更新系统

  - 重启

- 创建 zfs 池`pool`

- 设置池属性

  ```bash
  # 设置继承
  zfs set aclinherit=passthrough pool  
  # 设置扩展属性,一开始就必须设置,改变设置只会对新文件生效
  zfs set acltype=posixacl pool
  zfs set acltype=posixacl pool
  # 开启压缩,lz4占用资源很少,速度很快
  zfs set compression=lz4 
  ```

- **可选 **限制zfs最大内存使用为4G（物理内存的一半），理论上在不影响其他服务的情况下，默认管理即可（默认4G内存以上使用最大内存-1G）

  ```bash
  echo "options zfs zfs_arc_max=4294967296" | sudo tee -a /etc/modprobe.d/zfs.conf
  echo 4294967296 > /sys/module/zfs/parameters/zfs_arc_max
  ```

  重启后查看

  ```bash
  cat /proc/spl/kstat/zfs/arcstats | grep c_max
  ```

- 设置自动创建快照
  
  - 安装`ZnapZend`
  
    ```bash
    # 安装必要组件 不想安装perl可以下载二进制文件存到/opt/
    apt-get update
    apt-get install perl unzip    
    apt-get install  gcc automake autoconf libtool make
    
    wget https://github.com/oetiker/znapzend/releases/download/v0.20.0/znapzend-0.20.0.tar.gz
    tar zxvf znapzend-0.20.0.tar.gz
    cd znapzend-0.20.0
    ./configure --prefix=/opt/znapzend-0.20.0
    make
    make install
    
    # 设置环境变量 可选
    for x in /opt/znapzend-0.20.0/bin/*; do ln -s $x /usr/local/bin; done
    ```
  
  - 设置`ZnapZend`
  
    - 创建规则
  
    ```bash
    # pool 备份规则代表 1小时备份1次保留最新的2周,1天备份一次保留最新的3个月,1星期备份一次保留最新的10年
    znapzendzetup create --tsformat='znapzend-%Y-%m-%d-%H%M%S' SRC '2w=>1h,3m=>1d,10y=>1w' pool 
    
    # 测试规则
    znapzendzetup list
    znapzend --noaction --debug --runonce=pool
    ```
  
    - 创建`znapzend systemctl`服务
  
      - 复制安装时生成的服务文件`/root/znapzend-0.20.0/init/znapzend.service`到`/etc/systemd/system/`
  
      - 启动并设置开启自动启动
  
        ```bash
        # 重载系统服务
        #systemctl daemon-reload
        
        # 设置开机启动
        systemctl enable znapzend.service
        # 启动服务
        systemctl start znapzend.service
        ```
  
      - 重启后查看是否自动启动
  
        ```bash
        systemctl status znapzend.service
        ps -aux | grep "znapzend"
        ```
  
        

## 安装 Docker 与 Porainer

- OMV-Extras 直接安装

## 安装 UPS 管理插件

- 插件名`openmediavault-nut 5.1.0-1`

## 设置邮件通知

- 以GMail为例
  
  SMTP 服务器: smtp.gmail.com

  SMTP 端口: 587

  加密模式: 启用TLS

  发送Email: Gmai账号

  需要验证: 打开

  用户名: Gmail账号
  
  密码: Gmail密码,开启两步验证的账号请使用应用专用密码


