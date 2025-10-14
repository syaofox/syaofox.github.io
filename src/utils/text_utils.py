# -*- coding: utf-8 -*-
"""
文本处理工具模块
封装 Markdown 转换和文本处理逻辑
"""

import re
import markdown
import logging
from typing import Optional

from ..core.config import config

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
                },
                'toc': {
                    'anchorlink': True,
                    'permalink': False,
                    'baselevel': 1,
                    'slugify': self._slugify
                }
            }
        )
        self._setup_url_patterns()
        logger.debug("Markdown 处理器初始化完成")
    
    def _setup_url_patterns(self) -> None:
        """设置 URL 替换模式"""
        # 匹配 GitHub raw 链接的两种格式：
        # 1. https://raw.githubusercontent.com/syaofox/syaofox.github.io/main/assets/...
        # 2. https://raw.githubusercontent.com/syaofox/syaofox.github.io/refs/heads/main/assets/...
        escaped_repo = re.escape(config.github_repository)
        self._github_raw_pattern = re.compile(
            r'https://raw\.githubusercontent\.com/'
            + escaped_repo
            + r'/(?:main|refs/heads/main)/(assets/[^"\s)]+)'
        )
        logger.debug(f"URL 模式初始化完成，仓库: {config.github_repository}")
    
    def _convert_github_urls_to_relative(self, html_content: str, article_category: str) -> str:
        """
        将 GitHub raw 链接转换为相对路径
        
        Args:
            html_content: HTML 内容
            article_category: 文章分类（用于计算相对路径）
            
        Returns:
            转换后的 HTML 内容
        """
        # 从 html/articles/分类/ 到 html/assets/
        # 需要向上两级：../../assets/
        def replace_url(match):
            asset_path = match.group(1)  # assets/images/xxx
            return f'../../{asset_path}'
        
        converted = self._github_raw_pattern.sub(replace_url, html_content)
        
        # 统计转换数量
        original_count = len(self._github_raw_pattern.findall(html_content))
        if original_count > 0:
            logger.info(f"URL 转换完成，分类: {article_category}，转换了 {original_count} 个链接")
        
        return converted
    
    def convert_to_html(self, markdown_text: str, article_category: str = '') -> str:
        """
        将 Markdown 文本转换为 HTML
        
        Args:
            markdown_text: Markdown 文本
            article_category: 文章分类（用于 URL 转换）
            
        Returns:
            转换后的 HTML 文本
        """
        try:
            # 重置 Markdown 实例状态
            self._md_instance.reset()
            
            # 转换 Markdown 内容为 HTML
            html_content = self._md_instance.convert(markdown_text or '')
            
            # 转换 GitHub raw 链接为相对路径
            if article_category:
                html_content = self._convert_github_urls_to_relative(html_content, article_category)
            
            logger.debug("Markdown 转换成功")
            return html_content
            
        except Exception as e:
            logger.error(f"Markdown 转换失败: {str(e)}")
            raise
    
    def extract_toc(self, markdown_text: str) -> list:
        """
        提取文章的目录结构
        
        Args:
            markdown_text: Markdown 文本
            
        Returns:
            目录列表，每个元素包含 level, title, anchor
        """
        try:
            import re
            
            toc_items = []
            lines = markdown_text.split('\n')
            
            for line in lines:
                # 匹配标题行 (# ## ### 等)
                match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
                if match:
                    level = len(match.group(1))  # 标题级别
                    title = match.group(2).strip()  # 标题文本
                    
                    # 生成锚点ID（与markdown-toc扩展保持一致）
                    # 使用与 markdown-toc 相同的 slugify 函数
                    anchor = self._slugify(title)
                    
                    toc_items.append({
                        'level': level,
                        'title': title,
                        'anchor': anchor
                    })
            
            logger.debug(f"提取到 {len(toc_items)} 个目录项")
            return toc_items
            
        except Exception as e:
            logger.error(f"提取目录失败: {str(e)}")
            return []
    
    def _slugify(self, text: str, separator: str = '-') -> str:
        """
        生成与 markdown-toc 扩展一致的锚点ID
        与 markdown-toc 的默认 slugify 函数保持一致
        """
        import re
        
        # 转换为小写
        text = text.lower()
        
        # 替换空格为分隔符
        text = text.replace(' ', separator)
        
        # 移除特殊字符，只保留字母、数字和连字符
        text = re.sub(r'[^\w\-]', '', text)
        
        # 移除连续的分隔符
        text = re.sub(r'-+', separator, text)
        
        # 移除首尾分隔符
        text = text.strip(separator)
        
        return text
    
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
