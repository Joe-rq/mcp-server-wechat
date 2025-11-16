"""
获取微信文章详情工具
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field

from ..utils import WechatScraperClient, ResponseFormatter, MCPError

class GetWechatArticleInput(BaseModel):
    """获取微信文章详情输入模型"""
    model_config = {"extra": "forbid"}
    
    article_id: str = Field(
        description="文章ID或URL",
        min_length=1,
        examples=["https://mp.weixin.qq.com/s?__biz=MzIwMzA5NTI3NQ==&mid=2649914567"]
    )
    
    include_content: bool = Field(
        default=True,
        description="是否包含文章正文内容"
    )
    
    format: Literal["json", "markdown"] = Field(
        default="json",
        description="响应格式：'json' 或 'markdown'"
    )

async def get_wechat_article(input: GetWechatArticleInput) -> str:
    """
    获取微信文章详情
    
    获取指定微信文章的详细信息，包括标题、作者、发布时间、正文内容等。
    
    Args:
        article_id: 文章ID或完整URL
        include_content: 是否包含文章正文内容
        format: 响应格式 - "json" 返回结构化数据，"markdown" 返回可读文本
    
    Returns:
        文章详细信息，包括标题、作者、发布时间、正文内容等
    
    Examples:
        get_wechat_article(article_id="https://mp.weixin.qq.com/s?__biz=MzIwMzA5NTI3NQ==&mid=2649914567")
        get_wechat_article(article_id="MzIwMzA5NTI3NQ==", include_content=False, format="markdown")
    
    错误处理:
        - 无效文章ID: 提供有效的文章ID或URL
        - 文章不存在: 确认文章ID是否正确
        - 访问频率限制: 等待一段时间后重试
        - 网络错误: 检查网络连接
    """
    try:
        async with WechatScraperClient() as client:
            # 调用爬虫客户端获取文章详情
            article = await client.get_article_details(
                article_id=input.article_id,
                include_content=input.include_content
            )
            
            # 格式化响应
            response = ResponseFormatter.format_response(
                data=article,
                format=input.format,
                detail="detailed"  # 文章详情始终使用详细模式
            )
            
            return response
            
    except MCPError:
        # MCPError 已经包含可操作的建议，直接抛出
        raise
    except Exception as e:
        # 其他异常转换为 MCPError
        raise MCPError(
            message=f"获取文章详情时发生未预期的错误: {str(e)}",
            suggestion="请检查文章ID是否正确，网络连接是否正常，并稍后重试"
        )