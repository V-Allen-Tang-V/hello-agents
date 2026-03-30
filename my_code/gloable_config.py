import os

MODEL_NAME = "Qwen/Qwen3.5-27B"
BASE_URL = "https://api-inference.modelscope.cn/v1/"
API_KEY = os.environ.get("MODELSCOPE_SDK_TOKEN")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")


SETTINGS = {
    "MODEL_NAME": MODEL_NAME,
    "BASE_URL": BASE_URL,
    "API_KEY": API_KEY,
    "TAVILY_API_KEY": TAVILY_API_KEY,
    "SERPAPI_API_KEY": SERPAPI_API_KEY,
}