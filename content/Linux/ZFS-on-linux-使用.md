---
title: "ZFS on Linux 使用"
date: 2020-06-18T11:13:29+08:00
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

Linux上的ZFS项目是OpenZFS的实现，旨在在Linux环境中工作。OpenZFS是一个出色的存储平台，它包含传统文件系统，卷管理器等的功能，并且在所有发行版中均具有一致的可靠性，功能和性能。有关OpenZFS的其他信息，请参见[OpenZFS维基百科文章](https://en.wikipedia.org/wiki/OpenZFS)。

本文以 Ubuntu 下使用 ZFS 为例

<!--more-->

## 硬件需求

- 建议的硬件要求是：ECC内存。这并不是必须的，但强烈建议。
- 8GB +的内存以获得最佳性能。也完全可以用2GB或更少的内存来运行,前提是禁用数据去重。

## 安装

```bash
sudo apt install zfsutils
```

## 创建存储池

- RAID0 条带式，速度提升，没有冗余盘，单盘数据损坏全部数据丢失

  ```bash
  zpool create your-pool /dev/sdc /dev/sdd
  ```

- RAID1 镜像，一对一冗余，空间损失1半，任意单盘数据损坏可以无痛还原

  ```bash
  zpool create your-pool mirror /dev/sdc /dev/sdd
  ```

- RAIDZ1 单盘奇偶校验，至少需要3盘，可用空间=单盘*（盘-1），允许算坏一盘不丢失数据

  ```bash
  zpool create your-pool raidz1 /dev/sdc /dev/sdd /dev/sde
  ```

- RAIDZ2/RAIDZ3 同RAIDZ1，增加了校验盘数量

  ```bash
  zpool create your-pool raidz2 /dev/sdc /dev/sdd /dev/sde /dev/sdf
  ```

  

## 创建池时选择设备名

创建ZFS池时，可以使用不同的设备名。每个选项都有优缺点，取决于现实需求。

- **/dev/sdX，/dev/hdX：**最适合开发/测试池
  - 优点：此方法易于快速测试，名称简短，兼容所有Linux发行版中。
  - 缺点：名称会根据检测到磁盘的顺序改变导致池出错。这时需要删除`zpool.cache`文件，并使用新名称重新导入池。
  - 例： `zpool create tank sda sdb`

- **/dev/disk/by-id /：**最适合小型池（少于10个磁盘）

  - 优点：名称是永久性的不会更改，磁盘可以随便安装。
  - 缺点：不方便辨认硬盘。
  - 例： `zpool create tank scsi-SATA_Hitachi_HTS7220071201DP1D10DGG6HMRP`

- **/dev/disk/by-path /：**适用于大型池（大于10个磁盘）

  - 简介：使用设备名称，其中包括系统中的物理线缆布局。
  - 优点：大型存储里方便定位。
  - 缺点：名称冗长难于管理。
  - 例： `zpool create tank pci-0000:00:1f.2-scsi-0:0:0:0 pci-0000:00:1f.2-scsi-1:0:0:0`


更改现有池的设备名
-- 

通过导出现有池,然后在导入时指定设备名即可

```bash
zpool export tank
zpool import -d /dev/disk/by-id tank
```

## /etc/zfs/zpool.cache文件

缓存文件记录池配置信息,记录了池的状态和设备名,缓存异常时使用以下命令检测并导入该池

```bash
/etc/zfs/zpool.cache file
zpool import
zpool import -d /dev/disk/by-id
```

## 生成一个新的/etc/zfs/zpool.cache文件

`/etc/zfs/zpool.cache`更改池配置后，该文件将自动更新。更新异常可使用`/etc/zfs/zpool.cache`命令在池中设置cachefile属性来强制生成新缓存文件。

```bash
zpool set cachefile=/etc/zfs/zpool.cache tank
```

相反，可以禁用缓存文件。

```bash
zpool set cachefile=none tank
```

## 池的操作

- 查看池的状态

  ```bash
  zpool status
  ```

- 重新插回硬盘后,有时候会自动识别,有时候不会,可以手动通知zpool

  ```bash
  zpool online pool 设备名
  ```

- 更换损坏的硬盘

  ```bash
  # 模拟sdb损坏
  dd if=/dev/zero of=/dev/sdb
  
  # 扫描池提示sdb掉线
  zpool scrub 
  
  #更换设备
  zpool replace pool 坏盘 新盘
  
  ```

- 导出池

  ```bash
  zpool export tank
  ```

  导入池

  ```bash
  # -f 代表强制导入
  zpool import -f dozer 
  
  # 池中存在名称冲突时先查看池的数字id
  zpool import 
  zpool import 数字id
  ```

- 池数据清理

    ```bash
    zpool scrub your-pool #数据清理
    zpool status -v your-pool #显示清理状态
    zpool scrub -s your-pool #停止清理
    ```



## ZFS配置

查看 zfs 属性

- 查看zfs文件系统信息

  ```bash
  zfs list
  ```

- 查询属性

  ```bash
  zfs get #列出所有属性
  zfs get version #查询指定属性
  ```

  

CEPH文件存储后端严重依赖于xattrs，为获得最佳性能，所有CEPH工作负载将受益于以下ZFS数据集参数

- `xattr=sa`
- `dnodesize=auto`

## 4k对齐

要强制池在池创建时使用4,096字节扇区，可以运行：

```bash
zpool create -o ashift=12 tank mirror sda sdb
```

要在将vdev添加到池中时强制池使用4,096字节扇区，可以运行：

```bash
zpool add -o ashift=12 tank mirror sdc sdd
```

## 开启压缩

默认不开启压缩，建议开启

```bash
zfs create -o compression=lz4
# 查看是否开启数据压缩
zfs get compression
# 查看压缩倍率
zfs get compressratio
```

## 创建 回滚和销毁 ZFS 快照

```bash
zfs snapshot -r your-pool/downloads@ss1 #为downloads数据集创建了名位ss1快照
zfs rollback -r your-pool/downloads@ss1 #将downloads数据回滚到ss1快照
zfs destroy -r your-pool/downloads@ss1 #将ss1快照销毁
```

## 显示和访问 ZFS 快照

可以通过 `listsnapshots` 池属性启用或禁用 `zfs list` 输出中的快照列表显示。缺省情况下，此属性处于启用状态。

如果禁用了此属性,则可以使用 `zfs list` `-t snapshot` 命令来显示快照信息。