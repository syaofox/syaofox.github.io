---
title: "Seahorse + SSH + GitHub PAT 全量导出/导入教程"
created_at: "2025-10-30 08:46:17"
updated_at: "2025-10-30 08:46:17"
issue_number: 58
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/58
---

# Seahorse + SSH + GitHub PAT 全量导出/导入教程

**Seahorse + SSH + GitHub PAT 全量导出/导入教程**，专为 **LMDE 7 / Linux Mint / Ubuntu 系** 设计。

---

## 目标：重装系统后 **一键恢复** 全部内容

| 项目 | 是否恢复 |
|------|----------|
| GitHub PAT（Git 凭证） | Yes |
| Wi-Fi 密码 | Yes |
| 浏览器/应用密码 | Yes |
| SSH 私钥（id_rsa、id_ed25519） | Yes |
| `ssh user@host` 记住的密码 | Yes |
| `known_hosts`、`config` | Yes |
| Seahorse `login` 密钥环 | Yes |
| ssh-agent 自动加载 | Yes |

---

## 两个脚本（复制粘贴即可用）

---

### 脚本 1：`backup-seahorse-ssh.sh` —— **一键备份**

```bash
#!/usr/bin/env bash
# 一键备份 Seahorse + SSH + Git 凭证
# 保存为: ~/backup-seahorse-ssh.sh
# 用法: chmod +x backup-seahorse-ssh.sh && ./backup-seahorse-ssh.sh

set -e

BACKUP_DIR="/tmp/seahorse-ssh-backup-$(date +%Y%m%d-%H%M%S)"
FINAL_BACKUP="$HOME/seahorse-ssh-full-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

echo "正在创建备份目录: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"/{keyrings,ssh}

# 1. 备份 Seahorse 密钥环（加密文件）
echo "正在备份 Seahorse 密钥环..."
cp -r ~/.local/share/keyrings/* "$BACKUP_DIR"/keyrings/ 2>/dev/null || true

# 2. 导出明文 PAT（可选防丢失）
echo "正在导出 GitHub PAT（明文）..."
secret-tool search --unlock server github.com > "$BACKUP_DIR"/github-pat.txt 2>/dev/null || echo "无 GitHub 凭证" > "$BACKUP_DIR"/github-pat.txt

# 3. 备份 SSH 私钥和配置
echo "正在备份 SSH 密钥..."
mkdir -p "$BACKUP_DIR"/ssh
cp ~/.ssh/id_* "$BACKUP_DIR"/ssh/ 2>/dev/null || true
cp ~/.ssh/config "$BACKUP_DIR"/ssh/ 2>/dev/null || true
cp ~/.ssh/known_hosts "$BACKUP_DIR"/ssh/ 2>/dev/null || true
cp ~/.ssh/authorized_keys "$BACKUP_DIR"/ssh/ 2>/dev/null || true

# 4. 导出 SSH 登录密码（如果记住过）
echo "正在导出 SSH 登录密码..."
secret-tool search --unlock protocol ssh >> "$BACKUP_DIR"/ssh-passwords.txt 2>/dev/null || true

# 5. 打包
echo "正在压缩备份..."
tar -czf "$FINAL_BACKUP" -C "$BACKUP_DIR" .

# 6. 清理
rm -rf "$BACKUP_DIR"

echo ""
echo "备份完成！"
echo "文件: $FINAL_BACKUP"
echo "请复制到 U 盘/云盘，并记住你的登录密码！"
echo "恢复时使用 restore-seahorse-ssh.sh"
```

---

### 脚本 2：`restore-seahorse-ssh.sh` —— **一键恢复**

```bash
#!/usr/bin/env/bash
# 一键恢复 Seahorse + SSH + Git 凭证
# 保存为: ~/restore-seahorse-ssh.sh
# 用法: chmod +x restore-seahorse-ssh.sh && ./restore-seahorse-ssh.sh

set -e

echo "一键恢复 Seahorse + SSH + Git 凭证"
echo "请确保："
echo "  1. 用户名与旧系统相同"
echo "  2. 登录密码与旧系统相同"
echo "  3. 已安装: sudo apt install seahorse gnome-keyring libsecret-tools openssh-client"
echo ""

# 查找最新备份文件
BACKUP_FILE=$(ls -t ~/seahorse-ssh-full-backup-*.tar.gz 2>/dev/null | head -n1)
if [[ -z "$BACKUP_FILE" ]]; then
    echo "未找到备份文件！请放入 seahorse-ssh-full-backup-*.tar.gz 到 ~/"
    exit 1
fi

echo "找到备份: $BACKUP_FILE"
echo "正在解压..."

# 临时解压
TEMP_DIR="/tmp/restore-seahorse-ssh"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# 1. 恢复 keyrings
echo "正在恢复 Seahorse 密钥环..."
mkdir -p ~/.local/share/keyrings
cp "$TEMP_DIR"/keyrings/* ~/.local/share/keyrings/ 2>/dev/null || true
chmod 600 ~/.local/share/keyrings/*.keyring 2>/dev/null || true
chmod 700 ~/.local/share/keyrings/

# 2. 恢复 SSH
echo "正在恢复 SSH 密钥..."
mkdir -p ~/.ssh
cp "$TEMP_DIR"/ssh/id_* ~/.ssh/ 2>/dev/null || true
cp "$TEMP_DIR"/ssh/config ~/.ssh/ 2>/dev/null || true
cp "$TEMP_DIR"/ssh/known_hosts ~/.ssh/ 2>/dev/null || true
cp "$TEMP_DIR"/ssh/authorized_keys ~/.ssh/ 2>/dev/null || true
chmod 600 ~/.ssh/id_* 2>/dev/null || true
chmod 644 ~/.ssh/config ~/.ssh/known_hosts ~/.ssh/authorized_keys 2>/dev/null || true

# 3. 启动 GNOME Keyring（含 ssh）
echo "正在启动 GNOME Keyring..."
eval $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)
export SSH_AUTH_SOCK

# 4. 永久配置 .bashrc
echo "正在写入开机自启..."
if ! grep -q "gnome-keyring-daemon.*ssh" ~/.bashrc 2>/dev/null; then
    cat >> ~/.bashrc << 'EOF'

# === GNOME Keyring + SSH Agent (Auto Restore) ===
eval $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)
export SSH_AUTH_SOCK
EOF
fi

# 5. 配置 Git
echo "正在配置 Git 使用 libsecret..."
git config --global credential.helper libsecret 2>/dev/null || true

# 6. 清理
rm -rf "$TEMP_DIR"

echo ""
echo "恢复完成！"
echo ""
echo "请执行以下操作触发解锁："
echo "   1. git ls-remote https://github.com/your-username/any-repo.git"
echo "      → 输入原登录密码解锁 keyring"
echo "   2. ssh user@your-server"
echo "      → 自动登录或加载密钥"
echo "   3. seahorse &"
echo "      → 查看 Passwords → login → github.com"
echo ""
echo "重启终端或系统后，所有凭证自动生效！"
```

---


[backup&restore-seahorse.tar.gz](https://github.com/user-attachments/files/23229161/backup.restore-seahorse.tar.gz)

## 使用方法（超简单）

### 第一步：旧系统运行备份

```bash
# 1. 保存脚本
nano ~/backup-seahorse-ssh.sh
# 粘贴上面第一个脚本，Ctrl+O 保存，Enter 确认，Ctrl+X 退出

# 2. 运行
chmod +x ~/backup-seahorse-ssh.sh
~/backup-seahorse-ssh.sh
```

输出：
```
备份完成！
文件: /home/user/seahorse-ssh-full-backup-20251030-1423.tar.gz
```

将此文件复制到 **U 盘 / 云盘**

---

### 第二步：新系统运行恢复

```bash
# 1. 安装依赖
sudo apt update
sudo apt install seahorse gnome-keyring libsecret-tools openssh-client git

# 2. 放入备份文件到 ~
#    cp /path/to/seahorse-ssh-full-backup-*.tar.gz ~/

# 3. 保存恢复脚本
nano ~/restore-seahorse-ssh.sh
# 粘贴上面第二个脚本，保存退出

# 4. 运行
chmod +x ~/restore-seahorse-ssh.sh
~/restore-seahorse-ssh.sh
```

---

## 验证全部恢复（3 个命令）

```bash
# 1. Git 自动登录
git ls-remote https://github.com/your-username/private-repo.git
# → 不提示密码

# 2. SSH 自动登录
ssh your-server-ip
# → 自动登录

# 3. 查看 Seahorse
seahorse &
# → Passwords → login → github.com → Show password → 输入旧密码 → 看到 PAT
```

---

## 不能恢复的情况（红线）

| 情况 | 是否可恢复 |
|------|------------|
| 忘记原登录密码 | No |
| 新用户名不同 | No |
| 没运行备份脚本 | No |

---

## 推荐备份频率

| 项目 | 建议 |
|------|------|
| 每次生成新 PAT | 运行备份 |
| 每次添加 SSH 密钥 | 运行备份 |
| 每月一次 | 运行备份 |


