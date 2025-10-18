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
        # GitHub 附件 URL 正则模式 - Markdown 格式
        self._github_attachment_markdown_pattern = re.compile(
            r'!\[([^\]]*)\]\((https://github\.com/user-attachments/assets/[a-f0-9\-]+)\)'
        )
        # GitHub 附件 URL 正则模式 - HTML 格式
        self._github_attachment_html_pattern = re.compile(
            r'<img[^>]*src="(https://github\.com/user-attachments/assets/[a-f0-9\-]+)"[^>]*>'
        )
        # GitHub files 附件 URL 正则模式 - Markdown 格式
        self._github_files_markdown_pattern = re.compile(
            r'\[([^\]]+)\]\((https://github\.com/user-attachments/files/\d+/[^)]+)\)'
        )
        # GitHub files 附件 URL 正则模式 - HTML 格式
        self._github_files_html_pattern = re.compile(
            r'<a[^>]*href="(https://github\.com/user-attachments/files/\d+/[^"]+)"[^>]*>'
        )
        # raw.githubusercontent.com URL 正则模式 - Markdown 图片格式
        self._raw_github_markdown_pattern = re.compile(
            r'!\[([^\]]*)\]\((https://raw\.githubusercontent\.com/[^)]+\.(?:jpg|jpeg|png|gif|webp|svg|bmp))\)',
            re.IGNORECASE
        )
        # raw.githubusercontent.com URL 正则模式 - HTML 格式（宽松匹配所有图片）
        self._raw_github_html_pattern = re.compile(
            r'<img[^>]*src="(https://raw\.githubusercontent\.com/[^"]+\.(?:jpg|jpeg|png|gif|webp|svg|bmp))"[^>]*>',
            re.IGNORECASE
        )
        # raw.githubusercontent.com URL 正则模式 - Markdown 链接格式（所有附件类型）
        self._raw_github_link_pattern = re.compile(
            r'(?<!!)\[([^\]]+)\]\((https://raw\.githubusercontent\.com/[^)]+\.[a-zA-Z0-9]+)\)',
            re.IGNORECASE
        )
        # 知乎图片 URL 正则模式 - Markdown 格式
        self._zhihu_markdown_pattern = re.compile(
            r'!\[([^\]]*)\]\((https?://pic[^.]*\.zhimg\.com/[^)]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^)]*)?)\)',
            re.IGNORECASE
        )
        # 知乎图片 URL 正则模式 - HTML 格式
        self._zhihu_html_pattern = re.compile(
            r'<img[^>]*src="(https?://pic[^.]*\.zhimg\.com/[^"]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^"]*)?)"[^>]*>',
            re.IGNORECASE
        )
        logger.debug("图片处理器初始化完成")
    
    def _extract_uuid_from_url(self, url: str) -> str:
        """
        从 GitHub 附件 URL 中提取 UUID
        
        Args:
            url: GitHub 附件 URL
            
        Returns:
            UUID 字符串，如果提取失败返回空字符串
        """
        try:
            # GitHub 附件 URL 格式: https://github.com/user-attachments/assets/{uuid}
            match = re.search(r'/assets/([a-f0-9\-]+)', url)
            if match:
                return match.group(1)
            return ""
        except Exception as e:
            logger.warning(f"提取 UUID 失败 {url}: {str(e)}")
            return ""
    
    def _extract_file_id_and_name(self, url: str) -> tuple:
        """
        从 user-attachments/files URL 中提取文件 ID 和原始文件名
        
        Args:
            url: user-attachments/files URL
            格式: https://github.com/user-attachments/files/{id}/{filename}
            
        Returns:
            (file_id, filename) 元组，失败返回 ("", "")
        """
        try:
            from urllib.parse import unquote
            
            # 提取文件 ID 和文件名
            match = re.search(r'/files/(\d+)/([^/?#]+)', url)
            if match:
                file_id = match.group(1)
                filename = unquote(match.group(2))  # URL 解码
                logger.debug(f"从 files URL 提取: ID={file_id}, 文件名={filename}")
                return file_id, filename
            return "", ""
        except Exception as e:
            logger.warning(f"提取文件 ID 和文件名失败 {url}: {str(e)}")
            return "", ""
    
    def _extract_filename_from_raw_url(self, url: str) -> str:
        """
        从 raw.githubusercontent.com URL 中提取文件名
        
        Args:
            url: raw.githubusercontent.com URL
            
        Returns:
            文件名，如果提取失败返回空字符串
        """
        try:
            from urllib.parse import urlparse, unquote
            
            # 解析 URL
            parsed = urlparse(url)
            # 获取路径的最后一部分
            path = parsed.path
            filename = path.split('/')[-1]
            
            # URL 解码（处理中文等字符）
            filename = unquote(filename)
            
            if filename:
                logger.debug(f"从 raw URL 提取文件名: {filename}")
                return filename
            
            return ""
        except Exception as e:
            logger.warning(f"从 raw URL 提取文件名失败 {url}: {str(e)}")
            return ""
    
    def _extract_filename_from_zhihu_url(self, url: str) -> str:
        """
        从知乎图片 URL 中提取文件名
        URL 格式: https://pic1.zhimg.com/50/v2-xxx_720w.jpg?source=xxx
        
        Args:
            url: 知乎图片 URL
            
        Returns:
            文件名，如果提取失败返回空字符串
        """
        try:
            from urllib.parse import urlparse, unquote
            
            # 解析 URL，移除查询参数
            parsed = urlparse(url)
            # 获取路径的最后一部分
            path = parsed.path
            filename = path.split('/')[-1]
            
            # URL 解码（处理中文等字符）
            filename = unquote(filename)
            
            if filename:
                logger.debug(f"从知乎 URL 提取文件名: {filename}")
                return filename
            
            return ""
        except Exception as e:
            logger.warning(f"从知乎 URL 提取文件名失败 {url}: {str(e)}")
            return ""
    
    def extract_github_image_urls(self, content: str) -> List[str]:
        """
        从内容中提取图片和附件 URL（支持 Markdown 和 HTML 格式）
        包括：GitHub 附件 URL (assets/files)、raw.githubusercontent.com URL 和知乎图片 URL
        
        Args:
            content: Markdown 或 HTML 内容
            
        Returns:
            图片和附件 URL 列表
        """
        try:
            urls = []
            
            # 提取 GitHub 附件 URL (assets) - Markdown 格式
            attachment_markdown_matches = self._github_attachment_markdown_pattern.findall(content)
            attachment_markdown_urls = [match[1] for match in attachment_markdown_matches]  # match[1] 是 URL 部分
            urls.extend(attachment_markdown_urls)
            
            # 提取 GitHub 附件 URL (assets) - HTML 格式
            attachment_html_matches = self._github_attachment_html_pattern.findall(content)
            urls.extend(attachment_html_matches)
            
            # 提取 GitHub files 附件 URL - Markdown 格式
            files_markdown_matches = self._github_files_markdown_pattern.findall(content)
            files_markdown_urls = [match[1] for match in files_markdown_matches]  # match[1] 是 URL 部分
            urls.extend(files_markdown_urls)
            
            # 提取 GitHub files 附件 URL - HTML 格式
            files_html_matches = self._github_files_html_pattern.findall(content)
            urls.extend(files_html_matches)
            
            # 提取 raw.githubusercontent.com URL - Markdown 图片格式
            raw_markdown_matches = self._raw_github_markdown_pattern.findall(content)
            raw_markdown_urls = [match[1] for match in raw_markdown_matches]  # match[1] 是 URL 部分
            urls.extend(raw_markdown_urls)
            
            # 提取 raw.githubusercontent.com URL - HTML 格式
            raw_html_matches = self._raw_github_html_pattern.findall(content)
            urls.extend(raw_html_matches)
            
            # 提取 raw.githubusercontent.com URL - Markdown 链接格式（所有附件类型）
            raw_link_matches = self._raw_github_link_pattern.findall(content)
            raw_link_urls = [match[1] for match in raw_link_matches]  # match[1] 是 URL 部分
            urls.extend(raw_link_urls)
            
            # 提取知乎图片 URL - Markdown 格式
            zhihu_markdown_matches = self._zhihu_markdown_pattern.findall(content)
            zhihu_markdown_urls = [match[1] for match in zhihu_markdown_matches]  # match[1] 是 URL 部分
            urls.extend(zhihu_markdown_urls)
            
            # 提取知乎图片 URL - HTML 格式
            zhihu_html_matches = self._zhihu_html_pattern.findall(content)
            urls.extend(zhihu_html_matches)
            
            # 去重
            urls = list(set(urls))
            
            # 统计数量
            assets_count = len(attachment_markdown_urls) + len(attachment_html_matches)
            files_count = len(files_markdown_urls) + len(files_html_matches)
            raw_count = len(raw_markdown_urls) + len(raw_html_matches) + len(raw_link_urls)
            zhihu_count = len(zhihu_markdown_urls) + len(zhihu_html_matches)
            
            logger.debug(f"提取到 {len(urls)} 个附件 URL (GitHub assets: {assets_count}, GitHub files: {files_count}, raw: {raw_count}, 知乎: {zhihu_count})")
            return urls
            
        except Exception as e:
            logger.error(f"提取附件 URL 失败: {str(e)}")
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
                logger.debug(f"附件已存在，跳过下载: {save_path}")
                return True
            
            # 确保目录存在
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 下载图片
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 保存文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"附件下载成功: {url} -> {save_path}")
            return True
            
        except Exception as e:
            logger.warning(f"图片下载失败 {url}: {str(e)}")
            return False
    
    def download_article_images(self, article: Article) -> Dict[str, str]:
        """
        下载文章的所有图片和附件
        
        Args:
            article: 文章对象
            
        Returns:
            URL 映射表 {原始URL: 本地相对路径}
        """
        try:
            # 提取图片和附件 URL
            image_urls = self.extract_github_image_urls(article.content)
            
            if not image_urls:
                logger.debug(f"文章 {article.title} 没有需要处理的附件")
                return {}
            
            # 确保附件目录存在
            image_dir = article.local_images_dir
            logger.info(f"附件保存目录: {image_dir.absolute()}")
            image_dir.mkdir(parents=True, exist_ok=True)
            
            url_map = {}
            success_count = 0
            
            for url in image_urls:
                try:
                    # 判断 URL 类型并提取文件名
                    if 'user-attachments/files/' in url:
                        # GitHub files 附件 - 使用 ID-原始文件名
                        file_id, original_name = self._extract_file_id_and_name(url)
                        if not file_id or not original_name:
                            logger.warning(f"无法从 files URL 中提取文件信息: {url}")
                            url_map[url] = url
                            continue
                        filename = f"{file_id}-{original_name}"
                    elif 'raw.githubusercontent.com' in url:
                        # raw.githubusercontent.com URL - 提取原始文件名
                        filename = self._extract_filename_from_raw_url(url)
                        if not filename:
                            logger.warning(f"无法从 raw URL 中提取文件名: {url}")
                            url_map[url] = url
                            continue
                    elif 'zhimg.com' in url:
                        # 知乎图片 URL - 提取原始文件名
                        filename = self._extract_filename_from_zhihu_url(url)
                        if not filename:
                            logger.warning(f"无法从知乎 URL 中提取文件名: {url}")
                            url_map[url] = url
                            continue
                    else:
                        # GitHub 附件 URL (assets) - 使用 UUID 作为文件名
                        uuid = self._extract_uuid_from_url(url)
                        if not uuid:
                            logger.warning(f"无法从 URL 中提取 UUID: {url}")
                            url_map[url] = url
                            continue
                        
                        # 获取文件扩展名
                        extension = self._get_image_extension(url)
                        filename = f"{uuid}{extension}"
                    
                    save_path = image_dir / filename
                    
                    # 下载附件（download_image 方法会打印详细日志）
                    if self.download_image(url, save_path):
                        # 生成相对路径（从 html/articles/{分类}/ 到附件）
                        relative_path = f"../../../assets/images/{article.image_dir_name}/{filename}"
                        url_map[url] = relative_path
                        success_count += 1
                    else:
                        # 下载失败，保留原始 URL
                        url_map[url] = url
                        
                except Exception as e:
                    logger.warning(f"处理附件失败 {url}: {str(e)}")
                    url_map[url] = url  # 保留原始 URL
            
            logger.info(f"文章 {article.title} 附件处理完成: {success_count}/{len(image_urls)} 成功")
            return url_map
            
        except Exception as e:
            logger.error(f"下载文章附件失败 {article.title}: {str(e)}")
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
