#!/usr/bin/env python
"""
示例：获取微信文章详情

这个示例展示如何使用 mcp-server-wechat 获取指定微信文章的详细信息。
"""
import asyncio
import sys
sys.path.insert(0, 'src')

from mcp_server_wechat.tools.article import get_wechat_article, GetWechatArticleInput


async def main():
    """获取文章详情示例"""

    # 示例文章 URL
    article_url = "https://mp.weixin.qq.com/s/UjZAqvkfk8AzpOoK1KV0yw"

    print(f"正在获取文章: {article_url}")
    print("-" * 80)

    # 创建输入参数
    input_data = GetWechatArticleInput(
        article_id=article_url,
        include_content=True,  # 包含正文内容
        format="markdown"       # 使用 Markdown 格式输出
    )

    # 调用工具获取文章
    result = await get_wechat_article(input_data)

    print(result)
    print("-" * 80)
    print("✓ 获取成功！")


if __name__ == "__main__":
    asyncio.run(main())
