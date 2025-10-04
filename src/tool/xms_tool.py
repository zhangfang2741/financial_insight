import json
import logging
from typing import List, Optional, Dict, Any

from langchain_core.tools import tool
from langgraph.constants import END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from src.integration.xhs_mcp_client import XhsMCPClient

# 全局MCP客户端，需要在使用前初始化
_xhs_mcp_client = None


def set_mcp_client(client):
    """设置MCP客户端实例"""
    global _xhs_mcp_client
    _xhs_mcp_client = client
    init_response = _xhs_mcp_client.initialize()
    logging.info(json.dumps(init_response, indent=2, ensure_ascii=False))
    logging.info("xhs_client初始化完成...")


def get_mcp_client():
    """获取MCP客户端实例"""
    if _xhs_mcp_client is None:
        raise RuntimeError("MCP client not initialized. Call set_mcp_client() first.")
    return _xhs_mcp_client


# 工具函数
@tool
def check_login_status() -> Dict[str, Any]:
    """检查小红书登录状态

    Returns:
        Dict: 包含登录状态信息的字典
    """
    try:
        client = get_mcp_client()
        result = client.call_tool(
            tool_name="check_login_status",
            arguments={}
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def get_login_qrcode() -> Dict[str, Any]:
    """获取小红书登录二维码，返回Base64图片和超时时间

    Returns:
        Dict: 包含二维码Base64数据和超时时间的字典
    """
    try:
        client = get_mcp_client()
        result = client.call_tool(
            tool_name="get_login_qrcode",
            arguments={}
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def list_feeds() -> Dict[str, Any]:
    """获取用户发布的内容列表

    Returns:
        Dict: 包含用户发布的所有内容列表
    """
    try:
        client = get_mcp_client()
        result = client.call_tool(
            tool_name="list_feeds",
            arguments={}
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def search_feeds(keyword: str) -> Dict[str, Any]:
    """搜索小红书内容（需要已登录）

    Args:
        keyword: 搜索关键词，不能为空，最多100个字符

    Returns:
        Dict: 包含搜索结果的字典
    """
    try:
        keyword = keyword.strip()
        if not keyword:
            return {"success": False, "error": "关键词不能为空"}
        if len(keyword) > 100:
            return {"success": False, "error": "关键词最多100个字符"}

        client = get_mcp_client()
        result = client.call_tool(
            tool_name="search_feeds",
            arguments={"keyword": keyword}
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def get_feed_detail(feed_id: str, xsec_token: str) -> Dict[str, Any]:
    """获取小红书笔记详情，返回笔记内容、图片、作者信息、互动数据及评论列表

    Args:
        feed_id: 小红书笔记ID，不能为空
        xsec_token: 访问令牌，不能为空

    Returns:
        Dict: 包含笔记详情的字典
    """
    try:
        feed_id = feed_id.strip()
        xsec_token = xsec_token.strip()

        if not feed_id:
            return {"success": False, "error": "笔记ID不能为空"}
        if not xsec_token:
            return {"success": False, "error": "访问令牌不能为空"}

        client = get_mcp_client()
        result = client.call_tool(
            tool_name="get_feed_detail",
            arguments={
                "feed_id": feed_id,
                "xsec_token": xsec_token
            }
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def user_profile(user_id: str, xsec_token: str) -> Dict[str, Any]:
    """获取小红书用户主页，返回用户基本信息、关注/粉丝/获赞量及其笔记内容

    Args:
        user_id: 小红书用户ID，不能为空
        xsec_token: 访问令牌，不能为空

    Returns:
        Dict: 包含用户信息的字典
    """
    try:
        user_id = user_id.strip()
        xsec_token = xsec_token.strip()

        if not user_id:
            return {"success": False, "error": "用户ID不能为空"}
        if not xsec_token:
            return {"success": False, "error": "访问令牌不能为空"}

        client = get_mcp_client()
        result = client.call_tool(
            tool_name="user_profile",
            arguments={
                "user_id": user_id,
                "xsec_token": xsec_token
            }
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def publish_content(
        title: str,
        content: str,
        images: List[str],
        tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """发布小红书图文内容

    Args:
        title: 内容标题，不能为空，最多20个字符
        content: 正文内容，不能为空
        images: 图片路径列表，至少需要1张图片
        tags: 话题标签列表，可选

    Returns:
        Dict: 包含发布结果的字典
    """
    try:
        title = title.strip()
        content = content.strip()

        if not title:
            return {"success": False, "error": "标题不能为空"}
        if len(title) > 20:
            return {"success": False, "error": "标题最多20个字符"}
        if not content:
            return {"success": False, "error": "正文内容不能为空"}
        if not images:
            return {"success": False, "error": "至少需要1张图片"}

        # 验证图片路径
        validated_images = []
        for img in images:
            img = img.strip()
            if not img:
                return {"success": False, "error": "图片路径不能为空"}
            validated_images.append(img)

        # 处理标签
        validated_tags = None
        if tags:
            validated_tags = [tag.strip() for tag in tags if tag.strip()]

        client = get_mcp_client()
        arguments = {
            "title": title,
            "content": content,
            "images": validated_images
        }
        if validated_tags:
            arguments["tags"] = validated_tags

        result = client.call_tool(
            tool_name="publish_content",
            arguments=arguments
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def publish_with_video(
        title: str,
        content: str,
        video: str,
        tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """发布小红书视频内容（仅支持本地单个视频文件）

    Args:
        title: 内容标题，不能为空，最多20个字符
        content: 正文内容，不能为空
        video: 本地视频绝对路径，必须是 .mp4, .mov, .avi, .mkv 格式
        tags: 话题标签列表，可选

    Returns:
        Dict: 包含发布结果的字典
    """
    try:
        title = title.strip()
        content = content.strip()
        video = video.strip()

        if not title:
            return {"success": False, "error": "标题不能为空"}
        if len(title) > 20:
            return {"success": False, "error": "标题最多20个字符"}
        if not content:
            return {"success": False, "error": "正文内容不能为空"}
        if not video:
            return {"success": False, "error": "视频路径不能为空"}
        if not video.startswith('/'):
            return {"success": False, "error": "必须提供绝对路径"}
        if not any(video.endswith(ext) for ext in ['.mp4', '.mov', '.avi', '.mkv']):
            return {"success": False, "error": "视频格式不支持，仅支持 .mp4, .mov, .avi, .mkv"}

        # 处理标签
        validated_tags = None
        if tags:
            validated_tags = [tag.strip() for tag in tags if tag.strip()]

        client = get_mcp_client()
        arguments = {
            "title": title,
            "content": content,
            "video": video
        }
        if validated_tags:
            arguments["tags"] = validated_tags

        result = client.call_tool(
            tool_name="publish_with_video",
            arguments=arguments
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def post_comment_to_feed(feed_id: str, xsec_token: str, content: str) -> Dict[str, Any]:
    """发表评论到小红书笔记

    Args:
        feed_id: 小红书笔记ID，不能为空
        xsec_token: 访问令牌，不能为空
        content: 评论内容，不能为空，最多1000个字符

    Returns:
        Dict: 包含评论结果的字典
    """
    try:
        feed_id = feed_id.strip()
        xsec_token = xsec_token.strip()
        content = content.strip()

        if not feed_id:
            return {"success": False, "error": "笔记ID不能为空"}
        if not xsec_token:
            return {"success": False, "error": "访问令牌不能为空"}
        if not content:
            return {"success": False, "error": "评论内容不能为空"}
        if len(content) > 1000:
            return {"success": False, "error": "评论内容不能超过1000个字符"}

        client = get_mcp_client()
        result = client.call_tool(
            tool_name="post_comment_to_feed",
            arguments={
                "feed_id": feed_id,
                "xsec_token": xsec_token,
                "content": content
            }
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_xiaohongshu_tools() -> List:
    """创建小红书工具集合

    Returns:
        List: 包含所有小红书工具的列表
    """
    return [
        check_login_status,
        get_login_qrcode,
        list_feeds,
        search_feeds,
        get_feed_detail,
        user_profile,
        publish_content,
        publish_with_video,
        post_comment_to_feed,
    ]


# 1. 初始化MCP客户端
set_mcp_client(XhsMCPClient())

# 2. 创建工具集
xhs_tools = create_xiaohongshu_tools()
__all__ = ["xhs_tools"]

# 使用示例
if __name__ == "__main__":
    import os

    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    os.environ["GOOGLE_API_KEY"] = "AIzaSyB8-MZdYkN_OCtdj3OUP7UmoSzE3YSr4lc"

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain.agents import ToolNode

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0,
    )

    # 2. 创建 LLM 并绑定工具
    llm_with_tools = llm.bind_tools(xhs_tools)


    # 3. 定义 agent 节点
    def call_model(state: MessagesState):
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}


    # 4. 定义路由逻辑
    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if not last_message.tool_calls:
            return END
        return "tools"


    # 5. 构建图
    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(xhs_tools))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    # 6. 编译
    app = workflow.compile()

    # 7. 使用
    response = app.invoke({
        "messages": [
            SystemMessage(
                content="你是一个小红书的中文创作助手，创作内容包括图像、文本和视频，并能帮我使用小红书的相关工具完成任务。当调用工具时，请仔细检查参数类型和格式，确保所有必需参数都已提供。"
            ),
            HumanMessage(content="""
                帮我写一篇帖子发布到小红书上，
                配图为：/Users/zhangfang/Pictures/蜂蜜/淘宝蜂蜜主图/油菜蜜主图/7371654063385_.pic.jpg
                标题是："纽西兰陶波湖的Ngātoroirangi矿湾毛利岩雕"
                正文内容："在新西兰的心脏地带，陶波湖畔，有一个令人惊叹的地方——Ngātoroirangi矿湾毛利岩雕。这些岩雕不仅是毛利文化的瑰宝，更是大自然与人类艺术完美结合的见证。每一块岩石都讲述着一个古老的故事，诉说着毛利人的传说和信仰。走近这些岩雕，你会感受到一种穿越时空的力量，仿佛能听到远古时代的回响。无论是清晨的第一缕阳光，还是傍晚的余晖洒在岩石上，Ngātoroirangi矿湾毛利岩雕总是展现出它独特的魅力。来这里，不仅是一次视觉的盛宴，更是一场心灵的洗礼。让我们一起走进这片神秘的土地，感受毛利文化的深厚底蕴，体验大自然的无穷魅力。"
                话题标签：["新西兰旅游", "毛利文化", "陶波湖", "自然与艺术"]
                """)
        ]
    })

    print(response["messages"][-1].content)
