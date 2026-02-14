#!/bin/bash
# Start Frontend Server
# Run from project root: bash scripts/start-frontend.sh

set -e

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;32mStarting frontend server...\033[0m"
echo -e "\033[0;90mProject root: $PROJECT_ROOT\033[0m"

cd "$PROJECT_ROOT/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "\033[0;33mWARNING: node_modules not found. Running npm install first...\033[0m"
    npm install
fi

npm run dev
