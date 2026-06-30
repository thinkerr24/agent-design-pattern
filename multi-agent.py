import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# pip install langchain-openai langchain langchain-core

# 多智能体协作 (Multi-Agent Collaboration)：不同角色分工，串行接力完成
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

writer = ChatPromptTemplate.from_template("你是文案，写一段{topic}的产品介绍，50字内。") | llm | StrOutputParser()
editor = ChatPromptTemplate.from_template("你是编辑，润色并指出一个改进点：\n{draft}") | llm | StrOutputParser()

if __name__ == "__main__":
    draft = writer.invoke({"topic": "智能水杯"})
    print("文案：", draft)
    print("编辑：", editor.invoke({"draft": draft}))
