import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# pip install langchain-openai langchain langchain-core

# 初始化 LLM，指向本地网关
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url="http://127.0.0.1:3030/v1",  # 替换为本地网关地址
    api_key="any-string-is-ok"            # 替换为网关要求的任意字符串
)
# 1. 定义每个步骤的独立处理链
extraction_chain = (
    ChatPromptTemplate.from_template("请从以下文本中提取技术规格：\n\n{text_input}")
    | llm
    | StrOutputParser()
)

# 2. 构建完整提示链（前一步输出作为下一步输入）
full_chain = (
    {"specifications": extraction_chain}  # 第一步输出传递给第二步
    | ChatPromptTemplate.from_template("请将以下技术规格转为JSON：\n\n{specifications}")
    | llm
    | StrOutputParser()
)

# 3. 执行链式调用 (基于图片1)
result = full_chain.invoke({"text_input": "笔记本配备3.5GHz处理器、16GB内存"})
print(result)