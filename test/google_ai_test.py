import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_API_KEY"] = "AIzaSyB8-MZdYkN_OCtdj3OUP7UmoSzE3YSr4lc"
#
# from google.api_core.client_options import ClientOptions
# from google.ai.generativelanguage_v1beta.services.model_service import ModelServiceClient
#
# # 从环境变量读取 API Key，避免硬编码
# API_KEY = os.environ.get("GOOGLE_API_KEY")
# if not API_KEY:
#     raise RuntimeError("请先在环境变量中设置 GOOGLE_API_KEY")
#
# # 使用 REST 传输，避免 gRPC 被墙/不走代理的问题
# client = ModelServiceClient(
#     transport="rest",
#     client_options=ClientOptions(api_key=API_KEY),
# )
#
# # 列出模型（加超时，避免长时间卡住）
# for m in client.list_models(timeout=30):
#     print(m.name, m.supported_generation_methods)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",      # 使用已验证可用的模型名
    temperature=0,
    max_output_tokens=128,         # 使用正确参数名
    timeout=30,
    max_retries=2,
    # 不要传 proxy=""，避免覆盖环境变量导致不走代理
)

messages = [
    SystemMessage(content="You are a helpful assistant that translates English to Chinese. Translate the user sentence."),
    HumanMessage(content="I love programming."),
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)