#!/usr/bin/env python3
"""
Goal Tracker - Check progress on long-term goals
"""

import argparse
import yaml
import sys
from pathlib import Path
from datetime import datetime, date

GOALS_FILE = Path.home() / ".openclaw/workspace/goals.yaml"

def load_goals():
    if not GOALS_FILE.exists():
        print(f"⚠️  No goals file found at {GOALS_FILE}")
        print("Create one with your goals! See SKILL.md for format.")
        return {"goals": []}
    
    with open(GOALS_FILE) as f:
        return yaml.safe_load(f) or {"goals": []}

def save_goals(data):
    with open(GOALS_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def progress_bar(current, target, width=20):
    pct = min(current / target, 1.0) if target > 0 else 0
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct*100:.1f}%"

def days_until(deadline_str):
    if not deadline_str:
        return None
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        delta = deadline - date.today()
        return delta.days
    except:
        return None

def check_goals(data, verbose=True):
    goals = data.get("goals", [])
    
    if not goals:
        print("📭 No goals defined yet!")
        return
    
    print("🎯 GOAL STATUS\n")
    
    needs_attention = []
    celebrations = []
    
    for goal in goals:
        name = goal.get("name", "Unnamed")
        current = goal.get("current", 0)
        target = goal.get("target", 100)
        unit = goal.get("unit", "")
        deadline = goal.get("deadline")
        milestones = goal.get("milestones", [])
        
        pct = (current / target * 100) if target > 0 else 0
        bar = progress_bar(current, target)
        
        print(f"📌 {name}")
        print(f"   {bar}")
        print(f"   {current:,.2f} / {target:,.2f} {unit}")
        
        if deadline:
            days = days_until(deadline)
            if days is not None:
                if days < 0:
                    print(f"   ⚠️  OVERDUE by {-days} days!")
                    needs_attention.append(name)
                elif days < 30:
                    print(f"   ⏰ {days} days remaining")
                else:
                    print(f"   📅 Due: {deadline}")
        
        # Check milestones
        for ms in milestones:
            ms_target = ms.get("target", 0)
            ms_done = ms.get("done", False)
            ms_name = ms.get("name", "Milestone")
            
            if not ms_done and current >= ms_target:
                ms["done"] = True
                celebrations.append(f"🎉 MILESTONE: {ms_name} on '{name}'!")
            
            icon = "✅" if ms.get("done") else "⬜"
            print(f"   {icon} {ms_name} ({ms_target:,.0f} {unit})")
        
        print()
    
    # Show celebrations
    for c in celebrations:
        print(c)
    
    if celebrations:
        save_goals(data)
        print("(Goals file updated with completed milestones)\n")
    
    # Summary
    total = len(goals)
    on_track = sum(1 for g in goals if g.get("current", 0) / g.get("target", 1) >= 0.1)
    print(f"📊 {on_track}/{total} goals with meaningful progress")
    
    if needs_attention:
        print(f"⚠️  Needs attention: {', '.join(needs_attention)}")

def update_goal(data, goal_id, current):
    for goal in data.get("goals", []):
        if goal.get("id") == goal_id:
            old = goal.get("current", 0)
            goal["current"] = current
            save_goals(data)
            print(f"✅ Updated '{goal.get('name')}': {old} → {current}")
            return True
    print(f"❌ Goal '{goal_id}' not found")
    return False

def add_goal(data, name, target, unit="units"):
    goal_id = name.lower().replace(" ", "-")[:20]
    new_goal = {
        "id": goal_id,
        "name": name,
        "target": target,
        "current": 0,
        "unit": unit,
        "milestones": [],
        "notes": f"Created {date.today()}"
    }
    data.setdefault("goals", []).append(new_goal)
    save_goals(data)
    print(f"✅ Added goal: {name} (target: {target} {unit})")

def main():
    parser = argparse.ArgumentParser(description="Track your goals")
    parser.add_argument("--update", help="Goal ID to update")
    parser.add_argument("--current", type=float, help="New current value")
    parser.add_argument("--add", help="Add new goal (name)")
    parser.add_argument("--target", type=float, help="Target for new goal")
    parser.add_argument("--unit", default="units", help="Unit for new goal")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    data = load_goals()
    
    if args.update and args.current is not None:
        update_goal(data, args.update, args.current)
    elif args.add and args.target:
        add_goal(data, args.add, args.target, args.unit)
    else:
        check_goals(data)

if __name__ == "__main__":
    main()
