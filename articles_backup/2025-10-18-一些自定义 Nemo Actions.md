---
title: "一些自定义 Nemo Actions"
created_at: "2025-10-18 09:06:52"
updated_at: "2025-10-18 09:06:52"
issue_number: 36
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/36
---

# 一些自定义 Nemo Actions

# Nemo Actions 使用说明

## 简介

Nemo Actions 是 Cinnamon 桌面环境的文件管理器 Nemo 的扩展功能，允许用户通过右键菜单快速执行自定义操作。这里提供5个 Nemo Actions 实用的文件管理功能：

| 功能 | 用途 | 主要依赖 |
|------|------|----------|
| 批量压缩为ZIP | 文件夹批量打包 | zip |
| 复制完整路径 | 快速获取文件路径 | xclip |
| 合并视频音频 | 视频音频流合并 | ffmpeg |
| 拼接MP4视频 | 多视频顺序拼接 | ffmpeg |
| 刷新 | 强制刷新视图 | xdotool |

下载：[nemo_actions.zip](https://github.com/user-attachments/files/22983335/nemo_actions.zip)

### 安装位置

- **Actions 配置文件**：`~/.local/share/nemo/actions/`
- **执行脚本**：`~/.local/share/nemo/scripts/`

这些文件已经安装在正确的位置，重启Nemo(`nemo -q`)，Nemo 会自动加载并在右键菜单中显示相应的选项。

---

## 功能列表

本工具集包含以下5个功能：

1. **批量压缩为ZIP文件** - 将多个文件夹分别压缩为独立的 ZIP 文件
2. **复制完整路径到剪贴板** - 快速复制文件或文件夹的绝对路径
3. **合并视频音频为MP4** - 将独立的视频流和音频流合并为 MP4 文件
4. **拼接MP4视频** - 将多个 MP4 视频文件按顺序拼接成一个文件
5. **刷新** - 快速刷新 Nemo 文件管理器视图

---

## 1. 批量压缩为ZIP文件

### 功能描述

将选中的每个文件夹分别压缩为独立的 `.zip` 文件，压缩文件与源文件夹同名，保存在同一目录下。

### 使用场景

- 需要分享或备份多个项目文件夹
- 批量打包多个目录以节省磁盘空间
- 准备邮件附件或上传到云存储

### 使用步骤

1. 在 Nemo 文件管理器中，选择一个或多个文件夹
2. 右键点击选中的文件夹
3. 在右键菜单中选择 **"批量压缩为ZIP文件"** (Compress to individual ZIP files)
4. 终端窗口会打开并显示压缩进度
5. 压缩完成后，每个文件夹旁边会生成对应的 `.zip` 文件

### 示例

```
原始文件夹：
  /home/user/Documents/Project1/
  /home/user/Documents/Project2/

压缩后生成：
  /home/user/Documents/Project1.zip
  /home/user/Documents/Project2.zip
```

### 技术细节

- **脚本位置**：`~/.local/share/nemo/scripts/compress_folders_to_zip.sh`
- **压缩方式**：使用 `zip -r -q` 命令递归压缩
- **权限检查**：自动检查读取和写入权限
- **错误处理**：跳过无法访问的文件夹并继续处理其他文件夹

### 依赖项

- `zip` - ZIP 压缩工具
- `bash` - Shell 解释器
- `realpath` - 获取绝对路径（通常已预装）

### 注意事项

- 仅对文件夹生效，选中的文件会被忽略
- 如果同名 `.zip` 文件已存在，会被覆盖
- 压缩过程在终端窗口中显示，完成后可手动关闭

---

## 2. 复制完整路径到剪贴板

### 功能描述

将选中的文件或文件夹的完整绝对路径复制到系统剪贴板，方便在命令行或其他应用中使用。

### 使用场景

- 在终端中快速导航到某个目录
- 在配置文件中填写文件路径
- 与他人分享文件的准确位置
- 在代码中引用文件路径

### 使用步骤

1. 在 Nemo 文件管理器中，选择单个文件或文件夹
2. 右键点击选中的项目
3. 在右键菜单中选择 **"复制完整路径到剪贴板"** (Copy Path to Clipboard)
4. 路径已复制，可以直接粘贴使用（Ctrl+V）

### 示例

```
选中文件：/home/user/Documents/report.pdf
复制后剪贴板内容：/home/user/Documents/report.pdf

可直接在终端中使用：
$ cd /home/user/Documents/
$ cat /home/user/Documents/report.pdf
```

### 技术细节

- **命令**：`echo -n "%F" | xclip -selection clipboard`
- **剪贴板**：使用系统剪贴板（clipboard selection）
- **无换行符**：`echo -n` 确保不添加额外的换行符

### 依赖项

- `xclip` - X11 剪贴板工具
- `bash` - Shell 解释器

### 注意事项

- 仅支持单个文件或文件夹选择（多选时不显示此选项）
- 适用于所有文件类型和扩展名
- 复制的是绝对路径，不是相对路径

---

## 3. 合并视频音频为MP4

### 功能描述

将独立的视频文件和音频文件合并为一个 MP4 视频文件。脚本会自动检测编码格式，如果已经是 H.264/AAC 格式则直接复制流（速度快），否则自动转码。

### 使用场景

- 某些录屏或下载工具生成的视频和音频是分离的
- 需要为静音视频添加音轨
- 为视频替换音频轨道
- 处理 B站下载的分离视频和音频

### 使用步骤

1. 在 Nemo 文件管理器中，**按顺序选择2个文件**：
   - **第一个**：提供视频流的文件
   - **第二个**：提供音频流的文件
2. 右键点击
3. 选择 **"合并视频音频为mp4"** (Merge video audio to mp4)
4. 终端窗口打开，显示处理进度和编码信息
5. 完成后，在第一个文件的同一目录下生成 `[原文件名]_merge.mp4`

### 示例

```
选中文件：
  1. video.m4v （包含 H.264 视频流）
  2. audio.m4a （包含 AAC 音频流）

输出文件：
  video_merge.mp4
```

### 技术细节

- **脚本位置**：`~/.local/share/nemo/scripts/merge-h264acc.sh`
- **自动检测**：使用 `ffprobe` 检测视频和音频编码格式
- **智能处理**：
  - H.264 视频 → 直接复制（`-c:v copy`）
  - 非 H.264 视频 → 转码为 H.264（`-c:v libx264 -crf 23`）
  - AAC 音频 → 直接复制（`-c:a copy`）
  - 非 AAC 音频 → 转码为 AAC（`-c:a aac -b:a 128k`）
- **优化参数**：添加 `-movflags +faststart` 支持边下载边播放

### 依赖项

- `ffmpeg` - 视频处理工具
- `ffprobe` - 媒体信息检测工具（通常随 ffmpeg 安装）
- `bash` - Shell 解释器

### 注意事项

- **必须选择恰好2个文件**，否则会报错
- 文件选择顺序很重要：第一个提供视频，第二个提供音频
- 如果输出文件已存在会被覆盖
- 支持的输入格式：所有 ffmpeg 支持的视频和音频格式
- 转码质量：CRF 23（平衡质量和文件大小）

---

## 4. 拼接MP4视频

### 功能描述

将多个 MP4 或 QuickTime 视频文件按选择顺序拼接成一个完整的视频文件。

### 使用场景

- 合并分段录制的视频
- 将课程的多个章节合并为完整版
- 拼接行车记录仪的多个视频片段
- 合并多个短视频为长视频

### 使用步骤

1. 在 Nemo 文件管理器中，按需要的顺序选择多个 MP4 文件（至少2个）
   - **提示**：按 Ctrl 键依次点击文件可以控制顺序
2. 右键点击
3. 选择 **"拼接MP4视频"** (Merge MP4 videos)
4. 终端窗口打开，显示拼接进度
5. 完成后，在第一个文件的同一目录下生成 `merged_video.mp4`

### 示例

```
选中文件（按顺序）：
  1. part1.mp4
  2. part2.mp4
  3. part3.mp4

输出文件：
  merged_video.mp4
```

### 技术细节

- **脚本位置**：`~/.local/share/nemo/scripts/merge-videos.sh`
- **拼接方法**：使用 ffmpeg 的 concat demuxer（`-f concat`）
- **编码方式**：流复制模式（`-c copy`），无需重新编码，速度快
- **临时文件**：创建临时文件列表，处理完成后自动清理

### 依赖项

- `ffmpeg` - 视频处理工具
- `bash` - Shell 解释器
- `realpath` - 获取绝对路径（通常已预装）

### 注意事项

- **至少需要选择2个文件**
- 支持的格式：MP4 和 QuickTime (MOV)
- 为获得最佳效果，建议所有视频具有相同的：
  - 分辨率（宽度和高度）
  - 编码格式（视频和音频编解码器）
  - 帧率
- 如果视频参数不一致，可能出现黑屏、音画不同步等问题
- 输出文件名固定为 `merged_video.mp4`，如果已存在会被覆盖

---

## 5. 刷新

### 功能描述

快速刷新 Nemo 文件管理器的当前视图，相当于按下 `Ctrl+R` 快捷键。

### 使用场景

- 外部程序修改了文件，需要更新显示
- 删除或移动文件后视图未更新
- 挂载新设备后需要刷新
- 任何需要重新加载当前目录内容的情况

### 使用步骤

1. 在 Nemo 文件管理器的任意位置右键点击（无需选择文件）
2. 选择 **"Refresh"** 或 **"Tazele"**（土耳其语）
3. 视图立即刷新

### 技术细节

- **实现方式**：使用 `xdotool` 模拟键盘输入 `Ctrl+R`
- **无需选择**：可在空白区域直接使用

### 依赖项

- `xdotool` - X11 自动化工具

### 注意事项

- 不需要选择任何文件或文件夹
- 适用于任何文件类型和扩展名
- 某些情况下，Nemo 会自动刷新，此功能用于强制刷新

---

## 依赖安装指南

所有功能都需要一些外部工具支持。以下是完整的依赖安装指南：

### 在 Ubuntu/Debian/Linux Mint 上安装

```bash
# 安装所有依赖（推荐）
sudo apt update
sudo apt install zip xclip ffmpeg xdotool

# 或者按需安装：

# 压缩功能
sudo apt install zip

# 剪贴板功能
sudo apt install xclip

# 视频处理功能
sudo apt install ffmpeg

# 刷新功能
sudo apt install xdotool
```

### 在 Fedora/RHEL/CentOS 上安装

```bash
# 安装所有依赖
sudo dnf install zip xclip ffmpeg xdotool

# FFmpeg 可能需要启用 RPM Fusion 仓库
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install ffmpeg
```

### 在 Arch Linux 上安装

```bash
# 安装所有依赖
sudo pacman -S zip xclip ffmpeg xdotool
```

### 验证安装

安装完成后，可以使用以下命令验证：

```bash
# 检查 zip
zip --version

# 检查 xclip
xclip -version

# 检查 ffmpeg
ffmpeg -version

# 检查 xdotool
xdotool --version
```

---

## 常见问题与故障排除

### Q1: 右键菜单中没有显示这些选项？

**解决方法**：
1. 确认文件位置正确：
   ```bash
   ls ~/.local/share/nemo/actions/
   ls ~/.local/share/nemo/scripts/
   ```
2. 检查脚本是否有执行权限：
   ```bash
   chmod +x ~/.local/share/nemo/scripts/*.sh
   ```
3. 重启 Nemo：
   ```bash
   nemo -q
   nemo &
   ```

### Q2: 点击菜单后没有反应或报错？

**解决方法**：
1. 检查是否安装了必要的依赖（参见上方安装指南）
2. 在终端中手动运行脚本查看错误信息：
   ```bash
   bash ~/.local/share/nemo/scripts/[脚本名称].sh [测试文件路径]
   ```

### Q3: 复制路径功能不工作？

**解决方法**：
1. 确认已安装 xclip：
   ```bash
   sudo apt install xclip
   ```
2. 确认 X11 会话正常运行（Wayland 可能需要额外配置）

### Q4: 如何卸载这些 Actions？

```bash
# 删除 action 配置文件
rm ~/.local/share/nemo/actions/compress-folders-to-zip.nemo_action
rm ~/.local/share/nemo/actions/copy_path_to_clipboard.nemo_action
rm ~/.local/share/nemo/actions/merge-h264acc.nemo_action
rm ~/.local/share/nemo/actions/merge-mp4-videos.nemo_action
rm ~/.local/share/nemo/actions/refresh.nemo_action

# 删除脚本文件
rm ~/.local/share/nemo/scripts/compress_folders_to_zip.sh
rm ~/.local/share/nemo/scripts/merge-h264acc.sh
rm ~/.local/share/nemo/scripts/merge-videos.sh

# 重启 Nemo
nemo -q
```

---

## 自定义和修改

所有脚本都是标准的 Bash 脚本，可以根据需要进行修改：

### 修改压缩格式

编辑 `compress_folders_to_zip.sh`，将 `zip` 命令替换为其他压缩工具（如 `tar`）。

### 修改视频输出质量

编辑 `merge-h264acc.sh`，调整以下参数：
- CRF 值（0-51，越小质量越高）：`-crf 23`
- 预设速度：`-preset medium`（可选：ultrafast, fast, medium, slow, veryslow）
- 音频比特率：`-b:a 128k`

### 修改输出文件名

编辑相应脚本中的 `output_file` 变量定义部分。





