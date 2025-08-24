from typing import Dict, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langgraph.prebuilt import create_react_agent
from app.llm.client import LLMClient
PERSONALITY_PROMPT = (
    """
    You are an agent specialized in using other agents information and messages to responde
    to the user in a human way, use the users language to respond it.
    """
)

def create_personality_agent(tools, model):
    personality_agent = create_react_agent(
        model=model,
        name="personality_agent",
        tools=tools,
        prompt=PERSONALITY_PROMPT
    )
    return personality_agent