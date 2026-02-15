# LangSmith tracing now done via @traceable decorators in providers
import os
from app.config import get_settings

settings = get_settings()

if settings.langsmith_api_key:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
