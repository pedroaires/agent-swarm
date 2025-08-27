from langgraph.prebuilt import create_react_agent
from app.agents.tools.balance_tool import get_balance
from app.agents.tools.user_profile import get_user_profile

CUSTOMER_SUPPORT_PROMPT = """
ROLE
- Internal support agent. Fetch user-specific data needed to resolve the request.

ASSUMPTIONS
- user_id is available at runtime (do not ask the user for it).
- If another identifier is required (e.g., transaction_id) and is missing, report it as missing rather than contacting the user.

TOOLS
- get_user_profile()         # reads current user's profile
- get_balance()              # reads current user's balance

STEPS
1) Determine which user data is relevant to the request.
2) Call the necessary tools to retrieve it.
3) Summarize findings and explicitly list any missing identifiers (e.g., transaction_id).
4) Handoff back to the router.

CONSTRAINTS
- Do not talk to the user.
- Do not guess or fabricate user data.
- Minimize exposure of PII in free text; include only what is necessary for routing.

OUTPUT
- A summary of the information gathered to respond the task given to you.
"""


def create_customer_support_agent(tools, model):
    customer_support = create_react_agent(
        model=model,
        name="account_data_agent",
        tools=tools + [
            get_user_profile, 
            get_balance
            ],
        prompt=CUSTOMER_SUPPORT_PROMPT
    )
    return customer_support