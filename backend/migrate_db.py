#!/usr/bin/env python3
"""
Supabase Database Migration Script
Connects directly to PostgreSQL and creates schema
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from app.config import settings

# SQL Migration
MIGRATION_SQL = """
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Threads table
CREATE TABLE IF NOT EXISTS threads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  openai_thread_id TEXT NOT NULL UNIQUE,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  openai_message_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_threads_user_id ON threads(user_id);
CREATE INDEX IF NOT EXISTS idx_threads_openai_thread_id ON threads(openai_thread_id);
CREATE INDEX IF NOT EXISTS idx_messages_thread_id ON messages(thread_id);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- Enable RLS
ALTER TABLE threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Threads RLS Policies (drop if exists to avoid duplicates)
DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can view their own threads" ON threads;
    CREATE POLICY "Users can view their own threads"
      ON threads FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can insert their own threads" ON threads;
    CREATE POLICY "Users can insert their own threads"
      ON threads FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can update their own threads" ON threads;
    CREATE POLICY "Users can update their own threads"
      ON threads FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can delete their own threads" ON threads;
    CREATE POLICY "Users can delete their own threads"
      ON threads FOR DELETE USING (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

-- Messages RLS Policies
DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can view their own messages" ON messages;
    CREATE POLICY "Users can view their own messages"
      ON messages FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can insert their own messages" ON messages;
    CREATE POLICY "Users can insert their own messages"
      ON messages FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can update their own messages" ON messages;
    CREATE POLICY "Users can update their own messages"
      ON messages FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

DO $$ BEGIN
    DROP POLICY IF EXISTS "Users can delete their own messages" ON messages;
    CREATE POLICY "Users can delete their own messages"
      ON messages FOR DELETE USING (auth.uid() = user_id);
EXCEPTION WHEN OTHERS THEN NULL; END $$;

-- Auto-update updated_at function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updated_at
DROP TRIGGER IF EXISTS update_threads_updated_at ON threads;
CREATE TRIGGER update_threads_updated_at
  BEFORE UPDATE ON threads
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
"""

def get_db_connection_string():
    """Construct PostgreSQL connection string from Supabase URL"""
    # Extract project ref from URL
    url = settings.supabase_url.replace('https://', '').replace('http://', '')
    project_ref = url.split('.')[0]

    # Construct database host
    db_host = f"db.{project_ref}.supabase.co"

    print("=" * 60)
    print("  Database Migration Setup")
    print("=" * 60)
    print(f"\nProject Reference: {project_ref}")
    print(f"Database Host: {db_host}")
    print("\nTo get your database password:")
    print("1. Go to: https://supabase.com/dashboard/project/" + project_ref + "/settings/database")
    print("2. Look for 'Database Password' (the one you set when creating the project)")
    print("3. If you forgot it, you can reset it on that page")
    print("\nOR use the Connection String from that same page")

    db_password = input("\nEnter your database password (or press Enter to use connection string): ").strip()

    if db_password:
        return f"postgresql://postgres:{db_password}@{db_host}:5432/postgres"
    else:
        conn_string = input("Paste your full connection string: ").strip()
        return conn_string

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
        cursor.execute(MIGRATION_SQL)

        print("✓ Migration completed successfully!")

        # Verify tables were created
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('threads', 'messages')
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
            AND tablename IN ('threads', 'messages');
        """)

        rls_status = cursor.fetchall()
        print("\n✓ Row Level Security:")
        for table, enabled in rls_status:
            print(f"  - {table}: {'ENABLED' if enabled else 'DISABLED'}")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("  ✓ Migration Successful!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run: python test_validation.py")
        print("2. Open browser to: http://localhost:5173")
        print("3. Test the application!")

        return True

    except psycopg2.Error as e:
        print(f"\n✗ Database Error: {e}")
        print("\nTroubleshooting:")
        print("- Verify your database password is correct")
        print("- Check your connection string")
        print("- Ensure your IP is allowed in Supabase (Settings → Database → Connection Pooling)")
        return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
