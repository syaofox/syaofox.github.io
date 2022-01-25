---
title: "Python Jinja2使用方法"
date: 2021-12-22T10:43:25+08:00 
description: ""
image: ""
categories: [Coding]
tags: [python]
---

说起Jinja2 想必每个资深的python程序猿都有所接触，因为它被作为了一些主流web框架(如Flask, Django)的数据渲染的底层调用，尤其是其模板语言，相当方便。

近期利用Jinja2完成了一个后台(Python)与前端(HTML)之间的数据交互，利用了Jinja2的模板语言，省下了相当于多的心思，下面就先分享一下我使用的模板语言主要有哪些，还有注意事项吧~~

一、 作为一个模板语言，它的主要优势是可以省去很多重复的前端代码，用类似于后台循环代码等方式来产生html，首先，需要读入一个带有模板语言的html 模板，类似于如下:

```html
<html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
            <p style='font-size:15px; font-family:Arial;'>{{ content }}</p>
            <table border="1" cellspacing="0" cellpadding="0">
            <tr>
                {% if array_table_head %}
                {% for var_i in array_table_head %}
                    <th style="font-size: 15px; padding: 3px;">{{var_i}}</th>
                {% endfor %}
                {% endif %}
            </tr>
            {% if dict_table_data %}
            {% for table_data in dict_table_data %}
            <tr>
                <th style="font-size: 12px; padding: 3px;">{{ table_data.Name }}</th>
                <th style="font-size: 12px; padding: 3px;">{{ table_data.Type }}</th>
                <th style="font-size: 12px; padding: 3px;">{{ table_data.Value }}</th>
            </tr>
            {% endfor %}
            {% endif %}
            </table>
    </body>
</html>
```

其中， 以{% %}包裹的为模板语句，语法和python神似，只有些许不同，详见[Jinja2官方文档](http://jinja.pocoo.org/docs/2.10/)(过滤器等)，以{{ }} 包裹的为变量引用，会被Jinja2解析为一个变量，即动态变化的数据。

二、加载模板

有了上述的html模板，后台利用如下代码读入。

```python
    import jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
    temp = env.get_template('statics/template.html')
```

注意一点: 其中path需要为当前python文件**所在目录**的完整路径，get\_template内部的参数为html模板相对于该python文件所在目录的路径(相对路径)。

三、模拟数据，对模板进行Render

通过第一部分的html模板中我们不难发现该模板一共需要三个变量，content、 array\_table\_head 以及 dict\_table\_data。所以我们需要在后台对这三个变量进行模拟。

1\. 类型分析。需要注意的是，变量的类型一定要把控好，从模板的观察可以看出content是直接用{{ }}包裹来引用的，所以在后台应该是一种可以直接取值的类型，例如str， int等。而array\_table\_head是通过遍历来引用的，说明最外层在后台是一个List或tuple等可遍历对象，其次在内层是直接取值的，所以后台应该是一个简单的str或者int的列表。同理，对于dict\_table\_data, 则是一个字典字符串，所以三个变量的模拟应该如下:

```python
    render_dict = {}
    dict_table_data = [{'Name': 'Basketball', 'Type': 'Sports', 'Value': 5},
                       {'Name': 'Football', 'Type': 'Sports', 'Value': 4.5},
                       {'Name': 'Pencil', 'Type': 'Learning', 'Value': 5},
                       {'Name': 'Hat', 'Type': 'Wearing', 'Value': 2}]
    render_dict.update({'Content': 'Hello reader, here is a table:',
                        'array_table_head': ['Name', 'Type', 'Value'],
                        'dict_table_data': dict_table_data})
```

2\. 模板渲染

最后一步，即通过render方法将变量放入模板中，然后生成新的html写入文件，此时，模板语言将会全部被转化为html。

```python
temp_out = temp.render(content=render_dict['Content'], 
                       array_table_head=render_dict['array_table_head'],
                       dict_table_data=render_dict['dict_table_data'])
with open(os.path.join(path, 'statics/out.html'), 'w', encoding='utf-8') as f:
    f.writelines(temp_out)
    f.close()
```

四、总结

Jinja2 对于html数据渲染有奇效，同时还具有许多优点：

(1)安全: 强大的 HTML 自动转义系统保护系统免受 XSS攻击。

(2)编译快速: 及时编译最优的 python 代码。

(3)易于调试。异常的行数直接指向模板中的对应行。

(4)具有模板继承的特性，减少大量的工作量。
