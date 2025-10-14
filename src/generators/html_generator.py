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
from ..utils.text_utils import MarkdownProcessor
from ..utils.image_utils import download_article_images

logger = logging.getLogger(__name__)


class HTMLGenerator:
    """HTML 生成器"""
    
    def __init__(self):
        """初始化 HTML 生成器"""
        self._setup_jinja_env()
        self._markdown_processor = MarkdownProcessor()
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
            # 先转换 Markdown 内容为 HTML
            html_content = self._markdown_processor.convert_to_html(
                article.content,
                article_category=article.primary_label
            )
            
            # 从转换后的 HTML 中提取图片 URL 并下载
            logger.debug(f"开始处理文章图片: {article.title}")
            url_map = self._process_html_images(article, html_content)
            
            # 替换 HTML 中的图片链接
            if url_map:
                html_content = self._replace_html_image_urls(html_content, url_map, article.image_dir_name)
            
            # 提取目录结构
            toc_items = self._markdown_processor.extract_toc(article.content)
            
            # 准备模板数据
            template_data = {
                'article': article.to_dict(),
                'toc_items': toc_items,
                'user_name': github_client.user_name,
                'blog_name': github_client.blog_name,
                'css_base_path': '../../'  # html/articles/分类/ -> html/
            }
            
            # 更新文章内容为转换后的 HTML
            template_data['article']['content'] = html_content
            
            # 渲染模板
            template = self._jinja_env.get_template('article.html')
            html = template.render(**template_data)
            
            logger.debug(f"文章 HTML 生成成功: {article.title}, 目录项: {len(toc_items)}, 图片: {len(url_map)}")
            return html
            
        except Exception as e:
            logger.error(f"生成文章 HTML 失败 {article.title}: {str(e)}")
            raise
    
    def _process_html_images(self, article: Article, html_content: str) -> Dict[str, str]:
        """
        从 HTML 内容中处理图片
        
        Args:
            article: 文章对象
            html_content: HTML 内容
            
        Returns:
            URL 映射表
        """
        try:
            from ..utils.image_utils import ImageProcessor
            
            processor = ImageProcessor()
            image_urls = processor.extract_github_image_urls(html_content)
            
            if not image_urls:
                logger.debug(f"文章 {article.title} 没有 GitHub 附件图片")
                return {}
            
            # 确保图片目录存在
            image_dir = article.local_images_dir
            logger.info(f"图片保存目录: {image_dir.absolute()}")
            image_dir.mkdir(parents=True, exist_ok=True)
            
            url_map = {}
            success_count = 0
            
            for i, url in enumerate(image_urls, 1):
                try:
                    # 获取文件扩展名
                    extension = processor._get_image_extension(url)
                    
                    # 生成文件名
                    filename = f"image-{i}{extension}"
                    save_path = image_dir / filename
                    
                    # 下载图片
                    if processor.download_image(url, save_path):
                        # 生成相对路径（从 html/articles/{分类}/ 到图片）
                        relative_path = f"../../../assets/images/{article.image_dir_name}/{filename}"
                        url_map[url] = relative_path
                        logger.info(f"图片下载成功: {url} -> {save_path.absolute()}")
                        success_count += 1
                    else:
                        # 下载失败，保留原始 URL
                        url_map[url] = url
                        
                except Exception as e:
                    logger.warning(f"处理图片失败 {url}: {str(e)}")
                    url_map[url] = url  # 保留原始 URL
            
            logger.info(f"文章 {article.title} 图片处理完成: {success_count}/{len(image_urls)} 成功")
            return url_map
            
        except Exception as e:
            logger.error(f"处理 HTML 图片失败 {article.title}: {str(e)}")
            return {}
    
    def _replace_html_image_urls(self, html_content: str, url_map: Dict[str, str], image_dir_name: str) -> str:
        """
        替换 HTML 中的图片 URL
        
        Args:
            html_content: HTML 内容
            url_map: URL 映射表
            image_dir_name: 图片目录名
            
        Returns:
            替换后的 HTML 内容
        """
        try:
            converted_content = html_content
            
            for original_url, local_path in url_map.items():
                if original_url != local_path:  # 只替换成功下载的图片
                    # 替换 HTML img 标签中的 src 属性
                    pattern = f'<img([^>]*)src="{re.escape(original_url)}"([^>]*)>'
                    replacement = f'<img\\1src="{local_path}"\\2>'
                    converted_content = re.sub(pattern, replacement, converted_content)
            
            # 统计转换数量
            converted_count = len([url for url in url_map.keys() if url != url_map[url]])
            if converted_count > 0:
                logger.info(f"HTML 图片 URL 转换完成，转换了 {converted_count} 个链接")
            
            return converted_content
            
        except Exception as e:
            logger.error(f"替换 HTML 图片 URL 失败: {str(e)}")
            return html_content
    
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
        if self._markdown_processor:
            self._markdown_processor.close()
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
