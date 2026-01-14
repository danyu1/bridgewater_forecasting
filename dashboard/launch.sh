#!/bin/bash

# Bridgewater Dashboard Launch Script
# Ensures clean startup and correct directory

clear

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   🎯 Bridgewater x Metaculus 2026 Dashboard           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the dashboard directory
cd "$SCRIPT_DIR" || exit 1

echo "📁 Working directory: $SCRIPT_DIR"
echo ""

# Check if index.html exists
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found in $SCRIPT_DIR"
    echo "   Please make sure you're in the correct directory."
    exit 1
fi

echo "✓ index.html found"
echo "✓ Dashboard files verified"
echo ""

# Check for existing process on port 8000
PORT_CHECK=$(lsof -ti:8000 2>/dev/null)
if [ ! -z "$PORT_CHECK" ]; then
    echo "⚠️  Port 8000 is already in use by process $PORT_CHECK"
    echo ""
    read -p "Kill existing process and continue? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill -9 $PORT_CHECK 2>/dev/null
        echo "✓ Killed process $PORT_CHECK"
        sleep 1
    else
        echo "❌ Aborted. Please manually stop the process or use a different port."
        exit 1
    fi
fi

# Start the server
PORT=8000
URL="http://localhost:$PORT"

echo "🚀 Starting server on port $PORT..."
echo ""

# Try Python 3 first
if command -v python3 &> /dev/null; then
    echo "✓ Using Python 3"
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  Dashboard is running!                                 ║"
    echo "║                                                        ║"
    echo "║  🌐 URL: http://localhost:8000                         ║"
    echo "║  📂 Directory: $SCRIPT_DIR                             ║"
    echo "║                                                        ║"
    echo "║  Press Ctrl+C to stop the server                       ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""

    # Try to open browser (optional, may not work in all environments)
    if command -v xdg-open &> /dev/null; then
        xdg-open "$URL" 2>/dev/null &
    elif command -v open &> /dev/null; then
        open "$URL" 2>/dev/null &
    fi

    # Start Python HTTP server
    python3 -m http.server $PORT

elif command -v python &> /dev/null; then
    echo "✓ Using Python"
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  Dashboard is running!                                 ║"
    echo "║                                                        ║"
    echo "║  🌐 URL: http://localhost:8000                         ║"
    echo "║  📂 Directory: $SCRIPT_DIR                             ║"
    echo "║                                                        ║"
    echo "║  Press Ctrl+C to stop the server                       ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""

    python -m SimpleHTTPServer $PORT

else
    echo "❌ Error: Python not found!"
    echo ""
    echo "Please install Python:"
    echo "  • Ubuntu/Debian: sudo apt install python3"
    echo "  • macOS: brew install python3"
    exit 1
fi
