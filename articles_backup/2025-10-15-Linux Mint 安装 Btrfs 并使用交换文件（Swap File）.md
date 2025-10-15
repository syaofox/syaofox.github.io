---
title: "Linux Mint 安装 Btrfs 并使用交换文件（Swap File）"
created_at: "2025-10-15 09:11:49"
updated_at: "2025-10-15 09:11:49"
issue_number: 26
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/26
---

# Linux Mint 安装 Btrfs 并使用交换文件（Swap File）

在 Btrfs 上使用交换文件（Swap File）是推荐的做法，尤其如果你想使用 **Timeshift** 等工具进行快照。因为 **Btrfs 的限制是包含活动交换文件的子卷不能创建快照**。

Linux Mint 22.2 的安装程序本身不提供 Btrfs 子卷的配置选项，所以我们需要进行**手动分区**，并在安装完成后**手动创建和配置交换文件**。

以下是详细的安装和配置流程：

- - -

## **第一部分：安装前的准备和分区**

### **1\. 启动 Live Session**

1.  将 **Linux Mint 22.2** 安装介质（U盘或光盘）插入电脑。
    
2.  从安装介质启动，进入 **Linux Mint Live** 环境。
    

### **2\. 使用 GParted 分区**

打开 **GParted**（分区编辑器），在你的目标硬盘上创建必要的分区。假设你的硬盘是 `/dev/sda`。

| 分区类型 | 大小（建议） | 文件系统 | 挂载点（用于安装程序） | 作用 |
| :--- | :--- | :--- | :--- | :--- |
| **EFI System Partition (ESP)** | 512MB ~ 1GB | FAT32 | /boot/efi | UEFI 启动所需 |
| **Btrfs Root/Data** | 剩下的所有空间 | btrfs | / | 整个 Linux Mint 系统和数据 |

导出到 Google 表格

**步骤：**

1.  **创建 GPT 分区表**（如果是新盘）。
    
2.  **创建 EFI 分区**：
    
    *   大小：512MB - 1GB
        
    *   文件系统：**fat32**
        
    *   设置 Flags：**boot** 和 **esp**。
        
3.  **创建 Btrfs 分区**：
    
    *   大小：剩余所有空间
        
    *   文件系统：**btrfs**
        

- - -

## **第二部分：运行 Linux Mint 安装程序**

### **3\. 选择安装类型**

1.  运行桌面上的 **Install Linux Mint** 图标。
    
2.  在“安装类型”步骤，选择 **Something else**（其他选项）。
    

### **4\. 配置分区挂载点**

1.  找到你刚才创建的 **FAT32** 分区，双击或选择 **Change**：
    
    *   **Use as:** EFI System Partition
        
    *   **Mount point:** `/boot/efi`
        
2.  找到你刚才创建的 **Btrfs** 分区，双击或选择 **Change**：
    
    *   **Use as:** Btrfs journaling filesystem
        
    *   **Mount point:** **`/`** (根目录)
        
    *   **不要选择** "Format the partition"（格式化分区）**以外的任何选项**（通常默认会选中 Format，保持即可，确保是干净的 Btrfs 文件系统）。
        
3.  继续安装过程（选择用户、密码、时区等）。
    

- - -

## **第三部分：创建 Btrfs 子卷和交换文件**

安装程序完成后，**不要立即重启**。选择 **Continue Testing**（继续测试），然后打开**终端**。

### **5\. 挂载 Btrfs 分区并创建子卷**

假设你的 Btrfs 分区是 `/dev/sda2` (请用 `lsblk` 确认实际设备名)。


```bash
# 1. 确认 Btrfs 分区并挂载到临时目录 /mnt
sudo mount /dev/sda2 /mnt

# 2. 检查默认的根子卷 ID（通常是5）并卸载
# 安装程序会自动创建一些默认子卷（如 @ 或类似），我们需要为快照和交换文件进行调整

# 3. 创建新的子卷（@ 约定用于根文件系统，@home 用于用户数据，@swap 用于交换文件）
# 这一步是为了Timeshift快照做准备，它可以排除不需要快照的子卷。
sudo btrfs subvolume create /mnt/@
sudo btrfs subvolume create /mnt/@home
sudo btrfs subvolume create /mnt/@swap

# 4. 将安装程序安装的内容移动到新的 @ 子卷中
# 假设安装程序将文件放在了根目录，现在需要移动到 @
sudo mv /mnt/{bin,boot,etc,lib,lib64,mnt,opt,proc,root,run,sbin,srv,sys,usr,var} /mnt/@
# 移动用户目录内容
sudo mv /mnt/home/* /mnt/@home/
# 清理临时挂载点下的 home 目录
sudo rm -rf /mnt/home

# 5. 卸载临时挂载点
sudo umount /mnt
```

### **6\. 重新挂载新创建的子卷**

我们需要将新子卷挂载到正确的位置，以便进行交换文件配置。


```bash
# 1. 重新挂载根子卷
sudo mount -o subvol=@ /dev/sda2 /mnt

# 2. 创建其他挂载点
sudo mkdir -p /mnt/{home,swap}

# 3. 挂载 @home 和 @swap 子卷
sudo mount -o subvol=@home /dev/sda2 /mnt/home
sudo mount -o subvol=@swap /dev/sda2 /mnt/swap
```

### **7\. 创建 Btrfs 交换文件**

**Btrfs 交换文件必须满足两个关键条件：**

1.  位于一个**独立的子卷**（我们已经创建了 `@swap`）。
    
2.  **禁用 COW** (Copy-on-Write) 属性。
    

我们使用 `btrfs filesystem mkswapfile` 命令创建，它会自动处理 NODATACOW 和预分配等问题，这是最安全的方法。

**确定交换文件大小**：通常建议至少等于你的物理内存大小，或者如果你需要休眠（Hibernation），则要大于内存。这里以 **8G** 为例。


```bash
# 1. 在 @swap 子卷中创建并初始化交换文件
# --size 参数指定大小，例如 8G (8 Gigabytes)
sudo btrfs filesystem mkswapfile --size 8G /mnt/swap/swapfile

# 2. 启用交换文件
sudo swapon /mnt/swap/swapfile

# 3. 验证交换文件是否启用
sudo swapon --show
# 如果看到 /mnt/swap/swapfile，则表示成功
```

### **8\. 更新 fstab**

你需要更新 `/mnt/etc/fstab` 文件，确保系统在启动时能正确挂载子卷和启用交换文件。

首先获取 Btrfs 分区的 **UUID**：

```bash
lsblk -no UUID /dev/sda2
# 复制输出结果 (例如：a1b2c3d4-e5f6-7890-1234-567890abcdef)
```

然后编辑 `/mnt/etc/fstab` 文件：

```bash
sudo nano /mnt/etc/fstab
```

在文件末尾添加或修改为以下内容（请将 `YOUR_BTRFS_UUID` 替换为你实际的 UUID）：

代码段

```
# / (Root Subvolume)
UUID=YOUR_BTRFS_UUID /               btrfs   subvol=@,defaults,noatime,compress=zstd 0 0

# /home (Home Subvolume)
UUID=YOUR_BTRFS_UUID /home           btrfs   subvol=@home,defaults,noatime,compress=zstd 0 0

# /swap (Swap Subvolume) - 必须先挂载它才能激活交换文件
UUID=YOUR_BTRFS_UUID /swap           btrfs   subvol=@swap,defaults,noatime 0 0

# Swap File
/swap/swapfile none swap defaults 0 0

# /boot/efi (EFI Partition) - UUID请使用你的EFI分区UUID
# UUID=EFI_UUID /boot/efi   vfat    umask=0077 0 1
```

> **注意：**
> 
> *   `compress=zstd` 是 Btrfs 的一个推荐选项，可以提高性能并节省空间。
>     
> *   `/swap` 子卷的挂载选项中**不要**包含 `compress` 或 `nodatacow`（因为 `mkswapfile` 已经处理了文件级别的 `NODATACOW`，而且这个子卷本身不建议启用压缩）。
>     
> *   交换文件的 fstab 条目是 `/swap/swapfile none swap defaults 0 0`。
>     

### **9\. 卸载分区并重启**

完成所有配置后，执行：


```bash
# 卸载所有挂载点
sudo umount -R /mnt

# 检查是否全部卸载
ls /mnt 
# 如果为空，则可以继续

# 重启
reboot
```

系统重启后，进入 Linux Mint。打开终端，运行 `free -h` 应该可以看到你设置的交换文件大小。


```bash
free -h
# 应该会显示 Swap 行有大小和使用量
```

至此，Linux Mint 22.2 在 Btrfs 上使用独立子卷中的交换文件的安装和配置已完成。

