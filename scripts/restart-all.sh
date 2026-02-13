#!/bin/bash
# Restart All Services
# Run from project root: bash scripts/restart-all.sh

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;36mRestarting all services...\033[0m"

# Stop all services
bash "$PROJECT_ROOT/scripts/stop-all.sh"

# Wait a moment for ports to be released
sleep 2

# Start all services
bash "$PROJECT_ROOT/scripts/start-all.sh"
