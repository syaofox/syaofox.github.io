---
title: "python+playwright 学习-46 鼠标操作- 滚轮操作mouse.wheel"
date: 2023-04-16 10:47:15+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

有些网站是动态加载的，当拖动页面右侧滚动条后会自动加载网页下面的内容，或者通过鼠标滚轮操作。

# 鼠标滚轮操作

鼠标滚轮操作调用page.mouse.wheel() 方法

*   delta\_x 横向移动距离
*   delta\_y 纵向移动距离

```smalltalk
    def wheel(self, delta_x: float, delta_y: float) -> None:
        """Mouse.wheel

        Dispatches a `wheel` event.

        **NOTE** Wheel events may cause scrolling if they are not handled, and this method does not wait for the scrolling
        to finish before returning.

        Parameters
        ----------
        delta_x : float
            Pixels to scroll horizontally.
        delta_y : float
            Pixels to scroll vertically.
        """
```

# 使用示例

一边滚动一边加载网页

```csharp
# 上海悠悠 wx:283340479
# blog:https://www.cnblogs.com/yoyoketang/
from playwright.sync_api import Playwright, sync_playwright


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('http://events.jianshu.io/')

    for i in range(50):
        page.mouse.wheel(0, 100)
        page.wait_for_timeout(500)

    page.pause()
    browser.close()
```

  



