---
title: "python+playwright 学习-16.new_context上下文之非常好用的base_url 参数"
date: 2023-04-16 10:37:35+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

在做自动化测试的时候，我们经常是基于某个测试环境地址去测试某个项目，所以应该把它单独拿出来做为一个全局的配置。  
其它地方用相对地址就行。在pytest用例里面可以用到pytest-base-url 插件来实现。  
playwright 不得不说设计的非常人性化，堪称web自动化界的“海底捞”服务，就差上厕所帮你扶着了~

# 使用场景

如下测试场景, 在多个地方都会有访问的地址，并且环境地址都是一样`https://www.cnblogs.com`, 也就是我们说的base\_url地址。

```mipsasm
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    # 打开首页
    page.goto("https://www.cnblogs.com/")

    # 点点点后打开其他页
    page.goto("https://www.cnblogs.com/yoyoketang")

    context.close()
    browser.close()
```

当很多地方都用到base\_url 的时候，为了方便切换环境，应该单独拿出来,做全局配置

# base\_url 的使用

base\_url 参数是在new\_context() 新建上下文的时候使用

优化后的代码如下：

```mipsasm
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(base_url='https://www.cnblogs.com')

    page = context.new_page()
    # 打开首页
    page.goto("/")

    # 点点点后打开其他页
    page.goto("/yoyoketang")

    context.close()
    browser.close()
```

这样只需相对地址即可访问了。

# pytest-playwright 使用

在pytest-playwright 插件中已经自带了pytest-base-url 插件，于是仅需在pytest.ini中配置

```ini
[pytest]
base_url=https://www.cnblogs.com
```

或者使用命令行参数

```csharp
pytest --base-url https://www.cnblogs.com
```

在测试用例中写相对地址即可

```python
from playwright.sync_api import Page


def test_blog(page: Page):
    """首页"""
    page.goto("/")


def test_yoyo_blog(page: Page):
    """上海悠悠博客地址"""
    page.goto("/yoyoketang")
```

  



