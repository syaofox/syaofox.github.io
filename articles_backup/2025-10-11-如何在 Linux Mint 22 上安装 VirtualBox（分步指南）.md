---
title: "如何在 Linux Mint 22 上安装 VirtualBox（分步指南）"
created_at: "2025-10-11 11:51:02"
updated_at: "2025-10-12 01:12:29"
issue_number: 20
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/20
---

# 如何在 Linux Mint 22 上安装 VirtualBox（分步指南）

# 如何在 Linux Mint 22 上安装 VirtualBox（分步指南）

您可以通过以下步骤在 Linux Mint 22 上安装最新版本的 Oracle VirtualBox：

## 第 1 步：在安装前移除任何冲突的 VirtualBox 版本

如果您是从 Linux Mint 的默认仓库安装的 VirtualBox，请先将其卸载。该仓库中的版本通常不是最新的。我们将从 virtualbox.org 安装最新版本。

```bash
sudo apt purge virtualbox
```

## 第 2 步：安装依赖项

接下来，运行以下命令安装 VirtualBox 所需的依赖项：

```bash
sudo apt update
sudo apt install -y dkms build-essential linux-headers-$(uname -r)
```


## 第 3 步：下载适用于 Linux Mint 22 的 VirtualBox

要下载适用于 Linux Mint 的 VirtualBox，先查看系统报告确定ubuntu内核版本，然后访问 [VirtualBox Linux 下载页面](https://www.virtualbox.org/wiki/Downloads)](https://www.virtualbox.org/wiki/Downloads) 并下载标记为 **Ubuntu 24.04** 的软件包。

## 第 4 步：apt 安装 下载的deb包

将文件移动到 /tmp 目录,避免atp权限错误

```bash
mv ~/Downloads/virtualbox-7.2_7.2.2-170484~Ubuntu~noble_amd64.deb /tmp/
```

然后尝试安装

```bash
sudo apt install /tmp/virtualbox-7.2_7.2.2-170484~Ubuntu~noble_amd64.deb
```

## 第 5 步：将您的用户帐户添加到 `vboxusers` 组

接下来，您需要将您的 Linux 用户帐户添加到 `vboxusers` 组——任何使用 VirtualBox 的用户都需要在这个组中。

```bash
sudo usermod -aG vboxusers $USER
```

之后，您需要**重启您的系统**才能使更改生效。

## 第 6 步：安装 VirtualBox 扩展包 (Extension Pack)

我们最后一步是安装 VirtualBox 扩展包，以启用附加功能，如 USB 2.0/3.0 设备、RDP（远程桌面协议）、磁盘加密等。

首先，访问 [[VirtualBox 下载页面](https://www.virtualbox.org/wiki/Downloads)](https://www.virtualbox.org/wiki/Downloads) 并下载 VirtualBox 扩展包——**请确保版本与您安装的 VirtualBox 版本匹配**。

下载扩展包后，双击该文件进行安装。

## 如何更新 VirtualBox 到最新版本

要更新 VirtualBox 到最新版本，请遵循与安装时相同的步骤：

1.  从 VirtualBox Linux 下载页面下载最新的 `.deb` 软件包。
2.  使用 `gdebi` 命令安装它。
3.  **重要提示：** 同时下载并安装最新的**扩展包**——它必须与您更新后的 VirtualBox 版本匹配。

这将把 VirtualBox 更新到最新版本，而不会删除您任何现有的虚拟机。

## VirtualBox 已可使用

这就是您需要做的全部。您现在可以使用 VirtualBox 在您的 Linux Mint 桌面环境上运行虚拟机了。



## 报错无法启动虚拟机的解决方法

如下报错

```bash
VT-x is being used by another hypervisor (VERR_VMX_IN_VMX_ROOT_MODE).

VirtualBox can't operate in VMX root mode. Please disable the KVM kernel extension, recompile your kernel and reboot (VERR_VMX_IN_VMX_ROOT_MODE).
```


这是致命的启动错误，它明确地告诉您：VirtualBox 无法启动，因为它需要的 硬件虚拟化 功能（VT-x，在 Intel CPU 上）已经被主机系统上的 另一个 hypervisor (虚拟机管理器) 占用了。您需要确保 KVM 模块（Linux 的原生虚拟化模块）没有被加载或使用。

### 临时解决方案

尝试命令：`sudo modprobe -r kvm_intel` 或 `sudo modprobe -r kvm_amd`（取决于 CPU 类型）。


### 永久解决方案

##### 方法一：创建 Blacklist 文件（推荐）

这是最标准和推荐的方法，用于阻止特定内核模块的自动加载。

1.  **创建配置文件:** 打开终端并使用文本编辑器（如 `nano` 或 `vim`）创建一个新的 `.conf` 文件。

    ```bash
    sudo nano /etc/modprobe.d/blacklist-kvm.conf
    ```

2.  **添加禁用指令:** 在文件中添加以下两行内容，将 `kvm_intel` 和 `kvm` 本身都列入黑名单：

    ```conf
    # 阻止 KVM 模块自动加载，避免与 VirtualBox 冲突
    blacklist kvm_intel
    blacklist kvm
    ```

    *（如果你是 AMD CPU，则应添加 `blacklist kvm_amd`）*

3.  **保存并退出:**

      * 如果你使用的是 `nano`：按 $\text{Ctrl+O}$ 写入，然后按 $\text{Enter}$ 确认，最后按 $\text{Ctrl+X}$ 退出。

4.  **更新 Initramfs (重要步骤):** 有些 Linux 发行版（如 Ubuntu/Debian）需要更新启动时的初始内存文件系统，才能使黑名单生效：

    ```bash
    sudo update-initramfs -u
    ```

5.  **重启系统:**

    ```bash
    sudo reboot
    ```

##### 方法二：通过 GRUB 启动参数禁用（备用）

你可以修改 GRUB 配置文件，在内核启动时就指定不加载 KVM 模块。

1.  **编辑 GRUB 配置文件:**

    ```bash
    sudo nano /etc/default/grub
    ```

2.  **修改 GRUB\_CMDLINE\_LINUX\_DEFAULT:**
    在这一行中，添加 `modprobe.blacklist=kvm,kvm_intel` 到现有参数的**引号内**。

    **修改前示例：**

    ```conf
    GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
    ```

    **修改后示例：**

    ```conf
    GRUB_CMDLINE_LINUX_DEFAULT="quiet splash modprobe.blacklist=kvm,kvm_intel"
    ```

    *（AMD 用户将 `kvm_intel` 替换为 `kvm_amd`。）*

3.  **保存并退出:** (同上)

4.  **更新 GRUB 配置:**

    ```bash
    sudo update-grub
    ```

5.  **重启系统:**

    ```bash
    sudo reboot
    ```

-----

**重启后验证:**

系统重启后，你可以再次运行以下命令来确认 `kvm_intel` 是否已经被禁用了：

```bash
lsmod | grep kvm
```

如果这条命令没有输出任何结果，说明 `kvm` 模块没有被加载，此时你应该能够顺利启动你的 VirtualBox 虚拟机了。

