#!/bin/bash
# Startup script for JomiGuard Land Fraud & Double-Selling Alert System

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

echo "=========================================================="
echo "🛡️  Starting JomiGuard Land Fraud Alert System..."
echo "=========================================================="

export PYTHONPATH=.
.venv/bin/streamlit run app.py --server.port 8501 --server.headless false
