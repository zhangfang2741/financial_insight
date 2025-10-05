# python
# 文件: src/agent/xhs_agent.py
import os
import re
import json

from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

from src.tool.xms_tool import xhs_tools

# 可选: 仅在未设置时为代理赋默认值
os.environ.setdefault("http_proxy", "http://127.0.0.1:7890")
os.environ.setdefault("https_proxy", "http://127.0.0.1:7890")
os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyB8-MZdYkN_OCtdj3OUP7UmoSzE3YSr4lc")
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import ToolNode

# 从环境变量读取密钥，避免硬编码
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("缺少 GOOGLE_API_KEY 环境变量")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0,
    api_key=GOOGLE_API_KEY,
)

# 绑定工具
llm_with_tools = llm.bind_tools(xhs_tools)

GOAL_TARGET = 10  # 目标完成数


def _extract_progress(text: str):
    """
    从 AI 输出中解析 <progress>{...}</progress> 段落，返回 dict 或 None
    """
    m = re.search(r"<progress>\s*(\{.*?\})\s*</progress>", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


# agent 节点
def call_model(state: MessagesState):
    messages = state["messages"]

    # 系统提示: 强制输出进度 JSON；未达成必须继续调用工具；达成后才结束
    if not messages or messages[0].type != "system":
        system_msg = SystemMessage(
            content=(
                "你是一个小红书中文创作助手。要点:\n"
                "1. 若尚未达到目标, 必须继续调用工具推进任务；禁止空转或无意义回复。\n"
                "2. 仅当已达到目标时才停止工具调用并输出最终汇总。\n"
                "3. 在每轮消息末尾, 必须输出一个 <progress>{JSON}</progress>:\n"
                "   - JSON 字段: {\"succeeded\": 已完成条数, \"target\": 目标条数, \"status\": \"continue\"|\"done\"}\n"
                "4. 当 status==\"continue\" 时, 下一步必须至少发起一次工具调用；当 status==\"done\" 时不得再发起工具调用。"
            )
        )
        messages = [system_msg] + messages

    response = llm_with_tools.invoke(messages)
    print(response.content)  # 调试可见每轮输出与进度
    return {"messages": [response]}


# 路由: 基于进度 JSON 判定
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]

    # 默认: 未解析到进度时, 若有工具调用则进入 tools, 否则结束
    if not isinstance(last_message, AIMessage):
        return END

    progress = _extract_progress(last_message.content or "")
    if progress:
        succeeded = int(progress.get("succeeded", 0))
        target = int(progress.get("target", GOAL_TARGET))
        status = str(progress.get("status", "continue")).lower()
        print(f"[progress] succeeded={succeeded}, target={target}, status={status}")
        if status == "done" or succeeded >= target:
            return END

    # 未达成目标时必须进入 tools
    if getattr(last_message, "tool_calls", None):
        return "tools"

    # 若模型未给出工具调用, 仍然结束(依赖系统提示避免此分支)
    return END


# 构图
workflow = (
    StateGraph(MessagesState)
    .add_node("agent", call_model)
    .add_node("tools", ToolNode(xhs_tools))
    .add_edge(START, "agent")
    .add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    .add_edge("tools", "agent")
)

app = workflow.compile()

# 运行
response = app.invoke(
    {
        "messages": [
            HumanMessage(content="""
你的任务是：搜索“蜂巢蜜”相关的帖子，分析公开可访问的小红书笔记（例如官方 API 或第三方已授权数据源返回的内容），聚焦于与“蜂巢蜜”、“蜂蜜”、“原生态蜂蜜”、“蜂农直采”、“蜂巢蜜购买”、“蜂巢蜜试吃”相关的帖子与评论。
对每条评论执行以下任务：
1. 判断评论者的意图类别：
   - high_intent：明确表示想买、询价、想了解购买方式、想试吃。
   - medium_intent：表达兴趣但未明确购买意愿。
   - low_intent：仅随意评论或夸赞，没有购买迹象。
   - noise：无关、广告、刷屏等内容。
2. 对于 high_intent 或 medium_intent 的评论，生成一条友好、自然的公开评论回复建议，引导用户加入你主页的“小红书群”了解更多蜂巢蜜信息。
   - 语气：真诚、自然、非促销化。
   - 不要包含任何私信、微信号、二维码或违规引流内容。
本次目标是评论回复成功10条；未达到目标前，必须持续自我反思并调用工具推进任务；达到目标时再输出最终总结，并在消息末尾给出 <progress>{"succeeded":X,"target":10,"status":"done"}</progress>。
我的 xsec_token 已在上文给出。
""")
        ]
    },
    # 提高递归上限，确保可持续循环直到达成目标
    config={"recursion_limit": 500},
)

print(response["messages"][-1].content)
