---
title: "python+playwright 学习-38.checkbox和radio 相关操作"
date: 2023-04-16 10:45:34+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

单选框和复选框相关操作总结  
locator.click() 点击操作  
locator.check() 选中  
locator.uncheck() 不选中  
locator.set\_checked() 设置选中状态  
locator.is\_checked() 判断是否被选中

# 使用场景

radio 和 checkbox 使用场景

```bash
       <div>
           <label>性别：
               <input type="radio" name="sex" id="man" checked>男
               <input type="radio" name="sex" id="woman">女
           </label>
       </div>
       <div>
           <label>标签：
               <input type="checkbox" id="a1"> 旅游
               <input type="checkbox" id="a2">看书
               <input type="checkbox" id="a3" checked >学习
               <input type="checkbox" id="a4" >学python
           </label>
       </div>
```

# radio 单选操作

radio 是单选，如果男已经是选择状态，那么点击它是不会改变状态的，只能点另外一个radio 改变状态。

方法1：click() 点击

```bash
    # radio 操作
    status1 = page.locator('#man').is_checked()
    print(status1)
    # 选择 女
    page.locator('#woman').click()
    print(page.locator('#woman').is_checked())
```

方法2： check()

```scss
 # 选择 女
    page.locator('#woman').check()
    print(page.locator('#woman').is_checked())
```

方法3： set\_checked()需传checked 参数，布尔值

```python
# 选择 女
    page.locator('#woman').set_checked(checked=True)
    print(page.locator('#woman').is_checked())
```

另外一种写法, 调用page对象相关方法

```python
page.check('#woman')

page.set_checked('#woman', checked=True)
```

需注意的是，如果男本身就是选择状态，去设置unchecked 状态，会报错: Clicking the checkbox did not change its state

```scss
page.locator('#man').uncheck()
```

报错内容

```java
    result = next(iter(done)).result()
playwright._impl._api_types.Error: Clicking the checkbox did not change its state
=========================== logs ===========================
waiting for locator("#man")
```

# checkbox 复选框

checkbox 复选框跟 radio 操作的区别在于，如果已经被选择了，再点击会被取消选中，所以不会有前面的报错。

click 是点击操作，未选中的时候，点击就会被选中。

```scss
    # checkbox 操作
    page.locator('#a1').click()
    print(page.locator('#a1').is_checked())
```

如果想让元素必须是选择状态(不管之前有没被选中），可以使用check() 或 set\_checked() 方法

```scss
    page.locator('#a1').check()
    print(page.locator('#a1').is_checked())
```

set\_checked() 方法

```python
   # checkbox 操作
    page.locator('#a1').set_checked(checked=True)
    print(page.locator('#a1').is_checked())
```

# 批量选中checkbox

定位全部CheckBox 批量选中

```rust
  # checkbox 操作
    box = page.locator('[type="checkbox"]')
    for item in box.all():
        item.check()
```

  



