# Database Migrations

## Instructions

These SQL files must be run in the **Supabase SQL Editor** in the following order:

1. `001_module2_schema.sql` - Creates documents and chunks tables with pgvector
2. `002_match_chunks_function.sql` - Creates vector similarity search function

## How to Run

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Create a new query
4. Copy and paste the contents of each migration file
5. Run the query
6. Verify success in the **Database** > **Tables** section

## Verification

After running migrations, verify:
- Tables exist: `documents`, `chunks`
- Function exists: `match_chunks`
- Extension enabled: `vector`
- RLS policies active on both tables
