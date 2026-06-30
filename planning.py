import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# pip install langchain-openai langchain langchain-core

# 规划 (Planning)：先让模型拆解任务为步骤计划，再逐步执行
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

planner = (
    ChatPromptTemplate.from_template("请把目标拆解为不超过5个可执行步骤，每行一个：\n{goal}")
    | llm | StrOutputParser()
)
executor = (
    ChatPromptTemplate.from_template("按以下计划完成任务，给出最终结果：\n计划：\n{plan}\n目标：{goal}")
    | llm | StrOutputParser()
)

if __name__ == "__main__":
    goal = "为一家奶茶店策划一场周末促销活动"
    plan = planner.invoke({"goal": goal})
    print("计划：\n", plan)
    print("\n执行结果：\n", executor.invoke({"goal": goal, "plan": plan}))
