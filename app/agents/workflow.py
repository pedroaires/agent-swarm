from app.llm.client import LLMClient
from app.agents.router import create_router_agent
from app.agents.personality import create_personality_agent
from app.agents.source_agent import create_source_agent
from app.agents.tools.handoff import transferToKnowledgeAgent, transferToPersonality
from langgraph.checkpoint.memory import MemorySaver
from langgraph_swarm import create_swarm

def build_graph():
    model = LLMClient().chat_model
    checkpointer = MemorySaver()
    personality = create_personality_agent([], model)
    source_agent = create_source_agent([], model)
    router = create_router_agent([transferToKnowledgeAgent(), transferToPersonality()], model)

    workflow = create_swarm(
        [router, personality, source_agent],
        default_active_agent="router"
    )
    return workflow.compile(checkpointer=checkpointer)
