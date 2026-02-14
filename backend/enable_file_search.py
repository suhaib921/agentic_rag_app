#!/usr/bin/env python3
"""Enable file_search tool on OpenAI Assistant."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

assistant_id = settings.openai_assistant_id
vector_store_id = settings.openai_vector_store_id

print(f"Enabling file_search tool on assistant...")
print(f"Assistant ID: {assistant_id}")

try:
    # Update the assistant with file_search tool
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        }
    )

    print("\n✅ Success! File search enabled")
    print(f"\nAssistant Configuration:")
    print(f"  Name: {assistant.name or 'Agentic RAG Assistant'}")
    print(f"  Model: {assistant.model}")
    print(f"  Tools: {[tool.type for tool in assistant.tools]}")

    if assistant.tool_resources and assistant.tool_resources.file_search:
        print(f"  Vector Stores: {assistant.tool_resources.file_search.vector_store_ids}")

    print("\n🎉 Ready to test! Your assistant can now search documents.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
