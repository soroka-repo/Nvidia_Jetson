#!/bin/bash

# -------------------------------------------------------------------
# START MANAGER (BG Mode) - FOR SILENT, CONTINUOUS OPERATION
# -------------------------------------------------------------------

set -e

# --- Configuration ---
SCRIPT_DIR=$(dirname "$0")
VENV_DIR="$SCRIPT_DIR/.venv"
APP_FILE="$SCRIPT_DIR/app.py"
PID_FILE="$SCRIPT_DIR/manager.pid"
LOG_FILE="$SCRIPT_DIR/manager.log"
# ---------------------

echo "==================================================="
echo "🚀 Starting Remote Command Dashboard Manager (BACKGROUND MODE)"
echo "==================================================="

# --- Pre-Flight Check 1: VENV Existence ---
if [ ! -d "$VENV_DIR" ]; then
    echo "FATAL ERROR: Virtual environment not found at $VENV_DIR."
    echo "Please run: python3 -m venv .venv"
    exit 1
fi

# --- Pre-Flight Check 2: Check if already running ---
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "🚨 Manager already running (PID: $PID). Use ./stop_manager.sh to stop it first."
    exit 1
fi

# --- Execution ---
echo "✅ Environment and state checked. Starting Flask application in background..."

# Execution: Run the application in the background AND redirect all output
# to a log file. This makes it truly silent in the terminal.
"$VENV_DIR/bin/python" "$APP_FILE" > "$LOG_FILE" 2>&1 &
FLASK_PID=$!

# Store the PID in a file for later retrieval (essential for stopping the service)
echo $FLASK_PID > "$PID_FILE"

echo "✨ Dashboard started successfully in the background."
echo "Process ID: $FLASK_PID"
echo "Check $LOG_FILE for real-time output and errors."
echo "Use ./stop_manager.sh to gracefully stop the service."
