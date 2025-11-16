# MCP微信文章服务 - Cherry Studio配置指南

## 🚨 前提条件检查清单

在另一台电脑上配置前，先确认这些，别到时候又来找我问为什么启动不了：

- [ ] 已安装Python 3.8+
- [ ] 已安装`uv`包管理器 (`pip install uv`)
- [ ] 已克隆此仓库到本地
- [ ] 已安装Cherry Studio

## 📋 配置步骤

### 1. 获取仓库路径
在你的电脑上找到这个仓库的完整路径，比如：
```
/Users/your-username/projects/mcp-server-wechat
```

### 2. Cherry Studio JSON配置

在Cherry Studio的设置中，找到MCP配置部分，添加以下JSON：

```json
{
  "mcpServers": {
    "wechat-articles": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/your-username/projects/mcp-server-wechat",
        "run",
        "mcp-server-wechat"
      ]
    }
  }
}
```

### 3. 🔥 关键替换项

**把上面的路径替换成你电脑上的实际路径！**

不同操作系统的路径格式：

- **macOS/Linux**: `/Users/your-username/path/to/mcp-server-wechat`
- **Windows**: `C:\\Users\\your-username\\path\\to\\mcp-server-wechat`

⚠️ **Windows用户特别注意**：路径中的反斜杠要双写：`\\`

### 4. 验证配置

配置完后，在Cherry Studio中：

1. 重启Cherry Studio
2. 查看MCP服务状态
3. 应该能看到"wechat-articles"服务已连接

## 🐛 常见问题排查

### 问题1: uv命令找不到
**症状**: 启动失败，提示找不到uv命令
**解决**:
```bash
pip install uv
# 或者
pip3 install uv
```

### 问题2: 路径错误
**症状**: 服务启动但立即崩溃
**解决**: 检查路径是否正确，是否存在该目录

### 问题3: 依赖问题
**症状**: 导入错误，缺少模块
**解决**: 在仓库目录下运行：
```bash
cd /your/path/to/mcp-server-wechat
uv pip install -r requirements.txt
# 或者如果有pyproject.toml
uv sync
```

### 问题4: 权限问题
**症状**: 权限被拒绝
**解决**:
```bash
chmod +x /your/path/to/mcp-server-wechat/mcp-server-wechat
```

## 🎯 测试配置是否成功

在Cherry Studio的对话框中输入：
```
请帮我获取一篇微信文章的内容
```

如果配置正确，你应该能看到MCP服务被调用，并返回相关结果。

## ⚡ 快速诊断命令

在终端运行这些命令快速检查问题：

```bash
# 检查uv是否安装
uv --version

# 检查仓库路径是否存在
ls -la /your/path/to/mcp-server-wechat

# 测试手动启动MCP服务
cd /your/path/to/mcp-server-wechat
uv run mcp-server-wechat
```

## 📝 注意事项

1. **路径千万别写错** - 这是90%的配置失败原因
2. **Windows路径格式** - 必须用双反斜杠`\\`
3. **依赖必须完整** - 确保requirements.txt中的依赖都安装了
4. **重启Cherry Studio** - 配置修改后必须重启才能生效

---

**配置失败？** 先按照这个文档一步步排查，90%的问题都能解决。如果还有问题，带上具体的错误信息再来问我！