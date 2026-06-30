import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 评估与监控 (Evaluation & Monitoring)：用模型给另一回答打分
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

if __name__ == "__main__":
    answer = llm.invoke("用一句话介绍长城").content
    score = llm.invoke(f"给以下回答的准确性打1-5分并说明：\n{answer}").content
    print("回答：", answer)
    print("评估：", score)
