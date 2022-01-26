---
title: "两行代码，给 Python 脚本生成命令行"
date: 2022-01-06 09:17:43+08:00
description: ""
image: ""
categories: [Coding]
tags: [python]
---

有时候我们会有这样的一个需求：

我们定义了一个 Python 的方法，方法接收一些参数，但是调用的时候想将这些参数用命令行暴露出来。

比如说这里有个爬取方法：

```python
import requests

def scrape(url, timeout=10):
    response = requests.get(url, timeout=timeout)
    print(response.text)
```

这里定义了一个 scrape 方法，第一个参数接收 url，即爬取的网址，第二个参数接收 timeout，即指定超时时间。

调用的时候我们可能这么调用：

```python
scrape('https:///www.baidu.com', 10)
```

如果我们想改参数换 url，那就得改代码对吧。

所以有时候我们就想把这些参数用命令行暴露出来，这时候我们可能就用上了 argparse 等等的库，挨个声明各个参数是干嘛的，非常繁琐，代码如下：

```python
parser = argparse.ArgumentParser(description='Scrape Function')
parser.add_argument('url', type=str,
                    help='an integer for the accumulator')
parser.add_argument('timeout',  type=int,
                    help='sum the integers (default: find the max)')

if __name__ == '__main__':
    args = parser.parse_args()
    scrape(args.url, args.timeout)
```

这样我们才能顺利地使用命令行来调用这个脚本：

```python
python3 main.py https://www.baidu.com 10
```

是不是感觉非常麻烦？argparse 写起来又臭又长，想想就费劲。

## Fire

但接下来我们要介绍一个库，用它我们只需要两行代码就可以做到如上操作。

这个库的名字叫做Fire，它可以快速为某个 Python 方法或者类添加命令行的参数支持。

先看看安装方法，使用 pip3 安装即可：

```python
pip3 install fire
```

这样我们就安装好了。

## 使用

下面我们来看几个例子。

### 方法支持

第一个代码示例如下：

```python
import fire

def hello(name="World"):
  return "Hello %s!" % name

if __name__ == '__main__':
  fire.Fire(hello)
```

这里我们定义了一个 hello 方法，然后接收一个 name 参数，默认值是 World，接着输出了 Hello 加 name 这个字符串。

然后接着我们导入了 fire 这个库，调用它的 Fire 方法并传入 hello 这个方法声明，会发生什么事情呢？

我们把这段代码保存为 demo1.py，接着用 Python3 来运行一下：

```python
python3 demo1.py
```

运行结果如下：

```python
Hello World!
```

看起来并没有什么不同。

但我们这时候如果运行如下命令，就可以看到一些神奇的事情了：

```python
python3 demo1.py --help
```

运行结果如下：

```python
NAME
    demo1.py

SYNOPSIS
    demo1.py <flags>

FLAGS
    --name=NAME
        Default: 'World'
```

可以看到，这里它将 name 这个参数转化成了命令行的一个可选参数，我们可以通过 `—-name` 来替换 name 参数。

我们来试下：

```python
python3 demo1.py --name 123
```

这里我们传入了一个 name 参数是 123，这时候我们就发现运行结果就变成了如下内容：

```python
Hello 123!
```

是不是非常方便？我们没有借助 argparse 就轻松完成了命令行参数的支持和替换。

那如果我们将 name 这个参数的默认值取消呢？代码改写如下：

```python
import fire

def hello(name):
  return "Hello %s!" % name

if __name__ == '__main__':
  fire.Fire(hello)
```

这时候重新运行：

```python
python3 demo1.py --help
```

就可以看到结果变成了如下内容：

```python
NAME
    demo1.py

SYNOPSIS
    demo1.py NAME

POSITIONAL ARGUMENTS
    NAME

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

这时候我们发现 name 这个参数就变成了必传参数，我们必须在命令行里指定这个参数内容，调用就会变成如下命令：

```python
python3 demo1.py 123
```

运行结果还是一样的。

### 类支持

当然 fire 这个库不仅仅支持给方法添加命令行的支持，还支持给一个类添加命令行的支持。

下面我们再看一个例子：

```python
import fire

class Calculator(object):    
    def double(self, number):
        return 2 * number

if __name__ == '__main__':
    fire.Fire(Calculator)
```

我们把这个代码保存为 demo2.py，然后运行：

```python
python3 demo2.py
```

运行结果如下：

```python
NAME
    demo2.py

SYNOPSIS
    demo2.py COMMAND

COMMANDS
    COMMAND is one of the following:

     double
```

可以看到，这里它将 Calculator 这个类中的方法识别出来了，COMMAND 之一就是 double，我们试着调用下：

```python
python3 demo2.py double
```

运行结果如下：

```python
ERROR: The function received no value for the required argument: number
Usage: demo2.py double NUMBER

For detailed information on this command, run:
  demo2.py double --help
```

这里就说了，这里必须要指定另外一个参数，叫做 NUMBER，同时这个参数还是必填参数，我们试着加下：

```python
python3 demo2.py double 4
```

运行结果如下：

```python
8
```

这时候就可以达到正确结果了。

所以说，综合来看，fire 可以为一个类命令行，每个命令都对应一个方法的名称，同时在后面添加额外的可选或必选参数，加到命令行参数的后面。

## 重新改写

最后，让我们回过头来，给我们一开始定义的 scrape 方法添加命令行的参数支持：

```python
import requests
import fire

def scrape(url, timeout=10):
    response = requests.get(url, timeout=timeout)
    print(response.text)


if __name__ == '__main__':
    fire.Fire(scrape)
```

这样就可以了！省去了冗长的 argparse 的代码，是不是非常方便？

调用就是如下形式：

```python
NAME
    main.py

SYNOPSIS
    main.py URL <flags>

POSITIONAL ARGUMENTS
    URL

FLAGS
    --timeout=TIMEOUT
        Default: 10
```

这里说了，URL 是必传参数，timeout 是可选参数。

最后调用下：

```python
python3 main.py https://www.baidu.com
```

这样我们就可以轻松将 url 通过命令行传递过去了。

当然 timeout 还是可选值，我们可以通过 `—-timeout` 来指定 timeout 参数：

```python
python3 main.py https://www.baidu.com --timeout 5
```

这样两个参数就都能顺利赋值了，最后效果就是爬取百度，5 秒超时。

怎么样？是不是很方便？大家快用起来吧！