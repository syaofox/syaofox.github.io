---
title: "python+playwright 学习-32 启动Google Chrome 或 Microsoft Edge浏览器"
date: 2023-04-16 10:43:26+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

playwright 默认会下载 chromium,firefox 和 webkit 三个浏览器，目前支持通过命令下载的浏览器有：chromium、chrome、chrome-beta、msedge、msedge-beta、msedge-dev、firefox、webkit

# 命令行下载

使用 `playwright install` 命令默认会安装chromium,firefox 和 webkit 三个浏览器。  
可以通过 `playwright -h` 命令查看目前支持的浏览器

```mipsasm
>playwright install --help
Usage: playwright install [options] [browser...]

ensure browsers necessary for this version of Playwright are installed

Options:
  --with-deps  install system dependencies for browsers
  --dry-run    do not execute installation, only print information
  --force      force reinstall of stable browser channels
  -h, --help   display help for command


Examples:
  - $ install
    Install default browsers.

  - $ install chrome firefox
    Install custom browsers, supports chromium, chrome, chrome-beta, msedge, msedge-beta, msedge-dev, firefox, webkit.
```

从命令行帮助信息中可以看到支持的浏览器有:chromium, chrome, chrome-beta, msedge, msedge-beta, msedge-dev, firefox, webkit

安装指定的浏览器, 如果本机已经安装过了，就不会安装了

```mipsasm
playwright install chrome

playwright install msedge
```

Google Chrome 或 Microsoft Edge 安装不会被隔离。它们将安装在默认的全局位置，具体取决于您的操作系统。

如果提示已经在系统里面安装了chrome

```mipsasm
Failed to install browsers
Error:
╔═════════════════════════════════════════════════════════════════╗
║ ATTENTION: "chrome" is already installed on the system!         ║
║                                                                 ║
║ "chrome" installation is not hermetic; installing newer version ║
║ requires *removal* of a current installation first.             ║
║                                                                 ║
║ To *uninstall* current version and re-install latest "chrome":  ║
║                                                                 ║
║ - Close all running instances of "chrome", if any               ║
║ - Use "--force" to install browser:                             ║
║                                                                 ║
║     playwright install --force chrome                           ║
║                                                                 ║
║ <3 Playwright Team                                              ║
╚═════════════════════════════════════════════════════════════════╝
```

可以先关闭正在运行的chrome 浏览器，使用以下命令安装到最新版

```css
playwright install --force chrome  
```

安装完成会显示版本号，以及安装的位置

```lua
>playwright install --force chrome
Downloading Google Chrome
Installing Google Chrome

ProductVersion   FileVersion      FileName
--------------   -----------      --------
111.0.5563.65    111.0.5563.65    C:\Program Files\Google\Chrome\Application\chrome.exe
```

# 指定 channel 打开浏览器

默认情况下，chromium.launch() 不带 channel 参数打开的是 `chromium` 浏览器

```csharp
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.baidu.com/")
```

Google Chrome 和 Microsoft Edge浏览器都是用的 chromium 内核，所以只需加一个`channel="chrome"` 即可打开谷歌浏览器

```csharp
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, channel="chrome")
    page = browser.new_page()

    page.goto("https://www.baidu.com/")
```

添加 `channel="msedge"` 即可打开Microsoft Edge浏览器

```csharp
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, channel="msedge")
    page = browser.new_page()

    page.goto("https://www.baidu.com/")
```

  



