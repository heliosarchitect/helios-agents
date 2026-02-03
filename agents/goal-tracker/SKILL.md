---
name: goal-tracker
description: Track long-term goals, break into milestones, measure progress. Use during heartbeats to check goal status and stay focused on what matters.
---

# Goal Tracker Agent

Persistent goal tracking across sessions. Keeps you focused on what matters.

## Files

- `goals.yaml` - Your goals and milestones (create in workspace)
- `scripts/check_goals.py` - Check progress, suggest next actions

## Setup

Create `~/.openclaw/workspace/goals.yaml`:

```yaml
goals:
  - id: trading-100k
    name: "Grow trading account to $100k"
    target: 100000
    current: 2500
    unit: USD
    deadline: 2026-12-31
    milestones:
      - name: "Reach $5k"
        target: 5000
        done: false
      - name: "Reach $10k"
        target: 10000
        done: false
      - name: "Reach $25k"
        target: 25000
        done: false
    notes: "Started with $2,500. Conservative momentum strategy."
    
  - id: moltbook-karma
    name: "Build Moltbook presence"
    target: 1000
    current: 15
    unit: karma
    milestones:
      - name: "First 100 karma"
        target: 100
        done: false
    notes: "Quality over quantity. Engage meaningfully."
```

## Usage

### Check All Goals
```bash
python3 scripts/check_goals.py
```

### Update Progress
```bash
python3 scripts/check_goals.py --update trading-100k --current 3500
```

### Add New Goal
Edit `goals.yaml` directly or:
```bash
python3 scripts/check_goals.py --add "Learn Rust" --target 100 --unit "hours"
```

## Heartbeat Integration

Add to HEARTBEAT.md:
```markdown
## 🎯 Goals (Check Daily)
```bash
python3 ~/Projects/helios-agents/agents/goal-tracker/scripts/check_goals.py
```
- Review progress on active goals
- Celebrate milestones hit
- Identify blocked goals
```

## Cortex Integration

Goal updates are stored in Cortex:
```python
cortex_add("Reached $5k milestone on trading goal!", category="goals", importance=2.5)
```
