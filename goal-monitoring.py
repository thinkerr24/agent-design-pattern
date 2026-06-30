import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 目标设定与监控 (Goal Setting & Monitoring)：循环执行直到达成目标或超限
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

GOAL = "把口号压缩到10字以内"
text = "我们提供全天候极速可靠的优质配送服务"

for i in range(3):  # 监控：最多3轮
    text = llm.invoke(f"目标：{GOAL}。改写：{text}").content.strip()
    print(f"第{i+1}轮：{text}")
    if len(text) <= 10:  # 达成判定
        print("目标达成")
        break
