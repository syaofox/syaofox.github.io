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
from .models.backup import ArticleBackup
from .generators.html_generator import HTMLGenerator
from .generators.wordcloud_generator import WordCloudGenerator
from .utils.file_utils import (
    save_index_html, 
    save_article_html, 
    create_article_directory,
    cleanup_old_articles,
    copy_static_files,
    copy_assets_to_html
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
        self.wordcloud_generator = None
        self.article_backup = None
        self.articles: List[Article] = []
        
        logger.info("博客生成器初始化开始")
    
    def initialize(self) -> None:
        """初始化各个组件"""
        try:
            # 确保目录存在
            config.ensure_directories()
            
            # 初始化生成器
            self.html_generator = HTMLGenerator()
            self.wordcloud_generator = WordCloudGenerator()
            self.article_backup = ArticleBackup(config.backup_dir)
            
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
            
            # 转换为 Article 对象（包含评论）
            self.articles = [Article.from_github_issue(issue, include_comments=True) for issue in issues]
            
            logger.info(f"数据获取完成，共 {len(self.articles)} 篇文章")
            
        except Exception as e:
            logger.error(f"获取数据失败: {str(e)}")
            raise
    
    def backup_articles(self) -> int:
        """
        备份文章到 Markdown 文件
        
        Returns:
            备份的文章数量
        """
        try:
            logger.info("开始备份文章...")
            
            # 构建评论映射（如果需要的话）
            issue_comments_map = {}
            for article in self.articles:
                if article.comments:
                    issue_comments_map[article.number] = article.comments
            
            # 执行备份
            backup_count = self.article_backup.backup_all_articles(self.articles, issue_comments_map)
            
            logger.info(f"文章备份完成! 共备份 {backup_count} 篇文章")
            return backup_count
            
        except Exception as e:
            logger.error(f"备份文章失败: {str(e)}")
            # 备份失败不影响主流程，只记录错误
            return 0
    
    def generate_content(self) -> str:
        """
        生成内容
        
        Returns:
            index.html 内容
        """
        try:
            cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            logger.info("开始生成内容...")
            
            # 生成词云
            logger.info("生成词云...")
            self.wordcloud_generator.generate(self.articles)
            
            # 生成首页 HTML
            logger.info("生成 index.html...")
            index_html = self.html_generator.generate_index_html(self.articles, cur_time)
            
            logger.info("内容生成完成")
            return index_html
            
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
    
    def save_files(self, index_html: str) -> None:
        """
        保存文件
        
        Args:
            index_html: index.html 内容
        """
        try:
            logger.info("开始保存文件...")
            
            # 保存 index.html
            save_index_html(index_html)
            logger.info("index.html 保存成功")
            
            # 清理旧文章（可选）
            cleanup_old_articles(self.articles)
            
            # 复制静态文件（CSS 等）
            copy_static_files()
            logger.info("静态文件复制完成")
            
            # 复制 assets 到 html 目录
            copy_assets_to_html()
            logger.info("Assets 复制完成")
            
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
            backup_count = self.backup_articles()
            index_html = self.generate_content()
            article_count = self.generate_articles()
            self.save_files(index_html)
            
            # 统计信息
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info(f"博客生成器运行完成!")
            logger.info(f"处理时间: {duration:.2f} 秒")
            logger.info(f"备份文章: {backup_count} 篇")
            logger.info(f"生成文章: {article_count} 篇")
            
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
