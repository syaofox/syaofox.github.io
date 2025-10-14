# -*- coding: utf-8 -*-
"""
配置管理模块
封装环境变量加载和全局配置管理
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置"""
        self._load_env_vars()
        self._setup_paths()
    
    def _load_env_vars(self) -> None:
        """加载环境变量"""
        # 检查是否在 GitHub Actions 环境中运行
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print("检测到 GitHub Actions 环境，跳过 .env 文件加载")
            return
        
        env_file = ".env"
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print(f"已加载环境变量文件: {env_file}")
        else:
            print("未找到 .env 文件，使用系统环境变量")
    
    def _setup_paths(self) -> None:
        """设置路径配置"""
        self.project_root = Path(__file__).parent.parent.parent
        self.templates_dir = self.project_root / "src" / "templates"
        self.assets_dir = self.project_root / "assets"
        self.fonts_dir = self.project_root / "lib" / "fonts"
        
        # HTML 输出目录配置
        self.html_dir = self.project_root / "html"
        self.html_articles_dir = self.html_dir / "articles"
        self.html_assets_dir = self.html_dir / "assets"
        self.html_static_dir = self.html_dir / "static"
    
    @property
    def github_repository(self) -> str:
        """获取 GitHub 仓库名称"""
        repo = os.environ.get("GITHUB_REPOSITORY")
        if not repo:
            raise ValueError("GITHUB_REPOSITORY 环境变量未设置")
        return repo
    
    @property
    def github_token(self) -> str:
        """获取 GitHub 访问令牌"""
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN 环境变量未设置")
        return token
    
    @property
    def user_name(self) -> str:
        """获取用户名"""
        repo = self.github_repository
        return repo.split('/')[0]
    
    @property
    def blog_name(self) -> str:
        """获取博客仓库名"""
        repo = self.github_repository
        return repo.split('/')[1]
    
    @property
    def font_path(self) -> str:
        """获取字体文件路径"""
        font_file = self.fonts_dir / "wqy-microhei.ttc"
        if not font_file.exists():
            raise FileNotFoundError(f"字体文件不存在: {font_file}")
        return str(font_file)
    
    def ensure_directories(self) -> None:
        """确保必要的目录存在"""
        directories = [
            self.assets_dir,
            self.html_dir,
            self.html_articles_dir,
            self.html_assets_dir,
            self.html_static_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"确保目录存在: {directory}")


# 全局配置实例
config = Config()
