#!/usr/bin/env python3
"""
AI Industry Layoffs Monitor
============================

Automated monitoring for Metaculus question:
"Will layoffs.fyi report at least 100 AI industry layoffs between Jan 12 - Mar 13, 2026?"

This script:
1. Searches for AI company layoff news
2. Tracks cumulative count toward 100 threshold
3. Uses Claude API to analyze if findings are relevant
4. Sends alerts when significant news is found

Setup:
    pip install requests beautifulsoup4 anthropic feedparser python-dotenv

Environment variables (.env file):
    ANTHROPIC_API_KEY=your_key_here
    EMAIL_FROM=your_email@gmail.com (optional)
    EMAIL_PASSWORD=your_app_password (optional)
    EMAIL_TO=your_email@gmail.com (optional)

Run:
    python ai_layoffs_monitor.py

Cron (run every 12 hours):
    0 */12 * * * cd /path/to/script && python ai_layoffs_monitor.py >> monitor.log 2>&1
"""

import os
import json
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import hashlib

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    "forecast": {
        "question": "Will layoffs.fyi report ≥100 AI industry layoffs between Jan 12 - Mar 13, 2026?",
        "current_probability": 32,
        "threshold": 100,
        "start_date": "2026-01-12",
        "end_date": "2026-03-13",
        "resolution_date": "2026-03-14"
    },
    "tracking": {
        "cumulative_count": 0,  # Update this as layoffs are confirmed
        "last_updated": None,
        "confirmed_events": []
    },
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "state_file": "ai_layoffs_state.json"
}

# AI companies to watch (high-risk for layoffs)
AI_COMPANIES_WATCHLIST = [
    # Frontier labs (low risk but high impact)
    "OpenAI", "Anthropic", "Google DeepMind", "xAI", "Meta AI", "Microsoft AI",
    # Medium-high risk companies
    "Stability AI", "Scale AI", "Character AI", "Inflection AI", "Cohere",
    "Hugging Face", "Runway", "Jasper", "Copy.ai", "Midjourney",
    # AI infrastructure
    "Cerebras", "SambaNova", "Graphcore", "Groq",
    # Other AI companies
    "Adept", "AI21 Labs", "Aleph Alpha", "Imbue", "Mistral",
    "Perplexity", "Pika", "Reka", "Synthesia", "Weights & Biases"
]

# Keywords for filtering
LAYOFF_KEYWORDS = [
    "layoff", "laid off", "job cuts", "workforce reduction",
    "restructuring", "downsizing", "let go", "terminated",
    "firing", "staff cuts", "headcount reduction"
]

AI_INDUSTRY_KEYWORDS = [
    "AI company", "AI startup", "artificial intelligence",
    "machine learning", "ML company", "AI lab", "AI firm"
]

# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def load_state() -> dict:
    """Load tracking state from file."""
    try:
        with open(CONFIG["state_file"], "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "cumulative_count": 0,
            "confirmed_events": [],
            "seen_hashes": [],
            "last_run": None,
            "forecast_history": []
        }

def save_state(state: dict):
    """Save state to file."""
    state["last_run"] = datetime.now().isoformat()
    with open(CONFIG["state_file"], "w") as f:
        json.dump(state, f, indent=2)

def get_content_hash(content: str) -> str:
    """Generate hash for deduplication."""
    return hashlib.md5(content.encode()).hexdigest()[:16]

# =============================================================================
# NEWS SEARCH FUNCTIONS
# =============================================================================

def search_google_news(query: str, days_back: int = 3) -> List[Dict]:
    """Search Google News RSS for relevant articles."""
    results = []
    encoded_query = requests.utils.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}+when:{days_back}d&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            results.append({
                "source": f"Google News - {entry.get('source', {}).get('title', 'Unknown')}",
                "title": entry.get("title", "")[:200],
                "description": entry.get("summary", "")[:500],
                "url": entry.get("link", ""),
                "date": entry.get("published", "")[:25],
                "type": "news"
            })
        print(f"✓ Google News '{query}': {len(results)} results")
    except Exception as e:
        print(f"✗ Google News search failed: {e}")
    
    return results

def search_for_ai_layoffs() -> List[Dict]:
    """Search for AI company layoff news."""
    all_results = []
    
    # General AI layoff searches
    queries = [
        "AI company layoffs",
        "AI startup layoffs 2026",
        "artificial intelligence job cuts",
        "AI lab restructuring",
        "machine learning company layoffs"
    ]
    
    # Company-specific searches for high-risk companies
    high_risk_companies = ["Stability AI", "Scale AI", "Character AI", "Inflection AI"]
    for company in high_risk_companies:
        queries.append(f"{company} layoffs")
    
    for query in queries:
        results = search_google_news(query, days_back=3)
        all_results.extend(results)
        
    return all_results

def check_trueup_layoffs() -> List[Dict]:
    """Check TrueUp layoffs tracker."""
    results = []
    url = "https://www.trueup.io/layoffs"
    
    try:
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # Check for AI-related layoffs
            for company in AI_COMPANIES_WATCHLIST:
                if company.lower() in text:
                    results.append({
                        "source": "TrueUp Layoffs",
                        "title": f"Potential layoff mention: {company}",
                        "description": f"Found mention of {company} on TrueUp layoffs tracker",
                        "url": url,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "tracker",
                        "company": company
                    })
            
            print(f"✓ TrueUp check complete: {len(results)} AI company mentions")
    except Exception as e:
        print(f"✗ TrueUp check failed: {e}")
    
    return results

# =============================================================================
# CLAUDE API ANALYSIS
# =============================================================================

def analyze_with_claude(items: List[Dict], state: dict) -> Dict:
    """Use Claude API to analyze news items and update forecast."""
    if not CONFIG["anthropic_api_key"]:
        print("⚠ ANTHROPIC_API_KEY not set, using keyword analysis")
        return keyword_analysis(items, state)
    
    # Prepare items for analysis
    items_text = "\n\n".join([
        f"ITEM {i+1}:\nSource: {item['source']}\nTitle: {item['title']}\nDescription: {item.get('description', 'N/A')}"
        for i, item in enumerate(items[:15])
    ])
    
    if not items_text.strip():
        return {"relevant_items": [], "forecast_update": None}
    
    prompt = f"""You are analyzing news for a forecasting question about AI INDUSTRY layoffs.

QUESTION: "Will layoffs.fyi report at least 100 AI industry layoffs between Jan 12 - Mar 13, 2026?"

CRITICAL DISTINCTION: This is about layoffs AT AI companies (like OpenAI, Stability AI, xAI), 
NOT about layoffs CAUSED BY AI at other companies.

Current tracking:
- Cumulative AI industry layoffs so far: {state.get('cumulative_count', 0)}
- Threshold needed: 100
- Current forecast: {CONFIG['forecast']['current_probability']}%

AI companies to watch: {', '.join(AI_COMPANIES_WATCHLIST[:15])}

Analyze these news items:
{items_text}

For EACH item, determine:
1. Is this about an AI COMPANY having layoffs? (not AI causing layoffs elsewhere)
2. If yes, which company and how many people?
3. Relevance: HIGH (confirmed AI company layoff) / MEDIUM (possible/rumored) / LOW (not relevant)

Then provide:
- List of relevant items with company name and estimated layoff count
- Whether the forecast should change and why

Respond in JSON:
{{
  "analyses": [
    {{"item": 1, "is_ai_company_layoff": true/false, "company": "name or null", 
      "estimated_count": number or null, "relevance": "HIGH/MEDIUM/LOW", "reasoning": "..."}}
  ],
  "total_new_layoffs": number,
  "forecast_recommendation": {{
    "direction": "UP/DOWN/UNCHANGED",
    "new_probability": number or null,
    "reasoning": "..."
  }}
}}"""

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CONFIG["anthropic_api_key"])
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        
        # Extract JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            analysis = json.loads(json_match.group())
            
            relevant_items = []
            for i, item_analysis in enumerate(analysis.get("analyses", [])):
                if item_analysis.get("relevance") in ["HIGH", "MEDIUM"]:
                    if i < len(items):
                        items[i]["analysis"] = item_analysis
                        relevant_items.append(items[i])
            
            return {
                "relevant_items": relevant_items,
                "total_new_layoffs": analysis.get("total_new_layoffs", 0),
                "forecast_update": analysis.get("forecast_recommendation")
            }
        
        print("✓ Claude analysis complete")
        
    except ImportError:
        print("⚠ anthropic package not installed")
        return keyword_analysis(items, state)
    except Exception as e:
        print(f"✗ Claude analysis failed: {e}")
        return keyword_analysis(items, state)
    
    return {"relevant_items": [], "forecast_update": None}

def keyword_analysis(items: List[Dict], state: dict) -> Dict:
    """Fallback keyword-based analysis."""
    relevant_items = []
    
    for item in items:
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        
        # Check if it mentions an AI company
        mentioned_company = None
        for company in AI_COMPANIES_WATCHLIST:
            if company.lower() in text:
                mentioned_company = company
                break
        
        # Check if it mentions layoffs
        has_layoff = any(kw in text for kw in LAYOFF_KEYWORDS)
        
        if mentioned_company and has_layoff:
            item["analysis"] = {
                "company": mentioned_company,
                "relevance": "HIGH",
                "reasoning": f"Mentions {mentioned_company} and layoff keywords"
            }
            relevant_items.append(item)
        elif has_layoff and any(kw in text for kw in AI_INDUSTRY_KEYWORDS):
            item["analysis"] = {
                "company": "Unknown AI company",
                "relevance": "MEDIUM",
                "reasoning": "Mentions AI industry and layoff keywords"
            }
            relevant_items.append(item)
    
    print(f"✓ Keyword analysis: {len(relevant_items)} relevant items")
    return {"relevant_items": relevant_items, "forecast_update": None}

# =============================================================================
# FORECAST UPDATE LOGIC
# =============================================================================

def calculate_updated_forecast(state: dict, new_layoffs: int = 0) -> dict:
    """Calculate updated forecast based on current cumulative count."""
    
    cumulative = state.get("cumulative_count", 0) + new_layoffs
    threshold = CONFIG["forecast"]["threshold"]
    
    # Days elapsed and remaining
    start = datetime.strptime(CONFIG["forecast"]["start_date"], "%Y-%m-%d")
    end = datetime.strptime(CONFIG["forecast"]["end_date"], "%Y-%m-%d")
    today = datetime.now()
    
    days_elapsed = (today - start).days
    days_remaining = (end - today).days
    total_days = (end - start).days
    
    # Calculate progress
    progress_pct = (cumulative / threshold) * 100 if threshold > 0 else 0
    
    # Simple heuristic for forecast update
    base_forecast = CONFIG["forecast"]["current_probability"]
    
    if cumulative >= threshold:
        new_forecast = 99  # Already resolved YES
    elif cumulative >= 70:
        new_forecast = 85  # Very likely to hit threshold
    elif cumulative >= 50:
        new_forecast = 65  # On track
    elif days_remaining < 30 and cumulative < 30:
        new_forecast = max(15, base_forecast - 10)  # Behind pace
    elif days_remaining < 14 and cumulative < 50:
        new_forecast = max(10, base_forecast - 15)  # Unlikely
    else:
        new_forecast = base_forecast  # No change
    
    return {
        "cumulative_count": cumulative,
        "threshold": threshold,
        "progress_pct": round(progress_pct, 1),
        "days_elapsed": days_elapsed,
        "days_remaining": max(0, days_remaining),
        "base_forecast": base_forecast,
        "updated_forecast": new_forecast,
        "status": "ON_TRACK" if cumulative >= (days_elapsed / total_days) * threshold * 0.8 else "BEHIND"
    }

# =============================================================================
# ALERT FORMATTING
# =============================================================================

def format_alert(relevant_items: List[Dict], forecast_info: dict) -> str:
    """Format alert message."""
    lines = [
        "=" * 60,
        "AI INDUSTRY LAYOFFS MONITOR ALERT",
        "=" * 60,
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "PROGRESS TRACKER:",
        f"  Cumulative count: {forecast_info['cumulative_count']} / {forecast_info['threshold']}",
        f"  Progress: {forecast_info['progress_pct']}%",
        f"  Days remaining: {forecast_info['days_remaining']}",
        f"  Status: {forecast_info['status']}",
        "",
        f"FORECAST: {forecast_info['base_forecast']}% → {forecast_info['updated_forecast']}%",
        "",
    ]
    
    if relevant_items:
        lines.extend([
            "RELEVANT NEWS ITEMS:",
            "-" * 40,
        ])
        
        for i, item in enumerate(relevant_items, 1):
            analysis = item.get("analysis", {})
            lines.extend([
                f"\n[{i}] {item['title']}",
                f"    Source: {item['source']}",
                f"    Company: {analysis.get('company', 'Unknown')}",
                f"    Relevance: {analysis.get('relevance', 'Unknown')}",
                f"    URL: {item.get('url', 'N/A')}",
            ])
    else:
        lines.append("No new relevant items found.")
    
    lines.extend([
        "",
        "=" * 60,
        "NEXT STEPS:",
        "1. Verify any HIGH relevance items at layoffs.fyi",
        "2. Update cumulative count if confirmed",
        "3. Check: https://layoffs.fyi/ (filter by Industry=AI)",
        "=" * 60,
    ])
    
    return "\n".join(lines)

# =============================================================================
# MAIN MONITORING FUNCTION
# =============================================================================

def run_monitor():
    """Main monitoring function."""
    print("\n" + "=" * 60)
    print(f"AI LAYOFFS MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Load state
    state = load_state()
    all_items = []
    
    # 1. Search for AI layoff news
    print("\n[1/3] Searching for AI company layoff news...")
    all_items.extend(search_for_ai_layoffs())
    
    # 2. Check layoff trackers
    print("\n[2/3] Checking layoff trackers...")
    all_items.extend(check_trueup_layoffs())
    
    # 3. Deduplicate
    seen_hashes = set(state.get("seen_hashes", []))
    unique_items = []
    for item in all_items:
        h = get_content_hash(item.get("title", "") + item.get("url", ""))
        if h not in seen_hashes:
            unique_items.append(item)
            seen_hashes.add(h)
    
    print(f"\n   Total items: {len(all_items)}, New items: {len(unique_items)}")
    
    # 4. Analyze with Claude
    print("\n[3/3] Analyzing relevance...")
    analysis_result = {"relevant_items": [], "forecast_update": None}
    if unique_items:
        analysis_result = analyze_with_claude(unique_items, state)
    
    relevant_items = analysis_result.get("relevant_items", [])
    new_layoffs = analysis_result.get("total_new_layoffs", 0)
    
    # 5. Calculate forecast update
    forecast_info = calculate_updated_forecast(state, new_layoffs)
    
    # 6. Generate alert
    alert_text = format_alert(relevant_items, forecast_info)
    print("\n" + alert_text)
    
    # 7. Update and save state
    state["seen_hashes"] = list(seen_hashes)[-500:]
    state["cumulative_count"] = forecast_info["cumulative_count"]
    if relevant_items:
        state["forecast_history"].append({
            "date": datetime.now().isoformat(),
            "forecast": forecast_info["updated_forecast"],
            "cumulative": forecast_info["cumulative_count"]
        })
    save_state(state)
    
    # 8. Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Items checked: {len(all_items)}")
    print(f"New items: {len(unique_items)}")
    print(f"Relevant items: {len(relevant_items)}")
    print(f"Cumulative count: {forecast_info['cumulative_count']}")
    print(f"Current forecast: {forecast_info['updated_forecast']}%")
    print("=" * 60)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "items_checked": len(all_items),
        "relevant_items": len(relevant_items),
        "cumulative_count": forecast_info["cumulative_count"],
        "forecast": forecast_info["updated_forecast"]
    }

# =============================================================================
# QUICK CHECK WITH CLAUDE (simpler version)
# =============================================================================

def quick_check():
    """Quick check using Claude's web search capability."""
    if not CONFIG["anthropic_api_key"]:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return
    
    print("\n" + "=" * 60)
    print("AI LAYOFFS QUICK CHECK")
    print("=" * 60)
    
    prompt = """Search for recent news about layoffs at AI companies.

I'm tracking a forecast: "Will layoffs.fyi report ≥100 AI industry layoffs between Jan 12 - Mar 13, 2026?"

Current status: ~0 confirmed AI industry layoffs so far in 2026
Threshold: 100 people
Current forecast: 32%

Please search for:
1. Any AI COMPANY layoffs announced in the past week
2. News about Stability AI, Scale AI, Character AI, or other AI startups
3. Any AI company restructuring or workforce changes

IMPORTANT: I need layoffs AT AI companies, not layoffs CAUSED BY AI at other companies.

For each relevant finding, tell me:
- Company name
- Number of people laid off (if known)
- Date
- Source

Then update the cumulative count and tell me if the forecast should change."""

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CONFIG["anthropic_api_key"])
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        print("\nSEARCH RESULTS:")
        print("-" * 60)
        print(response.content[0].text)
        print("-" * 60)
        
    except Exception as e:
        print(f"ERROR: {e}")

# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Industry Layoffs Monitor")
    parser.add_argument("--quick", action="store_true", help="Quick check with Claude")
    parser.add_argument("--update-count", type=int, help="Manually update cumulative count")
    parser.add_argument("--status", action="store_true", help="Show current status")
    args = parser.parse_args()
    
    if args.quick:
        quick_check()
    elif args.update_count is not None:
        state = load_state()
        state["cumulative_count"] = args.update_count
        save_state(state)
        print(f"Updated cumulative count to {args.update_count}")
    elif args.status:
        state = load_state()
        forecast_info = calculate_updated_forecast(state)
        print(f"\nCurrent Status:")
        print(f"  Cumulative: {forecast_info['cumulative_count']} / {forecast_info['threshold']}")
        print(f"  Progress: {forecast_info['progress_pct']}%")
        print(f"  Days remaining: {forecast_info['days_remaining']}")
        print(f"  Forecast: {forecast_info['updated_forecast']}%")
    else:
        run_monitor()
