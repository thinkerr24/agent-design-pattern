import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 智能体间通信 (Agent-to-Agent)：两个智能体多轮对话协作
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

msg = "我想学做菜，预算100元。"
for i in range(2):  # 顾问与采购来回沟通
    plan = llm.invoke(f"你是美食顾问，给出建议（一句话）：{msg}").content
    msg = llm.invoke(f"你是采购，回应顾问的需求并报价（一句话）：{plan}").content
    print(f"轮{i+1}：{plan} -> {msg}")
