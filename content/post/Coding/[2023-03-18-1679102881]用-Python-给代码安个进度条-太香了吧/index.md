---
title: "用 Python 给代码安个进度条，太香了吧！"
date: 2023-03-18 09:28:01+08:00
draft: false
categories: [Coding]
tags: [tqdm,python]
---

### 前言

* * *

今天和大家分享一个进度条可视化库，它的名字叫做 `tqdm` ，可以帮助我们监测程序运行的进度，用户只需要封装可迭代对象即可。

![image.png](assets/1679102881-d066e234e699996d63e6b5f167e0a78e.png "image.png")

  

### 安装

* * *

通过命令行直接安装。

```plain
pip install tqdm
复制代码
```

  

也可以使用豆瓣镜像安装。

```plain
pip install -i https://pypi.douban.com/simple tqdm
复制代码
```

  

执行上述命令后，可以检查一下是否安装成功。

```plain
pip show tqdm
复制代码
```

  

### 使用方式

* * *

**以下演示运行环境：`jupyter notebook`不同运行环境使用方式稍有不同，可根据警告自行调整。**

`tqdm` 主要参数可选参数众多，我们先看一下常用的一些参数。

  

**主要参数**

*   `iterable`: 可迭代的对象, 在手动更新时不需要进行设置
*   `desc`: str, 左边进度条的描述性文字
*   `total`: 总的项目数
*   `leave`: bool, 执行完成后是否保留进度条
*   `file`: 输出指向位置, 默认是终端, 一般不需要设置
*   `ncols`: 调整进度条宽度, 默认是根据环境自动调节长度, 如果设置为0, 就没有进度条, 只有输出的信息
*   `unit`: 描述处理项目的文字, 默认是'it', 例如: 100 it/s, 处理照片的话设置为'img' ,则为 100 img/s
*   `unit_scale`: 自动根据国际标准进行项目处理速度单位的换算, 例如 100000 it/s >> 100k it/s
*   `colour`: 进度条颜色，例如：'green', '#00ff00'。

  

#### 示例

直接将列表传入 `tqdm()`。

```plain
from tqdm.notebook import tqdm
from time import sleep
for char in tqdm(['C', 'Python', 'Java', 'C++']):
    sleep(0.25)
复制代码
```

![image.png](assets/1679102881-e85a99953e5a86c3daaa9bc3f15119a6.png "image.png")

  

使用可迭代对象。

```plain
for i in tqdm(range(100)):
    sleep(0.05)
复制代码
```

![image.png](assets/1679102881-3af2507d9f19fae7aa914019a5173f51.png "image.png")

  

`tqdm` 提供了 `trange()` 方法可以代替 `tqdm(range())`。

```plain
from tqdm.notebook import trange
for i in trange(100):
    sleep(0.05)
复制代码
```

![image.png](assets/1679102881-cc2204586d9abbac473e0ef96275832f.png "image.png")

  

我们在进度条前面添加描述性内容，这里把 `tqdm` 写在循环外，使用 `set_description()` 在进度条前面添加 "进度 %d"。

```plain
pbar = tqdm(range(5))
for char in pbar:
    pbar.set_description("进度 %d" %char)
    sleep(1)
复制代码
```

![image.png](assets/1679102881-91294bb1351617dc28fbd81267c0e962.png "image.png")

  

我们可以设置进度条的更新的间隔，下面我们设置总数为 `total=100`，然后分四次，使得进度条按 10%，20%，30%，40%的间隔来更新。

```plain
with tqdm(total=100) as pbar:
    for i in range(1, 5):
        sleep(1)
        # 更新进度
        pbar.update(10*i)
复制代码
```

![image.png](assets/1679102881-b289c6da7a18ae9b3a9405215a5bcb8d.png "image.png")

  

更改进度条颜色。

```plain
with tqdm(total=100, colour='pink') as pbar:
    for i in range(1, 5):
        sleep(1)
        # 更新进度
        pbar.update(10*i)
复制代码
```

![image.png](assets/1679102881-ff16f8789e70940600cd48dd497602c4.png "image.png")

  

注：在使用 `tqdm` 显示进度条的时候，如果想要输出内容的话不能够使用 `print` ，`print` 会导致输出多行进度条，可以使用 `tqdm.write()`。

```plain
for i in tqdm(range(5)):
  tqdm.write("come on")
  sleep(0.1)
复制代码
```

  

对于多重循环可以指定多个进度条，设置 `leave=False` 第二个循环执行完后，进度条不保存。

```plain
for i in trange(3, desc='1st loop'):
    for i in trange(100, desc='2nd loop', leave=False):
        sleep(0.01)
复制代码
```

![image.png](assets/1679102881-fdbb937542f8ca58808a912de651cef9.png "image.png")