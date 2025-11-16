#!/usr/bin/env python
"""
示例：搜索微信文章

这个示例展示如何使用 mcp-server-wechat 搜索微信文章。
"""
import asyncio
import sys
sys.path.insert(0, 'src')

from mcp_server_wechat.tools.search import search_wechat_articles, SearchWechatArticlesInput


async def main():
    """搜索文章示例"""

    # 搜索关键词
    query = "Claude AI"

    print(f"正在搜索: {query}")
    print("-" * 80)

    # 创建输入参数
    input_data = SearchWechatArticlesInput(
        query=query,
        limit=5,              # 返回 5 条结果
        page=1,               # 第一页
        format="markdown",    # 使用 Markdown 格式输出
        detail="concise"      # 简洁模式
    )

    # 调用工具搜索文章
    result = await search_wechat_articles(input_data)

    print(result)
    print("-" * 80)
    print("✓ 搜索成功！")


if __name__ == "__main__":
    asyncio.run(main())
