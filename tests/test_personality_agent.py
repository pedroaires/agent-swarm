from __future__ import annotations

def test_create_personality_agent_passes_correct_arguments(
    mock_create_react_agent,  
    fake_agent,               
):
    from app.agents.personality import create_personality_agent, PERSONALITY_PROMPT

    model = object()
    tools = [object(), object()]

    agent = create_personality_agent(tools=tools, model=model)

    assert agent is fake_agent
    mock_create_react_agent.assert_called_once()
    kwargs = mock_create_react_agent.call_args.kwargs
    assert kwargs["model"] is model
    assert kwargs["name"] == "personality_agent"
    assert kwargs["tools"] == tools
    assert kwargs["prompt"] == PERSONALITY_PROMPT
