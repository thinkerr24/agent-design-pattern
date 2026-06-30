import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 异常处理与恢复 (Exception Handling & Recovery)：失败重试 + 降级回退
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)


def ask_safe(q: str, retries: int = 2) -> str:
    for i in range(retries):
        try:
            return llm.invoke(q).content
        except Exception as e:
            print(f"第{i+1}次失败：{e}")
    return "服务暂不可用，请稍后再试（降级回复）"  # 回退


if __name__ == "__main__":
    print(ask_safe("用一句话解释什么是缓存"))
