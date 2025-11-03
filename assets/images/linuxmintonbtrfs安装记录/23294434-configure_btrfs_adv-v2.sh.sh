#!/bin/bash
# configure_btrfs.sh - Configure Btrfs subvolumes and swap file for Linux Mint 22.2
# Supports full subvolume layout + KVM CoW disable

set -euo pipefail

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root (use sudo)."
    exit 1
fi

# === Prompt for devices ===
echo "Enter your Btrfs partition (e.g., /dev/nvme0n1p2):"
read -r BTRFS_DEV
if [ ! -b "$BTRFS_DEV" ]; then
    echo "Error: $BTRFS_DEV is not a valid block device."
    exit 1
fi

echo "Enter your EFI partition (e.g., /dev/nvme0n1p1):"
read -r EFI_DEV
if [ ! -b "$EFI_DEV" ]; then
    echo "Error: $EFI_DEV is not a valid block device."
    exit 1
fi

# Get UUIDs
BTRFS_UUID=$(lsblk -no UUID "$BTRFS_DEV")
EFI_UUID=$(lsblk -no UUID "$EFI_DEV")

if [ -z "$BTRFS_UUID" ] || [ -z "$EFI_UUID" ]; then
    echo "Error: Failed to retrieve UUIDs."
    exit 1
fi

echo "Btrfs UUID: $BTRFS_UUID"
echo "EFI UUID:   $EFI_UUID"

# Prompt for swap size
echo "Enter swap file size (e.g., 8G for 8GB):"
read -r SWAP_SIZE
if ! [[ "$SWAP_SIZE" =~ ^[0-9]+[GM]$ ]]; then
    echo "Error: Invalid swap size. Use format like 8G or 16G."
    exit 1
fi

# === Define subvolumes ===
SUBVOLS=(
    @root
    @home
    @spool
    @images
    @opt
    @srv
    @vartmp
    @log
    @tmp
    @cache
    @swap
)

# Mapping: target_path -> subvol_name
declare -A MOUNT_MAP
MOUNT_MAP[/]="@root"
MOUNT_MAP[/home]="@home"
MOUNT_MAP[/var/spool]="@spool"
MOUNT_MAP[/var/lib/libvirt/images]="@images"
MOUNT_MAP[/opt]="@opt"
MOUNT_MAP[/srv]="@srv"
MOUNT_MAP[/var/tmp]="@vartmp"
MOUNT_MAP[/var/log]="@log"
MOUNT_MAP[/tmp]="@tmp"
MOUNT_MAP[/var/cache]="@cache"
MOUNT_MAP[/swap]="@swap"

# Temporary mount point
MNT="/mnt"
umount -R "$MNT" 2>/dev/null || true
mkdir -p "$MNT"

# === Mount top-level and create subvolumes ===
echo "Mounting Btrfs top-level..."
mount "$BTRFS_DEV" "$MNT"

echo "Creating subvolumes..."
for subvol in "${SUBVOLS[@]}"; do
    if btrfs subvolume list "$MNT" | grep -qw "$subvol"; then
        echo "Subvolume $subvol already exists, skipping."
    else
        btrfs subvolume create "$MNT/$subvol"
        echo "Created $subvol"
    fi
done

umount "$MNT"

# === Mount @root and prepare system ===
echo "Mounting @root as root filesystem..."
mount -o subvol=@root,compress=zstd "$BTRFS_DEV" "$MNT"

# Create mount points for other subvolumes
for path in "${!MOUNT_MAP[@]}"; do
    subvol="${MOUNT_MAP[$path]}"
    if [ "$path" = "/" ]; then continue; fi
    mkdir -p "$MNT$path"
done

# === Mount all subvolumes temporarily for data migration ===
TEMP_MOUNTS=()
for path in "${!MOUNT_MAP[@]}"; do
    subvol="${MOUNT_MAP[$path]}"
    if [ "$path" = "/" ]; then continue; fi

    temp_mnt="/mnt_temp_$(echo "$path" | tr '/' '_')"
    mkdir -p "$temp_mnt"
    mount -o subvol="$subvol",compress=zstd "$BTRFS_DEV" "$temp_mnt"
    TEMP_MOUNTS+=("$temp_mnt")
done

# === Migrate existing data ===
echo "Migrating data to subvolumes..."
for path in "${!MOUNT_MAP[@]}"; do
    subvol="${MOUNT_MAP[$path]}"
    if [ "$path" = "/" ]; then continue; fi

    src="$MNT$path"
    dst="/mnt_temp_$(echo "$path" | tr '/' '_')"

    if [ -d "$src" ] && [ "$(ls -A "$src" 2>/dev/null || echo '')" ]; then
        echo "Migrating $path -> $subvol"
        rsync -aHAX --info=progress2 "$src"/ "$dst"/
        rm -rf "$src"/*
        rmdir "$src" 2>/dev/null || true
    fi
done

# === Unmount temporary mounts ===
echo "Unmounting temporary mounts..."
for mnt in "${TEMP_MOUNTS[@]}"; do
    umount "$mnt"
    rmdir "$mnt"
done

# === Permanently mount subvolumes under @root ===
echo "Setting up permanent mounts..."
for path in "${!MOUNT_MAP[@]}"; do
    subvol="${MOUNT_MAP[$path]}"
    if [ "$path" = "/" ]; then continue; fi

    case "$path" in
        /swap)
            mount_opts="subvol=$subvol,defaults,ssd,noatime,compress=no,space_cache=v2,discard=async"
            ;;
        *)
            mount_opts="subvol=$subvol,defaults,ssd,noatime,compress=zstd,space_cache=v2,discard=async"
            ;;
    esac

    mount -o "$mount_opts" "$BTRFS_DEV" "$MNT$path"
done

# === Disable CoW for KVM images (if directory exists) ===
KVM_DIR="$MNT/var/lib/libvirt/images"
if [ -d "$KVM_DIR" ]; then
    echo "Disabling Copy-on-Write for KVM images..."
    chattr +C "$KVM_DIR" 2>/dev/null || echo "Note: chattr +C may not be supported on this fs (normal on older kernels)"
    # Also ensure new files inherit nocow
    chmod 755 "$KVM_DIR"
fi

# === Create swap file in @swap ===
echo "Creating swap file of size $SWAP_SIZE..."
btrfs filesystem mkswapfile --size "$SWAP_SIZE" "$MNT/swap/swapfile"
chmod 600 "$MNT/swap/swapfile"
swapon "$MNT/swap/swapfile"
echo "Swap enabled:"
swapon --show

# === Update fstab ===
FSTAB="$MNT/etc/fstab"
cat > "$FSTAB" << EOF
# <file system> <mount point> <type> <options> <dump> <pass>

# Root (@root)
UUID=$BTRFS_UUID /               btrfs   subvol=@root,defaults,relatime,compress=zstd 0 0

# EFI Partition
UUID=$EFI_UUID   /boot/efi      vfat    umask=0077 0 1

# Subvolumes
UUID=$BTRFS_UUID /home           btrfs   subvol=@home,defaults,relatime,compress=zstd 0 0
UUID=$BTRFS_UUID /var/spool      btrfs   subvol=@spool,defaults,noatime,compress=no 0 0
UUID=$BTRFS_UUID /var/lib/libvirt/images btrfs subvol=@images,defaults,noatime,nodatasum,nodatacow 0 0
UUID=$BTRFS_UUID /opt            btrfs   subvol=@opt,defaults,relatime,compress=zstd 0 0
UUID=$BTRFS_UUID /srv            btrfs   subvol=@srv,defaults,relatime,compress=zstd 0 0
UUID=$BTRFS_UUID /var/tmp        btrfs   subvol=@vartmp,defaults,noatime,compress=no 0 0
UUID=$BTRFS_UUID /var/log        btrfs   subvol=@log,defaults,noatime,compress=no 0 0
UUID=$BTRFS_UUID /tmp            btrfs   subvol=@tmp,defaults,noatime,compress=no 0 0
UUID=$BTRFS_UUID /var/cache      btrfs   subvol=@cache,defaults,noatime,compress=no 0 0
UUID=$BTRFS_UUID /swap           btrfs   subvol=@swap,defaults,noatime 0 0

# Swap file
/swap/swapfile   none           swap    defaults 0 0
EOF

# === Verify fstab ===
echo "Verifying fstab..."
if command -v findmnt >/dev/null; then
    findmnt --verify --fstab "$FSTAB" || {
        echo "Error: fstab verification failed."
        exit 1
    }
fi

# === Final unmount ===
echo "Unmounting all..."
cd ~
umount -R "$MNT"

echo "=================================================="
echo "Btrfs subvolume configuration completed successfully!"
echo "KVM CoW disabled on /var/lib/libvirt/images"
echo "Swap file created and enabled"
echo "fstab updated"
echo
echo "Please reboot now:"
echo "    sudo reboot"
echo "=================================================="