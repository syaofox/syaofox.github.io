---
title: "群晖中实现 Jellyfin 核心显卡硬解实时转码"
date: 2020-06-18T10:09:10+08:00
description: ""
tags: [群晖, Jellyfin, 硬解]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Tips
comment : false
draft: false 
author: "syaofox"
type: post
---

## 实时转码到底是干嘛用的

举个例子哈：大家在手机APP端看爱奇艺、优酷、QQ视频的时候。影片是可以选择清晰度的。一般有流畅、高清、蓝光等等选项。  
当然按照清晰度（分辨率）的不同，相应消耗的流量也不一样。

一般来说;极速＜流畅＜高清＜超清720P＜1080P蓝光

其实这些视频播放软件，在服务器中针对同一个视频分别存放了不通分辨率的版本。根据客户端的需求选择播放。来满足不同人群对视频源的需求。

在我们的群晖中。自带的套件Video Station 就有离线转码的功能。

DS video 客户端可让您执行离线转码以将视频转换到不同分辨率的 .mp4 格式，这是在移动设备上最兼容的视频格式。 离线转码启动后，Video Station 将开始转码视频以便可离线使用。完成离线转码后，DS video 将自动下载或在线播放转码视频供您欣赏。当然也会在我们的群晖中生成一份转码成功的视频文件。

## Jellyfin 的实时转码

Jellyfin 在客户端，或者网页端播放视频的时候，是支持选择码率的。比方说我们在手机客户端上选择群晖的某个视频进行播放的时候。默认为原始码率播放。若你的原始视频是1080P。则将会以1080P 60Mbps 进行播放。当然，如果你的网络足够流畅。家里的上传宽带足够大的话。原始码率能够带给你最高清晰度的体验。但如果，你是在外面播放家里群晖的视频的话。可能会受到两方面的限制：

*   家里的上传宽带无法达到原始码率的需求
*   原始码率播放非常消耗手机流量

这个时候，我们就需要Jellyfin 的实时转码功能啦。比方说我们可以选择 1080P 10Mbps 、或者选择720P 3Mbps来解决刚刚提到的两点问题。

## Jellyfin 实时转码消耗CPU资源

如果我们没有在Jellyfin的后台开启硬解的功能.我们的群晖将会使用CPU 来进行软解进行实时转码。在转码的过程中，CPU将会以接近100%的工作模式来帮助我们进行转码。对于CPU来说如此繁重的“体力劳动”可能会带来发热严重，群晖其他功能受到性能影响等等问题。

另外，一般我们群晖系统CPU中的核心显卡是没有用武之地的。所以，本教程将教会大家。如何利用CPU 的核心显卡进行硬解实时转码。

## Jellyfin核心显卡硬解实时转码的必要条件

*   群晖的系统版本需要：DS916+ 或 DS918+ (DS3617xs 、 DS3615xs不支持)
*   CPU 有核心显卡。当然集成的核心显卡越厉害越好
*   黑群晖、白群晖、全洗白群晖、半洗白群晖均可

> \[查看系统是否支持显卡硬解转码\]
> 
> SSH链接成功后。输入 ls /dev/dri 之后若如下图显示，则说明支持显卡硬解。  
> 输出 card0 renderD128

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-0c37741280c6962d0c6b5c026d74280f.jpg)

## 教程开始-搭建并运行Jellyfin容器

在[《群晖NAS-使用Jellyfin搭建媒体服务器》](https://www.izcv.com/2231.html)这篇教程中，已经教大家如何在群晖中搭建Jellyfin媒体服务器啦。  
今天的这篇教程中，我们将利用命令行的方式搭建。因为图形界面的搭建没法指定容器转载核心显卡的文件。

**1\. 在群晖的套件中心，安装Docker套件。**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-8e5ab1d8702568f32149802496834098.jpg)

**2\. Docker安装成功后，我们的file station中即可看到多出来一个Docker文件夹。 我们在此文件夹内建里 jellyfin 文件夹。再进入jellyfin文件夹。分别建里 config文件夹及cache文件夹。  
（分别为以后jellyfin的配置文件和缓存文件准备目录）**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-83a22b03b17428144a3efffca855a7c3.jpg)

**3\. 群晖系统中打开SSH功能 (控制面板->终端机和SNMP->启动SSH功能->应用)**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-93baa32fbdc09acbf1755803ebd169de.jpg)

**4\. 利用我们的管理员账号、密码通过ssh客户端登陆群晖系统。 通过 sudo su – 命令切换为root用户**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-507807c91878bb2c7ea663209aead984.jpg)

**5\. 运行以下命令：以管理员身份在Docker中下载jellyfin镜像**

```plain
sudo docker pull jellyfin/jellyfin
```

**6\. 运行以下命令：根据指定参数运行Jellyfin容器**

```plain
sudo docker run -d --name jellyfin \
-v /volume1/docker/jellyfin/config:/config \
-v /volume1/docker/jellyfin/cache:/cache \
-v /volume1/video:/video \
-p 8096:8096 \
-p 8920:8920 \
--device=/dev/dri/renderD128 \
--restart unless-stopped \
jellyfin/jellyfin
```

> -v 参数表示装载文件夹。所以第2-4行请根据实际情况更改。
> 
> 第2-3行指定卷1的两个文件夹分别作为配置文件和缓存文件地址  
> 第4行指定卷1下video文件夹为Jellyfin的媒体文件夹

**7\. 测试容器是否已经成功挂载device 下的驱动文件**

运行如下代码查看运行容器（Jellyfin）的ID：

```plain
docker ps
```

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-d0d227f767bc73f2fe275637939ebb47.jpg)

检查输出结果，若发现有如下图所示的字段则说明已经挂载成功。

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-84149eba561930d6f7d27a9847c3990e.jpg)

## 教程继续-配置Jellyfin设置

访问 http://你的内网ip:8096 即可初始化配置Jellyfin。配置媒体库等。

具体请参照 [《群晖NAS-使用Jellyfin搭建媒体服务器》](https://www.izcv.com/2231.html)这篇教程中的：【**二、Jellyfin配置部分】**，这里不再赘述

**Jellyfin 后台启用硬件转码功能 \[ 硬件加速选择：Video Acceleration API (VA API)(experimental) ，并勾选“启用硬件解码” \]**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-d33ff81f025ea5a4d406fbff7fcda1ef.jpg)

至此，搭建和配置结束。我们的手机端电脑端，可以实现实时硬解转码啦！

## **测试实时转码CPU占用率**

首先，我们测试一部1080P 电影。影片参数如下图：

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-bfe6aea28731aad6aff1faeea3038d5d.jpg)

### **开启硬件加速：**

**后台按照我们刚刚的设置。然后播放该视频，并选择转码为 1080P 10Mbps**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-71e8809b1fe19052f8e8e2bc3bc7d552.jpg)

**打开群晖分别查看 Docker容器，以及系统的CPU占用。**

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-bc359f2605be43de41b5ba20df9fdda4.jpg)

同时，我们链接群晖的SSH 通过 top 命令查看解码过程是否调用了显卡驱动：

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-34d6d316da12144ac8ef77ed6b67b52f.jpg)

### 关闭后台硬件加速功能。（硬件加速选择“没有”）

![](/群晖中实现Jellyfin核心显卡硬解实时转码/1570004742-1f5bb3c8f032e22f4e5a86aa58e3b59e.jpg)

可以明显看出，关闭硬件加速后。转码会非常消耗CPU资源。