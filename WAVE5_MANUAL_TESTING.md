# Wave 5: Manual Testing Guide

Complete these manual tests in the browser to validate the full Module 2 implementation.

## Prerequisites

1. **Start Backend:**
   ```bash
   cd /home/suhkth/Desktop/Rag/agentic_rag_app/backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd /home/suhkth/Desktop/Rag/agentic_rag_app/frontend
   npm run dev
   ```

3. **Open Browser:**
   - Navigate to: http://localhost:5173
   - Open Developer Tools (F12) → Console tab

---

## Test 1: Document Ingestion Flow ⏱️ 5 minutes

### Upload PDF Document

1. Create a test PDF or download one
2. Go to Documents page in the app
3. Click upload or drag-and-drop the PDF
4. **Expected Results:**
   - Document appears in list immediately
   - Status: "uploaded"
   - Console shows: "Uploaded: {id: ..., status: 'uploaded'}"

### Watch Status Transitions (Realtime)

5. Watch the document status change **without refreshing**:
   - uploaded → processing (a few seconds)
   - processing → chunking (a few seconds)
   - chunking → embedding (longer, depending on size)
   - embedding → completed
6. **Expected Results:**
   - Console shows: "Document updated:" for each transition
   - UI updates automatically
   - Final status shows chunk count (e.g., "42 chunks")

### Upload TXT Document

7. Create a test .txt file with some content
8. Upload it the same way
9. **Expected Results:**
   - Same status transitions
   - Completes successfully

### Upload Unsupported File Type

10. Try uploading a .jpg or .exe file
11. **Expected Results:**
    - Error message: "Unsupported file type"
    - Document does NOT appear in list

---

## Test 2: RAG Chat Flow ⏱️ 10 minutes

### Upload Document with Known Content

1. Create a text file with specific, searchable content:
   ```
   The capital of France is Paris.
   The Eiffel Tower is 330 meters tall.
   Paris is located on the Seine River.
   ```

2. Save as `france_facts.txt`
3. Upload to the app
4. Wait for status: "completed"

### Ask Question About Content

5. Go to Chat page
6. Create a new thread
7. Ask: "What is the capital of France?"
8. **Expected Results:**
   - Response mentions "Paris"
   - Response cites the document (e.g., "According to your document...")
   - Streaming works smoothly

### Verify Context Retrieval

9. Open Browser DevTools → Network tab
10. Send another message: "How tall is the Eiffel Tower?"
11. Check backend logs (terminal running uvicorn)
12. **Expected Results:**
    - Backend logs show RAG retrieval
    - Response cites document
    - Correct answer: "330 meters"

### Test Chat Without Documents

13. Delete all documents from Documents page
14. Go to Chat, ask: "What is 2+2?"
15. **Expected Results:**
    - Chat still works
    - Response: "4"
    - No document citations (no context available)

---

## Test 3: Multi-Provider Testing ⏱️ 15 minutes

### Test OpenAI Provider (Default)

1. Verify `.env` has:
   ```
   CHAT_PROVIDER=openai
   CHAT_MODEL=gpt-4o
   CHAT_API_KEY=sk-...
   ```
2. Restart backend
3. Send a chat message
4. **Expected Results:**
   - Chat works
   - Response from GPT-4

### Test OpenRouter (Optional)

5. Update `.env`:
   ```
   CHAT_PROVIDER=openrouter
   CHAT_MODEL=anthropic/claude-3.5-sonnet
   CHAT_API_KEY=sk-or-v1-...
   ```
6. Restart backend
7. Send a chat message
8. **Expected Results:**
   - Chat works
   - Response from Claude

### Test Ollama (If Running Locally)

9. Start Ollama: `ollama serve`
10. Pull a model: `ollama pull llama3.2`
11. Update `.env`:
    ```
    CHAT_PROVIDER=ollama
    CHAT_MODEL=llama3.2
    CHAT_BASE_URL=http://localhost:11434/v1
    ```
12. Restart backend
13. Send a chat message
14. **Expected Results:**
    - Chat works
    - Response from local Llama model

---

## Test 4: Row-Level Security ⏱️ 10 minutes

### Create Two Users

1. Sign out from current session
2. Create User A: test-user-a@example.com
3. Sign in as User A
4. Upload a document: "user_a_doc.txt"
5. Note the document ID from the list

### Test Isolation

6. Sign out
7. Sign in as User B: test-user-b@example.com
8. Go to Documents page
9. **Expected Results:**
   - User B sees NO documents
   - User A's document is not visible

### Test API Isolation

10. In browser console, try to fetch User A's document:
    ```javascript
    const token = (await supabase.auth.getSession()).data.session.access_token
    fetch('http://localhost:8000/api/documents/{user-a-doc-id}', {
      headers: {'Authorization': `Bearer ${token}`}
    }).then(r => r.json()).then(console.log)
    ```
11. **Expected Results:**
    - 404 Not Found
    - User B cannot access User A's document

### Test Vector Search Isolation

12. User B uploads own document: "user_b_doc.txt"
13. User B asks in chat about content from User A's document
14. **Expected Results:**
    - Response does NOT include User A's content
    - Only retrieves from User B's documents

---

## Test 5: Error Handling ⏱️ 5 minutes

### Corrupted File

1. Create a file: `corrupted.pdf`
2. Put random text in it (not valid PDF)
3. Upload it
4. **Expected Results:**
   - Status changes to: "failed"
   - Error message appears
   - Error message describes the problem

### Chat with Invalid Config

5. Stop backend
6. Update `.env` with invalid API key: `CHAT_API_KEY=invalid-key`
7. Restart backend
8. Try to send a chat message
9. **Expected Results:**
   - Error message in chat UI
   - Console shows error
   - Backend logs show authentication error

### Restore Config

10. Fix `.env` with correct API key
11. Restart backend
12. Verify chat works again

---

## Test 6: LangSmith Observability ⏱️ 5 minutes

### Upload Document

1. Upload a new document
2. Wait for completion
3. Go to: https://smith.langchain.com
4. Select project: "agentic-rag-module2"
5. **Expected Traces:**
   - `extract_text`
   - `chunk_text`
   - `process_document`
   - `generate_embeddings_batch`

### Send Chat Message

6. Send a chat message in the app
7. Refresh LangSmith dashboard
8. **Expected Traces:**
   - `retrieve_context`
   - `generate_embedding` (for query)
   - `openai_stream_chat` (or provider-specific)

### Check Trace Details

9. Click on a trace
10. **Expected Details:**
   - Input/output logged
   - Latency recorded
   - No errors

---

## Validation Checklist

After completing all tests, check off:

- [ ] Document upload works (PDF, TXT, DOCX)
- [ ] Status updates in realtime without refresh
- [ ] Chunk count appears when complete
- [ ] Unsupported file types rejected
- [ ] RAG retrieves relevant context
- [ ] Chat responses cite documents
- [ ] Chat works without documents
- [ ] Multiple LLM providers work
- [ ] RLS isolates user data completely
- [ ] API returns 404 for unauthorized access
- [ ] Vector search respects RLS
- [ ] Error handling shows meaningful messages
- [ ] Failed documents show error status
- [ ] LangSmith traces appear for all operations
- [ ] Traces show input/output correctly

---

## Success Criteria

✅ **Module 2 Complete** if:
- All automated tests pass (23/24+)
- All manual tests pass
- No console errors in normal operation
- Realtime updates work smoothly
- RLS completely isolates users
- LangSmith traces visible

---

## Troubleshooting

### Documents stuck in "processing"
- Check backend logs for errors
- Verify OpenAI API key is valid
- Check file is not corrupted

### Realtime updates not working
- Verify Supabase RLS policies allow reading own documents
- Check browser console for Realtime connection errors
- Refresh page and try again

### RAG not retrieving context
- Verify document reached "completed" status
- Check chunks were created (chunk_count > 0)
- Verify query is semantically similar to document content

### Chat errors
- Check CHAT_API_KEY is valid
- Verify CHAT_PROVIDER matches available service
- Check backend logs for detailed error messages

---

**Estimated Total Time:** 50-60 minutes for complete validation
