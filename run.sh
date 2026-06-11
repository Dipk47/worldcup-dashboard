#!/bin/bash

# Navigate to the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

echo "⚽ Starting FIFA 2026 World Cup Predictions Dashboard..."
echo "📂 Project location: $DIR"

# Check if server is already running on port 8080
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8080 is already in use. Opening browser anyway..."
    open "http://localhost:8080/index.html"
    exit 0
fi

# Open browser after a small delay to let server spin up
(sleep 1 && open "http://localhost:8080/index.html") &

# Start python server
python3 server.py
