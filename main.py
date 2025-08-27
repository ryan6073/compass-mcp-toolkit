# main.py (最终手动实现版)

import os
import json
import asyncio
from datetime import datetime, timedelta

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 1. 定义我们工具的元数据 (描述信息)
TOOL_METADATA = {
    "name": "get_contributor_milestone_persona",
    "description": "通过OSS-Compass API获取指定仓库在过去一年内的贡献者里程碑画像数据。",
    "parameters": {
        "type": "object",
        "properties": {
            "repo_url": {
                "type": "string",
                "description": "需要分析的GitHub或Gitee仓库的完整URL。例如：https://github.com/langflow-ai/langflow"
            }
        },
        "required": ["repo_url"]
    }
}

# 2. 我们的核心业务逻辑
def get_contributor_persona_logic(repo_url: str) -> dict:
    access_token = os.getenv("OSS_COMPASS_ACCESS_TOKEN")
    if not access_token:
        return {"error": "错误：服务器环境变量 'OSS_COMPASS_ACCESS_TOKEN' 未设置。"}
    
    # ... (API 调用代码保持不变) ...
    api_url = "https://oss-compass.org/api/v2/metricModel/contributorMilestonePersona"
    end_date = datetime.now().strftime('%Y-%m-%d')
    begin_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    payload = {
        "access_token": access_token, "label": repo_url,
        "begin_date": begin_date, "end_date": end_date,
        "page": "1", "size": "1000"
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        items = response.json().get('items', [])
        return {"result": items}
    except requests.exceptions.RequestException as e:
        return {"error": f"错误：调用API失败 - {str(e)}"}

# 3. 创建我们自己的 FastAPI 应用
app = FastAPI(title="Reliable MCP Server")

# 4. 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. 实现健壮的 MCP over SSE 端点
async def mcp_event_stream(request: Request):
    # 步骤 A: 客户端一连接，立刻发送工具元数据
    yield f"event: tool_metadata\ndata: {json.dumps(TOOL_METADATA)}\n\n"
    print("已发送 tool_metadata。")

    # 步骤 B: 检查初始请求是不是 POST。如果是，说明 Langflow 要运行工具。
    if request.method == "POST":
        try:
            body_bytes = await request.body()
            if body_bytes:
                run_request = json.loads(body_bytes.decode('utf-8'))
                
                # 确认是运行我们的工具
                if run_request.get("name") == TOOL_METADATA["name"]:
                    params = run_request.get("parameters", {})
                    repo_url = params.get("repo_url")
                    
                    print(f"--- 接收到 tool_run 请求，参数: {params} ---")
                    result_data = get_contributor_persona_logic(repo_url=repo_url)
                    
                    # 准备并发送 tool_result 或 tool_error
                    if "error" in result_data:
                        event_type, payload = "tool_error", {"error": result_data["error"]}
                    else:
                        event_type, payload = "tool_result", {"result": json.dumps(result_data["result"], indent=2, ensure_ascii=False)}
                    
                    yield f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"
                    print(f"已发送 {event_type}。")
        except Exception as e:
            yield f"event: tool_error\ndata: {json.dumps({'error': str(e)})}\n\n"
            print(f"处理 POST 请求时发生错误: {e}")
    
    # 步骤 C: 对于所有连接 (包括 GET 和 完成了 POST 的)，保持心跳直到客户端断开
    try:
        while True:
            await asyncio.sleep(1) # 保持连接
    except asyncio.CancelledError:
        # 当客户端断开连接时，FastAPI/Uvicorn 会取消这个任务
        print("客户端断开连接，数据流正常关闭。")
        

@app.get("/mcp", tags=["MCP"])
@app.post("/mcp", tags=["MCP"])
async def mcp_endpoint(request: Request):
    # 这个端点是 Langflow 连接的目标
    return StreamingResponse(mcp_event_stream(request), media_type="text/event-stream")

# mcp: 127.0.0.1
# 0.0.0.0
