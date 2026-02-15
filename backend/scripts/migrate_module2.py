#!/usr/bin/env python3
"""
Module 2: Custom RAG Database Migration Script
Enables pgvector and creates documents/chunks tables with RLS
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from app.config import settings

# Read migration SQL from file
with open('migration_module2.sql', 'r') as f:
    MIGRATION_SQL = f.read()

def get_db_connection_string():
    """Construct PostgreSQL connection string from Supabase URL"""
    # Extract project ref from URL
    url = settings.supabase_url.replace('https://', '').replace('http://', '')
    project_ref = url.split('.')[0]

    # Construct database host
    db_host = f"db.{project_ref}.supabase.co"

    print("=" * 60)
    print("  Module 2: Custom RAG Database Migration")
    print("=" * 60)
    print(f"\nProject Reference: {project_ref}")
    print(f"Database Host: {db_host}")
    print(f"\nProject URL: https://supabase.com/dashboard/project/{project_ref}")
    print("\n" + "=" * 60)
    print("  Database Connection Options")
    print("=" * 60)
    print("\nOption 1: Direct Connection String (Recommended)")
    print("  1. Go to: Project Settings → Database")
    print("  2. Find 'Connection String' section")
    print("  3. Select 'URI' tab")
    print("  4. Copy the connection string")
    print("  5. Replace [YOUR-PASSWORD] with your actual database password")
    print("\nOption 2: Password Only")
    print("  Enter just your database password (from when you created the project)")

    print("\n" + "=" * 60)

    choice = input("\nEnter connection string OR password (or 'q' to quit): ").strip()

    if choice.lower() == 'q':
        print("Migration cancelled.")
        sys.exit(0)

    # Check if it looks like a full connection string
    if choice.startswith('postgresql://') or choice.startswith('postgres://'):
        return choice
    else:
        # Treat as password
        return f"postgresql://postgres.{project_ref}:{choice}@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

def run_migration():
    """Execute the migration"""
    try:
        # Get connection string
        conn_string = get_db_connection_string()

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
            print("✗ Warning: pgvector extension not available in this database")
            print("  You may need to enable it in Supabase dashboard first")
            return False

        cursor.execute(MIGRATION_SQL)

        print("✓ Migration completed successfully!")

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
            print(f"  - {table}: {'ENABLED' if enabled else 'DISABLED'}")

        # Verify pgvector extension
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if cursor.fetchone():
            print("\n✓ pgvector extension: ENABLED")
        else:
            print("\n✗ pgvector extension: NOT ENABLED")

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

        # Check vector index (may not exist if no data yet)
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND indexname = 'chunks_embedding_idx';
        """)
        if cursor.fetchone():
            print("✓ Vector similarity index: CREATED")
        else:
            print("⚠ Vector similarity index: NOT CREATED (this is normal if no data exists yet)")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("  ✓ Migration Successful!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Create Supabase Storage bucket named 'documents'")
        print("2. Set up RLS policy for the bucket (users can only access {user_id}/* paths)")
        print("3. Test the document ingestion workflow")

        return True

    except psycopg2.Error as e:
        print(f"\n✗ Database Error: {e}")
        print("\nTroubleshooting:")
        print("- Verify your database password is correct")
        print("- Check your connection string")
        print("- Ensure your IP is allowed in Supabase (Settings → Database → Connection Pooling)")
        print("- Make sure pgvector extension is available in Supabase")
        return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
