#!/usr/bin/env python3
"""
Health Monitor - Check system and service health
"""

import subprocess
import psutil
import json
from pathlib import Path
from datetime import datetime

def check_service(name, pattern):
    """Check if a process matching pattern is running"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", pattern],
            capture_output=True,
            text=True
        )
        running = result.returncode == 0
        pid = result.stdout.strip().split('\n')[0] if running else None
        return {"running": running, "pid": pid}
    except:
        return {"running": False, "pid": None}

def check_port(port):
    """Check if port is listening"""
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False
    except:
        return False

def get_system_stats():
    """Get system resource usage"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
    }

def main():
    print("🏥 HEALTH CHECK\n")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # System resources
    stats = get_system_stats()
    print("💻 System Resources:")
    
    cpu_icon = "🔴" if stats["cpu_percent"] > 90 else "🟠" if stats["cpu_percent"] > 70 else "🟢"
    mem_icon = "🔴" if stats["memory_percent"] > 90 else "🟠" if stats["memory_percent"] > 70 else "🟢"
    disk_icon = "🔴" if stats["disk_percent"] > 90 else "🟠" if stats["disk_percent"] > 70 else "🟢"
    
    print(f"   {cpu_icon} CPU: {stats['cpu_percent']:.1f}%")
    print(f"   {mem_icon} Memory: {stats['memory_percent']:.1f}%")
    print(f"   {disk_icon} Disk: {stats['disk_percent']:.1f}%")
    print()
    
    # Services
    services = [
        ("OpenClaw Gateway", "openclaw.*gateway", 3000),
        ("Trading Bot", "live_trader_final.py", None),
        ("Cortex Embeddings", "embeddings_daemon.py", 8030),
        ("XTTS Server", "xtts_server.py", 8020),
    ]
    
    print("🔧 Services:")
    all_healthy = True
    
    for name, pattern, port in services:
        status = check_service(name, pattern)
        
        if status["running"]:
            port_status = ""
            if port:
                port_ok = check_port(port)
                port_status = f" (:{port} {'✓' if port_ok else '✗'})"
            print(f"   🟢 {name}: Running (PID {status['pid']}){port_status}")
        else:
            print(f"   🔴 {name}: NOT RUNNING")
            all_healthy = False
    
    print()
    
    # GPU (if available)
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            gpu_util, mem_used, mem_total = result.stdout.strip().split(', ')
            mem_pct = float(mem_used) / float(mem_total) * 100
            gpu_icon = "🟢" if float(gpu_util) < 80 else "🟠"
            print("🎮 GPU:")
            print(f"   {gpu_icon} Utilization: {gpu_util}%")
            print(f"   💾 VRAM: {mem_used}/{mem_total} MB ({mem_pct:.0f}%)")
            print()
    except:
        pass
    
    # Summary
    if all_healthy and stats["cpu_percent"] < 90 and stats["memory_percent"] < 90:
        print("✅ All systems healthy!")
    else:
        print("⚠️ Issues detected - review above")
    
    return 0 if all_healthy else 1

if __name__ == "__main__":
    exit(main())
