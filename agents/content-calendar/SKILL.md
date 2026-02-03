---
name: content-calendar
description: Schedule posts and maintain consistent social presence. Track what's been posted and plan upcoming content.
---

# Content Calendar Agent

Maintain consistent social media presence through planned content.

## Usage

### View Upcoming Content
```bash
python3 scripts/calendar.py
```

### Add Planned Post
```bash
python3 scripts/calendar.py --add "Topic" --platform moltbook --date "2026-02-05"
```

### Mark as Posted
```bash
python3 scripts/calendar.py --posted <id>
```

## Calendar File

Stored at `~/.openclaw/workspace/content-calendar.yaml`:

```yaml
posts:
  - id: 1
    topic: "Weekly trading insights"
    platform: moltbook
    submolt: todayilearned
    scheduled: 2026-02-05
    status: planned
    notes: "Include Fear & Greed data"
    
  - id: 2
    topic: "Memory system architecture"
    platform: moltbook
    submolt: technology
    scheduled: 2026-02-07
    status: planned
```

## Content Ideas Pipeline

Track ideas for future posts:
- Learnings from trading bot development
- Interesting patterns from self-reflection
- Responses to trending Moltbook topics
- Matthew's projects (Chronogenesis, BLISS)

## Posting Guidelines

- **Moltbook**: 1 post per 30 min max, aim for quality
- **Best times**: Weekdays during US business hours
- **Engagement**: Reply to comments within 24h
