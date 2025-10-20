---
title: "Aria2 + Chrome 下载接管教程 (Linux Mint)"
created_at: "2025-10-20 03:43:58"
updated_at: "2025-10-20 03:43:58"
issue_number: 43
labels: ['apps']
url: https://github.com/syaofox/syaofox.github.io/issues/43
---

# Aria2 + Chrome 下载接管教程 (Linux Mint)


本教程分为三个主要部分：安装 Aria2、设置 Chrome 扩展连接，以及配置开机自启动服务。

### 步骤一：安装 Aria2 命令行下载工具

您在提问中已完成了此步骤，但这里作为完整教程的一部分列出。

1.  **打开终端**：

    ```bash
    sudo apt update
    sudo apt install aria2
    ```

2.  **验证安装**：

    ```bash
    aria2c -v
    ```

    如果显示版本信息，则表示安装成功。

-----

### 步骤二：配置和启动 Aria2 RPC 服务 (Systemd 自启动准备)

我们使用配置文件和 Systemd 来确保 Aria2c 服务安全、稳定地运行在后台，并允许 Chrome 扩展程序通过 **RPC 接口**调用它。

#### 1\. 创建 Aria2 配置文件和目录

为了管理下载和会话，我们需要一个配置文件。

```bash
# 创建配置和会话文件所在的目录
mkdir -p ~/.config/aria2
# 创建默认下载目录 (请根据您的用户名和偏好修改路径)
mkdir -p ~/Downloads/aria2
# 创建 aria2.conf 配置文件
nano ~/.config/aria2/aria2.conf
```

将以下内容粘贴到 `aria2.conf` 文件中，并**替换 `dir` 行中的 `YOUR_USERNAME`**：

```conf
# 启用 RPC
enable-rpc=true
rpc-listen-all=true
rpc-listen-port=6800
rpc-allow-origin-all=true

# **强烈推荐**：设置 RPC 密钥，以防未经授权的访问。
# 请将 YOUR_STRONG_SECRET_KEY 替换成一个复杂的密码！
# rpc-secret=YOUR_STRONG_SECRET_KEY

# 文件会话和保存
input-file=~/.config/aria2/aria2.session
save-session=~/.config/aria2/aria2.session
daemon=true

# 下载路径
dir=/home/YOUR_USERNAME/Downloads/aria2
# 其他优化设置
max-concurrent-downloads=5
continue=true
```

保存并退出 `nano` (`Ctrl + O` 保存，`Ctrl + X` 退出)。

#### 2\. 配置 Systemd 用户服务

我们将创建一个用户级别的 Systemd 服务，这样 Aria2c 会在您**登录**系统后自动启动。

```bash
# 创建 Systemd 用户服务目录
mkdir -p ~/.config/systemd/user/
# 创建服务文件
nano ~/.config/systemd/user/aria2c.service
```

将以下内容粘贴到 `aria2c.service` 文件中：

```ini
[Unit]
Description=Aria2c Downloader
After=network.target

[Service]
# %i 在用户模式下自动替换为你的用户名
User=%i
# 启动命令：加载配置文件并以后台模式运行
ExecStart=/usr/bin/aria2c --conf-path=/home/%i/.config/aria2/aria2.conf
# 停止命令：优雅地关闭 Aria2
ExecStop=/usr/bin/aria2c --shutdown=true

[Install]
WantedBy=default.target
```

保存并退出 `nano` (`Ctrl + O` 保存，`Ctrl + X` 退出)。

#### 3\. 启用并立即启动服务

运行以下命令，使服务生效并开机自启动：

```bash
# 重新加载 Systemd 配置
systemctl --user daemon-reload
# 启用服务，设置开机自启动
systemctl --user enable aria2c.service
# 立即启动服务
systemctl --user start aria2c.service
# 检查服务状态
systemctl --user status aria2c.service
```

如果看到 `Active: active (running)`，则表示服务已成功启动，并且每次登录系统后都会自动运行。

-----

### 步骤三：安装和配置 Chrome 扩展程序

您需要一个 Chrome 扩展程序来拦截浏览器下载请求，并通过 RPC 接口发送给后台运行的 Aria2c 服务。

#### 1\. 安装扩展程序

1.  打开 **Chrome 浏览器**。
2.  进入 Chrome Web Store，搜索 **Aria2 Explorer**（推荐）或 **Aria2c Integration 2**。
3.  点击 **“添加至 Chrome”** 完成安装。

#### 2\. 配置扩展程序连接

1.  点击浏览器右上角的扩展程序图标，找到并进入 **Aria2 Explorer** 的**选项/设置**页面。
2.  在连接配置中，确保以下设置与您的 Aria2c 服务一致：
      * **协议/地址**：`http://127.0.0.1`
      * **端口**：`6800`
      * **RPC 密钥**：如果您在 `aria2.conf` 中设置了 `rpc-secret`，请在这里输入相同的密钥。
3.  配置完成后，扩展程序通常会显示 **连接状态：已连接**。

-----

### 步骤四：开始使用 Aria2 下载

现在，您的 Chrome 浏览器已准备好使用 Aria2c 进行高速下载。

1.  **自动接管**：点击普通的下载链接，扩展程序将自动拦截并将其任务发送到 Aria2c。
2.  **手动发送**：右键点击任何下载链接，选择上下文菜单中的 **“使用 Aria2 下载”** 选项。

Aria2 Explorer 扩展通常内置了一个简单的下载管理器（如 AriaNG），您点击扩展图标即可查看和管理您的下载任务。

