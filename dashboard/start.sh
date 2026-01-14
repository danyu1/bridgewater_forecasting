#!/bin/bash

# Bridgewater Dashboard Quick Start Script

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   🎯 Bridgewater x Metaculus 2026 Dashboard           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found"
    echo "🚀 Starting server with Python..."
    python3 serve.py
elif command -v python &> /dev/null; then
    echo "✓ Python found"
    echo "🚀 Starting server with Python..."
    python serve.py
# Check if Node.js is available
elif command -v node &> /dev/null; then
    echo "✓ Node.js found"
    echo "🚀 Starting server with npx http-server..."
    npx http-server -p 8000
# Check if PHP is available
elif command -v php &> /dev/null; then
    echo "✓ PHP found"
    echo "🚀 Starting server with PHP..."
    php -S localhost:8000
else
    echo "❌ Error: No suitable HTTP server found!"
    echo ""
    echo "Please install one of the following:"
    echo "  • Python 3: sudo apt install python3"
    echo "  • Node.js: sudo apt install nodejs npm"
    echo "  • PHP: sudo apt install php"
    echo ""
    exit 1
fi
