---
layout: post
title: linux mint samba挂载
date: 2025-10-03 11:46:00 +0800
categories: [tips]
tags: [system]
---

#### 使用 Cifs 挂载 

Cifs (Common Internet File System) 是另一种在 Linux 上挂载 SMB/CIFS 共享的协议。与 GVfs 相比，通过 `mount.cifs` 挂载的文件共享会更像一个本地文件系统，其路径是一个标准的本地目录，例如 `/mnt/my_smb_share`。这使得大多数应用程序可以无缝地处理这些文件。

**步骤：**

1.  **安装 cifs-utils:**

    ```bash
    sudo apt update
    sudo apt install cifs-utils
    ```

2.  **创建挂载点:**

    ```bash
    sudo mkdir /mnt/smb_share
    ```

3. **创建凭证文件**
  在你的用户主目录下创建一个新的隐藏文件，例如 `.smbcredentials`。
  
  ```bash
  nano ~/.smbcredentials
  ```

在该文件中，写入你的用户名和密码，格式如下：

```
username=你的samba用户名
password=你的samba密码
```

4. **设置文件权限**

**这是最关键的一步。** 确保这个文件的权限只允许你（文件的所有者）读取和写入。

```bash
chmod 600 ~/.smbcredentials
```

  * `chmod 600` 表示只有文件所有者有读写权限，其他任何人都无法访问该文件。

5.  **手动挂载 (临时测试)**

在终端中，使用 `-o credentials` 选项来指定这个凭证文件。

```bash
sudo mount -t cifs -o credentials=/home/你的用户名/.smbcredentials,uid=$(id -u),gid=$(id -g) //windows_server_ip/share_folder /mnt/smb_share
```

  * `credentials=/home/你的用户名/.smbcredentials`: 指向你刚才创建的凭证文件。
  * `uid=$(id -u),gid=$(id -g)`: 确保挂载后的文件所有者和用户组都是你当前的用户。这可以让你像操作本地文件一样来读写它们。

-----

6. **自动挂载 (永久)**

如果你想让系统每次启动时都自动挂载，可以编辑 `/etc/fstab` 文件。

```bash
sudo nano /etc/fstab
```

在文件末尾添加以下一行，同样使用 `credentials` 选项。

```
//windows_server_ip/share_folder /mnt/smb_share cifs credentials=/home/你的用户名/.smbcredentials,uid=1000,gid=1000 0 0
```

  * 将 `你的用户名` 替换为你的实际用户名。
  * `uid=1000,gid=1000` 是大多数 Linux Mint 用户的默认 UID 和 GID。你可以通过在终端输入 `id -u` 和 `id -g` 来确认你的 ID。

设置好 `fstab` 后，保存并退出。然后可以执行 `sudo mount -a` 命令，测试是否可以成功挂载。如果没有报错，下次重启系统时，你的 Samba 共享就会自动挂载到 `/mnt/smb_share` 目录了。