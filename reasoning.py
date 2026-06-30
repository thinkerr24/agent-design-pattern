import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 推理技术 (Reasoning)：思维链，引导模型分步推理后给出答案
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

if __name__ == "__main__":
    q = "鸡兔同笼，共8头26脚，各几只？请分步推理再给结论。"
    print(llm.invoke(q).content)
