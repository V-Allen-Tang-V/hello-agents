from typing import Any, Callable

class ToolExecutor:
    """
    工具执行器，负责管理和执行工具
    """

    def __init__(self):
        self.tools: dict[str, dict[str, Any]] = {}


    def tool_register(self, tool_name: str, args: list[str], tool_desc: str, func: Callable) -> None:
        """注册一个新工具"""
        if tool_name in self.tools:
            print(f"[{tool_name}]已经注册，将被覆盖。")

        self.tools[tool_name] = {
            "args": args,
            "description": tool_desc,
            "func": func
        }
        print(f"[{tool_name}]注册成功！")


    def get_tool(self, tool_name: str) -> Callable:
        """获取特定tool的功能"""
        if tool_name not in self.tools:
            raise Exception(f"[{tool_name}]未注册！")

        return self.tools[tool_name]["func"]

    def get_available_tools(self) -> list:
        """获取可调用的所有工具名称，主要给大模型展示"""
        available_tools = []
        for tool in self.tools:
            available_tools.append({
                "tool_name": tool,
                "tool_args": self.tools[tool]["args"],
                "tool_desc": self.tools[tool]["description"],
            })
        return available_tools