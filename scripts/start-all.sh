#!/bin/bash
# Start All Services
# Run from project root: bash scripts/start-all.sh
# This opens two new terminal windows for backend and frontend

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "\033[0;32mStarting all services...\033[0m"
echo -e "\033[0;90mProject root: $PROJECT_ROOT\033[0m"

# Detect available terminal emulator
if command -v gnome-terminal &> /dev/null; then
    TERMINAL="gnome-terminal"
elif command -v konsole &> /dev/null; then
    TERMINAL="konsole"
elif command -v xterm &> /dev/null; then
    TERMINAL="xterm"
else
    echo -e "\033[0;33mWARNING: No suitable terminal emulator found.\033[0m"
    echo -e "\033[0;33mStarting services in background instead...\033[0m"

    # Start backend in background
    bash "$PROJECT_ROOT/scripts/start-backend.sh" > "$PROJECT_ROOT/backend.log" 2>&1 &
    echo -e "\033[0;36mBackend started in background (logs: backend.log)\033[0m"

    sleep 1

    # Start frontend in background
    bash "$PROJECT_ROOT/scripts/start-frontend.sh" > "$PROJECT_ROOT/frontend.log" 2>&1 &
    echo -e "\033[0;36mFrontend started in background (logs: frontend.log)\033[0m"

    echo -e "\n\033[0;36mServices running in background:\033[0m"
    echo -e "  \033[0;33mBackend:  http://localhost:8000\033[0m"
    echo -e "  \033[0;33mFrontend: http://localhost:5173\033[0m"
    echo -e "\n\033[0;90mUse './scripts/stop-all.sh' to stop services\033[0m"
    exit 0
fi

# Start backend in new terminal window
if [ "$TERMINAL" = "gnome-terminal" ]; then
    gnome-terminal -- bash -c "cd '$PROJECT_ROOT' && bash ./scripts/start-backend.sh; exec bash"
elif [ "$TERMINAL" = "konsole" ]; then
    konsole -e bash -c "cd '$PROJECT_ROOT' && bash ./scripts/start-backend.sh; exec bash" &
elif [ "$TERMINAL" = "xterm" ]; then
    xterm -e "cd '$PROJECT_ROOT' && bash ./scripts/start-backend.sh; bash" &
fi

# Brief pause to stagger startup
sleep 0.5

# Start frontend in new terminal window
if [ "$TERMINAL" = "gnome-terminal" ]; then
    gnome-terminal -- bash -c "cd '$PROJECT_ROOT' && bash ./scripts/start-frontend.sh; exec bash"
elif [ "$TERMINAL" = "konsole" ]; then
    konsole -e bash -c "cd '$PROJECT_ROOT' && bash ./scripts/start-frontend.sh; exec bash" &
elif [ "$TERMINAL" = "xterm" ]; then
    xterm -e "cd '$PROJECT_ROOT' && bash ./scripts/start-frontend.sh; bash" &
fi

echo -e "\033[0;36mServices starting in separate windows:\033[0m"
echo -e "  \033[0;33mBackend:  http://localhost:8000\033[0m"
echo -e "  \033[0;33mFrontend: http://localhost:5173\033[0m"
