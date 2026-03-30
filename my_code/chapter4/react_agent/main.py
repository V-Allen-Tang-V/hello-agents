from tool_executor import ToolExecutor
from tools import AVAILABLE_TOOLS
from react_agent import ReActAgent
from my_code.chapter4.llm_client import LLMClient
from my_code.gloable_config import SETTINGS

if __name__ == "__main__":

    tool_executor = ToolExecutor()
    # 注册tool
    for tool in AVAILABLE_TOOLS:
        tool_executor.tool_register(
            tool_name=tool["name"],
            args=tool["args"],
            tool_desc=tool["description"],
            func=tool["func"]
        )

    llm_client = LLMClient(
        model=SETTINGS["MODEL_NAME"],
        base_url=SETTINGS["BASE_URL"],
        api_key=SETTINGS["API_KEY"],
    )

    agent_client = ReActAgent(
        client=llm_client,
        tool_executor=tool_executor,
    )
    print(str(agent_client.available_tools))

    while True:
        print("请输入您的需求：")
        user_prompt = input()

        if user_prompt.strip() == "" or user_prompt.strip().lower() == "exit":
            print("再见...")
            break

        agent_client.start(user_prompt)