# 使用示例

这个目录包含了 `mcp-server-wechat` 的使用示例。

## 运行示例

确保已经安装依赖：

```bash
pip install -e .
playwright install chromium
```

## 可用示例

### 1. 获取文章详情 (`get_article.py`)

获取指定微信文章的完整信息：

```bash
PYTHONPATH=src python examples/get_article.py
```

### 2. 搜索文章 (`search_articles.py`)

搜索微信公众号文章：

```bash
PYTHONPATH=src python examples/search_articles.py
```

## 自定义示例

你可以修改这些示例中的参数来测试不同的功能：

- 修改 `article_url` 来获取不同的文章
- 修改 `query` 来搜索不同的关键词
- 修改 `format` 参数（"json" 或 "markdown"）来改变输出格式
- 修改 `detail` 参数（"concise" 或 "detailed"）来控制详细程度
