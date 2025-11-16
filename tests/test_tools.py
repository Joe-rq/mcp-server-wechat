"""
测试工具函数的基本功能

注意：这些是示例测试，实际运行会访问真实的微信网站。
在 CI/CD 环境中，应该使用 mock 来避免真实网络请求。
"""
import pytest
from mcp_server_wechat.tools.search import SearchWechatArticlesInput
from mcp_server_wechat.tools.article import GetWechatArticleInput


def test_search_input_validation():
    """测试搜索输入参数验证"""
    # 正常输入
    input_data = SearchWechatArticlesInput(
        query="测试",
        limit=10,
        page=1,
        format="json",
        detail="concise"
    )
    assert input_data.query == "测试"
    assert input_data.limit == 10
    assert input_data.page == 1

    # 测试默认值
    input_data2 = SearchWechatArticlesInput(query="测试")
    assert input_data2.limit == 10
    assert input_data2.page == 1
    assert input_data2.format == "json"

    # 测试参数边界
    with pytest.raises(Exception):
        # 空查询应该失败
        SearchWechatArticlesInput(query="")

    with pytest.raises(Exception):
        # limit 超出范围应该失败
        SearchWechatArticlesInput(query="测试", limit=100)


def test_article_input_validation():
    """测试文章输入参数验证"""
    # 正常输入
    input_data = GetWechatArticleInput(
        article_id="https://mp.weixin.qq.com/s/test123",
        include_content=True,
        format="markdown"
    )
    assert input_data.article_id == "https://mp.weixin.qq.com/s/test123"
    assert input_data.include_content is True

    # 测试默认值
    input_data2 = GetWechatArticleInput(article_id="test_id")
    assert input_data2.include_content is True
    assert input_data2.format == "json"

    # 测试参数边界
    with pytest.raises(Exception):
        # 空 article_id 应该失败
        GetWechatArticleInput(article_id="")


# 以下是集成测试示例（需要网络，默认跳过）

@pytest.mark.skip(reason="需要真实网络访问，仅在手动测试时运行")
@pytest.mark.asyncio
async def test_search_articles_integration(sample_search_query):
    """集成测试：搜索文章"""
    from mcp_server_wechat.tools.search import search_wechat_articles

    input_data = SearchWechatArticlesInput(
        query=sample_search_query,
        limit=5,
        format="json"
    )

    result = await search_wechat_articles(input_data)
    assert result is not None
    assert len(result) > 0


@pytest.mark.skip(reason="需要真实网络访问，仅在手动测试时运行")
@pytest.mark.asyncio
async def test_get_article_integration(sample_article_url):
    """集成测试：获取文章详情"""
    from mcp_server_wechat.tools.article import get_wechat_article

    input_data = GetWechatArticleInput(
        article_id=sample_article_url,
        include_content=True,
        format="markdown"
    )

    result = await get_wechat_article(input_data)
    assert result is not None
    assert "Claude Skills" in result  # 检查文章标题是否存在
