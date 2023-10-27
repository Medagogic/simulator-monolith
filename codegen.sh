#!/bin/bash

# Define the path to the virtual environment and the script
VENV_PATH="venv/bin/activate"
SCRIPT_PATH="packages/tools/codegen.py"
WORKING_DIR="$(pwd)"

# Check if the virtual environment exists
if [ -f "$VENV_PATH" ]; then
    # Activate the virtual environment
    source $VENV_PATH

    export PYTHONPATH="$WORKING_DIR"

    # Check if the Python script exists
    if [ -f "$SCRIPT_PATH" ]; then
        # Run the Python script
        python "$SCRIPT_PATH"
    else
        echo "Error: Python script not found: $SCRIPT_PATH"
        exit 1
    fi

    meld "packages/frontend/src/"

    # Deactivate the virtual environment (optional, but good practice)
    deactivate
else
    echo "Error: Virtual environment not found: $VENV_PATH"
    exit 1
fi
