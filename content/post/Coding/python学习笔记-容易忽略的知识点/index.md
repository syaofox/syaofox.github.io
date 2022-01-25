---
title: "Python学习笔记 容易忽略的知识点"
date: 2022-01-12 20:57:19+08:00
description: ""
image: ""
categories: [Coding]
tags: [python,temp]
draft: false
---

## 作用域
Python 中只有模块（module），类（class）以及函数（def、lambda）才会引入新的作用域，其它的代码块（如 if/elif/else/、try/except、for/while等）是不会引入新的作用域的，也就是说这些语句内定义的变量，外部也可以访问，

## 切片
返回新的列表

## 环境变量模块
python-dotenv

## lambda
```python 
lambda param:returnvalue
```

## Mixins(多重继承)
```python
class Loggable:
    def __init__(self):
        self.title = ''
    def log(self):
        print('Log message from ' + self.title)

class Connection:
    def __init__(self):
        self.server = ''
    def connect(self):
        print('Connecting to database on ' + self.server)

# 继承自两个类
class SqlDatabase(Connection, Loggable): 
    def __init__(self):
        super().__init__()
        self.title = 'Sql Connection Demo'
        self.server = 'Some_Server'
        

def framework(item):
    if isinstance(item, Connection):
        item.connect()
    if isinstance(item, Loggable):
        item.log()

sql_connection = SqlDatabase() 
# just_logger = Loggable() 按需要传入类，实现不同功能
framework(sql_connection)

```

## pathlib
3.6以后自带的库，性能比`so.path`高

```python
# Python 3.6 or higher
# Grab the library
from pathlib import Path

# What is the current working directory?
cwd = Path.cwd()
print('\nCurrent working directory:\n' + str(cwd))

# Create full path name by joining path and filename
new_file = Path.joinpath(cwd, 'new_file.txt')
print('\nFull path:\n' + str(new_file))

# Check if file exists
print('\nDoes that file exist? ' + str(new_file.exists()) + '\n')


# Get the parent directory
parent = cwd.parent

# Is this a directory?
print('\nIs this a directory? ' + str(parent.is_dir()))

# Is this a file?
print('\nIs this a file? ' + str(parent.is_file()))

# List child directories
print('\n-----directory contents-----')
for child in parent.iterdir():
    if child.is_dir():
        print(child)

demo_file = Path(Path.joinpath(cwd, 'demo.txt'))

# Get the file name
print('\nfile name: ' + demo_file.name)

# Get the extension
print('\nfile suffix: ' + demo_file.suffix)

# Get the folder
print('\nfile folder: ' + demo_file.parent.name)

# Get the size
print('\nfile size: ' + str(demo_file.stat().st_size) + '\n')
```

## flush()
文件读写中的flush方法，用于立即将缓冲区的数据写入文件，但不写入磁盘

## timeit
计时
```python
from timeit import default_timer
start_time = default_timer()
...
elapsed_time = default_timer() - start_time
```

## async 异步

```python
from timeit import default_timer
import aiohttp
import asyncio

async def load_data(session, delay):
    print(f'Starting {delay} second timer')
    async with session.get(f'http://httpbin.org/delay/{delay}') as resp:
        text = await resp.text()
        print(f'Completed {delay} second timer')
        return text

async def main():
    # Start the timer
    start_time = default_timer()

    # Creating a single session
    async with aiohttp.ClientSession() as session:
        # Setup our tasks and get them running
        two_task = asyncio.create_task(load_data(session, 2))
        three_task = asyncio.create_task(load_data(session, 3))

        # Simulate other processing
        await asyncio.sleep(1)
        print('Doing other work')

        # Let's go get our values
        two_result = await two_task
        three_result = await three_task

        # Print our results
        elapsed_time = default_timer() - start_time
        print(f'The operation took {elapsed_time:.2} seconds')

asyncio.run(main())

```