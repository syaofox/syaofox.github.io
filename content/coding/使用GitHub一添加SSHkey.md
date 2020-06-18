---
title: "使用GitHub（一）：添加SSHkey"
date: 2020-06-18T09:01:14+08:00
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

> - 本文简单介绍使用GitHub对代码进行版本控制，包括**添加SSHkey**、**配置Git**、**使用Git创建版本库**并在GitHub上进行管理，主要目的是对学习内容进行总结以及方便日后查阅。


## 前言

- 简单说，SSH是一种**网络协议**，用于计算机之间的**加密登录**。
- 如果一个用户从本地计算机，**使用SSH**协议登录另一台远程计算机，我们就可以认为，这种登录是**安全**的，即使被中途截获，密码也不会泄露。
- 最早的时候，互联网通信都是明文通信，一旦被截获，内容就暴露无疑。1995年，芬兰学者TatuYlonen设计了SSH协议，将**登录信息全部加密**，成为互联网安全的一个基本解决方案，迅速在全世界获得推广，目前已经成为Linux系统的标准配置。
- 在这里你只需要知道使用GitHub之前需要添加SSHkey，用来验证GitHub远程仓库就可以了，如果想深入了解原理，参考[阮一峰SSH原理](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html)。

## 步骤：

1. 进入 https://github.com/settings/keys
2. 如果页面里已经有一些 key，就点「delete」按钮把这些 key 全删掉。如果没有，就往下看

    ![参考示例](/使用GitHub一添加SSHkey/4282016414-5aaa2f527f39b_articlex.jpg)

1. 点击 New SSH key，你需要输入 Title 和 Key，但是你现在没有 key，往下看

   > 添加步骤参考[这里](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

2. 打开 Git Bash

3. 复制并运行 `rm -rf ~/.ssh/*` 把现有的 ssh key都删掉，这句命令行如果你多打一个空格，可能就要重装系统了，建议复制运行。

4. 运行 `ssh-keygen -t rsa -b 4096 -C "你的邮箱"`，注意填写你的真实邮箱。

5. 按回车三次

    参考示例：

    ![参考示例](/使用GitHub一添加SSHkey/1460000013759213.jpg)

    这时会在~目录下生成一个.ssh的隐藏文件!

    [参考示例2](/使用GitHub一添加SSHkey/1460000013759214.jpg)

1. 运行 `cat ~/.ssh/id_rsa.pub`，得到一串东西，完整的复制这串东西
2. 回到上面第 3 步的页面，在 Title 输入「我的第一个 key」
3. 在 Key 里粘贴刚刚你你复制的那串东西

    ![复制key](/使用GitHub一添加SSHkey/1460000013759215.jpg)

1. 点击 Add SSH key
2. 回到 Git Bash
3. 运行 `ssh -T git@github.com`，你可能会看到这样的提示：

    ![提示](/使用GitHub一添加SSHkey/1460000013759216.jpg)

1. 输入 `yes` 回车
2. 然后如果你看到 `Permission denied (publickey).` 就说明你失败了，请回到第 1 步重来，是的，回到第 1步重来；如果你看到 `Hi FrankFang! You've successfully authenticated, but GitHub does not provide shell access.`

    ![成功示例](/使用GitHub一添加SSHkey/1460000013759217.jpg)

    就说明你成功了！

    1. 好了， 添加了一SSH key，接下来就会用到它。

    > - 一台电脑只需要一个 SSH key
    > - 一个 SSH key 可以访问你的所有仓库，即使你有 1000000 个仓库，都没问题
    > - 如果你新买了电脑，就在新电脑上重新生成一个 SSH key，把这个 key 也上传到 GitHub，它可以和之前的 key 共存在 GitHub 上
    > - 如果你把 key 从电脑上删除了，重新生成一个 key 即可，替换之前的 key