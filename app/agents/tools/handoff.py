from langgraph_swarm import create_handoff_tool

def transferToPersonality():
    return create_handoff_tool(
        agent_name="personality_agent",
        description="Transfer user to the personality agent."
    )

def transferToKnowledgeAgent():
    return create_handoff_tool(
        agent_name="knowledge_agent",
        description="Transfer user to the knowledge agent."
    )

def transferToCustomerSupport():
    return create_handoff_tool(
        agent_name="customer_support_agent",
        description="Transfer user to the customer support agent."
    )

def transferToRouterAgent():
    return create_handoff_tool(
        agent_name="router",
        description="Transfer user to the router"
    )