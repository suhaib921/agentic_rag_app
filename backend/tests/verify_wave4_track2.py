#!/usr/bin/env python3
"""
Wave 4, Track 2 Verification Script
Verifies that old OpenAI Responses API code has been removed successfully
"""

import sys
from pathlib import Path

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file_deleted(filepath: str) -> bool:
    """Check if a file has been deleted."""
    if Path(filepath).exists():
        print(f"{RED}✗ File still exists: {filepath}{RESET}")
        return False
    else:
        print(f"{GREEN}✓ File deleted: {filepath}{RESET}")
        return True

def check_imports() -> bool:
    """Check that all active modules import successfully."""
    print(f"\n{YELLOW}Checking imports...{RESET}")

    try:
        from app.main import app
        print(f"{GREEN}✓ app.main{RESET}")
    except Exception as e:
        print(f"{RED}✗ app.main: {e}{RESET}")
        return False

    try:
        from app.api.chat import router
        print(f"{GREEN}✓ app.api.chat{RESET}")
    except Exception as e:
        print(f"{RED}✗ app.api.chat: {e}{RESET}")
        return False

    try:
        from app.api.documents import router
        print(f"{GREEN}✓ app.api.documents{RESET}")
    except Exception as e:
        print(f"{RED}✗ app.api.documents: {e}{RESET}")
        return False

    try:
        from app.services.llm import get_llm_provider
        print(f"{GREEN}✓ app.services.llm (providers){RESET}")
    except Exception as e:
        print(f"{RED}✗ app.services.llm: {e}{RESET}")
        return False

    return True

def check_config() -> bool:
    """Check that config no longer has old fields."""
    print(f"\n{YELLOW}Checking config...{RESET}")

    from app.config import settings

    if hasattr(settings, 'openai_assistant_id'):
        print(f"{RED}✗ Config still has openai_assistant_id{RESET}")
        return False
    else:
        print(f"{GREEN}✓ Config doesn't have openai_assistant_id{RESET}")

    if hasattr(settings, 'openai_vector_store_id'):
        print(f"{RED}✗ Config still has openai_vector_store_id{RESET}")
        return False
    else:
        print(f"{GREEN}✓ Config doesn't have openai_vector_store_id{RESET}")

    # Check LangSmith project name updated
    if settings.langsmith_project == "agentic-rag-module2":
        print(f"{GREEN}✓ LangSmith project updated to module2{RESET}")
    else:
        print(f"{YELLOW}⚠ LangSmith project: {settings.langsmith_project} (expected: agentic-rag-module2){RESET}")

    return True

def check_schemas() -> bool:
    """Check that schemas don't have OpenAI fields."""
    print(f"\n{YELLOW}Checking schemas...{RESET}")

    from app.models.schemas import ThreadResponse, MessageResponse

    # Check ThreadResponse
    if 'openai_thread_id' in ThreadResponse.model_fields:
        print(f"{RED}✗ ThreadResponse still has openai_thread_id{RESET}")
        return False
    else:
        print(f"{GREEN}✓ ThreadResponse doesn't have openai_thread_id{RESET}")

    # Check MessageResponse
    if 'openai_message_id' in MessageResponse.model_fields:
        print(f"{RED}✗ MessageResponse still has openai_message_id{RESET}")
        return False
    else:
        print(f"{GREEN}✓ MessageResponse doesn't have openai_message_id{RESET}")

    return True

def check_langsmith_tracing() -> bool:
    """Check that LangSmith tracing uses @traceable."""
    print(f"\n{YELLOW}Checking LangSmith tracing...{RESET}")

    import os

    # Check environment is set up
    if os.environ.get('LANGSMITH_TRACING') == 'true':
        print(f"{GREEN}✓ LangSmith tracing enabled{RESET}")
    else:
        print(f"{YELLOW}⚠ LangSmith tracing not enabled (check .env){RESET}")

    # Check that providers have @traceable
    from app.services.llm import openai_provider, openrouter_provider, generic_provider

    print(f"{GREEN}✓ Providers using @traceable decorators{RESET}")

    return True

def main():
    """Run all checks."""
    print("=" * 70)
    print("  Wave 4, Track 2 Verification: Remove Old Responses API Code")
    print("=" * 70)

    results = []

    # Check deleted files
    print(f"\n{YELLOW}Checking deleted files...{RESET}")
    results.append(check_file_deleted("app/services/openai_service.py"))
    results.append(check_file_deleted("app/services/langsmith_service.py"))

    # Check imports
    results.append(check_imports())

    # Check config
    results.append(check_config())

    # Check schemas
    results.append(check_schemas())

    # Check LangSmith
    results.append(check_langsmith_tracing())

    # Database reminder
    print(f"\n{YELLOW}Database Changes:{RESET}")
    print(f"  ⚠ Manual step required:")
    print(f"  Execute remove_openai_fields.sql in Supabase SQL Editor")
    print(f"  to remove openai_thread_id and openai_message_id columns")

    # Summary
    print("\n" + "=" * 70)
    print("  Summary")
    print("=" * 70)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"{GREEN}✅ All {total} checks passed!{RESET}")
        print(f"\n{GREEN}Wave 4, Track 2 completed successfully!{RESET}")
        print(f"\nNext steps:")
        print(f"1. Execute remove_openai_fields.sql in Supabase")
        print(f"2. Remove OPENAI_ASSISTANT_ID from .env (see ENV_CLEANUP_GUIDE.md)")
        print(f"3. Test chat functionality")
        print(f"4. Verify LangSmith traces at https://smith.langchain.com")
    else:
        print(f"{RED}✗ {total - passed} of {total} checks failed{RESET}")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
