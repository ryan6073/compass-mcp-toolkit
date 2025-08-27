# Gitee Compass MCP 工具包 (Compass MCP Toolkit)

本项目是一个基于 [FastMCP](https://github.com/homexlab/fast-mcp) 框架构建的服务套件，旨在提供一套完整的工具，用于调用 [Gitee Compass](https://oss-compass.isrc.ac.cn/) 社区的开放 API。

它目前包含两个独立的服务：
1.  **指标模型数据服务**: 提供高阶的分析模型数据，例如贡献者画像、项目活跃度、社区健康度等。
2.  **丰富化数据服务**: 提供更细粒度的原始事件数据，例如 Fork、Commit、Issue、PR 等详细信息。

## ✨ 核心服务

### 1. 指标模型数据服务 (`compass_model_data_tools.py`)

此服务运行在 `http://0.0.0.0:8000`，提供以下分析模型工具：

-   `get_contributor_milestone_persona`: 获取贡献者里程画像（临时/常规/核心）。
-   `get_contributor_role_persona`: 获取贡献者角色画像（组织/个人）。
-   `get_contributor_domain_persona`: 获取贡献者领域画像（代码/Issue/文档等）。
-   `get_organizations_activity`: 分析项目中的组织（公司、机构）活跃度。
-   `get_project_activity`: 获取项目的整体活跃度指标。
-   `get_community_service_and_support`: 分析 Issue 和 PR 的响应与处理效率。
-   `get_collaboration_development_index`: 衡量项目的协作开发效率指数。

### 2. 丰富化数据服务 (`enriched_data_server.py`)

此服务运行在 `http://0.0.0.0:8001`，提供以下详细数据工具：

-   `get_fork_enriched_data`: 获取仓库的 fork 详细数据。
-   `get_pull_event_enriched_data`: 获取 Pull Request 事件数据。
-   `get_git_commit_enriched_data`: 获取 Git 提交的详细数据。
-   `get_issue_enriched_data`: 获取 Issue 的详细数据。
-   `get_pull_request_enriched_data`: 获取 Pull Request 的元数据。
-   `get_repo_enriched_data`: 获取仓库的综合信息。
-   `get_stargazer_enriched_data`: 获取 Stargazer（点赞者）的详细数据。
-   `get_watch_enriched_data`: 获取 Watch（关注者）的详细数据。
-   `get_releases_enriched_data`: 获取版本发布的详细数据。
-   `get_github_event_data`: 获取原始的 GitHub Event 数据。
-   `get_github_repo_event_data`: 获取仓库级别的 Event 聚合数据。

## 🚀 快速开始

本项目推荐使用 `uv` 进行高性能的包管理和虚拟环境创建。

### 环境要求
-   Python 3.8+
-   [uv](https://github.com/astral-sh/uv) (安装: `pip install uv`)

### 安装步骤

1.  **克隆仓库**
    ```bash
    git clone [https://github.com/ryan6073/compass-mcp-toolkit.git](https://github.com/ryan6073/compass-mcp-toolkit.git)
    cd compass-mcp-toolkit
    ```

2.  **创建并激活虚拟环境 (使用 uv)**
    ```bash
    # 创建虚拟环境，uv 会自动生成一个 .venv 文件夹
    uv venv

    # 激活虚拟环境
    # macOS / Linux
    source .venv/bin/activate
    # Windows (CMD)
    # .venv\Scripts\activate
    ```

3.  **安装依赖 (使用 uv)**
    ```bash
    uv pip install -r requirements.txt
    ```

## 🔧 环境配置

在启动服务之前，你需要在项目根目录下创建一个 `.env` 文件来存放你的 Gitee Access Token。

1.  创建文件:
    ```bash
    touch .env
    ```

2.  编辑 `.env` 文件，填入以下内容:
    ```env
    GITEE_ACCESS_TOKEN="your_gitee_access_token_here"
    ```
    请将 `your_gitee_access_token_here` 替换为你自己的有效 Token。

## ▶️ 启动服务

两个服务是相互独立的，需要分别启动。你需要**打开两个终端窗口**，并确保在每个窗口中都已激活虚拟环境。

**终端 1: 启动指标模型数据服务**
```bash
python compass_model_data_tools.py
```
> ✅ 服务成功启动后，你将看到日志输出，服务监听在端口 **8000**。

**终端 2: 启动丰富化数据服务**
```bash
python enriched_data_server.py
```
> ✅ 服务成功启动后，你将看到日志输出，服务监听在端口 **8001**。

现在，两个 MCP 服务都已成功运行，你可以通过 MCP 客户端来调用它们提供的工具了。