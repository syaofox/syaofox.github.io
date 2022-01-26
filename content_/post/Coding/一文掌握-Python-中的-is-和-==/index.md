---
title: "一文掌握 Python 中的 \"is\" 和 \"==\""
date: 2022-01-07 18:30:50+08:00
description: ""
image: ""
categories: [Coding]
tags: [python]
---
## **引言**

Python 的 "is" 和 "==" 想必大家都不陌生，我们在比较变量和字面量时常常用到它们，可是它们的区别在哪里？什么情况下该用 `is`？什么情况下该用 `==`？这成了不少人心中的困惑。

当我们判断一个变量是否为 `None` 时，通常会用 `is`:

```python
>>> a = None
>>> a is None
True
>>> b = 1
>>> b is None
False
```

而当我们判断一个变量是否为字面量（比如某个数值）时，通常会用 `==`:

```python
>>> a = 0
>>> a == 0
True
>>> a == 1
False
```

要想解决上面的疑惑，我们首先需要搞明白 `is` 和 `==` 是什么。

## **"is" 和 "==" 是什么**

`is` 用来检查身份（identity）的同一性，即两个变量是否指向同一个对象。

`==` 用来检查值的相等性（equality），即两个变量的值是否相等。

身份的同一性同时也意味值的相等性，既然两个都指向同一个对象，那值就肯定相等。但是反之则不是。

### **\_\_eq\_\_ 魔法方法**

既然 `==` 是用来检查值的相等性，那么两个对象的值比较究竟是怎么进行的？

对于基本类型的对象的值比较，我们很容易理解。比如列表对象 \[1, 2, 3\] 的值比较就是比较列表的长度和列表中每个元素的值。

但是对于自定义的对象，该如何进行值比较？这里就涉及到了 `__eq__(self, other)` 魔法方法，我们可以通过该方法来实现对象的 `==` 逻辑。比如：

```python
>>> class Foo(object):
...   def __eq__(self, other):
...     return True
...
>>> foo = Foo()
>>> foo == 1
True
>>> foo == None
True
>>> foo is None
False
```

在上面的示例中，我们定义了 `Foo` 类，并实现了 `__eq__(self, other)` 方法，它永远返回 `True`，也就意味着和任何对象做值比较（`==`）结果都是 `True`。而当它做同一性比较时，比如和 `None` 比较，由于不是同一个对象，所以返回 `False`。

## **场景示例**

### **示例一：指向同一个对象的变量比较**

```python
>>> a = [1, 2, 3]
>>> b = a  # b 指向 a，a 指向 [1, 2, 3]，所以 b 指向同一个 [1, 2, 3]
>>> b is a
True
>>> b == a
True
```

在上述示例中 `a` 和 `b` 均指向同一个列表对象 `[1, 2, 3]`，所以对它们使用 `is` 和 `==`，结果都是 `True`。

### **示例二：指向不同对象（但值相同）的变量比较**

```python
>>> a = [1, 2, 3]
>>> b = a[:]  # b 复制了一份 a 所指向的列表，产生新的 [1, 2, 3]
>>> b is a
False
>>> b == a
True
```

在上述示例中，由于 `b` 指向的是 `a` 的副本，也就是说 `a` 和 `b` 指向两个不同的对象，所以对它们使用 `is` 的结果是 `False`。但由于值相等，使用 `==` 的结果就是 `True`。

### **示例三：指向字面量的变量比较**

```python
>>> a = 256
>>> b = 256  # 和 a 指向同一字面量 256
>>> a is b  # 表明指向同一对象
True
>>> a == b
True
>>>
>>> a = 257
>>> b = 257
>>> a == b
True
>>> a is b  # 表明指向不同对象
False
>>>
```

通常来说，两个变量指向字面量，它们的比较应该使用 `==`，而非 `is`，否则就可能有类似上述示例中的困惑。

在 Python 的交互解释器中，把可能频繁使用的整数对象规定在范围 `[-5, 256]` 之间，当它们创建好后就会被缓存下来。但凡是需要再用到它们时，就会从缓存中取，而不是重新创建对象。

*   当 `a` 和 `b` 都指向同一个字面量 `256` 时，`a is b` 返回 `True`。这是因为声明 `b = 256` 时，`256` 整数对象是从缓存中取的，而非重新创建，所以 `a` 和 `b` 指向同一个整数对象。
*   当 `a` 和 `b` 都指向同一个字面量 `257` 时，`a is b` 返回 `False`。这是因为声明 `b = 257` 时，`257` 整数对象没被缓存，是重新创建的，所以 `a` 和 `b` 指向不同的整数对象。

同理，如果字面量是字符串，结果也类似。

```python
>>> a = 'python.org'
>>> b = 'python.org'
>>> a is b
False
>>> a == b
True
>>> a = 'pythonorg'
>>> b = 'pythonorg'
>>> a is b
True
>>> a == b
True
```

## **Python 3.8 引入 `is` 比较字面量时报 SyntaxWarning**

鉴于使用 `is` 比较字面量其实是不正确的，在 Python 3.8 的 **release notes\[1\]** 中，引入如下内容：

> The compiler now produces a SyntaxWarning when identity checks (is and is not) are used with certain types of literals (e.g. strings, numbers). These can often work by accident in CPython, but are not guaranteed by the language spec. The warning advises users to use equality tests (== and !=) instead. (Contributed by Serhiy Storchaka in **bpo-34850\[2\]**.)  

因此，当我们使用 `is` 去比较数字、字符串等字面量时，就会报 `SyntaxWarning`：

```python
>>> x = 200
>>> x is 200
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
SyntaxWarning: "is" with a literal. Did you mean "=="?
```

## **总结**

说了这么多，其实我们只需要记住如下两点：

*   当要比较值是否相等时，请用 `==`。
*   当要比较是否是同一个对象时，请用 `is`。

### **参考资料**

\[1\]

Python 3.8 release notes: _[https://docs.python.org/3.8/whatsnew/3.8.html#changes-in-python-behavior](https://docs.python.org/3.8/whatsnew/3.8.html#changes-in-python-behavior)_

\[2\]

bpo-34850: _[https://bugs.python.org/issue34850](https://bugs.python.org/issue34850)_
