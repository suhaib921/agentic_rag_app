-- Create vector similarity search function for RAG retrieval
-- This function must be run in Supabase SQL Editor

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
