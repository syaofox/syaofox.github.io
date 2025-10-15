# -*- coding: utf-8 -*-
"""
README 生成器模块
生成 README.md 内容
"""

import logging
from typing import List

from ..core.github_client import github_client
from ..models.article import Article, Category, group_articles_by_category
from ..utils.text_utils import generate_summary_section, format_issue_summary

logger = logging.getLogger(__name__)


class ReadmeGenerator:
    """README 生成器"""
    
    def __init__(self):
        """初始化 README 生成器"""
        logger.debug("README 生成器初始化完成")
    
    def generate_readme_content(self, articles: List[Article], cur_time: str, wordcloud_url: str) -> str:
        """
        生成 README.md 内容
        
        Args:
            articles: 文章列表
            cur_time: 当前时间
            wordcloud_url: 词云图片 URL
            
        Returns:
            生成的 README 内容
        """
        try:
            # 生成摘要部分
            summary_section = self._generate_summary_section(cur_time)
            
            # 生成标签列表部分
            list_by_labels_section = self._generate_list_by_labels_section(articles, wordcloud_url)
            
            # 组合内容
            content = summary_section + list_by_labels_section
            
            logger.info("README 内容生成成功")
            return content
            
        except Exception as e:
            logger.error(f"生成 README 内容失败: {str(e)}")
            raise
    
    def _generate_summary_section(self, cur_time: str) -> str:
        """
        生成摘要部分
        
        Args:
            cur_time: 当前时间
            
        Returns:
            摘要部分内容
        """
        return generate_summary_section(
            github_client.user_name,
            github_client.blog_name,
            cur_time
        )
    
    def _generate_list_by_labels_section(self, articles: List[Article], wordcloud_url: str) -> str:
        """
        生成按标签分类的文章列表部分
        
        Args:
            articles: 文章列表
            wordcloud_url: 词云图片 URL
            
        Returns:
            标签列表部分内容
        """
        try:
            # 按分类分组文章
            categories = group_articles_by_category(articles)
            
            # 生成词云部分
            wordcloud_section = self._generate_wordcloud_section(wordcloud_url)
            
            # 生成分类列表
            categories_html = ""
            for category in categories:
                if category.count > 0:
                    # 生成该分类下的文章列表
                    articles_html = ""
                    for article in category.articles:
                        articles_html += f"- {article.created_date_str} [{article.title}]({article.github_url}) \n"
                    
                    categories_html += f"""
<details open>
<summary>{category.name}\t[{category.count}篇]</summary>

{articles_html}

</details>
"""
            
            return wordcloud_section + categories_html
            
        except Exception as e:
            logger.error(f"生成标签列表部分失败: {str(e)}")
            raise
    
    def _generate_wordcloud_section(self, wordcloud_url: str) -> str:
        """
        生成词云部分
        
        Args:
            wordcloud_url: 词云图片 URL
            
        Returns:
            词云部分内容
        """
        return f"""
<summary>
    <a href="https://{github_client.user_name}.github.io/{github_client.blog_name}/"><img src="{wordcloud_url}" title="心似白云常自在，意如流水任东西。" alt="syaofox的博客标签云"></a>
</summary>  
"""


def generate_readme_content(articles: List[Article], cur_time: str, wordcloud_url: str) -> str:
    """
    便捷函数：生成 README 内容
    
    Args:
        articles: 文章列表
        cur_time: 当前时间
        wordcloud_url: 词云图片 URL
        
    Returns:
        README 内容
    """
    generator = ReadmeGenerator()
    return generator.generate_readme_content(articles, cur_time, wordcloud_url)
