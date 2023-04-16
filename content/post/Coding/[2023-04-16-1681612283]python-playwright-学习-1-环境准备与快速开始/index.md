---
title: "python+playwright 学习-1.环境准备与快速开始"
date: 2023-04-16 10:31:23+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

说到 web 自动化，大家最熟悉的就是 selenium 了，selenium 之后又出现了三个强势的框架Puppeteer、CyPress、TestCafe， 但这3个都需要掌握 JavaScript 语言，所以只是少部分人在用。  
2020年微软开源一个 UI 自动化测试工具 Playwright, 支持 Node.js、Python、C# 和 Java 语言。

# 为什么要学 Playwright ？

selenium 在国内普及程度非常高，说到 web 自动化很多人第一个就会想到 selenium，它的出现确实是给整个行业带来了很多的影响。  
支持多语言，开源的框架，可以兼容多种浏览器，上手非常容易。

那么现在微软推出的 Playwright 到底有没必要去学呢？先看下官方介绍[https://playwright.dev/python/](https://playwright.dev/python/)

**跨浏览器和平台**

*   跨浏览器。Playwright 支持所有现代渲染引擎，包括 Chromium、WebKit 和 Firefox。
*   跨平台。在 Windows、Linux 和 macOS 上进行本地测试或在 CI 上进行无头或有头测试。
*   跨语言。在TypeScript、JavaScript、Python、.NET、Java中使用 Playwright API 。
*   测试移动网络。适用于 Android 和 Mobile Safari 的 Google Chrome 浏览器的本机移动仿真。相同的渲染引擎适用于您的桌面和云端。

**稳定性**

*   自动等待。Playwright 在执行动作之前等待元素可操作。它还具有一组丰富的内省事件。两者的结合消除了人为超时的需要——这是不稳定测试的主要原因。
*   Web优先断言。Playwright 断言是专门为动态网络创建的。检查会自动重试，直到满足必要的条件。
*   追踪。配置测试重试策略，捕获执行跟踪、视频、屏幕截图以消除薄片。

**运行机制**

浏览器在不同进程中运行属于不同来源的 Web 内容。Playwright 与现代浏览器架构保持一致，并在进程外运行测试。这使得 Playwright 摆脱了典型的进程内测试运行器的限制。

*   多重一切。测试跨越多个选项卡、多个来源和多个用户的场景。为不同的用户创建具有不同上下文的场景，并在您的服务器上运行它们，所有这些都在一次测试中完成。
*   可信事件。悬停元素，与动态控件交互，产生可信事件。Playwright 使用与真实用户无法区分的真实浏览器输入管道。
*   测试框架，穿透 Shadow DOM。Playwright 选择器穿透影子 DOM 并允许无缝地输入帧。

**完全隔离-快速执行**

*   浏览器上下文。Playwright 为每个测试创建一个浏览器上下文。浏览器上下文相当于一个全新的浏览器配置文件。这提供了零开销的完全测试隔离。创建一个新的浏览器上下文只需要几毫秒。
*   登录一次。保存上下文的身份验证状态并在所有测试中重用它。这绕过了每个测试中的重复登录操作，但提供了独立测试的完全隔离。

**强大的工具**

*   代码生成器。通过记录您的操作来生成测试。将它们保存为任何语言。
*   调试。检查页面、生成选择器、逐步执行测试、查看点击点、探索执行日志。
*   跟踪查看器。捕获所有信息以调查测试失败。Playwright 跟踪包含测试执行截屏、实时 DOM 快照、动作资源管理器、测试源等等。

# 环境准备

Playwright 是专门为满足端到端测试的需要而创建的。Playwright 支持所有现代渲染引擎，包括 Chromium、WebKit（Safari 的浏览器引擎）和 Firefox。  
在 Windows、Linux 和 macOS 上进行本地测试或在 CI 上进行测试.

python 版本要求 python3.7+ 版本。

安装 playwright：

```mipsasm
pip install playwright
```

安装所需的浏览器 chromium,firefox 和 webkit：

```mipsasm
playwright install
```

仅需这一步即可安装所需的浏览器，并且不需要安装驱动包了（解决了selenium启动浏览器，总是要找对应驱动包的痛点）

如果安装报错，提示缺少Visual C++， 解决办法：  
安装Microsoft Visual C++ Redistributable 2019

```bash
https://aka.ms/vs/16/release/VC_redist.x64.exe
```

直接点击就可以下载了，下载后直接安装即可。

# 简单使用

安装后，您可以在 Python 脚本中使用 Playwright，并启动 3 种浏览器中的任何一种（chromium,firefox和webkit）。

启动浏览器并打开百度页面

```csharp
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)          # 启动 chromium 浏览器
    page = browser.new_page()              # 打开一个标签页
    page.goto("https://www.baidu.com")     # 打开百度地址
    print(page.title())                    # 打印当前页面title
    browser.close()                        # 关闭浏览器对象
```

Playwright 支持2种运行方式：同步和异步。如果您的现代项目使用asyncio，您应该使用 async API：

以下是异步运行方式

```python
import asyncio
from playwright.async_api import async_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.baidu.com")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

如果你不习惯with语句，也可以用start() 和stop() 的方式

```mipsasm
from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.baidu.com/")


browser.close()
playwright.stop()
```

# headless 模式

默认情况下，Playwright 以无头模式运行浏览器。要查看浏览器 UI，请headless=False在启动浏览器时传递标志。

headless 无头模式运行浏览器示例：

```csharp
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


with sync_playwright() as p:
    browser = p.chromium.launch()          # 启动 chromium 浏览器
    page = browser.new_page()              # 打开一个标签页
    page.goto("https://www.baidu.com")     # 打开百度地址
    print(page.title())                    # 打印当前页面title
    browser.close()                        # 关闭浏览器对象
```

# 关于等待

Playwright 打开浏览器运行脚本的速度那就是一个字：快！

您还可以用来slow\_mo （单位是毫秒）减慢执行速度。它的作用范围是全局的，从启动浏览器到操作元素每个动作都会有等待间隔，方便在出现问题的时候看到页面操作情况。

```python
chromium.launch(headless=False, slow_mo=50)
```

使用示例

```css
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.fill('#kw', "上海-悠悠博客")
    page.click('#su')
    browser.close()
```

运行后会发现每个操作都会有间隔时间。

**time.sleep() 不再使用**

Playwright 在查找元素的时候具有自动等待功能，如果你在调试的时候需要使用等待，你应该使用page.wait\_for\_timeout(5000) 代替 time.sleep(5)并且最好不要等待超时。

```css
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    # 等待5秒
    page.wait_for_timeout(5000)
    page.fill('#kw', "上海-悠悠博客")
    page.click('#su')
    browser.close()
```

请使用 wait( wait\_for\_timeout) 方法而不是time模块。这是因为我们内部依赖于异步操作，并且在使用时time.sleep(5)无法正确处理它们。  
  