from openai import OpenAI

class LLMClient:
    def __init__(self, model: str, base_url: str, api_key: str, timeout: int = 60):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )


    def answer(self, messages: list[dict[str, str]], temperature: float = 0) -> str:
        """调用大语言模型，返回响应"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True
            )

            print("✔大语言模型响应成功！")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)
        except Exception as e:
            return f"❌大语言模型响应失败：{e}"