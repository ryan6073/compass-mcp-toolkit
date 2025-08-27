# Compass Enriched Data Tools

这是一个基于 FastMCP 框架构建的服务，提供了一系列工具用于从 Gitee Compass 社区 API 获取丰富的（Enriched）开源项目数据。

## ✨ 功能特性

服务提供以下数据查询工具：
- `get_fork_enriched_data`: 获取仓库的 fork 详细数据。
- `get_pull_event_enriched_data`: 获取 Pull Request 事件数据。
- `get_git_commit_enriched_data`: 获取 Git 提交的详细数据。
- `get_issue_enriched_data`: 获取 Issue 的详细数据。
- `get_pull_request_enriched_data`: 获取 Pull Request 的元数据。
- `get_repo_enriched_data`: 获取仓库的综合信息。
- `get_stargazer_enriched_data`: 获取 Stargazer（点赞者）的详细数据。
- `get_watch_enriched_data`: 获取 Watch（关注者）的详细数据。
- `get_releases_enriched_data`: 获取版本发布的详细数据。
- `get_github_event_data`: 获取原始的 GitHub Event 数据。
- `get_github_repo_event_data`: 获取仓库级别的 Event 聚合数据。

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone [https://github.com/your-username/compass-enriched-data-tools.git](https://github.com/your-username/compass-enriched-data-tools.git)
cd compass-enriched-data-tools
```

### 2. 安装依赖
建议在虚拟环境中使用：
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. 配置环境
复制 `.env.example` (如果提供了) 或者手动创建一个 `.env` 文件，并填入你的 Gitee Access Token:
```
GITEE_ACCESS_TOKEN="your_gitee_access_token_here"
```

### 4. 启动服务
```bash
python enriched_data_server.py
```
服务将运行在 `http://0.0.0.0:8001`。

## 🔧 使用方法

服务启动后，你可以通过 MCP 客户端调用已注册的工具。