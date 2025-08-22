from app.agents.router import create_router_agent
from app.agents.personality import create_personality_agent
from app.agents.source_agent import create_source_agent

def build_graph():
    source_agent = create_source_agent()
    personality_agent = create_personality_agent()
    workflow = create_router_agent([source_agent, personality_agent])
    return workflow.compile()
