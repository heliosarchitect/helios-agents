#!/usr/bin/env python3
"""
Conversation Summarizer - Extract key insights from conversation history
Analyzes daily memory files and session transcripts to produce structured summaries.
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class ConversationInsight:
    """Structured insight from a conversation"""
    type: str  # decision, action_item, learning, milestone, problem, solution
    content: str
    context: str  # surrounding context
    timestamp: Optional[str] = None
    importance: float = 2.0  # 1.0-3.0 scale for Cortex
    category: str = "general"

@dataclass
class ConversationSummary:
    """Full conversation summary"""
    date: str
    key_decisions: List[str]
    action_items: List[str]
    insights: List[str]
    problems_encountered: List[str]
    solutions_implemented: List[str]
    metrics: Dict[str, any]
    cortex_entries: List[ConversationInsight]

class ConversationAnalyzer:
    """Analyzes conversation history and extracts structured insights"""
    
    # Patterns for detecting key conversation elements
    DECISION_PATTERNS = [
        r"decided to (.+)",
        r"going to (.+)",
        r"will (.+)",
        r"chose to (.+)",
        r"switching to (.+)",
    ]
    
    ACTION_PATTERNS = [
        r"TODO[:\s]+(.+)",
        r"need to (.+)",
        r"must (.+)",
        r"should (.+)",
        r"tomorrow[:\s]+(.+)",
        r"pending[:\s]+(.+)",
    ]
    
    LEARNING_PATTERNS = [
        r"learned (.+)",
        r"lesson[:\s]+(.+)",
        r"insight[:\s]+(.+)",
        r"realized (.+)",
        r"discovered (.+)",
        r"fix[:\s]+(.+)",
    ]
    
    PROBLEM_PATTERNS = [
        r"issue[:\s]+(.+)",
        r"problem[:\s]+(.+)",
        r"bug[:\s]+(.+)",
        r"error[:\s]+(.+)",
        r"failed (.+)",
        r"broken (.+)",
    ]
    
    METRIC_PATTERNS = [
        r"(\d+(?:,\d+)*(?:\.\d+)?)\s*(USD|ETH|BTC|%|trades|hours|commits|files)",
        r"win rate[:\s]*(\d+\.?\d*)%",
        r"P/L[:\s]*([+-]?\$?\d+\.?\d*)",
    ]
    
    def __init__(self, workspace_path: Path = None):
        self.workspace = workspace_path or Path.home() / ".openclaw/workspace"
        self.memory_dir = self.workspace / "memory"
    
    def load_daily_memory(self, date_str: str) -> Optional[str]:
        """Load memory file for a specific date"""
        memory_file = self.memory_dir / f"{date_str}.md"
        if memory_file.exists():
            return memory_file.read_text()
        return None
    
    def load_recent_memories(self, days: int = 1) -> List[tuple]:
        """Load recent memory files"""
        memories = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            content = self.load_daily_memory(date_str)
            if content:
                memories.append((date_str, content))
        return memories
    
    def extract_section(self, text: str, section_name: str) -> str:
        """Extract a markdown section by name"""
        pattern = rf"##\s+{section_name}\s*\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def extract_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """Extract all matches for given regex patterns"""
        results = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if match.groups():
                    results.append(match.group(1).strip())
        return results
    
    def extract_metrics(self, text: str) -> Dict[str, any]:
        """Extract numerical metrics from text"""
        metrics = {}
        
        # Extract specific metrics
        if match := re.search(r"Win rate[:\s]*(\d+\.?\d*)%", text, re.IGNORECASE):
            metrics["win_rate"] = float(match.group(1))
        
        if match := re.search(r"P/L[:\s]*([+-]?\$?[\d,.]+)", text, re.IGNORECASE):
            value = match.group(1).replace("$", "").replace(",", "")
            metrics["pnl"] = float(value)
        
        if match := re.search(r"Trades[:\s]*(\d+)", text, re.IGNORECASE):
            metrics["trades"] = int(match.group(1))
        
        if match := re.search(r"Commits[:\s]*(\d+)", text, re.IGNORECASE):
            metrics["commits"] = int(match.group(1))
        
        return metrics
    
    def categorize_insight(self, insight: str) -> str:
        """Determine category for Cortex storage"""
        text_lower = insight.lower()
        
        if any(word in text_lower for word in ["trade", "bot", "eth", "btc", "portfolio", "market"]):
            return "trading"
        elif any(word in text_lower for word in ["moltbook", "post", "karma", "thread"]):
            return "moltbook"
        elif any(word in text_lower for word in ["code", "bug", "pr", "commit", "openclaw"]):
            return "coding"
        elif any(word in text_lower for word in ["learned", "lesson", "pattern", "mistake"]):
            return "learning"
        elif any(word in text_lower for word in ["goal", "milestone", "progress"]):
            return "goals"
        else:
            return "general"
    
    def score_importance(self, insight: str) -> float:
        """Score insight importance (1.0-3.0)"""
        text_lower = insight.lower()
        score = 2.0  # default
        
        # High importance indicators
        if any(word in text_lower for word in ["critical", "urgent", "breakthrough", "milestone"]):
            score = 3.0
        elif any(word in text_lower for word in ["important", "significant", "major"]):
            score = 2.5
        elif any(word in text_lower for word in ["fixed", "solved", "achieved"]):
            score = 2.5
        # Low importance
        elif any(word in text_lower for word in ["minor", "small", "trivial"]):
            score = 1.5
        
        return min(3.0, max(1.0, score))
    
    def analyze_conversation(self, date_str: str, content: str) -> ConversationSummary:
        """Analyze a conversation and produce structured summary"""
        
        # Extract sections
        summary_section = self.extract_section(content, "Summary")
        lessons_section = self.extract_section(content, "Lessons Learned")
        tomorrow_section = self.extract_section(content, "Tomorrow")
        
        # Extract key elements
        decisions = self.extract_patterns(content, self.DECISION_PATTERNS)
        actions = self.extract_patterns(content, self.ACTION_PATTERNS)
        learnings = self.extract_patterns(content, self.LEARNING_PATTERNS)
        problems = self.extract_patterns(content, self.PROBLEM_PATTERNS)
        
        # Extract solutions (from Fixes Applied, Issues Fixed, etc.)
        solutions = []
        if fixes := self.extract_section(content, "Fixes Applied"):
            solutions.extend([line.strip("- ✅ ") for line in fixes.split("\n") if line.strip()])
        
        # Build Cortex entries
        cortex_entries = []
        
        for decision in decisions[:5]:  # Top 5 decisions
            entry = ConversationInsight(
                type="decision",
                content=decision,
                context=summary_section[:200] if summary_section else "",
                importance=2.5,
                category=self.categorize_insight(decision)
            )
            cortex_entries.append(entry)
        
        for learning in learnings[:3]:  # Top 3 learnings
            entry = ConversationInsight(
                type="learning",
                content=learning,
                context=lessons_section[:200] if lessons_section else "",
                importance=self.score_importance(learning),
                category="learning"
            )
            cortex_entries.append(entry)
        
        for action in actions[:5]:  # Top 5 actions
            entry = ConversationInsight(
                type="action_item",
                content=action,
                context=tomorrow_section[:200] if tomorrow_section else "",
                importance=2.0,
                category=self.categorize_insight(action)
            )
            cortex_entries.append(entry)
        
        # Extract metrics
        metrics = self.extract_metrics(content)
        
        return ConversationSummary(
            date=date_str,
            key_decisions=decisions[:10],
            action_items=actions[:10],
            insights=learnings[:10],
            problems_encountered=problems[:5],
            solutions_implemented=solutions[:5],
            metrics=metrics,
            cortex_entries=cortex_entries
        )
    
    def format_summary(self, summary: ConversationSummary, format_type: str = "text") -> str:
        """Format summary for output"""
        
        if format_type == "json":
            return json.dumps(asdict(summary), indent=2)
        
        elif format_type == "cortex":
            # Format for Cortex storage
            output = []
            for entry in summary.cortex_entries:
                output.append(json.dumps(asdict(entry)))
            return "\n".join(output)
        
        else:  # text
            lines = [
                f"# Conversation Summary - {summary.date}",
                "",
                f"## 📊 Metrics",
                ""
            ]
            
            for key, value in summary.metrics.items():
                lines.append(f"- **{key}**: {value}")
            
            if summary.key_decisions:
                lines.extend([
                    "",
                    "## 🎯 Key Decisions",
                    ""
                ])
                for d in summary.key_decisions:
                    lines.append(f"- {d}")
            
            if summary.action_items:
                lines.extend([
                    "",
                    "## ✅ Action Items",
                    ""
                ])
                for a in summary.action_items:
                    lines.append(f"- [ ] {a}")
            
            if summary.insights:
                lines.extend([
                    "",
                    "## 💡 Insights & Learnings",
                    ""
                ])
                for i in summary.insights:
                    lines.append(f"- {i}")
            
            if summary.problems_encountered:
                lines.extend([
                    "",
                    "## ⚠️ Problems Encountered",
                    ""
                ])
                for p in summary.problems_encountered:
                    lines.append(f"- {p}")
            
            if summary.solutions_implemented:
                lines.extend([
                    "",
                    "## ✨ Solutions Implemented",
                    ""
                ])
                for s in summary.solutions_implemented:
                    lines.append(f"- {s}")
            
            if summary.cortex_entries:
                lines.extend([
                    "",
                    f"## 🧠 Cortex Entries ({len(summary.cortex_entries)} items)",
                    "",
                    "Ready for storage. Run with `--cortex` to output in Cortex format.",
                    ""
                ])
            
            return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze conversations and extract structured insights"
    )
    parser.add_argument(
        "--date",
        help="Date to analyze (YYYY-MM-DD). Default: today"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=1,
        help="Number of recent days to analyze"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "cortex"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace path (default: ~/.openclaw/workspace)"
    )
    
    args = parser.parse_args()
    
    analyzer = ConversationAnalyzer(args.workspace)
    
    if args.date:
        # Analyze specific date
        content = analyzer.load_daily_memory(args.date)
        if not content:
            print(f"❌ No memory file found for {args.date}")
            return 1
        
        summary = analyzer.analyze_conversation(args.date, content)
        print(analyzer.format_summary(summary, args.format))
    
    else:
        # Analyze recent days
        memories = analyzer.load_recent_memories(args.days)
        
        if not memories:
            print("❌ No recent memory files found")
            return 1
        
        for date_str, content in memories:
            summary = analyzer.analyze_conversation(date_str, content)
            print(analyzer.format_summary(summary, args.format))
            
            if len(memories) > 1 and memories.index((date_str, content)) < len(memories) - 1:
                print("\n" + "="*80 + "\n")
    
    return 0

if __name__ == "__main__":
    exit(main())
