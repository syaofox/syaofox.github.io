---
title: "使用 Mergerfs 合并多块硬盘的剩余空间"
date: 2020-06-18T11:03:08+08:00
description: ""
tags: [Mergerfs]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

两年前，我买了一台 HP Gen8 微型服务器，其功能之一是作为网络存储。当时它只接了一块 SSD 作为系统盘和一块 2 TB HDD 作为存储盘。随着存储文件的增多，我又先后增加了两块 4 TB HDD，现在它已经接了共计 10 TB 的存储空间。我觉得有必要分享一下我用来将这些硬盘的空间合并在一起的工具——mergerfs。

原文出处:[https://wzyboy.im/post/1148.html](https://wzyboy.im/post/1148.html)

## 一、网络存储之硬盘困境

在讲工具之前，我有必要先说明一下我目前的存储方案。

我的 Gen8 没有直接装通用操作系统，而是先通过 ESXi 实现了虚拟化，再将存储盘通过 RDM 的方式完整地映射给其中的一台虚拟机（Arch Linux）。在 Arch Linux 里运行了 Samba, NFS, aria2 RPC, Transmission daemon, BorgBackup 等服务，供局域网电脑存取文件、远程下载，以及备份。

我在存储盘里的东西分为两类：一类是多份备份中的一份BorgBackup；另一类是从互联网上下载的可再生资源。前者本身有冗余，后者丢了不心疼。出于以上考虑，为了硬盘空间利用率的最大化，我并没有采用 RAID 1 或 RAID 5 之类的冗余存储的方案，而是采用了 JBOD 方案——Just Bunch of Disks。

不使用 RAID 做冗余还有一个原因：我希望这些硬盘从 Gen8 上拔下来之后接到别的电脑上我能直接读取它们。

当我的第一块存储盘快要装满的时候，我买了第二块盘，这时候就面临了一个问题：如何把两块硬盘的空间合并？考虑到我已经在运行的那些服务，我自然不想再增加一个额外的挂载点。我曾考虑过三个硬盘空间合并方案：

*   RAID 0。与 RAID 1 或 RAID 5 不同，RAID 0 是对多块相同容量的硬盘进行平行读写，从而提升性能，其额外效果就是硬盘空间也被合并了。但这种方案非常危险：多块硬盘中的任意一块挂了，所有的数据都将无法读取。这个方案不行。
*   LVM。相比 RAID 0 的原理，LVM 只是将空间连接起来了，而没有平行读写，所以多块硬盘中的一块挂了，也只是丢了那一块的数据。但创建过 LVM PV 的硬盘，在别的机器上读取起来比较麻烦，所以这个方案我也不喜欢。
*   MooseFS。相对前两种方案，由于它在 FUSE 层面实现，所以更灵活一些，甚至可以通过网络，把没有挂在 Gen8 上的硬盘也纳入存储空间。但这个方案和 LVM 一样，协作性不强，硬盘在别的机器上只能看到一堆数据碎块文件，因此也被我否决了。

以上三种方案还有一个问题：我需要把硬盘里现有的数据全部倒出来再倒进去……我需要的是能将文件分散存储到多块硬盘，同时又不改变文件形态的方案。

## 二、mhddfs 与 mergerfs

早有人遇到过像我一样的困境，于是他开发了 [mhddfs](https://romanrm.net/mhddfs)。在用了它一段时间之后，我又发现了一个更好的实现 [mergerfs](https://github.com/trapexit/mergerfs)。两者的思路类似，但后者比前者功能更丰富、更安全、更稳定。本文以后者为例说明。

mergerfs 的思路是用 FUSE 实现一个新的文件系统，它的下层存储并不是直接的块设备，而是别的已经挂载的文件系统。mergerfs 接收到读写请求时，它会根据约定好的策略，从下层文件系统中读取文件，或是将数据写入下层文件系统。mergerfs 所呈现的文件系统，容量是所有下层文件系统之和，而内容则是所有下层文件系统的合并。

引用 mergerfs README 里的 ASCII art：

```plain
A         +      B        =       C
/disk1           /disk2           /merged
|                |                |
+-- /dir1        +-- /dir1        +-- /dir1
|   |            |   |            |   |
|   +-- file1    |   +-- file2    |   +-- file1
|                |   +-- file3    |   +-- file2
+-- /dir2        |                |   +-- file3
|   |            +-- /dir3        |
|   +-- file4        |            +-- /dir2
|                     +-- file5   |   |
+-- file6                         |   +-- file4
                                  |
                                  +-- /dir3
                                  |   |
                                  |   +-- file5
                                  |
                                  +-- file6
```

如图所示，`/merged` 是 mergerfs 的挂载点，其下层两个文件系统的挂载点是 `/disk1` 和 `/disk2`。

这样一个文件系统完全符合我的需求：读写文件时能获得合并空间的优势，而当硬盘损坏或是想要直接读取硬盘里的数据的时候又可以单独把硬盘拆出来读取。而且我不用把现有的数据倒腾来倒腾去了，无痛迁移！

## 三、mergerfs 的安装与配置

mergerfs 的作者非常勤奋，每个版本都会为 RHEL / CentOS, Fedora, Debian, Ubuntu 不同发行版的不同版本、不同架构组合打包 30 多个 [rpm 和 deb 安装包](https://github.com/trapexit/mergerfs/releases)，其中包括了 ARM 甚至 PowerPC 架构，方便使用 Raspberry Pi 或是老 Mac 作为网络存储设备的用户。Arch Linux 用户则可以通过 AUR 安装。

安装之后通过编辑 `/etc/fstab` 来挂载 mergerfs。我使用的 fstab 如下：

```plain
/dev/sdb1               /media/disk1    ext4            defaults,noauto                 0 0
/dev/sdc1               /media/disk2    ext4            defaults,noauto                 0 0
/dev/sdd1               /media/disk3    ext4            defaults,noauto                 0 0
/media/disk1:/media/disk2:/media/disk3  /media/vdisk    fuse.mergerfs   defaults,noauto,allow_other,use_ino,minfreespace=100G,ignorepponrename=true 0 0
```

前三行是三块存储盘的普通挂载，第四行是 mergerfs 的条目，它的挂载源是前三块盘的的挂载点，用冒号分隔。最后一列的参数说明：

*   `defaults`: 开启以下 FUSE 参数以提升性能：atomic\_o\_trunc, auto\_cache, big\_writes, default\_permissions, splice\_move, splice\_read, splice\_write；
*   `noauto`: 禁止开机自动挂载。意外关机重启之后我可能需要手动检查文件系统后再挂载，所以我不希望它自动挂载；
*   `allow_other`: 允许挂载者以外的用户访问 FUSE。你可能需要编辑 `/etc/fuse.conf` 来允许这一选项；
*   `use_ino`: 使用 mergerfs 而不是 libfuse 提供的 inode，使硬链接的文件 inode 一致；
*   `minfreespace=100G`: 选择往哪个下层文件系统写文件时，跳过剩余空间低于 100G 的文件系统；
*   `ignorepponrename=true`: 重命名文件时，不再遵守路径保留原则，见下一节详解。

写完 fstab 之后就可以让 mergerfs 跑起来了：

```plain
mount /media/disk1 && mount /media/disk2 && mount /media/disk3 && mount /media/vdisk
```

效果：

```plain
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb1       1.8T  1.7T  179G  91% /media/disk1
/dev/sdc1       3.6T  3.4T  215G  95% /media/disk2
/dev/sdd1       3.6T   89M  3.4T   1% /media/disk3
1:2:3           9.0T  5.0T  3.8T  57% /media/vdisk
```

disk3 是我今天刚装上的，所以它还是空的。

## 四、mergerfs 的读写策略

如果多块硬盘里同名的目录或文件，从哪儿读？往哪儿写？如果多块硬盘都有足够的剩余空间，在哪块硬盘创建新文件？mergerfs 对 FUSE 的不同操作有着不同的读写策略。默认的策略是：

*   action 类别：对于 chmod, chown 等改变文件或目录属性的操作，mergerfs 检索所有下层文件系统，确保所有文件或目录都得到更改；
*   search 类别：对于 open, getattr 等读取文件或目录的操作，mergerfs **按挂载源列表的顺序**检索下层文件系统，返回第一个找到结果；
*   create 类别：对于 create, mkdir 等创建文件或目录的操作，mergerfs **优先选择相对路径已经存在的下层文件系统中剩余空间最大的那个作为写入目标**。

前两条很好理解，最后一条比较拗口。举例来说是这样：

*   disk1 剩余 100 GiB 空间，有 `/dir1` 目录；
*   disk2 剩余 200 GiB 空间，有 `/dir2` 目录；
*   disk3 剩余 300 GiB 空间，有 `/dir3` 目录；
*   mergerfs 将这三块硬盘的文件系统合并成一个，可以同时看到 `/dir1, /dir2, /dir3` 三个目录。

这时在 mergerfs 对于上层文件系统写入一个 150 GiB 的文件到 `/dir2/foo.bin` 位置，按照默认的策略，mergerfs 会选择 disk2 写入。因为：disk1 剩余空间不足（小于 `minfreespace` 或是只读文件系统也会被跳过选择），而虽然 disk3 比 disk2 剩余空间更多，但因为 disk2 已经有 `/dir2` 目录了，所以 mergerfs 会优先选择写入 disk2 而不是 disk3。

这个策略的意义在于，当下层文件系统的剩余空间差不多时，你的文件不会被分散开。比如你正在将你的[相机图片文件夹](https://en.wikipedia.org/wiki/Design_rule_for_Camera_File_system)复制到 mergerfs 里，一个文件夹里有 999 张图片，第一张图片的落点也将决定接下来 998 张文件的落点，而不会因为下层文件系统剩余空间的交替变化而一会儿落到这个文件系统，一会儿落到那个文件系统。最终下层文件系统会被平衡地使用，但相同目录的文件会尽可能地在同一个文件系统里，这非常棒。

但这个策略一直有一个痛点让我难受了很久：移动文件。比如 2016 年份的文件位于 disk1，而 2017 年份的文件因为 disk1 已经满了写到 disk2 来了，在 2018 年的时候我想把三年的文件都归到一个新目录里。此时 2016 年的文件可以瞬间完成，2017 年的文件则由于上述策略会优先选择 disk1，于是就从瞬间完成变成了缓慢的跨盘移动，当这些文件数量巨大的时候，已经开始的传输我又不敢贸然中止……这样的坑我在整理文件时掉过很多次。终于，mergerfs 2.23.0 版本新增了 `ignorepponrename` 选项，使得在重命名文件的时候，忽略路径保留规则，避免了简单的文件整理操作变成痛苦的跨盘移动的悲剧。

如果 mergerfs 的默认读写策略不适用于你的应用场景，可以通过挂载参数选用别的策略。

本文地址：[https://wzyboy.im/post/1148.html](https://wzyboy.im/post/1148.html)

* * *

## 读者来信：有关 ZFS

2018-02-11 读者 Rmrf99 <r...@protonmail.com> 来信推荐了 ZFS。Rmrf99 在自己的 Ubuntu 工作站上使用 ZFS 作为存储方案。我没有用过 Solaris，对 ZFS on Linux 也不是很了解。在 Rmrf99 的推荐下，我在 Ubuntu 虚拟机中尝试了 ZFS。ZFS 将 RAID / LVM 中的「卷」的概念与文件系统概念结合了：使用块设备直接创建 ZFS pool，而 pool 的更小单位就直接是文件系统了，调整大小、快照、缓存、加密、配额等都很方便，不再需要像 LVM 像俄罗斯套娃那样一层一层地操作。

然而，在我的使用场景下，ZFS 相比 mergerfs 有两点不适合我的地方：

*   有时我需要高速读取/写入大量数据，我目前的做法是直接将一块存储盘从 Gen8 上拔下来，使用 SATA-USB 转换器将其连接至计算机，而 ZFS pool 中的某个成员不能脱离 pool 单独工作，你也不能将一块已经加入 pool 的成员从 pool 中移除（除非拆毁 pool 并重建）；
*   相比 Ubuntu，目前 Arch Linux 对 ZFS on Linux 的支持不够完善，使用和维护成本较高，与 ZFS 的 zero administration 理念相违背。

此外，对于需要跨平台协作的用户来说，mergerfs 可以将不同文件系统的分区拼成一个，使 Ext4 与 NTFS 和谐共处，而 ZFS 在可预见的未来没有可用的 Windows 支持。
