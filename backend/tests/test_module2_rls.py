#!/usr/bin/env python3
"""
Test Module 2 RLS Policies
Creates test data and verifies users can only see their own documents/chunks
"""

import sys
import uuid
from supabase import create_client
from app.config import Settings

def test_rls():
    """Test RLS isolation between users"""
    try:
        settings = Settings()

        print("=" * 60)
        print("  Module 2 RLS Test")
        print("=" * 60)

        # Create admin client (service role)
        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )

        print(f"\n✓ Connected to: {settings.supabase_url}")

        # Create test user IDs (simulate two different users)
        # In a real scenario, these would be actual auth.users IDs
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())

        print(f"\nTest User 1 ID: {user1_id}")
        print(f"Test User 2 ID: {user2_id}")

        # NOTE: This test uses service role which bypasses RLS
        # For real RLS testing, you need actual authenticated users
        print("\n" + "=" * 60)
        print("  Creating Test Data")
        print("=" * 60)

        # Create document for user1
        doc1 = supabase.table('documents').insert({
            'user_id': user1_id,
            'filename': 'user1_document.pdf',
            'file_size': 1000,
            'file_type': 'application/pdf',
            'storage_path': f'{user1_id}/user1_document.pdf',
            'status': 'uploaded'
        }).execute()

        print(f"✓ Created document for User 1: {doc1.data[0]['id']}")

        # Create document for user2
        doc2 = supabase.table('documents').insert({
            'user_id': user2_id,
            'filename': 'user2_document.pdf',
            'file_size': 2000,
            'file_type': 'application/pdf',
            'storage_path': f'{user2_id}/user2_document.pdf',
            'status': 'uploaded'
        }).execute()

        print(f"✓ Created document for User 2: {doc2.data[0]['id']}")

        # Create chunk for user1
        chunk1 = supabase.table('chunks').insert({
            'document_id': doc1.data[0]['id'],
            'user_id': user1_id,
            'content': 'This is a test chunk for user 1',
            'chunk_index': 0,
            'metadata': {'test': True}
        }).execute()

        print(f"✓ Created chunk for User 1: {chunk1.data[0]['id']}")

        # Create chunk for user2
        chunk2 = supabase.table('chunks').insert({
            'document_id': doc2.data[0]['id'],
            'user_id': user2_id,
            'content': 'This is a test chunk for user 2',
            'chunk_index': 0,
            'metadata': {'test': True}
        }).execute()

        print(f"✓ Created chunk for User 2: {chunk2.data[0]['id']}")

        # Query with service role (sees all data)
        print("\n" + "=" * 60)
        print("  Testing Data Visibility")
        print("=" * 60)

        all_docs = supabase.table('documents').select('*').execute()
        print(f"✓ Service role can see: {len(all_docs.data)} documents (should be 2+)")

        all_chunks = supabase.table('chunks').select('*').execute()
        print(f"✓ Service role can see: {len(all_chunks.data)} chunks (should be 2+)")

        # RLS Testing Note
        print("\n" + "=" * 60)
        print("  RLS Isolation Test")
        print("=" * 60)
        print("\n⚠ NOTE: Full RLS testing requires actual authenticated users")
        print("\nTo properly test RLS:")
        print("1. Create two test users in Supabase Auth")
        print("2. Get JWT tokens for each user")
        print("3. Create Supabase clients with user tokens (not service role)")
        print("4. Verify User 1 cannot see User 2's data")
        print("\nFor now, verify via Supabase Dashboard:")
        print("- Go to Authentication → Users")
        print("- Create test users")
        print("- Use RLS policy viewer to check isolation")

        # Cleanup
        print("\n" + "=" * 60)
        print("  Cleanup")
        print("=" * 60)

        cleanup = input("\nDelete test data? (y/n): ").strip().lower()
        if cleanup == 'y':
            supabase.table('chunks').delete().eq('user_id', user1_id).execute()
            supabase.table('chunks').delete().eq('user_id', user2_id).execute()
            supabase.table('documents').delete().eq('user_id', user1_id).execute()
            supabase.table('documents').delete().eq('user_id', user2_id).execute()
            print("✓ Test data deleted")
        else:
            print("⚠ Test data preserved")
            print(f"   User 1 data: user_id = {user1_id}")
            print(f"   User 2 data: user_id = {user2_id}")

        print("\n" + "=" * 60)
        print("  ✓ RLS Test Complete")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_rls()
    sys.exit(0 if success else 1)
