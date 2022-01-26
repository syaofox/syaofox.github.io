---
title: "windows上powershell脚本文件运行权限的问题"
date: 2022-01-22T10:59:57+08:00
description: ""
image: ""
categories: [Tips]
tags: [windows,vscode]
draft: false
---


## 问题描述

我在某个项目里使用了pipenv虚拟环境，当我在VS Code中右键该项目的文件-在集成终端中打开，就会爆出下面的错误 - `& : 无法加载文件 C:\Users\Kearney\.virtualenvs\fb-xzc3iOtr\Scripts\Activate.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅 https:/go.micros oft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。`  

![](v2-111911d588d094c155f5f8d4029a66e2_r.jpg)

  

## 解决办法

在[PowerShell：因为在此系统上禁止运行脚本，解决方法 - sinler](https://www.jianshu.com/p/4eaad2163567)中可以知道问题的根源在于win10默认的执行策略是**不载入任何配置文件，不运行任何脚本**。这一点可以通过命令行查看

## 查看当前执行策略

在控制台敲入命令`get-executionpolicy`回车即可，默认是Restricted

```shell
> get-executionpolicy
Restricted
```

可以加上参数`-Scope CurrentUser`表示当前用户，默认是本机

### 参数详解

> – Restricted: 不载入任何配置文件，不运行任何脚本。 “Restricted” 是默认的。  
> – AllSigned: 只有被Trusted publisher签名的脚本或者配置文件才能使用，包括你自己再本地写的脚本。  
> – RemoteSigned: 对于从Internet上下载的脚本或者配置文件，只有被Trusted，publisher签名的才能使用。  
> – Unrestricted: 可以载入所有配置文件，可以运行所有脚本文件. 如果你运行一个从internet下载并且没有签名的脚本，在运行之前，你会被提示需要一定的权限。  
> – Bypass: 所有东西都可以使用，并且没有提示和警告。  
> – Undefined: 删除当前scope被赋予的ExecutionPolicy，但是Group Policy scope的Execution Policy不会被删除。  

## 修改执行策略

.涉及到注册表问题，这里必须“以管理员身份运行”选项启动 **Windows PowerShell**

### 格式：

*   `Set-ExecutionPolicy 参数`：设置全局执行策略为参数
*   `Set-ExecutionPolicy 参数 -Scope CurrentUser`：设置当前用户执行策略为参数  
    例子

```shell
> Set-ExecutionPolicy  AllSigned
> Set-ExecutionPolicy -Scope CurrentUser Unrestricted
```

### 解决办法

实践表明，仅设置当前用户的执行策略不需要管理员身份的powershell，在vs code的集成终端就能解决

```shell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

实践表明：AllSigned参数不能解决问题，RemoteSigned才解决了这个问题，带来的好处就是省掉了每次进入环境都需要敲一次pipenv shell.