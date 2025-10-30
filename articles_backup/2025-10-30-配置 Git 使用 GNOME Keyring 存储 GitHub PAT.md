---
title: "配置 Git 使用 GNOME Keyring 存储 GitHub PAT"
created_at: "2025-10-30 08:25:39"
updated_at: "2025-10-30 08:25:39"
issue_number: 57
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/57
---

# 配置 Git 使用 GNOME Keyring 存储 GitHub PAT


## 1. 先检查系统是否已经自带 `libsecret` helper

```bash
git credential-libsecret --version
```

- **如果能输出版本号** → 说明系统已经装好，直接跳到第 4 步配置即可。  
- **如果提示 “command not found”** → 继续下面的编译步骤。

---

## 2. 安装编译所需依赖

```bash
sudo apt update
sudo apt install -y git libsecret-1-0 libsecret-1-dev pkg-config make gcc
```

> `libsecret-1-dev` 提供了 `pkg-config --cflags --libs libsecret-1` 需要的头文件和库。

---

## 3. **从源码编译** `git-credential-libsecret`

### 3.1 克隆 Git 源码（只需要 contrib 目录）

```bash
mkdir -p ~/src && cd ~/src
git clone --depth 1 https://github.com/git/git.git
cd git/contrib/credential/libsecret
```

### 3.2 编译（自动使用 pkg-config）

```bash
make
```

> 编译成功后会在当前目录生成可执行文件 **`git-credential-libsecret`**。

### 3.3 把它放到系统可执行路径（推荐）

```bash
sudo cp git-credential-libsecret /usr/local/bin/
sudo chmod 755 /usr/local/bin/git-credential-libsecret
```

> 这样 `git credential-libsecret` 就能全局找到，**不需要写完整路径**。

---

## 4. 配置 Git 使用 libsecret

```bash
git config --global credential.helper libsecret
```

> **注意**：直接写 `libsecret`（不带路径），Git 会自动在 `$PATH` 中搜索 `git-credential-libsecret`。  
> 如果你把二进制放到了别的目录（如 `/opt/bin`），只要确保该目录在 `$PATH` 里即可。

---

## 5. 验证是否生效

```bash
# 触发一次需要凭证的操作
git ls-remote https://github.com/syaofox/mmpices
```

第一次会弹出 **GNOME Keyring 解锁/输入密码** 对话框：

1. 输入 **GitHub 用户名**  
2. **密码** 栏里粘贴 **PAT**（Personal Access Token）

完成后，凭证会自动保存到 Keyring。

再次执行相同命令 **不应再弹密码框**。

---

## 6. 用 Seahorse 查看/删除（可选）

```bash
seahorse &
```

搜索 `github.com`，你会看到类似：

```
Login: your-github-username
Password: <encrypted>
Server: github.com
Protocol: https
```

---

## 常见问题 & 排查

| 症状 | 检查点 | 解决办法 |
|------|--------|----------|
| `git credential-libsecret: command not found` | `which git-credential-libsecret` | 确保第 3.3 步把二进制放进 `$PATH`（如 `/usr/local/bin`） |
| 编译报 `pkg-config` 找不到 `libsecret-1` | `pkg-config --modversion libsecret-1` | 重新安装 `libsecret-1-dev` |
| 弹出密码框但 **不保存**，下次仍要输入 | `git config --global --list | grep credential` | 确认是 `credential.helper=libsecret`（不是 `cache`、`store` 等） |
| 没有弹出解锁框，报 `Failed to unlock the keyring` | Keyring 守护进程未启动 | `eval $(gnome-keyring-daemon --start --components=secrets)` 并把这行加入 `~/.bashrc` |

---

## 完整一键脚本（复制粘贴即可）

```bash
#!/usr/bin/env bash
set -e

# 1. 安装依赖
sudo apt update
sudo apt install -y git libsecret-1-0 libsecret-1-dev pkg-config make gcc

# 2. 编译
mkdir -p ~/src && cd ~/src
git clone --depth 1 https://github.com/git/git.git
cd git/contrib/credential/libsecret
make

# 3. 安装到 /usr/local/bin
sudo cp git-credential-libsecret /usr/local/bin/
sudo chmod 755 /usr/local/bin/git-credential-libsecret

# 4. 配置 Git
git config --global credential.helper libsecret

echo "配置完成！现在执行一次需要认证的 Git 操作，输入 PAT 后即可自动保存。"
```

保存为 `setup-git-libsecret.sh`，`chmod +x` 后运行即可。

---

**搞定！** 以后 `git push/pull/clone` 再也不用手动敲 PAT，全部交给 GNOME Keyring（Seahorse）管理。

