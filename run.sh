#!/bin/bash
# Startup script for JomiGuard Land Title Audit & Fraud Alert System

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Check if .venv exists, otherwise create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment .venv..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
fi

PORT="${1:-8501}"

# Check if port is already in use and free it automatically
if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
    OLD_PID=$(lsof -Pi :"$PORT" -sTCP:LISTEN -t | head -n 1)
    echo "⚠️  Port $PORT was occupied by PID $OLD_PID. Freeing port $PORT..."
    kill -9 "$OLD_PID" 2>/dev/null || true
    sleep 1
fi

echo "=========================================================="
echo "🛡️  Starting JomiGuard Land Title Audit System on port $PORT..."
echo "=========================================================="

export PYTHONPATH=.
.venv/bin/streamlit run app.py --server.port "$PORT" --server.headless false
