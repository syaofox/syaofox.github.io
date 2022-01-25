---
title: "xorg按键测试"
date: 2022-03-28T10:14:16+08:00
description: ""
image: ""
categories: [Tips]
tags: [linux,archlinux]
---

## 安装
```shell
sudo pacamn -S xorg-xev
```

## 查看modkey

```shell
xmodmap

xmodmap:  up to 4 keys per modifier, (keycodes in parentheses):

shift       Shift_L (0x32),  Shift_R (0x3e)
lock        Caps_Lock (0x42)
control     Control_L (0x25),  Control_R (0x69)
mod1        Alt_L (0x40),  Alt_R (0x6c),  Meta_L (0xcd)
mod2        Num_Lock (0x4d)
mod3
mod4        Super_L (0x85),  Super_R (0x86),  Super_L (0xce),  Hyper_L (0xcf)
mod5        ISO_Level3_Shift (0x5c),  Mode_switch (0xcb)

```
## 测试键盘按键
```shell
xev | awk -F'[ )]+' '/^KeyPress/ { a[NR+2] } NR in a { printf "%-3s %s\n", $5, $8 }'

40  d
40  d
27  r
13  4
12  3
14  5

```

## 测试鼠标按键
```shell
xev -event button | grep button

state 0x0, button 1, same_screen YES
state 0x100, button 1, same_screen YES
state 0x0, button 1, same_screen YES
state 0x100, button 1, same_screen YES
state 0x0, button 3, same_screen YES
state 0x400, button 3, same_screen YES
state 0x0, button 3, same_screen YES
state 0x400, button 3, same_screen YES
state 0x0, button 1, same_screen YES


```