#!/usr/bin/env python3
"""
Module 2 Database Setup - Interactive Checklist
Guides user through setup process step-by-step
"""

import sys
from app.config import Settings

def print_header(text):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def wait_for_confirmation(step_num, description):
    """Wait for user to confirm step completion"""
    print(f"\n[Step {step_num}] {description}")
    response = input("  Press Enter when complete (or 'q' to quit): ").strip().lower()
    if response == 'q':
        print("\nSetup cancelled by user.")
        sys.exit(0)
    print("  ✓ Step completed!")

def main():
    """Run interactive setup checklist"""
    settings = Settings()

    # Extract project ref
    url = settings.supabase_url.replace('https://', '').replace('http://', '')
    project_ref = url.split('.')[0]

    print_header("MODULE 2 DATABASE SETUP - Interactive Checklist")

    print("This script will guide you through the Module 2 database setup.")
    print("\nProject Information:")
    print(f"  Project Ref: {project_ref}")
    print(f"  URL: {settings.supabase_url}")
    print(f"  Dashboard: https://supabase.com/dashboard/project/{project_ref}")

    print("\n" + "-" * 70)
    print("Setup Overview:")
    print("  1. Enable pgvector extension")
    print("  2. Run migration SQL")
    print("  3. Create storage bucket")
    print("  4. Add storage RLS policy")
    print("  5. Verify setup")
    print("-" * 70)

    input("\nPress Enter to begin or Ctrl+C to cancel...")

    # Step 1: Enable pgvector
    print_header("Step 1: Enable pgvector Extension")
    print("1. Open: https://supabase.com/dashboard/project/" + project_ref + "/database/extensions")
    print("2. Search for: vector")
    print("3. Toggle ON the 'vector' extension")
    print("4. Wait a few seconds for activation")
    wait_for_confirmation(1, "pgvector extension enabled")

    # Step 2: Run migration SQL
    print_header("Step 2: Run Migration SQL")
    print("1. Open: https://supabase.com/dashboard/project/" + project_ref + "/sql/new")
    print("2. In your file system, open: backend/migration_module2.sql")
    print("3. Copy the ENTIRE contents of the file")
    print("4. Paste into the SQL Editor")
    print("5. Click 'Run' (or press Cmd/Ctrl + Enter)")
    print("6. Verify you see: 'Success. No rows returned'")
    wait_for_confirmation(2, "Migration SQL executed")

    # Step 3: Create storage bucket
    print_header("Step 3: Create Storage Bucket")
    print("1. Open: https://supabase.com/dashboard/project/" + project_ref + "/storage/buckets")
    print("2. Click 'New bucket'")
    print("3. Name: documents")
    print("4. Public: OFF (unchecked)")
    print("5. Click 'Create bucket'")
    wait_for_confirmation(3, "Storage bucket 'documents' created")

    # Step 4: Add storage RLS
    print_header("Step 4: Add Storage RLS Policy")
    print("1. Open: https://supabase.com/dashboard/project/" + project_ref + "/sql/new")
    print("2. Paste this SQL:")
    print("\n" + "-" * 70)
    print("""CREATE POLICY "Users can access own documents"
ON storage.objects FOR ALL
USING (
  bucket_id = 'documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);""")
    print("-" * 70)
    print("\n3. Click 'Run'")
    wait_for_confirmation(4, "Storage RLS policy created")

    # Step 5: Verify setup
    print_header("Step 5: Verify Setup")
    print("Now we'll run the verification script to ensure everything is set up correctly.")
    print("\nThe script will check:")
    print("  - Tables exist (documents, chunks)")
    print("  - RLS is enabled")
    print("  - Storage bucket exists")
    print("  - pgvector extension is enabled")

    input("\nPress Enter to run verification...")

    import subprocess
    try:
        print("\n" + "=" * 70)
        result = subprocess.run(['python', 'verify_module2_migration.py'], check=False)
        print("=" * 70)

        if result.returncode == 0:
            print("\n✓ Verification successful!")
            print("\n" + "=" * 70)
            print("  SETUP COMPLETE!")
            print("=" * 70)
            print("\nYour Module 2 database is ready for use!")
            print("\nOptional: Run complete test suite:")
            print("  python test_module2_complete.py")
            print("\nNext steps:")
            print("  - Implement document upload endpoint")
            print("  - Add PDF text extraction")
            print("  - Implement chunking logic")
            print("  - Add embedding generation")
            return True
        else:
            print("\n✗ Verification failed!")
            print("\nPlease review the errors above and:")
            print("  1. Fix any issues")
            print("  2. Re-run: python verify_module2_migration.py")
            print("\nOr get help:")
            print("  - Check: SETUP_MODULE2_DATABASE.md")
            print("  - Review: MIGRATION_INSTRUCTIONS.md")
            return False

    except Exception as e:
        print(f"\n✗ Error running verification: {e}")
        print("\nYou can manually run verification:")
        print("  python verify_module2_migration.py")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
