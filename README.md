# syaofox's Blog

> 🎯 **心似白云常自在，意如流水任东西。**  
> 一个基于 GitHub Issues 的自动化博客系统，使用 GitHub Pages 托管

<p align='center'>
    <img src="https://badgen.net/github/issues/syaofox/syaofox.github.io"/>
    <img src="https://badgen.net/badge/last-commit/2025-10-15"/>
    <img src="https://badgen.net/github/forks/syaofox/syaofox.github.io"/>
    <img src="https://badgen.net/github/stars/syaofox/syaofox.github.io"/>
    <img src="https://badgen.net/github/watchers/syaofox/syaofox.github.io"/>
</p>

## 🌐 快速访问

- **博客地址**: [https://syaofox.github.io](https://syaofox.github.io)
- **项目仓库**: [https://github.com/syaofox/syaofox.github.io](https://github.com/syaofox/syaofox.github.io)

### ✨ 博客特色

- 📝 **GitHub Issues 作为 CMS** - 用 Issue 管理博客文章，支持 Markdown 格式
- 🏷️ **标签分类管理** - 通过 Labels 自动分类文章（tips、ACG、docker、apps）
- ☁️ **自动生成词云** - 基于文章内容智能生成词云图片
- 🤖 **全自动部署** - Issues 变更自动触发 GitHub Actions 部署
- 📱 **响应式设计** - 支持桌面和移动端访问

---

## 🚀 Fork 搭建指南

想要搭建自己的博客？按照以下步骤操作：

### Step 1: Fork 仓库

1. 点击右上角的 **Fork** 按钮
2. 选择你的 GitHub 账户作为目标
3. 仓库名称建议使用 `你的用户名.github.io`

### Step 2: 启用 GitHub Pages

1. 进入你的 Fork 仓库
2. 点击 **Settings** → **Pages**
3. 在 **Source** 中选择 **Deploy from a branch**
4. 选择 **gh-pages** 分支，**/ (root)** 目录
5. 点击 **Save** 保存配置

### Step 3: 配置 GitHub Secrets

在仓库 **Settings** → **Secrets and variables** → **Actions** 中添加以下 Secrets：

#### `BLOG_SECRET`
- 创建 GitHub Personal Access Token
- 访问：[GitHub Settings](https://github.com/settings/tokens) → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
- 权限选择：`repo`（完整仓库访问）、`workflow`（更新 GitHub Actions 工作流）
- 将生成的 token 复制到 `BLOG_SECRET`

#### `GIT_USERNAME`
- 你的 GitHub 用户名

#### `GIT_EMAIL`
- 你的 GitHub 邮箱地址

### Step 4: 修改仓库配置

1. 编辑 `env.example` 文件，将仓库名改为你的：
   ```bash
   GITHUB_REPOSITORY=你的用户名/你的仓库名
   ```

2. 本地测试时，复制 `env.example` 为 `.env` 并填入真实值

### Step 5: 触发首次部署

1. 创建任意一个 Issue 并添加标签（如 `tips`）
2. 系统会自动触发 GitHub Actions 部署
3. 几分钟后访问 `https://你的用户名.github.io/你的仓库名/` 查看效果

---

## 📖 使用说明

### 创建文章

1. 在仓库中点击 **Issues** → **New issue**
2. 标题作为文章标题，内容支持完整的 Markdown 语法
3. 添加对应的标签进行分类：
   - `tips` - 技术技巧和教程
   - `ACG` - 游戏和动漫相关内容
   - `docker` - Docker 相关技术
   - `apps` - 软件应用推荐

### 上传图片

1. 编辑 issue 时，从剪切板粘贴到文章编辑器里,会自动转为 github 附件
2. 网站生成时会自动抓取附件回本地，并推送到 gh-pages 对应图片资源目录

### 自动部署

- Issues 的任何变更（创建、编辑、添加标签等）都会自动触发部署
- 部署过程通常在 2-5 分钟内完成
- 可以在 **Actions** 标签页查看部署状态

---

## 💻 本地开发

### 环境要求

- Python >= 3.9
- [uv](https://github.com/astral-sh/uv) 包管理器

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 安装依赖
uv sync
```

### 运行脚本

```bash
# 生成博客内容
uv run python main.py

# 或运行重构后的模块
uv run python src/main.py
```

### 生成内容说明

脚本会自动：
- 从 GitHub API 获取所有 Issues 和 Labels
- 根据标签分类整理文章
- 使用 Jinja2 模板生成 HTML 文章页面
- 基于文章内容生成词云图片
- 更新 README.md 文件（如果启用了自动更新）

---

## 🛠️ 技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| **GitHub Issues** | 内容管理 | 作为 CMS 管理博客文章 |
| **GitHub Actions** | 自动化部署 | 监听 Issues 变更，自动构建部署 |
| **GitHub Pages** | 静态托管 | 免费托管静态网站 |
| **Python** | 后端逻辑 | 处理数据获取和内容生成 |
| **Jinja2** | 模板引擎 | 生成 HTML 页面 |
| **WordCloud** | 词云生成 | 基于文章内容生成词云图片 |
| **uv** | 包管理 | 快速的 Python 包管理器 |

## 📁 项目结构

```
├── src/                    # 核心代码模块
│   ├── core/              # 核心模块（配置、GitHub 客户端）
│   ├── models/            # 数据模型
│   ├── generators/        # 生成器（HTML、词云）
│   ├── utils/             # 工具模块
│   └── templates/         # Jinja2 模板
├── html/                  # 生成的静态网站
├── assets/                # 静态资源（图片、词云）
├── .github/workflows/     # GitHub Actions 工作流
├── pyproject.toml         # 项目配置和依赖
└── main.py               # 主程序入口
```

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

如果你觉得这个项目对你有帮助，请给它一个 ⭐ Star！