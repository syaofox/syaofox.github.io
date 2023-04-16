---
title: "python+playwright 学习-41.locator.evaluate()对定位的元素执行JavaScript脚本"
date: 2023-04-16 10:46:10+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

page.evaluate() 是直接在页面对象上执行JavaScript脚本  
locator.evaluate() 是对定位的元素执行JavaScript  
locator.evaluate\_all() 对定位到的所有元素执行JavaScript

# locator.evaluate() 对元素执行JavaScript

先用locator 方法定位到元素, 再对元素执行JavaScript

```php
    # 上海悠悠 wx:283340479
    # blog:https://www.cnblogs.com/yoyoketang/

    page = browser.new_page()
    page.goto("http://127.0.0.1/login.html")

    username = page.locator('#username')
    # 输入框输入内容
    username.evaluate('node => node.value="yoyo"')
    # 获取输入框内容
    input_value = username.evaluate('node => node.value')
    print(input_value)  # yoyo
```

# locator.evaluate\_all() 执行全部元素

在页面中执行 JavaScript 代码，将所有匹配的元素作为参数。

```csharp
# 上海悠悠 wx:283340479
# blog:https://www.cnblogs.com/yoyoketang/

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )
    page = browser.new_page()
    page.goto("https://www.baidu.com/")

    links = page.locator('#s-top-left>a')
    # 定位全部元素
    res = links.evaluate_all('nodes => nodes.length')
    print(res)  # 7
```

定位百度页面上的链接, 执行`nodes.length` 获取元素个数  
  



