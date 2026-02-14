#!/bin/bash

# 配置 Linux Mint 22.2 Btrfs 子卷和交换文件的脚本
# 在 Live Session 环境中运行，需先完成 Linux Mint 安装和分区

# 退出脚本如果有未处理的错误
set -e

# 检查是否为 root 用户
if [ "$(id -u)" != "0" ]; then
    echo "错误：请以 root 权限运行此脚本（使用 sudo）。"
    exit 1
fi

# 检查是否在 UEFI 模式
if [ -d /sys/firmware/efi ]; then
    echo "检测到 UEFI 模式，将获取 EFI 分区 UUID。"
else
    echo "检测到 BIOS 模式，无需 EFI 分区，确保 GRUB 安装到磁盘。"
fi

# 提示用户输入 Btrfs 分区设备
echo "列出块设备以帮助识别 Btrfs 分区："
lsblk -f
echo "请输入 Btrfs 分区（例如 /dev/nvme0n1p2）："
read BTRFS_DEV

# 验证分区是否存在且为 Btrfs
if ! lsblk -f "$BTRFS_DEV" | grep -q btrfs; then
    echo "错误：$BTRFS_DEV 不是 Btrfs 分区或不存在。"
    exit 1
fi

# 获取 Btrfs UUID
BTRFS_UUID=$(lsblk -no UUID "$BTRFS_DEV")
if [ -z "$BTRFS_UUID" ]; then
    echo "错误：无法获取 $BTRFS_DEV 的 UUID。"
    exit 1
fi
echo "您的 Btrfs UUID: $BTRFS_UUID"

# 获取 EFI 分区 UUID（如果存在）
EFI_UUID=""
if [ -d /sys/firmware/efi ]; then
    echo "请输入 EFI 分区（例如 /dev/nvme0n1p1）："
    read EFI_DEV
    if ! lsblk -f "$EFI_DEV" | grep -q vfat; then
        echo "错误：$EFI_DEV 不是 FAT32 分区或不存在。"
        exit 1
    fi
    EFI_UUID=$(lsblk -no UUID "$EFI_DEV")
    if [ -z "$EFI_UUID" ]; then
        echo "错误：无法获取 $EFI_DEV 的 UUID。"
        exit 1
    fi
    echo "您的 EFI 分区 UUID: $EFI_UUID"
fi

# 提示用户输入交换文件大小
echo "请输入交换文件大小（例如 8G，建议：内存 ≤8GB 设为内存+2GB，>8GB 设为 4-8GB）："
read SWAP_SIZE
if ! [[ "$SWAP_SIZE" =~ ^[0-9]+[GM]$ ]]; then
    echo "错误：交换文件大小格式无效（例如 8G）。"
    exit 1
fi

# 确保 /mnt 存在并卸载所有挂载点
cd ~
umount -R /mnt 2>/dev/null || true
mkdir -p /mnt

# 挂载 Btrfs 顶层
mount "$BTRFS_DEV" /mnt

# 检查现有子卷并警告
if btrfs subvolume list /mnt | grep -q .; then
    echo "检测到现有子卷："
    btrfs subvolume list /mnt
    read -p "继续可能覆盖现有子卷（y/N）？" confirm
    if [ "$confirm" != "y" ]; then
        umount /mnt
        echo "脚本已退出。"
        exit 1
    fi
fi

# 检查并创建 @ 和 @home 子卷（如果不存在）
if ! btrfs subvolume list /mnt | grep -q "[0-9]\+ @$" ; then
    echo "未找到 @ 子卷，正在创建..."
    btrfs subvolume create /mnt/@
    # 迁移根目录数据到 @ 子卷
    mkdir -p /mnt_temp
    mount -o subvolid=5 "$BTRFS_DEV" /mnt_temp
    if [ "$(ls -A /mnt_temp)" ]; then
        mv /mnt_temp/* /mnt/@/ || true
    fi
    umount /mnt_temp
    rmdir /mnt_temp
fi

if ! btrfs subvolume list /mnt | grep -q "[0-9]\+ @home$" ; then
    echo "未找到 @home 子卷，正在创建..."
    btrfs subvolume create /mnt/@home
fi

# 创建其他子卷
btrfs subvolume create /mnt/@swap
btrfs subvolume create /mnt/@cache
btrfs subvolume create /mnt/@log
echo "已创建/确认子卷：@, @home, @swap, @cache, @log"
btrfs subvolume list /mnt

# 卸载顶层挂载点
umount /mnt

# 挂载 @ 子卷（已安装系统）
mount -o subvol=@ "$BTRFS_DEV" /mnt || { echo "挂载 @ 子卷失败"; exit 1; }

# 创建临时挂载点并挂载 @log 和 @cache 子卷
mkdir -p /mnt_log /mnt_cache
mount -o subvol=@log "$BTRFS_DEV" /mnt_log || { echo "挂载 @log 子卷失败"; exit 1; }
mount -o subvol=@cache "$BTRFS_DEV" /mnt_cache || { echo "挂载 @cache 子卷失败"; exit 1; }

# 迁移 /var/log 和 /var/cache 数据
if [ -d /mnt/var/log ]; then
    if [ -L /mnt/var/log ]; then
        echo "错误：/mnt/var/log 是符号链接，请手动检查。"
        exit 1
    fi
    if [ "$(ls -A /mnt/var/log)" ]; then
        mv /mnt/var/log/* /mnt_log/ || true
        rmdir /mnt/var/log || echo "警告：/mnt/var/log 非空，请检查。"
    fi
fi

if [ -d /mnt/var/cache ]; then
    if [ -L /mnt/var/cache ]; then
        echo "错误：/mnt/var/cache 是符号链接，请手动检查。"
        exit 1
    fi
    if [ "$(ls -A /mnt/var/cache)" ]; then
        mv /mnt/var/cache/* /mnt_cache/ || true
        rmdir /mnt/var/cache || echo "警告：/mnt/var/cache 非空，请检查。"
    fi
fi

# 卸载临时挂载点
umount /mnt_log
umount /mnt_cache
rm -rf /mnt_log /mnt_cache

# 创建永久挂载点目录
mkdir -p /mnt/{var/log,var/cache,swap,home}
mount -o subvol=@home "$BTRFS_DEV" /mnt/home 2>/dev/null || true
mount -o subvol=@log "$BTRFS_DEV" /mnt/var/log || { echo "挂载 @log 子卷失败"; exit 1; }
mount -o subvol=@cache "$BTRFS_DEV" /mnt/var/cache || { echo "挂载 @cache 子卷失败"; exit 1; }
mount -o subvol=@swap "$BTRFS_DEV" /mnt/swap || { echo "挂载 @swap 子卷失败"; exit 1; }

# 创建并初始化交换文件
if ! btrfs filesystem mkswapfile --help >/dev/null 2>&1; then
    echo "mkswapfile 不可用，使用 dd 和 mkswap 创建交换文件。"
    truncate -s 0 /mnt/swap/swapfile
    chattr +C /mnt/swap/swapfile
    dd if=/dev/zero of=/mnt/swap/swapfile bs=1M count="${SWAP_SIZE%G}"000
    chmod 0600 /mnt/swap/swapfile
    mkswap /mnt/swap/swapfile
else
    btrfs filesystem mkswapfile --size "$SWAP_SIZE" /mnt/swap/swapfile
    chmod 0600 /mnt/swap/swapfile
fi

# 启用并验证交换文件
swapon /mnt/swap/swapfile
echo "交换文件状态："
swapon --show

# 备份 fstab
cp /mnt/etc/fstab /mnt/etc/fstab.bak
echo "已备份 /mnt/etc/fstab 到 /mnt/etc/fstab.bak"

# 更新 fstab
cat << EOF > /mnt/etc/fstab
# / (Root Subvolume)
UUID=$BTRFS_UUID /               btrfs   subvol=@,defaults,relatime,compress=zstd 0 0

# /boot/efi
$( [ -n "$EFI_UUID" ] && echo "UUID=$EFI_UUID  /boot/efi       vfat    umask=0077      0 1" )

# /home (Home Subvolume)
UUID=$BTRFS_UUID /home           btrfs   subvol=@home,defaults,relatime,compress=zstd 0 0

# /var/log Subvolume
UUID=$BTRFS_UUID /var/log        btrfs   subvol=@log,defaults,relatime,compress=zstd 0 0

# /var/cache Subvolume
UUID=$BTRFS_UUID /var/cache      btrfs   subvol=@cache,defaults,relatime,compress=zstd 0 0

# /swap Subvolume
UUID=$BTRFS_UUID /swap           btrfs   subvol=@swap,defaults,noatime,compress=no 0 0

# Swap File
/swap/swapfile none swap defaults 0 0
EOF

# 验证 fstab 挂载
mount -a || { echo "fstab 挂载测试失败，请检查 /mnt/etc/fstab"; exit 1; }
echo "fstab 挂载测试通过"

# 配置 Timeshift 排除
# mkdir -p /mnt/etc/timeshift
# cat << EOF > /mnt/etc/timeshift/timeshift.json
# {
#     "exclude": [
#         "/var/log/**",
#         "/var/cache/**",
#         "/swap/**"
#     ]
# }
# EOF
# echo "已配置 Timeshift 排除 /var/log, /var/cache, /swap"

# 卸载所有挂载点
cd ~
umount -R /mnt

echo "配置完成！请运行 'reboot' 重启系统。"
echo "重启后，运行 'free -h' 验证交换文件，检查 Timeshift GUI 确认排除设置。"