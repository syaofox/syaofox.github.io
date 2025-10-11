# 改造记录

## 文章 HTML 页面生成功能

### 改造概述
将原有的仅生成 `index.html` 和 `README.md` 的功能扩展为：
- 继续生成 `index.html`（博客首页）
- 继续生成 `README.md`（Markdown 格式）
- **新增**：为每个 GitHub Issue 生成独立的 HTML 文章页面

### 新增功能

#### 1. 文章 HTML 生成
- 从 GitHub Issues 获取内容并转换为 HTML
- 使用 Python `markdown` 库渲染 Markdown 内容
- 支持代码高亮、表格、引用块等扩展功能

#### 2. 按标签分类存储
- 文章按标签分类存储在 `articles/{label}/` 目录下
- 无标签文章存储在 `articles/uncategorized/` 目录下
- 文件名格式：`{日期}-{标题slug}.html`

#### 3. 现代化样式
- 文章页面使用与首页一致的现代化 CSS 样式
- 响应式设计，支持移动端
- 包含返回首页链接和原始 GitHub Issue 链接

#### 4. 链接更新
- `index.html` 中的文章链接现在指向本地生成的 HTML 文件
- 而不是直接链接到 GitHub Issues

### 技术实现

#### 新增依赖
- `markdown>=3.4.0` - Markdown 转 HTML
- `pymdown-extensions>=9.0` - 扩展功能

#### 新增函数
- `title_to_slug()` - 标题转 URL 安全 slug
- `get_article_url()` - 生成文章本地 URL
- `generate_article_html()` - 生成文章 HTML 内容
- `save_article_html()` - 保存文章到指定目录

#### 工作流更新
- GitHub Actions 现在使用 `uv` 包管理器
- 自动安装新依赖并运行文章生成

### 文件结构
```
articles/
├── tips/
│   ├── 2025-10-03-Linux调整Swap文件大小指南.html
│   ├── 2025-10-03-设置ssh-key-免密登录github.html
│   └── ...
├── ACG/
│   ├── 2025-10-03-成人版大富翁华丽人生2.html
│   ├── 2025-10-03-夏日的回忆同级生2.html
│   └── ...
├── docker/
│   └── ...
└── uncategorized/
    └── (无标签文章)
```

### 使用方式
1. 在 GitHub Issues 中创建或编辑文章
2. GitHub Actions 自动触发
3. 系统自动生成所有文章的 HTML 页面
4. 访问 `https://syaofox.github.io/syaofox.github.io/` 查看博客
5. 点击文章标题访问独立的 HTML 文章页面
