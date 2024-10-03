---
title: "你可能没用过Requests自带重试功能"
date: 2024-10-03 22:58:35+08:00
draft: false
categories: [Coding]
tags: [python]
---


# 你可能没用过Requests自带重试功能

在 [Python](https://zhida.zhihu.com/search?content_id=248788631&content_type=Article&match_order=1&q=Python&zhida_source=entity) 开发中，Requests 是一个非常受欢迎的 HTTP 请求库。遇到网络波动或其他问题时，请求可能会失败，这时我们通常会进行重试。

常见的写法一般是：

```python
 def login():
     for a in range(3):
         try:
             return requests.get('https://www.baidu.com')
         except Exception as e:
             print(e)
             continue
```

一种更高级的方式是编写一个装饰器，以便于重用

```python
 def retry_request():
     def decorator(func):
         def wrapper(*args, **kwargs):
             for attempt in range(3):
                 try:
                     return func(*args, **kwargs)
                 except Exception as e:
                     if attempt == 2:  # 最后一次重试
                         raise e
         return wrapper
     return decorator
 ​
 @retry_request()
 def fetch_data(url):
     response = requests.get(url)
     response.raise_for_status()
     return response
```

实际上，Requests 提供了自带的重试功能。

Requests 依赖了 urllib3 这个依赖库进行网络请求的发送，Requests 在 urllib3 的基础上做了一层封装，可以通过 HTTPAdapter 类实现自动重试。

```python
 import logging
 ​
 import requests
 from requests.adapters import HTTPAdapter
 ​
 # 开启 urllib3 的日志，以便于查看重试过程
 logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
 urllib3_logger = logging.getLogger('urllib3')
 urllib3_logger.setLevel(logging.DEBUG)
 ​
 # 使用 session 发送请求
 session = requests.session()
 # 打印 adapters
 print(session.adapters)
 session.mount('https://', HTTPAdapter(max_retries=3))
 session.mount('http://', HTTPAdapter(max_retries=3))
 try:
     print(session.get('https://www.baidu.com', timeout=0.01).text[:100])
 except Exception as e:
     print(e)
     print(type(e))
```

以上代码中，开启了 urllib3 的日志，方便我们后面查看重试的过程，并且在 session 中覆盖了默认的adapters，添加了重试次数参数，为了方便复现，我将超时时间设置了很小的一个值，0.01，以确保一定会超时。

代码的运行结果为：

![](assets/1727967515-24062a6ab99fc9f28cf16eb40a58beee.svg)

从上面的图片中可以看出，首先urllib3 设置了两次重试参数（新建了两个 Retry 类），正好对应我们新建了两个 HTTPAdapter 类，然后向百度发送请求，在发生超时后，打印了日志并且设置重试次数为 2，然后继续重试。在 3 次重试后，打印了 URL 超过最大重试次数的错误，并且抛了一个 ConnectionError 异常。

![](assets/1727967515-88bf337b8cf8d41bc789ca53c57f580b.svg)

根据 `max_retries` 的文档说明，该参数仅适用于 DNS 查找、套接字连接和连接超时，而默认情况下并不会自动重试，需要手动设置。

也就是说它不会针对响应解析失败或者证书验证错误这些情况进行重试，这些情况需要我们手动处理。

其实，max\_retries 参数最终会作为 Retry 类的一个参数来生效，通过 Retry 类可以更加精细的控制重试条件和重试流程，这个我们后面再说。

在以后的开发中，如果使用 Requests 需要对网络问题进行重试，可以直接使用以下代码，简单而有效！

```python
 session.mount('https://', HTTPAdapter(max_retries=3))
 session.mount('http://', HTTPAdapter(max_retries=3))
```