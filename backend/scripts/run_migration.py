#!/usr/bin/env python3
"""
Run Supabase database migration
Creates tables, indexes, RLS policies, and triggers
"""

import os
from supabase import create_client, Client
from app.config import settings

# SQL Migration Script
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
DROP POLICY IF EXISTS "Users can view their own threads" ON threads;
CREATE POLICY "Users can view their own threads"
  ON threads FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own threads" ON threads;
CREATE POLICY "Users can insert their own threads"
  ON threads FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update their own threads" ON threads;
CREATE POLICY "Users can update their own threads"
  ON threads FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete their own threads" ON threads;
CREATE POLICY "Users can delete their own threads"
  ON threads FOR DELETE USING (auth.uid() = user_id);

-- Messages RLS Policies (drop if exists to avoid duplicates)
DROP POLICY IF EXISTS "Users can view their own messages" ON messages;
CREATE POLICY "Users can view their own messages"
  ON messages FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own messages" ON messages;
CREATE POLICY "Users can insert their own messages"
  ON messages FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update their own messages" ON messages;
CREATE POLICY "Users can update their own messages"
  ON messages FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete their own messages" ON messages;
CREATE POLICY "Users can delete their own messages"
  ON messages FOR DELETE USING (auth.uid() = user_id);

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

def run_migration():
    """Execute the database migration using Supabase Management API"""
    print("=" * 60)
    print("  Running Database Migration")
    print("=" * 60)

    try:
        # We need to use the REST API directly to execute SQL
        import requests

        # Extract project ref from URL (e.g., https://PROJECT_REF.supabase.co)
        url_parts = settings.supabase_url.replace('https://', '').split('.')
        project_ref = url_parts[0]

        # Supabase SQL execution endpoint
        # Note: This uses the pg_net extension or direct SQL execution
        # We'll use the rpc endpoint with a custom function

        print("\nTo run this migration, you have a few options:\n")
        print("Option 1: Manual (Recommended)")
        print("-" * 60)
        print("1. Go to: https://supabase.com/dashboard/project/" + project_ref + "/sql")
        print("2. Click 'New Query'")
        print("3. Copy the SQL from: agentic_rag_app/SETUP_SUPABASE.md")
        print("4. Click 'Run'\n")

        print("Option 2: Using psql command line")
        print("-" * 60)
        print("You can get the connection string from:")
        print("Supabase Dashboard → Project Settings → Database → Connection String")
        print("Then run: psql '<connection_string>' -f migration.sql\n")

        print("Option 3: I'll create a migration.sql file for you")
        print("-" * 60)

        # Write SQL to a file
        with open('migration.sql', 'w') as f:
            f.write(MIGRATION_SQL)

        print("✓ Created migration.sql file")
        print("\nYou can now:")
        print("1. Copy the contents of migration.sql")
        print("2. Paste into Supabase SQL Editor")
        print("3. Click 'Run'\n")

        print("=" * 60)
        print("  Migration file ready!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    run_migration()
