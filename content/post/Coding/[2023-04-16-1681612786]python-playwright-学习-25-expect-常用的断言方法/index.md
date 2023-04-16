---
title: "python+playwright 学习-25 expect 常用的断言方法"
date: 2023-04-16 10:39:46+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

playwright 提供了一个 expect方法 用于断言

# expect 使用

| 断言 | 描述 |
| --- | --- |
| expect(locator).to\_be\_checked() | Checkbox is checked |
| expect(locator).to\_be\_disabled() | Element is disabled |
| expect(locator).to\_be\_editable() | Element is enabled |
| expect(locator).to\_be\_empty() | Container is empty |
| expect(locator).to\_be\_enabled() | Element is enabled |
| expect(locator).to\_be\_focused() | Element is focused |
| expect(locator).to\_be\_hidden() | Element is not visible |
| expect(locator).to\_be\_visible() | Element is visible |
| expect(locator).to\_contain\_text() | Element contains text |
| expect(locator).to\_have\_attribute() | Element has a DOM attribute |
| expect(locator).to\_have\_class() | Element has a class property |
| expect(locator).to\_have\_count() | List has exact number of children |
| expect(locator).to\_have\_css() | Element has CSS property |
| expect(locator).to\_have\_id() | Element has an ID |
| expect(locator).to\_have\_js\_property() | Element has a JavaScript property |
| expect(locator).to\_have\_text() | Element matches text |
| expect(locator).to\_have\_value() | Input has a value |
| expect(locator).to\_have\_values() | Select has options selected |
| expect(page).to\_have\_title() | Page has a title |
| expect(page).to\_have\_url() | Page has a URL |
| expect(api\_response).to\_be\_ok() | Response has an OK status |

to\_be\_checked()使用示例

```kotlin
from playwright.sync_api import expect

locator = page.get_by_label("Subscribe to newsletter")
expect(locator).to_be_checked()
```

to\_be\_visible()使用示例

```kotlin
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

from playwright.sync_api import expect

locator = page.locator('.my-element')
expect(locator).to_be_visible()
```

  



