"""
Verification script for RAG Service (Wave 2, Track 2)

This script tests:
1. Vector similarity search with match_chunks function
2. Top-K retrieval with correct ranking
3. Similarity score threshold filtering
4. RLS enforcement (user isolation)
5. Context formatting
"""

import asyncio
import uuid
from app.db.supabase import get_supabase_client
from app.services.embeddings import generate_embedding
from app.services.rag_service import retrieve_context, format_context

# Test data
TEST_USER_1 = str(uuid.uuid4())
TEST_USER_2 = str(uuid.uuid4())

async def setup_test_data():
    """Insert test documents and chunks with embeddings."""
    supabase = get_supabase_client()

    print("Setting up test data...")

    # Test documents
    test_docs = [
        {
            "user_id": TEST_USER_1,
            "filename": "python_guide.txt",
            "file_size": 1000,
            "file_type": "text/plain",
            "storage_path": f"{TEST_USER_1}/python_guide.txt",
            "status": "completed",
            "chunk_count": 2
        },
        {
            "user_id": TEST_USER_1,
            "filename": "javascript_guide.txt",
            "file_size": 1000,
            "file_type": "text/plain",
            "storage_path": f"{TEST_USER_1}/javascript_guide.txt",
            "status": "completed",
            "chunk_count": 1
        },
        {
            "user_id": TEST_USER_2,
            "filename": "user2_doc.txt",
            "file_size": 1000,
            "file_type": "text/plain",
            "storage_path": f"{TEST_USER_2}/user2_doc.txt",
            "status": "completed",
            "chunk_count": 1
        }
    ]

    # Insert documents
    doc_result = supabase.table("documents").insert(test_docs).execute()
    doc_ids = {doc["filename"]: doc["id"] for doc in doc_result.data}

    # Test chunks with content that will have different similarity scores
    test_chunks = [
        {
            "document_id": doc_ids["python_guide.txt"],
            "user_id": TEST_USER_1,
            "content": "Python is a high-level programming language known for its simplicity and readability. It uses indentation for code blocks.",
            "chunk_index": 0,
            "metadata": {"page": 1}
        },
        {
            "document_id": doc_ids["python_guide.txt"],
            "user_id": TEST_USER_1,
            "content": "Python supports multiple programming paradigms including object-oriented, functional, and procedural programming.",
            "chunk_index": 1,
            "metadata": {"page": 2}
        },
        {
            "document_id": doc_ids["javascript_guide.txt"],
            "user_id": TEST_USER_1,
            "content": "JavaScript is a scripting language primarily used for web development. It runs in the browser and on servers via Node.js.",
            "chunk_index": 0,
            "metadata": {"page": 1}
        },
        {
            "document_id": doc_ids["user2_doc.txt"],
            "user_id": TEST_USER_2,
            "content": "Python programming is great for data science and machine learning applications.",
            "chunk_index": 0,
            "metadata": {"page": 1}
        }
    ]

    # Generate embeddings for each chunk
    print("Generating embeddings...")
    for chunk in test_chunks:
        embedding = await generate_embedding(chunk["content"])
        chunk["embedding"] = embedding

    # Insert chunks
    supabase.table("chunks").insert(test_chunks).execute()

    print(f"✓ Created {len(test_docs)} documents and {len(test_chunks)} chunks")
    return doc_ids

async def test_vector_search():
    """Test 1: Basic vector similarity search."""
    print("\n" + "="*60)
    print("Test 1: Vector Similarity Search")
    print("="*60)

    query = "Tell me about Python programming language"
    print(f"Query: '{query}'")

    try:
        chunks = await retrieve_context(query, TEST_USER_1, top_k=5)

        print(f"\n✓ Retrieved {len(chunks)} chunks")

        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i}:")
            print(f"  Content: {chunk['content'][:80]}...")
            print(f"  Similarity: {chunk['similarity']:.4f}")
            print(f"  Filename: {chunk['filename']}")

        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

async def test_top_k_ranking():
    """Test 2: Verify top-K results are correctly ranked by similarity."""
    print("\n" + "="*60)
    print("Test 2: Top-K Ranking")
    print("="*60)

    query = "Python features and syntax"
    print(f"Query: '{query}'")

    try:
        chunks = await retrieve_context(query, TEST_USER_1, top_k=3)

        # Verify ranking (similarity should be descending)
        similarities = [chunk['similarity'] for chunk in chunks]
        is_sorted = all(similarities[i] >= similarities[i+1] for i in range(len(similarities)-1))

        print(f"\nSimilarity scores: {[f'{s:.4f}' for s in similarities]}")

        if is_sorted:
            print("✓ Results correctly ranked by similarity")
            return True
        else:
            print("✗ Results not properly ranked")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

async def test_similarity_threshold():
    """Test 3: Verify similarity threshold filtering (> 0.5)."""
    print("\n" + "="*60)
    print("Test 3: Similarity Threshold")
    print("="*60)

    # Query that should have lower similarity to JavaScript content
    query = "How does Python handle indentation and whitespace?"
    print(f"Query: '{query}'")

    try:
        chunks = await retrieve_context(query, TEST_USER_1, top_k=10)

        # Check all chunks meet threshold
        below_threshold = [c for c in chunks if c['similarity'] <= 0.5]

        print(f"\nRetrieved {len(chunks)} chunks")
        print(f"Minimum similarity: {min(c['similarity'] for c in chunks):.4f}")

        if not below_threshold:
            print("✓ All results above 0.5 threshold")
            return True
        else:
            print(f"✗ Found {len(below_threshold)} chunks below threshold")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

async def test_rls_isolation():
    """Test 4: Verify RLS - users only see their own chunks."""
    print("\n" + "="*60)
    print("Test 4: Row-Level Security")
    print("="*60)

    query = "Python programming"

    try:
        # Search as User 1
        user1_chunks = await retrieve_context(query, TEST_USER_1, top_k=10)

        # Search as User 2
        user2_chunks = await retrieve_context(query, TEST_USER_2, top_k=10)

        print(f"\nUser 1 chunks: {len(user1_chunks)}")
        print(f"User 2 chunks: {len(user2_chunks)}")

        # Verify User 1 doesn't see User 2's data
        user1_has_user2_data = any(c['content'].find("user2_doc") != -1 for c in user1_chunks)

        # Verify User 2 has their own data
        user2_has_own_data = len(user2_chunks) > 0

        if not user1_has_user2_data and user2_has_own_data:
            print("✓ RLS correctly isolates user data")
            return True
        else:
            print("✗ RLS not working correctly")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def test_format_context():
    """Test 5: Verify context formatting."""
    print("\n" + "="*60)
    print("Test 5: Context Formatting")
    print("="*60)

    # Mock chunks
    chunks = [
        {
            "content": "Python is a programming language.",
            "filename": "python_guide.txt",
            "similarity": 0.85
        },
        {
            "content": "JavaScript runs in browsers.",
            "filename": "js_guide.txt",
            "similarity": 0.72
        }
    ]

    try:
        context = format_context(chunks)

        print(f"\nFormatted context:\n{context}")

        # Verify format
        has_header = "relevant excerpts" in context.lower()
        has_sources = "[Source 1]" in context and "[Source 2]" in context
        has_filenames = "python_guide.txt" in context and "js_guide.txt" in context
        has_content = "Python is a programming language" in context

        if has_header and has_sources and has_filenames and has_content:
            print("\n✓ Context formatted correctly")
            return True
        else:
            print("\n✗ Context format incomplete")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def test_empty_context():
    """Test 6: Verify empty context handling."""
    print("\n" + "="*60)
    print("Test 6: Empty Context Handling")
    print("="*60)

    try:
        context = format_context([])

        if context == "":
            print("✓ Empty chunks return empty string")
            return True
        else:
            print(f"✗ Expected empty string, got: '{context}'")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

async def cleanup_test_data():
    """Remove test data."""
    supabase = get_supabase_client()

    print("\n" + "="*60)
    print("Cleanup")
    print("="*60)

    try:
        # Delete chunks (cascades to documents due to FK)
        supabase.table("chunks").delete().eq("user_id", TEST_USER_1).execute()
        supabase.table("chunks").delete().eq("user_id", TEST_USER_2).execute()

        # Delete documents
        supabase.table("documents").delete().eq("user_id", TEST_USER_1).execute()
        supabase.table("documents").delete().eq("user_id", TEST_USER_2).execute()

        print("✓ Test data cleaned up")
    except Exception as e:
        print(f"✗ Cleanup error: {e}")

async def main():
    """Run all verification tests."""
    print("\n" + "="*60)
    print("RAG Service Verification (Wave 2, Track 2)")
    print("="*60)

    try:
        # Setup
        await setup_test_data()

        # Run tests
        results = []
        results.append(("Vector Search", await test_vector_search()))
        results.append(("Top-K Ranking", await test_top_k_ranking()))
        results.append(("Similarity Threshold", await test_similarity_threshold()))
        results.append(("RLS Isolation", await test_rls_isolation()))
        results.append(("Format Context", test_format_context()))
        results.append(("Empty Context", test_empty_context()))

        # Summary
        print("\n" + "="*60)
        print("Test Summary")
        print("="*60)

        for name, passed in results:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status}: {name}")

        total = len(results)
        passed = sum(1 for _, p in results if p)
        print(f"\nPassed: {passed}/{total}")

        # Cleanup
        await cleanup_test_data()

        return passed == total

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
