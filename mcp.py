import os
from langchain_openai import ChatOpenAI

# pip install langchain-openai langchain langchain-core

# 模型上下文协议 (MCP)：用统一接口暴露资源/工具给模型。此处模拟一个最小资源服务
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

# 模拟 MCP server 提供的资源
RESOURCES = {"doc://policy": "退款需在7天内，保留小票。"}


def get_resource(uri: str) -> str:
    return RESOURCES.get(uri, "资源不存在")


if __name__ == "__main__":
    ctx = get_resource("doc://policy")  # 客户端读取资源，注入上下文
    print(llm.invoke(f"依据政策：{ctx}\n问题：买了5天能退吗？").content)
