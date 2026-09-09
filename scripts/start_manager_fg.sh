#!/bin/bash

# -------------------------------------------------------------------
# START MANAGER (FG Mode) - FOR DEBUGGING AND INTERACTIVE TESTING
# -------------------------------------------------------------------

set -e

# --- Configuration ---
SCRIPT_DIR=$(dirname "$0")
VENV_DIR="$SCRIPT_DIR/.venv"
APP_FILE="$SCRIPT_DIR/app.py"
# ---------------------

echo "==================================================="
echo "🚀 Starting Remote Command Dashboard Manager (FOREGROUND MODE)"
echo "==================================================="

# --- Pre-Flight Check 1: VENV Existence ---
if [ ! -d "$VENV_DIR" ]; then
    echo "FATAL ERROR: Virtual environment not found at $VENV_DIR."
    echo "Please run: python3 -m venv .venv"
    exit 1
fi

# --- Pre-Flight Check 2: Check if already running ---
# We skip the PID check here because we are running interactively.
# We assume if this script is running, it's the main process.

echo "✅ Environment and state checked. Starting Flask application..."

# EXECUTION: Run the application directly in the foreground (NO output redirection).
# This makes the terminal wait for the server to run.
"$VENV_DIR/bin/python" "$APP_FILE"
