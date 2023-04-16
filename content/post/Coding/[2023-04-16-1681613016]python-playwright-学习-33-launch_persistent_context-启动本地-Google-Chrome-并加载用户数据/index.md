---
title: "python+playwright 学习-33.launch_persistent_context 启动本地 Google Chrome 并加载用户数据"
date: 2023-04-16 10:43:36+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

playwright 启动Google Chrome 浏览器的时候默认用的是无痕模式，不加载本地的数据，这对于测试人员运行一个干净的浏览器是没问题的。  
大家在学selenium的时候，知道 selenium 可以启动本地的 Google Chrome 浏览器并加载本地数据，这样可以在本地已经登录过网站的情况下，下次打开网站不需要登录继续操作，对于一些爬虫用户是非常重要的功能。  
playwright 可以使用launch\_persistent\_context方法启动本地的chrome 浏览器

# selenium 加载 Google Chrome 插件

在启动浏览器的时候添加`--user-data-dir` 用户数据目录，即可启动带插件的浏览器，并且会记住用户的cookies数据

```python
from selenium import webdriver
import getpass
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


# 启用带插件的浏览器
option = webdriver.ChromeOptions()
option.add_argument(f"--user-data-dir=C:\\Users\\{getpass.getuser()}\\AppData\Local\Google\Chrome\\User Data")
driver = webdriver.Chrome(chrome_options=option)   # 打开chrome浏览器
driver.get("https://www.cnblogs.com/yoyoketang/")
```

# playwright 启动本地 Google Chrome

使用 launch\_persistent\_context 方法启动本地的chrome 浏览器，并且设置 `channel="chrome"`

```python
import getpass
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


# 获取 google chrome 的本地缓存文件
USER_DIR_PATH = f"C:\\Users\\{getpass.getuser()}\\AppData\Local\Google\Chrome\\User Data"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
                        # 指定本机用户缓存地址
                        user_data_dir=USER_DIR_PATH,
                        # 接收下载事件
                        accept_downloads=True,
                        # 设置 GUI 模式
                        headless=False,
                        bypass_csp=True,
                        slow_mo=1000,
                        channel="chrome",

                    )

    page = browser.new_page()
    page.goto("https://www.cnblogs.com/yoyoketang")

    page.pause()
```

在运行的时候，先关闭本地的chrome 浏览器，再执行代码，就可以看到启动的浏览器，打开网站不需要登录了，但是插件并没有加载进去。

# 配置args 参数加载插件

Google Chrome 插件加载需配置args 参数， 所有的 args 参数列表可以在这个地址查询[https://peter.sh/experiments/chromium-command-line-switches/](https://peter.sh/experiments/chromium-command-line-switches/)  
![](assets/1681613016-5ed3c4dd729186512f8be781cbad34ba.png)

在使用脚本加载扩展插件时，一定要解压crx文件，不要直接安装crx

```python
import getpass
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

# 获取 google chrome 的本地缓存文件
USER_DIR_PATH = f"C:\\Users\\{getpass.getuser()}\\AppData\Local\Google\Chrome\\User Data"
# chrome.exe指定可执行文件路径
# executable_path = "chromium-111/chrome-win/chrome.exe"

# chrome插件目录，下载后解压crx
path_to_extension = f"\\Users\\Downloads\\extension\\xxx"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
                        # 指定本机用户缓存地址
                        user_data_dir=USER_DIR_PATH,
                        # executable_path=executable_path,  # 如果有需要可以下载chrome.exe到指定目录加载
                        # 接收下载事件
                        accept_downloads=True,
                        # 设置 GUI 模式
                        headless=False,
                        bypass_csp=True,
                        slow_mo=1000,
                        channel="chrome",
                        args=[
                            f"--disable-extensions-except={path_to_extension}",
                            f"--load-extension={path_to_extension}"
                        ],  # 加载扩展插件

                    )
```

**扩展程序仅在 Chrome / Chromium GUI模式中使用。**

# 使用代理

使用代理可以在launch\_persistent\_context 加上proxy 参数

```ini
proxy=ProxySettings(server="http://xxx.xxx.xxx.xxx:xxxx"),
```

  



