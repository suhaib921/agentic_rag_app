#!/bin/bash
# Stop Backend Server
# Run from project root: bash scripts/stop-backend.sh

echo -e "\033[0;33mStopping backend server (port 8000)...\033[0m"

killed=false

# Method 1: Use lsof to find process on port 8000
if command -v lsof &> /dev/null; then
    pids=$(lsof -ti:8000 2>/dev/null || true)
    if [ -n "$pids" ]; then
        for pid in $pids; do
            proc_name=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
            echo -e "  \033[0;31mKilling process: $proc_name (PID: $pid)\033[0m"
            kill -9 $pid 2>/dev/null || true
            killed=true
        done
    fi
# Method 2: Fallback using fuser
elif command -v fuser &> /dev/null; then
    pids=$(fuser 8000/tcp 2>/dev/null || true)
    if [ -n "$pids" ]; then
        for pid in $pids; do
            proc_name=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
            echo -e "  \033[0;31mKilling process: $proc_name (PID: $pid)\033[0m"
            kill -9 $pid 2>/dev/null || true
            killed=true
        done
    fi
else
    echo -e "\033[0;31mERROR: Neither lsof nor fuser found. Cannot stop backend.\033[0m"
    exit 1
fi

# Verify it's stopped
sleep 0.5
if lsof -ti:8000 &> /dev/null || fuser 8000/tcp &> /dev/null; then
    echo -e "\033[0;31mWARNING: Backend may still be running.\033[0m"
elif [ "$killed" = true ]; then
    echo -e "\033[0;32mBackend server stopped.\033[0m"
else
    echo -e "\033[0;36mNo backend server running on port 8000.\033[0m"
fi
