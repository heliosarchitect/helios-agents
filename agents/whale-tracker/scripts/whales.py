#!/usr/bin/env python3
"""
Whale Tracker - Monitor large crypto transactions
Uses Blockchain.com and public APIs for free whale tracking
"""

import argparse
import json
import urllib.request
from datetime import datetime

def get_blockchain_stats():
    """Get Bitcoin blockchain stats from Blockchain.com"""
    try:
        url = "https://api.blockchain.info/stats"
        req = urllib.request.Request(url, headers={'User-Agent': 'Helios/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return {
                "market_cap": data.get("market_price_usd", 0) * 21000000,
                "btc_price": data.get("market_price_usd", 0),
                "hash_rate": data.get("hash_rate", 0) / 1e18,  # EH/s
                "difficulty": data.get("difficulty", 0),
                "n_tx_24h": data.get("n_tx", 0),
                "total_btc_sent_24h": data.get("total_btc_sent", 0) / 1e8,
            }
    except Exception as e:
        return {"error": str(e)}

def get_recent_large_txs():
    """Get recent large Bitcoin transactions"""
    try:
        # Blockchain.com unconfirmed transactions (sample for whales)
        url = "https://blockchain.info/unconfirmed-transactions?format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Helios/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            
            large_txs = []
            for tx in data.get('txs', [])[:100]:  # Check first 100
                total_output = sum(o.get('value', 0) for o in tx.get('out', [])) / 1e8
                if total_output >= 100:  # 100+ BTC
                    large_txs.append({
                        "hash": tx.get('hash', '')[:16] + "...",
                        "btc": total_output,
                        "outputs": len(tx.get('out', [])),
                        "time": datetime.fromtimestamp(tx.get('time', 0)).strftime('%H:%M:%S')
                    })
            
            return large_txs
    except Exception as e:
        return []

def get_exchange_flows_estimate(btc_price):
    """Estimate exchange flows from known exchange addresses (simplified)"""
    # Note: Real implementation would track known exchange addresses
    # This is a placeholder that returns market context
    return {
        "note": "Full exchange flow tracking requires paid APIs or direct blockchain indexing",
        "suggestion": "Consider: Glassnode, CryptoQuant, or Nansen for detailed flow data"
    }

def format_btc_amount(btc, price):
    """Format BTC amount with USD value"""
    usd = btc * price
    if usd >= 1e9:
        return f"{btc:,.0f} BTC (${usd/1e9:.1f}B)"
    elif usd >= 1e6:
        return f"{btc:,.0f} BTC (${usd/1e6:.1f}M)"
    else:
        return f"{btc:,.2f} BTC (${usd:,.0f})"

def main():
    parser = argparse.ArgumentParser(description="Track crypto whale activity")
    parser.add_argument("--chain", default="bitcoin", help="Blockchain to track")
    parser.add_argument("--min-btc", type=float, default=100, help="Minimum BTC for alerts")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    print("🐋 WHALE TRACKER\n")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Get blockchain stats
    stats = get_blockchain_stats()
    
    if stats and not stats.get("error"):
        btc_price = stats["btc_price"]
        
        print("📊 Bitcoin Network Stats:")
        print(f"   💰 BTC Price: ${btc_price:,.0f}")
        print(f"   ⛏️  Hash Rate: {stats['hash_rate']:.1f} EH/s")
        print(f"   📦 24h Transactions: {stats['n_tx_24h']:,}")
        print(f"   💸 24h BTC Moved: {format_btc_amount(stats['total_btc_sent_24h'], btc_price)}")
        print()
        
        # Large transactions
        large_txs = get_recent_large_txs()
        
        if large_txs:
            print(f"🐋 Recent Large Transactions (>{args.min_btc} BTC):")
            for tx in large_txs[:5]:
                size_emoji = "🐋" if tx['btc'] >= 1000 else "🐬" if tx['btc'] >= 500 else "🐟"
                print(f"   {size_emoji} {tx['time']} - {format_btc_amount(tx['btc'], btc_price)}")
                print(f"      {tx['hash']} ({tx['outputs']} outputs)")
            print()
        else:
            print("   No transactions above threshold in recent mempool\n")
        
        # Market interpretation
        print("📈 Market Context:")
        
        # Simple sentiment based on volume
        btc_moved_usd = stats['total_btc_sent_24h'] * btc_price
        if btc_moved_usd > 50e9:  # >$50B
            print("   🔥 HIGH activity - significant movement")
        elif btc_moved_usd > 20e9:  # >$20B
            print("   📊 NORMAL activity - typical volume")
        else:
            print("   😴 LOW activity - quiet market")
        
        # Note about paid services
        flows = get_exchange_flows_estimate(btc_price)
        print(f"\n💡 {flows['note']}")
        
    else:
        print(f"❌ Error fetching data: {stats.get('error', 'Unknown')}")

if __name__ == "__main__":
    main()
