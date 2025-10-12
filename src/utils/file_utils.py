# -*- coding: utf-8 -*-
"""
文件操作工具模块
封装文件读写和目录操作
"""

import os
import codecs
import shutil
import logging
from pathlib import Path
from typing import Optional

from ..core.config import config

logger = logging.getLogger(__name__)


def ensure_directory_exists(directory: Path) -> None:
    """
    确保目录存在
    
    Args:
        directory: 目录路径
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"确保目录存在: {directory}")
    except Exception as e:
        logger.error(f"创建目录失败 {directory}: {str(e)}")
        raise


def write_text_file(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """
    写入文本文件
    
    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 文件编码
    """
    try:
        # 确保父目录存在
        ensure_directory_exists(file_path.parent)
        
        with codecs.open(str(file_path), "w", encoding=encoding) as f:
            f.write(content)
            f.flush()
        
        logger.info(f"文件写入成功: {file_path}")
        
    except Exception as e:
        logger.error(f"文件写入失败 {file_path}: {str(e)}")
        raise


def read_text_file(file_path: Path, encoding: str = "utf-8") -> str:
    """
    读取文本文件
    
    Args:
        file_path: 文件路径
        encoding: 文件编码
        
    Returns:
        文件内容
    """
    try:
        with codecs.open(str(file_path), "r", encoding=encoding) as f:
            content = f.read()
        
        logger.debug(f"文件读取成功: {file_path}")
        return content
        
    except Exception as e:
        logger.error(f"文件读取失败 {file_path}: {str(e)}")
        raise


def file_exists(file_path: Path) -> bool:
    """
    检查文件是否存在
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件是否存在
    """
    return file_path.exists() and file_path.is_file()


def directory_exists(directory: Path) -> bool:
    """
    检查目录是否存在
    
    Args:
        directory: 目录路径
        
    Returns:
        目录是否存在
    """
    return directory.exists() and directory.is_dir()


def create_article_directory(label: str) -> Path:
    """
    创建文章目录
    
    Args:
        label: 标签名称
        
    Returns:
        创建的目录路径
    """
    articles_dir = config.html_articles_dir / label
    ensure_directory_exists(articles_dir)
    return articles_dir


def save_article_html(article_path: Path, html_content: str) -> None:
    """
    保存文章 HTML 文件
    
    Args:
        article_path: 文章文件路径
        html_content: HTML 内容
    """
    write_text_file(article_path, html_content)


def save_readme_md(content: str) -> None:
    """
    保存 README.md 文件
    
    Args:
        content: README 内容
    """
    readme_path = config.project_root / "README.md"
    write_text_file(readme_path, content)


def save_index_html(content: str) -> None:
    """
    保存 index.html 文件
    
    Args:
        content: index.html 内容
    """
    index_path = config.html_dir / "index.html"
    write_text_file(index_path, content)


def cleanup_old_articles(articles: list) -> None:
    """
    清理旧的文章文件（可选功能）
    
    Args:
        articles: 当前文章列表
    """
    if not config.html_articles_dir.exists():
        return
    
    # 获取所有当前文章的路径
    current_article_paths = set()
    for article in articles:
        # url_path 已经包含了 articles/ 前缀，所以需要移除它
        relative_path = article.url_path.replace("articles/", "")
        article_path = config.html_articles_dir / relative_path
        current_article_paths.add(article_path)
    
    # 删除不在当前列表中的文章文件
    for article_file in config.html_articles_dir.rglob("*.html"):
        if article_file not in current_article_paths:
            try:
                article_file.unlink()
                logger.info(f"删除旧文章文件: {article_file}")
            except Exception as e:
                logger.warning(f"删除旧文章文件失败 {article_file}: {str(e)}")


def copy_static_files() -> None:
    """
    复制静态文件到输出目录
    将模板目录中的静态文件复制到 html 目录
    """
    try:
        src_static = config.templates_dir / 'static'
        dst_static = config.html_static_dir
        
        if src_static.exists():
            if dst_static.exists():
                shutil.rmtree(dst_static)
            shutil.copytree(src_static, dst_static)
            logger.info(f"静态文件复制完成: {src_static} -> {dst_static}")
        else:
            logger.debug(f"源静态目录不存在: {src_static}")
            
    except Exception as e:
        logger.error(f"复制静态文件失败: {str(e)}")
        raise


def copy_assets_to_html() -> None:
    """
    复制 assets 目录到 html 目录
    """
    try:
        src_assets = config.assets_dir
        dst_assets = config.html_assets_dir
        
        if src_assets.exists():
            if dst_assets.exists():
                shutil.rmtree(dst_assets)
            shutil.copytree(src_assets, dst_assets)
            logger.info(f"Assets 复制完成: {src_assets} -> {dst_assets}")
        else:
            logger.debug(f"源 assets 目录不存在: {src_assets}")
            
    except Exception as e:
        logger.error(f"复制 assets 失败: {str(e)}")
        raise
