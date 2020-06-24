---
title: "Windows10 配置 FTP"
date: 2020-06-18T10:14:12+08:00
description: ""
tags: [Windows10, FTP]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---
1. 控制面板 > 程序 > 启用或关闭 Windows 功能 > …  

   控制面板可在 桌面右键>个性化>主题>桌面图标设置>勾选控制面板>确定

   ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-291b7fa89ad00c04312aec5ba5d85429.jpg)

2. 小娜搜索 IIS 打开 IIS 
  
   ![小娜搜索IIS打开IIS](/Win10开启FTP与配置/1589731070-ed7c5087487e1757f8158d40dda91050.jpg)  

3. 右击网站添加 FTP 站点  

   ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-7154999f157a09336c95a865ed16f9c1.jpg)

4. 输入站点名称和作为 FTP 的目录 
 
   ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-284d6c123085fa7f00043ee4aebae493.jpg)

5. IP 地址填 FTP 本机 IP，选择无 SSL 
    
    ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-c65e09198d0ef1ebb0b6ce4c9ece61f1.jpg)  

6. 根据需要选择身份验证，授权与权限  

    ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-179f3cd66c8fd595fc45c884ba71eb5d.jpg)  

7. 控制面板 > 系统和安全 > 防火墙 > 允许应用或功能通过 Window 防火墙 > …  

    ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-a295876d3ec467758ea7fa887df8f822.jpg)  

8. 点击更改设置，勾选 FTP 服务器&专用&公用  

    ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-299e3449b292a1059153f33442a17041.jpg) 

9. 点击允许其它应用,选择C:\\Windows\\System32\\svchost.exe然后添加，最后确定。 
     
    ![Windows10 配置 FTP](/Win10开启FTP与配置/1589731070-e68a243e5e4106efd3bbe261726b8830.jpg)  

10.  资源处理器访问ftp:// IP 试试吧！