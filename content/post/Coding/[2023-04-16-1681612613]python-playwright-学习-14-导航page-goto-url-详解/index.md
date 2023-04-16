---
title: "python+playwright 学习-14.导航page.goto(url) 详解"
date: 2023-04-16 10:36:53+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

Playwright 可以导航到 URL 并处理由页面交互引起的导航。本篇涵盖了等待页面导航和加载完成的常见场景。

# 导航生命周期

导航从更改页面 URL 或通过与页面交互（例如，单击链接）开始。导航意图可能会被取消，例如，在点击未解析的 DNS 地址或转换为文件下载时。  
解析响应标头并更新会话历史记录后，将提交导航。只有在导航成功（提交）后，页面才会开始加载文档。  
加载包括通过网络获取剩余的响应主体、解析、执行脚本和触发加载事件：

调用 page.goto(url) 后页面加载过程：

*   page.url 设定新的 url
*   document 文档内容通过网络加载并解析
*   page.on("domcontentloaded") 事件触发
*   执行页面的 js 脚本，页面执行一些脚本并加载 css 和图像等资源
*   page.on("load") 事件触发
*   页面执行动态加载的脚本
*   `networkidle` 当 500 毫秒内没有新的网络请求时触发

## 事件状态

导航到 URL 会自动等待页面触发事件`load`。如果页面之前进行了客户端重定向`load`，page.goto()将自动等待重定向页面触发事件load。

从源码可以看到 wait\_until 等待的事件可以支持\["commit", "domcontentloaded", "load", "networkidle"\] 四个参数，默认是等待`load` 触发。

wait\_until:Union\[“commit”，“domcontentloaded”，“load”，“networkidle”，无\]当认为操作成功时，默认为“加载”。事件可以是：

*   domcontentloaded： 在触发“domcontentloaded”事件时完成操作。
*   load： 触发 load事件时完成操作。
*   networkidle： 当 500 毫秒内没有新的网络请求时触发，认为操作已完成。
*   commit：考虑在接收到网络响应并且文档开始加载时完成操作。

```rust
    def goto(
        self,
        url: str,
        *,
        timeout: typing.Optional[float] = None,
        wait_until: typing.Optional[
            Literal["commit", "domcontentloaded", "load", "networkidle"]
        ] = None,
        referer: typing.Optional[str] = None
    ) -> typing.Optional["Response"]:
```

如果我们希望ajax 也请求完成了，再继续下一步，那么可以覆盖默认行为以等待特定事件，例如 `networkidle`.  
(对于 `click`、`fill` 等操作会自动等待元素出现。)

```php
# Navigate and wait until network is idle
page.goto("https://example.com", wait_until="networkidle")
```

## 等待元素

在延迟加载的页面中，使用locator.wait\_for()等待元素可见是很有用的。或者，像page.click()这样的页面交互会自动等待元素。

```php
# Navigate and wait for element
page.goto("https://example.com")
page.get_by_text("example domain").wait_for()

# Navigate and click element
# Click will auto-wait for the element
page.goto("https://example.com")
page.get_by_text("example domain").click()
```

# 页面交互

## click/fill 会自动等待

在下面的场景中，locator.click()启动导航，然后等待导航完成。  
默认情况下，locator.click()将等待导航步骤完成。这可以与导航页面上的页面交互相结合，该页面交互将自动等待元素。

```bash
# Click will auto-wait for navigation to complete
page.get_by_text("Login").click()

# Fill will auto-wait for element on navigated page
page.get_by_label("User Name").fill("John Doe")
```

## 自定义等待

locator.click可以结合page.wait\_for\_load\_state()来等待加载事件。

```bash
page.locator("button").click()  # Click triggers navigation
page.wait_for_load_state("networkidle")  # This waits for the "networkidle"
```

## 等待元素

在延迟加载的页面中，使用locator.wait\_for()等待元素可见是很有用的。或者，像locator.click()这样的页面交互会自动等待元素。

```scss
# Click triggers navigation
page.get_by_text("Login").click()
# Click will auto-wait for the element
page.get_by_label("User Name").wait_for()

# Click triggers navigation
page.get_by_text("Login").click()
# Fill will auto-wait for element
page.get_by_label("User Name").fill("John Doe")
```

# 异步导航

单击一个元素可以在启动导航之前触发异步处理。在这些情况下，建议显式调用page.expect\_navigation()。例如：

*   导航是从setTimeout
*   页面在导航前等待网络请求

```python
# Waits for the next navigation. Using Python context manager
# prevents a race condition between clicking and waiting for a navigation.
with page.expect_navigation():
    # Triggers a navigation after a timeout
    page.get_by_text("Navigate after timeout").click()
```

# 多重导航

击一个元素可能会触发多个导航。在这些情况下，建议将 `page.expect_navigation()` 显式指向特定的 url。例如：

*   load事件后发出的客户端重定向
*   多次推送到历史状态

```python
# Using Python context manager prevents a race condition
# between clicking and waiting for a navigation.
with page.expect_navigation(url="**/login"):
    # Triggers a navigation with a script redirect
    page.get_by_text("Click me").click()
```

# 加载弹出窗口

打开弹出窗口时，显式调用page.wait\_for\_load\_state()可确保将弹出窗口加载到所需状态。

```csharp
with page.expect_popup() as popup_info:
    page.get_by_text("Open popup").click() # Opens popup
popup = popup_info.value
popup.wait_for_load_state("load")
```

# 高级模式

对于具有复杂加载模式的页面，page.wait\_for\_function()是定义自定义等待条件的强大且可扩展的方法。

```php
page.goto("http://example.com")
page.wait_for_function("() => window.amILoadedYet()")
# Ready to take a screenshot, according to the page itself.
page.screenshot()
```

# timeout 等待超时

timeout 参数可以设置页面加载超时时间, 默认是30秒， 传递“0”以禁用超时。

```go
timeout : Union[float, None]
            Maximum operation time in milliseconds, defaults to 30 seconds, pass `0` to disable timeout. The default value can
            be changed by using the `browser_context.set_default_navigation_timeout()`,
            `browser_context.set_default_timeout()`, `page.set_default_navigation_timeout()` or
            `page.set_default_timeout()` methods.
```

更改默认值可以使用 以下方法更改

*   `browser_context.set_fault_navigation_timeout（）`进行更改，
*   `browser_context.set_fault_timeout（）`，
*   `page.set_fault_navigation_timeout）`
*   `page.set_fault_timeout（）`

  



