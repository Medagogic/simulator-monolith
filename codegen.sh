function runScript() {
  local VENV_PATH="venv/bin/activate"
  local SCRIPT_PATH="packages/tools/codegen.py"
  local WORKING_DIR="$(pwd)"

  if [ -f "$VENV_PATH" ]; then
    source $VENV_PATH
    export PYTHONPATH="$WORKING_DIR"

    if [ -f "$SCRIPT_PATH" ]; then
      python "$SCRIPT_PATH"
      local script_status=$?

      if [ $script_status -eq 0 ]; then
        meld "packages/frontend/src/"
      else
        echo "Error: Python script failed to run successfully."
        deactivate
        exit 1
      fi
    else
      echo "Error: Python script not found: $SCRIPT_PATH"
      deactivate
      exit 1
    fi

    deactivate
  else
    echo "Error: Virtual environment not found: $VENV_PATH"
    exit 1
  fi
}

runScript
