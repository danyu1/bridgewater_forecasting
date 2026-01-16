import json, re, time
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

PRICING_URLS = [
    "https://platform.openai.com/docs/pricing",
    "https://platform.openai.com/pricing",
    "https://openai.com/pricing",
    "https://openai.com/api/pricing"
]

NEWS_QUERIES = [
    "OpenAI API pricing",
    "GPT-5 pricing",
    "GPT-6 pricing",
    "OpenAI price cut"
]

results = {"timestamp": datetime.utcnow().isoformat(), "pricing": [], "news": []}

for url in PRICING_URLS:
    try:
        r = requests.get(url, timeout=20)
        status = r.status_code
        text = r.text
        soup = BeautifulSoup(text, "html.parser")
        flat = " ".join(soup.get_text(" ").split()).lower()
        hits = []
        for m in re.finditer(r"gpt-[56][^\\s]{0,20}", flat):
            start = max(0, m.start()-80)
            end = min(len(flat), m.end()+80)
            hits.append(flat[start:end])
        results["pricing"].append({"url": url, "status": status, "hits": hits[:10]})
    except Exception as e:
        results["pricing"].append({"url": url, "error": str(e)})

for q in NEWS_QUERIES:
    rss = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss)
    items = []
    for entry in feed.entries[:10]:
        items.append({"title": entry.get("title", ""), "link": entry.get("link", ""), "published": entry.get("published", "")})
    results["news"].append({"query": q, "results": items})
    time.sleep(0.5)

print(json.dumps(results, indent=2))
