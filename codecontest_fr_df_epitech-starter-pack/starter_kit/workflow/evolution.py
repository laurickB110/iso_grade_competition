#!/usr/bin/env python3
"""
AI-Guided Solver Evolution Workflow

Complete automation for evolving optimized solvers through AI generation.

Workflow:
1. BENCHMARK: Test all existing solvers on all datasets
2. ANALYZE: AI identifies patterns and opportunities
3. GENERATE: AI creates specialized solvers for each dataset
4. VALIDATE: Test generated solvers
5. ITERATE: Evolve best solvers further

Usage:
    python workflow/evolution.py [--generations 3] [--datasets dataset1 dataset2]
"""

import sys
import json
import time
import argparse
import importlib
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv
import os

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow.ai_solver_generator import SolverEvolutionEngine
from score_function import getSolutionScore
import starter_kit


class EvolutionWorkflow:
    """Complete workflow for AI-guided solver evolution"""

    def __init__(self, api_key: str):
        self.engine = SolverEvolutionEngine(api_key)
        self.root_dir = Path(__file__).parent.parent
        self.datasets_dir = self.root_dir / "datasets"
        self.results_dir = self.root_dir / "workflow" / "evolution_results"
        self.results_dir.mkdir(exist_ok=True)

        # Track all results
        self.benchmark_results = {}
        self.dataset_characteristics = {}
        self.generation_results = {}
        self.starting_generation = 1

    def load_dataset(self, dataset_name: str) -> dict:
        """Load a dataset from disk"""
        dataset_path = self.datasets_dir / f"{dataset_name}.json"
        with open(dataset_path) as f:
            return json.load(f)

    def detect_existing_generations(self, datasets: List[str]) -> Dict[str, int]:
        """
        Detect existing generated solvers for each dataset.
        Returns dict of {dataset_name: max_generation_number}
        """
        existing = {}

        for dataset_name in datasets:
            max_gen = 0
            # Look for ai_{dataset}_gen*.py files
            # Must match the naming in ai_solver_generator.py line 132
            safe_name = dataset_name.replace("_", "").replace("-", "")
            pattern = f"ai_{safe_name}_gen*.py"
            for filepath in self.engine.generated_dir.glob(pattern):
                # Extract generation number
                filename = filepath.stem
                if '_gen' in filename:
                    try:
                        gen_num = int(filename.split('_gen')[1])
                        max_gen = max(max_gen, gen_num)
                    except (ValueError, IndexError):
                        continue

            if max_gen > 0:
                existing[dataset_name] = max_gen

        return existing

    def load_existing_solvers_into_benchmark(self, datasets: List[str]) -> int:
        """
        Load existing generated solvers into benchmark results.
        Returns the maximum generation number found.
        """
        max_generation = 0

        for dataset_name in datasets:
            if dataset_name not in self.benchmark_results:
                self.benchmark_results[dataset_name] = {}

            # Find all generated solvers for this dataset
            # Must match the naming in ai_solver_generator.py line 132
            safe_name = dataset_name.replace("_", "").replace("-", "")
            pattern = f"ai_{safe_name}_gen*.py"

            for filepath in self.engine.generated_dir.glob(pattern):
                filename = filepath.stem

                # Extract generation number
                if '_gen' in filename:
                    try:
                        gen_num = int(filename.split('_gen')[1])
                        max_generation = max(max_generation, gen_num)

                        # Test this solver
                        solver_method = f"methods.generated.{filename}:solve"
                        dataset = self.load_dataset(dataset_name)

                        best_cost, avg_cost, is_valid = self.test_solver(
                            solver_method, dataset_name, dataset, seeds=[0, 1, 2]
                        )

                        if is_valid:
                            self.benchmark_results[dataset_name][filename] = best_cost

                    except (ValueError, IndexError, Exception):
                        continue

        return max_generation

    def ask_user_continue_or_restart(self, existing_gens: Dict[str, int]) -> bool:
        """
        Ask user if they want to continue from existing generations or restart.
        Returns True to continue, False to restart.
        """
        print("\n" + "⚠️ " * 20)
        print("EXISTING GENERATIONS DETECTED")
        print("⚠️ " * 20)
        print()

        for dataset_name, max_gen in existing_gens.items():
            print(f"  📁 {dataset_name}: {max_gen} generation(s) found")

        print()
        print("Options:")
        print("  [C] CONTINUE - Keep existing solvers and generate new generations")
        print("  [R] RESTART  - Delete existing solvers and start from generation 1")
        print()

        while True:
            choice = input("Your choice (C/R): ").strip().upper()

            if choice == 'C':
                print("\n✅ Continuing from existing generations...")
                return True
            elif choice == 'R':
                print("\n🔄 Restarting from generation 1...")

                # Ask for confirmation
                confirm = input("⚠️  This will DELETE existing solvers. Confirm? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    # Delete existing generated solvers
                    for filepath in self.engine.generated_dir.glob("ai_*.py"):
                        filepath.unlink()
                        print(f"  🗑️  Deleted {filepath.name}")
                    print("✅ Cleanup complete")
                    return False
                else:
                    print("Cancelled. Continuing instead...")
                    return True
            else:
                print("Invalid choice. Please enter C or R.")

    def analyze_dataset_characteristics(self, dataset_name: str, dataset: dict) -> dict:
        """Extract characteristics from a dataset"""
        buildings = dataset['buildings']

        # Calculate statistics
        demands = [max(b['populationPeakHours'], b['populationOffPeakHours'], b['populationNight'])
                   for b in buildings]

        xs = [b['x'] for b in buildings]
        ys = [b['y'] for b in buildings]

        # Simple clustering measure (variance)
        avg_x = sum(xs) / len(xs)
        avg_y = sum(ys) / len(ys)
        spread = sum((x - avg_x)**2 + (y - avg_y)**2 for x, y in zip(xs, ys)) / len(buildings)

        return {
            "num_buildings": len(buildings),
            "avg_demand": sum(demands) / len(demands),
            "max_demand": max(demands),
            "min_demand": min(demands),
            "spatial_spread": spread,
            "clustering": "high" if spread < 50000 else "medium" if spread < 200000 else "low",
            "distribution": "dense" if len(buildings) > 3000 else "moderate" if len(buildings) > 500 else "sparse"
        }

    def test_solver(
        self,
        solver_method: str,
        dataset_name: str,
        dataset: dict,
        seeds: List[int] = None
    ) -> Tuple[float, float, bool]:
        """
        Test a solver on a dataset.

        Returns:
            (best_cost, avg_cost, is_valid)
        """

        if seeds is None:
            seeds = list(range(5))

        costs = []

        for seed in seeds:
            try:
                # Import the solver
                if solver_method == "solver:optimized_solution":
                    solution = starter_kit.optimized_solution(dataset, seed=seed)
                else:
                    # Dynamic import
                    module_path, func_name = solver_method.split(":")
                    module = importlib.import_module(module_path)
                    solve_func = getattr(module, func_name)
                    solution = solve_func(dataset, seed=seed)

                # Score it
                solution_json = json.dumps(solution)
                dataset_json = json.dumps(dataset)
                cost, is_valid, message = getSolutionScore(solution_json, dataset_json)

                if is_valid:
                    costs.append(cost)
                else:
                    print(f"  ⚠️  Invalid solution for {solver_method} seed {seed}: {message}")

            except Exception as e:
                print(f"  ❌ Error testing {solver_method} seed {seed}: {e}")
                continue

        if not costs:
            return float('inf'), float('inf'), False

        return min(costs), sum(costs) / len(costs), True

    def benchmark_all_solvers(
        self,
        datasets: List[str],
        solvers: List[str] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Benchmark all solvers on all datasets.

        Args:
            datasets: List of dataset names
            solvers: List of solver methods (defaults to built-ins)

        Returns:
            Results dict: {dataset_name: {solver_name: cost}}
        """

        if solvers is None:
            solvers = [
                "solver:optimized_solution",
                "methods.baseline_place_on_buildings:solve",
                "methods.randomized_greedy:solve"
            ]

        print("=" * 70)
        print("PHASE 1: BENCHMARKING ALL SOLVERS")
        print("=" * 70)
        print()

        results = {}

        for dataset_name in datasets:
            print(f"\n📊 Benchmarking {dataset_name}...")
            dataset = self.load_dataset(dataset_name)

            # Analyze dataset
            self.dataset_characteristics[dataset_name] = self.analyze_dataset_characteristics(
                dataset_name, dataset
            )

            results[dataset_name] = {}

            for solver_method in solvers:
                solver_name = solver_method.split(":")[-1]
                print(f"  Testing {solver_name}...", end=" ", flush=True)

                best_cost, avg_cost, is_valid = self.test_solver(
                    solver_method, dataset_name, dataset
                )

                if is_valid:
                    results[dataset_name][solver_name] = best_cost
                    print(f"Best: {best_cost:,} | Avg: {avg_cost:,.0f}")
                else:
                    print("FAILED")

        self.benchmark_results = results

        # Save benchmark results
        benchmark_file = self.results_dir / "benchmark_results.json"
        with open(benchmark_file, 'w') as f:
            json.dump({
                "results": results,
                "characteristics": self.dataset_characteristics,
                "timestamp": time.time()
            }, f, indent=2)

        print(f"\n✅ Benchmark complete. Results saved to {benchmark_file}")

        return results

    def run_evolution_cycle(
        self,
        datasets: List[str],
        generation: int = 1
    ) -> Dict[str, str]:
        """
        Run one evolution cycle: analyze, generate, validate.

        Args:
            datasets: Datasets to generate solvers for
            generation: Generation number

        Returns:
            Dict of {dataset_name: generated_solver_path}
        """

        print("\n" + "=" * 70)
        print(f"PHASE {generation + 1}: EVOLUTION CYCLE {generation}")
        print("=" * 70)
        print()

        # Step 1: Analyze performance
        print("🧠 Step 1: AI Performance Analysis")
        analysis = self.engine.analyze_solver_performance(
            self.benchmark_results,
            self.dataset_characteristics
        )
        print("✅ Analysis complete")

        # Save analysis
        analysis_file = self.results_dir / f"analysis_gen{generation}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        # Step 2: Generate specialized solvers
        print(f"\n🧬 Step 2: Generating Specialized Solvers")

        generated_solvers = {}

        for dataset_name in datasets:
            print(f"\n  → {dataset_name}")

            filename, code = self.engine.generate_specialized_solver(
                dataset_name=dataset_name,
                dataset_characteristics=self.dataset_characteristics[dataset_name],
                benchmark_results=self.benchmark_results[dataset_name],
                analysis=analysis,
                generation=generation
            )

            # Save solver
            filepath = self.engine.save_solver(filename, code)

            # Validate syntax
            is_valid, error = self.engine.validate_solver_syntax(filepath)

            if is_valid:
                print(f"    ✅ Syntax valid")
                generated_solvers[dataset_name] = f"methods.generated.{filename[:-3]}:solve"
            else:
                print(f"    ❌ Syntax error: {error}")
                print(f"    Skipping this solver...")

        # Step 3: Test generated solvers
        print(f"\n🧪 Step 3: Validating Generated Solvers")

        validation_results = {}

        for dataset_name, solver_method in generated_solvers.items():
            print(f"\n  Testing {dataset_name}...", end=" ", flush=True)

            dataset = self.load_dataset(dataset_name)
            best_cost, avg_cost, is_valid = self.test_solver(
                solver_method, dataset_name, dataset, seeds=[0, 1, 2]
            )

            if is_valid:
                validation_results[dataset_name] = best_cost
                print(f"Best: {best_cost:,} | Avg: {avg_cost:,.0f}")

                # Compare to existing best
                existing_best = min(self.benchmark_results[dataset_name].values())
                improvement = (existing_best - best_cost) / existing_best * 100

                if best_cost < existing_best:
                    print(f"    🎉 IMPROVEMENT: {improvement:.1f}% better than existing best!")
                elif abs(improvement) < 5:
                    print(f"    ⚖️  Similar performance ({improvement:+.1f}%)")
                else:
                    print(f"    📉 Worse than existing best ({improvement:+.1f}%)")

                # Update benchmark if better
                if best_cost < existing_best:
                    solver_name = solver_method.split(":")[-1]
                    self.benchmark_results[dataset_name][solver_name] = best_cost

            else:
                print("FAILED - runtime errors")

        self.generation_results[f"gen{generation}"] = validation_results

        # Save generation results
        gen_file = self.results_dir / f"generation_{generation}_results.json"
        with open(gen_file, 'w') as f:
            json.dump({
                "generation": generation,
                "generated_solvers": generated_solvers,
                "validation_results": validation_results,
                "timestamp": time.time()
            }, f, indent=2)

        return generated_solvers

    def print_final_report(self):
        """Print summary of evolution workflow"""

        print("\n" + "=" * 70)
        print("EVOLUTION WORKFLOW COMPLETE")
        print("=" * 70)
        print()

        print("📊 Final Results by Dataset:")
        print()

        for dataset_name in self.benchmark_results:
            print(f"  {dataset_name}:")
            costs = self.benchmark_results[dataset_name]

            for solver_name, cost in sorted(costs.items(), key=lambda x: x[1]):
                print(f"    {solver_name:30s} {cost:>15,}")

            print()

        print(f"Generated solvers saved in: {self.engine.generated_dir}")
        print(f"Results saved in: {self.results_dir}")


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="AI-Guided Solver Evolution"
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=2,
        help="Number of evolution generations (default: 2)"
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["1_peaceful_village", "2_small_town", "3_suburbia"],
        help="Datasets to evolve solvers for"
    )
    parser.add_argument(
        "--continue",
        dest="continue_from_existing",
        action="store_true",
        help="Continue from existing generations without prompting"
    )

    args = parser.parse_args()

    # Load API key
    load_dotenv(Path(__file__).parent.parent / ".env")
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in .env")
        print("AI solver generation requires API access.")
        sys.exit(1)

    print()
    print("=" * 70)
    print("   AI-GUIDED SOLVER EVOLUTION")
    print("=" * 70)
    print()
    print(f"Target datasets: {', '.join(args.datasets)}")
    print(f"Requested generations: {args.generations}")
    print()

    # Initialize workflow
    workflow = EvolutionWorkflow(api_key)

    # Check for existing generations
    existing_gens = workflow.detect_existing_generations(args.datasets)

    if existing_gens:
        # Existing generations found
        if args.continue_from_existing:
            # Auto-continue mode
            print(f"🔄 Continuing from existing generations (--continue flag detected)")
            for dataset_name, max_gen in existing_gens.items():
                print(f"  📁 {dataset_name}: {max_gen} generation(s) found")
            print()

            should_continue = True
        else:
            # Ask user interactively
            should_continue = workflow.ask_user_continue_or_restart(existing_gens)

        if should_continue:
            # Load existing solvers into benchmark
            print("\n📊 Loading existing solvers into benchmark...")
            max_existing_gen = workflow.load_existing_solvers_into_benchmark(args.datasets)
            workflow.starting_generation = max_existing_gen + 1

            print(f"✅ Loaded {max_existing_gen} existing generation(s)")
            print(f"🚀 Will generate generations {workflow.starting_generation} to {workflow.starting_generation + args.generations - 1}")
            print()
        else:
            # Restart from generation 1
            workflow.starting_generation = 1
    else:
        # No existing generations
        print("No existing generations found. Starting from generation 1.")
        print()

    # Phase 1: Benchmark existing solvers (baseline + any previously generated)
    workflow.benchmark_all_solvers(args.datasets)

    # Phase 2-N: Evolution cycles
    end_generation = workflow.starting_generation + args.generations - 1

    for gen in range(workflow.starting_generation, end_generation + 1):
        try:
            workflow.run_evolution_cycle(args.datasets, generation=gen)
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Saving progress...")
            break
        except Exception as e:
            print(f"\n\n❌ Error in generation {gen}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Final report
    workflow.print_final_report()


if __name__ == "__main__":
    main()
