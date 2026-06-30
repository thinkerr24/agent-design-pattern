import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 探索与发现 (Exploration & Discovery)：发散生成多个新点子供后续筛选
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

if __name__ == "__main__":
    print(llm.invoke("围绕'校园咖啡店'头脑风暴5个新颖卖点，越大胆越好").content)
