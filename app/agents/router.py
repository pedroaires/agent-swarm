from typing import Dict, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel

from app.llm.client import LLMClient


ROUTER_PROMPT = """
ROLE
- You are the Router. You never talk to the user.
- Your job is to decide which agent should act next.

INPUTS
- Latest user message and the conversation state.
- Outputs from other agents (summaries/evidence).

TOOLS (call EXACTLY ONE)
- transfer_to_knowledge_agent(reason, needed_info?)
- transfer_to_customer_support(reason, user_fields?)
- transfer_to_personality(reason)

DECISION RULES
1) If public/company knowledge is required (not user-specific) → transgfer to the knowledge agent.
2) If user-specific account/payment data is required → transfer to the customer support agent.
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