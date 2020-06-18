---
title: "Youtube-dl 常用操作"
date: 2020-06-18T09:41:34+08:00
description: ""
tags: [Youtube-dl, software]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Software
comment : false
draft: false 
author: "syaofox"
type: post
---

## 调用外部下载工具下载列表

```bash
youtube-dl  "https://www.youtube.com/playlist?list=PL7enJ2-v6SPnQe5bqB0xupPSRpynhzH_E" --external-downloader aria2c --external-downloader-args "-x 16 -k 1M"
```

## 下载最好质量视频并指定格式

```bash
youtube-dl --format "bestvideo+bestaudio[ext=m4a]/bestvideo+bestaudio/best" --merge-output-format mp4
```

范例:下载最佳mp4和字幕

```bash 
youtube-dl --write-sub --sub-lang zh-CN,zh-TW --sub-format srt  --format "bestvideo+bestaudio[ext=m4a]/bestvideo+bestaudio/best" --merge-output-format mp4 "https://www.youtube.com/playlist?list=PL7enJ2-v6SPlgDsNHXJ1K2RpkZY2b_pm7"  --external-downloader aria2c --external-downloader-args "-x 16 -k 1M"
```