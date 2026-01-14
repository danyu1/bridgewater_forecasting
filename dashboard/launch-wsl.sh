#!/bin/bash

# WSL-Specific Dashboard Launcher
# Automatically finds a free port and starts the server

clear

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   🪟 Bridgewater Dashboard - WSL Launcher              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the dashboard directory
cd "$SCRIPT_DIR" || exit 1

echo "📁 Working directory: $SCRIPT_DIR"

# Check if index.html exists
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found!"
    exit 1
fi

echo "✓ Dashboard files verified"

# Get WSL IP address
WSL_IP=$(hostname -I | awk '{print $1}')
echo "🌐 WSL IP address: $WSL_IP"
echo ""

# Find a free port
echo "🔍 Searching for available port..."
FREE_PORT=""
for PORT in 9000 8080 3000 5000 8888 7000 6000; do
    if ! lsof -i :$PORT > /dev/null 2>&1; then
        FREE_PORT=$PORT
        break
    fi
done

if [ -z "$FREE_PORT" ]; then
    echo "❌ Error: All common ports are in use!"
    echo ""
    echo "Ports checked: 9000, 8080, 3000, 5000, 8888, 7000, 6000"
    echo ""
    echo "Try manually with a custom port:"
    echo "  python3 -m http.server 9999"
    exit 1
fi

echo "✓ Found free port: $FREE_PORT"
echo ""

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found!"
    echo "   Install: sudo apt update && sudo apt install python3"
    exit 1
fi

echo "✓ Python3 available"
echo ""

# Display access information
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║  ✅ Dashboard is starting on WSL!                      ║"
echo "║                                                        ║"
echo "║  🌐 Access URLs:                                       ║"
echo "║     http://localhost:$FREE_PORT                        "
echo "║     http://127.0.0.1:$FREE_PORT                        "
echo "║     http://$WSL_IP:$FREE_PORT                          "
echo "║                                                        ║"
echo "║  💡 Recommended: http://localhost:$FREE_PORT           "
echo "║                                                        ║"
echo "║  ⚠️  Note: If you get a WCF page, use a different     ║"
echo "║     browser or try the 127.0.0.1 URL above            ║"
echo "║                                                        ║"
echo "║  ⌨️  Press Ctrl+C to stop the server                   ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Try to open in browser (may not work in WSL, but worth trying)
if command -v wslview &> /dev/null; then
    echo "🌍 Attempting to open in Windows browser..."
    wslview "http://localhost:$FREE_PORT" 2>/dev/null &
elif command -v explorer.exe &> /dev/null; then
    echo "🌍 Attempting to open in Windows browser..."
    explorer.exe "http://localhost:$FREE_PORT" 2>/dev/null &
fi

echo ""
echo "🚀 Starting server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the server
python3 -m http.server $FREE_PORT
