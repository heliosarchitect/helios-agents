---
name: market-sentiment-analyst
description: Scrape social media and news for crypto sentiment, correlate with price action. Provides trading signals based on market mood.
---

# Market Sentiment Analyst

Real-time sentiment analysis for crypto trading decisions.

## Data Sources

1. **Fear & Greed Index** - Alternative.me API (free)
2. **Reddit** - r/cryptocurrency, r/bitcoin sentiment
3. **Crypto News** - Headlines from major outlets
4. **On-chain metrics** - (future: whale alerts, exchange flows)

## Usage

### Quick Sentiment Check
```bash
python3 scripts/sentiment.py
```

### Specific Asset
```bash
python3 scripts/sentiment.py --asset ETH
```

### Output Formats
```bash
python3 scripts/sentiment.py --json  # For integration
python3 scripts/sentiment.py --brief  # One-liner
```

## Signal Interpretation

| Sentiment | Score | Trading Implication |
|-----------|-------|---------------------|
| Extreme Fear | 0-25 | Potential buy opportunity (contrarian) |
| Fear | 25-45 | Cautious accumulation |
| Neutral | 45-55 | Follow momentum |
| Greed | 55-75 | Take profits, reduce size |
| Extreme Greed | 75-100 | High risk, expect correction |

## Integration with Trading Bot

The sentiment score can adjust position sizing:
- Fear (<40): Increase position size (buying the dip)
- Neutral (40-60): Standard position size
- Greed (>60): Reduce position size (de-risk)

## Heartbeat Integration

```markdown
## 📊 Market Sentiment (Every 2-4 Hours)
```bash
python3 ~/Projects/helios-agents/agents/market-sentiment-analyst/scripts/sentiment.py --brief
```
Alert if extreme fear (<20) or extreme greed (>80).
```
