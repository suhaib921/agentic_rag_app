from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    supabase_anon_key: str
    openai_api_key: str
    langsmith_api_key: str
    langsmith_project: str = "agentic-rag-module2"
    cors_origins: str = "http://localhost:5173"

    # LLM Provider
    chat_provider: str = "openai"  # openai, openrouter, ollama, lmstudio
    chat_model: str = "gpt-4o"
    chat_api_key: str = ""
    chat_base_url: str = ""  # For generic providers

    # Embeddings (always OpenAI)
    embedding_model: str = "text-embedding-3-small"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

def get_settings() -> Settings:
    """Get the application settings."""
    return Settings()

# Create singleton instance
settings = Settings()
