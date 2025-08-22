from langchain.tools import tool
from tavily import TavilyClient
from app.core.config import get_config

@tool
def web_search_tool(query: str) -> str:
    """Use this tool to search the web for information."""
    tavily = TavilyClient(api_key=get_config().OPENAI_API_KEY)
    search_results = tavily.search(query=query)
    return str(search_results)
