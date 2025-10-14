# -*- coding: utf-8 -*-
"""
图片处理工具模块
处理 GitHub 附件图片的下载和 URL 转换
"""

import re
import requests
import logging
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

from ..core.config import config
from ..models.article import Article

logger = logging.getLogger(__name__)


class ImageProcessor:
    """图片处理器"""
    
    def __init__(self):
        """初始化图片处理器"""
        # GitHub 附件 URL 正则模式
        self._github_attachment_pattern = re.compile(
            r'!\[([^\]]*)\]\((https://github\.com/user-attachments/assets/[a-f0-9\-]+)\)'
        )
        logger.debug("图片处理器初始化完成")
    
    def extract_github_image_urls(self, content: str) -> List[str]:
        """
        从 Markdown 内容中提取 GitHub 附件图片 URL
        
        Args:
            content: Markdown 内容
            
        Returns:
            GitHub 附件图片 URL 列表
        """
        try:
            matches = self._github_attachment_pattern.findall(content)
            urls = [match[1] for match in matches]  # match[1] 是 URL 部分
            
            logger.debug(f"提取到 {len(urls)} 个 GitHub 附件图片 URL")
            return urls
            
        except Exception as e:
            logger.error(f"提取图片 URL 失败: {str(e)}")
            return []
    
    def download_image(self, url: str, save_path: Path) -> bool:
        """
        下载图片到指定路径
        
        Args:
            url: 图片 URL
            save_path: 保存路径
            
        Returns:
            是否下载成功
        """
        try:
            # 检查文件是否已存在（缓存机制）
            if save_path.exists():
                logger.debug(f"图片已存在，跳过下载: {save_path}")
                return True
            
            # 确保目录存在
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 下载图片
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 保存文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.debug(f"图片下载成功: {url} -> {save_path}")
            return True
            
        except Exception as e:
            logger.warning(f"图片下载失败 {url}: {str(e)}")
            return False
    
    def download_article_images(self, article: Article) -> Dict[str, str]:
        """
        下载文章的所有图片
        
        Args:
            article: 文章对象
            
        Returns:
            URL 映射表 {原始URL: 本地相对路径}
        """
        try:
            # 提取图片 URL
            image_urls = self.extract_github_image_urls(article.content)
            
            if not image_urls:
                logger.debug(f"文章 {article.title} 没有 GitHub 附件图片")
                return {}
            
            # 确保图片目录存在
            image_dir = article.local_images_dir
            image_dir.mkdir(parents=True, exist_ok=True)
            
            url_map = {}
            success_count = 0
            
            for i, url in enumerate(image_urls, 1):
                try:
                    # 获取文件扩展名
                    parsed_url = urlparse(url)
                    # GitHub 附件通常没有扩展名，我们根据内容类型判断
                    # 这里先尝试从 URL 获取，如果没有则使用默认扩展名
                    extension = self._get_image_extension(url)
                    
                    # 生成文件名
                    filename = f"image-{i}{extension}"
                    save_path = image_dir / filename
                    
                    # 下载图片
                    if self.download_image(url, save_path):
                        # 生成相对路径（从 html/articles/{分类}/ 到图片）
                        relative_path = f"../../../assets/images/{article.image_dir_name}/{filename}"
                        url_map[url] = relative_path
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
            logger.error(f"下载文章图片失败 {article.title}: {str(e)}")
            return {}
    
    def _get_image_extension(self, url: str) -> str:
        """
        获取图片文件扩展名
        
        Args:
            url: 图片 URL
            
        Returns:
            文件扩展名（包含点号）
        """
        try:
            # 尝试从 URL 获取扩展名
            parsed_url = urlparse(url)
            path = parsed_url.path.lower()
            
            # 检查常见图片扩展名
            for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
                if path.endswith(ext):
                    return ext
            
            # 如果没有找到扩展名，尝试通过 HEAD 请求获取 Content-Type
            try:
                response = requests.head(url, timeout=10)
                content_type = response.headers.get('content-type', '').lower()
                
                if 'png' in content_type:
                    return '.png'
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    return '.jpg'
                elif 'gif' in content_type:
                    return '.gif'
                elif 'webp' in content_type:
                    return '.webp'
                elif 'svg' in content_type:
                    return '.svg'
            except:
                pass
            
            # 默认使用 .png
            return '.png'
            
        except Exception as e:
            logger.warning(f"获取图片扩展名失败 {url}: {str(e)}")
            return '.png'


def extract_github_image_urls(content: str) -> List[str]:
    """
    便捷函数：提取 GitHub 附件图片 URL
    
    Args:
        content: Markdown 内容
        
    Returns:
        GitHub 附件图片 URL 列表
    """
    processor = ImageProcessor()
    return processor.extract_github_image_urls(content)


def download_article_images(article: Article) -> Dict[str, str]:
    """
    便捷函数：下载文章图片
    
    Args:
        article: 文章对象
        
    Returns:
        URL 映射表
    """
    processor = ImageProcessor()
    return processor.download_article_images(article)
