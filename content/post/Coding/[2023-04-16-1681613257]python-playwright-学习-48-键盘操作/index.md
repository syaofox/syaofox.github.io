---
title: "python+playwright 学习-48 键盘操作"
date: 2023-04-16 10:47:37+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

Keyboard 提供了一个用于管理虚拟键盘的 API。高级 api 是keyboard.type()，它接受原始字符并在您的页面上生成适当的keydown、keypress/input和keyup事件。  
为了更好地控制，您可以使用keyboard.down()、keyboard.up()和keyboard.insert\_text()手动触发事件，就好像它们是从真实键盘生成的一样。

# 键盘操作示例

按住Shift以选择和删除某些文本的示例：

```vhdl
page.keyboard.type("Hello World!")
page.keyboard.press("ArrowLeft")
page.keyboard.down("Shift")
for i in range(6):
    page.keyboard.press("ArrowLeft")
page.keyboard.up("Shift")
page.keyboard.press("Backspace")
# result text will end up saying "Hello!"
```

按大写字母A 的例子

```bash
page.keyboard.press("Shift+KeyA")
# or
page.keyboard.press("Shift+A")
```

按`Ctrl+A`选择全部

```bash
# on windows and linux
page.keyboard.press("Control+A")
# on mac_os
page.keyboard.press("Meta+A")
```

# down 向下

调度一个keydown事件。

key可以指定预期的keyboardEvent.key值或单个字符来为其生成文本。可以在此处key找到这些值的超集。键的例子是：

F1- F12, Digit0- Digit9, KeyA- KeyZ, Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape, ArrowDown, End, Enter, Home, , , Insert,等\_PageDownPageUpArrowRightArrowUp

还支持以下修改快捷方式：Shift, Control, Alt, Meta, ShiftLeft.

按住将键入对应于大写字母Shift的文本。key

如果key是单个字符，则区分大小写，因此值a和A将生成各自不同的文本。

如果key是修饰键 、Shift、Meta、Control或Alt，则后续按键将在该修饰键激活的情况下发送。要释放修饰键，请使用keyboard.up()。

按下一次键后，对keyboard.down()的后续调用会将repeat设置为 true。要释放键，请使用keyboard.up()。

> 笔记 :修改键确实影响keyboard.down。按住Shift将以大写形式键入文本。

用法

```scss
keyboard.down(key)
```

# insert\_text 插入文本

仅调度input事件，不发出keydown,keyup或keypress事件。

```bash
page.keyboard.insert_text("嗨")
```

笔记：修改键不影响keyboard.insertText。按住Shift不会以大写形式键入文本。

# press 按住

key可以指定预期的keyboardEvent.key值或单个字符来为其生成文本。可以在此处key找到这些值的超集。键的例子是：

F1- F12, Digit0- Digit9, KeyA- KeyZ, Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape, ArrowDown, End, Enter, Home, , , Insert,等\_PageDownPageUpArrowRightArrowUp

还支持以下修改快捷方式：Shift, Control, Alt, Meta, ShiftLeft.

按住将键入对应于大写字母Shift的文本。key

如果key是单个字符，则区分大小写，因此值a和A将生成各自不同的文本。

也支持key: "Control+o"or等​​快捷方式。key: "Control+Shift+T"当使用修饰符指定时，修饰符被按下并在按下后续键时按住。

```lua
page = browser.new_page()
page.goto("https://keycode.info")
page.keyboard.press("a")
page.screenshot(path="a.png")
page.keyboard.press("ArrowLeft")
page.screenshot(path="arrow_left.png")
page.keyboard.press("Shift+O")
page.screenshot(path="o.png")
browser.close()
```

keyboard.down()和keyboard.up()的快捷方式。

# Type 操作

为文本中的每个字符发送keydown、keypress/input和事件。keyup

要按特殊键，例如Control或ArrowDown，请使用keyboard.press()。

使用示例

```python
# 上海悠悠 wx:283340479
# blog:https://www.cnblogs.com/yoyoketang/

page.keyboard.type("Hello") # types instantly
page.keyboard.type("World", delay=100) # types slower, like a user
```

# up 方法

调度一个keyup事件。

```scss
keyboard.up(key)
```

  



