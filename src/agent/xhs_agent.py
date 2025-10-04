import os

from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

from src.tool.xms_tool import xhs_tools

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_API_KEY"] = "AIzaSyB8-MZdYkN_OCtdj3OUP7UmoSzE3YSr4lc"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import ToolNode

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0
)

# 2. 创建 LLM 并绑定工具
llm_with_tools = llm.bind_tools(xhs_tools)


# 3. 定义 agent 节点
def call_model(state: MessagesState):
    messages = state["messages"]
    # 添加系统提示
    if not messages or messages[0].type != "system":
        system_msg = SystemMessage(
            content="你是一个小红书的中文创作助手，创作内容包括图像、文本和视频，并能帮我使用小红书的相关工具完成任务。当调用工具时，请仔细检查参数类型和格式，确保所有必需参数都已提供，所有工具调用不需要人工确认，直接调用即可。")
        messages = [system_msg] + messages

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
workflow = (
    StateGraph(MessagesState)
    .add_node("agent", call_model)
    .add_node("tools", ToolNode(xhs_tools))
    .add_edge(START, "agent")
    .add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    .add_edge("tools", "agent")
)

app = workflow.compile()

# 7. 使用
response = app.invoke({
    "messages": [
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
