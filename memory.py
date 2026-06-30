import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# pip install langchain-openai langchain langchain-core

# 记忆管理 (Memory Management)：用历史消息列表维持多轮上下文
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

history = []


def chat(text: str) -> str:
    history.append(HumanMessage(text))
    reply = llm.invoke(history).content
    history.append(AIMessage(reply))
    return reply


if __name__ == "__main__":
    print(chat("我叫小明。"))
    print(chat("我叫什么名字？"))  # 依赖记忆作答
