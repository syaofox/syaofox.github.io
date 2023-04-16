---
title: "python+playwright 学习-47 鼠标操作- Mouse"
date: 2023-04-16 10:47:27+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

Mouse 鼠标操作是基于page对象去调用。常用的鼠标操作有单击，双击，滚轮，按住，移动，释放。

# page.mouse 使用

Mouse 类在相对于视口左上角的主框架 CSS 像素中运行。

每个page对象都有自己的鼠标，可通过page.mouse访问。

```scss
# using ‘page.mouse’ to trace a 100x100 square.
page.mouse.move(0, 0)
page.mouse.down()
page.mouse.move(0, 100)
page.mouse.move(100, 100)
page.mouse.move(100, 0)
page.mouse.move(0, 0)
page.mouse.up()
```

# click 点击

鼠标click 点击是mouse.move()、mouse.down()、mouse.up()的快捷方式。

```sql
    def click(
        self,
        x: float,
        y: float,
        *,
        delay: typing.Optional[float] = None,
        button: typing.Optional[Literal["left", "middle", "right"]] = None,
        click_count: typing.Optional[int] = None
    ) -> None:
        """Mouse.click

        Shortcut for `mouse.move()`, `mouse.down()`, `mouse.up()`.

        Parameters
        ----------
        x : float
        y : float
        delay : Union[float, None]
            Time to wait between `mousedown` and `mouseup` in milliseconds. Defaults to 0.
        button : Union["left", "middle", "right", None]
            Defaults to `left`.
        click_count : Union[int, None]
            defaults to 1. See [UIEvent.detail].
        """
```

参数详解：

*   x 横向坐标位置
*   y 纵向坐标位置
*   delay 是`mousedown` 和 `mouseup` 事件中间的等待时间，单位是毫秒，默认是0
*   button 是点击元素的位置："left", "middle", "right"， 默认参数是left
*   click\_count 是点击次数

```scss
mouse.click(x, y)
mouse.click(x, y, **kwargs)
```

# dblclick 双击

鼠标双击是mouse.move()、mouse.down()、mouse.up()、mouse.down()和mouse.up()的快捷方式。

```shell
# 上海悠悠 wx:283340479
# blog:https://www.cnblogs.com/yoyoketang/

mouse.dblclick(x, y)
mouse.dblclick(x, y, **kwargs)
```

# mouse.down 按住鼠标

调度一个mousedown事件。  
有2个参数

*   button 是点击元素的位置："left", "middle", "right"， 默认参数是left
*   click\_count 是点击次数

```scss
mouse.down()
mouse.down(**kwargs)
```

# mouse.move 移动

调度一个 `mousemove` 事件。

```sql
  def move(self, x: float, y: float, *, steps: typing.Optional[int] = None) -> None:
        """Mouse.move

        Dispatches a `mousemove` event.

        Parameters
        ----------
        x : float
        y : float
        steps : Union[int, None]
            Defaults to 1. Sends intermediate `mousemove` events.
        """
```

用法

```cpp
mouse.move(x, y)
mouse.move(x, y, **kwargs)
```

# mouse.up 释放鼠标

调度一个mouseup事件。

```scss
mouse.up()
mouse.up(**kwargs)
```

# wheel 滚轮

调度一个wheel事件。（滚轮事件如果不处理可能会导致滚动，该方法不会等待滚动结束才返回。）

```scss
mouse.wheel(delta_x, delta_y)
```

鼠标操作实例参考  
[python+playwright 学习-46 鼠标操作- 滚轮操作mouse.wheel](https://www.cnblogs.com/yoyoketang/p/17284996.html)  
[python+playwright 学习-44 过登录页面的滑块拼图验证码](https://www.cnblogs.com/yoyoketang/p/17282358.html)  
[python+playwright 学习-39.登录页面滑动解锁](https://www.cnblogs.com/yoyoketang/p/17261358.html)

  



