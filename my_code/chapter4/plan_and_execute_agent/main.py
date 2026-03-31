from my_code.chapter4.llm_client import LLMClient
from my_code.chapter4.plan_and_execute_agent.plan_and_execute_agent import PlanAndExecuteAgent
from my_code.gloable_config import SETTINGS

if __name__ == '__main__':

    llm_client = LLMClient(
        model=SETTINGS["MODEL_NAME"],
        base_url=SETTINGS["BASE_URL"],
        api_key=SETTINGS["API_KEY"],
    )

    PE_agent = PlanAndExecuteAgent(llm_client)

    while True:
        print("请输入您的需求：")
        user_prompt = input()

        if user_prompt.strip() == "" or user_prompt.strip().lower() == "exit":
            print("再见...")
            break

        PE_agent.run_agent(user_prompt)