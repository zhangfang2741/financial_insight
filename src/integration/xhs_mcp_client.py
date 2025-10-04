import json
import logging
import time
from typing import Any, Dict, Optional

import requests


class XhsMCPClient:
    """MCP (Model Context Protocol) HTTP 客户端"""

    def __init__(self, base_url: str = "http://localhost:18060/mcp"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.session_id = None  # 存储 MCP 会话 ID

    def initialize(self) -> Dict[str, Any]:
        """初始化连接"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "python-mcp-client",
                    "version": "1.0.0"
                }
            }
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        result = response.json()

        # 获取并保存会话 ID
        session_id = response.headers.get('Mcp-Session-Id')
        if session_id:
            self.session_id = session_id
            # 在后续所有请求中使用这个会话 ID
            self.session.headers.update({'Mcp-Session-Id': session_id})
            logging.info(f"会话 ID: {session_id}")

        return result

    def send_initialized(self) -> None:
        """发送初始化完成通知（某些服务器不需要）"""
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }

        try:
            self.session.post(self.base_url, json=payload)
            time.sleep(0.1)
        except Exception:
            pass  # 如果服务器不支持，忽略错误

    def set_logging_level(self, level: str = "info") -> Dict[str, Any]:
        """设置日志级别"""
        payload = {
            "jsonrpc": "2.0",
            "id": 100,  # 添加 id 字段
            "method": "logging/setLevel",
            "params": {
                "level": level
            }
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def list_tools(self) -> Dict[str, Any]:
        """列出所有可用的工具"""
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """调用指定的工具"""
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def list_resources(self) -> Dict[str, Any]:
        """列出所有可用的资源"""
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/list",
            "params": {}
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def read_resource(self, uri: str) -> Dict[str, Any]:
        """读取指定的资源"""
        payload = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "resources/read",
            "params": {
                "uri": uri
            }
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def list_prompts(self) -> Dict[str, Any]:
        """列出所有可用的提示词模板"""
        payload = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "prompts/list",
            "params": {}
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_prompt(self, prompt_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """获取指定的提示词"""
        payload = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "prompts/get",
            "params": {
                "name": prompt_name,
                "arguments": arguments or {}
            }
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    """主函数 - 使用示例"""

    # 创建客户端实例
    client = XhsMCPClient()

    try:
        # 1. 初始化连接
        logging.info("=== 初始化连接 ===")
        init_response = client.initialize()
        logging.info(json.dumps(init_response, indent=2, ensure_ascii=False))
        logging.info("\n等待初始化完成...")
        time.sleep(0.5)  # 多等待一会儿
        logging.info()

        # 2. 列出所有可用工具
        logging.info("=== 列出可用工具 ===")
        tools_response = client.list_tools()
        logging.info(json.dumps(tools_response, indent=2, ensure_ascii=False))
        logging.info()

        # 3. 列出所有资源
        logging.info("=== 列出可用资源 ===")
        resources_response = client.list_resources()
        logging.info(json.dumps(resources_response, indent=2, ensure_ascii=False))
        logging.info()

        # 4. 调用工具示例（根据你的实际工具名称和参数调整）
        logging.info("=== 调用工具示例 ===")
        tool_response = client.call_tool(
            tool_name="check_login_status",
            arguments={}
        )
        logging.info(json.dumps(tool_response, indent=2, ensure_ascii=False))

        # 5. 读取资源示例
        # logging.info("=== 读取资源示例 ===")
        # resource_response = client.read_resource("resource://example")
        # logging.info(json.dumps(resource_response, indent=2, ensure_ascii=False))

        # 6. 列出提示词模板
        logging.info("=== 列出提示词模板 ===")
        prompts_response = client.list_prompts()
        logging.info(json.dumps(prompts_response, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        logging.info(f"请求错误: {e}")
    except Exception as e:
        logging.info(f"发生错误: {e}")
