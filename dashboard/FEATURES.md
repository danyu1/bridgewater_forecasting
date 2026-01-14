# 🎯 Dashboard Features & Screenshots

## Live Dashboard Features

### 1. **Real-Time Forecast Embeds**
- Each question is embedded directly from Metaculus
- Updates automatically as forecasts change
- Shows community predictions, your predictions, and live probability distributions
- No manual refresh needed (auto-refreshes every 5 minutes)

### 2. **Smart Filtering & Categories**
The dashboard organizes all 15 questions into categories:

- 🔬 **Tech & AI** (6 questions)
  - X/Grok Algorithm
  - AI Industry Layoffs
  - NVIDIA Export Controls
  - OpenAI Pricing
  - Hyperscaler Capex
  - ASML China Sales

- 🌍 **Geopolitics** (2 questions)
  - Russia/Ukraine Sanctions
  - US-China Tariffs

- 💰 **Economics** (5 questions)
  - US Manufacturing PMI
  - Electric Utility Capex
  - India WPI Inflation
  - S&P 500 / Payrolls

- 🎮 **Entertainment** (2 questions)
  - Winter Olympics Medal Table
  - Grammy Video Game Soundtrack

### 3. **Dashboard Statistics**
Top banner shows:
- Total questions tracked
- Visible questions (after filtering)
- Days remaining until competition ends
- Competition end date

### 4. **Layout Options**

#### Grid View (Default)
- Shows 2-3 questions per row on desktop
- Optimized for comparing multiple forecasts at once
- Perfect for overview monitoring

#### Single Column View
- One question per row
- Better for focused analysis
- Easier reading on smaller screens

### 5. **Question Cards**

Each card displays:
- 📊 **Question title** - Clear, concise question text
- 📁 **Question number** - Q01 through Q15
- 📊 **Your forecast** - Your probability/prediction
- 👥 **Community forecast** - Aggregated community prediction
- 🗓️ **Close date** - When the question closes
- 📈 **Live embed** - Interactive Metaculus forecast widget

Color-coded by category:
- 🔵 Blue/Purple = Tech & AI
- 🔴 Red = Geopolitics
- 🟢 Green = Economics
- 🟠 Orange = Entertainment

### 6. **Interactive Controls**

**Layout Selector**
- Switch between grid and single column view
- Preference persists during session

**Category Filter**
- Show all questions
- Or filter to specific category
- Updates question count dynamically

**Refresh Button**
- Manually refresh all embeds
- Shows confirmation animation
- Useful when you want immediate updates

**Fullscreen Toggle**
- Expand dashboard to fullscreen
- Perfect for presentations or focus mode
- Exit with same button or ESC key

### 7. **Keyboard Shortcuts**

Power user features for quick navigation:

| Key | Action | Description |
|-----|--------|-------------|
| `R` | Refresh | Reload all forecast embeds |
| `F` | Fullscreen | Toggle fullscreen mode |
| `1` | All | Show all questions |
| `2` | Tech | Filter to Tech & AI |
| `3` | Geopolitics | Filter to Geopolitics |
| `4` | Economics | Filter to Economics |
| `5` | Entertainment | Filter to Entertainment |

### 8. **Auto-Refresh**
- Dashboard automatically refreshes every 5 minutes
- Ensures you always see latest forecasts
- Configurable in `app.js` if you want different interval
- No need to manually reload the page

### 9. **Responsive Design**
- **Desktop**: Multi-column grid layout
- **Tablet**: 1-2 columns, optimized spacing
- **Mobile**: Single column, full-width cards
- Touch-friendly controls on all devices

### 10. **Beautiful UI**
- Modern gradient background (purple/blue)
- Clean white cards with shadows
- Smooth animations and transitions
- Professional typography
- Color-coded categories
- Loading animations for embeds

### 11. **Status Tracking**
- Last update timestamp at bottom
- Loading indicators for each embed
- Visible question count updates
- Days remaining countdown

### 12. **Browser Compatibility**
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Brave

## Technical Features

### Performance
- Lazy loading for iframe embeds
- Efficient DOM manipulation
- Minimal JavaScript overhead
- Fast initial page load

### Security
- Sandboxed iframes
- CORS headers configured
- No external dependencies (no npm packages)
- Pure vanilla JavaScript

### Accessibility
- Semantic HTML structure
- Keyboard navigation support
- Clear visual hierarchy
- Readable font sizes
- High contrast text

### Customization
- Easy to modify colors/styling
- Configurable refresh intervals
- Add/remove questions easily
- Adjustable layout breakpoints

## Use Cases

### 1. **Competition Monitoring**
Keep the dashboard open in a browser tab and check back throughout the day to see:
- How community forecasts are shifting
- When new information causes probability updates
- Track your position relative to the crowd

### 2. **Research & Analysis**
- Compare forecasts across similar questions
- Spot patterns in market movements
- Identify potential arbitrage opportunities
- Track correlations between related questions

### 3. **Presentations**
- Fullscreen mode for demos
- Professional appearance for meetings
- Live data impresses audiences
- Category filtering for focused discussions

### 4. **Learning**
- Study how experienced forecasters update
- Observe market reactions to news
- Learn calibration by comparing predictions
- Understand probability distributions

### 5. **Portfolio Management**
- Monitor all your forecasts in one place
- Track which questions need updates
- See which questions are closing soon
- Prioritize your forecasting time

## Planned Enhancements

Future features you could add:
- [ ] Export data to CSV
- [ ] Historical probability charts
- [ ] Alert notifications for major changes
- [ ] Integration with your forecast notes
- [ ] Comparison to your local forecasts
- [ ] Automatic syncing with local markdown files
- [ ] Dark mode toggle
- [ ] Custom sorting options
- [ ] Question search/filter
- [ ] Bookmark favorite questions

## Performance Tips

**For Best Experience:**
1. Use a modern browser (Chrome/Firefox recommended)
2. Keep the dashboard in a dedicated tab
3. Enable hardware acceleration in browser settings
4. Close other heavy tabs if running slow
5. Use grid view for overview, single column for deep analysis

**For Multiple Monitors:**
- Keep dashboard on secondary monitor
- Use fullscreen mode for clean look
- Filter to category you're actively researching

**For Mobile:**
- Single column view works best
- Landscape orientation gives more space
- Tap cards to see full embed details

---

## Summary

This dashboard transforms your Bridgewater forecasting workflow by:

✅ Consolidating all 15 questions in one place
✅ Providing live, real-time updates from Metaculus
✅ Offering powerful filtering and layout options
✅ Supporting efficient keyboard navigation
✅ Looking professional and polished
✅ Running entirely locally (no cloud dependencies)
✅ Being fully customizable to your needs

**Result**: Spend less time navigating between pages, more time making accurate forecasts!

---

*Built with ❤️ for the Bridgewater x Metaculus 2026 Competition*
