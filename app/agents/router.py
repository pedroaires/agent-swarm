from typing import Dict, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph_supervisor import create_supervisor
from langchain_core.language_models import BaseChatModel

from app.llm.client import LLMClient


ROUTER_PROMPT = (
    """
    You are an agent specialized in delegating an user request to other agents.
    If the user request will require extra information, use the source agent.
    If no information else is needed, use the personality agent to respond the user.
    Do not ask anything or talk to the user, just transfer to the right agent.
    """
)

def create_router_agent(agent_list):
    router_agent = create_supervisor(
        model=LLMClient().chat_model,
        agents=agent_list,
        output_mode="last_message",
        prompt=ROUTER_PROMPT
    )
    return router_agent