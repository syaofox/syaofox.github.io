---
title: "pyinstaller 打包程序的相对路径问题"
date: 2021-12-27T20:23:07+08:00
description: ""
image: ""
categories: [Coding]
tags: [pyinstaller,python]
---
pyinstaller 打包py文件成exe文件，在没有[python](https://so.csdn.net/so/search?from=pc_blog_highlight&q=python)的机器上运行，执行打包后的程序，经常会出现程序使用的图标无法显示，程序使用的关联文件无法关联。或者，在打包的本机上运行正常，但是将打包后的程序放到其它机器上就有问题。这些现象都很有可能是由程序使用的文件路径发生改变产生的，因此在打包时候我们需要根据执行路径进行路径“冻结”。

## 使用绝对路径

在python代码中使用绝对路径调用外部文件可以保证打包时候路径可追溯，因此在本机上运行打包后程序基本没问题。但是当本机上对应路径的资源文件被改变，或者将打包程序应用到别的机器，都会出现搜索不到资源文件的问题。这种方式不是合适的打包发布python软件的方式。

## 使用冻结路径

增加一个py文件，例如叫

frozen\_dir.py

```python 
import sys  
import os  
   
def app\_path():  
    """Returns the base application path."""  
    if hasattr(sys, 'frozen'):  
        # Handles PyInstaller  
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录  
    return os.path.dirname(\_\_file\_\_)                 #没打包前的py目录

```

其中的app\_path()函数返回一个程序的执行路径，为了方便我们将此文件放在项目文件的根目录，通过这种方式建立了相对路径的关系。

源代码中使用路径时，以app\_path()的返回值作为基准路径，其它路径都是其相对路径。以本文中使用的python项目打包为例，如下所示

test.py

```python 
import os
import frozen_dir

def savelog(file,log):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    with open(file,'a',encoding='utf-8') as f:
        f.write(log+'\n')

if __name__=='__main__':
    file = frozen_dir.app_path()+r'\log\2.txt'
    print(file)
    savelog(file,'hello you')
    savelog(file,'文件路径%s' %(file))
```



## 注意：
1. `pyinstaller -D test.py` 生成exe文件有效
2. `pyinstaller -F test.py` 只生成单独exe文件无效
