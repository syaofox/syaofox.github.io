---
title: "使用git和github"
date: 2021-12-20T14:25:16+08:00
description: ""
image: ""
categories: [Tips]
tags: [git,gitHub]
---

## 一、配置本地Git与Github

### 1.1 配置本地Git全局信息

```sh
git config --global user.name "syaofox"
git config --global user.email "syaofox@gmail.com"
#pull 默认合并
git config --global pull.rebase false
#设置大小写敏感
git config --global core.ignorecase false 
```

### 1.2 创建ssh密钥

```sh
ssh-keygen -t rsa -b 4096 -C "syaofox@gmail.com"
```

会在本地家目录的.ssh目录下生成密钥

### 1.3 配置Github

- 打开 https://github.com/settings/keys

- 添加SSHKey

- 取个名字，填入'~/.ssh/id_rsa.pub`内容

- 执行`ssh -T git@github.com`测试

## 二、Git常用操作

### 2.1 git仓库

- 本地文件
- 缓存区（ `git add` 命令可以添加项目到缓存区）
- 本地仓库（ `git commit` 可以添加到本地仓库）
- 远程仓库( `git push` 将本地仓库文件推送到远程仓库)

### 2.2 初始化git项目并且提交

- `git init`
- `echo '# project name' >> README.md` // 写入内容
- `git add README.md` 或 `git add .` 增加文件进行跟踪
- `git commit -m "commmit info"`
- `git push orgin master`

------

### 2.3 本地有修改，与远程有冲突

- `git stash` 备份本地文件
- `git pull origin master` 拉取远程文件
- `git stash pop` 推出备份文件，解决冲突

------

### 2.4 删除远程分支上的文件夹，但是保留本地分支的文件夹

- `git rm <delete file path>` 需要删除暂存区或分支上的文件, 同时工作区也不需要这个文件了
- `git rm --cached -r <delete folder path>` 需要删除暂存区或分支上的文件, 但不希望工作区删除这个文件
- `git commit -m 'delete folder'`
- `git push orgin master`

------

### 2.5 拉取

- `git fetch` 用户将远程最新内容拉取到本地，用户检查了是否要合并到本地工作分支中
- `git pull` 用户将远程内容拉取到本地，并且强制合并，相当于 `git fetch` + `git merge`
- `git fetch <远程主机名> <分支名>`
- `git pull <远程主机名> <远程分支名>:<本地分支名>` 从远程分支拉取内容到本地分支

### 2.6 分支相关操作

- `git branch` 查看本地所有分支
- `git branch -r` 查看远程所有分支
- `git branch -a` 查看本地和远程的所有分支
- `git branch <branchname>` 新建分支
- `git checkout newBranch` 切换到你的新分支
- `git checkout -b newBranch` 创建并切换到新分支
- `git push origin newBranch` 将新分支发布在github上
- `git branch -d <branchname>` 删除本地分支
- `git push origin :newBranch` 在github远程端删除一个分支 (分支名前的冒号代表删除)
- `git branch -m <oldbranch> <newbranch>` 重命名本地分支

### 2.7 常用命令

- `git status` 查看当前 git 状态（有几个文件修改，有几个新增）
- `git diff` 查看所有文件被修改的地方
- `git checkout [filepath]` 拉取删除本地被删除的具体文件
- `git remote -v` 查看远程版本
- `git merge <分支名>` 将指定分支内容合并到当前分支
- `ssh-keygen -p` 删除ssh密码
- `git reset [filename]` 撤销添加文件操作，如果跟文件名那么撤销此文件，如果不跟文件名那么撤销全部

### 2.8 简化符对应关系

- `-d => --delete` 删除
- `-D => --delete --force` 强制删除
- `-f => --force` 强制
- `-m => --move` 移动或重命名
- `-M => --move --force` 强制 移动或重命名
- `-r => --remote` 远程
- `-a => --all` 所有

### 2.9 回退到指定版本

可以回退到任意已经提交过的版本。已 add / commit 但未 push 的文件也适用。

命令如下：

```bash
git reset --hard [commit-hashcode]  
# [commit-hashcode]是某个 commit 的哈希值，可以用 git log 查看
```
因此一般用法是先用 `git log` 查看具体`commit`的哈希值，然后 `reset` 到那个版本。

###  2.10 删除未跟踪文件

`git clean` 命令支持以下参数：

```bash
git clean [-d] [-f] [-i] [-n] [-q] [-e ] [-x | -X] [--] ...
```

其中几个主要参数用法如下：

```bash
-d   # 删除未跟踪目录以及目录下的文件，如果目录下包含其他git仓库文件，并不会删除（-dff可以删除）。
-f   # 如果 git cofig 下的 clean.requireForce 为true，那么clean操作需要-f(--force)来强制执行。
-i   # 进入交互模式
-n   # 查看将要被删除的文件，并不实际删除文件
```
通过以上几根参数组合，基本上可以满足删除未跟踪文件的需求了。例如在删除前先查看有哪些文件将被删除运行：

```bash
git clean -n
```
想删除当前工作目录下的未跟踪文件，但不删除文件夹运行（如果 `clean.requireForce` 为 `false` 可以不加 `-f` 选项）：

```bash
git clean -f
```
想删除当前工作目录下的未跟踪文件以及文件夹运行：

```bash
git clean -df
```

## 三、子模块Git Submodule

### 3.1 添加子模块

克隆到本地，子模块信息保存到本地`.gitmodules`

```sh
git submodule add 仓库地址 本地文件夹
```

### 3.2 查看子模块

```sh
git submodule
```

### 3.3 更新子模块

```sh
git submodule update # 更新项目内子模块到最新版本
git submodule update --remote # 更新子模块为远程项目的最新版本
```

### 3.4 克隆包含子模块的项目

```sh
# 方法一

# 克隆父项目
git clone 父项目地址 本地文件夹

# 查看子模块
git submodule

# 初始化子模块
git submodule init

# 更新子模块
git submodule update

# 方法二
# 递归克隆，一步到位
git clone 父项目地址 本地文件夹 --recursive 
```

### 3.5 删除子模块

```sh
# 逆初始化模块，其中{MOD_NAME}为模块目录，执行后可发现模块目录被清空
git submodule deinit {MOD_NAME} 

# 删除.gitmodules中记录的模块信息（--cached选项清除.git/modules中的缓存）
git rm --cached {MOD_NAME} 

# 提交更改到代码库，可观察到'.gitmodules'内容发生变更
git commit -am "Remove a submodule."
```

此外，你可能还需要删除` .git/modules/{MOD_NAME}`的缓存，否则无法创建同名的module.

### 3.6 修改模块URL

- 修改'.gitmodules'文件中对应模块的”url“属性;

- 使用 `git submodule sync `命令，将新的URL更新到文件`.git/config`；
    ```sh
    git submodule sync 
    
    # 运行后可观察到'.git/config'中对应模块的url属性被更新
    git commit -am "Update submodule url." # 提交变更
    ```
    
    *PS: 本实验使用git 2.7.4 完成，较低版本git可能不能自动更新`.git/config`文件，需要修修改完".gitmodule"文件后手动修改`.git/config`.*
