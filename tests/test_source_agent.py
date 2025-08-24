from __future__ import annotations

def test_create_source_agent_adds_extra_tools(
    mock_create_react_agent,  
    fake_agent,               
    monkeypatch
):
    import app.agents.source_agent as sa

    web_tool = object()
    rag_tool = object()
    monkeypatch.setattr(sa, "web_search_tool", web_tool)
    monkeypatch.setattr(sa, "rag_tool", rag_tool)

    model = object()
    tools = [object()]
    tools_copy = list(tools)

    agent = sa.create_source_agent(tools=tools, model=model)

    assert agent is fake_agent
    mock_create_react_agent.assert_called_once()
    kwargs = mock_create_react_agent.call_args.kwargs
    assert kwargs["model"] is model
    assert kwargs["name"] == "knowledge_agent"
    assert kwargs["tools"] == tools + [web_tool, rag_tool]
    assert tools == tools_copy 
    assert kwargs["prompt"] == sa.SOURCE_PROMPT
