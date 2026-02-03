#!/usr/bin/env python3
"""
Task Decomposer - Break complex tasks into subtasks using LLM reasoning

Uses Claude via Anthropic API for intelligent decomposition.
Falls back to rule-based if no API key available.
"""

import argparse
import json
import os
import re
from datetime import datetime

# Try to import LLM libraries
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

DECOMPOSITION_PROMPT = """You are a task decomposition expert. Break down the following task into concrete, actionable subtasks.

TASK: {task}

Respond with a JSON object containing:
{{
  "subtasks": [
    {{
      "id": "unique_id",
      "description": "Clear, actionable description",
      "domain": "coding|research|writing|trading|devops|social|data|unknown",
      "estimated_minutes": <number>,
      "dependencies": ["id of tasks this depends on"],
      "can_parallelize": true/false,
      "tools_needed": ["optional list of tools/apis needed"]
    }}
  ],
  "complexity": "simple|medium|complex",
  "total_estimated_minutes": <number>,
  "critical_path": ["ids of tasks on critical path"],
  "risks": ["potential blockers or challenges"],
  "recommendation": "brief strategy recommendation"
}}

Guidelines:
- Break into 3-8 subtasks for most tasks
- Be specific about what each subtask produces
- Identify true dependencies (what MUST happen before what)
- Mark tasks that can run in parallel
- Estimate realistically (include buffer for unknowns)
- Identify the critical path (longest chain of dependencies)

Respond ONLY with valid JSON, no other text."""

def smart_decompose(task_text, api_key=None):
    """Use Claude to intelligently decompose a task"""
    if not HAS_ANTHROPIC:
        return None, "anthropic package not installed"
    
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None, "No API key available"
    
    try:
        client = anthropic.Anthropic(api_key=key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": DECOMPOSITION_PROMPT.format(task=task_text)}
            ]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON from response
        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
            result["original_task"] = task_text
            result["method"] = "llm"
            return result, None
        else:
            return None, "Could not parse JSON from response"
            
    except Exception as e:
        return None, str(e)

def openai_decompose(task_text, api_key=None):
    """Use OpenAI GPT-4 as fallback for decomposition"""
    if not HAS_OPENAI:
        return None, "openai package not installed"
    
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        return None, "No OpenAI API key available"
    
    try:
        client = openai.OpenAI(api_key=key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": DECOMPOSITION_PROMPT.format(task=task_text)}
            ]
        )
        
        response_text = response.choices[0].message.content
        
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
            result["original_task"] = task_text
            result["method"] = "openai"
            return result, None
        else:
            return None, "Could not parse JSON from response"
            
    except Exception as e:
        return None, str(e)

def rule_based_decompose(task_text):
    """Fallback rule-based decomposition"""
    # Domain keywords
    domains = {
        "trading": ["trade", "buy", "sell", "price", "market", "portfolio"],
        "coding": ["code", "script", "function", "api", "implement", "build"],
        "research": ["research", "find", "search", "learn", "analyze"],
        "writing": ["write", "document", "draft", "compose"],
        "devops": ["deploy", "server", "monitor", "backup", "config"],
        "data": ["data", "database", "query", "fetch", "store"],
    }
    
    def get_domain(text):
        text_lower = text.lower()
        for domain, keywords in domains.items():
            if any(kw in text_lower for kw in keywords):
                return domain
        return "unknown"
    
    # Split on conjunctions
    parts = re.split(r',\s*(?:and|then|plus)\s*|\s+and\s+|\s+then\s+', task_text)
    parts = [p.strip() for p in parts if len(p.strip()) > 5]
    
    subtasks = []
    for i, part in enumerate(parts):
        subtasks.append({
            "id": f"task_{i+1}",
            "description": part,
            "domain": get_domain(part),
            "estimated_minutes": 15,
            "dependencies": [f"task_{i}"] if i > 0 else [],
            "can_parallelize": i == 0
        })
    
    if len(subtasks) <= 1:
        subtasks = [
            {"id": "plan", "description": f"Plan approach for: {task_text}", "domain": "research", "estimated_minutes": 10, "dependencies": [], "can_parallelize": True},
            {"id": "execute", "description": "Execute the plan", "domain": get_domain(task_text), "estimated_minutes": 30, "dependencies": ["plan"], "can_parallelize": False},
            {"id": "verify", "description": "Test and verify results", "domain": "devops", "estimated_minutes": 10, "dependencies": ["execute"], "can_parallelize": False},
        ]
    
    return {
        "original_task": task_text,
        "subtasks": subtasks,
        "complexity": "simple" if len(subtasks) <= 3 else "medium" if len(subtasks) <= 6 else "complex",
        "total_estimated_minutes": sum(s["estimated_minutes"] for s in subtasks),
        "recommendation": "Rule-based decomposition - consider using --smart for better results",
        "method": "rule-based"
    }

def format_output(result, format_type="pretty"):
    """Format the decomposition result"""
    if format_type == "json":
        return json.dumps(result, indent=2)
    
    # Pretty print
    lines = [
        f"📋 TASK DECOMPOSITION",
        f"",
        f"📝 {result['original_task']}",
        f"",
        f"⚡ Complexity: {result.get('complexity', 'unknown')}",
        f"⏱️  Total Time: {result.get('total_estimated_minutes', '?')} min",
        f"🔧 Method: {result.get('method', 'unknown')}",
        f"",
        f"📝 SUBTASKS:",
    ]
    
    for st in result.get("subtasks", []):
        deps = st.get("dependencies", [])
        dep_str = f" → after [{', '.join(deps)}]" if deps else ""
        para = "∥" if st.get("can_parallelize") else "→"
        
        lines.append(f"")
        lines.append(f"   {para} [{st['id']}] {st['description']}")
        lines.append(f"      {st.get('domain', '?')} | {st.get('estimated_minutes', '?')}min{dep_str}")
        
        if st.get("tools_needed"):
            lines.append(f"      🔧 Tools: {', '.join(st['tools_needed'])}")
    
    # Critical path
    if result.get("critical_path"):
        lines.append(f"")
        lines.append(f"🔥 Critical Path: {' → '.join(result['critical_path'])}")
    
    # Risks
    if result.get("risks"):
        lines.append(f"")
        lines.append(f"⚠️  Risks:")
        for risk in result["risks"]:
            lines.append(f"   • {risk}")
    
    # Recommendation
    if result.get("recommendation"):
        lines.append(f"")
        lines.append(f"💡 {result['recommendation']}")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Decompose complex tasks into subtasks")
    parser.add_argument("task", nargs="?", help="Task to decompose")
    parser.add_argument("--smart", action="store_true", help="Use LLM for intelligent decomposition")
    parser.add_argument("--format", choices=["json", "pretty"], default="pretty")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY)")
    
    args = parser.parse_args()
    
    if not args.task:
        print("Usage: decompose.py [--smart] 'Your complex task'")
        print("")
        print("Examples:")
        print("  decompose.py 'Build a trading bot with signals and alerts'")
        print("  decompose.py --smart 'Write a book, create marketing, launch on Amazon'")
        return
    
    if args.smart:
        # Try Anthropic first
        result, error = smart_decompose(args.task, args.api_key)
        if error:
            print(f"⚠️  Anthropic failed: {error}")
            # Fallback to OpenAI
            print("Trying OpenAI...")
            result, error2 = openai_decompose(args.task)
            if error2:
                print(f"⚠️  OpenAI failed: {error2}")
                print("Falling back to rule-based...")
                result = rule_based_decompose(args.task)
    else:
        result = rule_based_decompose(args.task)
    
    print(format_output(result, args.format))

if __name__ == "__main__":
    main()
