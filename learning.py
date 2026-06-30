import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# pip install langchain-openai langchain langchain-core

# 学习与适应 (Learning & Adaptation)：把过往反馈作为示例注入提示，改进后续输出
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

lessons = []  # 累积的经验

chain = ChatPromptTemplate.from_template(
    "经验教训：\n{lessons}\n\n请回答：{q}"
) | llm | StrOutputParser()


def ask(q: str) -> str:
    return chain.invoke({"lessons": "\n".join(lessons) or "无", "q": q})


if __name__ == "__main__":
    print(ask("用一句话介绍咖啡"))
    lessons.append("用户偏好：回答需附带一个冷知识")
    print(ask("用一句话介绍咖啡"))  # 适应新偏好
