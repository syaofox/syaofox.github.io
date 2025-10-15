# -*- coding: utf-8 -*-
"""
文章数据模型
封装文章相关的数据结构和处理逻辑
"""

import re
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

from github.Issue import Issue


@dataclass
class Article:
    """文章数据类"""
    number: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    labels: List[str]
    github_url: str
    comments: List = None
    
    @classmethod
    def from_github_issue(cls, issue: Issue, include_comments: bool = False) -> 'Article':
        """从 GitHub Issue 创建文章实例"""
        labels = [label.name for label in issue.labels] if issue.labels else []
        
        # 获取评论（如果需要）
        comments = None
        if include_comments:
            try:
                comments = list(issue.get_comments())
            except Exception:
                comments = []
        
        return cls(
            number=issue.number,
            title=issue.title,
            content=issue.body or '',
            created_at=issue.created_at,
            updated_at=issue.updated_at,
            labels=labels,
            github_url=issue.html_url,
            comments=comments
        )
    
    @property
    def primary_label(self) -> str:
        """获取主要标签（第一个标签或 'uncategorized'）"""
        return self.labels[0] if self.labels else 'uncategorized'
    
    @property
    def created_date_str(self) -> str:
        """获取创建日期字符串"""
        return self.created_at.strftime("%Y-%m-%d")
    
    @property
    def created_datetime_str(self) -> str:
        """获取创建日期时间字符串"""
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def updated_datetime_str(self) -> str:
        """获取更新日期时间字符串"""
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def title_slug(self) -> str:
        """将标题转换为URL安全的slug"""
        return title_to_slug(self.title)
    
    @property
    def filename(self) -> str:
        """生成文件名"""
        return f"{self.created_date_str}-{self.title_slug}.html"
    
    @property
    def url_path(self) -> str:
        """生成相对URL路径"""
        return f"articles/{self.primary_label}/{self.filename}"
    
    @property
    def image_dir_name(self) -> str:
        """获取清理后的文章标题用作图片目录名"""
        return title_to_slug(self.title)
    
    @property
    def local_images_dir(self) -> Path:
        """获取图片保存的完整路径"""
        return Path("assets/images") / self.image_dir_name
    
    def to_dict(self) -> dict:
        """转换为字典格式（用于模板渲染）"""
        return {
            'number': self.number,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_datetime_str,
            'updated_at': self.updated_datetime_str,
            'labels': self.labels,
            'github_url': self.github_url,
            'url': self.url_path
        }
    
    def to_markdown(self) -> str:
        """转换为 Markdown 格式（用于备份）"""
        from .backup import ArticleBackup
        
        # 使用备份模块的格式化方法
        backup = ArticleBackup(Path("."))  # 临时实例，只用于格式化
        return backup._format_article_to_markdown(self, self.comments)


def title_to_slug(title: str) -> str:
    """
    将标题转换为URL安全的slug
    
    Args:
        title: 文章标题
        
    Returns:
        URL安全的slug字符串
    """
    if not title:
        return "untitled"
    
    # 移除特殊字符，保留中文、英文、数字和连字符
    slug = re.sub(r'[^\w\u4e00-\u9fff\-]', '', title)
    
    # 将多个连字符替换为单个
    slug = re.sub(r'-+', '-', slug)
    
    # 移除首尾的连字符
    slug = slug.strip('-')
    
    # 如果为空或过长，使用默认值
    if not slug:
        slug = "untitled"
    elif len(slug) > 100:  # 限制长度避免文件名过长
        slug = slug[:100].rstrip('-')
    
    return slug


@dataclass
class Category:
    """分类数据类"""
    name: str
    articles: List[Article]
    
    @property
    def count(self) -> int:
        """获取文章数量"""
        return len(self.articles)
    
    def to_dict(self) -> dict:
        """转换为字典格式（用于模板渲染）"""
        return {
            'name': self.name,
            'count': self.count,
            'articles': [article.to_dict() for article in self.articles]
        }


def group_articles_by_category(articles: List[Article]) -> List[Category]:
    """
    将文章按分类分组
    
    Args:
        articles: 文章列表
        
    Returns:
        分类列表，按文章数量降序排列
    """
    category_map = {}
    
    for article in articles:
        category_name = article.primary_label
        if category_name not in category_map:
            category_map[category_name] = []
        category_map[category_name].append(article)
    
    # 转换为 Category 对象并按文章数量排序
    categories = [
        Category(name=name, articles=articles_list)
        for name, articles_list in category_map.items()
    ]
    
    # 按文章数量降序排序
    categories.sort(key=lambda x: x.count, reverse=True)
    
    return categories
