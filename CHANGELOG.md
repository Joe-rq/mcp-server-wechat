# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-16

### Added
- 初始版本发布
- 实现基于 Playwright 的微信文章爬虫
- 实现 4 个 MCP 工具：
  - `search_wechat_articles`: 搜索微信文章
  - `get_wechat_article`: 获取文章详情
  - `list_wechat_articles_by_account`: 按公众号获取文章列表
  - `get_trending_wechat_articles`: 获取热门文章
- 支持 JSON 和 Markdown 两种输出格式
- 完整的错误处理和建议机制
- 命令行入口点 `mcp-server-wechat`

### Fixed
- 修复 `wechat_client.py:323` 中的 `hrefs` 拼写错误
- 修复包安装问题，添加正确的 `pyproject.toml` 配置
- 统一 Python 版本要求为 3.10+

### Documentation
- 添加完整的 README.md
- 添加 LICENSE 文件
- 添加使用示例
