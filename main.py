#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
兼容入口文件
为了保持向后兼容，此文件作为重构后模块的入口点
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# 导入重构后的模块
from src.main import main


if __name__ == "__main__":
    main()
