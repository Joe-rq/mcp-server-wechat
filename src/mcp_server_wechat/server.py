"""
微信文章 MCP 服务器
"""
from fastmcp import FastMCP

# 导入工具
from .tools.search import search_wechat_articles
from .tools.article import get_wechat_article
from .tools.account import list_wechat_articles_by_account
from .tools.trending import get_trending_wechat_articles

# 创建 FastMCP 实例
mcp = FastMCP(
    name="WeChat Articles MCP Server",
    instructions="""
    微信文章 MCP 服务器提供以下功能:
    
    1. 搜索微信文章 (search_wechat_articles)
    2. 获取文章详情 (get_wechat_article)
    3. 按公众号获取文章列表 (list_wechat_articles_by_account)
    4. 获取热门文章 (get_trending_wechat_articles)
    
    所有工具都支持 JSON 和 Markdown 格式的响应。
    """
)

# 注册工具
mcp.tool(
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True
    }
)(search_wechat_articles)

mcp.tool(
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True
    }
)(get_wechat_article)

mcp.tool(
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True
    }
)(list_wechat_articles_by_account)

mcp.tool(
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True
    }
)(get_trending_wechat_articles)

def main():
    """命令行入口点"""
    # 使用 STDIO 传输协议（默认，用于本地/Claude Desktop）
    mcp.run()

if __name__ == "__main__":
    main()

    # 如需使用 HTTP 传输协议（用于远程访问/多客户端）
    # mcp.run(transport="http", host="127.0.0.1", port=8000)