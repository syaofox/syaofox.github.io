---
title: "Arch Linux on Btrfs 安装教程"
created_at: "2025-10-23 03:58:57"
updated_at: "2025-10-23 03:58:57"
issue_number: 48
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/48
---

# Arch Linux on Btrfs 安装教程

一份**详细、完整、并采用 Btrfs 文件系统**的 Arch Linux 安装教程。

本教程融合了以下所有定制需求：

  * **文件系统：** Btrfs，用于快照和回滚。
  * **分区/子卷：** 1G `/boot` (ESP, `nvme0n1p1`), Btrfs 顶级卷 (`nvme0n1p2`), 包含 `@`, `@home`, `@swap`, `@log`, `@cache` 子卷。
  * **Swap：** 64G Swapfile。
  * **引导程序：** `systemd-boot`。
  * **基础环境：** 极简命令行，无桌面环境。
  * **本地化：** 中文语言包，系统环境显示英文 (`LANG=en_US.UTF-8`)，Fcitx5 输入法框架。
  * **主机名/用户：** `dev` / `syaofox`。
  * **开发/驱动：** `base-devel`, `git`, `nvidia-open` 驱动。
  * **软件包管理：** AUR 助手 `paru`，快照工具 `snapper`。

-----

# 🚀 Arch Linux Btrfs 开发者定制完整安装教程

## 阶段一：预安装准备 (Pre-installation)

### 1\. 引导、网络与时间同步

1.  下载 Arch Linux ISO 文件并写入 USB 驱动器。
2.  通过 **UEFI** 模式启动电脑，进入 Arch Linux Live 环境。
3.  **检查网络连通性：**
      * **有线：** 检查 `ip a`。
      * **无线：** 运行 `iwctl`，然后使用 `station wlan0 scan/get-networks/connect "Your-Wifi-SSID"` 连接。
      * 测试：`ping archlinux.org`
4.  **同步系统时间：**
    ```bash
    timedatectl set-ntp true
    ```

### 2\. 硬盘分区 (Partition the disk)

主硬盘：`/dev/nvme0n1`。

```bash
fdisk /dev/nvme0n1
```

1.  **创建 `/boot` (ESP) 分区 (`nvme0n1p1`)：**
      * `n` (New) -\> 分区号 `1` -\> 起始扇区默认 -\> 大小 `+1G`。
      * `t` (Type) -\> 类型码 `1` (EFI System)。
2.  **创建 Btrfs 根分区 (`nvme0n1p2`)：**
      * `n` (New) -\> 分区号 `2` -\> 起始扇区默认 -\> 大小默认（使用剩余全部）。
      * `t` (Type) -\> 类型码 `20` (Linux filesystem)。
3.  **保存并退出：** `w`。

### 3\. 格式化分区 (Formatting)

```bash
# 格式化 /boot (ESP) 分区为 FAT32
mkfs.fat -F 32 /dev/nvme0n1p1

# 格式化 Btrfs 根分区
mkfs.btrfs -f /dev/nvme0n1p2
```

### 4\. 挂载顶级卷并创建子卷

首先，挂载 Btrfs 顶级卷，然后创建您所需的子卷结构。

```bash
# 挂载 Btrfs 顶级卷 (subvolid=5)
mount /dev/nvme0n1p2 /mnt

# 创建子卷 (Subvolumes)
btrfs subvolume create /mnt/@        # 根目录
btrfs subvolume create /mnt/@home    # 家目录
btrfs subvolume create /mnt/@swap    # 用于存放 swapfile (禁用 CoW)
btrfs subvolume create /mnt/@log     # /var/log
btrfs subvolume create /mnt/@cache   # /var/cache

# 卸载顶级卷，准备重新挂载
umount /mnt
```

### 5\. 重新挂载子卷到最终挂载点

重新挂载时，应用 Btrfs 优化选项 (`compress=zstd`, `noatime`)。

```bash
# 挂载 @ 子卷作为根目录 /
mount -o subvol=@,compress=zstd,noatime /dev/nvme0n1p2 /mnt

# 创建其余子卷的挂载点
mkdir -p /mnt/{home,var/log,var/cache,swap,boot}

# 挂载其他子卷
mount -o subvol=@home,compress=zstd,noatime /dev/nvme0n1p2 /mnt/home
mount -o subvol=@log,compress=zstd,noatime /dev/nvme0n1p2 /mnt/var/log
mount -o subvol=@cache,compress=zstd,noatime /dev/nvme0n1p2 /mnt/var/cache
mount -o subvol=@swap /dev/nvme0n1p2 /mnt/swap # @swap 子卷不应启用压缩

# 挂载 /boot (ESP 分区)
mount /dev/nvme0n1p1 /mnt/boot
```

### 6\. 创建 64GB Swapfile

**禁用 `/mnt/swap` 子卷的写时复制 (CoW) 是创建 Swapfile 的必需步骤！**

```bash
# 禁用 /mnt/swap 目录的 CoW
chattr +C /mnt/swap

# 创建 64G swapfile
fallocate -l 64G /mnt/swap/swapfile

# 设置权限并格式化
chmod 600 /mnt/swap/swapfile
mkswap /mnt/swap/swapfile
```

## 阶段二：系统安装与 Chroot

### 7\. 安装基本系统、开发包和定制包

安装您所有要求的软件包。

```bash
# 1. 基础系统
pacstrap /mnt base linux linux-firmware systemd vim 

# 2. Btrfs 和开发工具
pacstrap /mnt btrfs-progs base-devel git 

# 3. NVIDIA Open 驱动和工具
pacstrap /mnt nvidia-open nvidia-settings nvidia-utils

# 4. 输入法框架
pacstrap /mnt fcitx5 fcitx5-chinese-addons
```

### 8\. 生成 fstab 文件

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

**重要：手动编辑 `/mnt/etc/fstab` 检查并添加 Swapfile 配置**

```bash
nano /mnt/etc/fstab
```

  * **检查：** Btrfs 挂载选项是否正确，特别是 `@swap` 子卷是否挂载。
  * **添加 Swapfile 配置：**
    ```
    /swap/swapfile none swap defaults 0 0
    ```

保存并退出。

### 9\. 进入新系统环境 (Chroot)

```bash
arch-chroot /mnt
```

## 阶段三：系统配置与引导

### 10\. 时区与本地化

1.  **设置时区：**
    ```bash
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
    hwclock --systohc
    ```
2.  **本地化 (中文包，英文环境)：**
      * 编辑 `/etc/locale.gen`，取消 `en_US.UTF-8 UTF-8` 和 `zh_CN.UTF-8 UTF-8` 的注释。
      * `locale-gen`。
      * 设置系统环境为英文：`echo "LANG=en_US.UTF-8" > /etc/locale.conf`。

### 11\. 主机名和网络

1.  **设置主机名 (`dev`)：**
    ```bash
    echo "dev" > /etc/hostname 
    ```
2.  **编辑 `/etc/hosts` 文件：**
    ```bash
    nano /etc/hosts
    # 添加：127.0.1.1	dev.localdomain	dev
    ```
3.  **启用网络管理服务：**
    ```bash
    pacman -S networkmanager 
    systemctl enable NetworkManager
    ```

### 12\. Root 密码和用户 (`syaofox`)

1.  **设置 root 密码**：`passwd`。
2.  **创建用户 `syaofox`**：
    ```bash
    useradd -m -g users -G wheel syaofox
    passwd syaofox
    ```
3.  **配置 `sudo`**：
      * `visudo`，取消 `%wheel ALL=(ALL:ALL) ALL` 的注释。

### 13\. 配置 NVIDIA Open 驱动加载

1.  **编辑 `/etc/mkinitcpio.conf`：**
    ```bash
    nano /etc/mkinitcpio.conf
    ```
    在 `MODULES` 数组中添加 NVIDIA 模块：
    ```
    MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)
    ```
2.  **重新生成 initramfs 镜像：**
    ```bash
    mkinitcpio -P
    ```

### 14\. 安装和配置引导程序 - systemd-boot

1.  **安装 bootctl：**
    ```bash
    bootctl install
    ```
2.  **安装 CPU 微码：**
    ```bash
    pacman -S intel-ucode # 或 amd-ucode
    mkinitcpio -P # 再次生成 initramfs
    ```
3.  **创建引导条目 `/boot/loader/entries/arch.conf`：**
      * 获取 Btrfs 根分区 UUID：`blkid /dev/nvme0n1p2` (记下 UUID)。
      * 创建文件：
        ```bash
        nano /boot/loader/entries/arch.conf
        ```
        **注意：** Btrfs 引导时需要指定 `rootflags=subvol=@` 来挂载根目录子卷。
        ```
        title   Arch Linux
        linux   /vmlinuz-linux
        initrd  /intel-ucode.img 
        initrd  /initramfs-linux.img
        options root=UUID=YOUR_ROOT_UUID rw rootflags=subvol=@
        ```
4.  **配置 loader.conf：**
    ```bash
    nano /boot/loader/loader.conf
    # 确保默认设置如下：
    # default arch
    # timeout 4
    # editor no
    ```

## 阶段四：收尾和首次启动

### 15\. 完成并重启

1.  **退出 chroot 环境：**
    ```bash
    exit
    ```
2.  **卸载所有已挂载分区：**
    ```bash
    umount -R /mnt
    ```
3.  **重启系统：**
    ```bash
    reboot
    ```
    **⚠ 拔掉 USB 启动盘！**

## 阶段五：首次启动后的配置

系统重启后，以用户名 `syaofox` 登录。

### 16\. 安装 Paru AUR 助手

```bash
# 切换到用户家目录
cd ~

# 1. 克隆 paru 仓库
git clone https://aur.archlinux.org/paru.git
cd paru

# 2. 编译并安装 paru
makepkg -si

# 3. 清理
cd ..
rm -rf paru
```

### 17\. 安装 Snapper 和自动快照工具

使用 `paru` 安装 Btrfs 快照和自动快照工具。

```bash
paru -S snapper snap-pac grub-btrfs 
# snap-pac 负责在 pacman/paru 操作前后自动创建快照。
```

### 18\. 配置 Snapper 快照

为需要快照的子卷创建配置。

1.  **创建根目录 (@) 配置：**
    ```bash
    sudo snapper create-config -f root @
    ```
2.  **创建家目录 (@home) 配置：**
    ```bash
    sudo snapper create-config -f home @home
    ```
3.  **启用 Snapper 自动清理服务：**
    ```bash
    sudo systemctl enable --now snapper-timeline.timer
    sudo systemctl enable --now snapper-cleanup.timer
    ```

### 19\. 安装 Brave 浏览器

```bash
paru -S brave-bin
```

### 20\. Fcitx5 环境变量配置 (命令行环境提示)

Fcitx5 需要图形环境才能工作。在 `syaofox` 用户的 shell 配置文件中设置以下环境变量，以便在您启动任何图形程序时输入法能正常工作。

```bash
# 编辑用户的 bash 配置文件
nano ~/.bashrc

# 在文件末尾添加以下内容：
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export SDL_IM_MODULE=fcitx

# 立即生效
source ~/.bashrc
```

至此，您的 Arch Linux Btrfs 开发者定制环境已配置完成。

