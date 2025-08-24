from __future__ import annotations

def test_create_router_agent_passes_correct_arguments(
    mock_create_react_agent,  
    fake_agent,               
):
    from app.agents.router import create_router_agent, ROUTER_PROMPT

    model = object()
    tools = [object()]

    agent = create_router_agent(tools=tools, model=model)

    assert agent is fake_agent
    mock_create_react_agent.assert_called_once()
    kwargs = mock_create_react_agent.call_args.kwargs
    assert kwargs["model"] is model
    assert kwargs["name"] == "router"
    assert kwargs["tools"] == tools
    assert kwargs["prompt"] == ROUTER_PROMPT
