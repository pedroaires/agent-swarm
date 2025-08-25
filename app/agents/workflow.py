from app.llm.client import LLMClient
from app.agents.router import create_router_agent
from app.agents.personality import create_personality_agent
from app.agents.source_agent import create_source_agent
from app.agents.customer_support import create_customer_support_agent
from app.agents.tools.handoff import transferToKnowledgeAgent, transferToPersonality, transferToCustomerSupport
from langgraph.checkpoint.memory import MemorySaver
from langgraph_swarm import create_swarm

def build_graph():
    model = LLMClient().chat_model
    checkpointer = MemorySaver()
    customer_support = create_customer_support_agent([], model)
    personality = create_personality_agent([], model)
    source_agent = create_source_agent([], model)
    router = create_router_agent([transferToKnowledgeAgent(), transferToPersonality(), transferToCustomerSupport()], model)

    workflow = create_swarm(
        [router, personality, source_agent, customer_support],
        default_active_agent="router"
    )
    return workflow.compile(checkpointer=checkpointer)
