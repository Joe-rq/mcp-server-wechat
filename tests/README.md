# 测试

本目录包含 `mcp-server-wechat` 的测试套件。

## 运行测试

### 安装测试依赖

```bash
pip install -e ".[dev]"
```

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_tools.py
```

### 查看测试覆盖率

```bash
pytest --cov=mcp_server_wechat tests/
```

## 测试说明

### 单元测试

- `test_tools.py`: 测试工具函数的输入验证和基本功能

这些测试不需要网络访问，可以快速运行。

### 集成测试

集成测试需要访问真实的微信网站，因此默认被跳过。

要运行集成测试：

```bash
pytest -m "not skip" tests/
```

或者运行特定的集成测试：

```bash
pytest tests/test_tools.py::test_search_articles_integration -v
```

## 注意事项

1. **网络依赖**: 集成测试需要稳定的网络连接
2. **反爬虫**: 频繁测试可能触发微信的反爬虫机制
3. **CI/CD**: 在 CI/CD 环境中应该使用 mock，避免真实网络请求

## 添加新测试

创建新的测试文件时，请遵循以下规范：

1. 文件名以 `test_` 开头
2. 测试函数以 `test_` 开头
3. 使用 `@pytest.mark.skip` 标记需要网络的测试
4. 使用 `conftest.py` 中的 fixtures 来提供测试数据
