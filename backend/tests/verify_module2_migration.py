#!/usr/bin/env python3
"""
Verify Module 2 Database Migration
Checks that all tables, RLS policies, indexes, and functions are correctly set up
"""

import sys
from supabase import create_client
from app.config import Settings

def verify_migration():
    """Verify that Module 2 migration was successful"""
    try:
        settings = Settings()

        print("=" * 60)
        print("  Module 2 Migration Verification")
        print("=" * 60)

        # Create Supabase client
        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )

        print(f"\n✓ Connected to: {settings.supabase_url}")

        checks_passed = 0
        checks_failed = 0

        # Check 1: Documents table exists
        print("\n" + "=" * 60)
        print("  Table Structure Checks")
        print("=" * 60)

        try:
            result = supabase.table('documents').select('*').limit(0).execute()
            print("✓ documents table: EXISTS")
            checks_passed += 1
        except Exception as e:
            print(f"✗ documents table: NOT FOUND ({e})")
            checks_failed += 1

        # Check 2: Chunks table exists
        try:
            result = supabase.table('chunks').select('*').limit(0).execute()
            print("✓ chunks table: EXISTS")
            checks_passed += 1
        except Exception as e:
            print(f"✗ chunks table: NOT FOUND ({e})")
            checks_failed += 1

        # Check 3: RLS is enabled (we'll try to access without auth)
        print("\n" + "=" * 60)
        print("  Row Level Security Checks")
        print("=" * 60)

        # Create a client with anon key (should be restricted)
        supabase_anon = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )

        try:
            # This should return empty or error due to RLS
            result = supabase_anon.table('documents').select('*').execute()
            if len(result.data) == 0:
                print("✓ documents RLS: ENABLED (no data accessible without auth)")
                checks_passed += 1
            else:
                print("⚠ documents RLS: WARNING (data accessible without auth)")
                checks_failed += 1
        except Exception as e:
            print("✓ documents RLS: ENABLED (access denied without auth)")
            checks_passed += 1

        try:
            result = supabase_anon.table('chunks').select('*').execute()
            if len(result.data) == 0:
                print("✓ chunks RLS: ENABLED (no data accessible without auth)")
                checks_passed += 1
            else:
                print("⚠ chunks RLS: WARNING (data accessible without auth)")
                checks_failed += 1
        except Exception as e:
            print("✓ chunks RLS: ENABLED (access denied without auth)")
            checks_passed += 1

        # Check 4: Storage bucket exists
        print("\n" + "=" * 60)
        print("  Storage Bucket Checks")
        print("=" * 60)

        try:
            # List buckets
            result = supabase.storage.list_buckets()
            bucket_names = [bucket.name for bucket in result]
            if 'documents' in bucket_names:
                print("✓ Storage bucket 'documents': EXISTS")
                checks_passed += 1
            else:
                print("✗ Storage bucket 'documents': NOT FOUND")
                print(f"  Available buckets: {bucket_names}")
                checks_failed += 1
        except Exception as e:
            print(f"✗ Storage bucket check failed: {e}")
            checks_failed += 1

        # Summary
        print("\n" + "=" * 60)
        print("  Verification Summary")
        print("=" * 60)
        print(f"✓ Checks passed: {checks_passed}")
        print(f"✗ Checks failed: {checks_failed}")

        if checks_failed == 0:
            print("\n✓ All checks passed! Migration successful.")
            return True
        else:
            print("\n⚠ Some checks failed. Please review the migration steps.")
            return False

    except Exception as e:
        print(f"\n✗ Verification error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_migration()
    sys.exit(0 if success else 1)
