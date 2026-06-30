import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 资源感知优化 (Resource-Aware Optimization)：按任务难度选择不同成本的模型
cheap = ChatOpenAI(model="gpt-5.4-mini", base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"), api_key=os.getenv("OPENAI_API_KEY", "placeholder-key"))
strong = ChatOpenAI(model="gpt-5.4", base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"), api_key=os.getenv("OPENAI_API_KEY", "placeholder-key"))


def ask(q: str) -> str:
    model = strong if len(q) > 20 else cheap  # 简单问题用便宜模型
    print(f"使用模型：{model.model_name}")
    return model.invoke(q).content


if __name__ == "__main__":
    print(ask("1+1=?"))
    print(ask("请详细解释什么是区块链以及它的核心优势"))
