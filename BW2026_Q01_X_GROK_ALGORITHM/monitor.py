#!/usr/bin/env python3
"""
Monitor: X Algorithm Powered by Grok
Question: Will the X algorithm be run by Grok before March 12, 2026?
Forecast: 12% YES
"""

import json
import urllib.request
import re
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

QUESTION = {
    'id': 'BW2026_Q02_X_GROK_ALGORITHM',
    'title': 'Will the X algorithm be run by Grok before March 12, 2026?',
    'forecast': 0.12,
    'closes': '2026-02-28',
    'resolution_date': '2026-03-12',
}

# Keywords to monitor
KEYWORDS = [
    'Grok algorithm', 'X algorithm Grok', 'Grok exclusively',
    'Grok recommendation', 'xAI algorithm', 'Musk algorithm announcement'
]

# Key accounts/sources
MONITOR_SOURCES = [
    '@elonmusk', '@xai', '@X', 'xAI blog', 'X engineering'
]

# Update triggers
TRIGGERS = {
    'musk_announces_complete': {'condition': 'Musk announces Grok exclusively runs X', 'new_forecast': 0.85},
    'xai_blog_complete': {'condition': 'xAI blog announces completion', 'new_forecast': 0.75},
    'jan17_grok_only_code': {'condition': 'Jan 17 open-source shows Grok-only', 'new_forecast': 0.45},
    'jan17_hybrid_code': {'condition': 'Jan 17 open-source shows hybrid system', 'new_forecast': 0.05},
    'musk_says_still_working': {'condition': 'Musk tweets "still working on" transition', 'new_forecast': 0.06},
    'tech_analysis_other_models': {'condition': 'Technical analysis shows other ML models active', 'new_forecast': 0.03},
}

TRACKER_FILE = Path(__file__).parent / 'tracker.json'

# =============================================================================
# TRACKER FUNCTIONS
# =============================================================================

def load_tracker():
    try:
        with open(TRACKER_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'forecast': QUESTION['forecast'],
            'status': 'monitoring',
            'events': [],
            'last_check': None,
            'key_dates': {
                'jan17_opensource': '2026-01-17',
                'question_closes': '2026-02-28',
                'resolution': '2026-03-12'
            },
            'forecast_history': [{'date': datetime.now().isoformat(), 'forecast': QUESTION['forecast'], 'reason': 'Initial'}]
        }

def save_tracker(data):
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def add_event(event_type: str, description: str, source: str = ''):
    """Add an event. Run: python monitor.py add "announcement" "Musk tweeted X" "Twitter" """
    t = load_tracker()
    t['events'].append({
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'type': event_type,
        'description': description,
        'source': source
    })
    t['last_check'] = datetime.now().isoformat()
    save_tracker(t)
    print(f"✓ Added event: {event_type}")
    print(f"  Description: {description}")

def update_forecast(new_forecast: float, reason: str):
    """Update forecast. Run: python monitor.py forecast 0.05 "Jan 17 showed hybrid" """
    t = load_tracker()
    old = t['forecast']
    t['forecast'] = new_forecast
    t['forecast_history'].append({
        'date': datetime.now().isoformat(),
        'forecast': new_forecast,
        'reason': reason
    })
    save_tracker(t)
    print(f"Forecast updated: {old:.0%} → {new_forecast:.0%}")
    print(f"Reason: {reason}")

# =============================================================================
# NEWS CHECK
# =============================================================================

def check_news():
    """Check tech news for X/Grok algorithm announcements."""
    print("\n📰 CHECKING NEWS...")
    
    feeds = [
        ('TechCrunch', 'https://techcrunch.com/feed/'),
        ('The Verge', 'https://www.theverge.com/rss/index.xml'),
    ]
    
    alerts = []
    search_terms = ['grok', 'x algorithm', 'xai', 'musk algorithm', 'recommendation']
    
    for name, url in feeds:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8')
            
            items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
            
            for item in items[:15]:
                title = re.search(r'<title>(.*?)</title>', item)
                title = title.group(1) if title else ''
                title_lower = title.lower()
                
                if any(term in title_lower for term in search_terms):
                    alerts.append({'source': name, 'title': title})
        except Exception as e:
            print(f"  Error checking {name}: {e}")
    
    if alerts:
        print(f"\n🚨 FOUND {len(alerts)} RELEVANT ARTICLES:")
        for a in alerts:
            print(f"   [{a['source']}] {a['title'][:60]}...")
    else:
        print("   ✓ No major news found")
    
    return alerts

# =============================================================================
# STATUS DISPLAY
# =============================================================================

def show_status():
    """Show current monitoring status."""
    t = load_tracker()
    
    # Calculate days
    today = datetime.now()
    jan17 = datetime.strptime('2026-01-17', '%Y-%m-%d')
    closes = datetime.strptime(QUESTION['closes'], '%Y-%m-%d')
    resolution = datetime.strptime(QUESTION['resolution_date'], '%Y-%m-%d')
    
    days_to_jan17 = (jan17 - today).days
    days_to_close = (closes - today).days
    days_to_resolution = (resolution - today).days
    
    print("=" * 60)
    print(f"  {QUESTION['id']}")
    print(f"  {QUESTION['title']}")
    print("=" * 60)
    
    print(f"\n  Current Forecast: {t['forecast']:.0%}")
    print(f"  Community:        5%")
    print(f"  Status:           {t.get('status', 'monitoring')}")
    
    print(f"\n  Key Dates:")
    print(f"    Jan 17 (open-source): {days_to_jan17} days {'⚠️ CRITICAL' if days_to_jan17 <= 7 else ''}")
    print(f"    Question closes:      {days_to_close} days")
    print(f"    Resolution:           {days_to_resolution} days")
    
    # Recent events
    if t.get('events'):
        print(f"\n  Recent events:")
        for e in t['events'][-3:]:
            print(f"    [{e['date']}] {e['type']}: {e['description'][:40]}...")
    
    # What to watch
    print(f"\n  📍 WHAT TO WATCH:")
    print(f"    1. @elonmusk, @xai, @X for announcements")
    print(f"    2. Jan 17 open-source release - will reveal if Grok-only")
    print(f"    3. Tech reporter analysis of X algorithm")
    
    print("=" * 60)

def run_daily():
    """Run daily monitoring check."""
    print(f"\n🔍 Daily Check: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    show_status()
    check_news()
    
    t = load_tracker()
    t['last_check'] = datetime.now().isoformat()
    save_tracker(t)
    
    # Check if Jan 17 is approaching
    jan17 = datetime.strptime('2026-01-17', '%Y-%m-%d')
    days_to_jan17 = (jan17 - datetime.now()).days
    
    if days_to_jan17 <= 5 and days_to_jan17 > 0:
        print(f"\n⚠️  CRITICAL: Jan 17 open-source release in {days_to_jan17} days!")
        print("   This will likely reveal if Grok runs algorithm exclusively.")
        print("   Be ready to update forecast based on what code shows.")
    elif days_to_jan17 <= 0:
        print(f"\n🔴 Jan 17 has passed - check if open-source was released!")
        print("   If released: analyze code for Grok-only vs hybrid")
        print("   If delayed: decrease forecast to ~8%")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        run_daily()
    elif sys.argv[1] == 'status':
        show_status()
    elif sys.argv[1] == 'news':
        check_news()
    elif sys.argv[1] == 'add' and len(sys.argv) >= 4:
        add_event(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else '')
    elif sys.argv[1] == 'forecast' and len(sys.argv) >= 4:
        update_forecast(float(sys.argv[2]), sys.argv[3])
    else:
        print("""
Usage:
  python monitor.py              # Run daily check
  python monitor.py status       # Show status only
  python monitor.py news         # Check news only
  python monitor.py add "type" "description" "source"  # Add event
  python monitor.py forecast 0.05 "reason"             # Update forecast
""")
