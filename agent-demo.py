import re
import json
from openai import OpenAI

# 1. 初始化客户端（指向你本地的网关）
client = OpenAI(
    base_url="http://127.0.0.1:3030/v1", 
    api_key="any-string-is-ok" 
)

# 2. 定义 Agent 的“双手”（工具函数）
def get_user_balance(user_name: str) -> str:
    """查询用户余额的工具"""
    db = {"张三": 100, "李四": 250, "王五": 1200}
    # 去除大模型可能多包的引号
    clean_name = user_name.strip("'\"")
    balance = db.get(clean_name, 0)
    return f"【系统回复：{clean_name} 的余额是 {balance} 元】"

# 3. 编写思维模板（System Prompt）
SYSTEM_PROMPT = """
你是一个带有工具使用能力的 AI 助手。你必须通过思考和调用工具来回答问题。

你目前拥有的工具：
- get_user_balance("用户名"): 传入用户名，返回该用户的余额。

当收到用户问题后，你必须严格按照以下格式输出，每次只输出一步，不要自己编造数据：

Thought: 思考你当前需要做什么，下一步需要什么信息。
Action: 决定要调用的工具，格式必须是：工具名("参数")。如果没有必要调用工具，直接进入 Final Answer。
Observation: （这一步你不需要写，系统执行完工具后会把结果喂给你）

当你收集到了足够的信息，请输出最终答案：
Final Answer: 最终的回答。
"""

# 4. 核心的 Agent 运行循环
def run_agent(user_question: str):
    print(f"🚀 用户问题: {user_question}\n" + "="*50)
    
    # 初始化记忆（对话历史）
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]
    
    # 限制最大思考轮数，防止死循环
    max_turns = 5
    
    for turn in range(max_turns):
        print(f"\n🧠 [第 {turn + 1} 轮思考...]")
        
        # 让大模型决策
        response = client.chat.completions.create(
            model="gpt-5.4",  # 这里填你本地网关实际支持的模型名称，如 qwen, llama 等
            messages=messages,
            temperature=0.0  # 设为0，让推理逻辑更稳定、更确定
        )
        
        llm_output = response.choices[0].message.content
        print(llm_output)
        
        # 将大模型的思考过程存入短期记忆
        messages.append({"role": "assistant", "content": llm_output})
        
        # 检查是否达成最终答案
        if "Final Answer:" in llm_output:
            print("\n✅ 任务完成！")
            break
            
        # 检查是否需要触发工具
        if "Action:" in llm_output:
            # 使用正则表达式提取 Action: 工具名("参数")
            match = re.search(r"Action:\s*(\w+)\((.*?)\)", llm_output)
            if match:
                tool_name = match.group(1)
                tool_arg = match.group(2)
                
                # 匹配并执行对应的本地 Python 函数
                if tool_name == "get_user_balance":
                    # 执行工具（获取外部世界的数据）
                    observation = get_user_balance(tool_arg)
                    print(f"\n⚙️ 正在执行本地工具... -> {observation}")
                    
                    # 把观察到的结果（Observation）作为下一轮的用户输入喂回给模型
                    messages.append({"role": "user", "content": f"Observation: {observation}"})
                else:
                    error_msg = f"Observation: 错误：找不到名为 {tool_name} 的工具。"
                    messages.append({"role": "user", "content": error_msg})
            else:
                # 输出了 Action 但格式不对，提醒模型修正
                messages.append({"role": "user", "content": "Observation: 格式错误。请严格按照 Action: 工具名(\"参数\") 的格式提出请求。"})
    else:
        print("\n❌ 达到最大思考轮数，Agent 未能完成任务。")

# 5. 测试运行
if __name__ == "__main__":
    run_agent("帮我查一下李四和张三谁的钱更多？")