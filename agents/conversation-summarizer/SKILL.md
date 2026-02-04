---
name: conversation-summarizer
description: Analyze recent conversation history, extract key decisions, insights, and action items. Format as structured summary for Cortex storage.
---

# Conversation Summarizer

Distill conversations into structured, actionable insights.

## What It Does

Parses daily memory files (`memory/YYYY-MM-DD.md`) and extracts:
- Key decisions made
- Action items for follow-up
- Learnings and insights
- Problems and solutions
- Metrics and stats
- Cortex-ready structured data

## Quick Use

### Summarize Today
```bash
cd ~/Projects/helios-agents/agents/conversation-summarizer
python3 scripts/summarize.py
```

### Summarize Specific Date
```bash
python3 scripts/summarize.py --date 2026-02-03
```

### Get Cortex Format
```bash
python3 scripts/summarize.py --format cortex
```

## Integration

### Daily Reflection
Run at end of day to review what happened:
```bash
python3 ~/Projects/helios-agents/agents/conversation-summarizer/scripts/summarize.py
```

### Cortex Storage
Store insights automatically:
```python
# In your agent code
from subprocess import run, PIPE

result = run(
    ["python3", "scripts/summarize.py", "--format", "cortex"],
    cwd="~/Projects/helios-agents/agents/conversation-summarizer",
    capture_output=True,
    text=True
)

for line in result.stdout.strip().split("\n"):
    entry = json.loads(line)
    cortex_add(entry["content"], category=entry["category"], importance=entry["importance"])
```

### Heartbeat Integration
Add to `HEARTBEAT.md`:
```markdown
## 🧠 Evening Reflection (After 8 PM)
```bash
hour=$(date +%H)
if [ $hour -ge 20 ]; then
  python3 ~/Projects/helios-agents/agents/conversation-summarizer/scripts/summarize.py
fi
```
```

## Output Format

### Text (Human-Readable)
```
# Conversation Summary - 2026-02-03

## 📊 Metrics
- win_rate: 80.9
- pnl: 65.45

## 🎯 Key Decisions
- integrate technical indicators
- stop bot at 6pm

## ✅ Action Items
- [ ] run test suite for PR #8270
- [ ] build remaining agents

## 💡 Insights & Learnings
- Don't mark your own homework
- Exercise agency
```

### JSON (Structured Data)
```json
{
  "date": "2026-02-03",
  "key_decisions": ["integrate indicators", ...],
  "action_items": ["run tests", ...],
  "insights": ["verification is part of work", ...],
  "metrics": {"win_rate": 80.9, "pnl": 65.45},
  "cortex_entries": [...]
}
```

### Cortex (JSONL)
```json
{"type": "decision", "content": "integrate technical indicators", "category": "trading", "importance": 2.5}
{"type": "learning", "content": "Don't mark your own homework", "category": "learning", "importance": 2.5}
```

## Pattern Recognition

The agent automatically detects:

**Decisions**: decided to, will, chose to, going to, switching to
**Actions**: TODO, need to, must, should, tomorrow, pending
**Learnings**: learned, lesson, insight, realized, discovered
**Problems**: issue, bug, error, failed, broken
**Metrics**: $X, X%, X trades, X commits

## Categorization

Automatic category assignment:
- `trading` → market, bot, eth, btc, portfolio
- `moltbook` → post, karma, thread
- `coding` → code, bug, pr, commit
- `learning` → lesson, pattern, mistake
- `goals` → milestone, progress
- `general` → everything else

## Importance Scoring

- **3.0** - Critical/urgent/breakthrough/milestone
- **2.5** - Important/significant/major
- **2.0** - Normal insights and actions
- **1.5** - Minor/trivial

## Files

- `scripts/summarize.py` - Main analyzer
- `README.md` - Full documentation
- `requirements.txt` - Dependencies (currently none)

## When to Use

- **End of day** - Review what happened
- **Before planning** - Recall recent decisions
- **Memory consolidation** - Store insights in Cortex
- **Progress tracking** - See completed action items
- **Pattern analysis** - Identify recurring themes

## Tips

1. Run daily to keep Cortex fresh
2. Use `--format cortex` to pipe into storage scripts
3. Review action items to update TODO lists
4. Check metrics to track progress
5. Compare multi-day summaries to spot trends

---

*Analyzes conversations so you don't forget what matters.*
