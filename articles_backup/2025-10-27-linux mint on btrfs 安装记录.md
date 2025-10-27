---
title: "linux mint on btrfs 安装记录"
created_at: "2025-10-27 04:23:12"
updated_at: "2025-10-27 07:06:02"
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

## 必备包

```bash
sudo apt install build-essential python3-dev git
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

安装完成后，需要将 CUDA 路径添加到您的 shell 配置文件中（~/.bashrc 或 ~/.zshrc），以确 系统可以找到 nvcc 和库文件。
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
```

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



## 切换 CUDA 版本的两种方法 

### 方法一：通过符号链接 (Symbolic Link) 切换（推荐）

这是最常见和最推荐的方法，因为它允许您通过更改一个指向实际版本的软链接来全局切换系统环境。

#### 1\. 确认已安装多个版本

官方安装程序通常会将每个版本的 CUDA Toolkit 安装到各自独立的目录中，例如：

  * `/usr/local/cuda-11.8/`
  * `/usr/local/cuda-12.1/`
  * `/usr/local/cuda-13.0/` (如果您安装了)

并且，会创建一个名为 `/usr/local/cuda` 的符号链接，它指向当前“活动”的版本。

```bash
ls -l /usr/local/
# 查找类似 cuda-11.8, cuda-12.1, 以及 cuda -> cuda-xx.y 的链接
```

#### 2\. 切换操作

假设您想从 CUDA 11.8 切换到 CUDA 12.1：

1.  **删除现有符号链接：**

    ```bash
    sudo rm /usr/local/cuda
    ```

2.  **创建新的符号链接：**

    ```bash
    # 将 /usr/local/cuda 指向你希望使用的版本
    sudo ln -s /usr/local/cuda-12.1 /usr/local/cuda
    ```

3.  **验证切换：**

    ```bash
    nvcc --version
    # 输出应该显示 CUDA 12.1 的版本信息
    ```

#### 3\. 环境变量设置（前提）

要使此方法生效，您的环境变量（在您的 `~/.bashrc` 中）**必须** 指向通用路径 `/usr/local/cuda`：

```bash
export CUDA_HOME=/usr/local/cuda # 指向符号链接
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

如果已经按照我们之前的建议设置了这些变量，那么只需更改符号链接即可实现全局切换。

-----

### 方法二：通过修改环境变量切换（适用于临时或项目级切换）

如果您不想改变系统的默认 CUDA 版本，而只是想在 **当前终端会话** 或 **特定项目** 中使用特定版本，可以通过直接设置环境变量来实现。

#### 1\. 临时切换操作

假设您的系统默认是 CUDA 12.1，但您想在当前终端编译 DeepSpeed 时使用 **CUDA 11.8**：

```bash
# 在当前终端会话中，直接指向特定版本目录
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH

# 此时运行 nvcc --version 将显示 11.8
nvcc --version

# 接着运行您的 uv 安装命令
uv pip install deepspeed==0.17.1
```

#### 2\. 项目级切换 (虚拟环境脚本)

如果您使用 Python 虚拟环境 (`venv`)，可以修改虚拟环境的 `bin/activate` 脚本，在激活环境时自动设置这些变量。

  * 编辑：`your_venv/bin/activate`
  * 在文件末尾添加上述 `export` 语句，指向您项目需要的特定 CUDA 版本。

-----

### 总结与建议

| 切换方式 | 优点 | 缺点 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **符号链接 (`/usr/local/cuda`)** | **全局生效**，操作简单，所有依赖 `/usr/local/cuda` 的程序都会切换。 | 需要 `sudo` 权限，会改变系统默认版本。 | 大部分时间只使用一个 CUDA 版本，且需要全局统一。 |
| **环境变量 (`export`)** | 无需 `sudo`，只影响当前 Shell 或项目，**隔离性好**。 | 每次打开新终端都需要重新设置。 | 需要在不同项目中使用不同 CUDA 版本，或进行临时测试。 |





