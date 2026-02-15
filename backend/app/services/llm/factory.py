from app.config import get_settings
from .base import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .openrouter_provider import OpenRouterProvider
from .generic_provider import GenericProvider

_provider_instance = None

def get_llm_provider() -> BaseLLMProvider:
    """Factory function to get the configured LLM provider."""
    global _provider_instance

    if _provider_instance is not None:
        return _provider_instance

    settings = get_settings()
    provider_name = settings.chat_provider.lower()

    if provider_name == "openai":
        _provider_instance = OpenAIProvider(api_key=settings.chat_api_key)
    elif provider_name == "openrouter":
        _provider_instance = OpenRouterProvider(api_key=settings.chat_api_key)
    elif provider_name in ["ollama", "lmstudio", "generic"]:
        _provider_instance = GenericProvider(
            base_url=settings.chat_base_url,
            api_key=settings.chat_api_key
        )
    else:
        raise ValueError(f"Unknown provider: {provider_name}")

    return _provider_instance
