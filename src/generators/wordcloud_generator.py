# -*- coding: utf-8 -*-
"""
词云生成器模块
重构现有的词云生成功能，优化 API 调用
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional

from wordcloud import WordCloud

from ..core.config import config
from ..core.github_client import github_client
from ..models.article import Article

logger = logging.getLogger(__name__)


class WordCloudGenerator:
    """词云生成器"""
    
    def __init__(self):
        """初始化词云生成器"""
        self._repo = github_client.repo
        self._font_path = config.font_path
        self._assets_dir = config.assets_dir
        
        logger.debug("词云生成器初始化完成")
    
    def generate(self, articles: Optional[List[Article]] = None) -> str:
        """
        生成词云图片
        
        Args:
            articles: 文章列表，如果为 None 则从 GitHub 获取
            
        Returns:
            生成的词云图片路径
        """
        try:
            # 计算标签频率
            frequencies = self._calculate_label_frequencies(articles)
            
            if not frequencies or all(freq == 0 for freq in frequencies.values()):
                logger.warning("没有找到带标签的文章，跳过词云生成")
                return 'assets/wordcloud.png'
            
            logger.info(f"标签频率: {frequencies}")
            
            # 生成浅色主题词云
            light_path = self._generate_wordcloud(
                frequencies, 
                'white', 
                'viridis',
                self._assets_dir / 'wordcloud-light.png'
            )
            
            # 生成深色主题词云
            dark_path = self._generate_wordcloud(
                frequencies, 
                '#1a1a1a', 
                'plasma',
                self._assets_dir / 'wordcloud-dark.png'
            )
            
            # 生成默认词云（兼容性）
            default_path = self._generate_wordcloud(
                frequencies, 
                'white', 
                'viridis',
                self._assets_dir / 'wordcloud.png'
            )
            
            logger.info("词云图片生成成功")
            return 'assets/wordcloud-light.png'
            
        except Exception as e:
            logger.error(f"词云生成失败: {str(e)}")
            # 返回默认路径，避免程序中断
            return 'assets/wordcloud.png'
    
    def _calculate_label_frequencies(self, articles: Optional[List[Article]] = None) -> Dict[str, int]:
        """
        计算标签频率
        
        Args:
            articles: 文章列表
            
        Returns:
            标签频率字典
        """
        frequencies = {}
        
        if articles is not None:
            # 使用提供的文章列表
            for article in articles:
                for label in article.labels:
                    frequencies[label] = frequencies.get(label, 0) + 1
        else:
            # 从 GitHub 获取数据（兼容原有逻辑）
            try:
                labels = github_client.get_all_labels()
                for label in labels:
                    issues = github_client.get_issues_by_label(label)
                    frequencies[label.name] = len(issues)
                    logger.debug(f"标签 {label.name}: {len(issues)} 个 issues")
            except Exception as e:
                logger.error(f"从 GitHub 获取标签数据失败: {str(e)}")
                raise
        
        return frequencies
    
    def _generate_wordcloud(
        self, 
        frequencies: Dict[str, int], 
        background_color: str, 
        colormap: str, 
        output_path: Path
    ) -> Path:
        """
        生成单个词云图片
        
        Args:
            frequencies: 标签频率
            background_color: 背景颜色
            colormap: 颜色映射
            output_path: 输出路径
            
        Returns:
            生成的图片路径
        """
        try:
            wc = WordCloud(
                font_path=self._font_path,
                width=1920,
                height=400,
                background_color=background_color,
                colormap=colormap,
                relative_scaling=0.5 if background_color == '#1a1a1a' else 1.0
            )
            
            wc.generate_from_frequencies(frequencies=frequencies)
            wc.to_file(str(output_path))
            
            logger.debug(f"词云图片保存到: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"生成词云图片失败 {output_path}: {str(e)}")
            raise


def generate_wordcloud(articles: Optional[List[Article]] = None) -> str:
    """
    便捷函数：生成词云
    
    Args:
        articles: 文章列表
        
    Returns:
        词云图片路径
    """
    generator = WordCloudGenerator()
    return generator.generate(articles)
