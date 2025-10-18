# -*- coding: utf-8 -*-
"""
HTML 生成器模块
使用 Jinja2 模板引擎生成 HTML 内容
"""

import re
import logging
from pathlib import Path
from typing import List, Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..core.config import config
from ..core.github_client import github_client
from ..models.article import Article, Category, group_articles_by_category

logger = logging.getLogger(__name__)


class HTMLGenerator:
    """HTML 生成器"""
    
    def __init__(self):
        """初始化 HTML 生成器"""
        self._setup_jinja_env()
        logger.debug("HTML 生成器初始化完成")
    
    def _setup_jinja_env(self) -> None:
        """设置 Jinja2 环境"""
        template_dir = config.templates_dir
        
        self._jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # 添加自定义过滤器
        self._jinja_env.filters['datetime'] = self._datetime_filter
        self._jinja_env.filters['date'] = self._date_filter
        
        logger.debug(f"Jinja2 环境初始化完成，模板目录: {template_dir}")
    
    def _datetime_filter(self, dt, format='%Y-%m-%d %H:%M:%S') -> str:
        """日期时间过滤器"""
        if hasattr(dt, 'strftime'):
            return dt.strftime(format)
        return str(dt)
    
    def _date_filter(self, dt, format='%Y-%m-%d') -> str:
        """日期过滤器"""
        if hasattr(dt, 'strftime'):
            return dt.strftime(format)
        return str(dt)
    
    def generate_article_html(self, article: Article) -> str:
        """
        生成文章 HTML
        
        Args:
            article: 文章对象
            
        Returns:
            生成的 HTML 内容
        """
        try:
            # 处理文章内容中的图片和附件（在 Markdown 中替换 URL）
            logger.debug(f"开始处理文章附件: {article.title}")
            processed_markdown = self._process_markdown_images(article)
            
            # 准备模板数据
            template_data = {
                'article': article.to_dict(),
                'user_name': github_client.user_name,
                'blog_name': github_client.blog_name,
                'css_base_path': '../../'  # html/articles/分类/ -> html/
            }
            
            # 更新文章内容为处理后的 Markdown
            template_data['article']['content'] = processed_markdown
            
            # 渲染模板
            template = self._jinja_env.get_template('article.html')
            html = template.render(**template_data)
            
            logger.debug(f"文章 HTML 生成成功: {article.title}")
            return html
            
        except Exception as e:
            logger.error(f"生成文章 HTML 失败 {article.title}: {str(e)}")
            raise
    
    def _process_markdown_images(self, article: Article) -> str:
        """
        从 Markdown 内容中处理图片和附件
        
        Args:
            article: 文章对象
            
        Returns:
            处理后的 Markdown 内容（图片和附件 URL 已替换为本地路径）
        """
        try:
            from ..utils.image_utils import ImageProcessor
            
            processor = ImageProcessor()
            
            # 使用 ImageProcessor 下载图片并获取 URL 映射
            url_map = processor.download_article_images(article)
            
            if not url_map:
                logger.debug(f"文章 {article.title} 没有需要处理的附件")
                return article.content
            
            # 替换 Markdown 和 HTML 中的附件 URL
            processed_content = article.content
            for original_url, local_path in url_map.items():
                # 替换所有出现的 URL（无论是 Markdown 还是 HTML 格式）
                processed_content = processed_content.replace(original_url, local_path)
            
            return processed_content
            
        except Exception as e:
            logger.error(f"处理 Markdown 附件失败 {article.title}: {str(e)}")
            return article.content  # 返回原始内容
    
    def generate_index_html(self, articles: List[Article], cur_time: str) -> str:
        """
        生成首页 HTML
        
        Args:
            articles: 文章列表
            cur_time: 当前时间
            
        Returns:
            生成的 HTML 内容
        """
        try:
            # 按分类分组文章
            categories = group_articles_by_category(articles)
            
            # 准备模板数据
            template_data = {
                'user_name': github_client.user_name,
                'blog_name': github_client.blog_name,
                'cur_time': cur_time,
                'categories': [category.to_dict() for category in categories],
                'css_base_path': ''  # html/ -> html/
            }
            
            # 渲染模板
            template = self._jinja_env.get_template('index.html')
            html = template.render(**template_data)
            
            logger.info(f"首页 HTML 生成成功，共 {len(categories)} 个分类")
            return html
            
        except Exception as e:
            logger.error(f"生成首页 HTML 失败: {str(e)}")
            raise
    
    def close(self) -> None:
        """清理资源"""
        logger.debug("HTML 生成器已清理")


def generate_article_html(article: Article) -> str:
    """
    便捷函数：生成文章 HTML
    
    Args:
        article: 文章对象
        
    Returns:
        HTML 内容
    """
    generator = HTMLGenerator()
    try:
        return generator.generate_article_html(article)
    finally:
        generator.close()


def generate_index_html(articles: List[Article], cur_time: str) -> str:
    """
    便捷函数：生成首页 HTML
    
    Args:
        articles: 文章列表
        cur_time: 当前时间
        
    Returns:
        HTML 内容
    """
    generator = HTMLGenerator()
    try:
        return generator.generate_index_html(articles, cur_time)
    finally:
        generator.close()
