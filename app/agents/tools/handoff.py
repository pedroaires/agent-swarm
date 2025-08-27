from typing import Annotated
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool, InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
def transferToPersonality():
    return create_custom_handoff_tool(
        agent_name="personality_agent",
        description="Transfer user to the personality agent to sinthetize the final answer."
    )

def transferToKnowledgeAgent():
    return create_custom_handoff_tool(
        agent_name="knowledge_agent",
        description="Transfer user to the knowledge agent to fetch information about the company or general purposes."
    )

def transferToAccountDataAgent():
    return create_custom_handoff_tool(
        agent_name="account_data_agent",
        description="Transfer user to the account data agent to fetch user's account related questions."
    )

def create_custom_handoff_tool(*, agent_name: str, description: str) -> BaseTool:
    tool_name = f"transfer_to_{agent_name}"
    @tool(tool_name, description=description)
    def handoff_to_agent(
        task_description: Annotated[str, "Detailed description of what the next agent should do, including all of the relevant context."],
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        tool_message = ToolMessage(
            content=f"Successfully transferred to {agent_name}",
            name=tool_name,
            tool_call_id=tool_call_id,
        )
        messages = state["messages"]
        return Command(
            goto=agent_name,
            graph=Command.PARENT,
            update={
                "messages": messages + [tool_message],
                "active_agent": agent_name,
                "task_description": task_description,
            },
        )

    return handoff_to_agent