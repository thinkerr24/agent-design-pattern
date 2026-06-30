import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 知识检索 (RAG)：先从知识库检索相关片段，再带上下文作答
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

DOCS = [
    "营业时间：每天9:00-22:00。",
    "会员积分1元1分，满100分抵5元。",
    "退货政策：7天无理由退货。",
]


def retrieve(q: str) -> str:
    # 简化检索：关键词命中（现实中用向量相似度）
    return "\n".join(d for d in DOCS if any(k in d for k in q)) or "无相关资料"


if __name__ == "__main__":
    q = "积分怎么用"
    print(llm.invoke(f"资料：\n{retrieve(q)}\n问题：{q}").content)
