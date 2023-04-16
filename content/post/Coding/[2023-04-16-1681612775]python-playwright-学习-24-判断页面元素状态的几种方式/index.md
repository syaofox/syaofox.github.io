---
title: "python+playwright 学习-24 判断页面元素状态的几种方式"
date: 2023-04-16 10:39:35+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

在操作元素之前，可以先判断元素的状态。判断元素操作状态也可以用于断言。

# 常用的元素判断方法

page对象调用的判断方法, 传一个selector 定位参数

*   page.is\_checked(selector: str) # checkbox or radio 是否选中
*   page.is\_disabled(selector: str) # 元素是否可以点击或编辑
*   page.is\_editable(selector: str) # 元素是否可以编辑
*   page.is\_enabled(selector: str) # 是否可以操作
*   page.is\_hidden(selector: str) # 是否隐藏
*   page.is\_visible(selector: str) # 是否可见

locator 对象调用的判断方法

*   locator.is\_checked()
*   locator.is\_disabled()
*   locator.is\_editable()
*   locator.is\_enabled()
*   locator.is\_hidden()
*   locator.is\_visible()

元素句柄 的判断方法

*   element\_handle.is\_checked()
*   element\_handle.is\_disabled()
*   element\_handle.is\_editable()
*   element\_handle.is\_enabled()
*   element\_handle.is\_hidden()
*   element\_handle.is\_visible()

元素句柄（element\_handle）是通过page.query\_selector()方法调用返回的ElementHandle ，这种一般不常用.  
关于元素句柄和locator 定位的区别这篇有介绍[https://www.cnblogs.com/yoyoketang/p/17190635.html](https://www.cnblogs.com/yoyoketang/p/17190635.html)

# locator 定位后判断元素

locator 对象调用的判断方法

*   locator.is\_checked()
*   locator.is\_disabled()
*   locator.is\_editable()
*   locator.is\_enabled()
*   locator.is\_hidden()
*   locator.is\_visible()

is\_checked() 用于判断checkbox or radio 的状态是否被选中

```bash
       <div>
           <label>性别：
               <input type="radio" name="sex" id="man" checked>男
               <input type="radio" name="sex" id="woman">女
               <input type="radio" name="sex" id="no" disabled>人妖
           </label>
       </div>
       <div>
           <label>标签：
               <input type="checkbox" id="a1"> 旅游
               <input type="checkbox" id="a2">看书
               <input type="checkbox" id="a3" checked >学习
               <input type="checkbox" id="a4" checked disabled>学python
           </label>
       </div>
```

![](assets/1681612775-2214c2fe00b03353790ed8ddb7e4f5b7.png)

代码示例

```lisp
    print(page.locator('#man').is_checked()) # checked
    print(page.locator('#man').is_enabled())
    print(page.locator('#no').is_checked())
    print(page.locator('#no').is_enabled())  # disabled
```

返回结果

```python
True
True
False
False
```

# page对象调用的判断方法

page对象调用的判断方法, 传一个selector 定位参数

*   page.is\_checked(selector: str) # checkbox or radio 是否选中
*   page.is\_disabled(selector: str) # 元素是否可以点击或编辑
*   page.is\_editable(selector: str) # 元素是否可以编辑
*   page.is\_enabled(selector: str) # 是否可以操作
*   page.is\_hidden(selector: str) # 是否隐藏
*   page.is\_visible(selector: str) # 是否可见

使用示例

```css
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/
    print(page.is_checked('#a3'))
    print(page.is_enabled('#a3'))
    print(page.is_checked('#a4'))
    print(page.is_enabled('#a4'))
```

运行结果

```python
True
True
True
False
```

总的来说有2种方式判断元素 `page.is_xx()` 和 `locator.is_xxx()`

  



