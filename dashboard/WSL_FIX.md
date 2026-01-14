# 🪟 WSL2 Fix - Getting WCF Service Page

## Problem

You're on WSL2 (Windows Subsystem for Linux) and seeing a Windows Communication Foundation service page instead of the dashboard. This happens because:

1. Windows IIS or another Windows service is using port 8000
2. WSL2 port forwarding is redirecting to the Windows service
3. The Python server in WSL isn't being reached

---

## Solution 1: Use a Different Port (Easiest)

Avoid the conflict by using a different port:

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 -m http.server 9000
```

Then visit: **http://localhost:9000**

---

## Solution 2: Find and Stop the Windows Service

### From Windows PowerShell (as Administrator):

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# The last column is the PID. Stop it:
taskkill /PID [PID_NUMBER] /F
```

### Common culprits on Windows:
- IIS (Internet Information Services)
- Visual Studio development server
- Docker Desktop
- Other development tools

---

## Solution 3: Bind to WSL IP Address Explicitly

```bash
cd /home/danyul/bridgewater-forecasting/dashboard

# Get your WSL IP
WSL_IP=$(hostname -I | awk '{print $1}')
echo "WSL IP: $WSL_IP"

# Start server on WSL IP only
python3 -m http.server 8000 --bind $WSL_IP
```

Then visit: `http://[WSL_IP]:8000` (use the IP shown)

---

## Solution 4: Use Modified launch Script for WSL

Create a WSL-specific launcher:

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
./launch-wsl.sh
```

---

## Recommended Ports for WSL Development

Try these ports (less likely to conflict):

- **9000** - Often free
- **8080** - Common alternative
- **3000** - Node.js default (usually free)
- **5000** - Flask default
- **5500** - VS Code Live Server

Example:
```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 -m http.server 9000
# Visit: http://localhost:9000
```

---

## Solution 5: Stop Windows IIS

If IIS is running on Windows:

1. Open Windows Services (`services.msc`)
2. Find "World Wide Web Publishing Service"
3. Right-click → Stop
4. Set Startup Type to "Manual" or "Disabled"

---

## Solution 6: Update Windows Firewall

Sometimes Windows firewall redirects WSL ports:

1. Open Windows Defender Firewall
2. Advanced Settings
3. Inbound Rules
4. Look for rules on port 8000
5. Disable or modify them

---

## Quick Test: Find Free Ports

```bash
# Test which ports are free in WSL
for port in 8000 8080 9000 3000 5000; do
    if ! lsof -i :$port > /dev/null 2>&1; then
        echo "✓ Port $port is FREE"
    else
        echo "✗ Port $port is IN USE"
    fi
done
```

---

## WSL-Specific Launch Script

I'll create a special launcher that handles WSL port conflicts:

```bash
#!/bin/bash
# WSL-aware launcher

cd /home/danyul/bridgewater-forecasting/dashboard

# Try ports in order until we find a free one
for PORT in 9000 8080 3000 5000 8888; do
    if ! lsof -i :$PORT > /dev/null 2>&1; then
        echo "✓ Using port $PORT"
        echo ""
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║  🎯 Dashboard is running on WSL!                       ║"
        echo "║                                                        ║"
        echo "║  🌐 URL: http://localhost:$PORT                        ║"
        echo "║                                                        ║"
        echo "║  Press Ctrl+C to stop                                  ║"
        echo "╚════════════════════════════════════════════════════════╝"
        echo ""
        python3 -m http.server $PORT
        exit 0
    fi
done

echo "❌ All common ports are in use!"
echo "   Try manually: python3 -m http.server [PORT]"
```

---

## Accessing from Windows Browser

When running in WSL, you can access from Windows using:

1. **localhost** (usually works): `http://localhost:9000`
2. **WSL IP** (always works):
   ```bash
   # In WSL terminal:
   hostname -I
   # Use that IP: http://[IP]:9000
   ```
3. **WSL2 hostname** (may work): `http://[your-wsl-hostname]:9000`

---

## Testing Your Setup

Run this diagnostic:

```bash
#!/bin/bash
echo "=== WSL Dashboard Diagnostic ==="
echo ""
echo "1. Current directory:"
pwd

echo ""
echo "2. Dashboard files present:"
ls -1 /home/danyul/bridgewater-forecasting/dashboard/*.{html,js} 2>/dev/null | wc -l
echo "   (should be at least 3)"

echo ""
echo "3. WSL IP address:"
hostname -I

echo ""
echo "4. Free ports:"
for port in 8000 8080 9000 3000 5000; do
    if ! lsof -i :$port > /dev/null 2>&1; then
        echo "   ✓ $port - FREE"
    else
        echo "   ✗ $port - IN USE"
    fi
done

echo ""
echo "5. Python available:"
python3 --version 2>/dev/null || echo "   ✗ Python3 not found"

echo ""
echo "=== Recommendation ==="
FREE_PORT=$(for p in 9000 8080 3000; do ! lsof -i :$p > /dev/null 2>&1 && echo $p && break; done)
if [ ! -z "$FREE_PORT" ]; then
    echo "Use port $FREE_PORT:"
    echo "  cd /home/danyul/bridgewater-forecasting/dashboard"
    echo "  python3 -m http.server $FREE_PORT"
    echo "  Then visit: http://localhost:$FREE_PORT"
else
    echo "All common ports busy. Try: python3 -m http.server 9999"
fi
```

Save this as `wsl-diagnostic.sh` and run it!

---

## Summary for WSL Users

**TL;DR:**

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 -m http.server 9000
```

Then open Windows browser to: **http://localhost:9000**

This avoids the port 8000 conflict entirely!
