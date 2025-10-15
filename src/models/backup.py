# -*- coding: utf-8 -*-
"""
文章备份模块
封装文章备份相关的功能，将 GitHub Issues 备份为 Markdown 文件
"""

import re
import codecs
import logging
from pathlib import Path
from typing import List, Optional

from .article import Article

logger = logging.getLogger(__name__)


class ArticleBackup:
    """文章备份类"""
    
    def __init__(self, backup_dir: Path):
        """
        初始化备份器
        
        Args:
            backup_dir: 备份目录路径
        """
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"备份目录: {self.backup_dir}")
    
    @staticmethod
    def sanitize_filename(title: str) -> str:
        """
        清理文件名，移除或替换特殊字符
        
        Args:
            title: 文章标题
            
        Returns:
            清理后的文件名
        """
        # 移除或替换文件名中不允许的字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', title)
        # 移除多余的空格和点
        filename = re.sub(r'\s+', ' ', filename).strip()
        filename = filename.strip('.')
        # 限制文件名长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    def backup_article(self, article: Article, comments: Optional[List] = None) -> bool:
        """
        备份单个文章到 Markdown 文件
        
        Args:
            article: 文章对象
            comments: 评论列表（可选）
            
        Returns:
            备份是否成功
        """
        try:
            # 创建文件名
            date_str = article.created_date_str
            title_clean = self.sanitize_filename(article.title)
            filename = f"{date_str}-{title_clean}.md"
            filepath = self.backup_dir / filename
            
            # 生成 Markdown 内容
            markdown_content = self._format_article_to_markdown(article, comments)
            
            # 保存文件（强制覆盖）
            with codecs.open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)
                f.flush()
            
            logger.info(f"备份文章: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"备份文章失败 {article.title}: {str(e)}")
            return False
    
    def backup_all_articles(self, articles: List[Article], issue_comments_map: Optional[dict] = None) -> int:
        """
        批量备份所有文章
        
        Args:
            articles: 文章列表
            issue_comments_map: Issue 编号到评论列表的映射（可选）
            
        Returns:
            成功备份的文章数量
        """
        logger.info("开始备份文章...")
        
        saved_count = 0
        total_count = len(articles)
        
        for article in articles:
            # 获取该文章的评论（如果有）
            comments = None
            if issue_comments_map and article.number in issue_comments_map:
                comments = issue_comments_map[article.number]
            
            if self.backup_article(article, comments):
                saved_count += 1
        
        logger.info(f"备份完成! 总共处理: {total_count} 个文章，成功备份: {saved_count} 个文件")
        if saved_count < total_count:
            logger.warning(f"备份失败: {total_count - saved_count} 个文件")
        
        return saved_count
    
    def _format_article_to_markdown(self, article: Article, comments: Optional[List] = None) -> str:
        """
        将文章转换为 Markdown 格式
        
        Args:
            article: 文章对象
            comments: 评论列表（可选）
            
        Returns:
            Markdown 格式的字符串
        """
        # 构建 Front Matter
        front_matter = f"""---
title: "{article.title}"
created_at: "{article.created_datetime_str}"
updated_at: "{article.updated_datetime_str}"
issue_number: {article.number}
labels: {article.labels}
url: {article.github_url}
---

"""
        
        # 构建正文内容
        content = front_matter
        content += f"# {article.title}\n\n"
        
        if article.content:
            content += f"{article.content}\n\n"
        else:
            content += "*此文章没有正文内容*\n\n"
        
        # 添加评论部分
        if comments:
            content += "---\n\n"
            content += "## 评论\n\n"
            
            for comment in comments:
                # 处理评论用户和日期
                user_login = getattr(comment.user, 'login', 'Unknown')
                created_at = getattr(comment, 'created_at', '')
                if hasattr(created_at, 'strftime'):
                    created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                
                content += f"### {user_login} - {created_at}\n\n"
                content += f"{comment.body}\n\n"
                content += "---\n\n"
        
        return content
