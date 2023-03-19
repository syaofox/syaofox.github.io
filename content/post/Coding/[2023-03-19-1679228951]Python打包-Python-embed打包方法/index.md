---
title: "【Python打包】Python embed打包方法"
date: 2023-03-19 20:29:11+08:00
draft: false
categories: [Coding]
tags: [embedded]
---


## 0\. 相关内容

### 0.1. 本文环境

win10+python3.10.4 64bit

### 0.2. python embed打包相关

**python embed是什么？**最小python环境

**为什么这样打包？**打出的包体积非常小

### 0.3. 本文相较于类似内容文章的区别

类似文章的问题 （类似文章链接见文尾）

*   使用get-pip.py 使embed环境变大
*   pythonXX.\_pth 处理不当 无法正常导入第三方库

## 1\. 准备一段代码

```plain
# main.py
import requests
import orjson

resp = requests.get("https://wallhaven.cc/api/v1/w/dgmj6m")
img_url = orjson.loads(resp.content)["data"]["path"]

with open("download.png", "wb") as f:
    resp = requests.get(img_url)
    f.write(resp.content)
```

* * *

## 2\. 下载 Python Embed版本

### 2.1 查看 Python 版本

打开 cmd/powershell 执行以下命令 查看版本和位数

`python -c "import sys;print(sys.version)"`

```text
(env) PS D:\python_embed_blog> python -c "import sys;print(sys.version)"
3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)]
```

### 2.2 下载对应版本的 Embed

**A. 国内镜像 (推荐)**

[华为源(点我跳转)](https://link.zhihu.com/?target=https%3A//mirrors.huaweicloud.com/python/) 找到你需要的版本

[https://mirrors.huaweicloud.com/python/3.10.4/](https://link.zhihu.com/?target=https%3A//mirrors.huaweicloud.com/python/3.10.4/)

按对应位数下载包

| 位数 | 包 |
| --- | --- |
| 64 | python-3.10.4-embed-amd64.zip |
| 32 | python-3.10.4-embed-win32.zip |

**B. 官方源**

在 [downloads(点我跳转)](https://link.zhihu.com/?target=https%3A//www.python.org/downloads/) 页面找到需要的版本

[https://www.python.org/downloads/release/python-3104/](https://link.zhihu.com/?target=https%3A//www.python.org/downloads/release/python-3104/)

滑倒页面底部

下载对应的包

| 位数 | 包 |
| --- | --- |
| 64 | Windows embeddable package (64-bit) |
| 32 | Windows embeddable package (32-bit) |

* * *

## 3\. 开始打包

### 3.1 解压

考虑以下文件夹结构

```text
你的工作目录
|   main.py
|   python-3.10.4-embed-amd64.zip
|
\---python-3.10.4-embed-amd64
        python.exe
        python310._pth # 文件名取决于python版本
        ... # 省略其他embed文件
```

### 3.2 删除 `pythonXX._pth`

`XX` 取决于你的python版本

如 `python310._pth`

目的: 使embed版本正常导入第三方库

参考: [关于\_pth文件的官方文档](https://link.zhihu.com/?target=https%3A//docs.python.org/zh-cn/3/using/windows.html%23finding-modules)

### 3.3 安装第三方库

> ⚠注意⚠：本节所说的pip是指你系统/虚拟环境中的pip  
> 而不是embed+[get-pip.py](https://link.zhihu.com/?target=https%3A//bootstrap.pypa.io/pip/get-pip.py)得到的pip  
> 正确举例: D:\\python\\3.10.4\\Scripts\\pip.exe

**创建 `Lib\site-packages` 目录**

目的: 存放第三方库

```text
你的工作目录
\---python-3.10.4-embed-amd64  
    \---Lib
        \---site-packages
```

**安装pipreqs**

目的: 快速提取出项目的依赖

```text
pip install pipreqs
```

**执行pipreqs**

```text
(env) PS D:\> pipreqs . --encoding=utf-8
INFO: Successfully saved requirements file in .\requirements.txt
```

文件树 会多出 `requirements.txt`

```text
你的工作目录
|   main.py
|   python-3.10.4-embed-amd64.zip
|   requirements.txt
|
\---python-3.10.4-embed-amd64
```

文件包含了所有依赖

```text
# requirements.txt
orjson==3.7.12
requests==2.28.1
```

**安装依赖到embed**

```text
pip install -r requirements.txt -t python-3.10.4-embed-amd64\Lib\site-packages
```

`-t` 作用: 将依赖安装到指定目录

### 3.4 编写启动器

创建 `start.bat`

```text
@echo off
python-3.10.4-embed-amd64\python.exe main.py
```

文件树

```text
你的工作目录
|   download.png
|   main.py
|   python-3.10.4-embed-amd64.zip
|   requirements.txt
|   start.bat
|
\---python-3.10.4-embed-amd64
```

## 4\. 测试

执行

```text
(env) PS D:\> .\start.bat
```

如果没有报错

你会看到一个 `download.png` 文件


## 恭喜！打包成功

### 如何分发？

只需要保留以下文件

```text
你的工作目录
|   main.py # 主程序
|   start.bat # 启动器
|
\---python-3.10.4-embed-amd64 #embed python
```

使用 7zip/winrar 等软件打包整个目录

**直接分发压缩包即可**


> 类似内容的文章: [python embeded，一种很好的pyinstaller的代替方式](https://link.zhihu.com/?target=https%3A//www.bilibili.com/read/cv14125166/)[https://www.jianshu.com/p/8bd34d13415e](https://link.zhihu.com/?target=https%3A//www.jianshu.com/p/8bd34d13415e)  
> [CodingDog：pyinstaller打包的exe太大？你需要嵌入式python玄学 惊喜篇](https://zhuanlan.zhihu.com/p/77028265)  
