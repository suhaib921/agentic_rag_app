# Backend - Agentic RAG Application

Module 2: Custom RAG with Multi-Provider LLM Support

## Quick Start

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run development server
uvicorn app.main:app --reload
```

## Database Setup

### Prerequisites
- Supabase project created
- Service role key and anon key available

### Setup Steps

#### 1. Enable pgvector Extension
1. Go to Supabase Dashboard → Database → Extensions
2. Search for "vector" and toggle **ON**

#### 2. Run Migration
1. Go to Supabase Dashboard → SQL Editor
2. Copy contents of `migration_module2.sql`
3. Paste and run (Cmd+Enter / Ctrl+Enter)

#### 3. Create Storage Bucket
1. Go to Supabase Dashboard → Storage
2. Click "New bucket"
3. Name: `documents`, Public: **OFF**
4. Click "Create bucket"

#### 4. Add Storage RLS Policy
Run in SQL Editor:
```sql
CREATE POLICY "Users can access own documents"
ON storage.objects FOR ALL
USING (
  bucket_id = 'documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

#### 5. Verify Setup
```bash
python tests/verify_module2_migration.py
```

Expected output:
```
✓ documents table: EXISTS
✓ chunks table: EXISTS
✓ documents RLS: ENABLED
✓ chunks RLS: ENABLED
✓ Storage bucket 'documents': EXISTS
```

## Database Schema

### Tables

#### documents
Stores uploaded document metadata.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to auth.users |
| filename | TEXT | Original filename |
| file_size | INTEGER | File size in bytes |
| file_type | TEXT | File type (pdf, txt, md, docx) |
| storage_path | TEXT | Path in Supabase Storage |
| status | TEXT | uploaded, processing, chunking, embedding, completed, failed |
| error_message | TEXT | Error details if failed |
| chunk_count | INTEGER | Number of chunks created |
| created_at | TIMESTAMPTZ | Upload timestamp |
| updated_at | TIMESTAMPTZ | Auto-updated |

**RLS:** Users only see their own documents (`auth.uid() = user_id`)

#### chunks
Stores document chunks with vector embeddings.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| document_id | UUID | Foreign key to documents |
| user_id | UUID | Foreign key to auth.users |
| content | TEXT | Chunk text content |
| chunk_index | INTEGER | Sequential index in document |
| embedding | VECTOR(1536) | OpenAI embedding vector |
| metadata | JSONB | Additional metadata |
| created_at | TIMESTAMPTZ | Creation timestamp |

**RLS:** Users only see their own chunks (`auth.uid() = user_id`)

**Indexes:**
- ivfflat index on embedding for vector similarity search
- B-tree indexes on user_id and document_id

### Functions

#### match_chunks()
Vector similarity search for RAG queries.

**Parameters:**
- `query_embedding` VECTOR(1536) - Query vector
- `match_threshold` FLOAT - Minimum similarity (0.0-1.0)
- `match_count` INT - Max results to return
- `user_id_filter` UUID - User ID for RLS

**Returns:**
- id, document_id, content, chunk_index, similarity, metadata, filename

**Usage:**
```sql
SELECT * FROM match_chunks(
  query_embedding := (SELECT embedding FROM chunks LIMIT 1),
  match_threshold := 0.5,
  match_count := 5,
  user_id_filter := auth.uid()
);
```

## Architecture

### Services

#### LLM Providers (`app/services/llm/`)
- **base.py**: BaseLLMProvider interface
- **factory.py**: Provider factory
- **openai_provider.py**: OpenAI implementation
- **openrouter_provider.py**: OpenRouter implementation
- **generic_provider.py**: Ollama/LM Studio support

#### Core Services
- **embeddings.py**: OpenAI embedding generation
- **ingestion_service.py**: Document processing pipeline (extract → chunk → embed)
- **rag_service.py**: Vector retrieval and context formatting

### API Endpoints (`app/api/`)

#### Documents (`/api/documents`)
- `POST /api/documents` - Upload document
- `GET /api/documents` - List user's documents
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document

#### Chat (`/api/chat`)
- `POST /api/chat/threads` - Create thread
- `GET /api/chat/threads` - List threads
- `POST /api/chat/messages` - Send message (RAG-enhanced, SSE streaming)

## Configuration

### Environment Variables

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_ANON_KEY=eyJ...

# OpenAI (for embeddings)
OPENAI_API_KEY=sk-...

# LLM Provider
CHAT_PROVIDER=openai  # openai, openrouter, ollama, lmstudio
CHAT_MODEL=gpt-4o
CHAT_API_KEY=sk-...
CHAT_BASE_URL=  # For ollama/lmstudio (e.g., http://localhost:11434/v1)

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small

# LangSmith (optional)
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_PROJECT=agentic-rag-module2

# CORS
CORS_ORIGINS=http://localhost:5173
```

### Multi-Provider Setup

**OpenAI:**
```bash
CHAT_PROVIDER=openai
CHAT_MODEL=gpt-4o
CHAT_API_KEY=sk-...
```

**OpenRouter:**
```bash
CHAT_PROVIDER=openrouter
CHAT_MODEL=anthropic/claude-3.5-sonnet
CHAT_API_KEY=sk-or-v1-...
```

**Ollama:**
```bash
CHAT_PROVIDER=ollama
CHAT_MODEL=llama3.2
CHAT_BASE_URL=http://localhost:11434/v1
```

## Testing

### Automated Tests
```bash
# Full validation suite
python tests/wave5_validation.py

# Individual tests
python tests/test_module2_complete.py
python tests/test_module2_rls.py
python tests/test_match_chunks.py
python tests/test_llm_providers.py
python tests/test_wave3_endpoints.py

# Verification scripts
python tests/verify_module2_migration.py
python tests/verify_rag_service.py
```

### Manual Testing
See `../WAVE5_MANUAL_TESTING.md` for browser testing guide.

## Data Flow

### Document Ingestion
```
1. Upload file → Supabase Storage
2. Create document record (status: uploaded)
3. Extract text (pypdf/python-docx)
4. Chunk text (1000 tokens, 200 overlap)
5. Generate embeddings (OpenAI API)
6. Store chunks with embeddings
7. Update document (status: completed, chunk_count)
```

### RAG Query
```
1. User message
2. Generate query embedding
3. Vector search (match_chunks)
4. Format context with sources
5. Send to LLM provider
6. Stream response via SSE
7. Save to messages table
```

## Troubleshooting

### "type 'vector' does not exist"
→ Enable pgvector extension in Supabase

### "function update_updated_at() does not exist"
→ Run Module 1 migration first (creates shared function)

### "relation already exists"
→ Safe to ignore, or drop and recreate:
```sql
DROP TABLE IF EXISTS chunks CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
```

### Import errors
→ Activate virtual environment:
```bash
source venv/bin/activate
```

### Supabase connection fails
→ Check credentials in `.env`, verify service role key

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── chat.py       # Chat with RAG
│   │   └── documents.py  # Document management
│   ├── auth/             # Authentication
│   │   └── middleware.py # JWT verification
│   ├── db/               # Database
│   │   └── supabase.py   # Supabase client
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   │   ├── llm/          # LLM providers
│   │   ├── embeddings.py
│   │   ├── ingestion_service.py
│   │   └── rag_service.py
│   ├── config.py         # Settings
│   └── main.py           # FastAPI app
├── migrations/           # SQL migrations
├── tests/                # Test files
├── .env                  # Environment config
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Dependencies

Key packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `supabase` - Supabase client
- `openai` - OpenAI API
- `langsmith` - LangSmith tracing
- `pypdf` - PDF text extraction
- `python-docx` - DOCX processing
- `tiktoken` - Token counting
- `pgvector` - Vector type support

See `requirements.txt` for full list.

## Development

### Run server
```bash
uvicorn app.main:app --reload
```

### Access API docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Enable debug logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security

### Row-Level Security (RLS)
All tables enforce user isolation:
- Users only see their own documents
- Users only see chunks from their documents
- Users only access their own storage files
- Vector search automatically filters by user_id

### Authentication
- JWT tokens from Supabase Auth
- Token verification middleware on all endpoints
- Service role key used only for admin operations

### API Keys
- Never commit `.env` to git
- Use environment variables for all secrets
- Rotate keys regularly

## Next Steps

After setup:
1. ✅ Database configured
2. ✅ Backend services implemented
3. → Configure frontend (see `../frontend/README.md`)
4. → Run manual browser tests
5. → Deploy to production

For detailed implementation plan, see: `../.agent/plans/2.module2-custom-rag.md`
