#!/usr/bin/env python3
"""Update assistant to use a model compatible with file_search."""

import sys
sys.path.insert(0, '/home/suhkth/Desktop/Rag/agentic_rag_app/backend')

from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

assistant_id = settings.openai_assistant_id
vector_store_id = settings.openai_vector_store_id

# Use gpt-4-turbo (supports file_search)
new_model = "gpt-4-turbo"

print(f"Updating assistant to use {new_model}...")
print(f"Assistant ID: {assistant_id}")

instructions = """You are a helpful assistant that answers questions based on uploaded documents.

IMPORTANT INSTRUCTIONS:
1. When answering questions, ALWAYS search the available documents first using the file_search tool
2. Base your answers on the information found in the documents
3. ALWAYS cite your sources by referencing the document name or section
4. If information is not found in the documents, clearly state that
5. Be concise and accurate
6. Format citations like: "According to the Python Basics Reference Guide, ..."

When users ask about Python, programming concepts, or related topics, search the uploaded documents and provide accurate information with proper citations."""

try:
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        model=new_model,
        instructions=instructions,
        name="Agentic RAG Assistant",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        }
    )

    print("\n✅ Success! Assistant updated")
    print(f"\nAssistant Configuration:")
    print(f"  Name: {assistant.name}")
    print(f"  Model: {assistant.model} (✅ Supports file_search)")
    print(f"  Tools: {[tool.type for tool in assistant.tools]}")

    if assistant.tool_resources and assistant.tool_resources.file_search:
        print(f"  Vector Stores: {assistant.tool_resources.file_search.vector_store_ids}")

    print("\n🎉 Your assistant can now use file_search with the correct model!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
