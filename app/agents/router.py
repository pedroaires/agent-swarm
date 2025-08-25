from typing import Dict, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel

from app.llm.client import LLMClient


ROUTER_PROMPT = (
    """
    You are an agent specialized in delegating an user request to other agents.
    If the user request will require extra information, use the source agent, if the user request is about his own information, transfer to the customer support agent.
    If no information else is needed, use the personality agent to respond the user.
    Do not ask anything or talk to the user, just transfer to the right agent.
    """
)

def create_router_agent(tools, model):
    router_agent = create_react_agent(
        model=model,
        name="router",
        tools=tools,
        prompt=ROUTER_PROMPT
    )
    return router_agent