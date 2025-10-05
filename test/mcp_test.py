import json
import time

import requests

from src.integration.xhs_mcp_client import XhsMCPClient


def main():
    """主函数 - 使用示例"""

    # 创建客户端实例
    client = XhsMCPClient()

    try:
        # 1. 初始化连接
        print("=== 初始化连接 ===")
        init_response = client.initialize()
        print(json.dumps(init_response, indent=2, ensure_ascii=False))
        print("\n等待初始化完成...")
        time.sleep(0.5)  # 多等待一会儿
        print()

        # 2. 列出所有可用工具
        print("=== 列出可用工具 ===")
        tools_response = client.list_tools()
        print(json.dumps(tools_response, indent=2, ensure_ascii=False))
        print()

        # 3. 列出所有资源
        print("=== 列出可用资源 ===")
        resources_response = client.list_resources()
        print(json.dumps(resources_response, indent=2, ensure_ascii=False))
        print()

        # 4. 调用工具示例（根据你的实际工具名称和参数调整）
        print("=== 调用工具示例 ===")
        tool_response = client.call_tool(
            tool_name="check_login_status",
            arguments={}
        )
        print(json.dumps(tool_response, indent=2, ensure_ascii=False))

        # 5. 读取资源示例
        # print("=== 读取资源示例 ===")
        # resource_response = client.read_resource("resource://example")
        # print(json.dumps(resource_response, indent=2, ensure_ascii=False))

        # 6. 列出提示词模板
        print("=== 列出提示词模板 ===")
        prompts_response = client.list_prompts()
        print(json.dumps(prompts_response, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()