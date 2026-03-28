import re
from client import OpenAIClient
from system_prompt import SYSTEM_PROMPT
from tools import AVAILABLE_TOOLS

def react_agent(user_prompt: str, model_name: str, base_url: str, api_key: str) -> None:
    """ReAct Agent实现"""

    client = OpenAIClient(
        model=model_name,
        base_url=base_url,
        api_key=api_key
    )

    # 对话栈
    conversations_history = [f"用户输入：{user_prompt}"]
    # 最大循环次数
    max_iterations = 5
    times = 1

    # 进入ReAct循环
    while times <= max_iterations:
        print(f"----第 {times} 次循环---")

        try:
            # 获取llm回答的结果
            llm_answer = client.query_llm(system_prompt=SYSTEM_PROMPT, user_prompt="\n".join(conversations_history))
            print(llm_answer + "\n")
        except Exception as e:
            print(f"错误：调用大语言模型时出错 - {e}")
            break

        # 提取Thought标签内容
        thought_match = re.search(r'<Thought>(.*?)</Thought>', llm_answer, re.DOTALL)
        thought_answer = thought_match.group(1).strip() if thought_match else None
        # 提取Action标签内容
        action_match = re.search(r'<Action>(.*?)</Action>', llm_answer, re.DOTALL)
        action_answer = action_match.group(1).strip() if action_match else None

        conversations_history.append(llm_answer)

        print(f"Thought: {thought_answer}")

        observation_str = ""
        # 排查Action标签是否符合格式
        if action_answer is None:
            observation_str += "错误：未解析到Action标签。请你的回答严格遵循'<Thought>...</Thought><Action>...</Action>'的格式"
        # 检查Action标签是否为Finish
        elif action_answer.startswith("Finish"):
            final_answer = re.match(r"Finish\[(.*)\]", action_answer, re.DOTALL)
            print(f"任务完成，最终答案：{final_answer.group(1)}")
            break
        else:
            try:
                # 检查Action标签中的工具名是否能正确调用
                tool_name = re.search(r"(\w+)\(", action_answer).group(1)
                args_str = re.search(r"\((.*)\)", action_answer).group(1)
                kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

                if tool_name in AVAILABLE_TOOLS:
                    tool_func = AVAILABLE_TOOLS[tool_name]
                    observation_str += tool_func(**kwargs)
                else:
                    observation_str += f"错误：未找到对应工具：{tool_name}"
            except Exception as e:
                observation_str += f"错误：解析或执行工具时出错 - {e}"

        print(f"观察结果：{observation_str}\n")
        conversations_history.append(f"观察结果：{observation_str}")
        times += 1

    if times > max_iterations:
        print("达到最大循环次数，任务未完成")
