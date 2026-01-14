# Bridgewater x Metaculus 2026 Dashboard

A live-updating dashboard for tracking all Bridgewater forecasting tournament questions.

## Features

- 📊 **Live Embeds**: Each question is embedded directly from Metaculus with real-time updates
- 🎨 **Beautiful UI**: Modern, responsive design with gradient backgrounds
- 🔍 **Smart Filtering**: Filter by category (Tech, Geopolitics, Economics, Entertainment)
- 📐 **Layout Options**: Grid view or single column view
- 🔄 **Auto-Refresh**: Questions refresh automatically every 5 minutes
- ⌨️ **Keyboard Shortcuts**: Quick navigation with keyboard
- 📱 **Mobile Responsive**: Works great on all screen sizes

## Getting Started

### Option 1: Simple HTTP Server (Python)

```bash
cd dashboard
python3 -m http.server 8000
```

Then open: http://localhost:8000

### Option 2: Simple HTTP Server (Node.js)

```bash
cd dashboard
npx http-server -p 8000
```

Then open: http://localhost:8000

### Option 3: VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Keyboard Shortcuts

- `R` - Refresh all questions
- `F` - Toggle fullscreen
- `1` - Show all questions
- `2` - Filter: Tech & AI
- `3` - Filter: Geopolitics
- `4` - Filter: Economics
- `5` - Filter: Entertainment

## Configuration

### Updating Question IDs

You'll need to update the Metaculus question IDs in `questions.js`. To find the correct IDs:

1. Go to https://www.metaculus.com/tournament/bridgewater/
2. Click on a question
3. The URL will be like: `https://www.metaculus.com/questions/32426/...`
4. The number `32426` is the question ID
5. Update the `questionId` field in `questions.js`

Example:
```javascript
{
    id: 1,
    title: "Will the X algorithm be run by Grok before March 12, 2026?",
    questionId: "32426", // <-- Update this with the actual Metaculus question ID
    category: "tech",
    // ...
}
```

### Adding New Questions

To add a new question, append to the `questions` array in `questions.js`:

```javascript
{
    id: 16,
    title: "Your question title",
    questionId: "12345", // Metaculus question ID
    category: "tech", // tech, geopolitics, economics, or entertainment
    closes: "2026-03-14", // Close date
    myForecast: "50%", // Your forecast
    community: "45%", // Community forecast
    folder: "BW2026_Q16_FOLDER_NAME"
}
```

## Troubleshooting

### iframes not loading?

If you see "Loading forecast data..." but the questions don't appear:

1. **CORS Issues**: Some browsers block iframes from localhost. Try:
   - Use `http://127.0.0.1:8000` instead of `localhost`
   - Or use a proper HTTP server (see Getting Started above)

2. **Wrong Question IDs**: Verify the question IDs in `questions.js` are correct

3. **Metaculus Embed Disabled**: Check if the question allows embedding by visiting:
   ```
   https://www.metaculus.com/questions/embed/[QUESTION_ID]/
   ```

### Questions not refreshing?

- Click the "🔄 Refresh All" button
- Or press `R` on your keyboard
- Check your browser console for errors (F12)

## Project Structure

```
dashboard/
├── index.html      # Main HTML structure
├── app.js          # Application logic
├── questions.js    # Question data configuration
└── README.md       # This file
```

## Customization

### Change Colors

Edit the gradient in `index.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change Layout

Modify the grid template in `index.html`:

```css
.grid {
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
}
```

### Change Auto-Refresh Interval

Edit in `app.js`:

```javascript
// Change 5 * 60 * 1000 (5 minutes) to your preferred interval
setInterval(() => {
    refreshAllIframes();
    updateLastUpdateTime();
}, 5 * 60 * 1000); // milliseconds
```

## Links

- [Bridgewater Tournament](https://www.metaculus.com/tournament/bridgewater/)
- [Metaculus Embed Documentation](https://www.metaculus.com/notebooks/17313/now-you-can-share-embed-all-question-types/)
- [Competition Details](https://www.bridgewater.com/bridgewater-x-metaculus-2026-competition)

## License

MIT License - feel free to customize and share!

---

**Prize Pool**: $30,000
**Competition Ends**: March 13, 2026

Good luck with your forecasts! 🎯
