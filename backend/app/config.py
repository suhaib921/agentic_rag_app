from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    supabase_url: str
    supabase_service_role_key: str
    supabase_anon_key: str
    openai_api_key: str
    openai_assistant_id: str
    openai_vector_store_id: str
    langsmith_api_key: str
    langsmith_project: str = "agentic-rag-module1"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
