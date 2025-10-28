---
title: "Flakes + Home-Manager（独立用户配置）"
created_at: "2025-10-28 11:38:57"
updated_at: "2025-10-28 11:38:57"
issue_number: 53
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/53
---

# Flakes + Home-Manager（独立用户配置）

**从图形化安装的 `configuration.nix` → Flakes + Home-Manager（独立用户配置）**  

> 目标：  
> 1. 系统配置用 **Flake** 管理（`flake.nix` + `configuration.nix`）  
> 2. 用户配置（桌面软件、dotfiles、shell）用 **Home-Manager** 管理  
> 3. 保留你现在的 Cinnamon、输入法、SPICE 等全部功能  
> 4. 以后 `nixos-rebuild switch --flake .#hostname` 一键升级  

---

## 1. 目录结构（建议）

```bash
/nixos-config/               # 项目根目录
├── flake.nix
├── flake.lock
├── configuration.nix        # 系统级（保持你原来的）
├── home.nix                 # 用户级（Home-Manager）
└── hardware-configuration.nix  # 保持不变
```

> 把你现在的 `/etc/nixos/` 内容 **整个复制** 到 `/nixos-config/`，然后按下面步骤改。

---

## 2. 启用 Flakes（只需一次）

```bash
sudo nix-channel --add https://github.com/nixos/nixpkgs/archive/nixos-unstable.tar.gz nixpkgs
sudo nix-channel --update
sudo nix flake init -t templates#simple   # 可选，生成模板
```

> 或者直接手动创建 `flake.nix`

---

## 3. `flake.nix`（核心）

```nix
{
  description = "NixOS + Home-Manager with Flakes";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    # 可选：锁定版本
    # flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, home-manager, ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };
      username = "syaofox";
      hostname = "nixos";
    in {
      nixosConfigurations.${hostname} = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./configuration.nix
          ./hardware-configuration.nix

          home-manager.nixosModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;
            home-manager.users.${username} = import ./home.nix;

            # 传递 username 给 home.nix（可选）
            home-manager.extraSpecialArgs = { inherit username; };
          }
        ];
      };
    };
}
```

---

## 4. `home.nix`（用户配置，替代 `users.users.syaofox.packages`）

```nix
{ config, pkgs, username, ... }:

{
  # Home Manager 版本
  home.stateVersion = "25.05";

  # ---------- 用户软件 ----------
  home.packages = with pkgs; [
    firefox
    # thunderbird
    # 其他你想装的
  ];

  # ---------- 桌面环境 ----------
  programs.bash.enable = true;  # 启用 bash 补全等

  # （可选）git 配置
  programs.git = {
    enable = true;
    userName = "syaofox";
    userEmail = "syaofox@example.com";
  };

  # （可选）zsh + oh-my-zsh
  # programs.zsh.enable = true;
  # programs.zsh.oh-my-zsh.enable = true;

  # ---------- 桌面文件、主题等 ----------
  # gtk 主题、图标、鼠标
  gtk = {
    enable = true;
    theme.package = pkgs.gnome-themes-extra;
    theme.name = "Adwaita";
    iconTheme.package = pkgs.papirus-icon-theme;
    iconTheme.name = "Papirus";
  };

  # ---------- fcitx5 环境变量（系统已设，这里可重复保险）----------
  home.sessionVariables = {
    GTK_IM_MODULE = "fcitx";
    QT_IM_MODULE  = "fcitx";
    XMODIFIERS    = "@im=fcitx";
  };

  # ---------- 启动 fcitx5 ----------
  systemd.user.services.fcitx5 = {
    description = "Fcitx5 input method";
    wantedBy = [ "default.target" ];
    serviceConfig = {
      ExecStart = "${pkgs.fcitx5}/bin/fcitx5 -d";
      Restart = "always";
    };
  };
}
```

> 你原来的 `environment.systemPackages` 里 fcitx5 相关包 **保留在系统**，这里只管用户级变量。

---

## 5. 修改 `configuration.nix`（删掉用户包，改用 HM）

```diff
-  users.users.syaofox = {
-    isNormalUser = true;
-    description = "syaofox";
-    extraGroups = [ "networkmanager" "wheel" ];
-    packages = with pkgs; [
-    #  thunderbird
-    ];
-  };
+  users.users.syaofox = {
+    isNormalUser = true;
+    description = "syaofox";
+    extraGroups = [ "networkmanager" "wheel" ];
+    # packages 移到 home.nix
+  };
```

> 其它所有系统配置 **完全不动**（内核、Cinnamon、SPICE、fcitx5 框架等）

---

## 6. 第一次构建

```bash
cd /nixos-config
sudo nixos-rebuild switch --flake .#nixos
```

> 成功后，你会看到 Home-Manager 也一起激活了

---

## 7. 以后怎么用？

```bash
# 修改系统配置 → 编辑 configuration.nix
# 修改用户配置 → 编辑 home.nix
sudo nixos-rebuild switch --flake .#nixos
```

> 想加新软件？  
> - 系统级 → `environment.systemPackages`  
> - 用户级 → `home.packages`（推荐）

---

## 8. 额外技巧

### 8.1 多个主机？用 `hosts/hostname/`

```
hosts/
├── laptop/
│   ├── flake.nix
│   ├── configuration.nix
│   └── home.nix
├── vm/
│   └── ...
```

### 8.2 锁定版本（推荐生产）

```nix
inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
```

### 8.3 垃圾回收

```bash
sudo nix-collect-garbage -d
sudo nix store optimise
```

---

## 总结：你只需要

1. 创建 `flake.nix` + `home.nix`
2. 把 `users.users.syaofox.packages` 移到 `home.nix`
3. `sudo nixos-rebuild switch --flake .#nixos`

---

**一键复制粘贴版**（直接用）

```bash
sudo mkdir -p /nixos-config
sudo cp -r /etc/nixos/* /nixos-config/
cd /nixos-config
```

然后贴入上面 `flake.nix` 和 `home.nix`，修改 `configuration.nix` 删掉 `packages`，最后：

```bash
sudo nixos-rebuild switch --flake .#nixos
```

---

搞定！以后你就是 **Flakes + Home-Manager** 专业选手了  


