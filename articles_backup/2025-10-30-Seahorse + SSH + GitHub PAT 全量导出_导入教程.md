---
title: "Seahorse + SSH + GitHub PAT 全量导出/导入教程"
created_at: "2025-10-30 08:46:17"
updated_at: "2025-10-30 08:54:17"
issue_number: 58
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/58
---

# Seahorse + SSH + GitHub PAT 全量导出/导入教程

 **Seahorse + SSH + Git 凭证备份/恢复脚本**

> **备份 → 输出到脚本所在目录**  
> **恢复 → 自动读取脚本所在目录的 `.tar.gz` 文件**

---

## 两个脚本（直接复制粘贴使用）

---

### 脚本 1：`backup-seahorse-ssh.sh` —— **一键备份到当前目录**

```bash
#!/usr/bin/env bash
# 一键备份 Seahorse + SSH + Git 凭证 → 输出到脚本所在目录
# 用法: 放在任意目录，运行 ./backup-seahorse-ssh.sh

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backup-tmp-$(date +%Y%m%d-%H%M%S)"
FINAL_BACKUP="$SCRIPT_DIR/seahorse-ssh-full-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

echo "正在创建临时备份目录: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"/{keyrings,ssh}

# 1. 备份 Seahorse 密钥环
echo "正在备份 Seahorse 密钥环..."
cp -r ~/.local/share/keyrings/* "$BACKUP_DIR"/keyrings/ 2>/dev/null || true

# 2. 导出 GitHub PAT（明文）
echo "正在导出 GitHub PAT..."
secret-tool search --unlock server github.com > "$BACKUP_DIR"/github-pat.txt 2>/dev/null || echo "无 GitHub 凭证" > "$BACKUP_DIR"/github-pat.txt

# 3. 备份 SSH 密钥和配置
echo "正在备份 SSH 密钥..."
mkdir -p "$BACKUP_DIR"/ssh
cp ~/.ssh/id_* "$BACKUP_DIR"/ssh/ 2>/dev/null || true
cp ~/.ssh/config "$BACKUP_DIR"/ssh/ 2>/dev/null || true
cp ~/.ssh/known_hosts "$BACKUP_DIR"/ssh/ 2>/dev/null || true
cp ~/.ssh/authorized_keys "$BACKUP_DIR"/ssh/ 2>/dev/null || true

# 4. 导出 SSH 登录密码
echo "正在导出 SSH 登录密码..."
secret-tool search --unlock protocol ssh >> "$BACKUP_DIR"/ssh-passwords.txt 2>/dev/null || true

# 5. 打包到脚本目录
echo "正在压缩到脚本目录..."
tar -czf "$FINAL_BACKUP" -C "$BACKUP_DIR" .

# 6. 清理
rm -rf "$BACKUP_DIR"

echo ""
echo "备份完成！"
echo "文件: $FINAL_BACKUP"
echo "位置: 脚本所在目录"
echo "请复制此文件到 U 盘/云盘，并记住你的登录密码！"
echo "恢复时将此文件与 restore-seahorse-ssh.sh 放在同一目录运行"
```

---

### 脚本 2：`restore-seahorse-ssh.sh` —— **一键恢复，从当前目录读取**

```bash
#!/usr/bin/env bash
# 一键恢复 Seahorse + SSH + Git 凭证 → 从脚本所在目录读取备份
# 用法: 将此脚本与 seahorse-ssh-full-backup-*.tar.gz 放在同一目录，运行 ./restore-seahorse-ssh.sh

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "脚本目录: $SCRIPT_DIR"

echo ""
echo "一键恢复 Seahorse + SSH + Git 凭证"
echo "请确保："
echo "  1. 用户名与旧系统相同"
echo "  2. 登录密码与旧系统相同"
echo "  3. 已安装: sudo apt install seahorse gnome-keyring libsecret-tools openssh-client git"
echo ""

# 查找当前目录下的最新备份
BACKUP_FILE=$(ls -t "$SCRIPT_DIR"/seahorse-ssh-full-backup-*.tar.gz 2>/dev/null | head -n1)
if [[ -z "$BACKUP_FILE" ]]; then
    echo "错误：在当前目录未找到备份文件！"
    echo "请将 seahorse-ssh-full-backup-*.tar.gz 与此脚本放在同一目录"
    exit 1
fi

echo "找到备份: $BACKUP_FILE"
echo "正在解压..."

# 临时解压目录
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

# 3. 启动 GNOME Keyring
echo "正在启动 GNOME Keyring（含 ssh 组件）..."
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
echo "   2. ssh your-server-ip"
echo "      → 自动登录"
echo "   3. seahorse &"
echo "      → 查看 Passwords → login → github.com"
echo ""
echo "重启终端或系统后，所有凭证自动生效！"
```

---

## 使用方法

[backup&restore-seahorse.tar.gz](https://github.com/user-attachments/files/23229348/backup.restore-seahorse.tar.gz)

### 第一步：旧系统备份

```bash
# 1. 创建目录
mkdir ~/backup-tools
cd ~/backup-tools

# 2. 保存两个脚本
nano backup-seahorse-ssh.sh
# → 粘贴第一个脚本 → 保存

nano restore-seahorse-ssh.sh
# → 粘贴第二个脚本 → 保存

# 3. 运行备份
chmod +x backup-seahorse-ssh.sh
./backup-seahorse-ssh.sh
```

输出：
```
备份完成！
文件: /home/user/backup-tools/seahorse-ssh-full-backup-20251030-1430.tar.gz
```

---

### 第二步：新系统恢复

```bash
# 1. 将整个 backup-tools 目录复制到新系统任意位置
#    例如：~/restore-kit/

# 2. 进入目录
cd ~/restore-kit

# 3. 安装依赖
sudo apt update
sudo apt install seahorse gnome-keyring libsecret-tools openssh-client git

# 4. 运行恢复
chmod +x restore-seahorse-ssh.sh
./restore-seahorse-ssh.sh
```

→ 自动读取同目录下的 `.tar.gz` 文件并恢复！

---

## 完美通用场景

| 场景 | 操作 |
|------|------|
| U 盘恢复 | 把 `backup-tools/` 整个目录复制到 U 盘 → 插入新系统 → 打开终端 → `cd /media/user/USBDISK/backup-tools` → `./restore-seahorse-ssh.sh` |
| 云盘恢复 | 下载整个文件夹 → 解压 → 运行恢复脚本 |
| 多人共享 | 发 `backup-tools.zip` 给朋友 → 解压运行 |

---

## 验证恢复成功

```bash
# Git
git ls-remote https://github.com/your-username/private-repo.git   # 不提示

# SSH
ssh your-server-ip                                               # 自动登录

# Seahorse
seahorse &                                                       # 看到 login → github.com
```

---

## 最终文件结构（backup-tools 目录）

```
backup-tools/
├── backup-seahorse-ssh.sh
├── restore-seahorse-ssh.sh
└── seahorse-ssh-full-backup-20251030-1430.tar.gz   ← 自动生成
```



