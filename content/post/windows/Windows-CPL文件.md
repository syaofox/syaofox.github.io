---
title: "Windows CPL文件"
date: 2020-06-18T10:26:56+08:00
description: ""
tags: [CPL]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---

## 前言

CPL文件，又叫控制面板项（Control Panel Item），多保存于系统安装目录的 system32 文件夹下，它们分别对应着控制面板中的项目，普通用户的访问受到限制。它可由shell32.dll、control.exe打开。此外，你也可以直接在资源管理器中双击调用Open命令打开（实质上调用了shell32.dll）。

CPL文件本质是Windows可执行性文件，但不属于可以直接独立运行的文件，通常由shell32.dll打开。

system32目录里绝大多数cpl文件是Windows系统文件，具有“存档”文件属性，Windows操作系统的文件保护功能保护它们不被篡改。

## 打开方式

1、在开始->运行中直接输入文件名来启动相应的项目

例：输入main.cpl并点击确定

2、打开命令提示符，输入rundll32 shell32.dll,Control_RunDLL <文件名>

例：输入rundll32 shell32.dll,Control_RunDLL main.cpl并按下Enter

3、打开命名提示符，输入control <文件名>

例：输入control main.cpl并按下Enter

>注意：所有rundll32 shell32.dll,Control_RunDLL的命令均可用control替代，control.exe实质调用了rundll32.exe。打开后找不到control.exe进程，只能找到rundll32.exe。

例1：下列命令：

rundll32.exe shell32.dll,Control_RunDLL main.cpl,,3

可以被替代：

control.exe main.cpl,,3

例2：下列命令

rundll32.exe shell32.dll,Control_RunDLL

可以被替代：

control.exe

例3：下列命令

rundll32.exe shell32.dll,Control_RunDLL main.cpl

可以被替代：

control.exe main.cpl

## 文件及作用

inetcpl.cpl，IE设置

joy.cpl，游戏控制器设置

mmsys.cpl 声音与音频设置

intl.cpl，区域与语言设置

ncpa.cpl，网络连接

netsetup.cpl，网络安装向导

lusrmgr.cpl，用户帐户

odbccp32.cpl，ODBC数据源管理器

wscui.cpl，Windows安全中心

wuaucpl.cpl，自动更新配置

igfxcpl.cpl，Intel集成显卡设置

nvcpl.cpl，nVidia显卡设置(NVIDIA控制面板)

access.cpl，辅助功能选项

appwiz.cpl，添加或删除程序

desk.cpl，显示属性

firewall.cpl，防火墙设置

hdwwiz.cpl，添加硬件向导

sysdm.cpl 我的电脑右键属性

## 常见问题解决


1、有时，因系统问题，无法正常使用控制面板相关功能，或功能不全，可以在命令行的模式下操作，但仅仅输入上述有时可能无效，输入后提示：选择程序来打开该文件，解决方法：引起原因，该文件的默认打开程序被更改，需要重新指向：Control.exe 该程序文件在c:\windows\system32\目录下.更改后即可.

2、要在 Windows 中运行“控制面板”工具，请在“打开”对话框或命令提示符下键入适当的命令

>注意: 如果希望从命令提示符运行命令，必须在 Windows 文件夹下进行操作。同时，请注意您的计算机可能并没有本文中所列的所有工具，因为您的 Windows 安装可能没有包括所有这些组件。

>注意: “扫描仪与数字相机”程序 (sticpl.cpl) 无法在 Windows Millenium 中运行。该程序已经被“扫描仪与数字相机”文件夹取代，其功能与如“打印机”文件夹和“拨号网络”文件夹之类的文件夹类似。

3、运行“控制面板”中的“用户”工具，请键入 control Ncpa.cpl users，然后按 ENTER 键。

4、运行 Windows 95/98/ME 的“用户”工具，请键入“control inetcpl.cpl users”（不键入引号），然后按 ENTER 键。