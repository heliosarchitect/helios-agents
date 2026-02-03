---
name: task-decomposer
description: Break complex tasks into subtasks, estimate effort, and delegate to sub-agents. Use for multi-step requests that benefit from structured decomposition.
---

# Task Decomposer Agent

Systematic decomposition of complex tasks into manageable subtasks.

## When to Use

- Multi-step requests spanning different domains
- Tasks requiring sequential dependencies
- Work that could parallelize across sub-agents
- Ambiguous requests needing clarification

## Usage

### Decompose a Task
```bash
python3 scripts/decompose.py "Build a trading dashboard with real-time prices, P&L tracking, and alerts"
```

### Output Formats
```bash
python3 scripts/decompose.py --format yaml "..."  # YAML task tree
python3 scripts/decompose.py --format json "..."  # JSON for automation
python3 scripts/decompose.py --format markdown "..."  # Markdown checklist
```

## Decomposition Strategy

1. **Identify domains** - What expertise areas does this touch?
2. **Find dependencies** - What must happen before what?
3. **Estimate effort** - How long will each part take?
4. **Identify blockers** - What could go wrong?
5. **Suggest delegation** - Which sub-agents could help?

## Integration with Sub-Agents

The decomposer can output tasks formatted for `sessions_spawn`:

```yaml
subtasks:
  - task: "Fetch real-time prices from Coinbase API"
    agent: default
    estimated_time: "5 min"
    dependencies: []
    
  - task: "Design P&L tracking schema"
    agent: default
    estimated_time: "10 min"
    dependencies: ["price_fetcher"]
```

## Complexity Thresholds

- **Simple** (<3 subtasks): Execute directly
- **Medium** (3-7 subtasks): Decompose, execute sequentially
- **Complex** (>7 subtasks): Decompose, parallelize with sub-agents
