import json

from my_code.chapter4.llm_client import LLMClient

PLAN_PROMPT = """
你是一个非常有经验的规划专家，你的任务是将用户提出的问题，分解成一个由多个简单步骤组成的行动计划。
你需要确保每个步骤都是一个独立、可执行的子任务，并且需要严格按照逻辑顺序排列。
你的输出必须是一个列表对象，对象中的每个元素都是一个描述子任务的字符串。

那么现在开始！
"""

class PlanAgent:

    def __init__(self, client: LLMClient):
        self.client = client

    def plan(self, question: str) -> list[str]:
        """根据用户提问，得到后续行动计划"""

        messages = [
            {"role": "system", "content": PLAN_PROMPT},
            {"role": "user", "content": question}
        ]

        plan = self.client.answer(messages=messages)

        if not plan:
            raise Exception("❌规划行动计划失败！")

        print(f"成功规划行动计划：\n{plan}")

        return json.loads(plan)