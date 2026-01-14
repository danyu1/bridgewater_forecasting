import requests, feedparser, json, time
from datetime import datetime, timedelta
from urllib.parse import quote

NEWS_KEYWORDS = [
    "Norway ski team injury",
    "biathlon Germany World Cup",
    "freestyle skiing United States",
    "snowboard Canada",
    "Italy alpine skiing",
    "Winter Olympics medal table",
    "Norway gold medals",
    "Germany gold medals",
    "United States gold medals",
    "Canada gold medals",
    "Italy gold medals"
]

POLYMARKET_TEXT = "Winter Olympics medal"
POLYMARKET_URL = "https://clob.polymarket.com/markets?limit=200&active=true"

def fetch_polymarket():
    try:
        r = requests.get(POLYMARKET_URL, timeout=20)
        r.raise_for_status()
        data = r.json().get("data", [])
        results = []
        for m in data:
            title = m.get("question", "")
            if any(x.lower() in title.lower() for x in ["winter", "olympic", "medal"]):
                outcomes = m.get("outcomes", [])
                yes_price = None
                if outcomes:
                    yes_price = outcomes[0].get("price")
                results.append({
                    "title": title,
                    "url": f"https://polymarket.com/event/{m.get('slug','')}",
                    "yes_price": yes_price,
                    "liquidity": m.get("liquidity"),
                    "volume24": m.get("volume24hr"),
                    "as_of": datetime.utcnow().isoformat()
                })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def fetch_google_news(query, days=7, limit=10):
    url = f"https://news.google.com/rss/search?q={quote(query)}+when:{days}d&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", "")
        })
    return items

def run_once():
    report = {"timestamp": datetime.utcnow().isoformat()}
    report["polymarket"] = fetch_polymarket()
    news_hits = []
    for kw in NEWS_KEYWORDS:
        hits = fetch_google_news(kw, days=7, limit=5)
        if hits:
            news_hits.append({"keyword": kw, "results": hits})
        time.sleep(0.5)
    report["news"] = news_hits
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_once()
