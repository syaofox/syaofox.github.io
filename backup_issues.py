#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import os
import re
import time
from datetime import datetime

from github import Github
from github.Issue import Issue
from github.Repository import Repository
from dotenv import load_dotenv


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


def login():
    """登录 GitHub 并获取仓库对象"""
    global user, user_name, blog_name, blog_repo
    
    github_repo_env = os.environ.get("GITHUB_REPOSITORY")
    user_name = github_repo_env[0 : github_repo_env.index("/")]
    blog_name = github_repo_env[github_repo_env.index("/") :]
    password = os.environ.get("GITHUB_TOKEN")
    user = Github(user_name, password)
    blog_repo = user.get_repo(github_repo_env)
    print(f"已连接到仓库: {blog_repo}")


def sanitize_filename(title):
    """清理文件名，移除或替换特殊字符"""
    # 移除或替换文件名中不允许的字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', title)
    # 移除多余的空格和点
    filename = re.sub(r'\s+', ' ', filename).strip()
    filename = filename.strip('.')
    # 限制文件名长度
    if len(filename) > 100:
        filename = filename[:100]
    return filename


def format_issue_to_markdown(issue: Issue):
    """将 Issue 转换为 Markdown 格式"""
    # 获取标签名称
    labels = [label.name for label in issue.labels]
    
    # 获取评论
    comments = list(issue.get_comments())
    
    # 构建 Front Matter
    front_matter = f"""---
title: "{issue.title}"
created_at: "{issue.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
updated_at: "{issue.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
issue_number: {issue.number}
state: {issue.state}
labels: {labels}
url: {issue.html_url}
---

"""
    
    # 构建正文内容
    content = front_matter
    content += f"# {issue.title}\n\n"
    
    if issue.body:
        content += f"{issue.body}\n\n"
    else:
        content += "*此 Issue 没有正文内容*\n\n"
    
    # 添加评论部分
    if comments:
        content += "---\n\n"
        content += "## 评论\n\n"
        
        for comment in comments:
            content += f"### {comment.user.login} - {comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            content += f"{comment.body}\n\n"
            content += "---\n\n"
    
    return content


def save_issue_to_file(issue: Issue, articles_dir: str):
    """保存 Issue 到 Markdown 文件（强制覆盖）"""
    # 创建文件名
    date_str = issue.created_at.strftime('%Y-%m-%d')
    title_clean = sanitize_filename(issue.title)
    filename = f"{date_str}-{title_clean}.md"
    filepath = os.path.join(articles_dir, filename)
    
    # 生成 Markdown 内容
    markdown_content = format_issue_to_markdown(issue)
    
    # 保存文件（强制覆盖）
    try:
        with codecs.open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            f.flush()
        print(f"  保存: {filename}")
        return True
    except Exception as e:
        print(f"  错误: 无法保存 {filename} - {str(e)}")
        return False


def backup_all_issues():
    """备份所有 Issues 到 articles/ 目录"""
    global blog_repo
    
    # 确保 articles 目录存在
    articles_dir = "articles_backup"
    if not os.path.exists(articles_dir):
        os.makedirs(articles_dir)
        print(f"创建目录: {articles_dir}")
    
    print("开始备份 Issues...")
    
    # 获取所有状态的 issues，过滤掉 PR
    all_issues = [issue for issue in blog_repo.get_issues(state="all", sort="created", direction="desc")
                  if not issue.pull_request]
    
    total_count = 0
    saved_count = 0
    
    for issue in all_issues:
        total_count += 1
        print(f"处理 Issue #{issue.number}: {issue.title}")
        
        if save_issue_to_file(issue, articles_dir):
            saved_count += 1
    
    print(f"\n备份完成!")
    print(f"总共处理: {total_count} 个 Issues")
    print(f"成功保存: {saved_count} 个文件")
    if saved_count < total_count:
        print(f"失败: {total_count - saved_count} 个文件")


def main():
    """主函数"""
    print("GitHub Issues 备份工具")
    print("=" * 50)
    
    # 加载环境变量
    load_env_file()
    
    # 登录 GitHub
    login()
    
    # 备份所有 issues
    backup_all_issues()


if __name__ == "__main__":
    main()
