from openai import OpenAI

class OpenAIClient:

    def __init__(self, model: str, base_url: str, api_key: str):
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def query_llm(self, system_prompt: str, user_prompt: str) -> str:
        """调用大语言模型并返回结果"""

        print("正在调用大语言模型...")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        llm_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
            timeout=30
        )
        answer = llm_response.choices[0].message.content
        print("调用大语言模型成功...")
        return "模型输出：\n" + answer