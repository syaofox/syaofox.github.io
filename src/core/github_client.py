# -*- coding: utf-8 -*-
"""
GitHub API 客户端模块
封装 GitHub API 交互和速率限制处理
"""

import time
import logging
from datetime import datetime
from typing import List, Optional

from github import Github, Auth
from github.Repository import Repository
from github.Label import Label
from github.Issue import Issue

from .config import config


logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHub API 客户端"""
    
    def __init__(self):
        """初始化 GitHub 客户端"""
        self._github: Optional[Github] = None
        self._repo: Optional[Repository] = None
        self._user_name: Optional[str] = None
        self._blog_name: Optional[str] = None
        self._connected: bool = False
    
    def _connect(self) -> None:
        """连接到 GitHub API"""
        if self._connected:
            return
            
        try:
            self._user_name = config.user_name
            self._blog_name = config.blog_name
            token = config.github_token
            
            # 使用新版 PyGithub Auth
            self._github = Github(auth=Auth.Token(token))
            self._repo = self._github.get_repo(config.github_repository)
            self._connected = True
            
            logger.info(f"成功连接到 GitHub 仓库: {config.github_repository}")
            print(f"GitHub 仓库: {self._repo}")
            
        except Exception as e:
            logger.error(f"GitHub 连接失败: {str(e)}")
            raise
    
    @property
    def github(self) -> Github:
        """获取 GitHub 客户端实例"""
        self._connect()
        if self._github is None:
            raise RuntimeError("GitHub 客户端未初始化")
        return self._github
    
    @property
    def repo(self) -> Repository:
        """获取仓库实例"""
        self._connect()
        if self._repo is None:
            raise RuntimeError("GitHub 仓库未初始化")
        return self._repo
    
    @property
    def user_name(self) -> str:
        """获取用户名"""
        self._connect()
        if self._user_name is None:
            raise RuntimeError("用户名未初始化")
        return self._user_name
    
    @property
    def blog_name(self) -> str:
        """获取博客名称"""
        self._connect()
        if self._blog_name is None:
            raise RuntimeError("博客名称未初始化")
        return self._blog_name
    
    def check_rate_limit(self) -> None:
        """检查 GitHub API 速率限制"""
        try:
            rate_limit = self.github.get_rate_limit()
            remaining = rate_limit.core.remaining
            
            logger.info(f"API 剩余配额: {remaining}")
            
            if remaining < 100:
                reset_time = rate_limit.core.reset
                wait_seconds = (reset_time - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    logger.warning(f"API 配额不足 (剩余: {remaining})，等待 {wait_seconds:.0f} 秒...")
                    print(f"API 配额不足 (剩余: {remaining})，等待 {wait_seconds:.0f} 秒...")
                    time.sleep(wait_seconds)
                    print("API 配额已重置，继续执行...")
                    logger.info("API 配额已重置")
                    
        except Exception as e:
            logger.error(f"检查 API 速率限制时出错: {str(e)}")
            print(f"检查 API 速率限制时出错: {str(e)}")
    
    def get_all_labels(self) -> List[Label]:
        """获取所有标签"""
        try:
            self.check_rate_limit()
            labels = list(self.repo.get_labels())
            logger.info(f"获取到 {len(labels)} 个标签")
            return labels
        except Exception as e:
            logger.error(f"获取标签失败: {str(e)}")
            raise
    
    def get_all_issues(self) -> List[Issue]:
        """获取所有 open 状态的 issues（不包括 PR）"""
        try:
            self.check_rate_limit()
            issues = [issue for issue in self.repo.get_issues(state="open") 
                      if not issue.pull_request]
            logger.info(f"获取到 {len(issues)} 个 open issues")
            return issues
        except Exception as e:
            logger.error(f"获取 issues 失败: {str(e)}")
            raise
    
    def get_all_issues_for_backup(self) -> List[Issue]:
        """获取所有状态的 issues（不包括 PR），用于备份"""
        try:
            self.check_rate_limit()
            issues = [issue for issue in self.repo.get_issues(state="all") 
                      if not issue.pull_request]
            logger.info(f"获取到 {len(issues)} 个 issues（所有状态）")
            return issues
        except Exception as e:
            logger.error(f"获取 issues 失败: {str(e)}")
            raise
    
    def get_issues_by_label(self, label: Label) -> List[Issue]:
        """根据标签获取 issues"""
        try:
            self.check_rate_limit()
            issues = list(self.repo.get_issues(labels=[label.name], state="all"))
            logger.debug(f"标签 {label.name} 下有 {len(issues)} 个 issues")
            return issues
        except Exception as e:
            logger.error(f"获取标签 {label.name} 的 issues 失败: {str(e)}")
            raise
    
    def close(self) -> None:
        """关闭连接"""
        # PyGithub 的 Github 对象没有 close() 方法
        # 这里只需要清理引用即可
        if self._github:
            self._github = None
            self._repo = None
            self._connected = False
            logger.info("GitHub 连接已清理")


# 全局 GitHub 客户端实例
github_client = GitHubClient()
