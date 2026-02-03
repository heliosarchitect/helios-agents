#!/usr/bin/env python3
"""
Self-Reflection Coach - Learn from experience

This script reads memory files and extracts patterns for reflection.
For deeper analysis, use the OpenClaw reflect() tool directly.
"""

import argparse
from pathlib import Path
from datetime import datetime, timedelta
import re
from collections import Counter

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"

def get_memory_files(days=7):
    """Get memory files from the last N days"""
    files = []
    today = datetime.now().date()
    
    for i in range(days):
        date = today - timedelta(days=i)
        filepath = MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        if filepath.exists():
            files.append(filepath)
    
    return files

def extract_patterns(text):
    """Extract patterns from memory text"""
    patterns = {
        "successes": [],
        "failures": [],
        "learnings": [],
        "decisions": [],
    }
    
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        
        # Success patterns
        if any(w in line_lower for w in ['✅', 'success', 'worked', 'completed', 'fixed', 'solved']):
            patterns["successes"].append(line.strip()[:100])
        
        # Failure patterns
        if any(w in line_lower for w in ['❌', 'failed', 'error', 'mistake', 'wrong', "didn't work"]):
            patterns["failures"].append(line.strip()[:100])
        
        # Learning patterns
        if any(w in line_lower for w in ['learned', 'realized', 'discovered', 'insight', 'til', 'note:']):
            patterns["learnings"].append(line.strip()[:100])
        
        # Decision patterns
        if any(w in line_lower for w in ['decided', 'chose', 'will', 'going to', 'plan to']):
            patterns["decisions"].append(line.strip()[:100])
    
    return patterns

def extract_themes(text):
    """Extract recurring themes/topics"""
    # Common topic keywords
    topic_keywords = {
        "trading": ["trade", "bot", "price", "buy", "sell", "profit", "loss"],
        "moltbook": ["moltbook", "post", "comment", "karma", "engage"],
        "coding": ["code", "script", "fix", "build", "implement", "function"],
        "memory": ["memory", "cortex", "store", "recall", "remember"],
        "communication": ["matthew", "signal", "message", "reply", "respond"],
    }
    
    text_lower = text.lower()
    theme_counts = Counter()
    
    for theme, keywords in topic_keywords.items():
        count = sum(text_lower.count(kw) for kw in keywords)
        if count > 0:
            theme_counts[theme] = count
    
    return dict(theme_counts.most_common(5))

def generate_reflection(patterns, themes, period):
    """Generate reflection output"""
    lines = [
        f"🪞 SELF-REFLECTION ({period})",
        f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        ""
    ]
    
    # Themes
    if themes:
        lines.append("📊 Focus Areas:")
        for theme, count in themes.items():
            bar = "█" * min(count // 2, 10)
            lines.append(f"   {theme}: {bar} ({count} mentions)")
        lines.append("")
    
    # Successes
    if patterns["successes"]:
        lines.append(f"✅ Successes ({len(patterns['successes'])}):")
        for s in patterns["successes"][:5]:
            lines.append(f"   • {s}")
        lines.append("")
    
    # Failures
    if patterns["failures"]:
        lines.append(f"❌ Challenges ({len(patterns['failures'])}):")
        for f in patterns["failures"][:5]:
            lines.append(f"   • {f}")
        lines.append("")
    
    # Learnings
    if patterns["learnings"]:
        lines.append(f"💡 Learnings ({len(patterns['learnings'])}):")
        for l in patterns["learnings"][:5]:
            lines.append(f"   • {l}")
        lines.append("")
    
    # Synthesis
    lines.extend([
        "🎯 Reflection Questions:",
        "   1. What pattern appears most often in successes?",
        "   2. Is there a common thread in the challenges?",
        "   3. What one thing would most improve effectiveness?",
        "",
        "💪 Suggested Action:",
    ])
    
    if len(patterns["failures"]) > len(patterns["successes"]):
        lines.append("   Focus on reducing errors before expanding scope")
    elif "trading" in themes and themes.get("trading", 0) > 10:
        lines.append("   Heavy trading focus - ensure it's profitable before continuing")
    else:
        lines.append("   Continue current patterns while documenting learnings")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Self-reflection through memory analysis")
    parser.add_argument("--period", choices=["day", "week", "month"], default="week")
    parser.add_argument("--focus", help="Focus on specific area")
    parser.add_argument("--store", action="store_true", help="Store reflection in Cortex")
    
    args = parser.parse_args()
    
    days = {"day": 1, "week": 7, "month": 30}[args.period]
    
    files = get_memory_files(days)
    
    if not files:
        print(f"📭 No memory files found for the last {days} days")
        print(f"   Looking in: {MEMORY_DIR}")
        return
    
    # Read all memory content
    all_text = ""
    for f in files:
        try:
            all_text += f.read_text() + "\n"
        except:
            pass
    
    if args.focus:
        # Filter to focus area
        lines = [l for l in all_text.split('\n') if args.focus.lower() in l.lower()]
        all_text = '\n'.join(lines)
    
    patterns = extract_patterns(all_text)
    themes = extract_themes(all_text)
    
    reflection = generate_reflection(patterns, themes, args.period)
    print(reflection)
    
    # Note about deeper analysis
    print("\n" + "="*50)
    print("💡 For deeper analysis, use OpenClaw's reflect() tool:")
    print(f"   reflect(period='{args.period}')")

if __name__ == "__main__":
    main()
