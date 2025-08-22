from dataclasses import dataclass
from typing import Optional

from core.config import get_config
from langchain_openai import ChatOpenAI 
from langchain_core.messages import BaseMessage


@dataclass
class LLMSettings:
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    timeout: Optional[float] = 60.0
    max_retries: int = 2


class LLMClient:
    def __init__(self, settings: Optional[LLMSettings] = None) -> None:
        settings = settings or LLMSettings()
        if not get_config().OPENAI_API_KEY:
            raise ValueError("The environmental variable OPENAI_API_KEY is not set.")

        self._lc = ChatOpenAI(
            model_name=settings.model,
            temperature=settings.temperature,
            request_timeout=settings.timeout,
            max_retries=settings.max_retries,
        )

    @property
    def chat_model(self) -> ChatOpenAI:
        """Returns the Langchain instance for the graphs/chains usage"""
        return self._chat
