---
title: "python+playwright 学习-29 如何判断元素是否存在"
date: 2023-04-16 10:42:58+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

playwright 如何判断某个元素是否存在？

# locator 定位元素

使用 locator 定位元素，不管元素存不存在，都会返回一个locator 对象，可以用到count() 方法统一元素的个数，如果元素个数是 0， 那么元素就不存在

```python
"""
判断元素存在
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()

    page.goto("https://www.baidu.com/")

    # 元素存在
    loc1 = page.locator("id=kw")
    print(loc1)
    print(loc1.count())

    # 元素不存在
    loc2 = page.locator('id=yoyo')
    print(loc2)
    print(loc2.count())
```

运行结果

```xml
<Locator frame=<Frame name= url='https://www.baidu.com/'> selector='id=kw'>
1
<Locator frame=<Frame name= url='https://www.baidu.com/'> selector='id=yoyo'>
0
```

locator 是定位当前页面上的元素，不会自动等待，如果用click等方法结合使用，会自动去等待元素处于可点击状态。

# query\_selector 定位

ElementHandle 表示页内 DOM 元素。ElementHandles 可以使用page.query\_selector()方法创建。  
Locator和ElementHandle之间的区别在于后者指向特定元素，而 Locator 捕获如何检索该元素的逻辑。

元素存在返回元素句柄，元素不存在返回None

```bash

    # 元素存在
    loc1 = page.query_selector('#kw')
    print(loc1)  # JSHandle@node

    # 元素不存在
    loc2 = page.query_selector('#yoyo')
    print(loc2)  # None
```

也可以用query\_selector\_all 复数定位方式返回一个list

```bash
    # 元素存在
    loc1 = page.query_selector_all('#kw')
    print(loc1)  # [<JSHandle preview=JSHandle@node>]

    # 元素不存在
    loc2 = page.query_selector_all('#yoyo')
    print(loc2)  # []
```

  



