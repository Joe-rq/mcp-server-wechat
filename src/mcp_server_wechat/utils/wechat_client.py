"""
微信文章爬虫客户端
"""
import os
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from urllib.parse import quote

from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup

from .errors import MCPError, handle_scraper_error

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("wechat_client")

# 环境变量配置
DEFAULT_TIMEOUT = int(os.getenv("WECHAT_SCRAPER_TIMEOUT", "30000"))  # 毫秒
DEFAULT_RETRY_COUNT = int(os.getenv("WECHAT_SCRAPER_RETRY_COUNT", "3"))
HEADLESS_MODE = os.getenv("WECHAT_SCRAPER_HEADLESS", "true").lower() == "true"

class WechatScraperClient:
    """微信文章爬虫客户端"""
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.timeout = DEFAULT_TIMEOUT
        self.retry_count = DEFAULT_RETRY_COUNT
        self.headless = HEADLESS_MODE
        
    async def __aenter__(self):
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def initialize(self):
        """初始化浏览器"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise MCPError(
                message=f"浏览器初始化失败: {str(e)}",
                suggestion="请检查 Playwright 是否正确安装，可尝试运行 'playwright install chromium'"
            )
    
    async def close(self):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        logger.info("浏览器已关闭")
    
    async def search_articles(self, query: str, page_num: int = 1, limit: int = 10) -> Dict[str, Any]:
        """
        搜索微信文章
        
        Args:
            query: 搜索关键词
            page_num: 页码，从1开始
            limit: 每页结果数量
            
        Returns:
            包含文章列表和分页信息的字典
        """
        try:
            # 创建新页面
            page = await self.context.new_page()
            
            # 构建搜索URL
            encoded_query = quote(query)
            search_url = f"https://weixin.sogou.com/weixin?type=2&query={encoded_query}&page={page_num}"
            
            # 访问搜索页面
            await page.goto(search_url, timeout=self.timeout)
            logger.info(f"访问搜索页面: {search_url}")
            
            # 等待搜索结果加载
            await page.wait_for_selector(".news-box", timeout=self.timeout)
            
            # 获取页面内容
            content = await page.content()
            
            # 解析搜索结果
            soup = BeautifulSoup(content, 'lxml')
            articles = []
            
            # 提取文章列表
            article_elements = soup.select(".news-list li")
            
            for article in article_elements[:limit]:
                try:
                    # 提取文章信息
                    title_element = article.select_one("h3 a")
                    title = title_element.text.strip() if title_element else "无标题"
                    
                    # 提取文章链接
                    article_url = title_element.get("href", "") if title_element else ""
                    if article_url and not article_url.startswith("http"):
                        article_url = f"https://weixin.sogou.com{article_url}"
                    
                    # 提取文章ID
                    article_id = article_url.split("url=")[-1] if "url=" in article_url else ""
                    
                    # 提取摘要
                    summary_element = article.select_one(".txt-info")
                    summary = summary_element.text.strip() if summary_element else "无摘要"
                    
                    # 提取公众号名称
                    account_element = article.select_one("div.txt-box > div > span.all-time-y2")
                    account_name = account_element.text.strip() if account_element else "未知公众号"
                    
                    # 提取发布时间
                    time_element = article.select_one(".s2")
                    publish_time = time_element.text.strip() if time_element else "未知时间"
                    
                    articles.append({
                        "article_id": article_id,
                        "title": title,
                        "summary": summary,
                        "url": article_url,
                        "account_name": account_name,
                        "publish_time": publish_time
                    })
                except Exception as e:
                    logger.warning(f"解析文章时出错: {str(e)}")
            
            # 提取分页信息
            total_pages = 1
            try:
                page_info = soup.select_one("#pagebar_container")
                if page_info:
                    page_links = page_info.select("a")
                    if page_links:
                        # 尝试从分页链接获取最大页码
                        page_numbers = [int(a.text) for a in page_links if a.text.isdigit()]
                        if page_numbers:
                            total_pages = max(page_numbers)
            except Exception as e:
                logger.warning(f"解析分页信息时出错: {str(e)}")
            
            # 关闭页面
            await page.close()
            
            return {
                "articles": articles,
                "pagination": {
                    "current_page": page_num,
                    "total_pages": total_pages,
                    "total_results": len(articles),
                    "has_more": page_num < total_pages
                },
                "query": query
            }
            
        except Exception as e:
            logger.error(f"搜索文章时出错: {str(e)}")
            raise handle_scraper_error(e)
    
    async def get_article_details(self, article_id: str, include_content: bool = True) -> Dict[str, Any]:
        """
        获取微信文章详情
        
        Args:
            article_id: 文章ID或URL
            include_content: 是否包含文章内容
            
        Returns:
            文章详情字典
        """
        try:
            # 创建新页面
            page = await self.context.new_page()
            
            # 构建文章URL
            article_url = article_id if article_id.startswith("http") else f"https://mp.weixin.qq.com/s?__biz={article_id}"
            
            # 访问文章页面
            await page.goto(article_url, timeout=self.timeout)
            logger.info(f"访问文章页面: {article_url}")
            
            # 等待文章内容加载
            await page.wait_for_selector("#activity-name", timeout=self.timeout)
            
            # 获取页面内容
            content = await page.content()
            
            # 解析文章详情
            soup = BeautifulSoup(content, 'lxml')
            
            # 提取标题
            title_element = soup.select_one("#activity-name")
            title = title_element.text.strip() if title_element else "无标题"
            
            # 提取作者和公众号
            account_element = soup.select_one("#js_name")
            account_name = account_element.text.strip() if account_element else "未知公众号"
            
            # 提取发布时间
            time_element = soup.select_one("#publish_time")
            publish_time = time_element.text.strip() if time_element else "未知时间"
            
            # 提取文章内容
            article_content = ""
            if include_content:
                content_element = soup.select_one("#js_content")
                if content_element:
                    # 清理内容中的样式
                    for tag in content_element.select("[style]"):
                        del tag["style"]
                    article_content = content_element.get_text(separator="\n").strip()
            
            # 提取阅读量和点赞数
            read_count = "未知"
            like_count = "未知"
            
            # 关闭页面
            await page.close()
            
            return {
                "article_id": article_id,
                "title": title,
                "account_name": account_name,
                "publish_time": publish_time,
                "content": article_content if include_content else None,
                "url": article_url,
                "stats": {
                    "read_count": read_count,
                    "like_count": like_count
                }
            }
            
        except Exception as e:
            logger.error(f"获取文章详情时出错: {str(e)}")
            raise handle_scraper_error(e)
    
    async def list_articles_by_account(self, account_name: str, limit: int = 10) -> Dict[str, Any]:
        """
        获取指定公众号的文章列表
        
        Args:
            account_name: 公众号名称
            limit: 返回的文章数量
            
        Returns:
            包含文章列表的字典
        """
        try:
            # 创建新页面
            page = await self.context.new_page()
            
            # 构建搜索URL
            encoded_account = quote(account_name)
            search_url = f"https://weixin.sogou.com/weixin?type=1&query={encoded_account}"
            
            # 访问搜索页面
            await page.goto(search_url, timeout=self.timeout)
            logger.info(f"访问公众号搜索页面: {search_url}")
            
            # 等待搜索结果加载
            await page.wait_for_selector(".news-box", timeout=self.timeout)
            
            # 获取页面内容
            content = await page.content()
            
            # 解析搜索结果
            soup = BeautifulSoup(content, 'lxml')
            
            # 查找公众号
            account_element = soup.select_one(".news-list2 li")
            if not account_element:
                await page.close()
                return {
                    "account_name": account_name,
                    "articles": [],
                    "total_results": 0
                }
            
            # 点击进入公众号
            account_link = account_element.select_one("a")
            if account_link and account_link.get("href"):
                account_url = account_link.get("href")
                if not account_url.startswith("http"):
                    account_url = f"https://weixin.sogou.com{account_url}"
                
                # 访问公众号页面
                await page.goto(account_url, timeout=self.timeout)
                logger.info(f"访问公众号页面: {account_url}")
                
                # 等待文章列表加载
                await page.wait_for_selector(".weui_media_box", timeout=self.timeout)
                
                # 获取页面内容
                content = await page.content()
                
                # 解析文章列表
                soup = BeautifulSoup(content, 'lxml')
                articles = []
                
                # 提取文章列表
                article_elements = soup.select(".weui_media_box")
                
                for article in article_elements[:limit]:
                    try:
                        # 提取文章信息
                        title_element = article.select_one("h4.weui_media_title")
                        title = title_element.text.strip() if title_element else "无标题"
                        
                        # 提取文章链接
                        article_url = title_element.get("href", "") if title_element else ""
                        
                        # 提取文章ID
                        article_id = article_url.split("?__biz=")[-1] if "?__biz=" in article_url else ""
                        
                        # 提取摘要
                        summary_element = article.select_one(".weui_media_desc")
                        summary = summary_element.text.strip() if summary_element else "无摘要"
                        
                        # 提取发布时间
                        time_element = article.select_one(".weui_media_extra_info")
                        publish_time = time_element.text.strip() if time_element else "未知时间"
                        
                        articles.append({
                            "article_id": article_id,
                            "title": title,
                            "summary": summary,
                            "url": article_url,
                            "publish_time": publish_time
                        })
                    except Exception as e:
                        logger.warning(f"解析文章时出错: {str(e)}")
                
                # 关闭页面
                await page.close()
                
                return {
                    "account_name": account_name,
                    "articles": articles,
                    "total_results": len(articles)
                }
            
            # 关闭页面
            await page.close()
            
            return {
                "account_name": account_name,
                "articles": [],
                "total_results": 0,
                "error": "未找到公众号或无法访问公众号页面"
            }
            
        except Exception as e:
            logger.error(f"获取公众号文章列表时出错: {str(e)}")
            raise handle_scraper_error(e)
    
    async def get_trending_articles(self, category: str = "hot", limit: int = 10) -> Dict[str, Any]:
        """
        获取热门微信文章
        
        Args:
            category: 分类，可选值: hot(热门)、tech(科技)、finance(财经)、entertainment(娱乐)
            limit: 返回的文章数量
            
        Returns:
            包含热门文章列表的字典
        """
        try:
            # 创建新页面
            page = await self.context.new_page()
            
            # 映射分类到URL
            category_urls = {
                "hot": "https://weixin.sogou.com/",
                "tech": "https://weixin.sogou.com/pcindex/pc/pc_1/1.html",
                "finance": "https://weixin.sogou.com/pcindex/pc/pc_2/1.html",
                "entertainment": "https://weixin.sogou.com/pcindex/pc/pc_4/1.html"
            }
            
            # 获取对应分类的URL
            url = category_urls.get(category, category_urls["hot"])
            
            # 访问页面
            await page.goto(url, timeout=self.timeout)
            logger.info(f"访问热门文章页面: {url}")
            
            # 等待文章列表加载
            await page.wait_for_selector(".news-list", timeout=self.timeout)
            
            # 获取页面内容
            content = await page.content()
            
            # 解析文章列表
            soup = BeautifulSoup(content, 'lxml')
            articles = []
            
            # 提取文章列表
            article_elements = soup.select(".news-list li")
            
            for article in article_elements[:limit]:
                try:
                    # 提取文章信息
                    title_element = article.select_one("h3 a")
                    title = title_element.text.strip() if title_element else "无标题"
                    
                    # 提取文章链接
                    article_url = title_element.get("href", "") if title_element else ""
                    if article_url and not article_url.startswith("http"):
                        article_url = f"https://weixin.sogou.com{article_url}"
                    
                    # 提取文章ID
                    article_id = article_url.split("url=")[-1] if "url=" in article_url else ""
                    
                    # 提取摘要
                    summary_element = article.select_one(".txt-info")
                    summary = summary_element.text.strip() if summary_element else "无摘要"
                    
                    # 提取公众号名称
                    account_element = article.select_one("div.txt-box > div > span.all-time-y2")
                    account_name = account_element.text.strip() if account_element else "未知公众号"
                    
                    # 提取发布时间
                    time_element = article.select_one(".s2")
                    publish_time = time_element.text.strip() if time_element else "未知时间"
                    
                    articles.append({
                        "article_id": article_id,
                        "title": title,
                        "summary": summary,
                        "url": article_url,
                        "account_name": account_name,
                        "publish_time": publish_time
                    })
                except Exception as e:
                    logger.warning(f"解析文章时出错: {str(e)}")
            
            # 关闭页面
            await page.close()
            
            return {
                "category": category,
                "articles": articles,
                "total_results": len(articles)
            }
            
        except Exception as e:
            logger.error(f"获取热门文章时出错: {str(e)}")
            raise handle_scraper_error(e)