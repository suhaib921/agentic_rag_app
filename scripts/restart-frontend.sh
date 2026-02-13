#!/bin/bash
# Restart Frontend Server
# Run from project root: bash scripts/restart-frontend.sh

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;36mRestarting frontend server...\033[0m"

# Stop frontend
bash "$PROJECT_ROOT/scripts/stop-frontend.sh"

# Wait for port to be released
sleep 2

# Start frontend
bash "$PROJECT_ROOT/scripts/start-frontend.sh"
