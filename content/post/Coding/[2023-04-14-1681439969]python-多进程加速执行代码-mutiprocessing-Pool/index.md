---
title: "python 多进程加速执行代码 mutiprocessing Pool"
date: 2023-04-14 10:39:29+08:00
draft: false
categories: [Coding]
tags: [python,并发]
---

### 使用多进程可以高效利用自己的cpu, 绕过python的全局解释器锁

### 下面将对比接受Pool 常见一个方法：apply, apply\__async, map, mapasync ,imap, imap\_unordered_

_总结： apply因为是阻塞，所以没有加速效果，其他都有。_

_而imap\_unorderd 获取的结果是无序的，相对比较高效和方便。_

### `apply`(_func_\[,_args_\[,_kwds_\]\])

因为apply是阻塞的，需要等待上一个进程结束，下一个进程才开始，**所以无法加速**，除非你自己再结合线程使用，不过这样就麻烦了。

```plain
from multiprocessing import Pool
import time


def target(x, y):
    time.sleep(2)
    print(x, y, "----")
    return x + y


if __name__ == '__main__':
    p = Pool(2)
    args = [(1, 2), (3, 4)]
    start = time.time()
    for arg in args:
        ret = p.apply(target, arg)  # 会阻塞的
        print(ret)
    print(f"It takes {time.time() - start} seconds!")
```

运行结果：

```console
1 2 ----
3
3 4 ----
7
It takes 4.085192918777466 seconds!
```

### `apply_async`(_func_\[,_args_\[,_kwds_\[,_callback_\[,_error\_callback_\]\]\]\])

同相比apply这个是异步的，返回一个异步对象，可以使用.get方法等待结果 ， 如果不需结果不必获取。因为异步**有加速效果。**

```plain
from multiprocessing import Pool
import time


def target(x, y):
    time.sleep(2)
    print(x, y, "----")
    return x + y


if __name__ == '__main__':
    p = Pool(2)
    args = [(1, 2), (3, 4)]
    start = time.time()
    rets = []
    for arg in args:
        ret = p.apply_async(target, arg)
        rets.append(ret)
    for ret in rets:
        print(ret.get())  # get 会阻塞
    print(f"It takes {time.time() - start} seconds!")
```

运行结果：

```text
3 41  2---- 
----
3
7
It takes 2.079228639602661 seconds!
```

### `map`(_func_,_iterable_\[,_chunksize_\])

可以加速

```text
def target(arg):  # map 的话只接受一次参数
    x, y = arg
    time.sleep(2)
    print(x, y, "----")
    return x + y


if __name__ == '__main__':
    p = Pool(2)
    args = [(1, 2), (3, 4)]
    start = time.time()
    ret = p.map(target, args)  # 会阻塞
    print(ret)
    print(f"It takes {time.time() - start} seconds!")
```

运行结果

```text
1 2 ----
3 4 ----
[3, 7]
It takes 2.0831923484802246 seconds!
```

### `map_async`(_func_,_iterable_\[,_chunksize_\[,_callback_\[,_error\_callback_\]\]\])

```text
from multiprocessing import Pool
import time


def target(arg):  # map 的话只接受一次参数
    x, y = arg
    time.sleep(2)
    print(x, y, "----")
    return x + y


if __name__ == '__main__':
    p = Pool(2)
    args = [(1, 2), (3, 4)]
    start = time.time()
    ret = p.map_async(target, args)
    print(ret.get())  # 在这里阻塞
    print(f"It takes {time.time() - start} seconds!")
```

运行结果

```text
31  2 4---- ----
[3, 7]
It takes 2.0892012119293213 seconds!
```

### `imap`(_func_,_iterable_\[,_chunksize_\])

```text
from multiprocessing import Pool
import time


def target(arg):  # map 的话只接受一次参数
    x, y = arg
    time.sleep(2)
    print(x, y, "----")
    return x + y


if __name__ == '__main__':
    p = Pool(2)
    args = [(1, 2), (3, 4)]
    start = time.time()
    ret = p.imap(target, args)  # 不会阻塞
    print(ret)
    for i in ret:  # 这里会阻塞
        print(i)
    print(f"It takes {time.time() - start} seconds!")
```

运行结果

```text
<multiprocessing.pool.IMapIterator object at 0x00000204DA485EC8>
3 41  2---- 
----
3
7
It takes 2.091893434524536 seconds!
```

### `imap_unordered`(_func_,_iterable_\[,_chunksize_\])

**注意**： 这相对imap的话，结果是无序的，那个进程先结束，结果就先获得。而imap结果是有序的。

```text
from multiprocessing import Pool
import time


def target(arg):  # map 的话只接受一次参数
    x, y = arg
    time.sleep(5 - x)
    print(x, y, "----")
    return x + y


if __name__ == '__main__':
    p = Pool(2)
    args = [(1, 2), (3, 4)]
    start = time.time()
    ret = p.imap_unordered(target, args)  # 不会阻塞
    print(ret)
    for i in ret:  # 这里会阻塞
        print(i)
    print(f"It takes {time.time() - start} seconds!")
```

运行结果：

```text
<multiprocessing.pool.IMapUnorderedIterator object at 0x0000027499E45E48>
3 4 ----
7
1 2 ----
3
It takes 4.084959506988525 seconds!
```