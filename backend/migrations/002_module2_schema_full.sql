-- Module 2: Custom RAG Database Migration
-- Enable pgvector extension and create documents/chunks tables with RLS

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
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
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  embedding VECTOR(1536),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_user_id ON chunks(user_id);

-- RLS policies
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;

-- Documents RLS Policies
DROP POLICY IF EXISTS "Users see own documents" ON documents;
CREATE POLICY "Users see own documents" ON documents
  FOR ALL USING (auth.uid() = user_id);

-- Chunks RLS Policies
DROP POLICY IF EXISTS "Users see own chunks" ON chunks;
CREATE POLICY "Users see own chunks" ON chunks
  FOR ALL USING (auth.uid() = user_id);

-- Vector similarity search index (ivfflat)
-- Note: This requires some data to exist first. If it fails, run it manually after ingesting documents.
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Auto-update updated_at for documents
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
CREATE TRIGGER update_documents_updated_at
  BEFORE UPDATE ON documents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Match chunks function for vector similarity search
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
