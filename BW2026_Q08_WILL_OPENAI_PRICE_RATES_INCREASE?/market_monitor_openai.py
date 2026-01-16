import json
import requests
from datetime import datetime

POLY_URL = "https://clob.polymarket.com/markets?limit=200&active=true"
MANIFOLD_URL = "https://api.manifold.markets/v0/search-markets?term=OpenAI%20pricing"

out = {"timestamp": datetime.utcnow().isoformat(), "polymarket": [], "manifold": []}

try:
    r = requests.get(POLY_URL, timeout=20)
    r.raise_for_status()
    data = r.json().get("data", [])
    for m in data:
        q = m.get("question", "")
        if any(k in q.lower() for k in ["openai","gpt","pricing","chatgpt","anthropic","claude","gemini"]):
            tokens = m.get("tokens", [])
            price = tokens[0].get("price") if tokens else None
            out["polymarket"].append({
                "question": q,
                "price": price,
                "slug": m.get("market_slug"),
                "liquidity": m.get("liquidity"),
                "volume24": m.get("volume24hr")
            })
except Exception as e:
    out["polymarket"].append({"error": str(e)})

try:
    r = requests.get(MANIFOLD_URL, timeout=20)
    r.raise_for_status()
    data = r.json()
    for m in data:
        q = m.get("question", "")
        if any(k in q.lower() for k in ["openai","gpt","pricing","chatgpt"]):
            out["manifold"].append({
                "question": q,
                "probability": m.get("probability"),
                "url": f"https://manifold.markets/{m.get('creatorUsername','')}/{m.get('slug','')}"
            })
except Exception as e:
    out["manifold"].append({"error": str(e)})

print(json.dumps(out, indent=2))
