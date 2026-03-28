import os
from agent import react_agent

MODEL_NAME = "Qwen/Qwen3.5-27B"
MODELSCOPE_BASE_URL = "https://api-inference.modelscope.cn/v1/"
API_KEY = os.environ.get("MODELSCOPE_SDK_TOKEN")

if __name__ == "__main__":
    print("请输入你的需求：")
    user_prompt = input()
    react_agent(user_prompt, MODEL_NAME, MODELSCOPE_BASE_URL, API_KEY)