#!/usr/bin/env python3
"""Link vector store to OpenAI Assistant."""

import sys
sys.path.insert(0, '/home/suhkth/Desktop/Rag/agentic_rag_app/backend')

from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

# Vector store ID
vector_store_id = "vs_698df86be3d081918dc449d66fb7f552"
assistant_id = settings.openai_assistant_id

print(f"Linking vector store to assistant...")
print(f"Assistant ID: {assistant_id}")
print(f"Vector Store ID: {vector_store_id}")

try:
    # Update the assistant to use the vector store
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        }
    )

    print("\n✅ Success! Vector store linked to assistant")
    print(f"\nAssistant Details:")
    print(f"  Name: {assistant.name}")
    print(f"  Model: {assistant.model}")
    print(f"  Tools: {[tool.type for tool in assistant.tools]}")

    if assistant.tool_resources and assistant.tool_resources.file_search:
        print(f"  Vector Stores: {assistant.tool_resources.file_search.vector_store_ids}")

    print("\n🎉 Your assistant can now search the uploaded documents!")
    print("\nTest it by asking:")
    print("  - 'What documents do you have access to?'")
    print("  - 'What are Python lists?'")
    print("  - 'Tell me about Python best practices'")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
