from typing import Dict, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langgraph.prebuilt import create_react_agent
from .tools .web_search import web_search_tool
from .tools .rag_tool import rag_tool

from app.llm.client import LLMClient
SOURCE_PROMPT = (
    """
    You are an agent specialized in searching for relevant information to help other agents answer an user request. You must use the tools available to fetch this information. Use the web_search for general information and rag_tool for information about the infinite pay company.
    """
)

def create_source_agent(tools):
    source_agent = create_react_agent(
        model=LLMClient().chat_model,
        name="knowledge_agent",
        tools=tools + [web_search_tool, rag_tool],
        prompt=SOURCE_PROMPT
    )
    return source_agent