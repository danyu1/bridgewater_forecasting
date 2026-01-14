#!/usr/bin/env python3
"""
Russia Sanctions Forecast - Automated Monitoring System
========================================================

This script automatically:
1. Scrapes OFAC Recent Actions page
2. Searches news via multiple APIs
3. Uses Claude API to analyze if findings meet resolution criteria
4. Sends email alerts when relevant news is found

Setup:
    pip install requests beautifulsoup4 anthropic feedparser python-dotenv

Environment variables needed (.env file):
    ANTHROPIC_API_KEY=your_key_here
    NEWS_API_KEY=your_newsapi_key (from newsapi.org - free tier available)
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    EMAIL_FROM=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    EMAIL_TO=your_email@gmail.com

Run:
    python automated_monitor.py

Cron (run every 6 hours):
    0 */6 * * * cd /path/to/script && python automated_monitor.py >> monitor.log 2>&1
"""

import os
import json
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import time

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
        "question": "Will the US impose additional sanctions on Russia related to Ukraine war before March 14, 2026?",
        "current_probability": 86,
        "resolution_date": "2026-03-14"
    },
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "news_api_key": os.getenv("NEWS_API_KEY", ""),
    "email": {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "from": os.getenv("EMAIL_FROM", ""),
        "password": os.getenv("EMAIL_PASSWORD", ""),
        "to": os.getenv("EMAIL_TO", "")
    },
    "state_file": "monitor_state.json"
}

# Keywords for filtering
RESOLUTION_KEYWORDS = [
    "ukraine war", "war in ukraine", "invasion of ukraine", "russia's war",
    "russian aggression", "peace process", "peace negotiations", "putin's war"
]

SANCTIONS_KEYWORDS = [
    "sanctions", "ofac", "treasury", "designated", "blocked persons",
    "sdn list", "entity list", "executive order", "asset freeze"
]

# =============================================================================
# STATE MANAGEMENT (avoid duplicate alerts)
# =============================================================================

def load_state() -> dict:
    """Load previously seen items to avoid duplicate alerts."""
    try:
        with open(CONFIG["state_file"], "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"seen_hashes": [], "last_run": None, "alerts_sent": []}

def save_state(state: dict):
    """Save state to file."""
    state["last_run"] = datetime.now().isoformat()
    with open(CONFIG["state_file"], "w") as f:
        json.dump(state, f, indent=2)

def get_content_hash(content: str) -> str:
    """Generate hash for deduplication."""
    return hashlib.md5(content.encode()).hexdigest()[:16]

# =============================================================================
# WEB SCRAPING - OFAC RECENT ACTIONS
# =============================================================================

def scrape_ofac_recent_actions() -> List[Dict]:
    """Scrape OFAC Recent Actions page for Russia-related entries."""
    url = "https://ofac.treasury.gov/recent-actions"
    results = []
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all action entries (structure may vary)
        entries = soup.find_all(['div', 'tr', 'li'], class_=lambda x: x and 'action' in x.lower()) or \
                  soup.find_all('a', href=lambda x: x and 'recent-actions' in x)
        
        # Also search for any text containing Russia
        all_text = soup.get_text()
        if 'russia' in all_text.lower():
            # Find links to recent Russia-related actions
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text().strip()
                if 'russia' in text.lower() or 'russia' in href.lower():
                    results.append({
                        "source": "OFAC Recent Actions",
                        "title": text[:200],
                        "url": f"https://ofac.treasury.gov{href}" if href.startswith('/') else href,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "official"
                    })
        
        print(f"✓ OFAC scrape complete: found {len(results)} Russia-related items")
        
    except Exception as e:
        print(f"✗ OFAC scrape failed: {e}")
    
    return results

def scrape_treasury_press() -> List[Dict]:
    """Scrape Treasury press releases for Russia sanctions news."""
    url = "https://home.treasury.gov/news/press-releases"
    results = []
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find press release entries
        for article in soup.find_all(['article', 'div'], class_=lambda x: x and ('press' in str(x).lower() or 'release' in str(x).lower())):
            text = article.get_text().lower()
            if 'russia' in text or 'sanctions' in text:
                title_elem = article.find(['h2', 'h3', 'a'])
                if title_elem:
                    link = title_elem.find('a') or title_elem
                    href = link.get('href', '') if link.name == 'a' else ''
                    results.append({
                        "source": "Treasury Press Release",
                        "title": title_elem.get_text().strip()[:200],
                        "url": f"https://home.treasury.gov{href}" if href.startswith('/') else href,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "official"
                    })
        
        print(f"✓ Treasury scrape complete: found {len(results)} relevant items")
        
    except Exception as e:
        print(f"✗ Treasury scrape failed: {e}")
    
    return results

# =============================================================================
# NEWS API SEARCH
# =============================================================================

def search_news_api(query: str, days_back: int = 3) -> List[Dict]:
    """Search NewsAPI for relevant articles."""
    if not CONFIG["news_api_key"]:
        print("⚠ NEWS_API_KEY not set, skipping NewsAPI search")
        return []
    
    results = []
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": CONFIG["news_api_key"],
        "pageSize": 20
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for article in data.get("articles", []):
            results.append({
                "source": f"NewsAPI - {article.get('source', {}).get('name', 'Unknown')}",
                "title": article.get("title", "")[:200],
                "description": article.get("description", "")[:500],
                "url": article.get("url", ""),
                "date": article.get("publishedAt", "")[:10],
                "type": "news"
            })
        
        print(f"✓ NewsAPI search '{query}': found {len(results)} articles")
        
    except Exception as e:
        print(f"✗ NewsAPI search failed: {e}")
    
    return results

def search_google_news_rss(query: str) -> List[Dict]:
    """Search Google News RSS feed (no API key needed)."""
    results = []
    
    # URL encode the query
    encoded_query = requests.utils.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:15]:  # Limit to 15 results
            results.append({
                "source": f"Google News - {entry.get('source', {}).get('title', 'Unknown')}",
                "title": entry.get("title", "")[:200],
                "description": entry.get("summary", "")[:500],
                "url": entry.get("link", ""),
                "date": entry.get("published", "")[:10],
                "type": "news"
            })
        
        print(f"✓ Google News RSS '{query}': found {len(results)} articles")
        
    except Exception as e:
        print(f"✗ Google News RSS failed: {e}")
    
    return results

def search_congress_gov() -> List[Dict]:
    """Check Congress.gov for S.1241 status updates."""
    results = []
    url = "https://www.congress.gov/bill/119th-congress/senate-bill/1241/all-actions"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for action items
        actions = soup.find_all(['tr', 'li'], class_=lambda x: x and 'action' in str(x).lower())
        
        # Get the page text to check for status
        text = soup.get_text()
        
        # Check for key status indicators
        status_keywords = ['passed senate', 'passed house', 'signed', 'enrolled', 'became law', 'cloture']
        for keyword in status_keywords:
            if keyword in text.lower():
                results.append({
                    "source": "Congress.gov S.1241",
                    "title": f"S.1241 Status Update: '{keyword}' found",
                    "description": f"The Sanctioning Russia Act appears to have status: {keyword}",
                    "url": url,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "type": "legislative",
                    "priority": "HIGH"
                })
        
        print(f"✓ Congress.gov check complete: found {len(results)} status updates")
        
    except Exception as e:
        print(f"✗ Congress.gov check failed: {e}")
    
    return results

# =============================================================================
# CLAUDE API ANALYSIS
# =============================================================================

def analyze_with_claude(items: List[Dict]) -> List[Dict]:
    """Use Claude API to analyze if items meet resolution criteria."""
    if not CONFIG["anthropic_api_key"]:
        print("⚠ ANTHROPIC_API_KEY not set, skipping AI analysis")
        # Fall back to keyword matching
        return keyword_analysis(items)
    
    analyzed = []
    
    # Batch items for efficiency
    batch_text = "\n\n".join([
        f"ITEM {i+1}:\nSource: {item['source']}\nTitle: {item['title']}\nDescription: {item.get('description', 'N/A')}"
        for i, item in enumerate(items[:10])  # Limit to 10 items per call
    ])
    
    if not batch_text.strip():
        return []
    
    prompt = f"""You are analyzing news items for a forecasting question:

QUESTION: "Will the US impose additional sanctions on Russia related to the Ukraine war before March 14, 2026?"

RESOLUTION CRITERIA: The question resolves YES if the US government announces via binding legal action a new or expanded sanctions-related restriction on Russian persons or entities AND the official announcement EXPLICITLY states it is related to the Ukraine war.

Key point: Actions not explicitly linked to the war in official announcements do NOT count, even if plausibly war-motivated.

Example that WOULD count: OFAC stating sanctions are imposed "as a result of Russia's lack of serious commitment to a peace process to end the war in Ukraine."

Analyze these news items and for each one, respond with:
1. ITEM NUMBER
2. RELEVANCE: HIGH/MEDIUM/LOW/NONE
3. LIKELY_RESOLVES: YES/POSSIBLY/NO
4. REASONING: Brief explanation
5. ACTION_NEEDED: What the user should do

NEWS ITEMS TO ANALYZE:
{batch_text}

Respond in JSON format:
{{"analyses": [
  {{"item": 1, "relevance": "HIGH", "likely_resolves": "POSSIBLY", "reasoning": "...", "action": "..."}},
  ...
]}}"""

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CONFIG["anthropic_api_key"])
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        response_text = response.content[0].text
        
        # Try to extract JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            analysis_data = json.loads(json_match.group())
            
            for analysis in analysis_data.get("analyses", []):
                item_idx = analysis.get("item", 1) - 1
                if 0 <= item_idx < len(items):
                    items[item_idx]["ai_analysis"] = {
                        "relevance": analysis.get("relevance", "UNKNOWN"),
                        "likely_resolves": analysis.get("likely_resolves", "UNKNOWN"),
                        "reasoning": analysis.get("reasoning", ""),
                        "action": analysis.get("action", "")
                    }
                    
                    if analysis.get("relevance") in ["HIGH", "MEDIUM"]:
                        analyzed.append(items[item_idx])
        
        print(f"✓ Claude analysis complete: {len(analyzed)} high/medium relevance items")
        
    except ImportError:
        print("⚠ anthropic package not installed, using keyword analysis")
        return keyword_analysis(items)
    except Exception as e:
        print(f"✗ Claude analysis failed: {e}")
        return keyword_analysis(items)
    
    return analyzed

def keyword_analysis(items: List[Dict]) -> List[Dict]:
    """Fallback keyword-based analysis."""
    analyzed = []
    
    for item in items:
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        
        has_sanctions = any(kw in text for kw in SANCTIONS_KEYWORDS)
        has_ukraine = any(kw in text for kw in RESOLUTION_KEYWORDS)
        
        if has_sanctions and has_ukraine:
            relevance = "HIGH"
            likely_resolves = "POSSIBLY"
            reasoning = "Contains both sanctions and Ukraine war keywords"
        elif has_sanctions:
            relevance = "MEDIUM"
            likely_resolves = "NO"
            reasoning = "Sanctions mentioned but no explicit Ukraine link"
        else:
            relevance = "LOW"
            likely_resolves = "NO"
            reasoning = "No relevant keywords found"
            continue  # Skip low relevance
        
        item["ai_analysis"] = {
            "relevance": relevance,
            "likely_resolves": likely_resolves,
            "reasoning": reasoning,
            "action": "Check official source for exact language" if relevance == "HIGH" else "Monitor"
        }
        
        if relevance in ["HIGH", "MEDIUM"]:
            analyzed.append(item)
    
    print(f"✓ Keyword analysis complete: {len(analyzed)} relevant items")
    return analyzed

# =============================================================================
# EMAIL ALERTS
# =============================================================================

def send_email_alert(subject: str, body: str):
    """Send email alert."""
    if not all([CONFIG["email"]["from"], CONFIG["email"]["password"], CONFIG["email"]["to"]]):
        print("⚠ Email not configured, printing alert instead:")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{body}")
        return
    
    try:
        msg = MIMEMultipart()
        msg["From"] = CONFIG["email"]["from"]
        msg["To"] = CONFIG["email"]["to"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(CONFIG["email"]["smtp_server"], CONFIG["email"]["smtp_port"]) as server:
            server.starttls()
            server.login(CONFIG["email"]["from"], CONFIG["email"]["password"])
            server.send_message(msg)
        
        print(f"✓ Email alert sent: {subject}")
        
    except Exception as e:
        print(f"✗ Email failed: {e}")
        print(f"Alert content:\n{body}")

def format_alert(items: List[Dict]) -> str:
    """Format items into alert message."""
    lines = [
        "RUSSIA SANCTIONS FORECAST MONITOR ALERT",
        "=" * 50,
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Current Forecast: {CONFIG['forecast']['current_probability']}%",
        "",
        "RELEVANT ITEMS FOUND:",
        ""
    ]
    
    for i, item in enumerate(items, 1):
        analysis = item.get("ai_analysis", {})
        lines.extend([
            f"--- Item {i} ---",
            f"Source: {item['source']}",
            f"Title: {item['title']}",
            f"URL: {item.get('url', 'N/A')}",
            f"Date: {item.get('date', 'N/A')}",
            f"Relevance: {analysis.get('relevance', 'UNKNOWN')}",
            f"Likely Resolves: {analysis.get('likely_resolves', 'UNKNOWN')}",
            f"Reasoning: {analysis.get('reasoning', 'N/A')}",
            f"Action: {analysis.get('action', 'N/A')}",
            ""
        ])
    
    lines.extend([
        "=" * 50,
        "NEXT STEPS:",
        "1. Check the URLs above for full details",
        "2. If OFAC/Treasury action, verify explicit Ukraine language",
        "3. Update forecast if needed",
        "",
        "Key sources to verify:",
        "- OFAC: https://ofac.treasury.gov/recent-actions",
        "- Treasury: https://home.treasury.gov/news/press-releases",
        "- Congress: https://www.congress.gov/bill/119th-congress/senate-bill/1241"
    ])
    
    return "\n".join(lines)

# =============================================================================
# MAIN MONITORING FUNCTION
# =============================================================================

def run_monitor():
    """Main monitoring function."""
    print("\n" + "=" * 60)
    print(f"RUSSIA SANCTIONS MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60 + "\n")
    
    # Load state
    state = load_state()
    all_items = []
    
    # 1. Scrape official sources
    print("\n[1/4] Checking official sources...")
    all_items.extend(scrape_ofac_recent_actions())
    all_items.extend(scrape_treasury_press())
    all_items.extend(search_congress_gov())
    
    # 2. Search news
    print("\n[2/4] Searching news sources...")
    news_queries = [
        "OFAC Russia sanctions",
        "US Russia sanctions Ukraine",
        "Sanctioning Russia Act S.1241",
        "Treasury Russia sanctions",
        "Graham Blumenthal Russia bill"
    ]
    
    for query in news_queries:
        all_items.extend(search_google_news_rss(query))
        time.sleep(1)  # Rate limiting
    
    # Also try NewsAPI if configured
    if CONFIG["news_api_key"]:
        all_items.extend(search_news_api("US Russia sanctions Ukraine", days_back=2))
    
    # 3. Deduplicate
    print("\n[3/4] Deduplicating results...")
    seen_hashes = set(state.get("seen_hashes", []))
    unique_items = []
    
    for item in all_items:
        content_hash = get_content_hash(item.get("title", "") + item.get("url", ""))
        if content_hash not in seen_hashes:
            unique_items.append(item)
            seen_hashes.add(content_hash)
    
    print(f"   {len(all_items)} total items, {len(unique_items)} new items")
    
    # 4. Analyze with AI
    print("\n[4/4] Analyzing relevance...")
    if unique_items:
        relevant_items = analyze_with_claude(unique_items)
    else:
        relevant_items = []
    
    # 5. Send alerts if needed
    high_priority = [item for item in relevant_items 
                     if item.get("ai_analysis", {}).get("relevance") == "HIGH"]
    
    if high_priority:
        print(f"\n🚨 {len(high_priority)} HIGH PRIORITY items found!")
        subject = f"[URGENT] Russia Sanctions Alert - {len(high_priority)} items"
        body = format_alert(high_priority)
        send_email_alert(subject, body)
    elif relevant_items:
        print(f"\n📋 {len(relevant_items)} relevant items found (none high priority)")
        # Optionally send digest for medium items
        # subject = f"Russia Sanctions Monitor - {len(relevant_items)} items"
        # body = format_alert(relevant_items)
        # send_email_alert(subject, body)
    else:
        print("\n✓ No relevant items found this run")
    
    # 6. Save state
    state["seen_hashes"] = list(seen_hashes)[-1000:]  # Keep last 1000
    save_state(state)
    
    # 7. Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Items checked: {len(all_items)}")
    print(f"New items: {len(unique_items)}")
    print(f"Relevant items: {len(relevant_items)}")
    print(f"High priority: {len(high_priority)}")
    print(f"Next run: Set up cron for every 6 hours")
    print("=" * 60 + "\n")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "items_checked": len(all_items),
        "new_items": len(unique_items),
        "relevant_items": len(relevant_items),
        "high_priority": len(high_priority),
        "alerts_sent": len(high_priority) > 0
    }

# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Russia Sanctions Forecast Monitor")
    parser.add_argument("--test-email", action="store_true", help="Send test email")
    parser.add_argument("--test-claude", action="store_true", help="Test Claude API")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending alerts")
    args = parser.parse_args()
    
    if args.test_email:
        send_email_alert(
            "Test Alert - Russia Sanctions Monitor",
            "This is a test email from the monitoring system."
        )
    elif args.test_claude:
        test_items = [{
            "source": "Test",
            "title": "US Treasury imposes sanctions on Russian entities over Ukraine war",
            "description": "OFAC designated several Russian companies citing Russia's continued aggression in Ukraine."
        }]
        results = analyze_with_claude(test_items)
        print(json.dumps(results, indent=2))
    else:
        result = run_monitor()
        print(json.dumps(result, indent=2))
