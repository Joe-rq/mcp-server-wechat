"""
错误处理模块
"""
from typing import Dict, Any, Optional
import httpx
from playwright.async_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError

class MCPError(Exception):
    """MCP 错误基类"""
    
    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion or "请稍后重试"
        super().__init__(f"{message}. {suggestion}" if suggestion else message)


def handle_scraper_error(error: Exception) -> MCPError:
    """
    处理爬虫错误并转换为 MCPError
    
    Args:
        error: 原始异常
        
    Returns:
        MCPError: 格式化的 MCP 错误
    """
    if isinstance(error, PlaywrightTimeoutError):
        return MCPError(
            message="请求超时，可能是网络问题或目标网站响应慢",
            suggestion="请检查网络连接并稍后重试，或增加超时时间 (WECHAT_SCRAPER_TIMEOUT 环境变量)"
        )
    elif isinstance(error, PlaywrightError):
        if "ERR_CONNECTION_REFUSED" in str(error):
            return MCPError(
                message="连接被拒绝，无法访问目标网站",
                suggestion="请检查网络连接或目标网站是否可访问"
            )
        elif "ERR_NAME_NOT_RESOLVED" in str(error):
            return MCPError(
                message="无法解析域名",
                suggestion="请检查网络连接和DNS设置"
            )
        elif "net::ERR_PROXY_CONNECTION_FAILED" in str(error):
            return MCPError(
                message="代理连接失败",
                suggestion="请检查代理设置或尝试不使用代理"
            )
        else:
            return MCPError(
                message=f"浏览器错误: {str(error)}",
                suggestion="请检查 Playwright 是否正确安装，可尝试运行 'playwright install chromium'"
            )
    elif isinstance(error, httpx.HTTPError):
        return MCPError(
            message=f"HTTP 请求错误: {str(error)}",
            suggestion="请检查网络连接并稍后重试"
        )
    elif "访问频率受限" in str(error) or "请输入验证码" in str(error):
        return MCPError(
            message="访问频率受限，可能触发了反爬虫机制",
            suggestion="请降低请求频率，稍后再试，或考虑使用代理"
        )
    else:
        return MCPError(
            message=f"未知错误: {str(error)}",
            suggestion="请检查日志获取详细信息并报告此问题"
        )