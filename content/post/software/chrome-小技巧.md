---
title: "Chrome 小技巧"
date: 2020-06-18T09:50:44+08:00
description: ""
tags: [Chrome]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Software
comment : false
draft: false 
author: "syaofox"
type: post
---

## 清除特定网站的 cache

有时候我们需要单独清空某个网站的缓存，但是chrome并没有提供单独删除某个站缓存的功能，这里有个小技巧

打开开发者工具（F12），选择 Network——Disable cache 即可。需要清除某网站缓存时 F12 打开开发者工具就会自动清除这个网站的缓存，而不必清除所有网站的缓存了。

---

## 另存为单一页面(mhtm) 

升级到75、76版本后谷歌浏览器`Chrome V75.0.3770.142 V76.0.3809.87`新版，发现无法另存为/保存网页为`MHTML`了。

原来chrome搞了个"Chrome Flag Ownership"的项目，目的是清理未使用的和过时的flags，现在`save-page-as-mhtml`仅作为开发者测试使用。就是说现在`save-page-as-mhtml`作为switch存在。

解决方案是，右键chrome快捷方式，选择快捷方式一栏，在目标输入框chrome.exe后加入空格和`--save-page-as-mhtml`，再重新打开chrome就可以了。