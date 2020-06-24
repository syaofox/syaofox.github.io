---
title: "FFMPEG 常用操作"
date: 2020-06-18T09:37:05+08:00
description: ""
tags: [FFMPEG]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Software
comment : false
draft: false 
author: "syaofox"
type: post
---

## 转码

```bash
ffmpeg -i out.ogv -vcodec h264 out.mp4
ffmpeg -i out.ogv -vcodec mpeg4 out.mp4
ffmpeg -i out.ogv -vcodec libxvid out.mp4
ffmpeg -i out.mp4 -vcodec wmv1 out.wmv
ffmpeg -i out.mp4 -vcodec wmv2 out.wmv
```
-i 后面是输入文件名。-vcodec 后面是编码格式，h264 最佳，但 Windows 系统默认不安装。如果是要插入 ppt 的视频，选择 wmv1 或 wmv2 基本上万无一失。

附加选项：-r 指定帧率，-s 指定分辨率，-b 指定比特率；于此同时可以对声道进行转码，-acodec 指定音频编码，-ab 指定音频比特率，-ac 指定声道数，例如
```bash
ffmpeg -i out.ogv -s 640x480 -b 500k -vcodec h264 -r 29.97 -acodec libfaac -ab 48k -ac 2 out.mp4
```
## 截取

用 -ss 和 -t 选项， 从第 30 秒开始，向后截取 10 秒的视频，并保存：
```bash
ffmpeg -i input.wmv -ss 00:00:30.0 -c copy -t 00:00:10.0 output.wmv
ffmpeg -i input.wmv -ss 30 -c copy -t 10 output.wmv
```
达成相同效果，也可以用 -ss 和 -to 选项， 从第 30 秒截取到第 40 秒:
```bash
ffmpeg -i input.wmv -ss 30 -c copy -to 40 output.wmv
```
值得注意的是，ffmpeg 为了加速，会使用关键帧技术， 所以有时剪切出来的结果在起止时间上未必准确。 通常来说，把 -ss 选项放在 -i 之前，会使用关键帧技术； 把 -ss 选项放在 -i 之后，则不使用关键帧技术。 如果要使用关键帧技术又要保留时间戳，可以加上 -copyts 选项：
```bash
ffmpeg -ss 00:01:00 -i video.mp4 -to 00:02:00 -c copy -copyts cut.mp4
```
## 合并

把两个视频文件合并成一个。
### 方法一
简单地使用 concat demuxer，示例：
```bash
$ cat mylist.txt
file '/path/to/file1'
file '/path/to/file2'
file '/path/to/file3'

$ ffmpeg -f concat -i mylist.txt -c copy output
```
更多时候，由于输入文件的多样性，需要转成中间格式再合成：
### 方法二
```shell
ffmpeg -i input1.avi -qscale:v 1 intermediate1.mpg
ffmpeg -i input2.avi -qscale:v 1 intermediate2.mpg
cat intermediate1.mpg intermediate2.mpg > intermediate_all.mpg
ffmpeg -i intermediate_all.mpg -qscale:v 2 output.avi
```
## 调速

### 加速四倍：
```bash
ffmpeg -i TheOrigin.mp4 -vf  "setpts=0.25*PTS" UpTheOrigin.mp4
```
### 四倍慢速：
```bash
ffmpeg -i TheOrigin.mp4 -vf  "setpts=4*PTS" DownTheOrigin.mp4
```
## 提取
### 增加字幕
```bash
ffmpeg -i video.avi -i sub.ass -map 0:0 -map 0:1 -map 1 -c:a copy -c:v copy -c:s copy video.mkv
```
### 提取字幕
```bash
ffmpeg -i input.mp4 -map 0:3 output.srt
```
### 提取视频
```bash
ffmpeg -i Life.of.Pi.has.subtitles.mkv -vcodec copy –an  videoNoAudioSubtitle.mp4
```
### 提取音频
```bash
ffmpeg -i Life.of.Pi.has.subtitles.mkv -vn -acodec copy audio.ac3
```
## 修改默认的音频轨道
```bash
ffmpeg -i input.mkv -map 0:0 -map 0:1 -map 0:2  -c copy -disposition:a:0 default -y output.mp4
```
输入文件包含一个视频轨道，两个音频轨道

0:0 表示视频轨道
0:1 表示第一个音频轨道
0:2 表示第二个音频轨道

`-c copy` 复制编码，也即是编码不变

最关键的，`-disposition:a:0 default`
设置音频轨道的第一个为默认值

## 设置音轨名称

```bash
ffmpeg -i in.mp4 -map 0:0 -map 0:1  -map 0:2 -map_metadata -1  -metadata:s:a:0  language=jpn -metadata:s:a:0 title="日语" -metadata:s:a:1 language=zho -metadata:s:a:1 title="国语"  -c copy -disposition:a:0 default out.mp4
```
[轨道编码参考链接](https://zh.wikipedia.org/wiki/ISO_639-2%E4%BB%A3%E7%A0%81%E8%A1%A8)

设定音轨名称是按照音轨顺序0,1类推,不是按照所有轨道顺序

## 清空元数据
```bash
ffmpeg -i in.mov -map_metadata -1 -c:v copy -c:a copy out.mov
```