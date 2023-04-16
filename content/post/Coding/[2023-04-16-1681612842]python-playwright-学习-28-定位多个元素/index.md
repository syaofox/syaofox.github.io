---
title: "python+playwright 学习-28 定位多个元素"
date: 2023-04-16 10:40:42+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

我们一般定位到页面上唯一的元素再进行操作，有时候一个元素的属性是一样的，会定位到多个元素

# click方法

当定位到页面唯一元素的时候，可以调用click方法

```bash
   <div>
           <label>标签：
               <input type="checkbox" id="a1"> 旅游
               <input type="checkbox" id="a2">看书
               <input type="checkbox" id="a3" checked >学习
               <input type="checkbox" id="a4">学python
           </label>
       </div>
```

如果直接通过id定位到，可以直接调用click 方法

```mipsasm
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

  a1 = page.locator('#a1')
    print(a1)   # <Locator>
    a1.click()
```

如果通过`type="checkbox"` 属性定位，会定位到多个元素

```mipsasm
a1 = page.locator('[type="checkbox"]')
    print(a1)   # <Locator>
    a1.click()
```

此时会抛出异常

```python
playwright._impl._api_types.Error: Error: strict mode violation: locator("[type=\"checkbox\"]") resolved to 4 elements:
    1) <input id="a1" type="checkbox"/> aka get_by_label("标签：\n                旅游\n               看书\n               学习\n               学python")
    2) <input id="a2" type="checkbox"/> aka get_by_role("checkbox").nth(1)
    3) <input id="a3" checked type="checkbox"/> aka get_by_role("checkbox").nth(2)
    4) <input id="a4" type="checkbox"/> aka get_by_role("checkbox").nth(3)
=========================== logs ===========================
waiting for locator("[type=\"checkbox\"]")
```

在异常里面会非常清晰的看到，按给的定位方式有4个元素被定位到，所以不能直接调用click的方法

# first 和 last

前面提到如果定位到多个元素，可以用first 和 last 取第一个和最后一个

```mipsasm
a1 = page.locator('[type="checkbox"]')
    a1.first.click()  # 点第一个
    a1.last.click()   # 点最后个
```

# nth() 根据索引定位

前面报错的时候会看到画面有 nth() 可以根据索引找到第几个元素

```python
    2) <input id="a2" type="checkbox"/> aka get_by_role("checkbox").nth(1)
    3) <input id="a3" checked type="checkbox"/> aka get_by_role("checkbox").nth(2)
    4) <input id="a4" type="checkbox"/> aka get_by_role("checkbox").nth(3)
```

使用示例

```armasm
 a1 = page.locator('[type="checkbox"]')
    a1.nth(0).click()
    a1.nth(3).click()
```

# count 统计个数

使用count 可以统计元素的个数

```bash
    a1 = page.locator('[type="checkbox"]')
    print(a1.count())    # 4
```

  



