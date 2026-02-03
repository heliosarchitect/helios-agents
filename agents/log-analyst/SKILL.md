---
name: log-analyst
description: Parse logs for anomalies, categorize errors, alert on issues. Use during heartbeats to catch problems early.
---

# Log Analyst Agent

Automated log analysis for error detection and anomaly alerting.

## Files

- `scripts/analyze_logs.py` - Main analysis script
- `patterns.yaml` - Error patterns to detect (customizable)

## Usage

### Quick Check
```bash
python3 scripts/analyze_logs.py
```

### Analyze Specific Log
```bash
python3 scripts/analyze_logs.py --file /path/to/log.log
```

### Watch Mode (Continuous)
```bash
python3 scripts/analyze_logs.py --watch --interval 60
```

## Default Log Sources

- `/tmp/openclaw-gateway.log` - OpenClaw gateway
- `~/logs/trader_*.log` - Trading bot logs
- `~/.openclaw/sessions/*/transcript.log` - Session transcripts

## Alert Levels

- 🔴 CRITICAL - Immediate attention (crashes, auth failures)
- 🟠 WARNING - Should investigate (rate limits, retries)
- 🟡 INFO - Noteworthy but not urgent
- ⚪ DEBUG - Verbose info (ignored by default)

## Heartbeat Integration

Add to HEARTBEAT.md:
```markdown
## 📋 Logs (Check Every Heartbeat)
```bash
python3 ~/Projects/helios-agents/agents/log-analyst/scripts/analyze_logs.py --quiet
```
Only alert if critical/warning issues found.
```
