#!/usr/bin/env python3
"""
Module 2: Automated Database Migration
Reads DB password from environment variable SUPABASE_DB_PASSWORD
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os
from pathlib import Path
from app.config import Settings

# Read migration SQL from file
migration_file = Path(__file__).parent / "migration_module2.sql"
with open(migration_file, 'r') as f:
    MIGRATION_SQL = f.read()

def run_migration():
    """Execute the migration"""
    try:
        settings = Settings()

        # Extract project ref from URL
        url = settings.supabase_url.replace('https://', '').replace('http://', '')
        project_ref = url.split('.')[0]

        print("=" * 60)
        print("  Module 2: Custom RAG Database Migration (Automated)")
        print("=" * 60)
        print(f"\nProject: {project_ref}")

        # Get password from environment
        db_password = os.getenv('SUPABASE_DB_PASSWORD')

        if not db_password:
            print("\n✗ Error: SUPABASE_DB_PASSWORD environment variable not set")
            print("\nTo set it:")
            print("  export SUPABASE_DB_PASSWORD='your-database-password'")
            print("\nOr run the interactive version:")
            print("  python migrate_module2.py")
            return False

        # Construct connection string using Supabase connection pooler
        # Format: postgresql://postgres.[ref]:[password]@[pooler-host]:6543/postgres
        conn_string = f"postgresql://postgres.{project_ref}:{db_password}@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

        print("\n" + "=" * 60)
        print("  Connecting to Database...")
        print("=" * 60)

        # Connect to database
        conn = psycopg2.connect(conn_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        print("✓ Connected successfully!")

        # Execute migration
        print("\n" + "=" * 60)
        print("  Running Migration...")
        print("=" * 60)

        cursor = conn.cursor()

        # Check if pgvector extension is available
        cursor.execute("SELECT * FROM pg_available_extensions WHERE name = 'vector';")
        if not cursor.fetchone():
            print("✗ Warning: pgvector extension not available")
            print("  Enable it in Supabase Dashboard: Database → Extensions → vector")
            return False

        # Execute migration SQL
        cursor.execute(MIGRATION_SQL)

        print("✓ Migration SQL executed successfully!")

        # Verify tables were created
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('documents', 'chunks')
            ORDER BY table_name;
        """)

        tables = cursor.fetchall()
        print("\n" + "=" * 60)
        print("  Verification")
        print("=" * 60)
        print("✓ Tables created:")
        for table in tables:
            print(f"  - {table[0]}")

        # Check RLS is enabled
        cursor.execute("""
            SELECT tablename, rowsecurity
            FROM pg_tables
            WHERE schemaname = 'public'
            AND tablename IN ('documents', 'chunks');
        """)

        rls_status = cursor.fetchall()
        print("\n✓ Row Level Security:")
        for table, enabled in rls_status:
            status = 'ENABLED' if enabled else 'DISABLED'
            symbol = '✓' if enabled else '✗'
            print(f"  {symbol} {table}: {status}")

        # Verify pgvector extension
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if cursor.fetchone():
            print("\n✓ pgvector extension: ENABLED")
        else:
            print("\n✗ pgvector extension: NOT ENABLED")
            print("  Please enable it in Supabase Dashboard")

        # Verify match_chunks function exists
        cursor.execute("""
            SELECT routine_name
            FROM information_schema.routines
            WHERE routine_schema = 'public'
            AND routine_name = 'match_chunks';
        """)
        if cursor.fetchone():
            print("✓ match_chunks function: CREATED")
        else:
            print("✗ match_chunks function: NOT FOUND")

        # Check vector index
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND indexname = 'chunks_embedding_idx';
        """)
        if cursor.fetchone():
            print("✓ Vector similarity index: CREATED")
        else:
            print("⚠ Vector similarity index: NOT CREATED (normal if no data exists yet)")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("  ✓ Migration Successful!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Create Supabase Storage bucket: 'documents'")
        print("2. Set up RLS policy for the bucket")
        print("3. Run verification: python verify_module2_migration.py")

        return True

    except psycopg2.Error as e:
        print(f"\n✗ Database Error: {e}")
        print("\nTroubleshooting:")
        print("- Verify SUPABASE_DB_PASSWORD is correct")
        print("- Check if pgvector extension is enabled")
        print("- Ensure your IP is allowed in Supabase")
        return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
