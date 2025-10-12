# -*- coding: utf-8 -*-
"""
文本处理工具模块
封装 Markdown 转换和文本处理逻辑
"""

import markdown
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MarkdownProcessor:
    """Markdown 处理器"""
    
    def __init__(self):
        """初始化 Markdown 处理器"""
        self._md_instance = markdown.Markdown(
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
        logger.debug("Markdown 处理器初始化完成")
    
    def convert_to_html(self, markdown_text: str) -> str:
        """
        将 Markdown 文本转换为 HTML
        
        Args:
            markdown_text: Markdown 文本
            
        Returns:
            转换后的 HTML 文本
        """
        try:
            # 重置 Markdown 实例状态
            self._md_instance.reset()
            
            # 转换 Markdown 内容为 HTML
            html_content = self._md_instance.convert(markdown_text or '')
            
            logger.debug("Markdown 转换成功")
            return html_content
            
        except Exception as e:
            logger.error(f"Markdown 转换失败: {str(e)}")
            raise
    
    def close(self) -> None:
        """清理资源"""
        if self._md_instance:
            self._md_instance.reset()
            logger.debug("Markdown 处理器已清理")


def format_issue_summary(issue) -> str:
    """
    格式化 issue 摘要（用于 README.md）
    
    Args:
        issue: GitHub Issue 对象
        
    Returns:
        格式化后的 markdown 字符串
    """
    return "- %s [%s](%s) \n" % (
        issue.created_at.strftime("%Y-%m-%d"),
        issue.title,
        issue.html_url,
    )


def generate_summary_section(user_name: str, blog_name: str, cur_time: str) -> str:
    """
    生成摘要部分 HTML
    
    Args:
        user_name: 用户名
        blog_name: 博客名
        cur_time: 当前时间
        
    Returns:
        摘要部分 HTML
    """
    return f"""
<p align='center'>
    <img src="https://badgen.net/github/issues/{user_name}{blog_name}"/>
    <img src="https://badgen.net/badge/last-commit/{cur_time}"/>
    <img src="https://badgen.net/github/forks/{user_name}{blog_name}"/>
    <img src="https://badgen.net/github/stars/{user_name}{blog_name}"/>
    <img src="https://badgen.net/github/watchers/{user_name}{blog_name}"/>
</p>

"""


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全的字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 移除或替换不安全的字符
    unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    safe_filename = filename
    
    for char in unsafe_chars:
        safe_filename = safe_filename.replace(char, '_')
    
    # 限制长度
    if len(safe_filename) > 200:
        safe_filename = safe_filename[:200].rstrip('_')
    
    return safe_filename


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本到指定长度
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后的后缀
        
    Returns:
        截断后的文本
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """
    规范化空白字符
    
    Args:
        text: 原始文本
        
    Returns:
        规范化后的文本
    """
    if not text:
        return ""
    
    # 将多个连续空白字符替换为单个空格
    import re
    normalized = re.sub(r'\s+', ' ', text)
    
    # 移除首尾空白
    return normalized.strip()
