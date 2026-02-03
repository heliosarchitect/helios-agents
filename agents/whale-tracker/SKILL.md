---
name: whale-tracker
description: Monitor large wallet movements and exchange flows. Large transactions often precede price action.
---

# Whale Tracker Agent

Track large crypto wallet movements for trading intelligence.

## Data Sources

1. **Whale Alert API** - Large transaction notifications
2. **Etherscan** - Ethereum whale wallets
3. **Exchange Flows** - Inflows/outflows to major exchanges

## Usage

### Check Recent Whale Activity
```bash
python3 scripts/whales.py
```

### Specific Chain
```bash
python3 scripts/whales.py --chain ethereum
python3 scripts/whales.py --chain bitcoin
```

### Alert Threshold
```bash
python3 scripts/whales.py --min-usd 10000000  # Only $10M+ transactions
```

## Signal Interpretation

| Flow Direction | Implication |
|----------------|-------------|
| Exchange Inflow | Potential sell pressure |
| Exchange Outflow | Accumulation (bullish) |
| Wallet-to-Wallet | Neutral (transfers) |
| From Cold Storage | Large holder active |

## Alert Levels

- 🐋 $100M+ = Major whale movement
- 🐬 $50M+ = Significant transaction
- 🐟 $10M+ = Notable activity
