import sys
import os
sys.path.insert(0, '/home/suhkth/Desktop/Rag/agentic_rag_app/backend')

# Set environment variables before importing
os.environ['LANGSMITH_TRACING'] = 'true'

from langsmith import Client
from langsmith.run_helpers import traceable
from app.config import settings

# Create client
client = Client(api_key=settings.langsmith_api_key)

print(f"Testing LangSmith connection...")
print(f"API Key: {settings.langsmith_api_key[:15]}...")
print(f"Project: {settings.langsmith_project}")

@traceable(
    run_type="llm",
    project_name=settings.langsmith_project,
    client=client
)
def test_function(input_text: str) -> str:
    """Test function for LangSmith tracing."""
    return f"Processed: {input_text}"

try:
    result = test_function("Hello LangSmith!")
    print(f"✅ Test function executed: {result}")
    print(f"✅ Check LangSmith project '{settings.langsmith_project}' for the trace")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
