#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import os
import time
import re
import urllib.parse
from datetime import datetime

from github import Github
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


def generate_article_html(issue: Issue):
    """生成单个文章的HTML内容"""
    # 配置 Markdown 扩展
    md = markdown.Markdown(
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
    
    # 转换 Markdown 内容为 HTML
    content_html = md.convert(issue.body or '')
    
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
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #fdfdfd;
            color: #111;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #ffffff;
            border: 1px solid #e8e8e8;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        
        .header {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e8e8e8;
        }}
        
        .back-link {{
            display: inline-block;
            color: #2a7ae2;
            text-decoration: none;
            margin-bottom: 15px;
            font-size: 0.9em;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        .article-title {{
            font-size: 2em;
            font-weight: 700;
            color: #111;
            margin-bottom: 15px;
        }}
        
        .article-meta {{
            color: #828282;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        
        .labels {{
            margin-top: 10px;
        }}
        
        .label {{
            display: inline-block;
            background: #f7f7f7;
            color: #111;
            padding: 4px 8px;
            border: 1px solid #e8e8e8;
            font-size: 0.8em;
            margin-right: 5px;
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
            color: #111;
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
            border: 1px solid #e8e8e8;
            margin: 15px 0;
        }}
        
        .article-content pre {{
            background: #f7f7f7;
            border: 1px solid #e8e8e8;
            padding: 15px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        .article-content code {{
            background: #f7f7f7;
            padding: 2px 6px;
            border: 1px solid #e8e8e8;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        .article-content pre code {{
            background: none;
            border: none;
            padding: 0;
        }}
        
        .article-content blockquote {{
            border-left: 4px solid #e8e8e8;
            margin: 15px 0;
            padding: 10px 20px;
            background: #f7f7f7;
        }}
        
        .article-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        .article-content th,
        .article-content td {{
            border: 1px solid #e8e8e8;
            padding: 10px;
            text-align: left;
        }}
        
        .article-content th {{
            background: #f7f7f7;
            font-weight: 600;
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
            border-top: 1px solid #e8e8e8;
            text-align: center;
            color: #828282;
            font-size: 0.9em;
        }}
        
        .github-link {{
            color: #2a7ae2;
            text-decoration: none;
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
        
        @media (min-width: 1024px) {{
            .article-content {{
                max-width: 700px;
                margin: 0 auto;
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
    user = Github(user_name, password)
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


def bundle_list_by_labels_section(wordcloud_image_url):
    global blog_repo
    global user
    global user_name
    global blog_name

    list_by_labels_section = """
<summary>
    <a href="https://%s.github.io/%s/"><img src="%s" title="词云" alt="词云"></a>
</summary>  
""" % (user_name, blog_name, wordcloud_image_url)

    all_labels = blog_repo.get_labels()
    for label in all_labels:
        temp = ""
        count = 0
        # 获取所有状态的 issues（包括 open 和 closed）
        issues_in_label = blog_repo.get_issues(labels=(label,), state="all")
        for issue in issues_in_label:
            temp += format_issue(issue)
            count += 1
        if count > 0:
            list_by_labels_section += """
<details open>
<summary>%s\t[%s篇]</summary>

%s

</details>
            """ % (label.name, count, temp)

    return list_by_labels_section


def bundle_html_content(wordcloud_image_url):
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
    
    # 构建词云HTML
    wordcloud_html = f"""
    <div class="wordcloud-section">
        <a href="https://{user_name}.github.io/{blog_name}/">
            <img src="{wordcloud_image_url}" title="词云" alt="词云" class="wordcloud-img">
        </a>
    </div>"""
    
    # 构建标签分类HTML
    issues_html = ""
    all_labels = blog_repo.get_labels()
    
    # 收集所有标签和对应的文章数量，按文章数量排序
    label_counts = []
    for label in all_labels:
        count = 0
        issues_in_label = blog_repo.get_issues(labels=(label,), state="all")
        for issue in issues_in_label:
            count += 1
        label_counts.append((label, count))
    
    # 按文章数量降序排序
    label_counts.sort(key=lambda x: x[1], reverse=True)
    
    for label, count in label_counts:
        temp = ""
        issues_in_label = blog_repo.get_issues(labels=(label,), state="all")
        for issue in issues_in_label:
            temp += f"""
            <div class="issue-item">
                <span class="issue-date">{issue.created_at.strftime("%Y-%m-%d")}</span>
                <a href="{get_article_url(issue)}" class="issue-link">{issue.title}</a>
            </div>"""
        
        if count > 0:
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
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #fdfdfd;
            color: #111;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
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
        
        .wordcloud-section {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .wordcloud-img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            border: 1px solid #e8e8e8;
        }}
        
        .categories-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: 1fr;
        }}
        
        .category-card {{
            background: #ffffff;
            border: 1px solid #e8e8e8;
            overflow: hidden;
        }}
        
        .category-header {{
            background: #f7f7f7;
            padding: 15px 20px;
            border-bottom: 1px solid #e8e8e8;
        }}
        
        .category-title {{
            font-size: 1.1em;
            font-weight: 700;
            color: #111;
            margin-bottom: 5px;
        }}
        
        .category-count {{
            color: #828282;
            font-size: 0.9em;
        }}
        
        .issues-list {{
            padding: 20px;
        }}
        
        .issue-item {{
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #f7f7f7;
        }}
        
        .issue-item:last-child {{
            border-bottom: none;
        }}
        
        .issue-date {{
            color: #828282;
            font-size: 0.9em;
            min-width: 80px;
            margin-right: 15px;
        }}
        
        .issue-link {{
            color: #2a7ae2;
            text-decoration: none;
            flex: 1;
        }}
        
        .issue-link:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #828282;
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
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            {badges_html}
        </header>
        
        <main>
            {wordcloud_html}
            
            <section class="categories-grid">
                {issues_html}
            </section>
        </main>
        
        <footer class="footer">
            <p>最后更新：{cur_time}</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html_content


def execute():
    global cur_time
    # common
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 0. 加载环境变量文件
    load_env_file()

    # 1. login & init rope
    login()

    # 2. summary section
    summary_section = bundle_summary_section()
    print(summary_section)

    # 3. generate word cloud once
    wordcloud_image_url = WordCloudGenerator(blog_repo).generate()
    print(f"Word cloud generated: {wordcloud_image_url}")

    # 4. list by labels section
    list_by_labels_section = bundle_list_by_labels_section(wordcloud_image_url)
    print(list_by_labels_section)

    # 5. generate README.md
    contents = [summary_section, list_by_labels_section]
    update_readme_md_file(contents)
    print("README.md updated successfully!!!")

    # 6. generate index.html
    html_content = bundle_html_content(wordcloud_image_url)
    update_index_html_file(html_content)
    print("index.html generated successfully!!!")

    # 7. generate article HTML files
    print("开始生成文章 HTML 文件...")
    all_issues = blog_repo.get_issues(state="all")
    generated_count = 0
    for issue in all_issues:
        try:
            # 生成文章 HTML
            article_html = generate_article_html(issue)
            # 保存文章 HTML
            filepath = save_article_html(issue, article_html)
            generated_count += 1
            print(f"生成文章: {issue.title} -> {filepath}")
        except Exception as e:
            print(f"生成文章失败 {issue.title}: {str(e)}")
    
    print(f"文章 HTML 生成完成! 共生成 {generated_count} 篇文章")


if __name__ == "__main__":
    execute()
