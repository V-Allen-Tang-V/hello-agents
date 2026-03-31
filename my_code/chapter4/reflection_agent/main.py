from my_code.chapter4.llm_client import LLMClient
from my_code.gloable_config import SETTINGS
from my_code.chapter4.reflection_agent.reflection_agent import ReflectionAgent

if __name__ == "__main__":
    client = LLMClient(
        model=SETTINGS["MODEL_NAME"],
        base_url=SETTINGS["BASE_URL"],
        api_key=SETTINGS["API_KEY"],
    )

    reflection_agent = ReflectionAgent(client=client)

    while True:
        print("请输入您的需求：")
        user_prompt = input()

        if user_prompt.strip() == "" or user_prompt.strip().lower() == "exit":
            print("再见...")
            break

        final_code = reflection_agent.reflect(user_prompt)
        print(f"【最终的代码】：\n{final_code}\n")