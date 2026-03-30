import re
from my_code.chapter4.llm_client import LLMClient
from tool_executor import ToolExecutor

REACT_PROMPT_TEMPLATE = """
你是一个有能力调用外部工具的智能助手，你需要根据你的知识回答用户提出的问题，当你的知识不足以支撑回答用户问题时，需要调用外部工具。

可调用的工具如下：
{tools}

请你的回答严格按照以下格式：
<Thought>你的思考过程，对于问题的分析、拆解和下一步的规划</Thought>
<Action>你决定采取的行动，你可以选择根据自己的知识回答，或调用外部工具后回答。</Action>

Action标签的内容必须是一下格式之一：
- `function_name(arg1="arg_value1", agr2="arg_value2", ...)`：调用一个可用的外部工具；
- `Finish[最终答案]`：当你认为自己已经获得答案时；

# 重要提示:
- 每次只输出一对Thought-Action标签
- Action标签必须在同一行，不要换行

现在，开始解决问题：
"""


def parse_response(response: str) -> dict[str, str]:
    """格式化大模型的响应"""

    # 提取Thought标签内容
    thought_match = re.search(r'<Thought>(.*?)</Thought>', response, re.DOTALL)
    thought_answer = thought_match.group(1).strip() if thought_match else None
    # 提取Action标签内容
    action_match = re.search(r'<Action>(.*?)</Action>', response, re.DOTALL)
    action_answer = action_match.group(1).strip() if action_match else None

    parse_result = {
        "Thought": thought_answer,
        "Action": action_answer,
        "Finish": action_answer and action_answer.startswith("Finish")
    }

    return parse_result


class ReActAgent:
    """ReAct Agent构造器"""

    def __init__(self, client: LLMClient, tool_executor: ToolExecutor, max_steps: int = 5):
        self.client = client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []
        self.available_tools = tool_executor.get_available_tools()


    def start(self, question: str) -> None:
        """运行ReAct智能体回答用户问题"""

        self.history = []
        current_step = 0
        system_prompt = REACT_PROMPT_TEMPLATE.format(tools=str(self.available_tools),)
        self.history.append(f"Question: {question}")

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n---第[{current_step}]次思考---\n")
            history_str = "\n".join(self.history)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": history_str}
            ]

            # 大语言模型响应
            response = self.client.answer(messages)

            if not response or response.startswith("❌大语言模型响应失败"):
                print(response)
                return

            response_dict = parse_response(response)
            self.history.append(f"Thought: {response_dict["Thought"]}")

            if response_dict["Finish"]:
                print(f"最终答案：\n{response_dict['Action']}")
                return
            else:
                # 未产生最终答案，需要调用外部工具
                observation_str = self.parse_tool_call(response_dict["Action"])
                print(f"工具调用结果：{observation_str}")
                self.history.append(f"Observation: {observation_str}")

        print("已超过最大循环次数，抱歉未能得到您想要的答案...")



    def parse_tool_call(self, tool_call: str) -> str:
        """解析调用的工具名，并返回调用工具的结果"""

        try:
            tool_name = re.search(r"(\w+)\(", tool_call).group(1)
            args_str = re.search(r"\((.*)\)", tool_call).group(1)
            kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

            if tool_name in self.tool_executor.tools:
                tool_func = self.tool_executor.get_tool(tool_name)
                return tool_func(**kwargs)
            else:
                return f"解析错误，未找到对应工具：{tool_name}"

        except Exception as e:
            return f"❌错误，解析工具时发生未知异常 - {e}"


