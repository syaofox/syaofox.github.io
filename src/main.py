# -*- coding: utf-8 -*-
"""
重构后的主程序
模块化架构的博客生成器主入口
"""

import time
import logging
from datetime import datetime
from typing import List

from .core.config import config
from .core.github_client import github_client
from .models.article import Article
from .generators.html_generator import HTMLGenerator
from .generators.readme_generator import ReadmeGenerator
from .generators.wordcloud_generator import WordCloudGenerator
from .utils.file_utils import (
    save_readme_md, 
    save_index_html, 
    save_article_html, 
    create_article_directory,
    cleanup_old_articles
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BlogGenerator:
    """博客生成器主类"""
    
    def __init__(self):
        """初始化博客生成器"""
        self.html_generator = None
        self.readme_generator = None
        self.wordcloud_generator = None
        self.articles: List[Article] = []
        
        logger.info("博客生成器初始化开始")
    
    def initialize(self) -> None:
        """初始化各个组件"""
        try:
            # 确保目录存在
            config.ensure_directories()
            
            # 初始化生成器
            self.html_generator = HTMLGenerator()
            self.readme_generator = ReadmeGenerator()
            self.wordcloud_generator = WordCloudGenerator()
            
            logger.info("博客生成器初始化完成")
            
        except Exception as e:
            logger.error(f"初始化失败: {str(e)}")
            raise
    
    def fetch_data(self) -> None:
        """获取数据"""
        try:
            logger.info("开始获取 GitHub 数据...")
            
            # 获取所有 issues
            issues = github_client.get_all_issues()
            
            # 转换为 Article 对象
            self.articles = [Article.from_github_issue(issue) for issue in issues]
            
            logger.info(f"数据获取完成，共 {len(self.articles)} 篇文章")
            
        except Exception as e:
            logger.error(f"获取数据失败: {str(e)}")
            raise
    
    def generate_content(self) -> tuple[str, str, str]:
        """
        生成内容
        
        Returns:
            (README 内容, index.html 内容, 词云路径)
        """
        try:
            cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            logger.info("开始生成内容...")
            
            # 生成词云
            logger.info("生成词云...")
            wordcloud_path = self.wordcloud_generator.generate(self.articles)
            
            # 生成 README
            logger.info("生成 README.md...")
            readme_content = self.readme_generator.generate_readme_content(
                self.articles, cur_time, wordcloud_path
            )
            
            # 生成首页 HTML
            logger.info("生成 index.html...")
            index_html = self.html_generator.generate_index_html(self.articles, cur_time)
            
            logger.info("内容生成完成")
            return readme_content, index_html, wordcloud_path
            
        except Exception as e:
            logger.error(f"生成内容失败: {str(e)}")
            raise
    
    def generate_articles(self) -> int:
        """
        生成文章 HTML 文件
        
        Returns:
            生成的文章数量
        """
        try:
            logger.info("开始生成文章 HTML 文件...")
            
            generated_count = 0
            
            for article in self.articles:
                try:
                    # 生成文章 HTML
                    article_html = self.html_generator.generate_article_html(article)
                    
                    # 创建文章目录
                    article_dir = create_article_directory(article.primary_label)
                    
                    # 保存文章文件
                    article_path = article_dir / article.filename
                    save_article_html(article_path, article_html)
                    
                    generated_count += 1
                    logger.debug(f"生成文章: {article.title} -> {article_path}")
                    
                except Exception as e:
                    logger.error(f"生成文章失败 {article.title}: {str(e)}")
                    continue
            
            logger.info(f"文章 HTML 生成完成! 共生成 {generated_count} 篇文章")
            return generated_count
            
        except Exception as e:
            logger.error(f"生成文章失败: {str(e)}")
            raise
    
    def save_files(self, readme_content: str, index_html: str) -> None:
        """
        保存文件
        
        Args:
            readme_content: README 内容
            index_html: index.html 内容
        """
        try:
            logger.info("开始保存文件...")
            
            # 保存 README.md
            save_readme_md(readme_content)
            logger.info("README.md 保存成功")
            
            # 保存 index.html
            save_index_html(index_html)
            logger.info("index.html 保存成功")
            
            # 清理旧文章（可选）
            cleanup_old_articles(self.articles)
            
            logger.info("文件保存完成")
            
        except Exception as e:
            logger.error(f"保存文件失败: {str(e)}")
            raise
    
    def cleanup(self) -> None:
        """清理资源"""
        try:
            if self.html_generator:
                self.html_generator.close()
            
            github_client.close()
            
            logger.info("资源清理完成")
            
        except Exception as e:
            logger.error(f"资源清理失败: {str(e)}")
    
    def run(self) -> None:
        """运行博客生成器"""
        try:
            logger.info("博客生成器开始运行")
            start_time = time.time()
            
            # 执行流程
            self.initialize()
            self.fetch_data()
            readme_content, index_html, wordcloud_path = self.generate_content()
            article_count = self.generate_articles()
            self.save_files(readme_content, index_html)
            
            # 统计信息
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info(f"博客生成器运行完成!")
            logger.info(f"处理时间: {duration:.2f} 秒")
            logger.info(f"生成文章: {article_count} 篇")
            logger.info(f"词云路径: {wordcloud_path}")
            
        except Exception as e:
            logger.error(f"博客生成器运行失败: {str(e)}")
            raise
        finally:
            self.cleanup()


def main():
    """主函数"""
    generator = BlogGenerator()
    generator.run()


if __name__ == "__main__":
    main()
