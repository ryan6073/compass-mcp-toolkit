import requests
import json

# 接口URL
url = "https://compass.gitee.com/api/v2/metricModel/contributorMilestonePersona"

# 请求体数据
payload = {
    "access_token": "11fb62bd88d4558d5480755ac653a075675036c9",  # 请在此处填入有效的access_token
    "label": "https://github.com/oss-compass/compass-web-service",
    "direction": "desc",
    "begin_date": "2010-02-22",
    "end_date": "2024-03-22",
    "page": 1,
    "size": 10
}

# 请求头，指定内容类型为JSON
headers = {
    "Content-Type": "application/json"
}

try:
    # 发送POST请求
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload)  # 将字典转换为JSON字符串
    )
    
    # 打印响应状态码
    print(f"响应状态码: {response.status_code}")
    
    # 尝试解析JSON响应
    try:
        response_json = response.json()
        print("响应内容:")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))  # 格式化打印JSON
    except json.JSONDecodeError:
        # 如果响应不是JSON格式，直接打印文本内容
        print("响应内容（非JSON格式）:")
        print(response.text)

except requests.exceptions.RequestException as e:
    # 捕获请求过程中的所有异常（如网络错误、超时等）
    print(f"请求发生错误: {str(e)}")