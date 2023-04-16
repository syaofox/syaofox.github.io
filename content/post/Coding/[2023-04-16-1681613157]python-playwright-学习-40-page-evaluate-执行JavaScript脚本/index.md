---
title: "python+playwright 学习-40.page.evaluate()执行JavaScript脚本"
date: 2023-04-16 10:45:57+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

大家在学selenium的时候，对于页面上的有些元素不好操作的时候，可以使用`driver.execute_script()` 方法执行JavaScript脚本。  
在playwright 中也有类似的方法，使用page.evaluate()执行JavaScript脚本。  
page.evaluate()和page.evaluate\_handle()之间的唯一区别是page.evaluate\_handle()返回JSHandle。

*   page.evaluate() 返回调用执行的结果
*   page.evaluate\_handle()返回JSHandle

# page.evaluate()

此方法返回evaluate() 返回执行JavaScript脚本的结果，使用示例

简单示例

```lisp
print(page.evaluate("1 + 2")) # prints "3"
x = 10
print(page.evaluate(f"1 + {x}")) # prints "11"
```

也可以是执行一个函数

```bash
res = page.evaluate("() => 'Hello World!'",)
print(res)   # Hello World!
```

函数也可以带上参数

```bash
res = page.evaluate("([a, b]) => a+b+'world'", ["hello", 'xx'])
print(res)  # helloxxworld
```

如果传递给page.evaluate()的函数返回一个不可序列化的值，则page.evaluate()解析为undefined

# 操作 web 网页示例

执行`document.title` 获取页面的title

```dos
    page.goto("https://www.baidu.com/")

    title = page.evaluate('document.title')
    print(title)
    page.pause()
```

登录网站示例

```python
# 上海悠悠 wx:283340479
# blog:https://www.cnblogs.com/yoyoketang/

    page = browser.new_page()
    page.goto("http://127.0.0.1/login.html")

    js = """
    document.getElementById('username').value='yoyo';
    document.getElementById('password').value='******';
    document.getElementById('loginBtn').click();
    """

    page.evaluate(js)
```

page.evaluate() 方法一般用于页面上操作元素，无法正常操作的情况，可以用执行JavaScript脚本协助解决。

# page.evaluate\_handle()返回JSHandle

page.evaluate()和page.evaluate\_handle()之间的唯一区别是page.evaluate\_handle()返回JSHandle。

```mipsasm
    a_handle = page.evaluate_handle("document.body")
    result_handle = page.evaluate_handle("body => body.innerHTML", a_handle)
    print(result_handle.json_value())
    result_handle.dispose()
```

  



