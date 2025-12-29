#!/usr/bin/env python3
"""
Run Tracker - Manages execution history and progress analysis

Tracks all solver runs, maintains best solutions, and provides
analysis capabilities for decision-making.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class RunResult:
    """Single solver run result"""
    dataset: str
    iteration: int
    seed: int
    cost: int
    is_valid: bool
    timestamp: float
    duration: float
    antenna_count: int
    message: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class IterationSummary:
    """Summary of one iteration across multiple seeds"""
    iteration: int
    best_cost: int
    avg_cost: float
    worst_cost: int
    valid_runs: int
    total_runs: int
    timestamp: float


class RunTracker:
    """Tracks solver runs and analyzes progress"""

    def __init__(self, workspace_dir: Path):
        self.workspace_dir = Path(workspace_dir)
        self.history_file = self.workspace_dir / "run_history.jsonl"
        self.state_file = self.workspace_dir / "workflow_state.json"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # In-memory state
        self.current_state = self._load_state()

    def _load_state(self) -> Dict:
        """Load current workflow state"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)

        return {
            "datasets": {},
            "started_at": time.time(),
            "last_update": time.time()
        }

    def _save_state(self):
        """Save current workflow state"""
        self.current_state["last_update"] = time.time()
        with open(self.state_file, 'w') as f:
            json.dump(self.current_state, f, indent=2)

    def record_run(self, result: RunResult):
        """Record a single run result"""
        # Append to history file
        with open(self.history_file, 'a') as f:
            f.write(json.dumps(result.to_dict()) + '\n')

        # Update in-memory state
        dataset = result.dataset
        if dataset not in self.current_state["datasets"]:
            self.current_state["datasets"][dataset] = {
                "iteration": 0,
                "best_cost": float('inf'),
                "best_solution": None,
                "history": [],
                "reflection_count": 0,
                "started_at": time.time()
            }

        ds = self.current_state["datasets"][dataset]

        # Update best if applicable
        if result.is_valid and result.cost < ds["best_cost"]:
            ds["best_cost"] = result.cost
            ds["best_improved_at"] = time.time()
            ds["best_iteration"] = result.iteration

        self._save_state()

    def start_iteration(self, dataset: str, iteration: int):
        """Mark the start of a new iteration"""
        if dataset not in self.current_state["datasets"]:
            self.current_state["datasets"][dataset] = {
                "iteration": 0,
                "best_cost": float('inf'),
                "best_solution": None,
                "history": [],
                "reflection_count": 0,
                "started_at": time.time()
            }

        self.current_state["datasets"][dataset]["iteration"] = iteration
        self._save_state()

    def finish_iteration(self, dataset: str, iteration: int, summary: IterationSummary):
        """Mark the end of an iteration with summary"""
        ds = self.current_state["datasets"][dataset]
        # Convert IterationSummary to dict for JSON serialization
        ds["history"].append(summary.to_dict() if hasattr(summary, 'to_dict') else asdict(summary))
        self._save_state()

    def increment_reflection(self, dataset: str):
        """Increment reflection counter"""
        self.current_state["datasets"][dataset]["reflection_count"] += 1
        self._save_state()

    def get_dataset_state(self, dataset: str) -> Optional[Dict]:
        """Get current state for a dataset"""
        return self.current_state["datasets"].get(dataset)

    def get_best_cost(self, dataset: str) -> float:
        """Get best cost achieved for dataset"""
        ds = self.get_dataset_state(dataset)
        return ds["best_cost"] if ds else float('inf')

    def get_iteration_history(self, dataset: str, window: int = 10) -> List[IterationSummary]:
        """Get recent iteration history"""
        ds = self.get_dataset_state(dataset)
        if not ds or not ds["history"]:
            return []

        history = ds["history"][-window:]
        return [IterationSummary(**h) if isinstance(h, dict) else h for h in history]

    def analyze_progress(self, dataset: str, window: int = 5) -> Dict:
        """Analyze recent progress for a dataset"""
        history = self.get_iteration_history(dataset, window)

        if len(history) < 2:
            return {
                "status": "insufficient_data",
                "trend": "unknown",
                "improvement_rate": 0.0,
                "is_stagnant": False,
                "iterations_analyzed": len(history)
            }

        # Calculate improvement
        first_cost = history[0].best_cost
        last_cost = history[-1].best_cost
        improvement = (first_cost - last_cost) / first_cost * 100

        # Detect stagnation (no improvement in recent iterations)
        recent_costs = [h.best_cost for h in history[-3:]]
        is_stagnant = len(set(recent_costs)) == 1  # All same

        # Determine trend
        if improvement > 1.0:
            trend = "improving"
        elif improvement > 0.1:
            trend = "slow_progress"
        elif improvement < -0.5:
            trend = "regressing"
        else:
            trend = "stagnant"

        return {
            "status": "analyzed",
            "trend": trend,
            "improvement_rate": improvement,
            "is_stagnant": is_stagnant,
            "iterations_analyzed": len(history),
            "best_cost": last_cost,
            "first_cost": first_cost,
            "improvement_absolute": first_cost - last_cost
        }

    def get_summary(self) -> Dict:
        """Get overall workflow summary"""
        total_runtime = time.time() - self.current_state["started_at"]

        dataset_summaries = {}
        for dataset, ds in self.current_state["datasets"].items():
            dataset_summaries[dataset] = {
                "iteration": ds["iteration"],
                "best_cost": ds["best_cost"],
                "total_iterations": len(ds["history"]),
                "reflection_count": ds["reflection_count"]
            }

        return {
            "total_runtime": total_runtime,
            "datasets": dataset_summaries,
            "started_at": self.current_state["started_at"]
        }

    def export_report(self, output_file: Path):
        """Export detailed report as JSON"""
        summary = self.get_summary()

        # Add detailed analysis for each dataset
        for dataset in self.current_state["datasets"].keys():
            analysis = self.analyze_progress(dataset, window=10)
            history = self.get_iteration_history(dataset, window=20)

            summary["datasets"][dataset].update({
                "analysis": analysis,
                "recent_history": [
                    {
                        "iteration": h.iteration,
                        "best_cost": h.best_cost,
                        "avg_cost": h.avg_cost
                    }
                    for h in history
                ]
            })

        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)

        return summary

    def print_status(self, dataset: str):
        """Print current status for dataset"""
        ds = self.get_dataset_state(dataset)
        if not ds:
            print(f"  {dataset}: No data yet")
            return

        analysis = self.analyze_progress(dataset)

        print(f"\n  {dataset}:")
        print(f"    Iteration: {ds['iteration']}")
        print(f"    Best cost: {ds['best_cost']:,}")
        print(f"    Trend: {analysis['trend']}")
        if analysis['improvement_rate'] != 0:
            print(f"    Recent improvement: {analysis['improvement_rate']:.2f}%")
        print(f"    Reflections: {ds['reflection_count']}")


def load_tracker(workspace_dir: Path) -> RunTracker:
    """Load or create a run tracker"""
    return RunTracker(workspace_dir)
