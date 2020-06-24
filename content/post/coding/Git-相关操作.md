---
title: "Git 相关操作"
date: 2020-06-18T08:58:45+08:00
description: ""
tags: [Git]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Coding 
comment : false
draft: false 
author: "syaofox"
type: post
---

## git仓库

- 本地文件
- 缓存区（ `git add` 命令可以添加项目到缓存区）
- 本地仓库（ `git commit` 可以添加到本地仓库）
- 远程仓库( `git push` 将本地仓库文件推送到远程仓库)

## 初始化git项目并且提交

- `git init`
- `echo '# project name' >> README.md` // 写入内容
- `git add README.md` 或 `git add .` 增加文件进行跟踪
- `git commit -m "commmit info"`
- `git push orgin master`

------

## 本地有修改，与远程有冲突

- `git stash` 备份本地文件
- `git pull origin master` 拉取远程文件
- `git stash pop` 推出备份文件，解决冲突

------

## 删除远程分支上的文件夹，但是保留本地分支的文件夹

- `git rm <delete file path>` 需要删除暂存区或分支上的文件, 同时工作区也不需要这个文件了
- `git rm --cached -r <delete folder path>` 需要删除暂存区或分支上的文件, 但不希望工作区删除这个文件
- `git commit -m 'delete folder'`
- `git push orgin master`

------

## 拉取

- `git fetch` 用户将远程最新内容拉取到本地，用户检查了是否要合并到本地工作分支中
- `git pull` 用户将远程内容拉取到本地，并且强制合并，相当于 `git fetch` + `git merge`
- `git fetch <远程主机名> <分支名>`
- `git pull <远程主机名> <远程分支名>:<本地分支名>` 从远程分支拉取内容到本地分支

## 分支相关操作

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

## 常用命令

- `git status` 查看当前 git 状态（有几个文件修改，有几个新增）
- `git diff` 查看所有文件被修改的地方
- `git checkout [filepath]` 拉取删除本地被删除的具体文件
- `git remote -v` 查看远程版本
- `git merge <分支名>` 将指定分支内容合并到当前分支
- `ssh-keygen -p` 删除ssh密码
- `git reset [filename]` 撤销添加文件操作，如果跟文件名那么撤销此文件，如果不跟文件名那么撤销全部

## 简化符对应关系

- `-d => --delete` 删除
- `-D => --delete --force` 强制删除
- `-f => --force` 强制
- `-m => --move` 移动或重命名
- `-M => --move --force` 强制 移动或重命名
- `-r => --remote` 远程
- `-a => --all` 所有