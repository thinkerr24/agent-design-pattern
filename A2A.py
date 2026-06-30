import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 初始化大模型实例（共用同一个大脑，但赋予不同的系统提示词）
llm = ChatOpenAI(
    model="gpt-5.4",
    base_url="http://127.0.0.1:3030/v1",  # 替换为本地网关地址
    api_key="any-string-is-ok"            # 替换为网关要求的任意字符串
)

# ==========================================
# 2. 定义角色 1：产品经理智能体 (PM Agent)
# ==========================================
pm_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位严谨的产品经理。请将用户的口头需求，转化为包含【核心组件】和【核心参数】的结构化产品规格说明书。"),
    ("human", "原始需求：{user_input}")
])
pm_agent = pm_prompt | llm | StrOutputParser()

# ==========================================
# 3. 定义角色 2：后端开发智能体 (Coder Agent)
# ==========================================
coder_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位精通数据结构的前端/后端开发专家。请接收产品经理发给你的产品规格说明书，并将其严格转换为标准 JSON 格式。除了纯 JSON 外，不要附带任何解释文字。"),
    ("human", "产品经理的规格书：{pm_specs}")
])
coder_agent = coder_prompt | llm | StrOutputParser()

# ==========================================
# 4. 协同编排（Agent-to-Agent 管道）
# ==========================================
# 这里利用 RunnablePassthrough 或字典字典映射，让 pm_agent 的输出直接挂载到 coder_agent 的输入参数 pm_specs 上
a2a_workflow = (
    {"pm_specs": pm_agent}  # 触发第一个 Agent，并将结果存入 pm_specs
    | coder_agent           # 将数据流传递给第二个 Agent 
)

# ==========================================
# 5. 启动智能体协同流程
# ==========================================
if __name__ == "__main__":
    print("🚀 正在启动 A2A 协同工作流...\n")
    
    user_query = "我想做个高配笔记本，CPU要是3.5GHz的，内存搞个16G，硬盘越大越好。"
    
    # 一键唤醒两个智能体接力工作
    final_output = a2a_workflow.invoke({"user_input": user_query})
    
    print("==== 最终智能体协同输出 (JSON) ====")
    print(final_output)