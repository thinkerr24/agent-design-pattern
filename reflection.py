import os
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# pip install langchain-openai langchain langchain-core

# 初始化 LLM，指向本地网关
llm = ChatOpenAI(
	model="gpt-5.4",
	base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
	api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

# ================================
# 4. 核心配置（任务定义 + 循环终止条件）
# ================================

# 目标任务：明确要生成的代码需求（可根据实际场景修改）
TASK_PROMPT = """
请用 Python 编写一个「文件批量重命名工具」，要求：
1. 功能：遍历指定文件夹下的所有 .txt 文件，按「前缀_序号.txt」格式重命名（如 doc_001.txt、doc_002.txt）；
2. 支持自定义前缀（默认值："file"）和起始序号（默认值：1）；
3. 包含异常处理（如文件夹不存在、无 .txt 文件、文件重命名失败）；
4. 输出日志：打印每个文件的重命名前后路径（成功/失败原因）；
5. 代码结构清晰，包含函数注释和使用示例。
"""

# 循环终止条件：最大迭代次数（避免无限循环）+ 反思关键词
MAX_ITERATIONS = 3  # 最多优化 3 轮，防止过度迭代
PERFECT_FLAG = "CODE_IS_PERFECT"  # 反思通过的标记

# ================================
# 5. 完善反思评估提示词（关键：明确审查维度）
# ================================
REFLECTOR_SYSTEM_PROMPT = """
你是一名资深 Python 软件工程师，负责审查代码是否满足原始任务要求。请按以下维度逐项评估：
1. 功能完整性：是否实现了所有需求（批量重命名、自定义参数、异常处理、日志输出）；
2. 代码正确性：语法是否无误、逻辑是否通顺（如序号递增、文件过滤正确）；
3. 健壮性：异常处理是否全面（文件夹不存在、权限不足、文件被占用等场景）；
4. 易用性：是否有清晰的函数注释、使用示例，参数设置是否合理；
5. 规范性：代码格式整洁、变量命名规范、无冗余代码。

评估结果输出要求：
- 若代码完全满足所有要求，仅输出标记「CODE_IS_PERFECT」，无需任何额外内容；
- 若代码存在问题，分点列出具体缺陷（如「1. 未处理文件夹不存在的异常」「2. 缺少自定义前缀的参数」），并给出明确的修改建议（如「添加 os.path.exists 判断，抛出 ValueError 并提示用户」），无需重写完整代码。
"""


def sanitize_generated_code(content: str) -> str:
	"""提取模型输出中的 Python 代码主体。"""
	match = re.search(r"```(?:python)?\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
	if match:
		return match.group(1).strip()
	return content.strip()


# ================================
# 6. 核心反思循环函数（递归实现迭代优化）
# ================================
def run_reflection_loop(message_history: list, iteration: int = 1) -> tuple[str, list]:
	"""
	反思循环：生成 -> 评估 -> 优化（迭代）-> 终止
	:param message_history: 消息历史（包含任务、之前的代码、反思意见）
	:param iteration: 当前迭代次数
	:return: （最终优化后的代码，完整反思历史）
	"""
	# 终止条件 1：达到最大迭代次数
	if iteration > MAX_ITERATIONS:
		print(f"\n⚠️ 已达到最大迭代次数（{MAX_ITERATIONS} 轮），终止优化")
		last_code = next(msg.content for msg in reversed(message_history) if isinstance(msg, AIMessage))
		return last_code, message_history

	print(f"\n=== 第 {iteration} 轮生成阶段 ===")
	# 1. 初始生成/优化生成：基于消息历史调用大模型
	response = llm.invoke(message_history)
	current_code = sanitize_generated_code(response.content)

	# 将生成的代码加入消息历史（AIMessage 表示模型输出）
	message_history.append(AIMessage(content=current_code))

	print(f"\n=== 第 {iteration} 轮反思评估阶段 ===")
	# 2. 反思评估：传入原始任务 + 当前代码，生成批判意见
	reflector_messages = [
		SystemMessage(content=REFLECTOR_SYSTEM_PROMPT),
		HumanMessage(content=f"原始任务：\n{TASK_PROMPT}\n\n待审查代码：\n{current_code}")
	]
	critique_response = llm.invoke(reflector_messages)
	critique = critique_response.content.strip()
	print(f"反思意见：\n{critique}")

	# 终止条件 2：代码通过评估（包含 PERFECT_FLAG）
	if PERFECT_FLAG in critique:
		print(f"\n✅ 第 {iteration} 轮代码通过评估，终止优化")
		return current_code, message_history

	# 3. 优化迭代：将反思意见加入消息历史，进入下一轮循环
	print(f"\n=== 第 {iteration} 轮优化迭代，进入下一轮 ===")
	message_history.append(HumanMessage(content=f"批判意见：\n{critique}"))
	return run_reflection_loop(message_history, iteration + 1)


# 初始化消息历史：先传入系统提示（代码生成的指导）+ 原始任务
initial_system_prompt = SystemMessage(content="你是一名高效的 Python 开发者，需严格按照用户任务要求编写代码，确保代码可直接运行。只输出完整的 Python 代码，不要解释，不要思考过程，不要 Markdown 代码块。")
initial_human_prompt = HumanMessage(content=TASK_PROMPT)
message_history = [initial_system_prompt, initial_human_prompt]

print("=== 启动反思循环（目标：生成文件批量重命名工具）===")

# 启动反思循环
final_code, reflection_history = run_reflection_loop(message_history)

# 输出最终结果
print("\n" + "=" * 50)
print("=== 最终优化后的代码 ===")
print(final_code)
