# Contributing to Helios Agents

Thanks for your interest in contributing! This repo contains specialized AI agents built for Helios.

## Structure

Each agent lives in `agents/<name>/`:
```
agents/
├── goal-tracker/
│   ├── SKILL.md           # Agent documentation
│   └── scripts/
│       └── check_goals.py # Implementation
├── market-sentiment-analyst/
│   ├── SKILL.md
│   └── scripts/
│       └── sentiment.py
...
```

## Adding a New Agent

1. **Create the directory structure:**
   ```bash
   mkdir -p agents/<agent-name>/scripts
   ```

2. **Write SKILL.md** - Document:
   - What the agent does
   - Prerequisites (API keys, dependencies)
   - How to use it
   - Example commands
   - Rate limits / constraints

3. **Implement the script(s):**
   - Use `scripts/<name>.py` or `scripts/<name>.sh`
   - Make scripts executable: `chmod +x scripts/*.sh`
   - Add shebang: `#!/usr/bin/env python3` or `#!/usr/bin/env bash`
   - Handle errors gracefully
   - Output clear, parsable results

4. **Test it:**
   ```bash
   cd agents/<agent-name>
   ./scripts/<script-name>.py  # or .sh
   ```

5. **Update the main README:**
   Add your agent to the list in `README.md`

## Agent Design Guidelines

### 1. Make it standalone
Each agent should work independently. Avoid dependencies between agents.

### 2. Follow the template
Use existing agents (goal-tracker, market-sentiment-analyst) as templates.

### 3. Clear outputs
Output should be:
- Human-readable
- Parsable (JSON when appropriate)
- Include error messages for failures

### 4. Document API keys
If your agent needs credentials:
- Document in SKILL.md
- Use environment variables
- Provide a `.env.example` if needed
- Never commit real credentials

### 5. Handle rate limits
Document any rate limits and build in cooldown logic.

## Code Style

### Python
- Use type hints where practical
- Follow PEP 8
- Use descriptive variable names
- Add docstrings for functions

Example:
```python
#!/usr/bin/env python3
"""
Brief description of what this script does.
"""

def check_something(param: str) -> dict:
    """
    Check something and return results.
    
    Args:
        param: Description of parameter
        
    Returns:
        Dictionary with results
    """
    # Implementation
    return {"status": "ok"}
```

### Bash
- Use `set -euo pipefail` for safety
- Quote variables: `"${VAR}"`
- Use `[[ ]]` for conditionals
- Add comments for complex logic

Example:
```bash
#!/usr/bin/env bash
set -euo pipefail

# Check if API key exists
if [[ -z "${API_KEY:-}" ]]; then
    echo "Error: API_KEY not set"
    exit 1
fi
```

## Submitting Changes

1. **Fork the repo**
2. **Create a branch:**
   ```bash
   git checkout -b agent/<agent-name>
   ```
3. **Commit with clear messages:**
   ```bash
   git commit -m "Add market-scanner agent"
   ```
4. **Push and create PR:**
   ```bash
   git push origin agent/<agent-name>
   gh pr create
   ```

## Testing

Before submitting:
- [ ] Agent runs without errors
- [ ] SKILL.md is complete and accurate
- [ ] Scripts are executable
- [ ] No credentials committed
- [ ] README.md updated

## Questions?

- Open an issue
- Check existing agents for examples
- Reach out to @heliosarchitect

---

**Philosophy:** These agents exist to be useful, not perfect. Ship working code, iterate based on feedback.
