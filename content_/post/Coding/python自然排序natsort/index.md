---
title: "Python自然排序natsort"
date: 2022-01-07 14:06:34+08:00
description: ""
image: ""
categories: [Coding]
tags: [python]
---

排序可以说是所有算法中最为基础的一个了，在[python](https://so.csdn.net/so/search?q=python)中只需要调用**sorted**函数就可以了，但是这个函数有一个缺点，就是它是按照从第一位开始的顺序排列的。意思是：

```python
wav_file = ['1.wav', '13.wav', '9.wav', '2.wav',"23.wav"]
sorted_file = sorted(wav_file)
print(sorted_file)

####['1.wav', '13.wav', '2.wav', '23.wav', '9.wav']
```

这和我们的需求是不一致的，因为我们所需要的是按照前面序号的顺序排列，为了解决这个问题，可以使用natsort包。

  

#### 安装

```bash
pip install natsort
```

  

#### 使用

```python
from natsort import natsorted
wav_file = ['1.wav', '13.wav', '9.wav', '2.wav',"23.wav"]
sorted_file = natsorted(wav_file)
print(sorted_file)

#### ['1.wav', '2.wav', '9.wav', '13.wav', '23.wav']
```

可以完美的解决问题
