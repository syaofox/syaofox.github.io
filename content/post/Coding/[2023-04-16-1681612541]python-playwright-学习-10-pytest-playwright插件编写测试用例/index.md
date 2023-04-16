---
title: "python+playwright 学习-10.pytest-playwright插件编写测试用例"
date: 2023-04-16 10:35:41+08:00
draft: false
categories: [Coding]
tags: [playwright,python]
---

# 前言

pytest-playwright插件完美的继承了pytest 用例框架和playwright基础使用的封装，基本能满足工作中的常规需求了，不需要我们再做额外的插件开发。

# pytest-playwright 环境准备

Playwright 建议使用官方的 pytest-playwright 插件来编写端到端测试。它提供上下文隔离，开箱即用地在多个浏览器配置上运行。或者，您可以使用该库使用您喜欢的测试运行程序手动编写测试基础设施。Pytest 插件使用 Playwright 的同步版本，还有一个可通过库访问的异步版本。

开始安装 Playwright 并运行示例测试以查看它的实际效果。

```mipsasm
pip install pytest-playwright
```

安装所需的浏览器：

```mipsasm
playwright install
```

仅需这一步即可安装所需的浏览器，并且不需要安装驱动包了,解决了selenium启动浏览器，总是要找对应驱动包的痛点。

# 快速开始

test\_my\_application.py 使用以下代码在当前工作目录或子目录中创建一个文件：

```python
import re
from playwright.sync_api import Page, expect
# 上海悠悠 wx:283340479  
# blog:https://www.cnblogs.com/yoyoketang/

def test_homepage(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

    # create a locator
    get_started = page.get_by_role("link", name="Get started")

    # Expect an attribute "to be strictly equal" to the value.
    expect(get_started).to_have_attribute("href", "/docs/intro")

    # Click the get started link.
    get_started.click()

    # Expects the URL to contain intro.
    expect(page).to_have_url(re.compile(".*intro"))
```

默认情况下，测试将在 chromium 上运行。这可以通过 CLI 选项进行配置。  
测试以无头模式运行，这意味着在运行测试时不会打开浏览器 UI。测试结果和测试日志将显示在终端中。

```diff
>pytest test_my_application.py
=========== test session starts ==============
platform win32 -- Python 3.8.5, pytest-7.2.1, pluggy-1.0.0
rootdir: D:\demo\play_web\cases
plugins: base-url-2.0.0, playwright-0.3.0
collected 1 item                                                                                                         

test_my_application.py .         [100%]

============ 1 passed in 2.40s ===
```

如果想看到打开的浏览器运行，可以加上`--headed` 参数

```css
>pytest test_my_application.py --headed
```

# 编写用例

Playwright 提供了`expect` 将等待直到满足预期条件的功能。

```kotlin
import re
from playwright.sync_api import expect

expect(page).to_have_title(re.compile("Playwright"))
```

定位器是 Playwright 自动等待和重试能力的核心部分。定位器代表了一种随时在页面上查找元素的方法，并用于对诸如.click .filletc之类的元素执行操作。

```kotlin
from playwright.sync_api import expect

get_started = page.get_by_role("link", name="Get started")

expect(get_started).to_have_attribute("href", "/docs/installation")
get_started.click()
```

Playwright Pytest 插件基于测试装置的概念，例如传递到您的测试中的内置页面装置。  
由于浏览器上下文，页面在测试之间被隔离，这相当于一个全新的浏览器配置文件，每个测试都会获得一个全新的环境，即使在单个浏览器中运行多个测试也是如此。

```python
from playwright.sync_api import Page

def test_basic_test(page: Page):
  # ...
```

您可以使用各种 fixture 在测试之前或之后执行代码，并在它们之间共享对象。  
例如，具有自动使用 function 作用域的 fixture 类似于 beforeEach/afterEach。  
具有module自动使用功能的作用域fixture的行为类似于 `beforeAll/afterAll`，它在所有测试之前和之后运行。

```python
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("beforeEach")
    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")
    yield
    print("afterEach")

def test_main_navigation(page: Page):
    # Assertions use the expect API.
    expect(page).to_have_url("https://playwright.dev/")
```

# 运行测试用例

您可以运行单个测试、一组测试或所有测试。测试可以在一个浏览器或多个浏览器上运行。  
默认情况下，测试以无头方式运行，这意味着在运行测试时不会打开浏览器窗口，并且会在终端中看到结果。如果您愿意，可以使用--headed标志以引导模式运行测试。

默认在 Chromium 上运行测试

```undefined
pytest
```

运行单个测试文件

```undefined
pytest test_login.py
```

运行一组测试文件

```bash
pytest tests/todo-page/ tests/landing-page/
```

使用函数名运行测试

```bash
pytest -k "test_add_a_todo_item"
```

在引导模式下运行测试

```css
pytest --headed test_login.py
```

在特定浏览器上运行测试

```css
pytest test_login.py --browser webkit
```

在多个浏览器上运行测试

```css
pytest test_login.py --browser webkit --browser firefox
```

如果您的测试在具有大量 CPU 的机器上运行，您可以通过使用pytest-xdist一次运行多个测试来加快测试套件的整体执行时间：

```cpp
# install dependency
pip install pytest-xdist
# use the --numprocesses flag
pytest --numprocesses auto
```

根据测试的硬件和性质，您可以设置numprocesses为从2机器上的 CPU 数量到 CPU 数量之间的任何值。如果设置得太高，您可能会注意到意外行为。

# Pytest 插件参考

Playwright 提供了一个Pytest插件来编写端到端测试。要运行测试，请使用Pytest CLI。

```css
pytest --browser webkit --headed
```

如果你想自动添加 CLI 参数而不指定它们，你可以使用pytest.ini文件：

CLI 相关参数  
`--headed`：以有头模式运行测试（默认：无头）。  
`--browserchromium`：在不同的浏览器、firefox或中运行测试webkit。它可以指定多次（默认值：）chromium。  
`--browser-channel` 要使用的浏览器通道。  
`--slowmo`使用慢动作运行测试。  
`--device` 要模拟的设备。  
`--output`测试生成的工件目录（默认值：）test-results。  
`--tracing`是否为每个测试记录轨迹。on、off或retain-on-failure（默认值：off）。  
`--video`是否为每次测试录制视频。on、off或retain-on-failure（默认值：off）。  
`--screenshot`是否在每次测试后自动捕获屏幕截图。on、off或only-on-failure（默认值：off）。

# 内置fixture

Function scope:：  
这些固定装置在测试功能中请求时创建，并在测试结束时销毁。

*   context:用于测试的新浏览器上下文。
*   page:用于测试的新浏览器页面。

Session scope:  
这些固定装置在测试函数中请求时创建，并在所有测试结束时销毁。

*   playwright:playwright实例。
*   browser\_type:当前浏览器的BrowserType实例。
*   browser：由 Playwright 启动的浏览器实例。
*   browser\_name: 浏览器名称作为字符串。
*   browser\_channel: 浏览器通道作为字符串。
*   is\_chromium, is\_webkit, is\_firefox: 相应浏览器类型的布尔值。

自定义fixture选项  
对于browser和context ，使用以下fixture来定义自定义启动选项。

*   browser\_type\_launch\_args：覆盖browser\_type.launch()的启动参数。它应该返回一个字典。
*   browser\_context\_args：覆盖browser.new\_context()的选项。它应该返回一个字典。

# 编写用例示例

写个简单的用例

```python
# test_my_application.py
from playwright.sync_api import Page

def test_visit_admin_dashboard(page: Page):
    page.goto("/admin")
    # ...
```

使用带有--slowmo参数的 slow mo 运行测试。

```css
pytest --slowmo 100
```

skip 某个浏览器

```python
# test_my_application.py
import pytest

@pytest.mark.skip_browser("firefox")
def test_visit_example(page):
    page.goto("https://example.com")
    # ...
```

在指定浏览器上运行

```python
# conftest.py
import pytest

@pytest.mark.only_browser("chromium")
def test_visit_example(page):
    page.goto("https://example.com")
    # ...
```

指定浏览器

```css
pytest --browser-channel chrome
```

```python
# test_my_application.py
def test_example(page):
    page.goto("https://example.com")
```

# 配置base-url

使用base-url参数启动 Pytest。该pytest-base-url插件用于允许您从配设置基本 url。

```python
# test_my_application.py
def test_visit_example(page):
    page.goto("/admin")
    # -> Will result in http://localhost:8080/admin
```

运行

```csharp
pytest --base-url http://localhost:8080
```

# 其它

忽略https 错误

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True
    }
```

自定义浏览器窗口大小

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }
```

设置手机设备

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    iphone_11 = playwright.devices['iPhone 11 Pro']
    return {
        **browser_context_args,
        **iphone_11,
    }
```

或者通过 CLI指定参数`--device="iPhone 11 Pro"`

持久的 context

```python
# conftest.py
import pytest
from playwright.sync_api import BrowserType
from typing import Dict

@pytest.fixture(scope="session")
def context(
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict
):
    context = browser_type.launch_persistent_context("./foobar", **{
        **browser_type_launch_args,
        **browser_context_args,
        "locale": "de-DE",
    })
    yield context
    context.close()
```

使用它时，测试中的所有页面都是从持久上下文创建的  
  



