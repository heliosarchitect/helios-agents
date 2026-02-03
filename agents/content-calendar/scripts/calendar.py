#!/usr/bin/env python3
"""
Content Calendar - Plan and track social media posts
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime, date

CALENDAR_FILE = Path.home() / ".openclaw/workspace/content-calendar.yaml"

def load_calendar():
    if not CALENDAR_FILE.exists():
        return {"posts": [], "ideas": []}
    with open(CALENDAR_FILE) as f:
        return yaml.safe_load(f) or {"posts": [], "ideas": []}

def save_calendar(data):
    CALENDAR_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CALENDAR_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def show_calendar(data):
    posts = data.get("posts", [])
    ideas = data.get("ideas", [])
    
    print("📅 CONTENT CALENDAR\n")
    
    # Upcoming
    today = date.today()
    upcoming = [p for p in posts if p.get("status") == "planned"]
    upcoming.sort(key=lambda x: x.get("scheduled", "9999"))
    
    if upcoming:
        print("📌 Upcoming Posts:")
        for p in upcoming[:5]:
            sched = p.get("scheduled", "TBD")
            platform = p.get("platform", "?")
            topic = p.get("topic", "Untitled")[:40]
            
            # Days until
            try:
                sched_date = datetime.strptime(sched, "%Y-%m-%d").date()
                days = (sched_date - today).days
                if days < 0:
                    days_str = f"⚠️ {-days}d overdue"
                elif days == 0:
                    days_str = "🔥 TODAY"
                elif days == 1:
                    days_str = "Tomorrow"
                else:
                    days_str = f"In {days}d"
            except:
                days_str = ""
            
            print(f"   [{p.get('id', '?')}] {sched} | {platform} | {topic}")
            if days_str:
                print(f"       {days_str}")
        print()
    
    # Recent
    recent = [p for p in posts if p.get("status") == "posted"]
    recent.sort(key=lambda x: x.get("posted_at", "0000"), reverse=True)
    
    if recent:
        print("✅ Recently Posted:")
        for p in recent[:3]:
            posted = p.get("posted_at", "?")
            topic = p.get("topic", "Untitled")[:40]
            print(f"   {posted} | {topic}")
        print()
    
    # Ideas
    if ideas:
        print(f"💡 Ideas Pipeline ({len(ideas)}):")
        for idea in ideas[:5]:
            print(f"   • {idea}")
        print()
    
    # Stats
    total = len(posts)
    posted = len([p for p in posts if p.get("status") == "posted"])
    planned = len([p for p in posts if p.get("status") == "planned"])
    
    print(f"📊 Stats: {posted} posted | {planned} planned | {len(ideas)} ideas")

def add_post(data, topic, platform, scheduled, submolt=None):
    posts = data.setdefault("posts", [])
    
    # Generate ID
    max_id = max([p.get("id", 0) for p in posts], default=0)
    new_id = max_id + 1
    
    post = {
        "id": new_id,
        "topic": topic,
        "platform": platform,
        "scheduled": scheduled,
        "status": "planned",
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    
    if submolt:
        post["submolt"] = submolt
    
    posts.append(post)
    save_calendar(data)
    
    print(f"✅ Added post #{new_id}: {topic}")
    print(f"   Scheduled: {scheduled} on {platform}")

def mark_posted(data, post_id):
    for post in data.get("posts", []):
        if post.get("id") == post_id:
            post["status"] = "posted"
            post["posted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_calendar(data)
            print(f"✅ Marked #{post_id} as posted")
            return
    print(f"❌ Post #{post_id} not found")

def add_idea(data, idea):
    ideas = data.setdefault("ideas", [])
    ideas.append(idea)
    save_calendar(data)
    print(f"✅ Added idea: {idea}")

def main():
    parser = argparse.ArgumentParser(description="Content calendar management")
    parser.add_argument("--add", help="Add planned post (topic)")
    parser.add_argument("--platform", default="moltbook", help="Platform")
    parser.add_argument("--date", help="Scheduled date (YYYY-MM-DD)")
    parser.add_argument("--submolt", help="Moltbook submolt")
    parser.add_argument("--posted", type=int, help="Mark post ID as posted")
    parser.add_argument("--idea", help="Add idea to pipeline")
    
    args = parser.parse_args()
    data = load_calendar()
    
    if args.add:
        scheduled = args.date or date.today().strftime("%Y-%m-%d")
        add_post(data, args.add, args.platform, scheduled, args.submolt)
    elif args.posted:
        mark_posted(data, args.posted)
    elif args.idea:
        add_idea(data, args.idea)
    else:
        show_calendar(data)

if __name__ == "__main__":
    main()
