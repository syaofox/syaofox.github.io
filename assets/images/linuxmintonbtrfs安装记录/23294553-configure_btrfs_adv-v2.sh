#!/usr/bin/env bash
# configure_btrfs.sh - Btrfs subvolume layout + swap + SSD-optimized mount options
# Author: ChatGPT (2025-11-02)
# Usage: sudo ./configure_btrfs.sh

set -euo pipefail
IFS=$'\n\t'

# ------------------- 颜色输出 -------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()  { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ------------------- 基础常量 -------------------
MNT="/mnt"
TEMP_ROOT="${MNT}_temp"
SWAPFILE="/swap/swapfile"

# 统一的挂载选项（SSD 专用）
BASE_OPTS="defaults,ssd,noatime,space_cache=v2,discard=async"
COMPRESS_OPTS="${BASE_OPTS},compress=zstd"
NOCOMPRESS_OPTS="${BASE_OPTS},compress=no"

# ------------------- 子卷定义 -------------------
declare -A SUBVOLS
# path => subvol_name : extra_mount_opts
SUBVOLS[/]="@root:${COMPRESS_OPTS}"
SUBVOLS[/home]="@home:${COMPRESS_OPTS}"
SUBVOLS[/var/spool]="@spool:${NOCOMPRESS_OPTS}"
SUBVOLS[/var/lib/libvirt/images]="@images:${NOCOMPRESS_OPTS},nodatasum,nodatacow"
SUBVOLS[/opt]="@opt:${COMPRESS_OPTS}"
SUBVOLS[/srv]="@srv:${COMPRESS_OPTS}"
SUBVOLS[/var/tmp]="@vartmp:${NOCOMPRESS_OPTS}"
SUBVOLS[/var/log]="@log:${NOCOMPRESS_OPTS}"
SUBVOLS[/tmp]="@tmp:${NOCOMPRESS_OPTS}"
SUBVOLS[/var/cache]="@cache:${NOCOMPRESS_OPTS}"
SUBVOLS[/swap]="@swap:${NOCOMPRESS_OPTS}"

# ------------------- 权限检查 -------------------
if [[ $EUID -ne 0 ]]; then
    err "Please run as root (sudo)."
    exit 1
fi

# ------------------- 输入设备 -------------------
read_device() {
    local prompt=$1; local var=$2
    while true; do
        echo -n "$prompt: "
        read -r "$var" || return 1
        if [[ -b "${!var}" ]]; then
            return 0
        fi
        warn "${!var} is not a valid block device."
    done
}

info "=== 输入分区 ==="
read_device "Btrfs partition (e.g. /dev/nvme0n1p2)" BTRFS_DEV
read_device "EFI partition   (e.g. /dev/nvme0n1p1)" EFI_DEV

BTRFS_UUID=$(lsblk -no UUID "$BTRFS_DEV")
EFI_UUID=$(lsblk -no UUID "$EFI_DEV")
[[ -n $BTRFS_UUID && -n $EFI_UUID ]] || { err "Failed to get UUIDs"; exit 1; }

info "Btrfs UUID: $BTRFS_UUID"
info "EFI   UUID: $EFI_UUID"

# ------------------- Swap 大小 -------------------
while true; do
    echo -n "Swap file size (e.g. 8G, 16G): "
    read -r SWAP_SIZE
    if [[ $SWAP_SIZE =~ ^[0-9]+[GM]$ ]]; then break; fi
    warn "Invalid format, use e.g. 8G"
done

# ------------------- 辅助函数 -------------------
cleanup() {
    set +e
    info "Cleaning up temporary mounts..."
    for m in "$TEMP_ROOT" "${!TEMP_MOUNTS[@]}" ; do
        umount "$m" 2>/dev/null || true
        rmdir "$m" 2>/dev/null || true
    done
    umount -R "$MNT" 2>/dev/null || true
    rmdir "$MNT" 2>/dev/null || true
}
trap cleanup EXIT

mount_top() { mount -o subvol=/ "$BTRFS_DEV" "$MNT"; }
umount_top() { umount "$MNT"; }

# ------------------- 创建子卷 -------------------
info "=== 创建子卷 ==="
mount_top

for path in "${!SUBVOLS[@]}"; do
    subvol="${SUBVOLS[$path]%%:*}"
    if btrfs subvolume list "$MNT" | grep -qw "$subvol"; then
        info "Subvolume $subvol 已存在，跳过"
    else
        btrfs subvolume create "$MNT/$subvol" && info "Created $subvol"
    fi
done
umount_top

# ------------------- 挂载 @root -------------------
info "=== 挂载 @root 并准备目录结构 ==="
mkdir -p "$MNT"
mount -o "subvol=@root,${SUBVOLS[/]#*:}" "$BTRFS_DEV" "$MNT"

for path in "${!SUBVOLS[@]}"; do
    [[ $path == "/" ]] && continue
    mkdir -p "${MNT}${path}"
done

# ------------------- 迁移数据（临时挂载） -------------------
declare -A TEMP_MOUNTS
info "=== 迁移已有数据 ==="
for path in "${!SUBVOLS[@]}"; do
    [[ $path == "/" ]] && continue
    subvol="${SUBVOLS[$path]%%:*}"
    tmp_mnt="${TEMP_ROOT}_$(echo "$path" | tr '/' '_')"
    mkdir -p "$tmp_mnt"
    mount -o "subvol=$subvol,${SUBVOLS[$path]#*:}" "$BTRFS_DEV" "$tmp_mnt"
    TEMP_MOUNTS[$path]="$tmp_mnt"
done

for path in "${!SUBVOLS[@]}"; do
    [[ $path == "/" ]] && continue
    src="${MNT}${path}"
    dst="${TEMP_MOUNTS[$path]}"
    if [[ -d $src ]] && ls -A "$src" >/dev/null 2>&1; then
        info "Migrating $path → $subvol"
        # 使用 pv 显示进度（若未安装则降级为 rsync）
        if command -v pv >/dev/null; then
            rsync -aHAX --info=progress2 "$src"/ "$dst"/ | pv -l -s $(find "$src" | wc -l) >/dev/null || true
        else
            rsync -aHAX --info=progress2 "$src"/ "$dst"/
        fi
        rm -rf "${src:?}"/*
        rmdir "$src" 2>/dev/null || true
    fi
done

# ------------------- 正式挂载子卷 -------------------
info "=== 正式挂载所有子卷 ==="
for path in "${!SUBVOLS[@]}"; do
    [[ $path == "/" ]] && continue
    subvol="${SUBVOLS[$path]%%:*}"
    opts="${SUBVOLS[$path]#*:}"
    mount -o "subvol=$subvol,$opts" "$BTRFS_DEV" "${MNT}${path}"
done

# ------------------- KVM NoCoW -------------------
KVM_DIR="${MNT}/var/lib/libvirt/images"
if [[ -d $KVM_DIR ]]; then
    info "Disabling CoW for KVM images..."
    chattr +C "$KVM_DIR" 2>/dev/null || warn "chattr +C not supported (old kernel)"
    chmod 755 "$KVM_DIR"
fi

# ------------------- 创建 Swap -------------------
info "=== 创建 $SWAP_SIZE Swap 文件 ==="
mkdir -p "${MNT}/swap"
btrfs filesystem mkswapfile --size "$SWAP_SIZE" "${MNT}${SWAPFILE}" >/dev/null
chmod 600 "${MNT}${SWAPFILE}"
swapon "${MNT}${SWAPFILE}"
info "Swap 已启用："
swapon --show

# ------------------- 写 fstab -------------------
FSTAB="${MNT}/etc/fstab"
info "=== 写入 /etc/fstab ==="
{
    echo "# <file system> <mount point> <type> <options> <dump> <pass>"
    echo ""
    echo "# EFI"
    echo "UUID=$EFI_UUID   /boot/efi   vfat   umask=0077   0  1"
    echo ""
    echo "# Btrfs subvolumes"
    for path in "${!SUBVOLS[@]}"; do
        subvol="${SUBVOLS[$path]%%:*}"
        opts="${SUBVOLS[$path]#*:}"
        # 把逗号换成空格，fstab 不接受逗号分隔的选项
        opts_fstab=$(echo "$opts" | tr ',' ' ')
        printf "UUID=%s %-15s btrfs subvol=%s,%s 0 0\n" \
               "$BTRFS_UUID" "$path" "$subvol" "$opts_fstab"
    done
    echo ""
    echo "# Swap file"
    echo "$SWAPFILE   none   swap   defaults   0 0"
} > "$FSTAB"

# ------------------- 验证 fstab -------------------
if command -v findmnt >/dev/null; then
    info "Verifying fstab..."
    findmnt --verify --fstab "$FSTAB" || { err "fstab verification failed"; exit 1; }
else
    warn "findmnt not available, skipping verification."
fi

# ------------------- 完成 -------------------
info "=================================================="
info "Btrfs 配置完成！"
info "   • 子卷已创建并挂载"
info "   • KVM 目录已禁用 CoW"
info "   • Swap 文件已启用"
info "   • /etc/fstab 已更新"
info "请现在重启系统："
echo "    sudo reboot"
info "=================================================="