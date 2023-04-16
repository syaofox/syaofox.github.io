---
title: "python+playwright 学习-31 事件添加与删除"
date: 2023-04-16 10:43:17+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

Playwright 允许监听网页上发生的各种类型的事件，例如网络请求、子页面的创建、 dedicated workers等。

# 等待特定事件

大多数时候，脚本需要等待特定事件的发生。下面是一些典型的事件等待模式。

使用page.expect\_request()等待具有指定 url 的请求：

```csharp
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/


with page.expect_request("**/*logo*.png") as first:
  page.goto("https://wikipedia.org")
print(first.value.url)
```

等待弹出窗口：

```csharp
with page.expect_popup() as popup:
  page.get_by_text("open the popup").click()
popup.value.goto("https://wikipedia.org")
```

# 添加/删除事件

有时，事件在随机时间发生，而不是等待它们，它们需要被处理。Playwright 支持用于订阅和取消订阅事件的传统语言机制：

添加事件使用`page.on('event', handle)`

```css
def print_request_sent(request):
  print("Request sent: " + request.url)

def print_request_finished(request):
  print("Request finished: " + request.url)

page.on("request", print_request_sent)
page.on("requestfinished", print_request_finished)
page.goto("https://wikipedia.org")
```

删除事件使用 `page.remove_listener("event", print_request_finished)`

```csharp
page.remove_listener("requestfinished", print_request_finished)
page.goto("https://www.openstreetmap.org/")
```

# 添加一次性事件

如果某个事件需要处理一次，有一个方便的 API：

```css
page.once("dialog", lambda dialog: dialog.accept("2021"))
page.evaluate("prompt('Enter a number:')")
```

以上代码`dialog` 事件仅处理一次。  
  



