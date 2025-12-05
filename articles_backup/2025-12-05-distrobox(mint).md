---
title: "distrobox(mint)"
created_at: "2025-12-05 00:42:23"
updated_at: "2025-12-05 00:42:23"
issue_number: 62
labels: ['apps']
url: https://github.com/syaofox/syaofox.github.io/issues/62
---

# distrobox(mint)

下面是从零到完美 Arch AUR 容器的**最短最纯净版**（全程只用 apt + 几条命令，适合 Mint 用户）：

```bash
# 1. 一条命令安装 distrobox + podman（Mint 21/22/23 都自带）
sudo apt update && sudo apt install -y distrobox podman

# 2. 创建持久化缓存目录
mkdir -p ~/.cache/distrobox/arch/{pacman,paru}

# 3. 创建终极 Arch 容器（带永久缓存）
distrobox create --name arch \
  --image docker.io/greyltc/archlinux-aur:paru \
  --pull \
  --additional-flags "-v ~/.cache/distrobox/arch/pacman:/var/cache/pacman:Z \
                      -v ~/.cache/distrobox/arch/paru:/var/cache/paru:Z"

# 4. 第一次进入完成初始化
distrobox enter arch -- echo "初始化完成！"

# 5. 写入你这辈子都要用的最简别名（复制粘贴就行）
cat << 'EOF' >> ~/.bashrc

# Distrobox Arch 终极快捷键（Mint 专用）
alias da='distrobox enter arch'
alias dparu='distrobox enter arch -- paru'
alias de='distrobox enter arch -- distrobox-export --app'
alias aur-update='distrobox stop arch --yes && podman pull docker.io/greyltc/archlinux-aur:paru && distrobox enter arch -- distrobox-upgrade && echo "更新完成！"'
EOF

# 6. 立刻生效
source ~/.bashrc
```

全过程结束！现在直接试试：

```bash
dparu -S google-chrome    # 直接装
de chrome                           # 导出到主机
da                                             # 进入容器玩
```


