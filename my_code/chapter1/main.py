from agent import react_agent
from ..gloable_config import SETTINGS

if __name__ == "__main__":
    print("请输入你的需求：")
    user_prompt = input()
    react_agent(
        user_prompt,
        SETTINGS["MODEL_NAME"],
        SETTINGS["BASE_URL"],
        SETTINGS["API_KEY"]
    )