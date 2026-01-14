# ⚡ QUICK FIX - WSL Port Conflict

## You're seeing a WCF service page because Windows is using port 8000!

---

## ✅ SOLUTION (30 seconds):

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
./launch-wsl.sh
```

This script automatically:
- ✅ Finds a free port (tries 9000, 8080, 3000, etc.)
- ✅ Starts the server correctly
- ✅ Shows you the exact URL to use
- ✅ Avoids all Windows port conflicts

---

## 🎯 Manual Alternative:

Use port 9000 instead of 8000:

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 -m http.server 9000
```

Then open in browser: **http://localhost:9000**

---

## 🔍 Why This Happened:

You're on **WSL2** (Windows Subsystem for Linux). Windows has a service (probably IIS or Visual Studio dev server) using port 8000, and WSL port forwarding sent you there instead of your Python server.

---

## 🚀 After Server Starts:

You should see:
```
Serving HTTP on 0.0.0.0 port 9000 (http://0.0.0.0:9000/) ...
```

In your browser, you'll see:
```
╔══════════════════════════════════════════════════════╗
║   🎯 Bridgewater x Metaculus 2026 Dashboard         ║
║   Live Forecast Tracking • Prize Pool: $30,000      ║
╚══════════════════════════════════════════════════════╝
```

NOT a WCF service configuration page!

---

## ℹ️ For More Help:

- WSL-specific issues: [WSL_FIX.md](WSL_FIX.md)
- General troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Full documentation: [README.md](README.md)

---

## 🎉 That's It!

Your dashboard will work perfectly on any port except 8000. The `launch-wsl.sh` script handles everything automatically.
