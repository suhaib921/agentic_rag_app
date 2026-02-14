#!/bin/bash
# Stop All Services
# Run from project root: bash scripts/stop-all.sh

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;33mStopping all services...\033[0m"

bash "$PROJECT_ROOT/scripts/stop-backend.sh"
bash "$PROJECT_ROOT/scripts/stop-frontend.sh"

echo -e "\n\033[0;32mAll services stopped.\033[0m"
