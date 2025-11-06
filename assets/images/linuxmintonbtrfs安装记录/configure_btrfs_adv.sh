#!/bin/bash
# configure_btrfs.sh - Configure Btrfs subvolumes and swap file for Linux Mint 22.2

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root (use sudo)."
    exit 1
fi

# Prompt for Btrfs partition
echo "Enter your Btrfs partition (e.g., /dev/nvme0n1p2):"
read BTRFS_DEV
if [ ! -b "$BTRFS_DEV" ]; then
    echo "Error: $BTRFS_DEV is not a valid block device."
    exit 1
fi

# Prompt for EFI partition
echo "Enter your EFI partition (e.g., /dev/nvme0n1p1):"
read EFI_DEV
if [ ! -b "$EFI_DEV" ]; then
    echo "Error: $EFI_DEV is not a valid block device."
    exit 1
fi

# Get Btrfs UUID
BTRFS_UUID=$(lsblk -no UUID "$BTRFS_DEV")
if [ -z "$BTRFS_UUID" ]; then
    echo "Error: Failed to get UUID for $BTRFS_DEV."
    exit 1
fi
echo "Btrfs UUID: $BTRFS_UUID"

# Get EFI UUID
EFI_UUID=$(lsblk -no UUID "$EFI_DEV")
if [ -z "$EFI_UUID" ]; then
    echo "Error: Failed to get UUID for $EFI_DEV."
    exit 1
fi
echo "EFI UUID: $EFI_UUID"

# Prompt for swap file size
echo "Enter swap file size (e.g., 8G for 8GB):"
read SWAP_SIZE
if ! [[ "$SWAP_SIZE" =~ ^[0-9]+[GM]$ ]]; then
    echo "Error: Invalid swap size format. Use format like 8G."
    exit 1
fi

# Unmount any existing mounts
umount -R /mnt 2>/dev/null
mkdir -p /mnt

# Mount Btrfs top-level
mount "$BTRFS_DEV" /mnt || { echo "Error: Failed to mount $BTRFS_DEV."; exit 1; }

# Create subvolumes with dynamic check
SUBVOLS=(@swap @cache @log @tmp)
for subvol in "${SUBVOLS[@]}"; do
    if btrfs subvolume list /mnt | grep -q "$subvol"; then
        echo "Subvolume $subvol already exists, skipping."
    else
        btrfs subvolume create "/mnt/$subvol" || { echo "Error: Failed to create $subvol."; exit 1; }
    fi
done

# Unmount top-level
umount /mnt

# Mount @ subvolume and migrate data
mount -o subvol=@ "$BTRFS_DEV" /mnt || { echo "Error: Failed to mount @ subvolume."; exit 1; }
mkdir -p /mnt_log /mnt_cache /mnt_tmp
mount -o subvol=@log "$BTRFS_DEV" /mnt_log || { echo "Error: Failed to mount @log."; exit 1; }
mount -o subvol=@cache "$BTRFS_DEV" /mnt_cache || { echo "Error: Failed to mount @cache."; exit 1; }
mount -o subvol=@tmp "$BTRFS_DEV" /mnt_tmp || { echo "Error: Failed to mount @tmp."; exit 1; }

# Migrate /var/log, /var/cache, /tmp
for dir in log cache tmp; do
    src="/mnt/var/$dir"
    dst="/mnt_$dir"
    if [ "$dir" = "tmp" ]; then
        src="/mnt/$dir"
    fi
    if [ -d "$src" ] && [ "$(ls -A "$src")" ]; then
        mv "$src"/* "$dst"/ || { echo "Error: Failed to migrate /$dir."; exit 1; }
        rmdir "$src"
    fi
done

# Unmount temporary mounts
umount /mnt_log /mnt_cache /mnt_tmp
rm -rf /mnt_log /mnt_cache /mnt_tmp

# Create permanent mount points and mount subvolumes
mkdir -p /mnt/{var/log,var/cache,tmp,swap,home}
mount -o subvol=@home "$BTRFS_DEV" /mnt/home 2>/dev/null
mount -o subvol=@log "$BTRFS_DEV" /mnt/var/log || { echo "Error: Failed to mount @log."; exit 1; }
mount -o subvol=@cache "$BTRFS_DEV" /mnt/var/cache || { echo "Error: Failed to mount @cache."; exit 1; }
mount -o subvol=@tmp "$BTRFS_DEV" /mnt/tmp || { echo "Error: Failed to mount @tmp."; exit 1; }
mount -o subvol=@swap "$BTRFS_DEV" /mnt/swap || { echo "Error: Failed to mount @swap."; exit 1; }

# Create and enable swap file
btrfs filesystem mkswapfile --size "$SWAP_SIZE" /mnt/swap/swapfile || { echo "Error: Failed to create swapfile."; exit 1; }
chmod 600 /mnt/swap/swapfile
swapon /mnt/swap/swapfile || { echo "Error: Failed to enable swapfile."; exit 1; }
swapon --show

# Update fstab
FSTAB=/mnt/etc/fstab
cat > "$FSTAB" << EOF
# / (Root Subvolume)
UUID=$BTRFS_UUID /               btrfs   subvol=@,defaults,relatime,compress=zstd 0 0
# /boot/efi
UUID=$EFI_UUID  /boot/efi       vfat    umask=0077      0 1
# /home
UUID=$BTRFS_UUID /home           btrfs   subvol=@home,defaults,relatime,compress=zstd 0 0
# /var/log
UUID=$BTRFS_UUID /var/log        btrfs   subvol=@log,defaults,noatime,compress=no 0 0
# /var/cache
UUID=$BTRFS_UUID /var/cache      btrfs   subvol=@cache,defaults,noatime,compress=no 0 0
# /tmp
UUID=$BTRFS_UUID /tmp            btrfs   subvol=@tmp,defaults,noatime,compress=no 0 0
# /swap
UUID=$BTRFS_UUID /swap           btrfs   subvol=@swap,defaults,noatime,compress=no 0 0
# Swap File
/swap/swapfile none swap defaults 0 0
EOF

# Verify fstab
findmnt --verify --fstab "$FSTAB" || { echo "Error: fstab verification failed."; exit 1; }

# Unmount all
cd ~
umount -R /mnt

echo "Configuration complete! Reboot now: sudo reboot"