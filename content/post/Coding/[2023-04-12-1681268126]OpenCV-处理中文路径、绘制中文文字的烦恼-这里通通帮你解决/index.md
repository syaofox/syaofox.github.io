---
title: "OpenCV 处理中文路径、绘制中文文字的烦恼，这里通通帮你解决！"
date: 2023-04-12 10:55:26+08:00
draft: false
categories: [Coding]
tags: [opencv]
---

发布于2020-07-23 11:32:15阅读 3.9K0

在 OpenCV 中，由于编码的缘故，对于中文的处理并不是很友好，比如中文路径的图片读取和写入以及在图片上绘制中文文字等，这几个问题都是笔者经常遇到的，本文列出这几个问题的解决办法，希望能够帮助到大家。

### **读取中文路径的图片**

首先是中文路径的读取

一般我们使用 `cv2.imread` 进行图片的读取，但是一遇到中文，就会出现错误，如下：

```javascript
import cv2image = cv2.imread("F:\莫山山.jpg")print(image)cv2.imshow("image", image)cv2.waitKey(0)cv2.destroyAllWindows()
```

![](assets/1681268126-cee43b652707e631a02ea919e9bdfac9.png)

解决的方法如下：我们借助 `np.fromfile` 和 `cv2.imdecode` 来实现中文路径的读取

```javascript
import cv2import numpy as npimage = cv2.imdecode(np.fromfile(file="F:\莫山山.jpg", dtype=np.uint8), cv2.IMREAD_COLOR)# print(image)cv2.imshow("image", image)cv2.waitKey(0)cv2.destroyAllWindows()
```

![](assets/1681268126-8dff599f41962670d8497728d4f653ac.png)

其中 `np.fromfile` 代表的含义是**从文本或者二进制文件构造 array，参数：file 是文件名，参数 dtype 是数据类型，因为是图像，所以我们使用 np.uint8 格式其中 np.fromfile 有个 shape 属性，其值是文件的字节数**

![](assets/1681268126-25e4f71971069814f488f15ca819978e.png)

`cv2.imdecode` 的含义是从内存中的指定缓冲区读取图像，参数：buf 就是数据缓存了，即上面 np.fromfile 得到的内容，参数：flag 见下图，即读取什么样的图片 (彩色、灰度等)

![](assets/1681268126-5ca5f6069bc2166d5e16090eb3dfa884.png)

参考：https://vovkos.github.io/doxyrest-showcase/opencv/sphinx\_rtd\_theme/enum\_cv\_ImreadModes.html

### **保存中文路径的图片**

既然有读取，那就有写入中文路径图片的需求 通常我们使用的是 `cv2.imwrite` 保存图片，但是遇见中文路径时，就会出现编码错误或者保存失败（我在不同的电脑上进行过测试，如果保存成功了，得到的文件名会是乱码）。

```javascript
import cv2import numpy as nppath = "F:/莫山山.jpg"image = cv2.imdecode(np.fromfile(file=path, dtype=np.uint8), cv2.IMREAD_COLOR)cv2.imwrite("F:/莫山山2.jpg", image)
```

解决方法如下：上面我们读取用的是 `imdecode` 那么写入自然是 `imencode` 了

```javascript
import cv2import numpy as nppath = r"F:\莫山山.jpg"image = cv2.imdecode(np.fromfile(file=path, dtype=np.uint8), cv2.IMREAD_COLOR)dst = r"F:/莫山山2.jpg"cv2.imencode(ext='.jpg', img=image)[1].tofile(dst)
```

**`cv2.imencode` 中的参数：ext 是图片的扩展名，参数：img 就是 array 矩阵了。单独运行 `cv2.imencode('.jpg', image)` 得到的是一个元组（2 部分，第二部分才是 array），所以上面程序中有一个取 \[1\] 的操作**

![](assets/1681268126-20b91247584e7e0e7f5ea64dcacd5455.png)

### **在图像中绘制中文文字**

OpenCV 处理中另外一个中文会出现问题是在图上绘制中文文字，要想在图片上绘制文字，我们一般使用的是 `cv2.putText()` 函数，一个示例如下：

```javascript
import cv2import numpy as nppath = r"F:\莫山山.jpg"image = cv2.imdecode(np.fromfile(file=path, dtype=np.uint8), cv2.IMREAD_COLOR)dst = r"F:/莫山山2.jpg"font = cv2.FONT_HERSHEY_SIMPLEX  # 指定字体cv2.putText(image, 'Person', (60, 60), font, 2, (20, 20, 255), 2, cv2.LINE_AA)  # 绘制的图像，文字，文字左下角的坐标,字体，字体颜色，厚度等cv2.imshow("image", image)cv2.waitKey(0)cv2.destroyAllWindows()
```

绘制英文文字一般没什么问题

![](assets/1681268126-3b9bb2b73f0c5696852272603e0020fe.png)

但是一到绘制中文文字时，**小朋友你是否会有很多问号？？？？？**

![](assets/1681268126-d7273615f918abdb5f42874e0717f1c2.png)

OpenCV 内置的函数不能帮助我们解决这个问题，我们需要借助另外一个库 PIL（pillow） 不过实现起来会稍微有点麻烦。

```javascript
import cv2from PIL import Image, ImageDraw, ImageFontimport numpy as nppath = r"F:\莫山山.jpg"image = cv2.imdecode(np.fromfile(file=path, dtype=np.uint8), cv2.IMREAD_COLOR)font = ImageFont.truetype('STZHONGS.TTF', 40)  # 字体设置，Windows系统可以在 "C:\Windows\Fonts" 下查找img_PIL = Image.fromarray(image[..., ::-1])  # 转成 PIL 格式draw = ImageDraw.Draw(img_PIL)  # 创建绘制对象draw.text(xy=(60, 60), text="莫山山", font=font, fill=(255, 0, 0))image = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)  # 再转成 OpenCV 的格式，记住 OpenCV 中通道排布是 BGRcv2.imshow("image", image)cv2.waitKey(0)cv2.destroyAllWindows()
```
