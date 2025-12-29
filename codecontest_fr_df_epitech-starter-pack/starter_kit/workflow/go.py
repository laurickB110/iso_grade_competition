#!/usr/bin/env python3
"""
GO - Main entry point for automated workflow

Single command to launch the complete optimization workflow:
- Iteratively runs solver
- Analyzes results
- Triggers AI reflection when needed
- Stops when targets are reached or limits exceeded

Usage:
    python workflow/go.py [--config workflow/config.yaml]
"""

import sys
import json
import time
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow.tracker import RunTracker, RunResult, IterationSummary
from workflow.analyzer import WorkflowAnalyzer, Decision, create_analyzer

from starter_kit import optimized_solution
from score_function import getSolutionScore


class WorkflowOrchestrator:
    """Orchestrates the complete optimization workflow"""

    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.root_dir = Path(__file__).parent.parent
        self.workspace_dir = self.root_dir / "workflow" / "workspace"
        self.datasets_dir = self.root_dir / "datasets"
        self.solutions_dir = self.root_dir / "solutions" / "best"

        # Initialize components
        self.tracker = RunTracker(self.workspace_dir)
        self.analyzer = create_analyzer(self.config)

        # Track start time
        self.start_time = time.time()

        # Ensure directories exist
        self.solutions_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: Path) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def _load_dataset(self, dataset_name: str) -> Dict:
        """Load a dataset from file"""
        dataset_path = self.datasets_dir / f"{dataset_name}.json"
        with open(dataset_path) as f:
            return json.load(f)

    def _get_active_datasets(self) -> List[str]:
        """Get list of active datasets from config"""
        active = self.config.get("active_datasets", [])

        if not active:
            # Process all datasets if none specified
            return [
                f.stem for f in self.datasets_dir.glob("*.json")
            ]

        return active

    def _run_solver_iteration(
        self,
        dataset_name: str,
        dataset: Dict,
        iteration: int,
        seed: int
    ) -> RunResult:
        """Run solver once and return result"""

        start = time.time()

        try:
            # Suppress solver print statements for cleaner output
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                # Run the solver
                solution = optimized_solution(
                    dataset,
                    num_iterations=self.config["solver_params"].get("iterations", 1000),
                    seed=seed
                )

            # Convert solution to JSON string for scoring
            solution_json = json.dumps(solution)
            dataset_json = json.dumps(dataset)

            # Score the solution
            cost, is_valid, message = getSolutionScore(solution_json, dataset_json)

            # Count antennas
            antenna_count = len(solution.get("antennas", []))

            duration = time.time() - start

            return RunResult(
                dataset=dataset_name,
                iteration=iteration,
                seed=seed,
                cost=cost if is_valid else float('inf'),
                is_valid=is_valid,
                timestamp=time.time(),
                duration=duration,
                antenna_count=antenna_count,
                message=message
            )

        except Exception as e:
            duration = time.time() - start
            return RunResult(
                dataset=dataset_name,
                iteration=iteration,
                seed=seed,
                cost=float('inf'),
                is_valid=False,
                timestamp=time.time(),
                duration=duration,
                antenna_count=0,
                message=f"Error: {str(e)}"
            )

    def _save_solution(self, dataset_name: str, solution: Dict, cost: int):
        """Save a solution to disk"""
        output_path = self.solutions_dir / f"{dataset_name}.json"

        # Always update if better
        if output_path.exists():
            with open(output_path) as f:
                existing = json.load(f)
                # Check if this solution is better (you may want to add score metadata)

        with open(output_path, 'w') as f:
            json.dump(solution, f, indent=2)

        # Also save with timestamp and cost
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = self.solutions_dir.parent / f"solution_{dataset_name}_{cost}_{timestamp}.json"
        with open(backup_path, 'w') as f:
            json.dump(solution, f, indent=2)

    def _run_iteration(
        self,
        dataset_name: str,
        dataset: Dict,
        iteration: int
    ) -> IterationSummary:
        """Run one iteration with multiple seeds"""

        seeds_count = self.config["seeds_per_iteration"]
        verbosity = self.config.get("verbosity", 1)

        if verbosity >= 1:
            print(f"  Iteration {iteration} (seeds: {seeds_count})...", end=" ", flush=True)

        results = []
        best_solution = None
        best_cost = float('inf')

        for seed in range(seeds_count):
            result = self._run_solver_iteration(dataset_name, dataset, iteration, seed)
            self.tracker.record_run(result)
            results.append(result)

            # Track best solution
            if result.is_valid and result.cost < best_cost:
                best_cost = result.cost
                # Re-run to get solution object for saving
                import io
                from contextlib import redirect_stdout
                f = io.StringIO()
                with redirect_stdout(f):
                    best_solution = optimized_solution(
                        dataset,
                        num_iterations=self.config["solver_params"].get("iterations", 1000),
                        seed=seed
                    )

        # Calculate summary
        valid_results = [r for r in results if r.is_valid]
        if not valid_results:
            print("NO VALID SOLUTIONS!")
            return None

        costs = [r.cost for r in valid_results]
        summary = IterationSummary(
            iteration=iteration,
            best_cost=min(costs),
            avg_cost=sum(costs) / len(costs),
            worst_cost=max(costs),
            valid_runs=len(valid_results),
            total_runs=len(results),
            timestamp=time.time()
        )

        # Save best solution if improved
        if best_solution and best_cost < self.tracker.get_best_cost(dataset_name):
            self._save_solution(dataset_name, best_solution, best_cost)

        if verbosity >= 1:
            print(f"Best: {summary.best_cost:,} | Avg: {summary.avg_cost:,.0f}")

        return summary

    def _reflect_and_improve(self, dataset_name: str) -> bool:
        """
        Trigger AI reflection phase to analyze and improve strategy.

        Returns:
            True if improvements were applied, False otherwise
        """
        print("\n" + "="*70)
        print("REFLECTION PHASE - Analyzing performance and suggesting improvements")
        print("="*70)

        # Get current state
        state = self.tracker.get_dataset_state(dataset_name)
        analysis = self.tracker.analyze_progress(dataset_name, window=10)

        print(f"\nCurrent state for {dataset_name}:")
        print(f"  Best cost: {state['best_cost']:,}")
        print(f"  Iterations completed: {len(state['history'])}")
        print(f"  Recent trend: {analysis['trend']}")
        print(f"  Improvement rate: {analysis['improvement_rate']:.2f}%")

        # Check if AI reflection is enabled
        if not self.config.get("enable_ai_reflection", False):
            print("\nAI reflection is disabled in config.")
            print("Continuing with current strategy...")
            return False

        print("\n[AI Reflection would be triggered here]")
        print("This would analyze:")
        print("  - Solver parameters effectiveness")
        print("  - Strategy bottlenecks")
        print("  - Potential improvements")
        print("\nNote: Implement AI reflection by calling Claude API with context")
        print("      See workflow/reflection_template.py for implementation guide")

        self.tracker.increment_reflection(dataset_name)

        # For now, just continue
        return False

    def _process_dataset(self, dataset_name: str) -> Dict:
        """Process a single dataset through the workflow"""

        print(f"\n{'='*70}")
        print(f"PROCESSING: {dataset_name}")
        print(f"{'='*70}")

        # Load dataset
        dataset = self._load_dataset(dataset_name)
        target_cost = self.config["target_scores"].get(dataset_name)

        if target_cost:
            print(f"Target score: {target_cost:,}")
        else:
            print("Target score: Not set")

        # Initialize tracking
        self.tracker.start_iteration(dataset_name, 0)
        dataset_start = time.time()

        iteration = 1
        while True:
            # Run iteration
            self.tracker.start_iteration(dataset_name, iteration)
            summary = self._run_iteration(dataset_name, dataset, iteration)

            if summary is None:
                print("Failed to generate valid solutions. Stopping.")
                break

            self.tracker.finish_iteration(dataset_name, iteration, summary)

            # Analyze progress
            best_cost = self.tracker.get_best_cost(dataset_name)
            analysis = self.tracker.analyze_progress(
                dataset_name,
                window=self.config.get("analysis_window", 5)
            )

            # Get current state
            state = self.tracker.get_dataset_state(dataset_name)
            elapsed = time.time() - dataset_start

            # Make decision
            decision, reason = self.analyzer.should_continue(
                dataset=dataset_name,
                current_iteration=iteration,
                best_cost=best_cost,
                analysis=analysis,
                reflection_count=state["reflection_count"],
                elapsed_time=elapsed
            )

            # Handle decision
            if decision == Decision.CONTINUE:
                iteration += 1
                continue

            elif decision == Decision.REFLECT:
                print(f"\n{reason}")
                improved = self._reflect_and_improve(dataset_name)

                if improved:
                    print("Improvements applied. Continuing optimization...")
                    iteration += 1
                    continue
                else:
                    # Continue anyway after reflection
                    iteration += 1
                    continue

            else:
                # Terminal decision (target reached, max iterations, etc.)
                msg = self.analyzer.format_decision_message(
                    decision, reason, dataset_name, best_cost, target_cost
                )
                print(msg)
                break

        # Return summary
        return {
            "dataset": dataset_name,
            "best_cost": self.tracker.get_best_cost(dataset_name),
            "iterations": iteration,
            "elapsed": time.time() - dataset_start
        }

    def run(self):
        """Run the complete workflow"""

        print("\n" + "="*70)
        print("AUTOMATED WORKFLOW - GO")
        print("="*70)

        active_datasets = self._get_active_datasets()
        print(f"\nDatasets to process: {', '.join(active_datasets)}")
        print(f"Configuration: {Path(self.config.get('__config_path__', 'config.yaml')).name}")

        # Process each dataset
        results = []
        for dataset_name in active_datasets:
            result = self._process_dataset(dataset_name)
            results.append(result)

            # Check global timeout
            total_elapsed = time.time() - self.start_time
            max_runtime = self.config.get("max_runtime_seconds", 0)
            if max_runtime > 0 and total_elapsed >= max_runtime:
                print(f"\n{'='*70}")
                print(f"GLOBAL TIMEOUT REACHED ({max_runtime}s)")
                print(f"{'='*70}")
                break

        # Generate final report
        self._print_final_report(results)

        # Export detailed report
        report_path = self.workspace_dir / "final_report.json"
        self.tracker.export_report(report_path)
        print(f"\nDetailed report saved to: {report_path}")

    def _print_final_report(self, results: List[Dict]):
        """Print final summary report"""

        total_time = time.time() - self.start_time

        print("\n" + "="*70)
        print("WORKFLOW COMPLETE - FINAL REPORT")
        print("="*70)

        print(f"\nTotal runtime: {total_time:.1f}s ({total_time/60:.1f} min)")
        print(f"Datasets processed: {len(results)}")

        print("\nResults by dataset:")
        print(f"{'Dataset':<25} {'Best Cost':>15} {'Iterations':>12} {'Time':>10}")
        print("-" * 70)

        for result in results:
            dataset = result["dataset"]
            cost = result["best_cost"]
            iterations = result["iterations"]
            elapsed = result["elapsed"]

            # Check if target was reached
            target = self.config["target_scores"].get(dataset)
            status = ""
            if target and cost <= target:
                status = " ✓"

            print(f"{dataset:<25} {cost:>15,}{status} {iterations:>12} {elapsed:>9.1f}s")

        print("\nBest solutions saved to: solutions/best/")


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="Automated optimization workflow - Single GO command"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).parent / "config.yaml",
        help="Path to configuration file (default: workflow/config.yaml)"
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: Configuration file not found: {args.config}")
        print("Create it from the template or check the path.")
        sys.exit(1)

    # Store config path in config dict for reference
    orchestrator = WorkflowOrchestrator(args.config)
    orchestrator.config["__config_path__"] = str(args.config)

    try:
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\nWorkflow interrupted by user.")
        print("Current progress saved. Resume by running again.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nWorkflow failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
