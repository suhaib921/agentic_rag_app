#!/bin/bash
# Restart Backend Server
# Run from project root: bash scripts/restart-backend.sh

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;36mRestarting backend server...\033[0m"

# Stop backend
bash "$PROJECT_ROOT/scripts/stop-backend.sh"

# Wait for port to be released
sleep 2

# Start backend
bash "$PROJECT_ROOT/scripts/start-backend.sh"
