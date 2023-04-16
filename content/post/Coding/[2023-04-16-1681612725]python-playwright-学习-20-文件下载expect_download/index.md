---
title: "python+playwright 学习-20.文件下载expect_download()"
date: 2023-04-16 10:38:45+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

文件下载操作

# expect\_download()

当浏览器上下文关闭时，所有属于浏览器上下文的下载文件都会被删除。  
下载开始后会发出下载事件。下载完成后，下载路径可用：

```makefile
with page.expect_download() as download_info:
    page.get_by_text("Download file").click()
download = download_info.value
# wait for download to complete
path = download.path()
```

# download 相关操作

1.取消下载。如果下载已经完成或取消，则不会失败。成功取消后，download.failure()将解析为'canceled'.

```scss
download.cancel()
```

2.删除下载的文件。如有必要，将等待下载完成。

```go
download.delete()
```

3.返回下载错误（如果有）。如有必要，将等待下载完成。

```scss
download.failure()
```

4.获取下载所属的页面。

```undefined
download.page
```

5.下载路径  
如果下载成功，则返回下载文件的路径。如有必要，该方法将等待下载完成。该方法在远程连接时抛出。  
请注意，下载的文件名是随机 GUID，使用download.suggested\_filename获取建议的文件名。

```lua
download.path()
```

返回NoneType|pathlib.Path 类型  
6.将下载复制到用户指定的路径。在下载仍在进行时调用此方法是安全的。如有必要，将等待下载完成。

```lua
download.save_as(path)
```

7.返回此下载的建议文件名。  
它通常由浏览器根据`Content-Disposition`响应标头或`download`属性计算得出。请参阅whatwg上的规范。不同的浏览器可以使用不同的逻辑来计算它。

```undefined
download.suggested_filename
```

8.返回下载的 url。

```undefined
download.url
```

# 使用示例

比如有个页面有下载地址

```xml
<body>
  <h1>下载文件</h1>
  <a href="https://www.python.org/ftp/python/3.10.10/python-3.10.10-embed-amd64.zip">点我下载</a>
</body>
```

代码示例

```python
from playwright.sync_api import sync_playwright
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, slow_mo=3000)
    page = browser.new_page()
    page.goto(r'*************down.html')
    with page.expect_download() as download_info:
        page.get_by_text("点我下载").click()
    download = download_info.value
    # wait for download to complete
    print(download.url)  # 获取下载的url地址
    # 这一步只是下载下来，生成一个随机uuid值保存，代码执行完会自动清除
    print(download.path())
    # 最终可以用save_as 保存到本地
    download.save_as(download.suggested_filename)

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```

这样在本地就会看到下载成功的文件  
  



