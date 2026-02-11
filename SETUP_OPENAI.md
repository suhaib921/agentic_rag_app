# Phase 5: OpenAI Assistant Setup (MANUAL STEP)

⚠️ **This step must be completed manually before chat functionality will work**

## Prerequisites

- OpenAI account with API access
- OpenAI API key (get from https://platform.openai.com/api-keys)

## Steps

### 1. Create OpenAI Assistant

1. Go to https://platform.openai.com/assistants
2. Click "Create" or "+ Create new assistant"
3. Configure the assistant:

**Basic Settings:**
- **Name:** Agentic RAG Assistant
- **Instructions:**
  ```
  You are a helpful assistant that answers questions based on uploaded documents.
  When documents are available, use the file_search tool to find relevant information.
  Provide clear, accurate answers based on the document content.
  ```
- **Model:** gpt-4o (or latest available model)

**Tools:**
- ✅ Enable "File Search"
  - This allows the assistant to search through uploaded documents
  - Note: Documents will be uploaded in Module 2

**Additional Settings (Optional):**
- Temperature: 0.7 (default is fine)
- Top P: 1.0 (default is fine)

4. Click "Save" or "Create"

### 2. Copy Assistant ID

After creating the assistant:
1. The Assistant ID will be displayed at the top (format: `asst_...`)
2. Copy this ID
3. Add it to `backend/.env`:
   ```
   OPENAI_ASSISTANT_ID=asst_xxxxxxxxxxxxxxxxxxxxx
   ```

### 3. Set API Key

1. If you haven't already, get your API key from https://platform.openai.com/api-keys
2. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
   ```

## Important Notes

- **File Search Tool:** In Module 1, the file_search tool is configured but won't find any documents yet. This is expected! Module 2 will add the document ingestion pipeline.

- **Cost:** The Responses API with file_search incurs charges. Monitor your usage at https://platform.openai.com/usage

- **Security:** Keep your API key and Service Role key secret! Never commit them to git.

✅ **Done!** Your OpenAI Assistant is ready.

## Next: LangSmith Setup

You'll also need to set up LangSmith for observability:

1. Go to https://smith.langchain.com
2. Create account / sign in
3. Create new project: "agentic-rag-module1"
4. Get API key from Settings
5. Add to `backend/.env`:
   ```
   LANGSMITH_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxxx
   LANGSMITH_PROJECT=agentic-rag-module1
   ```
