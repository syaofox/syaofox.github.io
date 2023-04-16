---
title: "python+playwright 学习-51 登录-验证码识别"
date: 2023-04-16 10:48:23+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

简单的登录验证码，数字和英文组合的，可以轻松识别

# 登录验证码

如下图登录验证码

![](assets/1681613303-61e1974b0e26008733cac86e6502cdf5.png)

验证码是一个图片链接，每次打开页面它会自动刷新

![](assets/1681613303-d948d250ce0a84aa74b735533e0603bd.png)

解决思路是先获取到验证码图片，获取验证码图片的方式，可以直接定位到img元素，对元素截图即可

```python
# 保存验证码  
page.locator('#imgCode').screenshot(path='yzm.png')
```

![](assets/1681613303-57cd2e7a923e576091c6323878621649.png)

最后使用ddddocr 快速识别

```python
import ddddocr


# 识别验证码  
ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化  
with open('yzm.png', 'rb') as f:  # 打开图片  
    img_bytes = f.read()  # 读取图片  
yzm = ocr.classification(img_bytes)  # 识别  
print(f'识别到的验证码: {yzm }')
```

# 代码示例

先安装ddddocr

```bash
pip install ddddocr -i https://pypi.douban.com/simple
```

完整代码

```python
"""  
简单的图像验证码  
"""  
from playwright.sync_api import sync_playwright  
import ddddocr  
  
  
with sync_playwright() as p:  
    browser = p.chromium.launch(headless=False)  
    context = browser.new_context()  
    page = context.new_page()  
  
    page.goto('https://www.xxx.com/login')  
    page.locator("#email").fill('123@qq.com')  
    page.locator('#pwd').fill('111111')  
    # 保存验证码  
    page.locator('#imgCode').screenshot(path='yzm.png')  
  
    # 识别验证码  
    ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化  
    with open('yzm.png', 'rb') as f:  # 打开图片  
        img_bytes = f.read()  # 读取图片  
    yzm = ocr.classification(img_bytes)  # 识别  
    print(f'识别到的验证码: {yzm }')  
  
    # 输入验证码  
    page.locator('#code').fill(yzm)  
  
  
    page.pause()
```

  



