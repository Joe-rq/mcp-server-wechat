"""
获取热门微信文章工具
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field

from ..utils import WechatScraperClient, ResponseFormatter, MCPError

class GetTrendingWechatArticlesInput(BaseModel):
    """获取热门微信文章输入模型"""
    model_config = {"extra": "forbid"}
    
    category: Literal["hot", "tech", "finance", "entertainment"] = Field(
        default="hot",
        description="文章分类：'hot'(热门)、'tech'(科技)、'finance'(财经)、'entertainment'(娱乐)"
    )
    
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="返回结果数量限制 (1-50)"
    )
    
    format: Literal["json", "markdown"] = Field(
        default="json",
        description="响应格式：'json' 或 'markdown'"
    )
    
    detail: Literal["concise", "detailed"] = Field(
        default="concise",
        description="详细程度：'concise' 返回摘要信息，'detailed' 返回完整信息"
    )

async def get_trending_wechat_articles(input: GetTrendingWechatArticlesInput) -> str:
    """
    获取热门微信文章
    
    获取当前热门或特定分类的微信文章列表。
    
    Args:
        category: 文章分类 - "hot"(热门)、"tech"(科技)、"finance"(财经)、"entertainment"(娱乐)
        limit: 返回结果数量限制 (1-50)
        format: 响应格式 - "json" 返回结构化数据，"markdown" 返回可读文本
        detail: "concise" 返回摘要信息，"detailed" 返回完整信息
    
    Returns:
        热门文章列表，包含标题、摘要、作者、发布时间等信息
    
    Examples:
        get_trending_wechat_articles(category="hot", limit=10, format="json")
        get_trending_wechat_articles(category="tech", format="markdown", detail="detailed")
    
    错误处理:
        - 无效分类: 使用支持的分类值
        - 访问频率限制: 等待一段时间后重试
        - 网络错误: 检查网络连接
    """
    try:
        async with WechatScraperClient() as client:
            # 调用爬虫客户端获取热门文章
            results = await client.get_trending_articles(
                category=input.category,
                limit=input.limit
            )
            
            # 格式化响应
            response = ResponseFormatter.format_response(
                data=results,
                format=input.format,
                detail=input.detail
            )
            
            return response
            
    except MCPError:
        # MCPError 已经包含可操作的建议，直接抛出
        raise
    except Exception as e:
        # 其他异常转换为 MCPError
        raise MCPError(
            message=f"获取热门文章时发生未预期的错误: {str(e)}",
            suggestion="请检查网络连接是否正常，并稍后重试"
        )