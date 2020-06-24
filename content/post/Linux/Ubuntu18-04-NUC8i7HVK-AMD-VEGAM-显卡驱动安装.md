---
title: "Intel NUC 冥王峡谷（NUC8i7HVK）安装 Ubuntu18 AMD 显卡的驱动方法"
date: 2020-06-18T11:23:52+08:00
description: ""
tags: [Ubuntu, NUC, 显卡]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

## 升级 BIOS

- 从 [这里](https://downloadcenter.intel.com/download/28073/BIOS-Update-HNKBLi70-86A-) 下载BIOS文件
- 按照 [说明](https://www.intel.com/content/www/us/en/support/articles/000005850/mini-pcs.html) 更新 BIOS

## 安装 Ubuntu

- BIOS内关闭安全启动
  
## 更新内核

AMD GPU的驱动程序随Linux 4.17一起提供，根据测试，只有4.18才提供正式支持，所以必须升级内核。

手动升级

```bash
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.18-rc5/linux-headers-4.18.0-041800rc5_4.18.0-041800rc5.201807152130_all.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.18-rc5/linux-headers-4.18.0-041800rc5-generic_4.18.0-041800rc5.201807152130_amd64.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.18-rc5/linux-image-unsigned-4.18.0-041800rc5-generic_4.18.0-041800rc5.201807152130_amd64.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.18-rc5/linux-modules-4.18.0-041800rc5-generic_4.18.0-041800rc5.201807152130_amd64.deb
sudo dpkg -i linux-*.deb
```

或者

```bash
sudo add-apt-repository ppa:teejee2008/ppa
sudo apt update
sudo apt install ukuu
```
从GUI运行UKUU，选择Linux Kernel 4.18.3，重新启动。
>注意：确保BIOS内安全启动已经关闭

重启后查看内核

```bash
uname -a
```


### 添加并更新 Mesa

```bash
sudo add-apt-repository ppa:ubuntu-x-swat/updates
sudo apt dist-upgrade
```

### 获得AMD Vega M Linux驱动程序并将其放在适当的目录中

```bash
wget -m -np https://people.freedesktop.org/~agd5f/radeon_ucode/vegam/
sudo cp people.freedesktop.org/~agd5f/radeon_ucode/vegam/*.bin /lib/firmware/amdgpu
```

然后更新Ramdisk以识别/选择正确的内核:

```bash
sudo /usr/sbin/update-initramfs -u -k all
```

### 关闭 nomodeset 选项

- 修改引导文件 `/etc/default/grub` 设置`GRUB_CMDLINE_LINUX_DEFAULT=""`
- 运行 `sudo update-grub2` 更新引导并重新启动
