# Phase 3: Supabase Setup (MANUAL STEP)

⚠️ **This step must be completed manually before the application can run**

## 1. Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Enter project details:
   - **Name:** agentic-rag-app
   - **Database Password:** (create a strong password)
   - **Region:** Choose closest to you
4. Click "Create new project" and wait for provisioning (~2 minutes)

## 2. Save Credentials

After project creation, save these values to `backend/.env` and `frontend/.env`:

From **Project Settings → API**:
- `SUPABASE_URL` → Project URL
- `SUPABASE_ANON_KEY` → anon/public key
- `SUPABASE_SERVICE_ROLE_KEY` → service_role key (keep secret!)

## 3. Run Database Migration

1. Go to **SQL Editor** in Supabase Dashboard
2. Click "New query"
3. Copy and paste the SQL from below
4. Click "Run" to execute

### SQL Migration

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Threads table
CREATE TABLE threads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  openai_thread_id TEXT NOT NULL UNIQUE,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  openai_message_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_threads_user_id ON threads(user_id);
CREATE INDEX idx_threads_openai_thread_id ON threads(openai_thread_id);
CREATE INDEX idx_messages_thread_id ON messages(thread_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Enable RLS
ALTER TABLE threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Threads RLS Policies
CREATE POLICY "Users can view their own threads"
  ON threads FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own threads"
  ON threads FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own threads"
  ON threads FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own threads"
  ON threads FOR DELETE USING (auth.uid() = user_id);

-- Messages RLS Policies
CREATE POLICY "Users can view their own messages"
  ON messages FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own messages"
  ON messages FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own messages"
  ON messages FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own messages"
  ON messages FOR DELETE USING (auth.uid() = user_id);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_threads_updated_at
  BEFORE UPDATE ON threads
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

## 4. Verify Setup

1. Go to **Table Editor** in Supabase Dashboard
2. Check that `threads` and `messages` tables exist
3. Click on each table → Check for lock icon (indicates RLS is enabled)
4. Go to **Authentication → Policies** → Verify RLS policies are listed

## 5. Create Test User

1. Go to **Authentication → Users**
2. Click "Add User" → "Create new user"
3. Enter email and password for testing
4. Click "Create User"
5. Save these credentials for testing the application

✅ **Done!** Your Supabase database is ready.
