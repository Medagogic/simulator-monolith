#!/bin/bash

# Start frontend
(cd ./packages/frontend && npm run dev) &

# Start server
(
    source venv/bin/activate
    python ./packages/server/main.py
) &

# Wait for both processes to complete
wait