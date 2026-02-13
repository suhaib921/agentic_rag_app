# Scripts Documentation

Linux automation scripts for managing the RAG application's backend and frontend services.

## 📋 Available Scripts

### **Main Orchestration Scripts**

| Script | Description |
|--------|-------------|
| `start-all.sh` | Starts both backend and frontend in separate terminal windows |
| `stop-all.sh` | Stops both backend and frontend services |
| `restart-all.sh` | Restarts both services (stops, waits 2s, then starts) |

### **Individual Service Scripts**

**Backend (Port 8000):**
- `start-backend.sh` - Activates venv and runs FastAPI server
- `stop-backend.sh` - Kills all processes using port 8000
- `restart-backend.sh` - Restarts only the backend service

**Frontend (Port 5173):**
- `start-frontend.sh` - Runs Vite dev server
- `stop-frontend.sh` - Kills all processes using port 5173
- `restart-frontend.sh` - Restarts only the frontend service

## 🚀 Usage

### From project root directory:

```bash
# Start everything (opens new terminal windows)
./scripts/start-all.sh

# Stop everything
./scripts/stop-all.sh

# Restart everything
./scripts/restart-all.sh

# Individual services
./scripts/start-backend.sh
./scripts/stop-frontend.sh
./scripts/restart-backend.sh
```

### Alternative: From anywhere

```bash
bash /path/to/agentic_rag_app/scripts/start-all.sh
```

## 🔍 What They Do

### Starting Services

**Backend:**
- Changes to `backend/` directory
- Activates Python virtual environment (`venv/bin/activate`)
- Runs `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Accessible at: http://localhost:8000

**Frontend:**
- Changes to `frontend/` directory
- Checks if `node_modules` exists (runs `npm install` if not)
- Runs `npm run dev`
- Accessible at: http://localhost:5173

**Terminal Behavior:**
- Detects available terminal emulator (gnome-terminal, konsole, xterm)
- Opens each service in a separate terminal window
- If no terminal emulator found, runs services in background with logging

### Stopping Services

- Uses `lsof` to find processes listening on ports 8000/5173
- Falls back to `fuser` if `lsof` is not available
- Force-kills processes using `kill -9`
- Verifies ports are released

## 📦 Requirements

**Backend:**
- Python virtual environment at `backend/venv`
- FastAPI application at `backend/app/main.py`

**Frontend:**
- Node.js and npm installed
- Package.json in `frontend/` directory

**System Tools:**
- `lsof` or `fuser` (for stopping services)
- Terminal emulator (optional, for separate windows):
  - gnome-terminal (GNOME/Ubuntu)
  - konsole (KDE)
  - xterm (fallback)

## 🎨 Color Output

Scripts use ANSI color codes for better readability:
- 🟢 **Green** - Success messages, starting services
- 🟡 **Yellow** - Warnings, stopping services
- 🔴 **Red** - Errors, killing processes
- 🔵 **Cyan** - Info messages
- ⚫ **Gray** - Debug info

## 🐛 Troubleshooting

**"Virtual environment not found":**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**"node_modules not found":**
```bash
cd frontend
npm install
```

**Port already in use:**
```bash
# Kill specific port
./scripts/stop-backend.sh  # for port 8000
./scripts/stop-frontend.sh # for port 5173

# Or manually
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

**No terminal emulator:**
- Scripts will run services in background mode automatically
- Check logs: `backend.log` and `frontend.log` in project root
- Or install a terminal emulator: `sudo apt install gnome-terminal`

## 📝 Notes

- All scripts automatically detect the project root directory
- Scripts can be run from any location
- Backend runs with `--reload` flag for auto-reloading on code changes
- Frontend runs in development mode with hot module replacement
- All scripts include error handling and status verification
