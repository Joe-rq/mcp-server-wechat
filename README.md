# 微信文章 MCP 服务器

基于 FastMCP 框架的微信文章搜索和分析服务器，使用 Playwright + Python 爬虫方案。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 功能特点

- 🔍 搜索微信文章
- 📄 获取文章详情
- 📚 按公众号获取文章列表
- 🔥 获取热门文章
- 📝 支持 JSON 和 Markdown 格式响应
- ⚠️ 完整的错误处理和可操作建议

## 快速开始

### 前置条件

- Python 3.10+
- pip 或 uv

### 安装步骤

#### 使用 uv（推荐 - 现代化、快速）

```bash
# 1. 克隆或进入项目目录
cd mcp-server-wechat

# 2. 创建虚拟环境并安装依赖（一步到位）
uv venv
uv pip install -e .

# 3. 安装 Playwright 浏览器
uv run playwright install chromium

# 4. 直接运行（无需激活虚拟环境）
uv run mcp-server-wechat
```

#### 传统 pip 方式

```bash
# 1. 克隆或进入项目目录
cd mcp-server-wechat

# 2. 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -e .

# 4. 安装 Playwright 浏览器
playwright install chromium
```

## 使用方法

### 方式 1: 命令行脚本（推荐）

#### 使用 uv 运行（最简洁）

```bash
# 无需激活虚拟环境，直接运行
uv run mcp-server-wechat
```

#### 传统方式

安装后会自动创建 `mcp-server-wechat` 命令：

```bash
# 直接运行服务器（需激活虚拟环境）
mcp-server-wechat

# 或使用 Python 模块方式
PYTHONPATH=src python -m mcp_server_wechat.server
```

### 方式 2: 使用 fastmcp dev 调试

#### 使用 uv 运行

```bash
# 无需设置 PYTHONPATH，直接调试
uv run fastmcp dev src/mcp_server_wechat/server.py:mcp
```

#### 传统方式

```bash
# 需要设置 PYTHONPATH
PYTHONPATH=src fastmcp dev src/mcp_server_wechat/server.py:mcp
```

然后访问 MCP Inspector 来测试工具。

### 方式 3: 集成到 Claude Desktop

#### 使用 uv（最推荐,自动管理虚拟环境）

**无需任何预处理，直接配置**：

```json
{
  "mcpServers": {
    "wechat-articles": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/你的用户名/path/to/mcp-server-wechat",
        "run",
        "mcp-server-wechat"
      ]
    }
  }
}
```

**优点**:
- ✅ 无需手动创建虚拟环境
- ✅ 无需激活环境
- ✅ 自动处理依赖隔离
- ✅ 路径问题最少

#### 使用虚拟环境 Python（次选）

如果你已经创建了虚拟环境:

```json
{
  "mcpServers": {
    "wechat-articles": {
      "command": "/Users/你的用户名/path/to/mcp-server-wechat/.venv/bin/python",
      "args": ["-m", "mcp_server_wechat.server"]
    }
  }
}
```

**重要**: 使用**虚拟环境内的 Python 绝对路径**,而不是系统的 `python` 或 `python3`

⚠️ **注意**: 这种方式需要手动维护虚拟环境，**不如 uv 方便**

#### 全局安装（⚠️ 强烈不推荐）

**仅用于测试，生产环境千万别用！**

```bash
# macOS/Linux 使用 python3 而不是 python
pip3 install -e .
```

配置文件:
```json
{
  "mcpServers": {
    "wechat-articles": {
      "command": "python3",
      "args": ["-m", "mcp_server_wechat.server"]
    }
  }
}
```

**问题**:
- ❌ 污染系统环境
- ❌ 依赖冲突风险高
- ❌ 权限问题多
- ❌ 路径问题频发

**建议**: **用uv！用uv！用uv！**

### 方式 4: 作为 Python 库使用

查看 `examples/` 目录下的示例代码：

```bash
# 获取文章详情
PYTHONPATH=src python examples/get_article.py

# 搜索文章
PYTHONPATH=src python examples/search_articles.py
```

## 环境变量配置

可以通过环境变量自定义爬虫行为：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `WECHAT_SCRAPER_TIMEOUT` | 爬虫超时时间（**毫秒**） | `30000`（30秒） |
| `WECHAT_SCRAPER_RETRY_COUNT` | 重试次数 | `3` |
| `WECHAT_SCRAPER_HEADLESS` | 无头模式（`true`/`false`） | `true` |

**示例**：

```bash
# 设置 60 秒超时，5 次重试
export WECHAT_SCRAPER_TIMEOUT=60000
export WECHAT_SCRAPER_RETRY_COUNT=5

# 启动服务器
mcp-server-wechat
```

## 可用工具

本服务器提供 4 个 MCP 工具：

### 1. `search_wechat_articles` - 搜索微信文章

**参数**：
- `query` (string): 搜索关键词，例如 "人工智能"、"Claude AI"
- `limit` (int, 可选): 返回结果数量，范围 1-50，默认 10
- `page` (int, 可选): 页码，从 1 开始，默认 1
- `format` (string, 可选): 响应格式，"json" 或 "markdown"，默认 "json"
- `detail` (string, 可选): 详细程度，"concise" 或 "detailed"，默认 "concise"

**示例**：
```python
{
  "query": "Claude AI",
  "limit": 10,
  "format": "markdown"
}
```

### 2. `get_wechat_article` - 获取文章详情

**参数**：
- `article_id` (string): 文章 ID 或完整 URL
- `include_content` (bool, 可选): 是否包含正文内容，默认 true
- `format` (string, 可选): 响应格式，"json" 或 "markdown"，默认 "json"

**示例**：
```python
{
  "article_id": "https://mp.weixin.qq.com/s/UjZAqvkfk8AzpOoK1KV0yw",
  "include_content": true,
  "format": "markdown"
}
```

### 3. `list_wechat_articles_by_account` - 按公众号获取文章列表

**参数**：
- `account_name` (string): 公众号名称
- `limit` (int, 可选): 返回结果数量，范围 1-50，默认 10
- `format` (string, 可选): 响应格式，默认 "json"
- `detail` (string, 可选): 详细程度，默认 "concise"

### 4. `get_trending_wechat_articles` - 获取热门文章

**参数**：
- `category` (string, 可选): 分类，可选 "hot"、"tech"、"finance"、"entertainment"，默认 "hot"
- `limit` (int, 可选): 返回结果数量，范围 1-50，默认 10
- `format` (string, 可选): 响应格式，默认 "json"
- `detail` (string, 可选): 详细程度，默认 "concise"

## 项目结构

```
mcp-server-wechat/
├── src/
│   └── mcp_server_wechat/
│       ├── __init__.py
│       ├── server.py              # MCP 服务器主入口
│       ├── tools/                 # MCP 工具实现
│       │   ├── search.py          # 搜索工具
│       │   ├── article.py         # 文章详情工具
│       │   ├── account.py         # 公众号文章列表工具
│       │   └── trending.py        # 热门文章工具
│       └── utils/                 # 工具模块
│           ├── wechat_client.py   # Playwright 爬虫客户端
│           ├── formatters.py      # 响应格式化
│           └── errors.py          # 错误处理
├── tests/                         # 测试文件
├── examples/                      # 使用示例
├── pyproject.toml                 # 项目配置
├── README.md
├── LICENSE
└── CHANGELOG.md
```

## 开发

### 安装开发依赖

#### 使用 uv
```bash
uv pip install -e ".[dev]"
```

#### 传统方式
```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行单元测试（不需要网络）
pytest tests/

# 运行集成测试（需要网络）
pytest -m "not skip" tests/

# 查看测试覆盖率
pytest --cov=mcp_server_wechat tests/
```

### 代码格式化

```bash
# 使用 black 格式化代码
black src/ tests/

# 使用 ruff 检查代码
ruff check src/ tests/
```

## 调试技巧

使用 `fastmcp dev` 进行调试时，你可以：

1. 在 MCP Inspector UI 中交互式测试工具调用
2. 查看详细的请求和响应日志
3. 检查错误和异常堆栈
4. 实时修改代码并自动重新加载

## 常见问题

### Q: Claude Desktop 报错 `spawn python ENOENT`？

**A**: 这是因为配置文件中的 Python 命令路径不正确:

**✅ 最佳方案 - 使用 uv**（自动处理所有路径问题）:
```json
{
  "mcpServers": {
    "wechat-articles": {
      "command": "uv",
      "args": ["--directory", "/path/to/project", "run", "mcp-server-wechat"]
    }
  }
}
```

**⚠️ 其他方案的问题**:
1. **macOS 系统通常没有 `python` 命令**,应使用 `python3` 或虚拟环境路径
2. **使用虚拟环境时**,必须指定虚拟环境内的 Python 完整路径
3. **全局安装最容易出问题**,强烈不推荐

### Q: 为什么抓取失败？

**A**: 可能的原因：
1. 网络连接问题 - 检查网络是否正常
2. 触发了反爬虫机制 - 降低请求频率，增加超时时间
3. Playwright 浏览器未安装 - 运行 `playwright install chromium`
4. 文章 URL 失效 - 确认 URL 是否正确

### Q: 为什么阅读量/点赞数显示"未知"？

**A**: 微信对这些数据有反爬虫保护，目前无法稳定获取。这是微信的限制，不是代码问题。

### Q: 如何提高抓取成功率？

**A**:
1. 增加超时时间：`export WECHAT_SCRAPER_TIMEOUT=60000`
2. 增加重试次数：`export WECHAT_SCRAPER_RETRY_COUNT=5`
3. 降低请求频率
4. 使用代理（需自行实现）

### Q: 可以在 CI/CD 中使用吗？

**A**: 可以，但建议：
1. 使用 mock 来避免真实网络请求
2. 设置环境变量 `WECHAT_SCRAPER_HEADLESS=true`
3. 确保 CI 环境安装了必要的浏览器依赖

## 注意事项

⚠️ **重要提醒**：

- 本工具仅供学习和研究使用
- 使用时请遵守相关法律法规和网站使用条款
- 爬虫可能受到反爬虫机制影响，请合理设置重试和延迟
- 大量请求可能导致 IP 被临时限制
- 不要用于商业用途或大规模数据采集

## 许可证

本项目采用 [MIT License](LICENSE)。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [FastMCP 文档](https://gofastmcp.com)
- [MCP 官方文档](https://modelcontextprotocol.io)
- [Playwright 文档](https://playwright.dev)
