#!/usr/bin/env python3
"""
Analyzer - Automatic decision logic for workflow control

Analyzes solver performance and makes decisions about:
- Whether to continue optimization
- When to trigger AI reflection
- When to stop (target reached or limits exceeded)
"""

import time
from typing import Dict, Tuple
from enum import Enum


class Decision(Enum):
    """Possible workflow decisions"""
    CONTINUE = "continue"           # Keep running iterations
    REFLECT = "reflect"             # Trigger AI reflection phase
    TARGET_REACHED = "target"       # Target score achieved, move to next dataset
    MAX_ITERATIONS = "max_iter"     # Max iterations reached
    MAX_REFLECTIONS = "max_reflect" # Max reflection cycles reached
    TIMEOUT = "timeout"             # Time limit exceeded
    STAGNANT = "stagnant"           # No progress, should reflect or stop


class WorkflowAnalyzer:
    """Makes decisions about workflow progression"""

    def __init__(self, config: Dict):
        self.config = config

    def should_continue(
        self,
        dataset: str,
        current_iteration: int,
        best_cost: float,
        analysis: Dict,
        reflection_count: int,
        elapsed_time: float
    ) -> Tuple[Decision, str]:
        """
        Decide whether to continue, reflect, or stop.

        Returns:
            (Decision, reason_message)
        """

        # Check if target is reached
        target = self.config["target_scores"].get(dataset)
        if target and best_cost <= target:
            return (
                Decision.TARGET_REACHED,
                f"Target score {target:,} reached with {best_cost:,}"
            )

        # Check max iterations
        max_iter = self.config["max_iterations"]
        if current_iteration >= max_iter:
            return (
                Decision.MAX_ITERATIONS,
                f"Maximum iterations ({max_iter}) reached"
            )

        # Check timeout
        max_runtime = self.config.get("max_runtime_per_dataset", 0)
        if max_runtime > 0 and elapsed_time >= max_runtime:
            return (
                Decision.TIMEOUT,
                f"Time limit ({max_runtime}s) exceeded"
            )

        # Check if we should trigger reflection
        if self._should_reflect(analysis, reflection_count, current_iteration):
            max_reflections = self.config["max_reflection_cycles"]
            if reflection_count >= max_reflections:
                return (
                    Decision.MAX_REFLECTIONS,
                    f"Maximum reflection cycles ({max_reflections}) reached"
                )
            return (
                Decision.REFLECT,
                f"Progress stagnant, triggering reflection (cycle {reflection_count + 1})"
            )

        # Continue normally
        return (Decision.CONTINUE, "Continuing optimization")

    def _should_reflect(
        self,
        analysis: Dict,
        reflection_count: int,
        current_iteration: int
    ) -> bool:
        """Determine if reflection should be triggered"""

        # Don't reflect if disabled
        if not self.config.get("enable_ai_reflection", False):
            return False

        # Don't reflect too early
        min_iter_before_reflect = 5
        if current_iteration < min_iter_before_reflect:
            return False

        # Check if insufficient data
        if analysis["status"] == "insufficient_data":
            return False

        # Check stagnation
        stagnation_limit = self.config.get("stagnation_limit", 10)
        if analysis.get("is_stagnant", False):
            # Check how many iterations have been stagnant
            # For simplicity, trigger if trend is stagnant
            return analysis["trend"] == "stagnant"

        # Check improvement rate
        min_improvement = self.config.get("min_improvement_threshold", 0.5)
        if 0 <= analysis["improvement_rate"] < min_improvement:
            return True

        # Check regression
        if analysis["trend"] == "regressing":
            return True

        return False

    def format_decision_message(
        self,
        decision: Decision,
        reason: str,
        dataset: str,
        best_cost: float,
        target_cost: float
    ) -> str:
        """Format a human-readable decision message"""

        lines = [
            f"\n{'='*70}",
            f"DECISION: {decision.value.upper()}",
            f"Dataset: {dataset}",
            f"Best cost: {best_cost:,}",
        ]

        if target_cost:
            gap = best_cost - target_cost
            gap_pct = (gap / target_cost) * 100
            lines.append(f"Target: {target_cost:,} (gap: {gap:+,} / {gap_pct:+.1f}%)")

        lines.extend([
            f"Reason: {reason}",
            f"{'='*70}\n"
        ])

        return "\n".join(lines)


def create_analyzer(config: Dict) -> WorkflowAnalyzer:
    """Create an analyzer from configuration"""
    return WorkflowAnalyzer(config)
