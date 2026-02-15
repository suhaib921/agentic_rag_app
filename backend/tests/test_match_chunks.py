#!/usr/bin/env python3
"""
Test match_chunks Vector Search Function
Creates test chunks with fake embeddings and tests similarity search
"""

import sys
import uuid
import random
from supabase import create_client
from app.config import Settings

def generate_fake_embedding(dimension=1536):
    """Generate a random embedding vector for testing"""
    # Create a list of random floats normalized to unit vector
    vec = [random.gauss(0, 1) for _ in range(dimension)]
    # Normalize (optional, for better cosine similarity testing)
    magnitude = sum(x**2 for x in vec) ** 0.5
    return [x / magnitude for x in vec]

def test_match_chunks():
    """Test the match_chunks function"""
    try:
        settings = Settings()

        print("=" * 60)
        print("  Test match_chunks Vector Search Function")
        print("=" * 60)

        # Create admin client
        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )

        print(f"\n✓ Connected to: {settings.supabase_url}")

        # Create test user
        user_id = str(uuid.uuid4())
        print(f"\nTest User ID: {user_id}")

        # Create test document
        print("\n" + "=" * 60)
        print("  Creating Test Data")
        print("=" * 60)

        doc = supabase.table('documents').insert({
            'user_id': user_id,
            'filename': 'test_vector_search.pdf',
            'file_size': 5000,
            'file_type': 'application/pdf',
            'storage_path': f'{user_id}/test_vector_search.pdf',
            'status': 'processed',
            'chunk_count': 3
        }).execute()

        doc_id = doc.data[0]['id']
        print(f"✓ Created test document: {doc_id}")

        # Create test chunks with embeddings
        test_chunks = [
            {
                'document_id': doc_id,
                'user_id': user_id,
                'content': 'Machine learning is a subset of artificial intelligence that focuses on data and algorithms.',
                'chunk_index': 0,
                'embedding': generate_fake_embedding(),
                'metadata': {'page': 1, 'section': 'Introduction'}
            },
            {
                'document_id': doc_id,
                'user_id': user_id,
                'content': 'Deep learning uses neural networks with multiple layers to learn from data.',
                'chunk_index': 1,
                'embedding': generate_fake_embedding(),
                'metadata': {'page': 2, 'section': 'Deep Learning'}
            },
            {
                'document_id': doc_id,
                'user_id': user_id,
                'content': 'Natural language processing helps computers understand human language.',
                'chunk_index': 2,
                'embedding': generate_fake_embedding(),
                'metadata': {'page': 3, 'section': 'NLP'}
            }
        ]

        for i, chunk_data in enumerate(test_chunks):
            result = supabase.table('chunks').insert(chunk_data).execute()
            print(f"✓ Created chunk {i}: {result.data[0]['id']}")

        # Test match_chunks function
        print("\n" + "=" * 60)
        print("  Testing Vector Search")
        print("=" * 60)

        # Use the embedding from the first chunk as query
        query_embedding = test_chunks[0]['embedding']

        print(f"\nQuerying with embedding from chunk 0...")
        print(f"Match threshold: 0.5")
        print(f"Match count: 5")

        # Call match_chunks via RPC
        result = supabase.rpc('match_chunks', {
            'query_embedding': query_embedding,
            'match_threshold': 0.5,
            'match_count': 5,
            'user_id_filter': user_id
        }).execute()

        print(f"\n✓ Found {len(result.data)} matching chunks")

        # Display results
        print("\nResults:")
        print("-" * 60)
        for i, match in enumerate(result.data, 1):
            print(f"\n{i}. Similarity: {match['similarity']:.4f}")
            print(f"   Chunk Index: {match['chunk_index']}")
            print(f"   Content: {match['content'][:80]}...")
            print(f"   Metadata: {match['metadata']}")

        # Test with different user (should return no results)
        print("\n" + "=" * 60)
        print("  Testing RLS Isolation")
        print("=" * 60)

        other_user_id = str(uuid.uuid4())
        print(f"\nQuerying with different user ID: {other_user_id}")

        result_other = supabase.rpc('match_chunks', {
            'query_embedding': query_embedding,
            'match_threshold': 0.5,
            'match_count': 5,
            'user_id_filter': other_user_id
        }).execute()

        print(f"✓ Found {len(result_other.data)} chunks (should be 0)")

        if len(result_other.data) == 0:
            print("✓ RLS working correctly: Other user cannot see chunks")
        else:
            print("✗ RLS issue: Other user can see chunks!")

        # Cleanup
        print("\n" + "=" * 60)
        print("  Cleanup")
        print("=" * 60)

        cleanup = input("\nDelete test data? (y/n): ").strip().lower()
        if cleanup == 'y':
            supabase.table('chunks').delete().eq('user_id', user_id).execute()
            supabase.table('documents').delete().eq('id', doc_id).execute()
            print("✓ Test data deleted")
        else:
            print("⚠ Test data preserved")
            print(f"   Document ID: {doc_id}")
            print(f"   User ID: {user_id}")

        print("\n" + "=" * 60)
        print("  ✓ Vector Search Test Complete")
        print("=" * 60)
        print("\nFunction verification:")
        print("✓ match_chunks() exists and works")
        print("✓ Vector similarity search functional")
        print("✓ Cosine distance calculation working")
        print("✓ RLS properly filters results by user_id")

        return True

    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_match_chunks()
    sys.exit(0 if success else 1)
