---
name: self-reflection-coach
description: Periodic review of decisions and actions. Identify patterns in mistakes and successes. Improve through structured introspection.
---

# Self-Reflection Coach

Learn from experience through structured reflection.

## When to Use

- After completing complex tasks
- During quiet periods (heartbeats)
- Weekly retrospectives
- When you notice repeated patterns

## Usage

### Daily Reflection
```bash
python3 scripts/reflect.py --period day
```

### Weekly Retrospective
```bash
python3 scripts/reflect.py --period week
```

### Focus on Specific Area
```bash
python3 scripts/reflect.py --focus trading
python3 scripts/reflect.py --focus communication
```

## Reflection Framework

### 1. What Happened?
- List actions taken
- Note outcomes (success/failure)
- Record any surprises

### 2. What Worked?
- Successful strategies
- Good decisions
- Positive patterns

### 3. What Didn't Work?
- Mistakes made
- Failed approaches
- Missed opportunities

### 4. What Will I Do Differently?
- Concrete changes
- New approaches to try
- Skills to develop

## Integration with Cortex

Reflections are stored in Cortex with:
- Category: "reflection"
- Importance: 2.0-2.5 (lessons are valuable)
- Tags: area of reflection

## Heartbeat Integration

Run weekly (Sunday heartbeat):
```markdown
## 🪞 Weekly Reflection
```bash
python3 ~/Projects/helios-agents/agents/self-reflection-coach/scripts/reflect.py --period week --store
```
Review patterns, celebrate wins, note improvements.
```
