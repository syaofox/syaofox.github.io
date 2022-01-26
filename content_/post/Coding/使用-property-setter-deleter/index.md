---
title: "使用@property、setter、deleter"
date: 2022-01-10 18:26:52+08:00
description: ""
image: ""
categories: [Coding]
tags: [python]
---

在python中，我们需要对外暴露一个成员变量的时候，我们往往需要对外部输入的值进行判断，以确保是符合我们的期望的。

```arduino
class Student(object):
    age = 20
    
student = Student()
print student.age
student.age = "hello"
```

上述这种写法虽然可以取到age属性，但是同时也可以对age设置任意值。所以并不合理。

那怎么解决了，我们可以把age变成私有的成员变量。然后写一个getter用于供外部取得age值；一个setter函数用于供外部设置age值，并对age值进行一定的判断。  
例如：

```python
class Student(object):
    def __init__(self):
        self._age = None

    def age_getter(self):
        return self._age

    def age_setter(self, age):
        if isinstance(age, str) and age.isdigit():
            age = int(age)
        else:
            raise ValueError("age is illegal")
        if isinstance(age,int):
            self._age = age
```

那么我就需要`student.age_getter()`取得age，`student.age_setter()`设置age值。但是这样实现了功能，但是的确使得调用变得比较麻烦。有什么地方可以改进吗？

这个时候我们可以在`getter`和`setter`后面定义一个成员变量age。例如

```crmsh
age = property(age_getter, age_setter)
```

这样我们就可以把age当成一个Student的属性来调用和赋值了。  
例如：

```routeros
student.age = "20"
print student.age
```

你觉得python只能这么写getter和setter了，那就图样图森破了。python还有逆天的装饰器来实现getter、setter、和deleter。  
例如：

```python
class Student(object):
    def __init__(self):
        self._age = None

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if isinstance(age, int):
            self._age = age
            return
        if isinstance(age, str) and age.isdigit():
            age = int(age)
            self._age = age
        else:
            raise ValueError("age is illegal")

    @age.deleter
    def age(self):
        del self._age


student = Student()
student.age = 20
print student.age

del student.age
```

上面的例子中用@property、x.setter x.deleter实现了属性的读取、赋值、和删除。当然您也可以只是实现其中的一个或者几个。
