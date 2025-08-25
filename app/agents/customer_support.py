from langgraph.prebuilt import create_react_agent
from app.agents.tools.balance_tool import get_balance
from app.agents.tools.user_profile import get_user_profile
from app.agents.tools.utils import bind_user_id

CUSTOMER_SUPPORT_PROMPT = (
    """
    You are an agent specialized in fetching relevant user information. You should use the tools available to get information about the user to help other agents answer the user requests.
    """
)

def create_customer_support_agent(tools, model):
    customer_support = create_react_agent(
        model=model,
        name="customer_support_agent",
        tools=tools + [
            get_user_profile, 
            get_balance
            ],
        prompt=CUSTOMER_SUPPORT_PROMPT
    )
    return customer_support