# 🚀 Start Here: Module 2 Database Setup

**Welcome!** This guide will help you set up the Module 2 Custom RAG database in about 10 minutes.

---

## ⚡ Quickest Way to Start

```bash
cd backend
python setup_checklist.py
```

This interactive script will guide you through everything! Just follow the prompts.

---

## 📖 What You're Setting Up

Module 2 adds a custom RAG (Retrieval-Augmented Generation) system to your app, which allows:

- **Document Upload**: Users can upload PDFs and text files
- **Vector Search**: Intelligent semantic search using OpenAI embeddings
- **RAG Queries**: Ask questions about uploaded documents
- **Data Isolation**: Each user only sees their own documents (RLS)

---

## 🎯 The 5-Minute Manual Setup

If you prefer to do it manually:

### Step 1: Enable pgvector (1 min)
1. Go to [Supabase Dashboard](https://supabase.com/dashboard/project/ebxchkaaujpzqvkokdjw/database/extensions)
2. Search for "vector"
3. Toggle it ON

### Step 2: Run Migration (2 min)
1. Go to [SQL Editor](https://supabase.com/dashboard/project/ebxchkaaujpzqvkokdjw/sql/new)
2. Open file: `backend/migration_module2.sql`
3. Copy all contents and paste into SQL Editor
4. Click "Run"

### Step 3: Create Storage (1 min)
1. Go to [Storage](https://supabase.com/dashboard/project/ebxchkaaujpzqvkokdjw/storage/buckets)
2. Click "New bucket"
3. Name: `documents`
4. Public: OFF
5. Create

### Step 4: Storage Security (1 min)
Go back to [SQL Editor](https://supabase.com/dashboard/project/ebxchkaaujpzqvkokdjw/sql/new) and run:

```sql
CREATE POLICY "Users can access own documents"
ON storage.objects FOR ALL
USING (
  bucket_id = 'documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

### Step 5: Verify (30 sec)
```bash
cd backend
python verify_module2_migration.py
```

You should see all checkmarks (✓)!

---

## 📚 Need Help?

### Quick References
- **Quick Start**: `backend/QUICK_REFERENCE.md` - One-page cheat sheet
- **5-Step Guide**: `backend/MODULE2_DB_SETUP_QUICK_START.md`

### Detailed Guides
- **Full Setup**: `SETUP_MODULE2_DATABASE.md` - Complete guide with troubleshooting
- **Migration Details**: `backend/MIGRATION_INSTRUCTIONS.md`

### Technical Reference
- **Schema Documentation**: `backend/MODULE2_DB_SCHEMA.md` - Complete schema with diagrams
- **File Overview**: `backend/README_MODULE2_SETUP.md`

---

## 🧪 Testing Your Setup

### Quick Verification
```bash
cd backend
python verify_module2_migration.py
```

### Complete Test Suite
```bash
python test_module2_complete.py
```

This will:
1. Verify basic setup
2. Test RLS isolation (creates test data)
3. Test vector search function
4. Show summary report

---

## ❓ Common Issues

### "type 'vector' does not exist"
**Fix:** Enable pgvector extension (Step 1)

### "function update_updated_at() does not exist"
**Fix:** Run Module 1 migration first (or add the function to migration SQL)

### "relation already exists"
**Fix:** Tables already created - safe to ignore

### More help
Check `backend/MIGRATION_INSTRUCTIONS.md` (troubleshooting section)

---

## ✅ Success Checklist

After setup, you should have:

- [ ] pgvector extension enabled
- [ ] `documents` table created
- [ ] `chunks` table created (with VECTOR(1536) column)
- [ ] RLS enabled on both tables
- [ ] `documents` storage bucket created
- [ ] Storage RLS policy added
- [ ] `match_chunks()` function exists
- [ ] Verification script passes

**Check all:** Run `python verify_module2_migration.py`

---

## 🎉 What's Next?

Once setup is complete, you'll have:

✅ Database schema for document storage
✅ Vector embeddings support (pgvector)
✅ Semantic search function (match_chunks)
✅ Row-Level Security (data isolation)
✅ File storage bucket (with RLS)

**Next Step:** Implement document upload endpoint (Wave 1, Track 2)

See the full plan: `.agent/plans/2.module2-custom-rag.md`

---

## 📁 File Locations

Everything you need is in:

```
/home/suhkth/Desktop/Rag/agentic_rag_app/
├── START_HERE_MODULE2.md              ← You are here
├── SETUP_MODULE2_DATABASE.md          ← Full setup guide
├── DELIVERABLES_SUMMARY.md            ← What was created
├── WAVE1_TRACK1_COMPLETION_REPORT.md  ← Completion report
│
└── backend/
    ├── migration_module2.sql          ← Run this in SQL Editor
    ├── setup_checklist.py             ← Interactive setup
    ├── verify_module2_migration.py    ← Verify setup
    ├── QUICK_REFERENCE.md             ← Quick reference
    └── MODULE2_DB_SETUP_QUICK_START.md ← 5-step guide
```

---

## 🚦 Getting Started Now

Choose your path:

**🔹 Easiest (Recommended):**
```bash
cd backend
python setup_checklist.py
```

**🔹 Manual:**
Follow the 5 steps above

**🔹 Learn First:**
Read `backend/MODULE2_DB_SETUP_QUICK_START.md`

---

## 📞 Support

- **Quick help:** Check `backend/QUICK_REFERENCE.md`
- **Troubleshooting:** Check `backend/MIGRATION_INSTRUCTIONS.md`
- **Schema questions:** Check `backend/MODULE2_DB_SCHEMA.md`
- **Full details:** Check `SETUP_MODULE2_DATABASE.md`

---

**Estimated Time:** 5-10 minutes
**Difficulty:** Easy
**Status:** Ready to execute

**Let's get started!** 🚀
