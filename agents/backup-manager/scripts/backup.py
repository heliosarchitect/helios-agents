#!/usr/bin/env python3
"""
Backup Manager - Ensure critical data is backed up
"""

import argparse
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import tarfile
import os

# Critical paths to backup
BACKUP_TARGETS = {
    "cortex": Path.home() / ".openclaw/workspace/memory",
    "workspace": Path.home() / ".openclaw/workspace",
    "openclaw_config": Path.home() / ".config/openclaw",
    "moltbook_creds": Path.home() / ".config/moltbook",
    "trading_bot": Path.home() / "Projects/Chad2930/Chad_Profit_Bot",
}

BACKUP_DIR = Path.home() / "backups/helios"

def get_dir_size(path):
    """Get total size of directory"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

def format_size(bytes):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

def create_backup(name, source_path, backup_dir):
    """Create a backup of a directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{name}_{timestamp}.tar.gz"
    backup_path = backup_dir / backup_name
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(source_path, arcname=name)
    
    return backup_path, os.path.getsize(backup_path)

def list_backups(backup_dir):
    """List existing backups"""
    if not backup_dir.exists():
        return []
    
    backups = []
    for f in backup_dir.glob("*.tar.gz"):
        backups.append({
            "name": f.name,
            "size": os.path.getsize(f),
            "modified": datetime.fromtimestamp(f.stat().st_mtime)
        })
    
    return sorted(backups, key=lambda x: x["modified"], reverse=True)

def check_backup_health():
    """Check backup status and age"""
    backups = list_backups(BACKUP_DIR)
    
    print("📦 BACKUP STATUS\n")
    
    for name, path in BACKUP_TARGETS.items():
        if not path.exists():
            print(f"   ⚠️  {name}: Source not found ({path})")
            continue
        
        size = get_dir_size(path)
        
        # Find latest backup for this target
        target_backups = [b for b in backups if b["name"].startswith(name)]
        
        if target_backups:
            latest = target_backups[0]
            age = datetime.now() - latest["modified"]
            
            if age.days > 7:
                icon = "🔴"
                status = f"OLD ({age.days} days)"
            elif age.days > 1:
                icon = "🟠"
                status = f"{age.days} days ago"
            else:
                icon = "🟢"
                status = "Recent"
            
            print(f"   {icon} {name}: {format_size(size)} | Last backup: {status}")
        else:
            print(f"   🔴 {name}: {format_size(size)} | NO BACKUP")
    
    print()
    
    # Summary
    total_backups = len(backups)
    total_size = sum(b["size"] for b in backups)
    
    print(f"💾 Total backups: {total_backups} ({format_size(total_size)})")
    print(f"📁 Backup location: {BACKUP_DIR}")

def main():
    parser = argparse.ArgumentParser(description="Manage backups of critical data")
    parser.add_argument("--backup", help="Create backup of specific target")
    parser.add_argument("--all", action="store_true", help="Backup all targets")
    parser.add_argument("--list", action="store_true", help="List existing backups")
    parser.add_argument("--status", action="store_true", help="Check backup health")
    
    args = parser.parse_args()
    
    if args.backup:
        if args.backup not in BACKUP_TARGETS:
            print(f"Unknown target: {args.backup}")
            print(f"Available: {', '.join(BACKUP_TARGETS.keys())}")
            return
        
        path = BACKUP_TARGETS[args.backup]
        print(f"📦 Backing up {args.backup}...")
        backup_path, size = create_backup(args.backup, path, BACKUP_DIR)
        print(f"✅ Created: {backup_path.name} ({format_size(size)})")
    
    elif args.all:
        print("📦 Creating full backup...\n")
        for name, path in BACKUP_TARGETS.items():
            if path.exists():
                print(f"   Backing up {name}...")
                backup_path, size = create_backup(name, path, BACKUP_DIR)
                print(f"   ✅ {backup_path.name} ({format_size(size)})")
            else:
                print(f"   ⚠️  {name}: Source not found")
        print("\n✅ Full backup complete!")
    
    elif args.list:
        backups = list_backups(BACKUP_DIR)
        if backups:
            print("📋 EXISTING BACKUPS\n")
            for b in backups[:10]:
                print(f"   {b['modified'].strftime('%Y-%m-%d %H:%M')} | {format_size(b['size']):>10} | {b['name']}")
        else:
            print("📭 No backups found")
    
    else:
        check_backup_health()

if __name__ == "__main__":
    main()
