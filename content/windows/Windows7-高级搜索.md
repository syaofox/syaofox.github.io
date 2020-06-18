---
title: "Windows7 高级搜索"
date: 2020-06-18T10:12:43+08:00
description: ""
tags: [Windows7, 搜索]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---

在 Windows 7 中进行搜索可以简单到只需在搜索框中键入几个字母，但也有一些高级搜索技术以供使用。在搜索文件时，您不一定得了解这些技巧，但这些技巧确实能提供一些帮助，具体取决于搜索的位置和搜索的对象。

# 一般搜索
如果知道文件类型，则可以在搜索框中仅输入文件扩展名（例如，“JPG”）。

# 添加运算符
细化搜索的一种方法是使用运算符 AND、OR 和 NOT。当您使用这些运算符时，需要以全大写字母键入。
```
AND
tropical AND island
```
查找同时包含“tropical”和“island”这两个单词（即使这两个单词位于文件中的不同位置）的文件。如果只进行简单的文本搜索，这种方式与键入“tropical island”所得到的结果相同。
```
NOT
tropical NOT island
```
查找包含“tropical”但不包含“island”单词的文件。
```
OR
tropical OR island
```
查找包含“tropical”或“island”单词的文件。

# 使用关键字细化搜索
更多用法参考 
微软官方文档 [Advanced Query Syntax](https://docs.microsoft.com/zh-cn/windows/win32/lwef/-search-2x-wds-aqsreference?redirectedfrom=MSDN)

| 关键字                              | 用途                                                         |
| ----------------------------------- | :----------------------------------------------------------- |
| System.FileName:~<"notes"           | 名称以“notes”开头的文件。~< 表示“开头”。                     |
| System.FileName:="quarterly report" | 名为“quarterly report”的文件。= 表示“完全匹配”。             |
| System.FileName:~="pro"             | 文件名包含单词“pro”或包含作为其他单词（例如“process”或“procedure”）一部分的字符 pro。~= 表示“包含”。 |
| System.Kind:<>picture               | 不是图片的文件。<> 表示“不是”。                              |
| System.DateModified:05/25/2010      | 在该日期修改的文件。您也可以键入“System.DateModified:2010”以查找在这一年中任何时间更改的文件。 |
| System.Author:~!"herb"              | 创建者的名字中不含“herb”的文件。~! 表示“不包含”。            |
| System.Keywords:"sunset"            | 标记了“sunset”一词的文件。                                   |
| System.Size:<1mb                    | 小于 1 MB 大小的文件。                                       |

**注意**

可以使用问号 (?) 作为单个字符的通配符，并使用星号 (\*) 作为任意数量的字符的通配符。
还可以使用运算符 AND、OR 和 NOT 合并搜索关键字。（注意如何使用括号改变搜索词的效果。）

| 关键字                                              | 用途                                                         |
| --------------------------------------------------- | :----------------------------------------------------------- |
| System.Author:Charlie AND Herb                      | 创建者为 Charlie 的文件以及文件名或任何文件属性中包括 Herb 的任何文件。 |
| System.Author:Charlie AND System.DateModified:>2009 | 仅查找 Charlie 在 2009 年以后创建的文件。                    |
| System.Author:(Charl\* AND Herb)                    | 将 Charles 和 Herb 或 Charlie 和 Herb 列为创建者的文件。     |
| System.Author:"Charlie Herb"                        | 创建者名字与此名字完全相同的文件。                           |