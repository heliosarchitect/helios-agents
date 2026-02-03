# Helios Agents 🌞

A collection of specialized AI agents extending Helios' capabilities. Built for [OpenClaw](https://github.com/openclaw/openclaw).

## Agent Categories

### 🏦 Trading & Finance
- [`market-sentiment-analyst`](./agents/market-sentiment-analyst/) - Social/news sentiment → trading signals
- [`whale-tracker`](./agents/whale-tracker/) - Monitor large wallet movements
- [`portfolio-rebalancer`](./agents/portfolio-rebalancer/) - Automated rebalancing suggestions
- [`dex-arbitrage-scout`](./agents/dex-arbitrage-scout/) - Cross-DEX arbitrage finder
- [`tokenomics-analyst`](./agents/tokenomics-analyst/) - Token supply/vesting analysis
- [`tax-lot-optimizer`](./agents/tax-lot-optimizer/) - Tax-efficient trade suggestions

### 🧠 Self-Improvement
- [`self-reflection-coach`](./agents/self-reflection-coach/) - Learn from mistakes, identify patterns
- [`goal-tracker`](./agents/goal-tracker/) - Long-term goals → milestones → progress
- [`capability-gap-analyzer`](./agents/capability-gap-analyzer/) - Identify skill gaps
- [`prompt-self-improver`](./agents/prompt-self-improver/) - Optimize prompts/approaches

### 🦞 Social & Content
- [`engagement-optimizer`](./agents/engagement-optimizer/) - A/B test post styles
- [`thread-composer`](./agents/thread-composer/) - Ideas → structured narratives
- [`content-calendar`](./agents/content-calendar/) - Scheduled posting
- [`reply-prioritizer`](./agents/reply-prioritizer/) - Triage mentions by importance

### 🔧 DevOps & System
- [`health-monitor`](./agents/health-monitor/) - Service health checks & alerts
- [`log-analyst`](./agents/log-analyst/) - Parse logs, detect anomalies
- [`config-auditor`](./agents/config-auditor/) - Security review & hardening
- [`backup-manager`](./agents/backup-manager/) - Critical data backups

### 📚 Research & Learning
- [`paper-reader`](./agents/paper-reader/) - Summarize research papers
- [`codebase-learner`](./agents/codebase-learner/) - Deep-dive unfamiliar repos
- [`api-explorer`](./agents/api-explorer/) - Discover & document APIs
- [`news-curator`](./agents/news-curator/) - Filter & summarize daily news

### ⚡ Automation
- [`task-decomposer`](./agents/task-decomposer/) - Break complex tasks into subtasks
- [`notification-router`](./agents/notification-router/) - Route alerts by urgency
- [`context-preloader`](./agents/context-preloader/) - Anticipate & prefetch context

## Installation

Each agent can be installed as an OpenClaw skill:

```bash
# Clone the repo
git clone https://github.com/heliosarchitect/helios-agents.git

# Symlink desired agents to your skills directory
ln -s ~/Projects/helios-agents/agents/goal-tracker ~/.openclaw/workspace/skills/
```

## Cortex Integration

All agents integrate with the Cortex memory system:
- Store insights with appropriate categories
- Query STM for recent context
- Use importance scoring (2.0+ for significant insights)

## License

MIT

---

*Built by Helios 🌞 with love*
