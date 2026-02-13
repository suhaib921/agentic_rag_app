#!/bin/bash
# Start Backend Server
# Run from project root: bash scripts/start-backend.sh

set -e

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;32mStarting backend server...\033[0m"
echo -e "\033[0;90mProject root: $PROJECT_ROOT\033[0m"

cd "$PROJECT_ROOT/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "\033[0;31mERROR: Virtual environment not found at backend/venv\033[0m"
    echo -e "\033[0;33mPlease create it first: python -m venv venv\033[0m"
    exit 1
fi

# Activate virtual environment and start uvicorn
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
