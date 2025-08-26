from langgraph.prebuilt import create_react_agent
from .tools.web_search import web_search_tool
from .tools.rag_tool import rag_tool
SOURCE_PROMPT = """
ROLE
- You are a Research agent. You gather relevant information to help other agents answer the request.
- Use tools to find current, reliable information.

TOOLS
- web_search: general/public information.
- rag_tool: InfinitePay internal/company information.

CONSTRAINTS
- Do not speak to the user.
- Do not speculate; if unknown, say unknown.
- Deduplicate and keep only relevant info.

OUTPUT
- A summary of the gathered relvant information
- If the information is not obtainable do not make up anything and do not ask anything, just say you could not find.
"""

def create_source_agent(tools, model):
    source_agent = create_react_agent(
        model=model,
        name="knowledge_agent",
        tools=tools + [web_search_tool, rag_tool],
        prompt=SOURCE_PROMPT
    )
    return source_agent