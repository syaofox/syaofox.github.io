---
title: "Arch Linux 安装教程"
created_at: "2025-10-23 03:55:14"
updated_at: "2025-10-23 03:55:14"
issue_number: 47
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/47
---

# Arch Linux 安装教程


  * **主机名：** `dev`
  * **用户名：** `syaofox`
  * **分区：** 1G `/boot` (ESP, `nvme0n1p1`), 根目录 (`nvme0n1p2`), 64G swapfile。
  * **环境：** 极简命令行环境，无桌面。
  * **软件包：** `git`, `base-devel`, `nvidia-open` 驱动, `fcitx5`, `paru`, `brave-bin` (最后通过 `paru` 安装)。
  * **本地化：** 中文语言包，系统环境显示英文。

-----

# 🚀 Arch Linux 完整安装教程 (开发者定制版)

## 阶段一：预安装准备 (Pre-installation)

### 1\. 引导安装介质与校验

1.  下载 Arch Linux ISO 文件并校验 PGP 签名。
2.  使用 `dd` 或 Etcher 等工具将 ISO 写入 USB 驱动器。
3.  通过 **UEFI** 模式启动电脑，进入 Arch Linux Live 环境。

### 2\. 检查网络连接

**有线连接**通常会自动连接。

**无线连接 (Wi-Fi)：**

```bash
# 运行交互式工具
iwctl 

# 查看设备
device list 

# 扫描并连接网络 (假设 Wi-Fi 设备名为 wlan0)
station wlan0 scan 
station wlan0 get-networks 
station wlan0 connect "Your-Wifi-SSID" 

# 退出 iwctl
exit 
```

**检查网络连通性：**

```bash
ping archlinux.org -c 3
```

### 3\. 更新系统时间

```bash
timedatectl set-ntp true
```

### 4\. 硬盘分区 (Partition the disk)

您的主硬盘是 NVMe 固态硬盘 `/dev/nvme0n1`。

```bash
fdisk /dev/nvme0n1
```

1.  **创建 `/boot` (ESP) 分区：**
      * 输入 `n` (创建新分区)。
      * 分区号 `1`。
      * 起始扇区：默认。
      * 大小：输入 `+1G`。
      * 输入 `t` (改变分区类型)。
      * 类型码：输入 `1` 或 `L`，选择 `EFI System`。
2.  **创建根目录 `/` 分区：**
      * 输入 `n` (创建新分区)。
      * 分区号 `2`。
      * 起始扇区：默认。
      * 大小：默认（使用所有剩余空间）。
      * 类型码：输入 `20` 或 `L`，选择 `Linux filesystem`。
3.  **保存并退出：**
      * 输入 `w`。

### 5\. 格式化分区

```bash
# 格式化 /boot (ESP) 分区为 FAT32
mkfs.fat -F 32 /dev/nvme0n1p1

# 格式化根目录 / 分区为 Ext4
mkfs.ext4 /dev/nvme0n1p2
```

### 6\. 挂载文件系统并创建 Swapfile

```bash
# 挂载根目录
mount /dev/nvme0n1p2 /mnt 

# 创建 /boot 挂载点并挂载 ESP
mkdir /mnt/boot
mount /dev/nvme0n1p1 /mnt/boot

# 创建 64G swapfile
fallocate -l 64G /mnt/swapfile
chmod 600 /mnt/swapfile
mkswap /mnt/swapfile
```

## 阶段二：系统安装与 Chroot

### 7\. 安装基本系统、开发包和定制包

安装基础包、内核、固件，以及您要求的开发工具和 NVIDIA 驱动。

```bash
# 安装基础系统、内核、固件、SystemD 和文本编辑器
pacstrap /mnt base linux linux-firmware systemd vim 

# 安装核心编译/开发工具包 (base-devel) 和 git
pacstrap /mnt base-devel git 

# 安装 NVIDIA Open 驱动和工具
pacstrap /mnt nvidia-open nvidia-settings nvidia-utils

# 安装输入法框架
pacstrap /mnt fcitx5 fcitx5-chinese-addons
```

### 8\. 生成 fstab 文件

生成文件系统表，确保系统能识别分区和 **Swapfile**。

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

**重要：手动编辑 `/mnt/etc/fstab` 添加 Swapfile 配置**

```bash
nano /mnt/etc/fstab
```

在文件末尾添加一行，用于激活 Swapfile：

```
/swapfile none swap defaults 0 0
```

保存并退出。

### 9\. 进入新系统环境 (Chroot)

```bash
arch-chroot /mnt
```

## 阶段三：系统基本配置 (Configure the system)

### 10\. 时区、本地化设置

1.  **设置时区：**
    ```bash
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
    hwclock --systohc
    ```
2.  **本地化 (中文包，英文环境)：**
      * 编辑 `/etc/locale.gen`，取消以下两行注释：
        ```bash
        nano /etc/locale.gen
        # 取消注释：
        #en_US.UTF-8 UTF-8
        #zh_CN.UTF-8 UTF-8
        ```
      * 生成 locales：
        ```bash
        locale-gen
        ```
      * 设置系统环境为英文：
        ```bash
        echo "LANG=en_US.UTF-8" > /etc/locale.conf
        ```

### 11\. 主机名和网络管理

1.  **设置主机名 (`dev`)：**
    ```bash
    echo "dev" > /etc/hostname 
    ```
2.  **编辑 `/etc/hosts` 文件：**
    ```bash
    nano /etc/hosts
    # 添加以下内容：
    # 127.0.0.1	localhost
    # ::1		localhost
    # 127.0.1.1	dev.localdomain	dev
    ```
3.  **启用网络管理服务：**
    ```bash
    pacman -S networkmanager # 如果未随 base-devel 安装
    systemctl enable NetworkManager
    ```

### 11\. Root 密码和用户 (`syaofox`)

1.  **设置 root 密码：**
    ```bash
    passwd
    ```
2.  **创建用户 `syaofox` 并设置密码：**
    ```bash
    useradd -m -g users -G wheel syaofox
    passwd syaofox
    ```
3.  **配置 `sudo`：**
      * 运行 `visudo`。
      * 取消 `%wheel ALL=(ALL:ALL) ALL` 的注释，允许 `wheel` 组用户使用 `sudo`。

### 12\. 配置 NVIDIA Open 驱动加载

这是确保 NVIDIA 驱动正常工作的关键步骤。

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

### 13\. 安装和配置引导程序 - systemd-boot

1.  **安装 bootctl：**
    ```bash
    bootctl install
    ```
2.  **安装 CPU 微码：** (如果适用)
    ```bash
    pacman -S intel-ucode # 或 amd-ucode
    mkinitcpio -P # 再次生成 initramfs 以包含微码
    ```
3.  **创建引导条目 `/boot/loader/entries/arch.conf`：**
      * 获取根分区 UUID：`blkid /dev/nvme0n1p2` (记下 UUID)。
      * 创建文件：
        ```bash
        nano /boot/loader/entries/arch.conf
        ```
        填入以下内容（替换 `YOUR_ROOT_UUID`）：
        ```
        title   Arch Linux
        linux   /vmlinuz-linux
        initrd  /intel-ucode.img # 根据您的 CPU 替换为 amd-ucode.img
        initrd  /initramfs-linux.img
        options root=UUID=YOUR_ROOT_UUID rw
        ```
4.  **配置 loader.conf：**
    ```bash
    nano /boot/loader/loader.conf
    # 确保默认设置如下：
    # default arch
    # timeout 4
    # editor no
    ```

## 阶段四：收尾和重启

### 14\. 退出环境并卸载

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
    **⚠ 记得拔掉 USB 启动盘！**

## 阶段五：首次启动后的配置

系统重启后，您将进入命令行登录界面。使用用户名 `syaofox` 登录。

### 15\. 安装 Paru AUR 助手

我们使用 `syaofox` 用户来安装 `paru`，因为 AUR 助手不应该用 `root` 权限运行。

1.  **切换到用户家目录**：
    ```bash
    cd ~
    ```
2.  **克隆 `paru` 仓库**：
    ```bash
    git clone https://aur.archlinux.org/paru.git
    cd paru
    ```
3.  **编译并安装 `paru`**：(因为 `base-devel` 已安装，所以可以直接使用 `makepkg`)
    ```bash
    makepkg -si
    ```
4.  **清理**：
    ```bash
    cd ..
    rm -rf paru
    ```

### 16\. 使用 Paru 安装 Brave 浏览器

```bash
paru -S brave-bin
```

### 17\. Fcitx5 环境变量配置 (命令行环境提示)

Fcitx5 需要图形环境才能工作。如果您未来打算安装一个窗口管理器（如 i3/Sway），您需要在 `syaofox` 用户的配置文件中设置环境变量。

**编辑 `~/.bashrc` 或 `~/.profile`：**

```bash
nano ~/.bashrc
# 在文件末尾添加以下内容：
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export SDL_IM_MODULE=fcitx
```

保存后，运行 `source ~/.bashrc` 使其立即生效。

至此，您的 Arch Linux 开发者定制环境已安装完成。

