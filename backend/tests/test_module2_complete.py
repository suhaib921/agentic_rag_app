#!/usr/bin/env python3
"""
Complete Module 2 Database Test Suite
Runs all verification and tests for Module 2 database setup
"""

import sys
import subprocess

def run_test(script_name, description):
    """Run a test script and report results"""
    print("\n" + "=" * 70)
    print(f"  {description}")
    print("=" * 70 + "\n")

    try:
        result = subprocess.run(
            ['python', script_name],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error running {script_name}: {e}")
        return False

def main():
    """Run complete test suite"""
    print("=" * 70)
    print("  MODULE 2 COMPLETE TEST SUITE")
    print("=" * 70)
    print("\nThis will run all Module 2 database verification and tests.")
    print("\nTests included:")
    print("1. Basic verification (tables, RLS, storage, functions)")
    print("2. RLS isolation test")
    print("3. Vector search function test")

    input("\nPress Enter to continue or Ctrl+C to cancel...")

    results = []

    # Test 1: Basic verification
    success = run_test('verify_module2_migration.py', 'Test 1: Basic Verification')
    results.append(('Basic Verification', success))

    if not success:
        print("\n⚠ Basic verification failed. Fix migration before proceeding.")
        print("  Run: python verify_module2_migration.py")
        return False

    # Ask before continuing to data tests
    print("\n" + "=" * 70)
    print("  Data Creation Tests")
    print("=" * 70)
    print("\nThe next tests will create and delete test data.")
    continue_tests = input("\nContinue with data tests? (y/n): ").strip().lower()

    if continue_tests != 'y':
        print("\nStopping after basic verification.")
        return True

    # Test 2: RLS test
    success = run_test('test_module2_rls.py', 'Test 2: RLS Isolation')
    results.append(('RLS Isolation', success))

    # Test 3: Vector search test
    success = run_test('test_match_chunks.py', 'Test 3: Vector Search Function')
    results.append(('Vector Search', success))

    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)

    all_passed = True
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not success:
            all_passed = False

    print("\n" + "=" * 70)

    if all_passed:
        print("  ✓ ALL TESTS PASSED")
        print("=" * 70)
        print("\nModule 2 database is fully set up and working!")
        print("\nNext steps:")
        print("1. Implement document ingestion endpoints")
        print("2. Add embedding generation with OpenAI")
        print("3. Build RAG query pipeline")
        return True
    else:
        print("  ✗ SOME TESTS FAILED")
        print("=" * 70)
        print("\nPlease review the failures and re-run specific tests:")
        print("- python verify_module2_migration.py")
        print("- python test_module2_rls.py")
        print("- python test_match_chunks.py")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest suite cancelled by user.")
        sys.exit(1)
