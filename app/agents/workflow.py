from app.llm.client import LLMClient
from app.agents.router import create_router_agent
from app.agents.personality import create_personality_agent
from app.agents.source_agent import create_source_agent
from app.agents.customer_support import create_customer_support_agent
from app.agents.tools.handoff import transferToKnowledgeAgent, transferToPersonality, transferToAccountDataAgent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END
from langgraph.graph import StateGraph, MessagesState

def build_graph():
    model = LLMClient().chat_model
    checkpointer = MemorySaver()
    customer_support = create_customer_support_agent([], model)
    personality = create_personality_agent([], model)
    source_agent = create_source_agent([], model)
    router = create_router_agent([transferToKnowledgeAgent(), transferToPersonality(), transferToAccountDataAgent()], model)
    graph = (
        StateGraph(MessagesState)
        .add_node(router, destinations=("knowledge_agent", "personality_agent", "account_data_agent"))
        .add_node(source_agent)
        .add_node(customer_support)
        .add_node(personality)
        # Always get back to the router
        .add_edge("knowledge_agent", "router")
        .add_edge("account_data_agent", "router")
        
        .add_edge(START, "router")
        .add_edge("personality_agent", END)
        .compile(checkpointer=checkpointer)
    )
    return graph
