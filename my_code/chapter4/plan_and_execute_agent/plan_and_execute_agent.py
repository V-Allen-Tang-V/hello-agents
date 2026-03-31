from my_code.chapter4.llm_client import LLMClient
from plan_agent import PlanAgent
from execute_agent import ExecuteAgent

class PlanAndExecuteAgent:

    def __init__(self, client: LLMClient):
        self.client = client
        self.plan_agent = PlanAgent(client)
        self.execute_agent = ExecuteAgent(client)


    def run_agent(self, question: str) -> None:
        plan = self.plan_agent.plan(question)

        final_answer = self.execute_agent.execute_plan(question, plan)
        print(final_answer)