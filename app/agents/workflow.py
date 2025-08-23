from app.agents.router import create_router_agent
from app.agents.personality import create_personality_agent
from app.agents.source_agent import create_source_agent
from app.agents.tools.handoff import transferToKnowledgeAgent, transferToPersonality
from langgraph.checkpoint.memory import MemorySaver
from langgraph_swarm import create_swarm

def build_graph():
    checkpointer = MemorySaver()
    personality = create_personality_agent([])
    source_agent = create_source_agent([])
    router = create_router_agent([transferToKnowledgeAgent(), transferToPersonality()])

    workflow = create_swarm(
        [router, personality, source_agent],
        default_active_agent="router"
    )
    return workflow.compile(checkpointer=checkpointer)
