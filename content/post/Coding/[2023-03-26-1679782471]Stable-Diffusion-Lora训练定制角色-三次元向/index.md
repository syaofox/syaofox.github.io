---
title: "Stable Diffusion Lora训练定制角色（三次元向）"
date: 2023-03-26 06:14:31+08:00
draft: false
categories: [Coding]
tags: [SDWebUI]
---

上一篇讲了如何训练二次元的人物。

总体来讲二次元人物算是最容易的了，当然有的冷门角色确实要花些心思，但是整体非常容易。

这篇就讲一下如何训练三次元的人物，三次元难就难在无法100%复刻出来原本角色，原因很多。基本上费很大力也不过8成左右。

我先说下为什么做不到高强度还原真人：

*   人的年龄会变化的，网上的素材其实他们脸一直在变；
*   人还会整容；
*   人会p图，而且p的图强度参数不同时候都不一样；
*   人拍摄的角度也不一样，我们细看不同时不同人拍的照片都不太一样，还有精修和路人照片都不一样；
*   人会化妆，妆容不一样；
*   如果脸要像还能做到，同时让身体也像，那就更加困难，训练一般得多步训练；

以上这些原因，使得网络要拟合一个让所有人都觉得高度还原的角色是十分困难的。更主要的还是三次元本身就比二次元难。

不过训练三次元和二次元除了数据处理之外，训练的其他步骤几乎一致，我也不就废话了。

首先我们先从网上找一堆图片，如果我们要做明星简直太容易了，我们直接到他们社交帐号爬。

图片不用太多，一定要质量高于数量，大概50张就可以不错的效果了。

然后我们要抠图，真人最好扣干净图，本身训练难度就大，所以我们尽量扣干净背景，让主体放在图片中间。训练人物一般要很多大头照，然后几张全身的照片（这点非常重要的，要不然就是大头娃娃）。如果搞不到合适的全身照，就用deepfake技术换脸，不需要很真实，反正神经网络能get到我们的意思。总之要高清贴脸的照片学细节，并且多个角度都要有，再搭配一些全身半身照，平衡人物大小。

打tags我建议真人使用BLIP。

打出来的标签是这样的：

```text
a woman with a peace sign in her hand and a white shirt on her shoulder and a black background
```

我们直接把主语 a woman，或者 a girl换成我们自定义的名字即可。由于我都扣了图，所以也没有啥背景描述。如下：

```text
XXXX with a peace sign in her hand and a white shirt on her shoulder and a black background
```

简单写了个脚本可以快速替换一下：

```plain
import os
new_word = "mizuki_yamashita"
for old in ["a woman", "a young girl", "a young woman", "a person", "a girl"]:
    for file in os.listdir("."):
        if file.endswith(".txt"):
            # 打开文件并读取内容
            with open(file, "r") as f:
                content = f.read()
            # 用新单词替换旧单词
            content = content.replace(old, new_word)
            # 重新写入文件
            with open(file, "w") as f:
                f.write(content)
```

然后就拿去训练啦。

实在不好拿图举例，总之真人比二次元难多了，但是更有意思。