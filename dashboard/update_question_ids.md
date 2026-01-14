# How to Update Metaculus Question IDs

The dashboard needs the actual Metaculus question IDs to embed the live forecasts. Here's how to find and update them:

## Quick Method (Manual)

1. Go to https://www.metaculus.com/tournament/bridgewater/
2. Click on each question
3. Look at the URL in your browser: `https://www.metaculus.com/questions/32426/will-the-x-algorithm-be-run-by-grok`
4. The number `32426` is the question ID
5. Update that number in `questions.js`

## Example Questions from Bridgewater Tournament

Based on the tournament, here are some likely question IDs (you'll need to verify these):

### Page 1 Questions:
- **Q01 - X/Grok Algorithm**: https://www.metaculus.com/questions/[ID]/
- **Q02 - Russia Sanctions**: https://www.metaculus.com/questions/[ID]/
- **Q03 - AI Layoffs**: https://www.metaculus.com/questions/[ID]/
- **Q04 - US-China Tariffs**: https://www.metaculus.com/questions/[ID]/
- **Q05 - NVIDIA/Blackwell**: https://www.metaculus.com/questions/[ID]/

### Page 2 Questions:
- **Q07 - Winter Olympics**: https://www.metaculus.com/questions/[ID]/
- **Q08 - OpenAI Pricing**: https://www.metaculus.com/questions/[ID]/
- **Q09 - US Manufacturing PMI**: https://www.metaculus.com/questions/[ID]/
- **Q10 - ASML China Share**: https://www.metaculus.com/questions/[ID]/
- **Q11 - Hyperscaler Capex**: https://www.metaculus.com/questions/[ID]/
- **Q12 - Electric Utility Capex**: https://www.metaculus.com/questions/[ID]/
- **Q13 - Grammy Video Game**: https://www.metaculus.com/questions/[ID]/
- **Q14 - India WPI**: https://www.metaculus.com/questions/[ID]/
- **Q15 - S&P 500 / Payrolls**: https://www.metaculus.com/questions/[ID]/

## After You Get the IDs

Edit `questions.js` and update each `questionId` field:

```javascript
{
    id: 1,
    title: "Will the X algorithm be run by Grok before March 12, 2026?",
    questionId: "32426", // <-- Replace with actual ID
    category: "tech",
    closes: "2026-02-28",
    myForecast: "12%",
    community: "5%",
    folder: "BW2026_Q01_X_GROK_ALGORITHM"
}
```

## Testing Embed URLs

To verify a question ID works, try visiting:
```
https://www.metaculus.com/questions/embed/[QUESTION_ID]/
```

If it loads, the ID is correct!

## Automated Method (Browser Console)

If you want to extract all IDs at once:

1. Go to https://www.metaculus.com/tournament/bridgewater/
2. Open browser DevTools (F12)
3. Go to Console tab
4. Paste this code:

```javascript
// Extract all question links from the tournament page
const links = Array.from(document.querySelectorAll('a[href*="/questions/"]'));
const questionIds = links
  .map(link => {
    const match = link.href.match(/questions\/(\d+)/);
    return match ? match[1] : null;
  })
  .filter(id => id !== null);

console.table(questionIds);
console.log('Copy these IDs:', JSON.stringify(questionIds, null, 2));
```

5. Copy the IDs and update `questions.js`

## Need Help?

If the embed URLs don't work:
1. Check if the question allows embedding
2. Verify you're using the correct question ID
3. Try viewing the embed URL directly in your browser
4. Check browser console for errors (F12)

---

**Note**: Metaculus embed format is:
```
https://www.metaculus.com/questions/embed/[QUESTION_ID]/
```

The dashboard uses this format automatically once you provide the IDs.
