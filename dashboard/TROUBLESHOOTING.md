# 🔧 Troubleshooting Guide

## Problem: Getting WCF Service Page Instead of Dashboard

If you see a "Windows Communication Foundation service" page instead of the dashboard, here are the solutions:

---

## Solution 1: Use the New Launch Script (Recommended)

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
./launch.sh
```

This script:
- ✅ Ensures you're in the correct directory
- ✅ Checks if files exist
- ✅ Kills any conflicting processes
- ✅ Starts from the right location

---

## Solution 2: Manual Start with Correct Directory

```bash
# Make sure you're in the dashboard directory
cd /home/danyul/bridgewater-forecasting/dashboard

# Verify index.html exists
ls -la index.html

# Start server from THIS directory
python3 -m http.server 8000
```

**Important**: The server must be started FROM the dashboard directory!

---

## Solution 3: Use a Different Port

If port 8000 has conflicts:

```bash
cd /home/danyul/bridgewater-forecasting/dashboard

# Try port 8080 instead
python3 -m http.server 8080

# Then visit: http://localhost:8080
```

---

## Solution 4: Check What's Running

```bash
# See what's on port 8000
lsof -i :8000

# Kill it if needed (replace PID with actual number)
kill -9 [PID]
```

---

## Solution 5: Use Python serve.py with CORS

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 serve.py
```

This includes proper headers and error handling.

---

## Solution 6: Specify Directory Explicitly

```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 -m http.server 8000 --directory .
```

---

## How to Verify It's Working

When correctly started, you should see in terminal:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

And when you visit http://localhost:8000, you should see:
- 🎯 Bridgewater x Metaculus 2026 Dashboard header
- Purple/blue gradient background
- Statistics cards showing "15 Total Questions"
- Grid of question cards

---

## Common Issues

### Issue: Blank page or 404

**Cause**: Server started from wrong directory

**Fix**:
```bash
cd /home/danyul/bridgewater-forecasting/dashboard
python3 -m http.server 8000
```

### Issue: "Address already in use"

**Cause**: Port 8000 is occupied

**Fix**:
```bash
# Kill existing process
lsof -i :8000
kill -9 [PID]

# Or use different port
python3 -m http.server 8888
```

### Issue: WCF Service page appears

**Cause**: Wrong directory or cached browser response

**Fix**:
1. Stop server (Ctrl+C)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Restart from dashboard directory:
   ```bash
   cd /home/danyul/bridgewater-forecasting/dashboard
   ./launch.sh
   ```
4. Try http://127.0.0.1:8000 instead of localhost

### Issue: Embeds show "Loading..." forever

**Cause**: Question IDs not updated yet

**Fix**: See [update_question_ids.md](update_question_ids.md)

---

## Alternative: Use a Different Web Server

### Using PHP:
```bash
cd /home/danyul/bridgewater-forecasting/dashboard
php -S localhost:8000
```

### Using Node.js:
```bash
cd /home/danyul/bridgewater-forecasting/dashboard
npx http-server -p 8000
```

### Using VS Code:
1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

---

## Still Not Working?

### Test if files are accessible:

```bash
cd /home/danyul/bridgewater-forecasting/dashboard

# Check files exist
ls -la index.html app.js questions.js

# Test reading the file
head -n 20 index.html
```

You should see HTML starting with:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bridgewater x Metaculus 2026 - Forecast Dashboard</title>
```

### Try direct file access:

```bash
# Open in browser directly (may not work due to CORS)
file:///home/danyul/bridgewater-forecasting/dashboard/index.html
```

### Check browser console:

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for any errors
4. Check Network tab for failed requests

---

## Best Practice: Clean Start

```bash
# 1. Stop any existing servers
pkill -f "python.*8000"

# 2. Navigate to dashboard
cd /home/danyul/bridgewater-forecasting/dashboard

# 3. Verify you're in the right place
pwd
# Should show: /home/danyul/bridgewater-forecasting/dashboard

# 4. List files to confirm
ls
# Should show: index.html app.js questions.js serve.py ...

# 5. Start server
./launch.sh

# 6. Open browser to http://localhost:8000
```

---

## Quick Diagnostic

Run this one-liner to diagnose:

```bash
cd /home/danyul/bridgewater-forecasting/dashboard && \
echo "Directory: $(pwd)" && \
echo "Files present:" && \
ls -1 *.html *.js 2>/dev/null && \
echo "Port 8000 status:" && \
lsof -i :8000 2>/dev/null || echo "  Port is free" && \
echo "" && \
echo "Starting server..." && \
python3 -m http.server 8000
```

---

## Contact Information

If none of these work:
1. Check the browser URL is exactly: `http://localhost:8000`
2. Try: `http://127.0.0.1:8000`
3. Try a different browser
4. Restart your computer (clears all port conflicts)

---

## Expected Result

When working correctly, you should see:

```
╔══════════════════════════════════════════════════════╗
║   🎯 Bridgewater x Metaculus 2026 Dashboard         ║
║   Live Forecast Tracking • Prize Pool: $30,000      ║
╚══════════════════════════════════════════════════════╝

[15] Total Questions
[15] Visible
[Mar 13] Competition Ends
[58] Days Remaining

[Grid of 15 question cards with purple/blue headers]
```

Not a WCF service configuration page!
