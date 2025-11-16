"""
测试配置文件

运行测试前，请确保：
1. 已安装依赖：pip install -e ".[dev]"
2. 已安装 Playwright：playwright install chromium
"""
import pytest
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_article_url():
    """示例文章 URL"""
    return "https://mp.weixin.qq.com/s/UjZAqvkfk8AzpOoK1KV0yw"


@pytest.fixture
def sample_search_query():
    """示例搜索关键词"""
    return "人工智能"
