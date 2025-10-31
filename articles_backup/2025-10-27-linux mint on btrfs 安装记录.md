---
title: "linux mint on btrfs 安装记录"
created_at: "2025-10-27 04:23:12"
updated_at: "2025-10-31 08:26:33"
issue_number: 51
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/51
---

# linux mint on btrfs 安装记录

## 运行 Linux Mint 安装程序

**分区设置**

- 选择 Something else（手动分区）。

**配置挂载点：**

- EFI 分区：选择 FAT32 分区，设置为 EFI System Partition，挂载点 /boot/efi，无需格式化（若已有数据）。
- Btrfs 分区：选择 Btrfs 分区，设置为 Btrfs journaling file system，勾选 Format，挂载点 /。

*确认“引导加载程序安装设备”为目标磁盘（例如 /dev/nvme0n1）。*

**完成安装**

- 设置用户名、密码、时区等。
- 点击 Install Now，等待安装完成。
- 选择 Continue Testing（不要重启），以进行子卷和交换文件配置。

## 配置 Btrfs 子卷和交换文件

下载自动化脚本 [configure_btrfs_adv.sh](https://raw.githubusercontent.com/syaofox/dotfiles/refs/heads/master/linuxmint-on-btrfs/configure_btrfs_adv.sh)

```bash
chmod +x configure_btrfs.sh
sudo ./configure_btrfs.sh
```
## 字体

[Google Inter](https://fonts.google.com/?query=inter)


## 升级fcixt5

安装依赖

```bash
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-frontend-gtk3 fcitx5-frontend-gtk4 fcitx5-frontend-qt5  fcitx5-rime
```

皮肤:[fcitx skins collection](https://github.com/winjeg/fcitx-skinsl)

打开【系统设置】【输入法】，输入法框架选择fcitx5，然后注销用户重新登录或重启电脑。



## 挂载nas上的文件(nfs)

依赖
```bash
sudo apt update && sudo apt install nfs-common
sudo mkdir -p /mnt/dnas
```

编辑`/etc/fstab`加入挂载信息

```bash
10.10.10.2:/fs/1000/nfs /mnt/dnas nfs _netdev,auto 0 0
```
测试

```bash
sudo mount -a
```

## rofi

安装

```bash
sudo apt install rofi
```
获取配置文件

```bash
cd
git clone https://github.com/syaofox/.dotfiles
```
或者直接下载 [.dotfiles.zip](https://github.com/user-attachments/files/23160884/default.dotfiles.zip) 解压到home目录


创建电源菜单软连接

```bash
# 1. 定义源文件路径 (集中管理的位置)
SOURCE_FILE="$HOME/.dotfiles/rofi/rofi-power-menu.desktop"

# 2. 定义目标链接路径 (系统查找 .desktop 文件的地方)
LINK_PATH="$HOME/.local/share/applications/rofi-power-menu.desktop"

# 3. 创建软链接
ln -s "$SOURCE_FILE" "$LINK_PATH"

# 4. 更新桌面文件数据库
update-desktop-database "$HOME/.local/share/applications/"
````

绑定快捷键命令

```bash
bash -c "rofi -show drun -config $HOME/.dotfiles/rofi/rofi.rasi"
```

如果要绑定 win + space ,必须先关闭系统占用
位置在 keybord -> layouts -> options -> Switching to another layout



## 恢复密码

[Seahorse + SSH + GitHub PAT 全量导出/导入教程](https://syaofox.github.io/articles/tips/2025-10-30-SeahorseSSHGitHubPAT%E5%85%A8%E9%87%8F%E5%AF%BC%E5%87%BA%E5%AF%BC%E5%85%A5%E6%95%99%E7%A8%8B.html)


## 必备软件

* **brave**：去广告浏览器 [地址](https://brave.com/linux/)
* **FreeFileSync**：免费开源的文件同步和备份软件，支持Windows、macOS和Linux，用于比较和同步本地、网络驱动器、移动设备或云存储上的文件夹。 [地址](https://freefilesync.org/)
* **Czkawka**：免费开源的多功能文件清理工具，用于查找和删除重复文件、临时文件、大文件等，帮助释放磁盘空间，支持快速扫描和GUI/CLI模式。 [地址](https://github.com/qarmin/czkawka)
* **FSearch**：基于GTK3的快速文件搜索工具，适用于Unix-like系统。 [地址](https://github.com/cboxdoerfer/fsearch/wiki/Search-syntax)
* **Clapgrep**：开源Linux应用，用于搜索文本文件、PDF和Office文档，提供快速搜索并显示相关元数据如页码和行号。 [地址](https://github.com/luleyleo/clapgrep)
* **KRename**：强大的批量文件重命名工具，支持基于表达式重命名、复制/移动文件，并处理数百个文件。 [地址](https://apps.kde.org/krename/)
* **LocalSend**：免费开源的跨平台应用，用于在本地网络中点对点分享文件，支持端到端加密，类似于AirDrop。 [地址](https://localsend.org/)
* **Gear Lever**：开源工具，用于轻松管理AppImage应用，支持安装、更新、组织AppImage文件并生成桌面入口。 [地址](https://github.com/mijorus/gearlever)
* **FileZilla**：免费FTP解决方案，支持FTP、FTPS和SFTP，用于远程文件传输，跨平台可用。 [地址](https://filezilla-project.org/)
* **Pinta**：免费开源的绘图和图像编辑程序，结合直观工具和强大功能，类似于简易版Paint.NET。 [地址](https://www.pinta-project.com/)
* **XnConvert**：快速强大的跨平台批量图像转换器，支持自动化编辑照片集合，包括调整大小、水印和滤镜。 [地址](https://www.xnview.com/en/xnconvert/)
* **HandBrake**：开源视频转码工具，支持从几乎任何格式转换为现代编解码器，适用于DVD和数字视频文件。 [地址](https://handbrake.fr/)
* **lazydocker** : 一个在终端中运行的 UI 工具，用于管理 Docker 和 Docker Compose。它通过提供简洁的界面和键盘快捷键，让用户不必记住复杂的命令行，就能轻松完成容器、镜像、网络和卷的查看、启动、停止、重启、删除等操作。 [地址](https://github.com/jesseduffield/lazydocker)
* **Video-downloader** : 下载视频,yt-dlp套皮 [地址](https://github.com/Unrud/video-downloader)
*  **xfce4-clipman**: 剪贴板管理,绑定快捷键 win+v  xfce4-clipman-history
* **bottles**: 跑windows程序 [地址](https://usebottles.com/)
* **btop**:现代且多彩的命令行资源监视器，显示使用情况和统计数据 [地址](https://usebottles.com/)
* **gpik**:屏幕取色器 [地址](http://www.gpick.org/)
* **diodon**:Cinnamon 桌面无缝集成，支持无限历史（通过 Zeitgeist）、同步主剪贴板和 Ctrl+C/V、Ubuntu 风格指示器。支持文本和图片。

## nemo插件

* **Nemo Mediainfo Tab**：显示媒体分辨率等信息。 [地址](https://github.com/linux-man/nemo-mediainfo-tab/releases)

* **Copy  Path To Clipborad**：复制文件路径

* **Move into a new folder**：将选定的文件、文件夹和其他项目移动到新目录中

自定义的一些插件 [nemo_actions.zip](https://github.com/user-attachments/files/23159130/nemo_actions.zip)

安装位置:`/home/syaofox/.local/share/nemo`,包括:
- 批量压缩为ZIP文件
- 复制完整路径到剪贴板
- 合并视频音频为mp4
- 拼接MP4视频
- 从剪贴板粘贴图像到文件(PNG)
- 刷新

依赖

```bash
sudo apt update
sudo apt install zip xclip ffmpeg xdotool tree
```

## applets

- **Simplified System Monitor** 显示温度占用

## extensions

- **Workspace Scroller** 鼠标滚动切换工作区


## 快捷键绑定

导出工具:
```bash
sudo apt install dconf-cli
```
常用操作
```bash
# 备份快捷键到文本文件（仅自定义）
dconf dump /org/cinnamon/desktop/keybindings/ > ~/cinnamon-shortcuts.conf

# 恢复/导入
dconf load /org/cinnamon/desktop/keybindings/ < ~/cinnamon-shortcuts.conf

# 重置所有到默认
dconf reset -f /org/cinnamon/desktop/keybindings/

# 查看自定义绑定
dconf dump /org/cinnamon/desktop/keybindings/custom-keybindings/
```
附件
[cinnamon-shortcuts.conf.tar.gz](https://github.com/user-attachments/files/23254812/cinnamon-shortcuts.conf.tar.gz)


## 开发环境

**git***
参考其他文章

**python 环境**

```bash
sudo apt install build-essential python3-dev python3-pip git
```
**uv包管理器**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**修改缓存位置**

```bash
# 查看当前位置
uv cache dir
```
`~/.bashrc`最后添加

```bash
export UV_CACHE_DIR="/path/to/new/uv_cache"
```
加载生效

```bash
source ~/.bashrc
```

*新位置要位于安装uv的同一个分区下*

**清理缓存**

uv 提供了几种不同的机制来移除缓存中的条目：

`uv cache clean` 会删除缓存目录中的 所有 缓存条目，彻底清空缓存。
`uv cache clean ruff` 会删除 ruff 包的所有缓存条目，适用于使特定包或有限集合的包缓存失效。
`uv cache prune` 会删除所有 未使用 的缓存条目。例如，缓存目录可能包含以前版本的 uv 创建的条目，这些条目不再需要并且可以安全移除。`uv cache prune` 可以定期运行，用于保持缓存目录的清洁。


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

1\. 确认已安装多个版本

官方安装程序通常会将每个版本的 CUDA Toolkit 安装到各自独立的目录中，例如：

  * `/usr/local/cuda-11.8/`
  * `/usr/local/cuda-12.1/`
  * `/usr/local/cuda-13.0/` (如果您安装了)

并且，会创建一个名为 `/usr/local/cuda` 的符号链接，它指向当前“活动”的版本。

```bash
ls -l /usr/local/
# 查找类似 cuda-11.8, cuda-12.1, 以及 cuda -> cuda-xx.y 的链接
```

 2\. 切换操作

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

3\. 环境变量设置（前提）

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

1\. 临时切换操作

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

2\. 项目级切换 (虚拟环境脚本)

如果您使用 Python 虚拟环境 (`venv`)，可以修改虚拟环境的 `bin/activate` 脚本，在激活环境时自动设置这些变量。

  * 编辑：`your_venv/bin/activate`
  * 在文件末尾添加上述 `export` 语句，指向您项目需要的特定 CUDA 版本。

-----

总结与建议

| 切换方式 | 优点 | 缺点 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **符号链接 (`/usr/local/cuda`)** | **全局生效**，操作简单，所有依赖 `/usr/local/cuda` 的程序都会切换。 | 需要 `sudo` 权限，会改变系统默认版本。 | 大部分时间只使用一个 CUDA 版本，且需要全局统一。 |
| **环境变量 (`export`)** | 无需 `sudo`，只影响当前 Shell 或项目，**隔离性好**。 | 每次打开新终端都需要重新设置。 | 需要在不同项目中使用不同 CUDA 版本，或进行临时测试。 |





