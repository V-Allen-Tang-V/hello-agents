from my_code.chapter4.llm_client import LLMClient

EXECUTE_PROMPT_TEMPLATE = """
你是一位顶级的执行专家。你的任务是严格按照给定的计划，一步步解决问题。
你将收到：原始问题、完整计划、以及到目前位置已经完成的步骤和结果。
你需要专注解决当【当前步骤】，并仅输出该步骤的答案，不需要额外的解释和对话。

【原始问题】
{question}

【完整计划】
{plan}

【历史步骤的完成结果】
{history}

【当前步骤】
{current_step}
"""

class ExecuteAgent:

    def __init__(self, client: LLMClient):
        self.client = client


    def execute_plan(self, question: str, plan: list[str]) -> str:
        """根据规划执行行动计划的每一个步骤"""

        plan_str = str(plan)
        history = []
        final_answer = ""

        for current_step in plan:

            print(f"当前执行的步骤：\n{current_step}")

            execute_prompt = EXECUTE_PROMPT_TEMPLATE.format(
                question=question,
                plan=plan_str,
                history=str(history),
                current_step=current_step
            )

            messages = [
                {"role": "system", "content": execute_prompt},
            ]

            llm_response = self.client.answer(messages=messages)

            print(f"执行结果：\n{llm_response}\n")

            history.append({
                "step": current_step,
                "execute_result": llm_response
            })
            final_answer = llm_response
        
        return final_answer
