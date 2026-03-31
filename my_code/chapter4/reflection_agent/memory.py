import enum
from typing import Any

class RecordType(enum.Enum):
    EXECUTE = "execute"
    REFLECT = "reflect"


class Memory:

    def __init__(self):
        self.memory: list[dict[str, Any]] = []
        self.last_execute: str = "无"

    def add_memory(self, record_type: RecordType, record_content: str) -> None:
        self.memory.append({
            "type": record_type,
            "content": record_content
        })
        if record_type == RecordType.EXECUTE:
            self.last_execute = record_content


    def convert_memory_to_str(self) -> str:
        """将memory的内容转化成字符串"""

        memory_str = []
        for single_mem in self.memory:
            if single_mem["type"] == RecordType.EXECUTE:
                memory_str.append(f"---上一轮的执行结果---\n{single_mem["content"]}")
            elif single_mem["type"] == RecordType.REFLECT:
                memory_str.append(f"---上一轮的反思结果---\n{single_mem['content']}")

        return "\n\n".join(memory_str)