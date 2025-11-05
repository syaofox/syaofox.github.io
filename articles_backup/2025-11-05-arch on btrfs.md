---
title: "arch on btrfs"
created_at: "2025-11-05 13:07:32"
updated_at: "2025-11-05 13:07:32"
issue_number: 61
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/61
---

# arch on btrfs

## 💻 Arch Linux 安装补充教程（Btrfs & GRUB EFI）

### 📝 1. Btrfs 子卷规划与挂载点

在 Btrfs 文件系统上，为了方便快照和备份管理，建议使用以下子卷结构：

| 子卷名称 | 挂载点 | 作用 | 优化说明 |
| :--- | :--- | :--- | :--- |
| `@` | `/` | 根目录 | 建议排除快照不需要的目录（如 `/var/cache`, `/var/tmp` 等） |
| `@home` | `/home` | 用户主目录 | 独立快照，方便用户数据恢复 |
| `@cache` | `/var/cache` | 包管理器缓存 | **排除**在 `@` 根快照之外，减少快照大小 |
| `@log` | `/var/log` | 系统日志 | **排除**在 `@` 根快照之外，减少写操作和快照大小 |
| `@snapshots` | N/A | Timeshift 默认快照位置 | Timeshift 会自动创建和管理 |

**创建子卷示例（假设 Btrfs 根目录挂载在 `/mnt`）：**

```bash
btrfs subvolume create /mnt/@
btrfs subvolume create /mnt/@home
btrfs subvolume create /mnt/@cache
btrfs subvolume create /mnt/@log
```

-----

### 💾 2. `/etc/fstab` 优化配置

在生成或编辑 `/etc/fstab` 时，针对 Btrfs 子卷，建议添加以下优化选项：

```bash
# UUID=你的BTRFS分区UUID /               btrfs   subvol=@,defaults,noatime,compress=zstd 0 0
# UUID=你的BTRFS分区UUID /home           btrfs   subvol=@home,defaults,noatime,compress=zstd 0 0
# UUID=你的BTRFS分区UUID /var/cache      btrfs   subvol=@cache,defaults,noatime,compress=zstd 0 0
# UUID=你的BTRFS分区UUID /var/log        btrfs   subvol=@log,defaults,noatime,compress=zstd 0 0
# UUID=你的EFI分区UUID   /boot/efi       vfat    defaults,noatime 0 2
```

> ⚠️ **注意**：
>
>   * `noatime`: 避免更新文件访问时间，提升 **I/O 性能**。
>   * `ssd`: 针对 SSD 优化，开启 Btrfs 的 SSD 特性（如 TRIM）。
>   * `compress=zstd`: 开启文件透明压缩，建议使用 `zstd` (更快) 或 `lzo` (更稳定)。

-----

### 🚀 3. GRUB 与 EFI 引导配置

为了方便快照和备份（例如 Timeshift/Snapper），将 GRUB 的 `boot` 目录指向 `/boot`，而不是默认的 `/efi/grub`。

```bash
# 1. 移除旧的 GRUB 目录（如果存在且未正确配置）
# rm -rf /efi/grub/
# 假设 /boot/efi 已经挂载

# 2. 安装 GRUB 到 /boot 目录
grub-install --target=x86_64-efi --efi-directory=/boot/efi --boot-directory=/boot --bootloader-id=arch

# 3. 生成 GRUB 配置文件
grub-mkconfig -o /boot/grub/grub.cfg
```

#### 🛠️ **手动 EFI 引导项管理 (可选)**

使用 `efibootmgr` 查看、创建或排序 EFI 引导项。

1.  **查看现有引导菜单：**

    ```bash
    efibootmgr
    ```
2.  **创建新的引导项（如果不存在）：**

    ```bash
    # 假设 EFI 分区是 /dev/vda1 (p 1)，并使用 arch 作为 Bootloader ID
    efibootmgr -c -d /dev/vda -p 1 -L "Arch Linux" -l "\EFI\arch\grubx64.efi"
    ```
3.  **删除引导项（例如删除 001 号）：**

    ```bash
    efibootmgr -b 001 -B
    ```
4.  **排序引导项（设置启动顺序）：**

    ```bash
    # 设置启动顺序为 Arch Linux (002) -> Windows/其他 (001) -> ...
    efibootmgr -o 002,001,000
    ```

-----

### 📦 4. 额外软件包安装与系统基础配置

#### **基础 & 实用工具包**

```bash
# 核心系统工具和增强
sudo pacman -S intel-ucode bash-completion git grub-btrfs inotify-tools nfs-utils timeshift
# 额外的实用工具
sudo pacman -S htop man-db man-pages man-pages-zh_cn neovim plocate firefox rsync reflector
```

#### **优化镜像源（可选）**

使用 `reflector` 快速获取最新的国内镜像列表。

```bash
sudo reflector -c China -f 5 --sort rate --save /etc/pacman.d/mirrorlist
```

#### **`ll` 别名配置**

为了使用方便，为 `ls -lh --color=auto` 创建别名 `ll`。

```bash
echo 'alias ll="ls -lh --color=auto"' >> /etc/bash.bashrc
source /etc/bash.bashrc
```

-----

### ⏰ 5. Timeshift 快照备份 + GRUB 集成

本节目标是实现**快照自动备份**和**在 GRUB 菜单中选择快照启动**。

#### 1\. 安装所需工具（已在前面步骤安装）

```bash
# sudo pacman -S timeshift grub-btrfs inotify-tools
```

#### 2\. 安装 Timeshift 自动快照工具（AUR）

```bash
# 确保你已经完成了 Paru 的安装 (参见 12. 安装 Paru)
paru -S timeshift-autosnap
```

#### 3\. 配置 GRUB 快照支持

配置 `mkinitcpio.conf` 以便在快照启动时正确挂载 Btrfs。

  * 编辑 `/etc/mkinitcpio.conf`：
    ```bash
    sudo vim /etc/mkinitcpio.conf
    ```
  * 在 `HOOKS` 数组中，将 `grub-btrfs-overlayfs` 添加到 **`block` 之后**、**`filesystems` 之前**（如果使用 Timeshift/Snapper/grub-btrfs）：
    ```ini
    HOOKS=(base udev autodetect modconf block grub-btrfs-overlayfs filesystems keyboard fsck)
    ```
  * **重新生成 initramfs 镜像：**
    ```bash
    sudo mkinitcpio -P
    ```

#### 4\. 配置 `grub-btrfsd` 服务

修改 `grub-btrfsd` 服务文件，启用对 Timeshift 自动快照的支持。

  * 编辑服务文件：
    ```bash
    sudo systemctl edit --full grub-btrfsd
    ```
  * 找到并修改 `ExecStart` 行：
    ```ini
    ExecStart=/usr/bin/grub-btrfsd --syslog --timeshift-auto
    ```
  * 重新加载、启动并启用服务：
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start grub-btrfsd
    sudo systemctl enable grub-btrfsd
    ```

#### 5\. 最终生成 GRUB 配置

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

> **重启后，GRUB 菜单将显示 Timeshift 快照入口。**

-----

### 🌍 6. 中文环境配置

#### 1\. 启用语言环境

  * 编辑 `/etc/locale.gen`：
    ```bash
    vim /etc/locale.gen
    ```
  * 取消注释以下两行：
    ```
    en_US.UTF-8 UTF-8
    zh_CN.UTF-8 UTF-8
    ```
  * **生成语言环境：**
    ```bash
    locale-gen
    ```

#### 2\. 设置系统默认语言

  * 创建或编辑 `/etc/locale.conf`：
    ```bash
    sudo vim /etc/locale.conf
    ```
  * 添加以下配置（保留英文界面，但使用中文格式习惯）：
    ```ini
    LANG=en_US.UTF-8         # 系统主语言环境为英文
    LC_NUMERIC=zh_CN.UTF-8   # 数字格式为中文
    LC_TIME=zh_CN.UTF-8      # 时间/日期格式为中文
    LC_MONETARY=zh_CN.UTF-8  # 货币格式为中文
    LC_PAPER=zh_CN.UTF-8     # 纸张尺寸为中文
    LC_NAME=zh_CN.UTF-8
    LC_ADDRESS=zh_CN.UTF-8
    LC_TELEPHONE=zh_CN.UTF-8
    LC_MEASUREMENT=zh_CN.UTF-8 # 度量衡为中文
    ```

> 💡 **提示**: 如果希望桌面环境完全显示中文，将 `LANG` 也设置为 `zh_CN.UTF-8`。

#### 3\. 配置用户 Shell 立即生效（可选）

```bash
# 此命令通常用于测试和即时生效，如果已在 /etc/locale.conf 配置，重启后会生效。
source /etc/profile # 或者 source ~/.config/locale.conf 如果是用户级别的配置
```

-----

### 🔠 7. 中文字体安装

安装常用的中文字体以确保界面和文档显示正常。

```bash
sudo pacman -S adobe-source-han-sans-cn-fonts wqy-microhei noto-fonts-emoji ttf-roboto
# 刷新字体缓存
fc-cache -fv
```

-----

### 🗝️ 8. 密码管理（GNOME Keyring）

用于存储各种密码（如 Wi-Fi、浏览器、Git 等），常用于桌面环境。

```bash
sudo pacman -S gnome-keyring seahorse
```

  * **检查守护进程是否运行：**
    ```bash
    pgrep -a gnome-keyring
    ```

> 💡 **提示**：主流桌面环境（GNOME, Cinnamon, KDE 等）通常会自动启动 Keyring。对于轻量级环境 (如 i3wm, Openbox)，你可能需要将 `gnome-keyring-daemon` 或相关服务添加到你的启动脚本中。

-----

### 🎵 9. 多媒体工具

#### **看图**

```bash
sudo pacman -S xviewer xviewer-plugins
```

#### **播放器**

```bash
sudo pacman -S mpv vlc
```

#### **视频编辑 & 音频**

```bash
sudo pacman -S avidemux-qt openshot audacity
```

-----

### 📂 10. 文件管理器扩展 (Nemo 示例)

如果使用 Nemo 文件管理器（如 Cinnamon 桌面环境），可以安装以下扩展。

```bash
sudo pacman -S nemo-share nemo-fileroller nemo-media-columns
# 可选（AUR）
# paru -S folder-color-switcher nemo-emblems
```

-----

### ✨ 11. 安装 Paru（AUR 助手）

AUR 助手用于简化安装 Arch User Repository 中的软件包。

```bash
# 1. 更新系统并安装构建工具
sudo pacman -Syyu
sudo pacman -S --needed base-devel git

# 2. 克隆 Paru 仓库并构建
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si

# 3. 清理安装文件
cd ..
rm -rf paru
```

-----

### 🌐 12. NFS 挂载优化选项（`/etc/fstab` 示例）

在 `/etc/fstab` 中配置 NFS 网络文件系统挂载的优化选项。

**示例条目：**

```bash
10.10.10.2:/fs/1000/nfs  /mnt/dnas  nfs  rw,hard,intr,timeo=300,retrans=3,nosymfollow,noatime,nodiratime  0 0
```

| 选项 | 说明 | 推荐理由 |
| :--- | :--- | :--- |
| `rw` | 读写权限 | 默认选项，读写挂载 |
| `hard` | 无限重试 | 确保数据完整性，但配合 `intr` 可中断 |
| `intr` | 允许中断 | 允许用户使用 `Ctrl+C` 中断卡死的 I/O 操作 |
| `timeo=300` | 超时 30 秒 | 1/10 秒为单位（300 = 30 秒），优于默认的 60 秒 |
| `retrans=3` | 失败重试 3 次 | 减少不必要的重试次数 |
| `nosymfollow` | 本地解析符号链接 | **安全优化**，减轻服务器负担，避免某些跨挂载点的符号链接问题 |
| `noatime,nodiratime` | 提升 I/O 性能 | 避免更新文件/目录访问时间 |

-----


