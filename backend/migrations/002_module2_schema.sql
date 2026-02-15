-- ============================================================
-- Complete Wave 1 & Wave 2 Track 2 Setup
-- ============================================================
-- Run this entire file in Supabase SQL Editor to set up:
-- 1. pgvector extension
-- 2. documents and chunks tables
-- 3. RLS policies
-- 4. Vector search index
-- 5. match_chunks function
-- ============================================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- WAVE 1 TRACK 1: Database Schema
-- ============================================================

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  filename TEXT NOT NULL,
  file_size INTEGER NOT NULL,
  file_type TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'uploaded',
  error_message TEXT,
  chunk_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks table with pgvector
CREATE TABLE IF NOT EXISTS chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id),
  content TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  embedding VECTOR(1536),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS policies
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Users see own documents" ON documents;
DROP POLICY IF EXISTS "Users see own chunks" ON chunks;

-- Create policies
CREATE POLICY "Users see own documents" ON documents
  FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own chunks" ON chunks
  FOR ALL USING (auth.uid() = user_id);

-- Vector similarity search index
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks
  USING ivfflat (embedding vector_cosine_ops);

-- ============================================================
-- WAVE 2 TRACK 2: match_chunks Function
-- ============================================================

CREATE OR REPLACE FUNCTION match_chunks(
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT,
  user_id_filter UUID
)
RETURNS TABLE (
  id UUID,
  document_id UUID,
  content TEXT,
  chunk_index INT,
  similarity FLOAT,
  metadata JSONB,
  filename TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    c.id,
    c.document_id,
    c.content,
    c.chunk_index,
    1 - (c.embedding <=> query_embedding) AS similarity,
    c.metadata,
    d.filename
  FROM chunks c
  JOIN documents d ON c.document_id = d.id
  WHERE
    c.user_id = user_id_filter
    AND 1 - (c.embedding <=> query_embedding) > match_threshold
  ORDER BY c.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- ============================================================
-- Verification Queries
-- ============================================================

-- Check tables exist
SELECT 'Tables created:' as status;
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('documents', 'chunks');

-- Check function exists
SELECT 'Function created:' as status;
SELECT routine_name FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name = 'match_chunks';

-- Check vector extension
SELECT 'Extension enabled:' as status;
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

-- Check RLS is enabled
SELECT 'RLS enabled:' as status;
SELECT tablename, rowsecurity FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('documents', 'chunks');
