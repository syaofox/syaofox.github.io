---
title: "使用GitHub（二）：配置并使用Git创建版本库"
date: 2020-06-18T09:12:27+08:00
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

# 前言

> - 本文简单介绍使用GitHub对代码进行版本控制，包括**添加SSHkey**、**配置Git**、**使用Git创建版本库**并在GitHub上进行管理，主要目的是对学习内容进行总结以及方便日后查阅。

------

## 配置Git

------

```
    git config --global user.name 你的英文名
    git config --global user.email 你的邮箱
    git config --global push.default matching
    git config --global core.quotepath false
    git config --global core.editor "vim"
```

五句话，依次运行。

## 使用Git创建版本库

------

使用 git 有三种方式，请按照需求选择。

1. 只在本地使用
2. 将本地仓库上传到 GitHub
3. 下载 GitHub 上的仓库

> 其中1+2的最终效果=3

### 1只在本地使用

------

#### 1.1 初始化

1. 创建目录作为我们的项目目录：`mkdir git-demo-1`

2. 进入目录 `cd git-demo-1`

3. `git init`，这句命令会在 `git-demo-1` 里创建一个 `.git` 目录

4. `ls -la` 你就会看到 `.git`目录，它就是一个「仓库」，不要进去看。

5. 在 `git-demo-1`目录里面添加任意文件，假设我们添加了两个文件，分别是 `index.html` 和 `css/style.css`

   ```
   touch index.html
   mkdir css
   touch css/style.css
   ```

6. 运行 `git status -sb` 可以看到文件前面有 `??` 号

   ```
       touch index.html
       mkdir css
       touch css/style.css
   ```

这个 `??` 表示 git不知道你要怎么对待这些变动。

1. 使用 `git add` 将文件添加到「暂存区」

2. 你可以一个一个地 add

   ```
       git add index.html
       git add css/style.css
   ```

3. 你也可以一次性 add

   ```
   git add .
   ```

意思是把当前目录（.表示当前目录）里面的变动都加到「暂存区」

1. 再次运行 `git status -sb`，可以看到 `??` 变成了 A

```
## Initial commit on master
A  css/style.css
A  index.html
```

A 的意思就是添加，也就是说你告诉 git，这些文件我要加到仓库里

1. 使用 `git commit -m "信息"` 将你 add过的内容「正式提交」到本地仓库（`.git`就是本地仓库），并添加一些注释信息，方便日后查阅
2. 你可以一个一个地 commit

```
git add index.html
git add css/style.css
```

1. 你也可以一次性 commit

   ```
   git commit . -m "添加了几个文件"
   ```

   1. 再再次运行 `git status -sb`，发现没有文件变动了，这是因为文件的变动已经记录在仓库里了。
   2. 这时你使用 `git log` 就可以看到历史上的变动：

```
commit f0d95058cd32a332b98967f6c0a701c64a00810a
 Author: frankfang <frankfang1990@gmail.com>
 Date:   Thu Sep 28 22:30:43 2017 +0800

添加几个文件
```

1. 以上就是 `git add` / `git commit` 的一次完整过程。

#### 1.2 文件变动

如果我想继续改文件，应该怎么做呢？

1. `start css/style.css` 会使用默认的编辑器打开 `css/style.css`（macOS 上对应的命令是 `open css/style.css`）
2. 然后我们在 `css/style.css` 里写入 `body {background: red}`，保存退出
3. 运行 `git status -sb` 发现提示中有一个 `M`

```
## master
M css/style.css
```

这个 `M` 的意思就是 Modified，表示这个文件被修改了

1. 此时你如果想让改动保存到仓库里，你需要先 `git add css/style.css` 或者也可以 `git add .`

   > 注意
   >
   > ：由于这个
   >
   >  
   >
   > ```
   > css/style.css
   > ```
   >
   >  
   >
   > 以前被我们 add 过，你往文章上面看，我们是 add 过
   >
   >  
   >
   > ```
   > css/style.css
   > ```
   >
   > 的，所以此处的 git add操作可以省略，但我建议你使用 git 的前一个月，不要省略 git add。
   >
   > 换句话说，每一次改动，都要经过 `git add` 和 `git commit` 两个命令，才能被添加到 .git 本地仓库里。

2. 再次运行 `git status -sb` 发现 M 有红色变成了绿色。

3. 运行 git commit -m` "更新 css/style.css"，这个改动就被提交到 .git 本地仓库了。再说一次，不要去 .git 目录里面。

4. 再再次运行 `git status -sb`，会发现没有变更了，这说明所有变动都被本地仓库记录在案了。

> **`git status -sb` 是什么意思：**
> `git status` 是用来显示当前的文件状态的，哪个文件变动了，方便你进行 `git add` 操作。
>
> - `-s` 的意思是显示总结（summary）
> - `-b` 的意思是显示分支（branch）
> - 所以 `-sb` 的意思是显示总结和分支。

#### 1.3 总结

至此，我们来总结一下用到的命令

1. `git init`，初始化本地仓库 `.git`

2. `git status -sb`，显示当前所有文件的状态

3. `git add 文件路径`，用来将变动加到暂存区

4. `git commit -m "信息"`，用来正式提交变动，提交至 `.git` 仓库

5. 如果有新的变动，我们只需要依次执行 `git add xxx` 和 `git commit -m 'xxx'` 两个命令即可。

   > 别看本教程废话那么多，其实就这一句有用！先 add 再 commit，行了，你学会 git 了。

6. `git log` 查看变更历史

### 2 将本地仓库上传到 GitHub

------

如何将我们这个 git-demo-1 上传到 GitHub 呢？

1. 在 GitHub 上新建一个空仓库，名称随意，一般可以跟本地目录名一致，也叫做

    

   ```
   git-demo-1
   ```

   ![建立空仓库](/使用GitHub二配置并使用Git创建版本库/1460000013760572.jpg)

   按照截图所示，除了仓库名，**其他的什么都别改**，这样你才能创建一个**空仓库**

2. 点击创建按钮之后，GitHub 就会把后续的操作全告诉你，如图

   请点击一下 ssh

   ![点击SSH](/使用GitHub二配置并使用Git创建版本库/1460000014076777.jpg)
   ![点击SSH2](/使用GitHub二配置并使用Git创建版本库/1460000014076778.jpg)

3. **点击一下 ssh**，你就会使用默认的 HTTPS 地址。但是千万不要使用 HTTPS 地址，因为 HTTPS地址使用起来特别麻烦，每次都要输入密码，而 SSH 不用输入用户名密码。

   > 为什么 SSH 不用密码呢，因为你已经上传了 SSH public key。详情请看上一篇博文使用GitHub（一）

4. 由于我们已经有本地仓库了，所以图中**下面半部分**就是你需要的命令，我们一行一行拷贝过来执行

   - 再次点击 SSH 按钮
   - 命令 `git remote add origin git@github.com:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/git-demo-1.git`，复制并运行它
   - 复制第二行 `git push -u origin master`，运行它
   - 刷新当前页面，你的仓库就上传到 GitHub 了.

> 在建立空库的情况下，以上两步在本地建一个Git仓库和将Git仓库上传到GitHub上加起来就等同于下面的第3条。

### 3 直接在 GitHub 创建一个仓库，然后下载到本地

------

> 上面两步讲了
>
> - 在本地创建仓库
> - 将本地仓库上传到 GitHub
>
> 这里讲第三种用法，那就是直接在 GitHub 创建一个仓库，然后下载到本地

1. 在GitHub 上新建一个仓库`git-demo-2`，这次就不创建空仓库了，而是自带 `README` 和 `Lisence` 的仓库，创建截图如下：

![创建新的仓库](/使用GitHub二配置并使用Git创建版本库/1460000013760573.jpg)
然后点击创建按钮。

1. 这样一来，这个仓库就会自动拥有三个文件：

![仓库文件](/使用GitHub二配置并使用Git创建版本库/1460000013760574.jpg)

1. 使用 `git clone` 命令下载到本地
2. 点击页面中唯一的绿色按钮「clone or download」，会看到一个弹出层

![clone](/使用GitHub二配置并使用Git创建版本库/1460000013760575.jpg)

```
> 请确保弹出层里的地址是 SSH 地址，也就是 git@github.com 开头的地址，如果不是，就点击 Use SSH 按钮，就**点击
> Use SSH 按钮**。然后复制这个地址。
```

1. 打开 Git Bash，找一个安全的目录，比如 `~/Desktop` 。

运行 `git clone 你刚才得到的以git@github.com开头的地址`，运行完了你就会发现，桌面上多出一个 `git-demo-2`。

1. `cd git-demo-2`进入这个目录。
2. 运行 ls -la 你会看到，远程目录的所有文件都在这里出现了，另外你还看到了 `.git` 本地仓库。这时你就可以添加文件，git add，然后 git commit 了。

> 三种方式都说完了，它们分别是：
>
> - 在本地创建仓库
> - 将本地仓库上传到 GitHub
> - 下载 GitHub 上的仓库到本地
>
> 其实呢，还有很多种不同的方式，但是，记住这几种就行了，够用了。我们并不想要了解 git 的所有高级用法，我们的目的很明确：能通过 Git
> 命令使用 GitHub 就行

**总结：**

回顾一遍已经学到的命令：（这次只多了一个 git clone 命令）

- `git clone git@github.com:xxxx`，下载仓库

- `git init`，初始化本地仓库 .git

- `git status -sb`，显示当前所有文件的状态

- `git add 文件路径`，用来将变动加到暂存区

- `git commit -m "信息"`，用来正式提交变动，提交至 .git 仓库

- 如果有新的变动，我们只需要依次执行 `git add xxx` 和 `git commit -m 'xxx'` 两个命令即可。

  > 别看本教程废话那么多，其实就这一句有用！先 add 再 commit，行了，学会 git 了。

- `git log` 查看变更历史

## 如何上传更新

你在本地目录有任何变动，只需按照以下顺序就能上传：

```
git add 文件路径
git commit -m "信息"
git pull  （一定不要忘记这一个命令）
git push
```

> 为何要push之前要pull？
> **push是推送**，**pull是拉取**的意思。假如你在远端修改了文件，然后本地并没有同步更新，这时候你push的时候就会出现错误，因为两端不同步了。多人合作的时候这种问题就会出现的更多，所以现在养成push之前要pull的习惯。

下面是例子

```
cd git-demo-1
touch index2.html
git add index2.html
git commit -m "新建 index2.html"
git pull
git push
```

然后去 `git-demo-1` 的 GitHub 页面，就能看到 `index2.html` 出现在里面了。