### 一、核心流程类 (Core Patterns)
1. <font color="red">[提示链 (Prompt Chaining)](prompt-chain.py)</font>

模式名称：提示链（Prompt Chaining），也称为流水线（Pipeline）模式。
动机：单一、复杂的提示在处理多步骤任务时，容易导致大型语言模型（LLM）出现忽略指令、丢失上下文、错误累积、上下文窗口不足或产生幻觉（不准确信息）等问题。需要通过一种方法来提升复杂任务处理的可靠性和可控性。

#### 转的好处
<ul>
	<li>降低对模型的要求</li>
	<li>消除智能体的黑箱，让中间结果可见</li>
	<li>灵活配置</li>
	<li>不同的阶段使用不同的模型</li>
</ul>
2. <font color="red">[路由 (Routing)](routing.py)</font>
n选1<br/>
动机：
- 现实中的智能体系统需要根据环境状态、用户输入或前序操作结果等因素，在多个潜在动作之间进行决策。
- 使系统能够根据特定条件将控制流导向不同的专用函数、工具或子流程。

优点：使系统从固定执行路径转变为动态评估的灵活模式，实现更灵活、具备上下文感知的系统行为；能够开发出更具适应性的执行流，动态响应更广泛的输入和状态变化；将智能体从静态执行者转变为能根据变化条件做出决策的动态系统。

3. <font color="red">[并行化 (Parallelization)](parallelization.py)</font>
n走n<br/>
动机：许多复杂的智能体任务包含多个可以同时执行的独立子任务。纯串行执行（每一步等待前一步完成）效率低下，尤其在依赖外部 I/O（如 API 调用、数据库查询）时，整体耗时过长，严重影响系统性能和响应速度。

优点：
- 显著提升效率：通过并发执行独立任务，大幅缩短整体延迟，使系统更具响应性。
- 优化资源利用：在等待外部服务响应时，可以同时处理其他任务。

4. <font color="red">[反思 (Reflection)](reflection.py)</font>
让大模型评价代码的难度低于生成一段好代码<br/>
反思->迭代<br/>
动机：智能体的初始输出或计划可能不理想、不准确或不完整，基础工作流缺乏自我纠错机制，因此需要一种自我改进机制来提升输出质量和适应性。

优势：显著提升输出质量、准确性、一致性和复杂性处理能力；使智能体具备自我意识和适应性。

问题：增加延迟、计算成本（更多 LLM 调用）和内存消耗；不适合实时性要求高的场景。

5. [工具使用 (Tool Use)](tool-use.py)

### 二、进阶能力类 (Advanced Patterns)
6. [规划 (Planning)](planning.py)
7. [多智能体协作 (Multi-Agent Collaboration)](multi-agent.py)
8. [记忆管理 (Memory Management)](memory.py)
9. [学习与适应 (Learning & Adaptation)](learning.py)
10. [模型上下文协议 (Model Context Protocol)](mcp.py)

### 三、系统保障类 (System Patterns)
11. [目标设定与监控 (Goal Setting & Monitoring)](goal-monitoring.py)
12. [异常处理与恢复 (Exception Handling & Recovery)](exception-handling.py)
13. [人类参与环节 (Human-in-the-Loop)](human-in-loop.py)
14. [知识检索 (RAG, Retrieval-Augmented Generation)](rag.py)
15. [智能体间通信 (Agent-to-Agent)](agent-to-agent.py)

### 四、优化与治理类 (Optimization Patterns)
16. [资源感知优化 (Resource-Aware Optimization)](resource-aware.py)
17. [推理技术 (Reasoning Techniques)](reasoning.py)
18. <font color="red">[护栏与安全模式 (Guardrails & Safety Patterns)](safe.py)</font>

动机：
- 智能体（AI Agent）日益自主并集成到关键系统中，存在生成有害、偏见、无关或其他不良响应的风险。
- 需要确保智能体运行稳健、可信且有益，降低风险，维护用户信任，防止对用户、组织及 AI 系统声誉造成损害。
- 动机是构建负责任的 AI 系统，确保行为符合伦理与法律标准。

19. [评估与监控 (Evaluation & Monitoring)](evaluation.py)

### 五、战略策略类 (Strategic Patterns)
20. [优先级排序 (Prioritization)](prioritization.py)
21. [探索与发现 (Exploration & Discovery)](exploration.py)