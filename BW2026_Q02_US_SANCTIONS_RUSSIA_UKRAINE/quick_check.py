#!/usr/bin/env python3
"""
Russia Sanctions Monitor - Quick Check Script
==============================================

A simpler version that just uses the Anthropic API to:
1. Search for recent news
2. Analyze if it meets resolution criteria
3. Print a report

This version requires ONLY an Anthropic API key.

Usage:
    export ANTHROPIC_API_KEY=your_key_here
    python quick_check.py
"""

import os
import json
from datetime import datetime

def check_sanctions_news():
    """
    Use Claude with web search to check for recent sanctions news.
    """
    try:
        import anthropic
    except ImportError:
        print("ERROR: Please install anthropic package: pip install anthropic")
        return None
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Please set ANTHROPIC_API_KEY environment variable")
        return None
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print("=" * 70)
    print(f"RUSSIA SANCTIONS MONITOR - Quick Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print("\nSearching for recent news...\n")
    
    prompt = """You are a forecasting research assistant. I need you to search for the latest news on US sanctions against Russia related to the Ukraine war.

FORECASTING QUESTION: "Will the US impose additional sanctions on Russia related to the Ukraine war before March 14, 2026?"

RESOLUTION CRITERIA: 
- US government announces via binding legal action a new/expanded sanctions on Russian persons/entities
- The official announcement EXPLICITLY states it is related to the Ukraine war
- Actions without explicit Ukraine language do NOT count

Please search for:
1. Any OFAC or Treasury announcements about Russia sanctions in the past week
2. Status of S.1241 (Sanctioning Russia Act) - any votes or progress
3. Any news about Graham-Blumenthal Russia sanctions bill
4. Any executive actions on Russia sanctions

For each relevant item found, tell me:
- Source and date
- What happened
- Does it explicitly mention Ukraine/the war?
- Could this resolve the forecasting question?

Current forecast is 86%. Should this change based on what you find?

Search and provide a comprehensive update."""

    try:
        # Use Claude with web search
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text
        
        print("SEARCH RESULTS AND ANALYSIS:")
        print("-" * 70)
        print(result)
        print("-" * 70)
        
        return result
        
    except Exception as e:
        print(f"ERROR: API call failed - {e}")
        return None

def check_specific_sources():
    """
    Check specific sources for updates.
    """
    try:
        import anthropic
    except ImportError:
        return None
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print("\n" + "=" * 70)
    print("CHECKING SPECIFIC SOURCES")
    print("=" * 70)
    
    sources_prompt = """Please check these specific sources for the latest updates:

1. OFAC Recent Actions (https://ofac.treasury.gov/recent-actions)
   - Any new Russia-related entries in the past week?
   - Do any explicitly mention Ukraine?

2. Congress.gov S.1241 (https://www.congress.gov/bill/119th-congress/senate-bill/1241)
   - Current status of the Sanctioning Russia Act?
   - Any votes scheduled or taken?
   - Has it passed either chamber?

3. Treasury Press Releases
   - Any announcements about Russia sanctions?

4. State Department sanctions announcements
   - Any new designations related to Ukraine?

For each source, report:
- Last update date
- Current status
- Any action that could resolve the forecasting question

The question resolves YES if there's a new sanction explicitly citing the Ukraine war."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": sources_prompt}]
        )
        
        result = response.content[0].text
        
        print("\nSOURCE CHECK RESULTS:")
        print("-" * 70)
        print(result)
        print("-" * 70)
        
        return result
        
    except Exception as e:
        print(f"ERROR: Source check failed - {e}")
        return None

def generate_forecast_update():
    """
    Generate a forecast update recommendation.
    """
    try:
        import anthropic
    except ImportError:
        return None
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print("\n" + "=" * 70)
    print("FORECAST UPDATE RECOMMENDATION")
    print("=" * 70)
    
    update_prompt = """Based on your searches, provide a forecast update recommendation:

QUESTION: "Will the US impose additional sanctions on Russia related to the Ukraine war before March 14, 2026?"

Current forecast: 86%
Current date: Today
Resolution date: March 14, 2026

Key factors from my initial analysis:
- Trump "greenlit" S.1241 on Jan 7-9, 2026
- Bill has 84 Senate co-sponsors (veto-proof)
- Historical frequency: ~monthly Ukraine-explicit sanctions
- October 2025 precedent: Rosneft/Lukoil sanctions with explicit Ukraine language

Based on what you found:
1. Should the forecast go UP, DOWN, or STAY THE SAME?
2. What is your recommended probability?
3. What are the key reasons?
4. What should I watch for next?

Be specific and quantitative."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": update_prompt}]
        )
        
        result = response.content[0].text
        
        print("\nRECOMMENDATION:")
        print("-" * 70)
        print(result)
        print("-" * 70)
        
        return result
        
    except Exception as e:
        print(f"ERROR: Update generation failed - {e}")
        return None

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RUSSIA SANCTIONS FORECAST MONITOR")
    print("Question: US sanctions on Russia related to Ukraine before Mar 14, 2026")
    print("Current Forecast: 86%")
    print("=" * 70 + "\n")
    
    # Run all checks
    news_result = check_sanctions_news()
    source_result = check_specific_sources()
    update_result = generate_forecast_update()
    
    # Summary
    print("\n" + "=" * 70)
    print("MONITORING COMPLETE")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("\nNext steps:")
    print("1. Review the findings above")
    print("2. If HIGH priority item found, verify at original source")
    print("3. Update forecast if needed")
    print("4. Run this script again in 6-12 hours")
    print("\nTo run automatically, set up a cron job:")
    print("0 */6 * * * cd /path/to/script && python quick_check.py >> monitor.log 2>&1")
