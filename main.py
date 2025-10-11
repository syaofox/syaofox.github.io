#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import os
import time

from github import Github
from github.Issue import Issue
from github.Repository import Repository

from word_cloud import WordCloudGenerator

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


def bundle_list_by_labels_section():
    global blog_repo
    global user
    global user_name
    global blog_name

    # word cloud
    wordcloud_image_url = WordCloudGenerator(blog_repo).generate()

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


def bundle_html_content():
    global blog_repo, user_name, blog_name, cur_time
    
    # 获取词云图
    wordcloud_image_url = WordCloudGenerator(blog_repo).generate()
    
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
                <a href="{issue.html_url}" class="issue-link">{issue.title}</a>
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
            background-color: #f8f9fa;
            color: #333333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
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
            transition: transform 0.2s ease;
        }}
        
        .badges img:hover {{
            transform: translateY(-2px);
        }}
        
        .wordcloud-section {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .wordcloud-img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .wordcloud-img:hover {{
            transform: scale(1.02);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }}
        
        .categories-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }}
        
        .category-card {{
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .category-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
        }}
        
        .category-header {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 15px 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .category-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #1976d2;
            margin-bottom: 5px;
        }}
        
        .category-count {{
            color: #666666;
            font-size: 0.9em;
        }}
        
        .issues-list {{
            padding: 20px;
        }}
        
        .issue-item {{
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .issue-item:last-child {{
            border-bottom: none;
        }}
        
        .issue-date {{
            color: #666666;
            font-size: 0.9em;
            min-width: 80px;
            margin-right: 15px;
        }}
        
        .issue-link {{
            color: #2196F3;
            text-decoration: none;
            flex: 1;
            transition: color 0.2s ease;
        }}
        
        .issue-link:hover {{
            color: #1976d2;
            text-decoration: underline;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666666;
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
                grid-template-columns: 1fr;
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
                grid-template-columns: repeat(3, 1fr);
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

    # 1. login & init rope
    login()

    # 2. summary section
    summary_section = bundle_summary_section()
    print(summary_section)

    # 3. list by labels section
    list_by_labels_section = bundle_list_by_labels_section()
    print(list_by_labels_section)

    # 4. generate README.md
    contents = [summary_section, list_by_labels_section]
    update_readme_md_file(contents)
    print("README.md updated successfully!!!")

    # 5. generate index.html
    html_content = bundle_html_content()
    update_index_html_file(html_content)
    print("index.html generated successfully!!!")


if __name__ == "__main__":
    execute()
