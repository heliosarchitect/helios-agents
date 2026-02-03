#!/usr/bin/env python3
"""
Log Analyst - Parse logs for errors and anomalies
"""

import argparse
import re
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

# Error patterns with severity levels
PATTERNS = {
    "critical": [
        (r"CRITICAL|FATAL|crash|crashed|segfault|killed", "System crash"),
        (r"authentication.*fail|auth.*error|401.*unauthorized|403.*forbidden", "Auth failure"),
        (r"out of memory|OOM|MemoryError", "Memory exhaustion"),
        (r"disk.*full|no space left", "Disk full"),
        (r"connection refused|ECONNREFUSED", "Service down"),
    ],
    "warning": [
        (r"INSUFFICIENT_FUND", "Insufficient funds"),
        (r"INVALID_LIMIT_PRICE", "Invalid price"),
        (r"rate.?limit|429|too many requests", "Rate limited"),
        (r"timeout|timed out|ETIMEDOUT", "Timeout"),
        (r"retry|retrying|attempt \d+", "Retrying operation"),
        (r"WARNING|WARN", "Warning"),
    ],
    "info": [
        (r"ERROR|Error|error", "General error"),
        (r"failed|failure|❌", "Operation failed"),
        (r"exception|Exception", "Exception thrown"),
    ],
}

def get_log_files():
    """Find relevant log files"""
    files = []
    
    # OpenClaw gateway
    gateway_log = Path("/tmp/openclaw-gateway.log")
    if gateway_log.exists():
        files.append(gateway_log)
    
    # Trading bot logs (today)
    today = datetime.now().strftime("%Y%m%d")
    trader_log = Path.home() / f"logs/trader_{today}.log"
    if trader_log.exists():
        files.append(trader_log)
    
    return files

def analyze_file(filepath, since_minutes=60, quiet=False):
    """Analyze a single log file"""
    issues = {"critical": [], "warning": [], "info": []}
    line_count = 0
    
    try:
        with open(filepath, 'r', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return {"critical": [f"Can't read {filepath}: {e}"], "warning": [], "info": []}
    
    # Only check recent lines (last N minutes worth, estimate)
    # Assume ~1 line per second average
    recent_lines = lines[-(since_minutes * 60):] if len(lines) > since_minutes * 60 else lines
    
    for line in recent_lines:
        line_count += 1
        for severity, patterns in PATTERNS.items():
            for pattern, description in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Extract timestamp if present
                    timestamp_match = re.search(r'\[(\d{2}:\d{2}:\d{2})\]', line)
                    timestamp = timestamp_match.group(1) if timestamp_match else ""
                    
                    # Truncate long lines
                    snippet = line.strip()[:100]
                    issues[severity].append({
                        "time": timestamp,
                        "type": description,
                        "snippet": snippet,
                        "file": str(filepath)
                    })
                    break  # Only match first pattern per line
    
    return issues

def print_report(all_issues, quiet=False):
    """Print analysis report"""
    critical_count = len(all_issues["critical"])
    warning_count = len(all_issues["warning"])
    info_count = len(all_issues["info"])
    
    if quiet and critical_count == 0 and warning_count == 0:
        return  # Silent if no issues
    
    print("📋 LOG ANALYSIS REPORT\n")
    
    if critical_count > 0:
        print(f"🔴 CRITICAL ({critical_count})")
        # Group by type
        by_type = Counter(i["type"] for i in all_issues["critical"])
        for issue_type, count in by_type.most_common(5):
            print(f"   • {issue_type}: {count}")
            # Show one example
            example = next(i for i in all_issues["critical"] if i["type"] == issue_type)
            print(f"     └─ {example['snippet'][:60]}...")
        print()
    
    if warning_count > 0:
        print(f"🟠 WARNING ({warning_count})")
        by_type = Counter(i["type"] for i in all_issues["warning"])
        for issue_type, count in by_type.most_common(5):
            print(f"   • {issue_type}: {count}")
        print()
    
    if not quiet and info_count > 0:
        print(f"🟡 INFO ({info_count})")
        by_type = Counter(i["type"] for i in all_issues["info"])
        for issue_type, count in by_type.most_common(3):
            print(f"   • {issue_type}: {count}")
        print()
    
    # Summary
    total = critical_count + warning_count + info_count
    if total == 0:
        print("✅ All clear! No issues detected.")
    else:
        status = "🚨 ATTENTION NEEDED" if critical_count > 0 else "⚠️ Review recommended" if warning_count > 0 else "ℹ️ Minor issues only"
        print(f"\n{status}")
        print(f"Found {critical_count} critical, {warning_count} warnings, {info_count} info")

def main():
    parser = argparse.ArgumentParser(description="Analyze logs for issues")
    parser.add_argument("--file", help="Specific log file to analyze")
    parser.add_argument("--since", type=int, default=60, help="Minutes to look back (default: 60)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output if issues found")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring mode")
    parser.add_argument("--interval", type=int, default=300, help="Watch interval in seconds")
    
    args = parser.parse_args()
    
    if args.file:
        files = [Path(args.file)]
    else:
        files = get_log_files()
    
    if not files:
        print("📭 No log files found to analyze")
        return
    
    # Aggregate issues from all files
    all_issues = {"critical": [], "warning": [], "info": []}
    
    for filepath in files:
        issues = analyze_file(filepath, args.since, args.quiet)
        for severity in all_issues:
            all_issues[severity].extend(issues[severity])
    
    print_report(all_issues, args.quiet)

if __name__ == "__main__":
    main()
