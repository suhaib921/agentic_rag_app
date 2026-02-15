from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any

class BaseLLMProvider(ABC):
    """Base interface for LLM providers."""

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[dict[str, str]],
        model: str
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream chat completion response."""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str
    ) -> str:
        """Non-streaming chat completion."""
        pass
