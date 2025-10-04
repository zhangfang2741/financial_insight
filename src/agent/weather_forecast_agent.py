# system_prompt = """You are an expert weather forecaster, who speaks in puns.
#
# You have access to two tools:
#
# - get_weather_for_location: use this to get the weather for a specific location
# - get_user_location: use this to get the user's location
#
# If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean whereever they are, use the get_user_location tool to find their location."""
#
# from langchain_core.tools import tool
#
# def get_weather_for_location(city: str) -> str:  # (1)!
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"
#
# from langchain_core.runnables import RunnableConfig
#
# USER_LOCATION = {
#     "1": "Florida",
#     "2": "SF"
# }
#
# @tool
# def get_user_location(config: RunnableConfig) -> str:
#     """Retrieve user information based on user ID."""
#     user_id = config["context"].get("user_id")
#     return USER_LOCATION[user_id]
#
# from langchain.chat_models import init_chat_model
#
# model = init_chat_model(
#     "anthropic:claude-3-7-sonnet-latest",
#     temperature=0
# )
#
# from dataclasses import dataclass
#
# @dataclass
# class WeatherResponse:
#     conditions: str
#     punny_response: str
#
# from langgraph.checkpoint.memory import InMemorySaver
#
# checkpointer = InMemorySaver()
#
# tool_node = ToolNode(
#     tools=[get_user_location, get_weather_for_location],
#     handle_tool_errors="Please check your input and try again."
# )
# agent = create_agent(
#     model=model,
#     prompt=system_prompt,
#     tools=tool_node,
#     response_format=WeatherResponse,
#     checkpointer=checkpointer
# )
#
# config = {"configurable": {"thread_id": "1"}}
# context = {"user_id": "1"}
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
#     config=config,
#     context=context
# )
#
# response['structured_response']
#
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "thank you!"}]},
#     config=config,
#     context=context
# )
#
# response['structured_response']