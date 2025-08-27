# gitee_pr_server.py (修改为 SSE 模式)

import os
import json
import httpx
from typing import Optional
from mcp.server import FastMCP
from dotenv import load_dotenv

# 加载 .env 文件 (我们依然保留方案2B中的代码，使其更健壮)
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

# 1. 初始化 FastMCP 时，指定 host 和 port
app = FastMCP(
    'gitee-tools',
    host='0.0.0.0', # 监听所有网络接口
    port=8000      # 您可以选择一个未被占用的端口
)

@app.tool()
async def get_pull_requests(
    label: str,
    begin_date: str,
    end_date: str,
    access_token: Optional[str] = None,
    direction: str = "desc",
    page: int = 1,
    size: int = 10,
) -> str:
    """
    从 Gitee Compass API 获取指定仓库的 Pull Request 元数据。

    Args:
        label: 要查询的仓库地址，例如 'https://github.com/oss-compass/compass-web-service'。
        begin_date: 查询起始日期，格式为 'YYYY-MM-DD'。
        end_date: 查询结束日期，格式为 'YYYY-MM-DD'。
        access_token: Gitee API 的访问令牌。如果未提供，将尝试从环境变量 GITEE_ACCESS_TOKEN 中获取。
        direction: 排序方向，'desc' (降序) 或 'asc' (升序)。默认为 'desc'。
        page: 分页页码。默认为 1。
        size: 每页数量。默认为 10。

    Returns:
        包含 Pull Request 数据的 JSON 字符串。如果请求失败，则返回错误信息。
    """
    # 接口 URL
    url = "https://compass.gitee.com/api/v2/metadata/pullRequests"

    # 优先使用函数参数中的 access_token，否则从环境变量中读取
    token = access_token or os.getenv("GITEE_ACCESS_TOKEN")
    if not token:
        return json.dumps({"error": "Access token not provided. Please provide it as a parameter or set the GITEE_ACCESS_TOKEN environment variable."})

    # 构建请求体
    payload = {
        "access_token": token,
        "label": label,
        "direction": direction,
        "begin_date": begin_date,
        "end_date": end_date,
        "page": page,
        "size": size,
    }

    headers = {
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=url,
                headers=headers,
                json=payload  # httpx可以直接使用json参数传递字典
            )
            # 抛出HTTP错误状态（如 4xx 或 5xx）的异常
            response.raise_for_status()
            
            # 返回 JSON 响应的字符串形式
            return response.text

        except httpx.HTTPStatusError as e:
            return json.dumps({
                "error": "HTTP Error",
                "status_code": e.response.status_code,
                "details": e.response.text
            })
        except httpx.RequestError as e:
            return json.dumps({
                "error": "Request Failed",
                "details": str(e)
            })

if __name__ == "__main__":
    # 使用 stdio 传输协议运行服务器
    app.run(transport='sse')