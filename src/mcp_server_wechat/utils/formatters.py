"""
响应格式化模块
"""
import json
from typing import Any, Dict, List, Literal, Optional

# 字符限制（约25k tokens）
CHARACTER_LIMIT = 25000 * 4

class ResponseFormatter:
    """响应格式化器"""
    
    @staticmethod
    def format_response(
        data: Any,
        format: Literal["json", "markdown"] = "json",
        detail: Literal["concise", "detailed"] = "concise"
    ) -> str:
        """
        格式化响应数据
        
        Args:
            data: 要格式化的数据
            format: 输出格式（json 或 markdown）
            detail: 详细级别（concise 或 detailed）
            
        Returns:
            格式化后的字符串
        """
        if format == "json":
            if detail == "concise":
                # 返回精简的 JSON
                result = json.dumps(ResponseFormatter._extract_concise_data(data), indent=2, ensure_ascii=False)
            else:
                # 返回完整的 JSON
                result = json.dumps(data, indent=2, ensure_ascii=False)
        else:  # markdown
            if detail == "concise":
                result = ResponseFormatter._format_markdown_concise(data)
            else:
                result = ResponseFormatter._format_markdown_detailed(data)
        
        # 检查字符限制
        if len(result) > CHARACTER_LIMIT:
            result = ResponseFormatter._truncate_response(result, CHARACTER_LIMIT)
        
        return result
    
    @staticmethod
    def _truncate_response(text: str, max_chars: int) -> str:
        """截断过长的响应"""
        truncated = text[:max_chars]
        return f"""{truncated}

... [Response truncated due to length]

To get complete info:
1. Use more specific filters
2. Request smaller batches
3. Use 'concise' detail level"""
    
    @staticmethod
    def _extract_concise_data(data: Any) -> Any:
        """提取精简数据"""
        if isinstance(data, dict):
            # 处理文章列表
            if "articles" in data:
                concise_data = {
                    "articles": [],
                    "total_results": data.get("total_results", len(data.get("articles", []))),
                }
                
                # 复制分页信息（如果存在）
                if "pagination" in data:
                    concise_data["pagination"] = data["pagination"]
                
                # 复制查询信息（如果存在）
                if "query" in data:
                    concise_data["query"] = data["query"]
                
                # 复制分类信息（如果存在）
                if "category" in data:
                    concise_data["category"] = data["category"]
                
                # 复制公众号信息（如果存在）
                if "account_name" in data:
                    concise_data["account_name"] = data["account_name"]
                
                # 精简文章列表
                for article in data.get("articles", []):
                    concise_article = {
                        "title": article.get("title", "无标题"),
                        "article_id": article.get("article_id", ""),
                        "account_name": article.get("account_name", "未知公众号"),
                        "publish_time": article.get("publish_time", "未知时间"),
                    }
                    
                    # 添加摘要（如果存在）
                    if "summary" in article:
                        concise_article["summary"] = article["summary"]
                    
                    concise_data["articles"].append(concise_article)
                
                return concise_data
            
            # 处理单篇文章
            elif "title" in data and "article_id" in data:
                concise_article = {
                    "title": data.get("title", "无标题"),
                    "article_id": data.get("article_id", ""),
                    "account_name": data.get("account_name", "未知公众号"),
                    "publish_time": data.get("publish_time", "未知时间"),
                }
                
                # 添加摘要（如果存在）
                if "summary" in data:
                    concise_article["summary"] = data["summary"]
                
                # 添加内容摘要（如果存在）
                if "content" in data and data["content"]:
                    content = data["content"]
                    concise_article["content_preview"] = content[:200] + "..." if len(content) > 200 else content
                
                return concise_article
            
            # 其他情况，返回原始数据
            return data
        
        # 非字典类型，返回原始数据
        return data
    
    @staticmethod
    def _format_markdown_concise(data: Any) -> str:
        """格式化为精简 Markdown"""
        if not isinstance(data, dict):
            return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        
        result = []
        
        # 处理文章列表
        if "articles" in data:
            # 添加标题
            if "query" in data:
                result.append(f"# 搜索结果: {data['query']}")
            elif "account_name" in data:
                result.append(f"# {data['account_name']} 的文章")
            elif "category" in data:
                category_names = {
                    "hot": "热门",
                    "tech": "科技",
                    "finance": "财经",
                    "entertainment": "娱乐"
                }
                category_display = category_names.get(data["category"], data["category"])
                result.append(f"# {category_display}文章")
            else:
                result.append("# 文章列表")
            
            # 添加分页信息
            if "pagination" in data:
                pagination = data["pagination"]
                result.append(f"\n**页码**: {pagination.get('current_page', 1)}/{pagination.get('total_pages', 1)} | "
                             f"**结果数**: {pagination.get('total_results', 0)}")
            
            # 添加文章列表
            result.append("\n## 文章\n")
            
            for i, article in enumerate(data.get("articles", []), 1):
                result.append(f"### {i}. {article.get('title', '无标题')}")
                result.append(f"**公众号**: {article.get('account_name', '未知公众号')} | "
                             f"**发布时间**: {article.get('publish_time', '未知时间')}")
                
                if "summary" in article:
                    result.append(f"\n{article['summary']}\n")
                
                result.append("---\n")
            
            # 添加结果统计
            result.append(f"\n共 {len(data.get('articles', []))} 篇文章")
        
        # 处理单篇文章
        elif "title" in data and "article_id" in data:
            result.append(f"# {data.get('title', '无标题')}")
            result.append(f"**公众号**: {data.get('account_name', '未知公众号')} | "
                         f"**发布时间**: {data.get('publish_time', '未知时间')}")
            
            if "summary" in data:
                result.append(f"\n> {data['summary']}\n")
            
            if "content" in data and data["content"]:
                content = data["content"]
                preview = content[:300] + "..." if len(content) > 300 else content
                result.append(f"\n## 内容预览\n\n{preview}\n")
        
        # 其他情况
        else:
            return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        
        return "\n".join(result)
    
    @staticmethod
    def _format_markdown_detailed(data: Any) -> str:
        """格式化为详细 Markdown"""
        if not isinstance(data, dict):
            return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        
        result = []
        
        # 处理文章列表
        if "articles" in data:
            # 添加标题
            if "query" in data:
                result.append(f"# 搜索结果: {data['query']}")
            elif "account_name" in data:
                result.append(f"# {data['account_name']} 的文章")
            elif "category" in data:
                category_names = {
                    "hot": "热门",
                    "tech": "科技",
                    "finance": "财经",
                    "entertainment": "娱乐"
                }
                category_display = category_names.get(data["category"], data["category"])
                result.append(f"# {category_display}文章")
            else:
                result.append("# 文章列表")
            
            # 添加分页信息
            if "pagination" in data:
                pagination = data["pagination"]
                result.append(f"\n**页码**: {pagination.get('current_page', 1)}/{pagination.get('total_pages', 1)} | "
                             f"**结果数**: {pagination.get('total_results', 0)}")
            
            # 添加文章列表
            result.append("\n## 文章\n")
            
            for i, article in enumerate(data.get("articles", []), 1):
                result.append(f"### {i}. {article.get('title', '无标题')}")
                result.append(f"**公众号**: {article.get('account_name', '未知公众号')} | "
                             f"**发布时间**: {article.get('publish_time', '未知时间')}")
                
                if "url" in article:
                    result.append(f"\n**链接**: {article['url']}")
                
                if "article_id" in article:
                    result.append(f"\n**文章ID**: {article['article_id']}")
                
                if "summary" in article:
                    result.append(f"\n**摘要**:\n> {article['summary']}\n")
                
                result.append("---\n")
            
            # 添加结果统计
            result.append(f"\n共 {len(data.get('articles', []))} 篇文章")
        
        # 处理单篇文章
        elif "title" in data and "article_id" in data:
            result.append(f"# {data.get('title', '无标题')}")
            result.append(f"**公众号**: {data.get('account_name', '未知公众号')} | "
                         f"**发布时间**: {data.get('publish_time', '未知时间')}")
            
            if "url" in data:
                result.append(f"\n**链接**: {data['url']}")
            
            if "article_id" in data:
                result.append(f"\n**文章ID**: {data['article_id']}")
            
            if "summary" in data:
                result.append(f"\n**摘要**:\n> {data['summary']}\n")
            
            if "stats" in data:
                stats = data["stats"]
                result.append(f"\n**阅读量**: {stats.get('read_count', '未知')} | "
                             f"**点赞数**: {stats.get('like_count', '未知')}")
            
            if "content" in data and data["content"]:
                result.append(f"\n## 内容\n\n{data['content']}\n")
        
        # 其他情况
        else:
            return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        
        return "\n".join(result)