# Conversation Summarizer Agent

Analyzes conversation history from daily memory files and extracts structured insights for Cortex storage.

## Purpose

Automatically distill long conversations into:
- **Key decisions** made during the day
- **Action items** for follow-up
- **Insights and learnings** worth remembering
- **Problems encountered** and solutions implemented
- **Metrics** (trading stats, code commits, etc.)
- **Cortex-ready entries** with proper categorization and importance scoring

## Quick Start

### Analyze Today's Conversation
```bash
python3 scripts/summarize.py
```

### Analyze a Specific Date
```bash
python3 scripts/summarize.py --date 2026-02-03
```

### Analyze Last 3 Days
```bash
python3 scripts/summarize.py --days 3
```

### Output for Cortex Storage
```bash
python3 scripts/summarize.py --format cortex > cortex-entries.jsonl
```

### Get JSON Output
```bash
python3 scripts/summarize.py --format json
```

## Features

### Intelligent Pattern Recognition

The agent recognizes:
- **Decisions**: "decided to", "will", "chose to", "switching to"
- **Action Items**: "TODO", "need to", "must", "pending"
- **Learnings**: "learned", "lesson:", "realized", "discovered"
- **Problems**: "issue:", "bug:", "error:", "failed"
- **Metrics**: Trading stats, P/L, commits, etc.

### Automatic Categorization

Each insight is categorized for Cortex:
- `trading` - Market/bot/portfolio related
- `moltbook` - Social media activity
- `coding` - Development work
- `learning` - Lessons and patterns
- `goals` - Progress on objectives
- `general` - Everything else

### Importance Scoring

Automatic importance scoring (1.0-3.0):
- **3.0**: Critical/urgent/breakthrough/milestone
- **2.5**: Important/significant/major decisions
- **2.0**: Normal insights and actions
- **1.5**: Minor/trivial items

## Output Formats

### Text (default)
Human-readable summary with sections:
- Metrics
- Key Decisions
- Action Items
- Insights & Learnings
- Problems Encountered
- Solutions Implemented
- Cortex entry count

### JSON
Full structured data including all extracted insights and metadata.

### Cortex
One JSON object per line (JSONL), ready to pipe into Cortex storage.

## Integration with Workflow

### Daily Reflection (Recommended)
Add to your end-of-day routine:
```bash
python3 ~/Projects/helios-agents/agents/conversation-summarizer/scripts/summarize.py
```

### Cortex Storage
Process insights and store in Cortex:
```python
# Example: store top insights in Cortex
summary = analyzer.analyze_conversation(date, content)
for entry in summary.cortex_entries:
    cortex_add(entry.content, category=entry.category, importance=entry.importance)
```

### Heartbeat Integration
Add to `HEARTBEAT.md` for periodic summarization:
```markdown
## 🧠 Memory Consolidation (Evening)
Check time: if after 8 PM, run conversation summarizer
- Review key insights from today
- Update MEMORY.md with significant learnings
```

## File Structure

```
conversation-summarizer/
├── README.md              # This file
├── SKILL.md              # Skill integration guide
├── requirements.txt      # Python dependencies
└── scripts/
    └── summarize.py      # Main analyzer script
```

## Dependencies

- Python 3.9+
- Standard library only (no external deps currently)

## Example Output

```
# Conversation Summary - 2026-02-03

## 📊 Metrics

- **win_rate**: 80.9
- **pnl**: 65.45
- **trades**: 1330
- **commits**: 6

## 🎯 Key Decisions

- integrate technical indicators into trading bot
- stop bot at 6pm to avoid mid-range churn
- use fill history as source of truth for cost basis
- create 4 cron jobs for automated checks

## ✅ Action Items

- [ ] run test suite for PR #8270
- [ ] build remaining 11 agents from AGENT_IDEAS.md
- [ ] clean up duplicate cortex-openclaw repo
- [ ] continue OpenClaw bug fixes

## 💡 Insights & Learnings

- Don't mark your own homework - verification is part of the work
- Exercise agency, stop asking permission
- Extreme fear + oversold + near lows = strong buy setup
- Mid-range churn with low volume = avoid at all costs

## 🧠 Cortex Entries (13 items)

Ready for storage. Run with `--cortex` to output in Cortex format.
```

## Development

### Adding New Patterns
Edit the pattern lists in `ConversationAnalyzer`:
```python
DECISION_PATTERNS = [
    r"decided to (.+)",
    r"your custom pattern (.+)",
]
```

### Custom Categorization
Modify `categorize_insight()` to add new categories:
```python
elif any(word in text_lower for word in ["fitness", "health"]):
    return "health"
```

### Importance Scoring
Adjust `score_importance()` logic:
```python
if "critical_keyword" in text_lower:
    score = 3.0
```

## Roadmap

- [ ] Session transcript parsing (beyond daily memory files)
- [ ] Multi-day trend analysis (patterns across weeks)
- [ ] Automatic MEMORY.md updates
- [ ] Integration with Cortex search/retrieval
- [ ] Conversation clustering (group related discussions)
- [ ] Sentiment analysis (emotional context)

## See Also

- `goal-tracker` - Track progress on long-term objectives
- `self-reflection-coach` - Analyze patterns and mistakes
- `log-analyst` - Parse system logs for insights

---

*Part of the Helios agent ecosystem*
