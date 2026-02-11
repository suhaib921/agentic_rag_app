# Agentic RAG Application - Module 1

A production-ready RAG (Retrieval-Augmented Generation) application with authentication, chat interface, and observability.

## Features

- 🔐 **Authentication** - Supabase Auth with Row-Level Security
- 💬 **Chat Interface** - Real-time streaming responses
- 🤖 **OpenAI Integration** - Responses API with managed threads
- 📊 **Observability** - LangSmith tracing for all LLM calls
- 🎨 **Modern UI** - React + TypeScript + Tailwind + shadcn/ui
- ⚡ **Fast Backend** - Python FastAPI with async support

## Architecture

**Frontend:** React + TypeScript + Vite + Tailwind + shadcn/ui
**Backend:** Python + FastAPI + Pydantic
**Database:** Supabase (Postgres + pgvector + Auth + Storage)
**LLM:** OpenAI Responses API (Module 1)
**Observability:** LangSmith

## Prerequisites

- Node.js 18+
- Python 3.11+
- Supabase account
- OpenAI account with API access
- LangSmith account

## Setup Instructions

### 1. Manual Setup Steps

⚠️ **Complete these manual steps first:**

1. **Supabase Setup** - See [SETUP_SUPABASE.md](./SETUP_SUPABASE.md)
   - Create Supabase project
   - Run database migration
   - Create test user
   - Save credentials

2. **OpenAI & LangSmith Setup** - See [SETUP_OPENAI.md](./SETUP_OPENAI.md)
   - Create OpenAI Assistant
   - Get API keys
   - Set up LangSmith project

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your actual credentials

# Start backend
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
Health check: http://localhost:8000/health

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env with your actual credentials

# Start frontend
npm run dev
```

Frontend runs at: http://localhost:5173

## Environment Variables

### Backend (.env)

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

OPENAI_API_KEY=sk-...
OPENAI_ASSISTANT_ID=asst_...

LANGSMITH_API_KEY=lsv2_...
LANGSMITH_PROJECT=agentic-rag-module1

CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)

```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:8000
```

## Usage

1. **Start both servers:**
   - Backend: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload`
   - Frontend: `cd frontend && npm run dev`

2. **Access the application:**
   - Go to http://localhost:5173
   - Sign in with your test user credentials
   - Click "New Chat" to create a conversation
   - Send messages and get AI responses

3. **Monitor observability:**
   - Check LangSmith at https://smith.langchain.com
   - View traces for all LLM interactions

## Project Structure

```
agentic_rag_app/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── auth/         # Authentication middleware
│   │   ├── models/       # Pydantic schemas
│   │   └── services/     # OpenAI & LangSmith services
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
│   ├── package.json
│   └── .env.example
├── SETUP_SUPABASE.md    # Supabase setup guide
├── SETUP_OPENAI.md      # OpenAI setup guide
└── README.md
```

## Development

### Backend

```bash
cd backend
source venv/bin/activate

# Run server
uvicorn app.main:app --reload

# Install new dependencies
pip install <package>
pip freeze > requirements.txt
```

### Frontend

```bash
cd frontend

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Testing

### Manual Testing

1. **Authentication:**
   - Sign in with valid credentials → Success
   - Sign in with invalid credentials → Error message
   - Sign out → Redirected to login

2. **Chat:**
   - Create new thread → Appears in sidebar
   - Send message → Streams response in real-time
   - Switch threads → Correct messages load
   - Verify messages in Supabase dashboard

3. **Security (RLS):**
   - Create two users
   - Verify users can't see each other's threads

## Troubleshooting

### Backend Issues

**Module import errors:**
```bash
# Make sure venv is activated
source venv/bin/activate
# Verify Python path
python -c "import sys; print(sys.path)"
```

**Environment variable errors:**
```bash
# Check .env file exists and has correct values
cat backend/.env
```

### Frontend Issues

**Build errors:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Verify backend CORS_ORIGINS matches frontend URL exactly
- Check both servers are running

## Next Steps

After Module 1 is working:

- **Module 2:** Document ingestion, vector search, Chat Completions API
- **Module 3:** Record management and deduplication
- **Module 4:** Metadata extraction
- **Module 5:** Multi-format support
- **Module 6:** Hybrid search & reranking
- **Module 7:** Additional tools (Text-to-SQL, web search)
- **Module 8:** Sub-agents

## Notes

- **langsmith 0.1.140 is yanked:** The version installs but has a warning. This is acceptable for Module 1.
- **File search in Module 1:** The OpenAI Assistant has file_search enabled but won't find documents until Module 2 adds the ingestion pipeline. This is expected!
- **Responses API:** Module 1 uses OpenAI's Responses API (managed threads). Module 2 transitions to Chat Completions API for provider flexibility.

## Support

For issues or questions:
- Check the setup guides: SETUP_SUPABASE.md, SETUP_OPENAI.md
- Review the plan: .agent/plans/1.module1-app-shell.md
- Check Supabase logs in dashboard
- Check LangSmith traces for LLM issues
