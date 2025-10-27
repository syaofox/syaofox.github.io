---
title: "linux mint on btrfs 安装记录"
created_at: "2025-10-27 04:23:12"
updated_at: "2025-10-27 04:23:12"
issue_number: 51
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/51
---

# linux mint on btrfs 安装记录

## 运行 Linux Mint 安装程序

分区设置

- 选择 Something else（手动分区）。

配置挂载点：

- EFI 分区：选择 FAT32 分区，设置为 EFI System Partition，挂载点 /boot/efi，无需格式化（若已有数据）。
- Btrfs 分区：选择 Btrfs 分区，设置为 Btrfs journaling file system，勾选 Format，挂载点 /。

*确认“引导加载程序安装设备”为目标磁盘（例如 /dev/nvme0n1）。*

完成安装

- 设置用户名、密码、时区等。
- 点击 Install Now，等待安装完成。
- 选择 Continue Testing（不要重启），以进行子卷和交换文件配置。

## 配置 Btrfs 子卷和交换文件

下载自动化脚本 [configure_btrfs_adv.sh](https://raw.githubusercontent.com/syaofox/dotfiles/refs/heads/master/linuxmint-on-btrfs/configure_btrfs_adv.sh)

```bash
chmod +x configure_btrfs.sh
sudo ./configure_btrfs.sh
```

## CUDA Toolkit

访问 [CNVIDIA CUDA Toolkit Archive(https://developer.nvidia.com/cuda-toolkit-archive), 在浏览器中打开 NVIDIA CUDA Toolkit Archive 页面。

选择正确的版本： 找到您需要的版本（例如 CUDA Toolkit 12.1 Update 1）。

>推荐版本：CUDA 12.1 或 11.8
>CUDA 12.1：这是 PyTorch 2.x 系列中较新的稳定版本通常推荐的版本。如果您的项目使用较新的 PyTorch，这是一个极好的选择。
>CUDA 11.8：这是一个非常成熟和稳定的版本，兼容很多旧版本的 PyTorch 和 TensorFlow。

选择系统配置： 进入该版本的页面，选择您的操作系统配置：

- Operating System (操作系统): Linux
- Architecture (架构): x86_64
- Version (版本): 例如：Ubuntu (根据您的 Linux 发行版选择)
- Installer Type (安装类型): deb (local) 或 runfile（推荐使用 deb (local) 或 runfile，因为它们提供了完整的安装命令）。
- 执行安装命令： 页面会给出下载文件和执行安装的一系列命令。您需要按顺序在终端中运行它们。


设置环境变量 (至关重要)

安装完成后，需要将 CUDA 路径添加到您的 shell 配置文件中（~/.bashrc 或 ~/.zshrc），以确保 DeepSpeed 和系统可以找到 nvcc 和库文件。
确定安装目录： 官方安装通常会将文件放在 /usr/local/cuda-XX.Y，并创建一个指向该版本的符号链接 /usr/local/cuda。

编辑配置文件： 打开 ~/.bashrc：

```bash
nano ~/.bashrc  
```

在文件末尾添加以下行：

```bash
# ========= CUDA Environment Variables =========
# 假设使用符号链接 /usr/local/cuda
export CUDA_HOME=/usr/local/cuda 
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
# ==============================================
```bash

*（注意：如果您的安装路径不是 /usr/local/cuda，请替换为您安装的特定版本路径，例如 /usr/local/cuda-12.1。）**

使更改生效：

```bash
source ~/.bashrc
```

验证 nvcc： 确保编译器现在可用：

```bash
nvcc --version
```

如果成功，应该看到安装的特定 CUDA 版本的编译器信息。




