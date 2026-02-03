#!/usr/bin/env python3
"""
Market Sentiment Analyst - Aggregate crypto market sentiment
"""

import argparse
import json
import urllib.request
from datetime import datetime

def get_fear_greed_index():
    """Get Fear & Greed Index from Alternative.me"""
    try:
        url = "https://api.alternative.me/fng/?limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Helios/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if data.get('data'):
                item = data['data'][0]
                return {
                    "value": int(item['value']),
                    "label": item['value_classification'],
                    "timestamp": item['timestamp'],
                    "source": "alternative.me"
                }
    except Exception as e:
        return {"error": str(e)}
    return None

def get_crypto_prices():
    """Get top crypto prices from CoinGecko (free API)"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        req = urllib.request.Request(url, headers={'User-Agent': 'Helios/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return {
                "BTC": {
                    "price": data.get('bitcoin', {}).get('usd', 0),
                    "change_24h": data.get('bitcoin', {}).get('usd_24h_change', 0)
                },
                "ETH": {
                    "price": data.get('ethereum', {}).get('usd', 0),
                    "change_24h": data.get('ethereum', {}).get('usd_24h_change', 0)
                },
                "SOL": {
                    "price": data.get('solana', {}).get('usd', 0),
                    "change_24h": data.get('solana', {}).get('usd_24h_change', 0)
                }
            }
    except Exception as e:
        return {"error": str(e)}

def sentiment_emoji(value):
    """Get emoji for sentiment value"""
    if value < 20:
        return "😱"  # Extreme fear
    elif value < 40:
        return "😰"  # Fear
    elif value < 60:
        return "😐"  # Neutral
    elif value < 80:
        return "😊"  # Greed
    else:
        return "🤑"  # Extreme greed

def trading_signal(sentiment_value, price_change):
    """Generate trading signal based on sentiment + momentum"""
    signals = []
    
    # Contrarian signals
    if sentiment_value < 25:
        signals.append("🟢 OPPORTUNITY: Extreme fear often marks bottoms")
    elif sentiment_value < 40 and price_change < -3:
        signals.append("🟢 Potential dip buy: Fear + price drop")
    elif sentiment_value > 75:
        signals.append("🔴 CAUTION: Extreme greed often precedes corrections")
    elif sentiment_value > 60 and price_change > 5:
        signals.append("🟠 Consider taking profits: Greed + rally")
    else:
        signals.append("⚪ Neutral: Follow momentum strategy")
    
    return signals

def main():
    parser = argparse.ArgumentParser(description="Crypto market sentiment analysis")
    parser.add_argument("--asset", default="BTC", help="Asset to focus on")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--brief", action="store_true", help="One-line output")
    
    args = parser.parse_args()
    
    # Fetch data
    fng = get_fear_greed_index()
    prices = get_crypto_prices()
    
    if args.json:
        print(json.dumps({
            "fear_greed": fng,
            "prices": prices,
            "timestamp": datetime.now().isoformat()
        }, indent=2))
        return
    
    if fng and not fng.get("error"):
        sentiment_value = fng["value"]
        sentiment_label = fng["label"]
        emoji = sentiment_emoji(sentiment_value)
        
        if args.brief:
            btc_change = prices.get("BTC", {}).get("change_24h", 0) if prices and not prices.get("error") else 0
            print(f"{emoji} Fear/Greed: {sentiment_value} ({sentiment_label}) | BTC 24h: {btc_change:+.1f}%")
            return
        
        print("📊 MARKET SENTIMENT REPORT")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # Fear & Greed
        print(f"{emoji} Fear & Greed Index: {sentiment_value}/100")
        print(f"   Classification: {sentiment_label}")
        
        # Visual bar
        bar_width = 20
        filled = int(sentiment_value / 100 * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"   [{bar}]")
        print()
        
        # Prices
        if prices and not prices.get("error"):
            print("💰 Top Crypto (24h):")
            for symbol, data in prices.items():
                change = data.get("change_24h", 0)
                price = data.get("price", 0)
                change_icon = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                print(f"   {change_icon} {symbol}: ${price:,.2f} ({change:+.1f}%)")
            print()
        
        # Trading signals
        btc_change = prices.get("BTC", {}).get("change_24h", 0) if prices else 0
        signals = trading_signal(sentiment_value, btc_change)
        
        print("📈 Trading Signals:")
        for signal in signals:
            print(f"   {signal}")
        
    else:
        print(f"❌ Could not fetch sentiment data: {fng}")

if __name__ == "__main__":
    main()
