import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# pip install langchain-openai langchain langchain-core

# 初始化 LLM，指向本地网关
llm = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)


# ================================
# 1. 定义工具：用 @tool 装饰普通函数即可
#    docstring 会作为说明，帮助模型判断何时调用
# ================================
@tool
def get_weather(city: str) -> str:
    """查询指定城市的实时天气（现实中应调用气象 API）。"""
    fake_db = {"武汉": "晴，28℃，微风", "北京": "多云，22℃", "上海": "小雨，25℃"}
    return fake_db.get(city, f"{city}：暂无数据")


@tool
def add(a: float, b: float) -> float:
    """计算两个数字之和。"""
    return a + b


# ================================
# 2. 绑定工具，让模型可以决定调用哪个
# ================================
tools = {"get_weather": get_weather, "add": add}
llm_with_tools = llm.bind_tools(list(tools.values()))


# ================================
# 3. 执行：模型先判断是否调用工具，再用结果生成回答
# ================================
def run(user_query: str) -> str:
    messages = [("user", user_query)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    if not ai_msg.tool_calls:
        return ai_msg.content

    # 依次执行模型请求的工具，并把结果回填
    for call in ai_msg.tool_calls:
        result = tools[call["name"]].invoke(call["args"])
        messages.append({"role": "tool", "content": str(result), "tool_call_id": call["id"]})

    return llm_with_tools.invoke(messages).content


if __name__ == "__main__":
    print(run("武汉今天天气怎么样？"))
    print(run("帮我算一下 23 加 19 等于多少"))
