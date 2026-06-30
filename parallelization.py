import asyncio
import os
from openai import RateLimitError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# pip install langchain-openai langchain langchain-core

# 初始化 LLM，指向本地网关
llm = ChatOpenAI(
	model="gpt-5.4",
	base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:3030/v1"),
	api_key=os.getenv("OPENAI_API_KEY", "placeholder-key")
)

# ================================
# 定义 3 个独立并行任务链（完善提示词模板）
# ================================

# 任务1：生成主题摘要（简洁概括核心信息）
summarize_chain = (
	ChatPromptTemplate.from_messages([
		("system", "你是专业的摘要助手，用 200 字以内概括主题的核心发展历程、关键节点和重要意义，语言精炼。"),
		("user", "请概括以下主题：{input}")
	])
	| llm
	| StrOutputParser()
)

# 任务2：生成相关核心问题（启发思考，覆盖关键维度）
questions_chain = (
	ChatPromptTemplate.from_messages([
		("system", "基于主题生成 5 个核心问题，覆盖背景、关键技术、现状、挑战、未来趋势，问题要具体、有深度、不重复。"),
		("user", "请围绕以下主题生成核心问题：{input}")
	])
	| llm
	| StrOutputParser()
)

# 任务3：提取关键术语（标注定义，便于理解）
terms_chain = (
	ChatPromptTemplate.from_messages([
		("system", "提取主题相关的 8-10 个关键术语或概念。每个术语后用 1 句话简要解释其含义，格式为“术语：解释”。"),
		("user", "请提取以下主题的关键术语：{input}")
	])
	| llm
	| StrOutputParser()
)

# ================================
# 5. 聚合并行结果，生成最终报告
# ================================
report_chain = (
	ChatPromptTemplate.from_template(
		"""
请以 Markdown 格式输出一份完整报告，不要输出说明语、前言、思考过程、任务完成提示，也不要只回复“已整理完成”之类的摘要句。

请以「{topic}」为主题，结合以下信息生成一份结构清晰、逻辑连贯的报告：

一、核心摘要
{summary}

二、关键术语解析
{key_terms}

三、核心思考问题
{questions}

报告要求：
1. 结构分点明确（保留一、二、三级标题）；
2. 语言正式、流畅，无语法错误；
3. 信息完整，不遗漏关键内容；
4. 总字数控制在 800-1000 字。
5. 直接输出 Markdown 正文，使用 #、##、### 标题和普通段落/列表。
6. 第一行必须是一级标题：# {topic}
"""
	)
	| llm
	| StrOutputParser()
)


async def invoke_with_retry(chain, payload, retries: int = 3):
	"""统一处理网关限流重试。"""
	for attempt in range(retries):
		try:
			return await chain.ainvoke(payload)
		except RateLimitError:
			if attempt == retries - 1:
				raise
			await asyncio.sleep(2 * (attempt + 1))


async def invoke_with_semaphore(chain, payload, semaphore: asyncio.Semaphore):
	"""限制并发度，避免本地网关拒绝过多同时请求。"""
	async with semaphore:
		return await invoke_with_retry(chain, payload)


# ================================
# 7. 异步执行并行任务（核心：提升效率，3 个任务同时运行）
# ================================
async def run_parallel_chain(topic: str) -> str:
	"""异步执行并行链，返回最终报告。"""
	semaphore = asyncio.Semaphore(2)

	summary_task = invoke_with_semaphore(summarize_chain, {"input": topic}, semaphore)
	questions_task = invoke_with_semaphore(questions_chain, {"input": topic}, semaphore)
	terms_task = invoke_with_semaphore(terms_chain, {"input": topic}, semaphore)

	summary, questions, key_terms = await asyncio.gather(
		summary_task,
		questions_task,
		terms_task
	)

	return await invoke_with_retry(
		report_chain,
		{
			"topic": topic,
			"summary": summary,
			"questions": questions,
			"key_terms": key_terms
		}
	)


target_topic = "太空探索的历史"

print(f"=== 开始生成 [{target_topic}] 报告（并行执行 3 个任务）===")
final_report = asyncio.run(run_parallel_chain(target_topic))

print("\n=== 最终报告 ===")
print("```markdown")
print(final_report)
print("```")
