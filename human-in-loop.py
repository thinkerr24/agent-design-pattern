import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 人类参与环节 (Human-in-the-Loop)：高风险操作前需人工确认
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

if __name__ == "__main__":
    draft = llm.invoke("写一封给客户的退款拒绝邮件，简短").content
    print("草稿：\n", draft)
    if input("是否发送？(y/n) ").lower() == "y":
        print("已发送")
    else:
        print("已取消，转人工处理")
