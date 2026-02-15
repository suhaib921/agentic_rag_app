-- Wave 4, Track 2: Remove OpenAI Responses API columns
-- These columns were used for Module 1's OpenAI Assistants API and are no longer needed.

-- Drop openai_thread_id column from threads table
ALTER TABLE threads DROP COLUMN IF EXISTS openai_thread_id CASCADE;

-- Drop openai_message_id column from messages table
ALTER TABLE messages DROP COLUMN IF EXISTS openai_message_id CASCADE;

-- Drop index on openai_thread_id (if it exists)
DROP INDEX IF EXISTS idx_threads_openai_thread_id;
