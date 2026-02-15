"""
Test script to verify LLM provider abstraction.
Tests each provider type and verifies streaming functionality.
"""
import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, '/home/suhkth/Desktop/Rag/agentic_rag_app/backend')

# Import tracing setup first
from app.services import langsmith_tracing

from app.services.llm import get_llm_provider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.openrouter_provider import OpenRouterProvider
from app.services.llm.generic_provider import GenericProvider
from app.config import get_settings


async def test_stream_chat(provider, provider_name: str, model: str):
    """Test streaming chat completion."""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name} - stream_chat()")
    print(f"{'='*60}")

    messages = [
        {"role": "user", "content": "Say 'Hello from {provider_name}' in one sentence."}
    ]

    try:
        chunks = []
        async for chunk in provider.stream_chat(messages, model):
            chunks.append(chunk)
            if chunk["type"] == "text_delta":
                print(chunk["content"], end="", flush=True)

        print("\n")

        # Verify format
        assert len(chunks) > 0, "No chunks received"
        assert chunks[-1]["type"] == "done", "Missing 'done' chunk"

        text_chunks = [c for c in chunks if c["type"] == "text_delta"]
        assert len(text_chunks) > 0, "No text chunks received"

        print(f"✓ Received {len(text_chunks)} text chunks + done signal")
        print(f"✓ Stream format is correct")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_chat(provider, provider_name: str, model: str):
    """Test non-streaming chat completion."""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name} - chat()")
    print(f"{'='*60}")

    messages = [
        {"role": "user", "content": "Say 'Hello from {provider_name}' in one sentence."}
    ]

    try:
        response = await provider.chat(messages, model)
        print(f"Response: {response}")

        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response is empty"

        print(f"✓ Received response of {len(response)} characters")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("LLM Provider Abstraction Test Suite")
    print("="*60)

    settings = get_settings()
    results = []

    # Test 1: Factory function with default settings
    print("\n" + "="*60)
    print("TEST 1: Factory Function")
    print("="*60)

    try:
        provider = get_llm_provider()
        print(f"✓ Factory returned: {type(provider).__name__}")
        print(f"  Provider: {settings.chat_provider}")
        print(f"  Model: {settings.chat_model}")
        results.append(("Factory", True))
    except Exception as e:
        print(f"✗ Factory failed: {e}")
        results.append(("Factory", False))
        return

    # Test 2: OpenAI Provider (if configured)
    if settings.openai_api_key:
        print("\n" + "="*60)
        print("TEST 2: OpenAI Provider")
        print("="*60)

        openai_provider = OpenAIProvider(api_key=settings.openai_api_key)
        model = "gpt-4o-mini"  # Use a cheaper model for testing

        stream_ok = await test_stream_chat(openai_provider, "OpenAI", model)
        results.append(("OpenAI Stream", stream_ok))

        chat_ok = await test_chat(openai_provider, "OpenAI", model)
        results.append(("OpenAI Chat", chat_ok))
    else:
        print("\n⊘ Skipping OpenAI tests (no API key)")

    # Test 3: OpenRouter Provider (if configured)
    if os.getenv("OPENROUTER_API_KEY"):
        print("\n" + "="*60)
        print("TEST 3: OpenRouter Provider")
        print("="*60)

        openrouter_provider = OpenRouterProvider(api_key=os.getenv("OPENROUTER_API_KEY"))
        model = "anthropic/claude-3-haiku"  # Use a cheaper model

        stream_ok = await test_stream_chat(openrouter_provider, "OpenRouter", model)
        results.append(("OpenRouter Stream", stream_ok))

        chat_ok = await test_chat(openrouter_provider, "OpenRouter", model)
        results.append(("OpenRouter Chat", chat_ok))
    else:
        print("\n⊘ Skipping OpenRouter tests (no API key)")

    # Test 4: Generic Provider (Ollama - if running)
    print("\n" + "="*60)
    print("TEST 4: Generic Provider (Ollama)")
    print("="*60)
    print("Note: This test requires Ollama to be running locally")
    print("Skip if Ollama is not available")

    # We'll just test instantiation, not actual calls
    try:
        generic_provider = GenericProvider(
            base_url="http://localhost:11434/v1",
            api_key="not-needed"
        )
        print(f"✓ Generic provider instantiated successfully")
        results.append(("Generic Instantiation", True))
    except Exception as e:
        print(f"✗ Generic provider failed: {e}")
        results.append(("Generic Instantiation", False))

    # Test 5: LangSmith Tracing
    print("\n" + "="*60)
    print("TEST 5: LangSmith Tracing")
    print("="*60)

    if settings.langsmith_api_key:
        print(f"✓ LangSmith is configured")
        print(f"  Project: {settings.langsmith_project}")
        print(f"  API Key: {settings.langsmith_api_key[:10]}...")
        print(f"  Tracing enabled: {os.getenv('LANGSMITH_TRACING')}")
        print(f"\nCheck traces at: https://smith.langchain.com/")
        results.append(("LangSmith Config", True))
    else:
        print("⊘ LangSmith not configured")
        results.append(("LangSmith Config", False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")


if __name__ == "__main__":
    asyncio.run(main())
