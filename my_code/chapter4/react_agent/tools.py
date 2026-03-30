from my_code.gloable_config import SERPAPI_API_KEY
from serpapi import SerpApiClient

def baidu_search(question: str) -> str:
    """基于SerpApi的搜索工具，它会智能地搜索结果，并优先返回直接答案或知识图谱信息"""

    params = {
        "engine": "baidu",
        "q": question,
        "api_key": SERPAPI_API_KEY,
    }

    serpapi_client = SerpApiClient(params)
    results = serpapi_client.get_dict()

    # 解析答案
    if "answer_box_list" in results:
        return "\n".join(results["answer_box_list"])
    if "answer_box" in results and "answer" in results["answer_box"]:
        return results["answer_box"]["answer"]
    if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
        return results["knowledge_graph"]["description"]
    if "organic_results" in results and results["organic_results"]:
        organic = results["organic_results"]
        abstract_list = []
        for i in range(min(3, len(organic))):
            title = organic[i].get("title", "无标题")
            snippet = organic[i].get("snippet", "无摘要")
            abstract_list.append(f"[{i + 1}] {title}\n{snippet}")
        return "\n\n".join(abstract_list)

    return "抱歉，没有搜索到对应的答案！"

AVAILABLE_TOOLS = [{
    "name": "baidu_search",
    "args": ["question"],
    "description": "基于SerpApi的搜索工具，它会智能地搜索结果，并优先返回直接答案或知识图谱信息",
    "func": baidu_search
}]