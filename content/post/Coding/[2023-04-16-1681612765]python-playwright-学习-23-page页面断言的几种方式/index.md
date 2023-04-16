---
title: "python+playwright 学习-23 page页面断言的几种方式"
date: 2023-04-16 10:39:25+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

当打开一个页面的时候，需要断言是否是期望的页面  
PageAssertions类提供断言方法，可用于在测试中对页面状态进行断言。

# 页面断言

主要有四个断言方法

*   to\_have\_title
*   not\_to\_have\_title
*   to\_have\_url
*   not\_to\_have\_url

to\_have\_title() 确保页面具有给定的标题。

```python
import re
from playwright.sync_api import expect
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

# ...
expect(page).to_have_title(re.compile(r".*checkout"))
```

参数

*   title\_or\_reg\_exp 预期的标题或正则表达式。
*   timeout （可选） 超时时间

not\_to\_have\_title 与expect(page).to\_have\_title()相反。

```scss
expect(page).not_to_have_title(title_or_reg_exp)
expect(page).not_to_have_title(title_or_reg_exp, **kwargs)
```

# 断言url

to\_have\_url 确保页面导航到给定的 URL。

```python
import re
from playwright.sync_api import expect

# ...
expect(page).to_have_url(re.compile(".*checkout"))
```

not\_to\_have\_url 与expect(page).to\_have\_url()相反。

```scss
expect(page).not_to_have_url(url_or_reg_exp)
expect(page).not_to_have_url(url_or_reg_exp, **kwargs)
```

  



