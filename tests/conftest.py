from __future__ import annotations
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def fake_agent() -> object:
    return object()

@pytest.fixture
def mock_create_react_agent(monkeypatch: pytest.MonkeyPatch, fake_agent: object) -> MagicMock:
    """
    Mocks langgraph.prebuilt.create_react_agent.
    Always returns `fake_agent`.
    """
    m = MagicMock(side_effect=lambda **kwargs: fake_agent)
    monkeypatch.setattr("langgraph.prebuilt.create_react_agent", m)
    return m
