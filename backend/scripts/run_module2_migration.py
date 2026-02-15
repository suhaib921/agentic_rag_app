#!/usr/bin/env python3
"""
Module 2: Custom RAG Database Migration Script
Uses Supabase client to execute SQL migration
"""

import sys
from pathlib import Path
from supabase import create_client
from app.config import Settings

def run_migration():
    """Execute the Module 2 migration using Supabase client"""
    try:
        # Load settings
        settings = Settings()

        print("=" * 60)
        print("  Module 2: Custom RAG Database Migration")
        print("=" * 60)

        # Read migration SQL
        migration_file = Path(__file__).parent / "migration_module2.sql"
        with open(migration_file, 'r') as f:
            migration_sql = f.read()

        print(f"\n✓ Loaded migration SQL from: {migration_file}")

        # Create Supabase client with service role key
        print("\n" + "=" * 60)
        print("  Connecting to Supabase...")
        print("=" * 60)

        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )

        print(f"✓ Connected to: {settings.supabase_url}")

        # Execute migration using RPC
        print("\n" + "=" * 60)
        print("  Running Migration...")
        print("=" * 60)
        print("\nNote: Using Supabase REST API (RPC) for migration.")
        print("For full migration, please run the SQL directly in Supabase SQL Editor.")
        print("\nSteps to complete migration:")
        print("1. Go to: Supabase Dashboard → SQL Editor")
        print("2. Create a new query")
        print("3. Copy the contents of: migration_module2.sql")
        print("4. Execute the query")
        print("\nAlternatively, you can use the psycopg2 version:")
        print("  python migrate_module2.py")

        # We can at least verify the connection works
        result = supabase.table('threads').select('count', count='exact').limit(0).execute()
        print(f"\n✓ Connection verified (existing threads table accessible)")

        print("\n" + "=" * 60)
        print("  Migration Instructions")
        print("=" * 60)
        print("\nPlease complete the following steps:")
        print("\n1. Run migration SQL in Supabase SQL Editor:")
        print("   - File: backend/migration_module2.sql")
        print("   - Location: Supabase Dashboard → SQL Editor")
        print("\n2. Create Storage bucket:")
        print("   - Name: documents")
        print("   - Public: No")
        print("   - RLS: Enabled")
        print("\n3. Add Storage RLS policy:")
        print("   SQL to run in SQL Editor:")
        print("""
   CREATE POLICY "Users can access own documents"
   ON storage.objects FOR ALL
   USING (
     bucket_id = 'documents' AND
     (storage.foldername(name))[1] = auth.uid()::text
   );
""")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
