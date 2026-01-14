# 🚀 Quick Start Guide

## Start the Dashboard (3 Easy Ways)

### Option 1: Auto-Start Script (Recommended)
```bash
cd dashboard
./start.sh
```

### Option 2: Python Server
```bash
cd dashboard
python3 serve.py
```

### Option 3: Simple Python HTTP Server
```bash
cd dashboard
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

---

## ⚠️ Important: Update Question IDs First!

The dashboard won't show live data until you add real Metaculus question IDs.

### Quick Update Process:

1. **Go to the tournament page:**
   https://www.metaculus.com/tournament/bridgewater/

2. **Click on a question** (e.g., "Will the X algorithm be run by Grok...")

3. **Copy the question ID from the URL:**
   ```
   https://www.metaculus.com/questions/32426/will-the-x-algorithm...
                                      ^^^^^ this number
   ```

4. **Update `questions.js`:**
   ```javascript
   {
       id: 1,
       title: "Will the X algorithm be run by Grok...",
       questionId: "32426", // <-- Replace this
       ...
   }
   ```

5. **Repeat for all 15 questions**

See [update_question_ids.md](update_question_ids.md) for detailed instructions.

---

## 🎨 Features

- ✅ Live embedded forecasts from Metaculus
- ✅ Auto-refresh every 5 minutes
- ✅ Filter by category (Tech, Geopolitics, Economics, Entertainment)
- ✅ Grid or single column layout
- ✅ Keyboard shortcuts (R to refresh, F for fullscreen)
- ✅ Mobile responsive design
- ✅ Beautiful gradient UI

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Refresh all questions |
| `F` | Toggle fullscreen |
| `1` | Show all questions |
| `2` | Filter: Tech & AI |
| `3` | Filter: Geopolitics |
| `4` | Filter: Economics |
| `5` | Filter: Entertainment |

---

## 🔧 Troubleshooting

### Questions not loading?

**Problem**: You see "Loading forecast data..." forever

**Solutions**:
1. Update the question IDs in `questions.js` with real Metaculus IDs
2. Try using `http://127.0.0.1:8000` instead of `localhost`
3. Check browser console for errors (press F12)
4. Verify the embed URL works: `https://www.metaculus.com/questions/embed/[ID]/`

### CORS errors in console?

**Problem**: Browser console shows CORS/iframe errors

**Solutions**:
1. Use the provided `serve.py` script (has CORS headers)
2. Or use a different browser (Chrome/Firefox handle iframes differently)
3. Or run from a proper web server (not just file://)

### Port already in use?

**Problem**: "Address already in use" error

**Solutions**:
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (replace PID with actual number)
kill -9 [PID]

# Or use a different port
python3 -m http.server 8080
```

---

## 📁 File Structure

```
dashboard/
├── index.html              # Main dashboard page
├── app.js                  # Application logic
├── questions.js            # Question data (UPDATE THIS!)
├── serve.py                # Python server with CORS
├── start.sh                # Auto-start script
├── README.md               # Full documentation
├── QUICKSTART.md           # This file
└── update_question_ids.md  # How to get question IDs
```

---

## 🎯 Next Steps

1. ✅ Start the server
2. ⚠️ Update question IDs in `questions.js`
3. 🎉 Enjoy your live forecasting dashboard!

---

## 💡 Pro Tips

1. **Bookmark the dashboard**: Add `http://localhost:8000` to your browser bookmarks
2. **Run in background**: Add `&` at the end to run server in background:
   ```bash
   python3 serve.py &
   ```
3. **Use tmux/screen**: Keep server running even after closing terminal
4. **Add to startup**: Add start command to your `.bashrc` or `.zshrc`

---

## 📞 Need Help?

Check these files:
- [README.md](README.md) - Full documentation
- [update_question_ids.md](update_question_ids.md) - Detailed ID update guide

---

**Happy Forecasting! 🎯**

*Competition ends: March 13, 2026 • Prize Pool: $30,000*
