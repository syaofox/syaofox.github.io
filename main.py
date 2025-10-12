#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import os
import time
import re
import urllib.parse
from datetime import datetime

from github import Github, Auth
from github.Issue import Issue
from github.Repository import Repository
from dotenv import load_dotenv
import markdown

from word_cloud import WordCloudGenerator


def title_to_slug(title):
    """将标题转换为URL安全的slug"""
    # 移除特殊字符，保留中文、英文、数字和连字符
    slug = re.sub(r'[^\w\u4e00-\u9fff\-]', '', title)
    # 将多个连字符替换为单个
    slug = re.sub(r'-+', '-', slug)
    # 移除首尾的连字符
    slug = slug.strip('-')
    return slug


def get_article_url(issue: Issue):
    """生成文章的本地URL路径"""
    # 获取第一个标签，如果没有标签则使用 'uncategorized'
    label = 'uncategorized'
    if issue.labels:
        label = issue.labels[0].name
    
    # 生成日期和标题slug
    date_str = issue.created_at.strftime("%Y-%m-%d")
    title_slug = title_to_slug(issue.title)
    
    # 生成文件名
    filename = f"{date_str}-{title_slug}.html"
    
    # 返回相对路径
    return f"articles/{label}/{filename}"


def generate_article_html(issue: Issue, md_instance):
    """生成单个文章的HTML内容"""
    # 重置 Markdown 实例状态（如果需要）
    md_instance.reset()
    
    # 转换 Markdown 内容为 HTML
    content_html = md_instance.convert(issue.body or '')
    
    # 获取标签信息
    labels_html = ""
    if issue.labels:
        labels_html = " ".join([f'<span class="label">{label.name}</span>' for label in issue.labels])
    
    # 生成完整的HTML页面
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{issue.title} - syaofox 的博客</title>
    <style>
        :root {{
            --bg-color: #fdfdfd;
            --text-color: #111;
            --border-color: #e8e8e8;
            --card-bg: #ffffff;
            --card-header-bg: #f7f7f7;
            --link-color: #2a7ae2;
            --muted-color: #828282;
            --search-bg: #ffffff;
            --search-border: #e8e8e8;
        }}
        
        body.dark-mode {{
            --bg-color: #1a1a1a;
            --text-color: #e0e0e0;
            --border-color: #333;
            --card-bg: #2a2a2a;
            --card-header-bg: #333;
            --link-color: #4a9eff;
            --muted-color: #999;
            --search-bg: #2a2a2a;
            --search-border: #333;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.5;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            margin-top: 20px;
            margin-bottom: 20px;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }}
        
        .header {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            transition: border-color 0.3s ease;
        }}
        
        .back-link {{
            display: inline-block;
            color: var(--link-color);
            text-decoration: none;
            margin-bottom: 15px;
            font-size: 0.9em;
            transition: color 0.3s ease;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        .article-title {{
            font-size: 2em;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 15px;
        }}
        
        .article-meta {{
            color: var(--muted-color);
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        
        .labels {{
            margin-top: 10px;
        }}
        
        .label {{
            display: inline-block;
            background: var(--card-header-bg);
            color: var(--text-color);
            padding: 4px 8px;
            border: 1px solid var(--border-color);
            font-size: 0.8em;
            margin-right: 5px;
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }}
        
        .article-content {{
            font-size: 1em;
            line-height: 1.6;
        }}
        
        .article-content h1,
        .article-content h2,
        .article-content h3,
        .article-content h4,
        .article-content h5,
        .article-content h6 {{
            color: var(--text-color);
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        .article-content h1 {{
            font-size: 1.8em;
            font-weight: 700;
        }}
        
        .article-content h2 {{
            font-size: 1.5em;
            font-weight: 700;
        }}
        
        .article-content h3 {{
            font-size: 1.3em;
            font-weight: 700;
        }}
        
        .article-content p {{
            margin-bottom: 15px;
        }}
        
        .article-content img {{
            max-width: 100%;
            height: auto;
            border: 1px solid var(--border-color);
            margin: 15px 0;
            transition: border-color 0.3s ease;
        }}
        
        .article-content pre {{
            background: var(--card-header-bg);
            border: 1px solid var(--border-color);
            padding: 15px;
            overflow-x: auto;
            margin: 15px 0;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }}
        
        .article-content code {{
            background: var(--card-header-bg);
            padding: 2px 6px;
            border: 1px solid var(--border-color);
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }}
        
        .article-content pre code {{
            background: none;
            border: none;
            padding: 0;
        }}
        
        .article-content blockquote {{
            border-left: 4px solid var(--border-color);
            margin: 15px 0;
            padding: 10px 20px;
            background: var(--card-header-bg);
            transition: background-color 0.3s ease, border-left-color 0.3s ease;
        }}
        
        .article-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        .article-content th,
        .article-content td {{
            border: 1px solid var(--border-color);
            padding: 10px;
            text-align: left;
            transition: border-color 0.3s ease;
        }}
        
        .article-content th {{
            background: var(--card-header-bg);
            font-weight: 600;
            transition: background-color 0.3s ease;
        }}
        
        .article-content ul,
        .article-content ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        .article-content li {{
            margin-bottom: 5px;
        }}
        
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            color: var(--muted-color);
            font-size: 0.9em;
            transition: border-color 0.3s ease, color 0.3s ease;
        }}
        
        .github-link {{
            color: var(--link-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .github-link:hover {{
            text-decoration: underline;
        }}
        
        /* 响应式设计 */
        @media (max-width: 767px) {{
            .container {{
                margin: 10px;
                padding: 15px;
            }}
            
            .article-title {{
                font-size: 1.5em;
            }}
            
            .article-content {{
                font-size: 0.9em;
            }}
        }}
        
        /* 代码块复制按钮样式 */
        .code-block-wrapper {{
            position: relative;
            display: inline-block;
            width: 100%;
        }}
        
        .copy-btn {{
            position: absolute;
            top: 8px;
            right: 8px;
            background: var(--card-header-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 8px;
            font-size: 0.8em;
            cursor: pointer;
            border-radius: 3px;
            opacity: 0.7;
            transition: all 0.3s ease;
            z-index: 10;
        }}
        
        .copy-btn:hover {{
            opacity: 1;
            background: var(--border-color);
        }}
        
        .copy-btn.copied {{
            background: #28a745;
            color: white;
            border-color: #28a745;
        }}
        
        .article-content pre:hover .copy-btn {{
            opacity: 1;
        }}
        
        @media (min-width: 1024px) {{
            .article-content {{
                max-width: 700px;
                margin: 0 auto;
            }}
        }}
        
        /* 滚动悬浮按钮样式 */
        .scroll-buttons {{
            position: fixed;
            right: 20px;
            bottom: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .scroll-btn {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(42, 122, 226, 0.9);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }}
        
        .scroll-btn:hover {{
            background: rgba(42, 122, 226, 1);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        .scroll-btn.visible {{
            opacity: 1;
            visibility: visible;
        }}
        
        .scroll-btn:active {{
            transform: translateY(0);
        }}
        
        /* 移动端适配 */
        @media (max-width: 767px) {{
            .scroll-buttons {{
                right: 15px;
                bottom: 15px;
            }}
            
            .scroll-btn {{
                width: 45px;
                height: 45px;
                font-size: 18px;
            }}
        }}
        
        /* 主题切换按钮样式 */
        .theme-toggle {{
            position: fixed;
            right: 20px;
            bottom: 90px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            background: var(--card-bg);
            color: var(--text-color);
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        .theme-toggle:active {{
            transform: translateY(0);
        }}
        
        .theme-icon {{
            width: 24px;
            height: 24px;
            fill: currentColor;
            transition: all 0.3s ease;
        }}
        
        .theme-icon.moon-icon {{
            display: none;
        }}
        
        body.dark-mode .theme-icon.sun-icon {{
            display: none;
        }}
        
        body.dark-mode .theme-icon.moon-icon {{
            display: block;
        }}
        
        /* 移动端适配主题按钮 */
        @media (max-width: 767px) {{
            .theme-toggle {{
                width: 45px;
                height: 45px;
                right: 15px;
                bottom: 75px;
            }}
            
            .theme-icon {{
                width: 22px;
                height: 22px;
            }}
        }}
        
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <a href="../../index.html" class="back-link">← 返回首页</a>
            <h1 class="article-title">{issue.title}</h1>
            <div class="article-meta">
                <div>创建时间：{issue.created_at.strftime("%Y-%m-%d %H:%M:%S")}</div>
                <div>更新时间：{issue.updated_at.strftime("%Y-%m-%d %H:%M:%S")}</div>
            </div>
            {f'<div class="labels">{labels_html}</div>' if labels_html else ''}
        </header>
        
        <main class="article-content">
            {content_html}
        </main>
        
        <footer class="footer">
            <p>本文原始链接：<a href="{issue.html_url}" class="github-link" target="_blank">GitHub Issue #{issue.number}</a></p>
        </footer>
    </div>
    
    <!-- 主题切换按钮 -->
    <button id="theme-toggle" class="theme-toggle" title="切换主题">
        <svg class="theme-icon sun-icon" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="5"/>
            <line x1="12" y1="1" x2="12" y2="3"/>
            <line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/>
            <line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg class="theme-icon moon-icon" viewBox="0 0 24 24" style="display: none;">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
    </button>
    
    <!-- 滚动悬浮按钮 -->
    <div class="scroll-buttons">
        <button class="scroll-btn" id="scroll-to-top" title="回到顶部">↑</button>
        <button class="scroll-btn" id="scroll-to-bottom" title="滚到底部">↓</button>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // 为所有代码块添加复制按钮
            const codeBlocks = document.querySelectorAll('pre > code');
            
            codeBlocks.forEach(function(codeBlock) {{
                // 跳过已经包装的代码块
                if (codeBlock.parentElement.classList.contains('code-block-wrapper')) {{
                    return;
                }}
                
                const pre = codeBlock.parentElement;
                const wrapper = document.createElement('div');
                wrapper.className = 'code-block-wrapper';
                
                // 创建复制按钮
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-btn';
                copyBtn.textContent = '复制';
                
                // 包装pre元素
                pre.parentElement.insertBefore(wrapper, pre);
                wrapper.appendChild(pre);
                wrapper.appendChild(copyBtn);
                
                // 添加复制功能
                copyBtn.addEventListener('click', function() {{
                    const text = codeBlock.textContent;
                    
                    // 使用现代Clipboard API
                    if (navigator.clipboard && navigator.clipboard.writeText) {{
                        navigator.clipboard.writeText(text).then(function() {{
                            showCopied(copyBtn);
                        }}).catch(function() {{
                            // 降级到传统方法
                            fallbackCopy(text, copyBtn);
                        }});
                    }} else {{
                        // 降级到传统方法
                        fallbackCopy(text, copyBtn);
                    }}
                }});
            }});
            
            function showCopied(btn) {{
                btn.textContent = '已复制';
                btn.classList.add('copied');
                
                setTimeout(function() {{
                    btn.textContent = '复制';
                    btn.classList.remove('copied');
                }}, 1500);
            }}
            
            function fallbackCopy(text, btn) {{
                // 创建临时文本区域
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                
                try {{
                    textArea.focus();
                    textArea.select();
                    document.execCommand('copy');
                    showCopied(btn);
                }} catch (err) {{
                    console.error('复制失败:', err);
                    btn.textContent = '复制失败';
                    setTimeout(function() {{
                        btn.textContent = '复制';
                    }}, 1500);
                }} finally {{
                    document.body.removeChild(textArea);
                }}
            }}
            
            // 滚动悬浮按钮功能
            const scrollToTopBtn = document.getElementById('scroll-to-top');
            const scrollToBottomBtn = document.getElementById('scroll-to-bottom');
            
            function updateScrollButtons() {{
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                const windowHeight = window.innerHeight;
                const documentHeight = document.documentElement.scrollHeight;
                
                // 显示/隐藏回到顶部按钮
                if (scrollTop > 300) {{
                    scrollToTopBtn.classList.add('visible');
                }} else {{
                    scrollToTopBtn.classList.remove('visible');
                }}
                
                // 显示/隐藏滚到底部按钮
                if (scrollTop + windowHeight < documentHeight - 300) {{
                    scrollToBottomBtn.classList.add('visible');
                }} else {{
                    scrollToBottomBtn.classList.remove('visible');
                }}
            }}
            
            // 监听滚动事件
            window.addEventListener('scroll', updateScrollButtons);
            
            // 回到顶部按钮点击事件
            scrollToTopBtn.addEventListener('click', function() {{
                window.scrollTo({{
                    top: 0,
                    behavior: 'smooth'
                }});
            }});
            
            // 滚到底部按钮点击事件
            scrollToBottomBtn.addEventListener('click', function() {{
                window.scrollTo({{
                    top: document.documentElement.scrollHeight,
                    behavior: 'smooth'
                }});
            }});
            
            // 初始化时检查按钮状态
            updateScrollButtons();
            
            // 主题切换功能
            const themeToggle = document.getElementById('theme-toggle');
            const body = document.body;
            
            // 更新词云图片
            function updateWordcloudImage(isDark) {{
                const wordcloudImg = document.getElementById('wordcloud-img');
                if (wordcloudImg) {{
                    const newSrc = isDark ? 'assets/wordcloud-dark.png' : 'assets/wordcloud-light.png';
                    if (wordcloudImg.src !== new URL(newSrc, window.location.href).href) {{
                        wordcloudImg.src = newSrc;
                        console.log('词云图片已切换至:', newSrc);
                    }}
                }} else {{
                    console.warn('未找到词云图片元素');
                }}
            }}
            
            // 初始化主题
            function initTheme() {{
                const savedTheme = localStorage.getItem('theme');
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                const isDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
                
                if (isDark) {{
                    body.classList.add('dark-mode');
                }} else {{
                    body.classList.remove('dark-mode');
                }}
                
                updateWordcloudImage(isDark);
            }}
            
            // 切换主题
            function toggleTheme() {{
                const isDarkMode = body.classList.contains('dark-mode');
                
                if (isDarkMode) {{
                    body.classList.remove('dark-mode');
                    localStorage.setItem('theme', 'light');
                    updateWordcloudImage(false);
                }} else {{
                    body.classList.add('dark-mode');
                    localStorage.setItem('theme', 'dark');
                    updateWordcloudImage(true);
                }}
            }}
            
            // 监听主题切换按钮点击
            themeToggle.addEventListener('click', toggleTheme);
            
            // 延迟初始化主题，确保 DOM 完全加载
            setTimeout(function() {{
                initTheme();
            }}, 100);
        }});
    </script>
</body>
</html>"""
    
    return html_content


def save_article_html(issue: Issue, html_content: str):
    """保存文章HTML到指定目录"""
    # 获取标签目录
    label = 'uncategorized'
    if issue.labels:
        label = issue.labels[0].name
    
    # 创建目录
    articles_dir = f"articles/{label}"
    os.makedirs(articles_dir, exist_ok=True)
    
    # 生成文件名
    date_str = issue.created_at.strftime("%Y-%m-%d")
    title_slug = title_to_slug(issue.title)
    filename = f"{date_str}-{title_slug}.html"
    
    # 直接使用原始文件名，覆盖已存在的文件
    filepath = os.path.join(articles_dir, filename)
    
    # 写入文件
    with codecs.open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        f.flush()
        f.close()
    
    return filepath


def load_env_file():
    """加载 .env 文件中的环境变量（仅限本地开发）"""
    # 检查是否在 GitHub Actions 环境中运行
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("检测到 GitHub Actions 环境，跳过 .env 文件加载")
        return
    
    env_file = ".env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"已加载环境变量文件: {env_file}")
    else:
        print("未找到 .env 文件，使用系统环境变量")

user: Github
user_name: str
blog_repo: Repository
cur_time: str
blog_name: str


def login():
    global user, user_name, blog_name, blog_repo
    github_repo_env = os.environ.get("GITHUB_REPOSITORY")
    user_name = github_repo_env[0 : github_repo_env.index("/")]
    blog_name = github_repo_env[github_repo_env.index("/") :]
    password = os.environ.get("GITHUB_TOKEN")
    user = Github(auth=Auth.Token(password))
    blog_repo = user.get_repo(github_repo_env)
    print(blog_repo)


def bundle_summary_section():
    global blog_repo
    global cur_time
    global user
    global user_name
    global blog_name

    summary_section = """
<p align='center'>
    <img src="https://badgen.net/github/issues/{0}{1}"/>
    <img src="https://badgen.net/badge/last-commit/{2}"/>
    <img src="https://badgen.net/github/forks/{0}{1}"/>
    <img src="https://badgen.net/github/stars/{0}{1}"/>
    <img src="https://badgen.net/github/watchers/{0}{1}"/>
</p>

    """.format(user_name, blog_name, cur_time)
    return summary_section


def format_issue(issue: Issue):
    return "- %s [%s](%s) \n" % (
        issue.created_at.strftime("%Y-%m-%d"),
        issue.title,
        issue.html_url,
    )


def update_readme_md_file(contents):
    with codecs.open("README.md", "w", encoding="utf-8") as f:
        f.writelines(contents)
        f.flush()
        f.close()


def update_index_html_file(html_content):
    with codecs.open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        f.flush()
        f.close()


def bundle_list_by_labels_section(wordcloud_image_url, all_labels, all_issues):
    global blog_repo
    global user
    global user_name
    global blog_name

    list_by_labels_section = """
<summary>
    <a href="https://%s.github.io/%s/"><img src="%s" title="词云" alt="词云"></a>
</summary>  
""" % (user_name, blog_name, wordcloud_image_url)

    # 使用缓存数据按 label 分组 issues
    label_issues_map = {}
    for issue in all_issues:
        if issue.labels:
            for label in issue.labels:
                if label.name not in label_issues_map:
                    label_issues_map[label.name] = []
                label_issues_map[label.name].append(issue)
        else:
            # 没有标签的 issues 归类到 uncategorized
            if 'uncategorized' not in label_issues_map:
                label_issues_map['uncategorized'] = []
            label_issues_map['uncategorized'].append(issue)

    for label in all_labels:
        temp = ""
        issues_in_label = label_issues_map.get(label.name, [])
        count = len(issues_in_label)
        for issue in issues_in_label:
            temp += format_issue(issue)
        
        if count > 0:
            list_by_labels_section += """
<details open>
<summary>%s\t[%s篇]</summary>

%s

</details>
            """ % (label.name, count, temp)

    return list_by_labels_section


def bundle_html_content(all_labels, all_issues):
    global blog_repo, user_name, blog_name, cur_time
    
    # 构建徽章HTML
    badges_html = f"""
    <div class="badges">
        <img src="https://badgen.net/github/issues/{user_name}{blog_name}" alt="Issues"/>
        <img src="https://badgen.net/badge/last-commit/{cur_time}" alt="Last Commit"/>
        <img src="https://badgen.net/github/forks/{user_name}{blog_name}" alt="Forks"/>
        <img src="https://badgen.net/github/stars/{user_name}{blog_name}" alt="Stars"/>
        <img src="https://badgen.net/github/watchers/{user_name}{blog_name}" alt="Watchers"/>
    </div>"""
    
    # 构建词云HTML (作为banner)
    wordcloud_html = f"""
    <div class="wordcloud-banner">
        <a href="https://{user_name}.github.io/{blog_name}/">
            <img id="wordcloud-img" src="assets/wordcloud-light.png" title="词云" alt="词云" class="wordcloud-img">
        </a>
    </div>"""
    
    # 构建搜索框HTML
    search_html = f"""
    <div class="search-section">
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="搜索文章标题...">
            <button type="button" id="clearButton" class="clear-button" style="display: none;">×</button>
        </div>
    </div>"""
    
    # 使用缓存数据按 label 分组 issues
    label_issues_map = {}
    for issue in all_issues:
        if issue.labels:
            for label in issue.labels:
                if label.name not in label_issues_map:
                    label_issues_map[label.name] = []
                label_issues_map[label.name].append(issue)
        else:
            # 没有标签的 issues 归类到 uncategorized
            if 'uncategorized' not in label_issues_map:
                label_issues_map['uncategorized'] = []
            label_issues_map['uncategorized'].append(issue)
    
    # 收集所有标签和对应的文章数量，按文章数量排序
    label_counts = []
    for label in all_labels:
        label_name = label.name
        count = len(label_issues_map.get(label_name, []))
        label_counts.append((label, count))
    
    # 按文章数量降序排序
    label_counts.sort(key=lambda x: x[1], reverse=True)
    
    # 构建标签分类HTML
    issues_html = ""
    for label, count in label_counts:
        if count > 0:
            temp = ""
            issues_in_label = label_issues_map.get(label.name, [])
            for issue in issues_in_label:
                temp += f"""
            <div class="issue-item">
                <span class="issue-date">{issue.created_at.strftime("%Y-%m-%d")}</span>
                <a href="{get_article_url(issue)}" class="issue-link">{issue.title}</a>
            </div>"""
            
            issues_html += f"""
            <div class="category-card">
                <div class="category-header">
                    <h3 class="category-title">{label.name}</h3>
                    <span class="category-count">[{count}篇]</span>
                </div>
                <div class="issues-list">
                    {temp}
                </div>
            </div>"""
    
    # 完整的HTML结构
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{user_name} 的博客</title>
    <style>
        :root {{
            --bg-color: #fdfdfd;
            --text-color: #111;
            --border-color: #e8e8e8;
            --card-bg: #ffffff;
            --card-header-bg: #f7f7f7;
            --link-color: #2a7ae2;
            --muted-color: #828282;
            --search-bg: #ffffff;
            --search-border: #e8e8e8;
        }}
        
        body.dark-mode {{
            --bg-color: #1a1a1a;
            --text-color: #e0e0e0;
            --border-color: #333;
            --card-bg: #2a2a2a;
            --card-header-bg: #333;
            --link-color: #4a9eff;
            --muted-color: #999;
            --search-bg: #2a2a2a;
            --search-border: #333;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.5;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .wordcloud-banner {{
            text-align: center;
            margin: 0 0 20px 0;
        }}
        
        .wordcloud-img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        
        .badges {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .badges img {{
            height: 20px;
            border-radius: 3px;
        }}
        
        .search-section {{
            text-align: center;
            margin: 20px 0 30px 0;
        }}
        
        .search-container {{
            position: relative;
            display: inline-block;
            width: 100%;
            max-width: 600px;
        }}
        
        .search-input {{
            width: 100%;
            padding: 12px 40px 12px 20px;
            font-size: 1em;
            border: 1px solid var(--search-border);
            border-radius: 4px;
            outline: none;
            box-sizing: border-box;
            background-color: var(--search-bg);
            color: var(--text-color);
            transition: border-color 0.3s ease, background-color 0.3s ease;
        }}
        
        .search-input:focus {{
            border-color: var(--link-color);
        }}
        
        .clear-button {{
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 18px;
            color: var(--muted-color);
            cursor: pointer;
            padding: 4px;
            line-height: 1;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        .clear-button:hover {{
            background-color: var(--border-color);
            color: var(--text-color);
        }}
        
        .hidden {{
            display: none !important;
        }}
        
        .categories-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: 1fr;
        }}
        
        .category-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            overflow: hidden;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }}
        
        .category-header {{
            background: var(--card-header-bg);
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-color);
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }}
        
        .category-title {{
            font-size: 1.1em;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 5px;
        }}
        
        .category-count {{
            color: var(--muted-color);
            font-size: 0.9em;
        }}
        
        .issues-list {{
            padding: 20px;
        }}
        
        .issue-item {{
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .issue-item:last-child {{
            border-bottom: none;
        }}
        
        .issue-date {{
            color: var(--muted-color);
            font-size: 0.9em;
            min-width: 80px;
            margin-right: 15px;
        }}
        
        .issue-link {{
            color: var(--link-color);
            text-decoration: none;
            flex: 1;
            transition: color 0.3s ease;
        }}
        
        .issue-link:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: var(--muted-color);
            font-size: 0.9em;
        }}
        
        /* 响应式设计 */
        @media (max-width: 767px) {{
            .container {{
                padding: 15px;
            }}
            
            .badges {{
                gap: 5px;
            }}
            
            .badges img {{
                height: 18px;
            }}
            
            .search-input {{
                padding: 10px 35px 10px 15px;
                font-size: 0.9em;
            }}
            
            .clear-button {{
                right: 6px;
                font-size: 16px;
                width: 22px;
                height: 22px;
            }}
            
            .categories-grid {{
                gap: 15px;
            }}
            
            .issue-item {{
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }}
            
            .issue-date {{
                min-width: auto;
                margin-right: 0;
            }}
        }}
        
        @media (min-width: 768px) and (max-width: 1023px) {{
            .categories-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (min-width: 1024px) {{
            .categories-grid {{
                grid-template-columns: 1fr;
            }}
            
            .category-card {{
                margin-bottom: 20px;
            }}
        }}
        
        /* 主题切换按钮样式 */
        .theme-toggle {{
            position: fixed;
            right: 20px;
            bottom: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            background: var(--card-bg);
            color: var(--text-color);
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        .theme-toggle:active {{
            transform: translateY(0);
        }}
        
        .theme-icon {{
            width: 24px;
            height: 24px;
            fill: currentColor;
            transition: all 0.3s ease;
        }}
        
        .theme-icon.moon-icon {{
            display: none;
        }}
        
        body.dark-mode .theme-icon.sun-icon {{
            display: none;
        }}
        
        body.dark-mode .theme-icon.moon-icon {{
            display: block;
        }}
        
        /* 移动端适配 */
        @media (max-width: 767px) {{
            .theme-toggle {{
                width: 45px;
                height: 45px;
                right: 15px;
                bottom: 15px;
            }}
            
            .theme-icon {{
                width: 22px;
                height: 22px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <main>
            {badges_html}
            {wordcloud_html}
            {search_html}
            
            <section class="categories-grid">
                {issues_html}
            </section>
        </main>
        
        <footer class="footer">
            <p>最后更新：{cur_time}</p>
        </footer>
    </div>
    
    <!-- 主题切换按钮 -->
    <button id="theme-toggle" class="theme-toggle" title="切换主题">
        <svg class="theme-icon sun-icon" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="5"/>
            <line x1="12" y1="1" x2="12" y2="3"/>
            <line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/>
            <line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg class="theme-icon moon-icon" viewBox="0 0 24 24" style="display: none;">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
    </button>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const searchInput = document.getElementById('searchInput');
            const clearButton = document.getElementById('clearButton');
            const categoryCards = document.querySelectorAll('.category-card');
            
            function toggleClearButton() {{
                if (searchInput.value.trim() !== '') {{
                    clearButton.style.display = 'flex';
                }} else {{
                    clearButton.style.display = 'none';
                }}
            }}
            
            function performSearch() {{
                const searchTerm = searchInput.value.toLowerCase().trim();
                
                categoryCards.forEach(card => {{
                    const issueItems = card.querySelectorAll('.issue-item');
                    let hasVisibleItems = false;
                    
                    issueItems.forEach(item => {{
                        const title = item.querySelector('.issue-link').textContent.toLowerCase();
                        if (searchTerm === '' || title.includes(searchTerm)) {{
                            item.classList.remove('hidden');
                            hasVisibleItems = true;
                        }} else {{
                            item.classList.add('hidden');
                        }}
                    }});
                    
                    // 隐藏没有匹配项的分类卡片
                    if (hasVisibleItems) {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }});
            }}
            
            searchInput.addEventListener('input', function() {{
                toggleClearButton();
                performSearch();
            }});
            
            clearButton.addEventListener('click', function() {{
                searchInput.value = '';
                searchInput.focus();
                toggleClearButton();
                performSearch();
            }});
            
            // 初始化时检查是否需要显示清空按钮
            toggleClearButton();
            
            // 主题切换功能
            const themeToggle = document.getElementById('theme-toggle');
            const body = document.body;
            
            // 更新词云图片
            function updateWordcloudImage(isDark) {{
                const wordcloudImg = document.getElementById('wordcloud-img');
                if (wordcloudImg) {{
                    const newSrc = isDark ? 'assets/wordcloud-dark.png' : 'assets/wordcloud-light.png';
                    if (wordcloudImg.src !== new URL(newSrc, window.location.href).href) {{
                        wordcloudImg.src = newSrc;
                        console.log('词云图片已切换至:', newSrc);
                    }}
                }} else {{
                    console.warn('未找到词云图片元素');
                }}
            }}
            
            // 初始化主题
            function initTheme() {{
                const savedTheme = localStorage.getItem('theme');
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                const isDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
                
                if (isDark) {{
                    body.classList.add('dark-mode');
                }} else {{
                    body.classList.remove('dark-mode');
                }}
                
                updateWordcloudImage(isDark);
            }}
            
            // 切换主题
            function toggleTheme() {{
                const isDarkMode = body.classList.contains('dark-mode');
                
                if (isDarkMode) {{
                    body.classList.remove('dark-mode');
                    localStorage.setItem('theme', 'light');
                    updateWordcloudImage(false);
                }} else {{
                    body.classList.add('dark-mode');
                    localStorage.setItem('theme', 'dark');
                    updateWordcloudImage(true);
                }}
            }}
            
            // 监听主题切换按钮点击
            themeToggle.addEventListener('click', toggleTheme);
            
            // 延迟初始化主题，确保 DOM 完全加载
            setTimeout(function() {{
                initTheme();
            }}, 100);
        }});
    </script>
</body>
</html>"""
    
    return html_content


def check_rate_limit():
    """检查 GitHub API 速率限制并处理"""
    try:
        rate_limit = user.get_rate_limit()
        remaining = rate_limit.core.remaining
        if remaining < 100:
            reset_time = rate_limit.core.reset
            wait_seconds = (reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"API 配额不足 (剩余: {remaining})，等待 {wait_seconds:.0f} 秒...")
                time.sleep(wait_seconds)
                print("API 配额已重置，继续执行...")
    except Exception as e:
        print(f"检查 API 速率限制时出错: {str(e)}")


def execute():
    global cur_time
    # common
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 0. 加载环境变量文件
    load_env_file()

    # 1. login & init rope
    login()
    
    # 1.1 检查 API 速率限制
    check_rate_limit()

    # 1.2 一次性获取所有数据（缓存）
    print("正在获取所有 labels 和 issues...")
    all_labels = list(blog_repo.get_labels())
    all_issues = list(blog_repo.get_issues(state="all"))
    print(f"获取到 {len(all_labels)} 个 labels 和 {len(all_issues)} 个 issues")
    
    # 1.3 创建全局 Markdown 实例
    global_md = markdown.Markdown(
        extensions=[
            'extra',
            'codehilite',
            'toc',
            'fenced_code',
            'tables',
            'nl2br'
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight'
            }
        }
    )

    # 2. summary section
    summary_section = bundle_summary_section()
    print(summary_section)

    # 3. generate word cloud once (now generates both light and dark versions)
    wordcloud_light_url = WordCloudGenerator(blog_repo).generate()
    print(f"Word cloud generated: {wordcloud_light_url}")

    # 4. list by labels section
    list_by_labels_section = bundle_list_by_labels_section(wordcloud_light_url, all_labels, all_issues)
    print(list_by_labels_section)

    # 5. generate README.md
    contents = [summary_section, list_by_labels_section]
    update_readme_md_file(contents)
    print("README.md updated successfully!!!")

    # 6. generate index.html
    html_content = bundle_html_content(all_labels, all_issues)
    update_index_html_file(html_content)
    print("index.html generated successfully!!!")

    # 7. generate article HTML files
    print("开始生成文章 HTML 文件...")
    generated_count = 0
    for issue in all_issues:
        try:
            # 生成文章 HTML
            article_html = generate_article_html(issue, global_md)
            # 保存文章 HTML
            filepath = save_article_html(issue, article_html)
            generated_count += 1
            print(f"生成文章: {issue.title} -> {filepath}")
        except Exception as e:
            print(f"生成文章失败 {issue.title}: {str(e)}")
    
    print(f"文章 HTML 生成完成! 共生成 {generated_count} 篇文章")


if __name__ == "__main__":
    execute()
