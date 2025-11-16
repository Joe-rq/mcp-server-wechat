"""
搜索微信文章工具
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field

from fastmcp import FastMCP
from ..utils import WechatScraperClient, ResponseFormatter, MCPError

class SearchWechatArticlesInput(BaseModel):
    """搜索微信文章输入模型"""
    model_config = {"extra": "forbid"}
    
    query: str = Field(
        description="搜索关键词，例如：'人工智能'、'区块链金融'",
        min_length=1,
        max_length=100,
        examples=["人工智能医疗", "区块链金融应用"]
    )
    
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="返回结果数量限制 (1-50)"
    )
    
    page: int = Field(
        default=1,
        ge=1,
        le=100,
        description="页码，从1开始"
    )
    
    format: Literal["json", "markdown"] = Field(
        default="json",
        description="响应格式：'json' 或 'markdown'"
    )
    
    detail: Literal["concise", "detailed"] = Field(
        default="concise",
        description="详细程度：'concise' 返回摘要信息，'detailed' 返回完整信息"
    )

async def search_wechat_articles(input: SearchWechatArticlesInput) -> str:
    """
    搜索微信文章
    
    使用关键词搜索微信公众号文章，支持分页和格式化选项。
    
    Args:
        query: 搜索关键词，例如：'人工智能'、'区块链金融'
        limit: 返回结果数量限制 (1-50)
        page: 页码，从1开始
        format: 响应格式 - "json" 返回结构化数据，"markdown" 返回可读文本
        detail: "concise" 返回摘要信息，"detailed" 返回完整信息
    
    Returns:
        格式化的文章列表，包含标题、摘要、作者、发布时间等信息
    
    Examples:
        search_wechat_articles(query="人工智能医疗", limit=10, page=1, format="json", detail="concise")
        search_wechat_articles(query="区块链金融", format="markdown", detail="detailed")
    
    错误处理:
        - 无效查询: 提供非空搜索词
        - 结果过多: 缩小查询范围或减少limit
        - 访问频率限制: 等待一段时间后重试
        - 网络错误: 检查网络连接
    """
    try:
        async with WechatScraperClient() as client:
            # 调用爬虫客户端搜索文章
            results = await client.search_articles(
                query=input.query,
                page_num=input.page,
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
            message=f"搜索文章时发生未预期的错误: {str(e)}",
            suggestion="请检查网络连接并稍后重试，或报告此问题"
        )