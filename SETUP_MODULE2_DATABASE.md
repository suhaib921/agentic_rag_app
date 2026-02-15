# Module 2 Database Setup Guide

This guide walks you through setting up the database for Module 2 (Custom RAG with pgvector).

## Prerequisites

- Supabase project already created (from Module 1)
- Database credentials saved in `backend/.env`

## Step 1: Enable pgvector Extension

1. Go to https://supabase.com/dashboard
2. Select your project
3. Navigate to **Database → Extensions**
4. Search for "vector"
5. Click the toggle to enable **vector** extension
6. Wait for it to activate (usually instant)

## Step 2: Run Database Migration

1. Navigate to **SQL Editor** in Supabase Dashboard
2. Click "New query"
3. Copy the entire contents of `backend/migration_module2.sql`
4. Paste into the SQL editor
5. Click "Run" (or press Cmd/Ctrl + Enter)
6. Verify you see "Success. No rows returned"

### What This Migration Creates:

- **documents table**: Stores document metadata (filename, size, type, status, etc.)
- **chunks table**: Stores document chunks with embeddings (VECTOR(1536) column)
- **RLS policies**: Users can only see their own documents and chunks
- **Indexes**: Performance indexes including vector similarity search (ivfflat)
- **match_chunks function**: Vector similarity search function for RAG queries

## Step 3: Create Storage Bucket

1. Navigate to **Storage** in Supabase Dashboard
2. Click "New bucket"
3. Enter bucket name: `documents`
4. Set **Public bucket**: OFF (unchecked)
5. Click "Create bucket"

## Step 4: Set Up Storage RLS Policy

1. Click on the `documents` bucket
2. Go to **Policies** tab
3. Click "New policy"
4. Select "For full customization" (or use the SQL editor)
5. Paste the following SQL in **SQL Editor**:

```sql
CREATE POLICY "Users can access own documents"
ON storage.objects FOR ALL
USING (
  bucket_id = 'documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

6. Click "Run" to create the policy

### Understanding the Storage Policy

This policy ensures users can only access files in paths like:
- `{their-user-id}/document.pdf` ✓ Allowed
- `{other-user-id}/document.pdf` ✗ Denied

## Step 5: Verify Migration

Run the verification script from the backend directory:

```bash
cd backend
python verify_module2_migration.py
```

This will check:
- ✓ Tables exist (documents, chunks)
- ✓ RLS is enabled on both tables
- ✓ Storage bucket 'documents' exists
- ✓ Pgvector extension is enabled

## Step 6: Manual Verification (Optional)

### Check Tables

1. Go to **Table Editor** in Supabase Dashboard
2. Verify these tables exist:
   - `documents`
   - `chunks`
3. Click on each table and look for the lock icon (🔒) - indicates RLS is enabled

### Check Columns

**documents table should have:**
- id (uuid)
- user_id (uuid)
- filename (text)
- file_size (int4)
- file_type (text)
- storage_path (text)
- status (text)
- error_message (text)
- chunk_count (int4)
- created_at (timestamptz)
- updated_at (timestamptz)

**chunks table should have:**
- id (uuid)
- document_id (uuid)
- user_id (uuid)
- content (text)
- chunk_index (int4)
- embedding (vector(1536)) ← This confirms pgvector is working!
- metadata (jsonb)
- created_at (timestamptz)

### Check Function

Run this in SQL Editor to verify the function exists:

```sql
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name = 'match_chunks';
```

Should return:
- routine_name: match_chunks
- routine_type: FUNCTION

## Troubleshooting

### Error: "type 'vector' does not exist"

**Solution:** Enable the pgvector extension (Step 1)

### Error: "relation 'documents' already exists"

**Solution:** Migration already ran. Safe to ignore or drop tables first:

```sql
DROP TABLE IF EXISTS chunks CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
-- Then re-run migration
```

### Error: "column 'embedding' has type vector but expected type text"

**Solution:** Make sure pgvector extension is enabled before creating tables

### Storage bucket policy not working

**Solution:** Verify the policy SQL uses `auth.uid()::text` (cast to text) and matches the folder structure `{user_id}/filename`

## Testing the Setup

### Test 1: RLS Isolation (Manual)

1. Go to **Authentication → Users**
2. Create two test users (if not already created):
   - user1@test.com
   - user2@test.com
3. Use the verification script or test via API:
   - Upload document as user1
   - Try to access as user2 (should fail)

### Test 2: Vector Search Function

Run in SQL Editor (after you have some chunks with embeddings):

```sql
-- Test match_chunks function
SELECT * FROM match_chunks(
  query_embedding := (SELECT embedding FROM chunks LIMIT 1),
  match_threshold := 0.5,
  match_count := 5,
  user_id_filter := (SELECT user_id FROM chunks LIMIT 1)
);
```

This should return chunk results with similarity scores.

## Next Steps

After successful verification:

1. ✓ Database tables created with RLS
2. ✓ Pgvector extension enabled
3. ✓ Storage bucket created with RLS
4. ✓ Vector search function available

You're ready to implement:
- Document ingestion endpoints (backend)
- Embedding generation (OpenAI text-embedding-3-small)
- RAG query pipeline with vector search
- Document management UI (frontend)

## Files Reference

- **Migration SQL**: `backend/migration_module2.sql`
- **Verification Script**: `backend/verify_module2_migration.py`
- **Module 2 Plan**: `.agent/plans/2.module2-custom-rag.md`
