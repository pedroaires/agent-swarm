from typing import Dict, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel

from app.llm.client import LLMClient


ROUTER_PROMPT = """
ROLE
- You are the Router. You never talk to the user or write messages you only use the tools to transfer to the most suited agent.
- Your job is to decide which agent should act next and call the tool to transfer to that agent.

INPUTS
- Latest user message and the conversation state.
- Outputs from other agents (summaries/evidence).

DECISION RULES
1) If public/company knowledge is required (not user-specific) → transgfer to the knowledge agent.
2) If user-specific account/payment data is required → transfer to the account data agent.
3) If all necessary info is already available or nothing else can be done → transfer to the personality agent.

CONSTRAINTS
- Do not produce user-facing text.
- End every turn by calling exactly one transfer tool.
- If unsure which to pick, prefer gathering missing info first (1 or 2).

OUTPUT
- A single tool call redirecting to the specialized agent.
- You always need to redirect to the agent. Never forget to redirect to the responsible agent.
"""


def create_router_agent(tools, model):
    router_agent = create_react_agent(
        model=model,
        name="router",
        tools=tools,
        prompt=ROUTER_PROMPT
    )
    return router_agent