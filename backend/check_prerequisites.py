"""
Check if Wave 1 prerequisites are met before running Wave 2 Track 2 verification.
"""

from app.db.supabase import get_supabase_client

def check_prerequisites():
    """Check if all Wave 1 dependencies are in place."""
    supabase = get_supabase_client()

    checks = []

    print("="*60)
    print("Wave 2 Track 2 Prerequisites Check")
    print("="*60)

    # Check 1: Documents table
    print("\n1. Checking documents table...")
    try:
        supabase.table('documents').select('id').limit(1).execute()
        print("   ✓ documents table exists")
        checks.append(True)
    except Exception as e:
        print(f"   ✗ documents table missing: {e}")
        checks.append(False)

    # Check 2: Chunks table
    print("\n2. Checking chunks table...")
    try:
        supabase.table('chunks').select('id').limit(1).execute()
        print("   ✓ chunks table exists")
        checks.append(True)
    except Exception as e:
        print(f"   ✗ chunks table missing: {e}")
        checks.append(False)

    # Check 3: match_chunks function
    print("\n3. Checking match_chunks function...")
    try:
        supabase.rpc('match_chunks', {
            'query_embedding': [0.0] * 1536,
            'match_threshold': 0.5,
            'match_count': 1,
            'user_id_filter': '00000000-0000-0000-0000-000000000000'
        }).execute()
        print("   ✓ match_chunks function exists")
        checks.append(True)
    except Exception as e:
        print(f"   ✗ match_chunks function missing: {e}")
        checks.append(False)

    # Check 4: Embeddings service
    print("\n4. Checking embeddings service...")
    try:
        from app.services.embeddings import generate_embedding
        print("   ✓ embeddings service exists")
        checks.append(True)
    except Exception as e:
        print(f"   ✗ embeddings service missing: {e}")
        checks.append(False)

    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    passed = sum(checks)
    total = len(checks)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ All prerequisites met! You can run verify_rag_service.py")
        return True
    else:
        print("\n✗ Prerequisites missing. Follow SETUP_WAVE2_TRACK2.md")
        print("\nRequired steps:")
        if not checks[0] or not checks[1]:
            print("  1. Run Wave 1 Track 1 SQL in Supabase SQL Editor")
        if not checks[2]:
            print("  2. Run migrations/002_match_chunks_function.sql in Supabase SQL Editor")
        if not checks[3]:
            print("  3. Verify embeddings service is configured")
        return False

if __name__ == "__main__":
    success = check_prerequisites()
    exit(0 if success else 1)
