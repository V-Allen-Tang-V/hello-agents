"""为Agent提供能力的Tools"""

import requests
from tavily import TavilyClient
from ..gloable_config import TAVILY_API_KEY


def get_current_weather(city: str) -> str:
    """获取某一具体城市实时天气的tool"""

    # 请求JSON格式的数据
    weather_url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(weather_url)
        # 检查返回码状态
        response.raise_for_status()
        # 获取JSON格式结果
        weather_json_data = response.json()

        current_data = weather_json_data["current_condition"][0]
        current_time = current_data["localObsDateTime"]
        current_weather = current_data["weatherDesc"][0]["value"]
        current_temperature = current_data["temp_C"]
        return f"当前时间是{current_time}，{city}的天气是{current_weather}，气温{current_temperature}℃"

    except requests.HTTPError:
        return "当前网络连接出现问题，请稍后重试！"


def get_recommended_attractions(city: str, weather: str) -> str:
    """根据城市名称和当前天气，推荐旅游景点的tool"""

    # 初始化tavily客户端
    client = TavilyClient(api_key=TAVILY_API_KEY)
    # 构造一个查询prompt
    query_prompt = f"请推荐{weather}天气下，{city}最值得去的旅游景点，并给出理由"

    try:
        tavily_response = client.search(
            query=query_prompt,
            search_depth="basic",
            include_answer=True,
        )

        # 若有综合性回答，直接返回结果
        if tavily_response.get("answer"):
            return tavily_response["answer"]

        # 若没有综合性回答，则格式化原始结果
        formatted_answer = []
        tavily_results = tavily_response["results"]
        for tavily_result in tavily_results:
            formatted_answer.append(f"- {tavily_result["title"]}：{tavily_result["content"]}")

        if not formatted_answer:
            return "抱歉，没有找到推荐的景点！"
        return "根据索索，为您找到以下信息：\n" + "\n".join(formatted_answer)

    except Exception as e:
        return f"执行搜索时发生错误 - {e}"

AVAILABLE_TOOLS = {
    "get_current_weather": get_current_weather,
    "get_recommended_attractions": get_recommended_attractions
}
