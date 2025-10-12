# 重构说明文档

## 重构概述

本次重构将原本 1512 行的单文件 `main.py` 重构为清晰的模块化架构，使用 Jinja2 模板引擎管理 HTML，大幅提高了代码的可维护性和复用性。

## 新架构

```
src/
├── core/                    # 核心模块
│   ├── config.py           # 配置管理
│   └── github_client.py    # GitHub API 交互
├── models/                  # 数据模型
│   └── article.py          # 文章数据模型
├── generators/              # 生成器模块
│   ├── html_generator.py   # HTML 生成器
│   ├── readme_generator.py # README 生成器
│   └── wordcloud_generator.py # 词云生成器
├── utils/                   # 工具模块
│   ├── file_utils.py       # 文件操作工具
│   └── text_utils.py       # 文本处理工具
├── templates/               # HTML 模板
│   ├── base.html           # 基础模板
│   ├── article.html        # 文章页面模板
│   └── index.html          # 首页模板
└── main.py                 # 主程序入口
```

## 主要改进

### 1. 模板分离
- 将 700+ 行 HTML/CSS/JS 代码提取到独立的 Jinja2 模板文件
- 使用模板继承和区块机制，避免代码重复
- 便于维护和修改样式

### 2. 职责分离
- **config.py**: 统一管理环境变量和配置
- **github_client.py**: 封装 GitHub API 交互，包含速率限制处理
- **article.py**: 定义文章数据模型，提供数据验证和格式化
- **html_generator.py**: 使用模板引擎生成 HTML 内容
- **readme_generator.py**: 生成 README.md 内容
- **wordcloud_generator.py**: 优化词云生成，减少 API 调用
- **file_utils.py**: 封装文件操作，提供错误处理
- **text_utils.py**: 封装文本处理，包括 Markdown 转换

### 3. 错误处理增强
- 添加完整的异常捕获和日志记录
- API 速率限制检查和自动等待
- 资源清理和连接管理

### 4. 代码复用
- 提取公共逻辑到工具函数
- 使用数据模型统一数据结构
- 模板继承减少重复代码

### 5. 可测试性
- 模块化设计便于单元测试
- 依赖注入模式便于模拟测试
- 清晰的接口定义

## 向后兼容

- 保留根目录的 `main.py` 作为入口点
- 保持现有的环境变量和配置方式
- 输出文件位置和格式保持不变
- 与 GitHub Actions 工作流完全兼容

## 使用方法

### 运行方式
```bash
# 使用 uv（推荐）
uv run python main.py

# 或直接使用 python
python main.py
```

### 环境变量
```bash
# 必需的环境变量
GITHUB_REPOSITORY=syaofox/syaofox.github.io
GITHUB_TOKEN=your_github_token

# 可选：本地开发时使用 .env 文件
echo "GITHUB_REPOSITORY=syaofox/syaofox.github.io" > .env
echo "GITHUB_TOKEN=your_token" >> .env
```

## 性能优化

1. **减少 API 调用**: 词云生成器现在使用缓存的文章数据，避免重复 API 请求
2. **批量处理**: 一次性获取所有数据，减少网络请求次数
3. **资源管理**: 正确关闭连接和清理资源
4. **错误恢复**: 单个文章生成失败不影响整体流程

## 开发指南

### 添加新功能
1. 在相应的模块中添加功能
2. 如需新的数据模型，在 `models/` 中定义
3. 如需新的工具函数，在 `utils/` 中添加
4. 如需新的生成器，在 `generators/` 中实现

### 修改模板
1. 修改 `src/templates/` 中的模板文件
2. 使用 Jinja2 语法进行动态内容渲染
3. 利用模板继承减少重复代码

### 调试
- 查看日志输出了解执行过程
- 使用 `uv run python -c "from src.core.config import config; print(config)"` 测试配置
- 单独测试各个模块的功能

## 技术栈

- **Python 3.9+**: 主开发语言
- **Jinja2**: 模板引擎
- **PyGithub**: GitHub API 客户端
- **Markdown**: Markdown 处理
- **WordCloud**: 词云生成
- **uv**: 包管理和虚拟环境

## 总结

重构后的代码具有以下优势：
- **可维护性**: 模块化设计，职责清晰
- **可扩展性**: 易于添加新功能和修改现有功能
- **可测试性**: 便于编写单元测试和集成测试
- **性能**: 优化了 API 调用和资源使用
- **用户体验**: 保持了原有的功能和界面

这次重构为项目的长期发展奠定了良好的基础，使得后续的维护和功能扩展变得更加容易。
