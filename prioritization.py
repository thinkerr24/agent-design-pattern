import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 优先级排序 (Prioritization)：让模型按紧急/重要度排序任务
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

if __name__ == "__main__":
    tasks = ["回复邮件", "服务器宕机修复", "整理桌面", "提交季度报告"]
    print(llm.invoke(f"按紧急重要程度排序并说明理由：{tasks}").content)
