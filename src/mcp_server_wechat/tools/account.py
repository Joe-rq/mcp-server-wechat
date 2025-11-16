"""
按公众号获取文章列表工具
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field

from ..utils import WechatScraperClient, ResponseFormatter, MCPError

class ListWechatArticlesByAccountInput(BaseModel):
    """按公众号获取文章列表输入模型"""
    model_config = {"extra": "forbid"}
    
    account_name: str = Field(
        description="公众号名称",
        min_length=1,
        examples=["人民日报", "腾讯科技"]
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

async def list_wechat_articles_by_account(input: ListWechatArticlesByAccountInput) -> str:
    """
    按公众号获取文章列表
    
    获取指定微信公众号的最新文章列表。
    
    Args:
        account_name: 公众号名称，例如：'人民日报'、'腾讯科技'
        limit: 返回结果数量限制 (1-50)
        format: 响应格式 - "json" 返回结构化数据，"markdown" 返回可读文本
        detail: "concise" 返回摘要信息，"detailed" 返回完整信息
    
    Returns:
        指定公众号的文章列表，包含标题、摘要、发布时间等信息
    
    Examples:
        list_wechat_articles_by_account(account_name="人民日报", limit=10, format="json")
        list_wechat_articles_by_account(account_name="腾讯科技", format="markdown", detail="detailed")
    
    错误处理:
        - 无效公众号名称: 提供正确的公众号名称
        - 公众号不存在: 确认公众号名称是否正确
        - 访问频率限制: 等待一段时间后重试
        - 网络错误: 检查网络连接
    """
    try:
        async with WechatScraperClient() as client:
            # 调用爬虫客户端获取公众号文章列表
            results = await client.list_articles_by_account(
                account_name=input.account_name,
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
            message=f"获取公众号文章列表时发生未预期的错误: {str(e)}",
            suggestion="请检查公众号名称是否正确，网络连接是否正常，并稍后重试"
        )