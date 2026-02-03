---
name: backup-manager
description: Ensure critical data (Cortex, configs, workspace) is backed up. Run during heartbeats to verify backup health.
---

# Backup Manager Agent

Automated backup and verification of critical data.

## What Gets Backed Up

- `cortex` - Memory system (STM, collections, embeddings)
- `workspace` - OpenClaw workspace files
- `openclaw_config` - OpenClaw configuration
- `moltbook_creds` - Moltbook API credentials
- `trading_bot` - Trading bot code and state

## Usage

### Check Backup Status
```bash
python3 scripts/backup.py --status
```

### Backup Everything
```bash
python3 scripts/backup.py --all
```

### Backup Specific Target
```bash
python3 scripts/backup.py --backup cortex
```

### List Existing Backups
```bash
python3 scripts/backup.py --list
```

## Backup Location

Default: `~/backups/helios/`

Format: `{target}_{YYYYMMDD_HHMMSS}.tar.gz`

## Heartbeat Integration

```markdown
## 💾 Backups (Check Daily)
```bash
python3 ~/Projects/helios-agents/agents/backup-manager/scripts/backup.py --status
```
Alert if any backup older than 7 days.
```

## Recommended Schedule

- **Daily**: Check status, alert if stale
- **Weekly**: Full backup of workspace and cortex
- **Monthly**: Full backup of everything + offsite sync
