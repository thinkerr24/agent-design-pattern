import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

# pip install langchain-openai langchain langchain-core

# 初始化 LLM，指向本地网关
llm = ChatOpenAI(
	model="gpt-5.4",
	base_url="http://127.0.0.1:3030/v1",  # 替换为本地网关地址
	api_key="any-string-is-ok"            # 替换为网关要求的任意字符串
)


def booking_handler(user_query: str) -> str:
	"""处理预订类请求（如预约、下单、挂号等）"""
	# 这里可扩展实际业务逻辑：调用预订接口、查询库存、生成订单等
	return f"📅 预订服务已响应：\n用户请求：{user_query}\n处理结果：已为你创建预订申请，请等待确认（实际场景中会对接预订系统）"


def info_handler(user_query: str) -> str:
	"""处理咨询类请求（如查询信息、了解规则、FAQ 等）"""
	# 这里可扩展实际业务逻辑：查询知识库、调用信息接口、返回常见问题答案等
	return f"ℹ️ 咨询服务已响应：\n用户请求：{user_query}\n处理结果：已为你查询相关信息（实际场景中会返回具体内容，如营业时间、价格详情等）"


def unclear_handler(user_query: str) -> str:
	"""处理意图不明确的请求"""
	return f"❓ 意图未明确：\n用户请求：{user_query}\n请你补充说明需求（例如：预订酒店、查询退款规则等），我会为你精准服务"


def normalize_decision(raw_decision: str) -> str:
	"""将模型输出标准化为固定路由标签。"""
	decision = raw_decision.strip().lower().replace("'", "").replace('"', "")
	if "booker" in decision:
		return "booker"
	if "info" in decision:
		return "info"
	return "unclear"


# 1. 定义路由判断链
coordinator_router_chain = (
	ChatPromptTemplate.from_messages([
		("system", "分析用户请求，判断意图。输出 'booker'、'info' 或 'unclear'。"),
		("user", "{request}")
	])
	| llm
	| StrOutputParser()
)

# 2. 定义分支处理器
branches = {
	"booker": lambda payload: booking_handler(payload["request"]),
	"info": lambda payload: info_handler(payload["request"]),
	"unclear": lambda payload: unclear_handler(payload["request"])
}

# 3. 构建路由分支逻辑
delegation_branch = RunnableBranch(
	(lambda payload: payload["decision"].strip() == "booker", branches["booker"]),
	(lambda payload: payload["decision"].strip() == "info", branches["info"]),
	branches["unclear"]
)

# 4. 组合完整路由智能体
coordinator_agent = (
	{
		"decision": coordinator_router_chain | normalize_decision,
		"request": RunnablePassthrough()
	}
	| delegation_branch
)

result = coordinator_agent.invoke("预订明天的会议室")
print(result)
