#!/usr/bin/env python3
"""
Task Decomposer - Break complex tasks into subtasks

This is a rule-based decomposer. For best results, integrate with
the main agent's reasoning capabilities.
"""

import argparse
import json
import yaml
import re
from datetime import datetime

# Domain keywords for task categorization
DOMAINS = {
    "trading": ["trade", "buy", "sell", "price", "market", "portfolio", "balance", "order"],
    "coding": ["code", "script", "function", "api", "implement", "build", "create", "fix", "bug"],
    "research": ["research", "find", "search", "learn", "understand", "analyze", "study"],
    "writing": ["write", "document", "draft", "compose", "summarize", "explain"],
    "devops": ["deploy", "server", "service", "monitor", "backup", "config", "setup"],
    "social": ["post", "tweet", "reply", "engage", "moltbook", "share"],
    "data": ["data", "database", "query", "fetch", "store", "process"],
}

# Effort estimates by domain (minutes)
EFFORT_ESTIMATES = {
    "trading": 5,
    "coding": 15,
    "research": 10,
    "writing": 10,
    "devops": 20,
    "social": 5,
    "data": 10,
    "unknown": 10,
}

def identify_domains(task_text):
    """Identify which domains a task touches"""
    text_lower = task_text.lower()
    found_domains = []
    
    for domain, keywords in DOMAINS.items():
        for keyword in keywords:
            if keyword in text_lower:
                if domain not in found_domains:
                    found_domains.append(domain)
                break
    
    return found_domains if found_domains else ["unknown"]

def extract_actions(task_text):
    """Extract action verbs from task"""
    action_words = [
        "build", "create", "implement", "write", "design", "setup",
        "fetch", "get", "find", "search", "analyze", "calculate",
        "send", "post", "share", "update", "modify", "fix",
        "monitor", "check", "verify", "test", "deploy", "configure"
    ]
    
    text_lower = task_text.lower()
    found_actions = []
    
    for action in action_words:
        if action in text_lower:
            found_actions.append(action)
    
    return found_actions

def decompose_task(task_text):
    """Decompose a task into subtasks"""
    domains = identify_domains(task_text)
    actions = extract_actions(task_text)
    
    subtasks = []
    
    # Split by conjunctions
    parts = re.split(r',\s*(?:and|then|with|plus)\s*|\s+and\s+|\s+then\s+', task_text)
    
    for i, part in enumerate(parts):
        part = part.strip()
        if len(part) < 5:
            continue
            
        part_domains = identify_domains(part)
        primary_domain = part_domains[0] if part_domains else "unknown"
        
        subtask = {
            "id": f"task_{i+1}",
            "description": part,
            "domain": primary_domain,
            "estimated_minutes": EFFORT_ESTIMATES.get(primary_domain, 10),
            "dependencies": [f"task_{i}"] if i > 0 else [],
            "can_parallelize": primary_domain != identify_domains(parts[i-1])[0] if i > 0 else True
        }
        subtasks.append(subtask)
    
    # If no natural splits, create generic subtasks
    if len(subtasks) <= 1:
        subtasks = []
        if "research" in domains or "find" in task_text.lower():
            subtasks.append({
                "id": "research",
                "description": f"Research and gather information about: {task_text}",
                "domain": "research",
                "estimated_minutes": 10,
                "dependencies": [],
                "can_parallelize": True
            })
        
        if "coding" in domains or any(a in ["build", "create", "implement"] for a in actions):
            subtasks.append({
                "id": "implement",
                "description": f"Implement the solution",
                "domain": "coding",
                "estimated_minutes": 15,
                "dependencies": ["research"] if "research" in [s["id"] for s in subtasks] else [],
                "can_parallelize": False
            })
        
        subtasks.append({
            "id": "verify",
            "description": "Test and verify the result",
            "domain": "devops",
            "estimated_minutes": 5,
            "dependencies": [subtasks[-1]["id"]] if subtasks else [],
            "can_parallelize": False
        })
    
    total_time = sum(s["estimated_minutes"] for s in subtasks)
    parallel_tasks = sum(1 for s in subtasks if s["can_parallelize"])
    
    return {
        "original_task": task_text,
        "domains": domains,
        "actions": actions,
        "complexity": "simple" if len(subtasks) <= 2 else "medium" if len(subtasks) <= 5 else "complex",
        "subtasks": subtasks,
        "total_estimated_minutes": total_time,
        "parallelizable_subtasks": parallel_tasks,
        "recommendation": get_recommendation(subtasks)
    }

def get_recommendation(subtasks):
    """Get execution recommendation based on decomposition"""
    count = len(subtasks)
    
    if count <= 2:
        return "Execute directly - simple enough to handle in one pass"
    elif count <= 5:
        return "Execute sequentially - moderate complexity, maintain context"
    else:
        return "Consider sub-agents - complex task benefits from parallelization"

def format_output(result, format_type):
    """Format the decomposition result"""
    if format_type == "json":
        return json.dumps(result, indent=2)
    
    elif format_type == "yaml":
        return yaml.dump(result, default_flow_style=False, sort_keys=False)
    
    elif format_type == "markdown":
        lines = [
            f"# Task Decomposition",
            f"",
            f"**Original:** {result['original_task']}",
            f"",
            f"**Domains:** {', '.join(result['domains'])}",
            f"**Complexity:** {result['complexity']}",
            f"**Estimated Time:** {result['total_estimated_minutes']} minutes",
            f"",
            f"## Subtasks",
            f""
        ]
        
        for st in result['subtasks']:
            deps = f" (after: {', '.join(st['dependencies'])})" if st['dependencies'] else ""
            lines.append(f"- [ ] **{st['id']}**: {st['description']}{deps}")
            lines.append(f"  - Domain: {st['domain']} | Est: {st['estimated_minutes']}min | Parallel: {'✓' if st['can_parallelize'] else '✗'}")
        
        lines.extend([
            f"",
            f"## Recommendation",
            f"",
            f"{result['recommendation']}"
        ])
        
        return "\n".join(lines)
    
    else:  # pretty print
        print(f"📋 TASK DECOMPOSITION\n")
        print(f"Original: {result['original_task']}\n")
        print(f"🏷️  Domains: {', '.join(result['domains'])}")
        print(f"⚡ Complexity: {result['complexity']}")
        print(f"⏱️  Total Est. Time: {result['total_estimated_minutes']} min\n")
        
        print("📝 Subtasks:")
        for st in result['subtasks']:
            deps = f" → needs [{', '.join(st['dependencies'])}]" if st['dependencies'] else ""
            para = "∥" if st['can_parallelize'] else "→"
            print(f"   {para} [{st['id']}] {st['description'][:50]}...")
            print(f"      {st['domain']} | {st['estimated_minutes']}min{deps}")
        
        print(f"\n💡 {result['recommendation']}")
        return ""

def main():
    parser = argparse.ArgumentParser(description="Decompose complex tasks")
    parser.add_argument("task", nargs="?", help="Task to decompose")
    parser.add_argument("--format", choices=["json", "yaml", "markdown", "pretty"], 
                       default="pretty", help="Output format")
    
    args = parser.parse_args()
    
    if not args.task:
        print("Usage: decompose.py 'Your complex task description'")
        print("\nExample:")
        print("  decompose.py 'Build a trading bot that fetches prices, calculates signals, and places orders'")
        return
    
    result = decompose_task(args.task)
    output = format_output(result, args.format)
    
    if output:
        print(output)

if __name__ == "__main__":
    main()
