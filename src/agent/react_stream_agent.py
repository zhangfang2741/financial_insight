# import asyncio
# from langchain_openai import ChatOpenAI
# from langchain_core.tools import tool
# from langchain.agents import create_react_agent, AgentExecutor
# from langchain import hub
#
#
# # 工具1：加法
# @tool
# def add_numbers(numbers: str) -> int:
#     """输入 'a,b'，返回a+b"""
#     a, b = numbers.split(",")
#     return int(a) + int(b)
#
#
# # 工具2：Wikipedia 搜索
# from langchain_community.utilities import WikipediaAPIWrapper
# from langchain_community.tools import WikipediaQueryRun
#
# wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="en", top_k_results=1))
#
# tools = [add_numbers, wiki_tool]
#
# # ReAct 模板 & 模型
# prompt = hub.pull("hwchase17/react")
# llm = ChatOpenAI(model="gpt-4o-mini")
#
# # 构建 ReAct Agent + 执行器
# agent = create_react_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
#
#
# async def demo_events(user_input: str):
#     # version="v2" 能拿到 parent_ids、更加结构化
#     async for ev in agent_executor.astream_events({"input": user_input}, version="v2"):
#         etype = ev["event"]
#         name = ev.get("name")
#         data = ev.get("data", {})
#
#         # 1) 模型增量token
#         if etype == "on_chat_model_stream":
#             chunk = data.get("chunk")
#             if getattr(chunk, "content", ""):
#                 print(chunk.content, end="", flush=True)
#
#         # 2) 工具开始/结束
#         elif etype == "on_tool_start":
#             print(f"\n[ToolStart] {name} -> {data.get('input')}")
#         elif etype == "on_tool_end":
#             print(f"\n[ToolEnd] {name} <- {data.get('output')}")
#
#         # 3) 最终输出（也可在 on_chain_end / on_chat_model_end 里拿）
#         elif etype == "on_agent_finish":
#             # 某些实现会发送代理结束事件；否则在 on_chat_model_end 拿 data['output']
#             pass
#
#     print()  # 换行
#
#
# if __name__ == "__main__":
#     asyncio.run(demo_events("把 123 和 456 相加，然后用英文一句话回答。"))
#     asyncio.run(demo_events("What is LangChain? Summarize briefly."))
