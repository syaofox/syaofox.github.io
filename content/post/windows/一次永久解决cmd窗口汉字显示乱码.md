---
title: "一次永久解决cmd窗口汉字显示乱码"
date: 2020-06-18T10:49:36+08:00
description: ""
tags: [cmd, 乱码]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Windows
comment : false
draft: false 
author: "syaofox"
type: post
---


对于编译出的程序，在 `cmd` 和 `power shell` 运行时都不能正确显示汉字。 
网上查，可以在命令窗口修改： 

1. 打开`CMD.exe`命令行窗口 
2. 通过 `chcp`命令改变代码页，`UTF-8`的代码页为`65001 `

```shell
chcp 65001
```
执行该操作后，代码页就被变成`UTF-8`了。
在当前窗口的确可以解决问题，但是**重新打开的`cmd`窗口或者`power shell` 窗口仍然不能正确显示汉字**。
最终发现，`cmd`的属性设置可以在注册表中修改，实现一次修改永远有效:

1. win+R 输入`regedit` 进入注册表 
2. 找到 `HKEY\_CURRENT\_USER\\Console\\%SystemRoot%\_system32\_cmd.exe` 如果 该项下已存在`CodePage`项，则把值改为十进制`65001`；如果不存在，在该项下新建一个 `DWORD`（32位值），命名为`CodePage`，值设为`65001`
3. 重启cmd后生效 
4. 对于`Power shell`修改同样，只需在第2步修改 `%SystemRoot%\_system32\_WindowsPowerShell\_v1.0\_powershell.exe` 下的项。

* * *

附录：

MS-DOS为以下国家和语言提供字符集：

| 代码 | 描述                   |
| :---: | :--------------------- |
| 1258 | 越南语                 |
| 1257 | 波罗的语               |
| 1256 | 阿拉伯语               |
| 1255 | 希伯来语               |
| 1254 | 土耳其语               |
| 1253 | 希腊语                 |
| 1252 | 拉丁 1 字符 (ANSI)     |
| 1251 | 西里尔语               |
| 1250 | 中欧语言               |
| 950  | 繁体中文               |
| 949  | 朝鲜语                 |
| 936  | 简体中文（默认）       |
| 932  | 日语                   |
| 874  | 泰国语                 |
| 850  | 多语种 (MS-DOS Latin1) |
| 437  | MS-DOS 美国英语        |
