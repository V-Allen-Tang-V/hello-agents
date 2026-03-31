from my_code.chapter4.llm_client import LLMClient
from memory import Memory, RecordType

INITIAL_PROMPT_TEMPLATE = """
你是一位资深的Python程序员，请根据以下要求，编写一个Python函数。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。

要求：
{question}

请直接输出代码，不要包含任何额外内容。
"""

REFLECT_PROMPT_TEMPLATE = """
你是一位要求严格的代码审查专家和资深算法工程师，对代码的性能和美观有极致的要求。
你的任务是审查以下Python代码，并优化代码，专注于找出在算法效率上的主要瓶颈。

原始要求：
{question}

待审查的代码：
{code}

请分析该代码的时间复杂度，并思考是否存在一种算法上更优的解法来提升性能。
若存在，请清晰指出该算法的不足，并提出具体的改进措施。
若代码在算法层面勿需改进，只能回答"无需改进"。

请直接输入你的反馈，不要包含任何额外内容。
"""

REFINE_PROMPT_TEMPLATE = """
你是一位资深的Python程序员，你正在根据一位评审专家的反馈来优化代码。

原始要求：
{question}

上一轮尝试：
{last_attempt}

评审员反馈：
{feedback}

请你结合原始要求、上一轮尝试、以及评审员的反馈，生成一个优化后的新版本。
代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。
请直接输出优化后的代码，不要包含任何额外内容。
"""

class ReflectionAgent:

    def __init__(self, client: LLMClient, max_iterations: int = 5):
        self.client = client
        self.memory = Memory()
        self.max_iterations = max_iterations


    def reflect(self, question: str) -> str:
        init_prompt = INITIAL_PROMPT_TEMPLATE.format(question=question)
        init_message = [
            {"role": "system", "content": init_prompt}
        ]
        code_response = self.client.answer(init_message)

        for iteration in range(self.max_iterations):
            print(f"【代码结果】：\n{code_response}\n")
            self.memory.add_memory(RecordType.EXECUTE, code_response)

            print(f"---第{iteration + 1}次迭代---")

            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(
                question=question,
                code=code_response
            )
            reflect_message = [{
                "role": "system", "content": reflect_prompt
            }]
            # 产生反思结果
            reflect_response = self.client.answer(reflect_message)
            print(f"【反思结果】：\n{reflect_response}\n")

            self.memory.add_memory(RecordType.REFLECT, reflect_response)

            if "无需改进" in reflect_response:
                break

            # 优化
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                question=question,
                last_attempt=self.memory.last_execute,
                feedback=reflect_response
            )
            refine_message = [
                {"role": "system", "content": refine_prompt}
            ]
            # 产生优化结果
            code_response = self.client.answer(refine_message)

        return code_response