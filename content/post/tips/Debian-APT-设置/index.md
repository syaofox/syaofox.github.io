---
title: "Debian APT 设置"
date: 2022-02-15 11:17:29+08:00
draft: false
categories: [Tips]
tags: [debian]
---

#### 指定更新源

这个问题其实困扰我很久了，前两天才刚刚弄明白！ 起因是我想安装 [redis](http://redis.io/)，但是官方网站上没有 deb 包，同时 Debian 自带的比较旧了。 后来发现在 [dotdeb.org](https://www.dotdeb.org/) 有包，但是我只想安装其中的 redis，别的好像用默认的。

解决方案就是，新建一个文件 `/etc/apt/preferences.d/dotdeb.pref`，其内容如下：

```text
Package: *
Pin: release o=packages.dotdeb.org
Pin-Priority: 1

Package: redis-server
Pin: release o=packages.dotdeb.org
Pin-Priority: 900
```

下面解释下含义：

*   第一段是说把 `packages.dotdeb.org` 下的所有的包优先级设置成 **1**，就是比默认的低
*   第二段是说把 `redis-server` 这个包的优先级单独调成 **900**，就是比默认的高
*   经过如上设置，就会变成只有 `redis-server` 这个包使用 `packages.dotdeb.org` 源了