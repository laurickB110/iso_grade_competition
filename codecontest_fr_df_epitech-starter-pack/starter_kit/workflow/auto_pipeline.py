#!/usr/bin/env python3
"""
AUTO PIPELINE - Complete Automated Workflow

Combines AI Solver Evolution + AI Reflection for maximum automation:
1. Generate specialized solvers for each dataset (Evolution)
2. Automatically select best solver per dataset
3. Optimize with AI Reflection using best solvers
4. Generate final report

This is the "one button" solution.

Usage:
    python workflow/auto_pipeline.py [--datasets ...] [--evolution-generations 2] [--optimization-iterations 50]
"""

import sys
import json
import time
import yaml
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv
import os

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow.evolution import EvolutionWorkflow
from workflow.go import WorkflowOrchestrator


class AutoPipeline:
    """
    Fully automated pipeline combining evolution and optimization.

    This is the ultimate automation:
    - No manual intervention needed
    - Generates best solvers automatically
    - Uses them automatically
    - Optimizes automatically
    """

    def __init__(self, api_key: str, continue_from_existing: bool = False):
        self.api_key = api_key
        self.continue_from_existing = continue_from_existing
        self.root_dir = Path(__file__).parent.parent
        self.config_path = self.root_dir / "workflow" / "config.yaml"
        self.results_dir = self.root_dir / "workflow" / "auto_results"
        self.results_dir.mkdir(exist_ok=True)

        # Load base config
        with open(self.config_path) as f:
            self.base_config = yaml.safe_load(f)

        # Results tracking
        self.evolution_results = {}
        self.optimization_results = {}
        self.best_solvers = {}

    def run_evolution_phase(
        self,
        datasets: List[str],
        generations: int
    ) -> Dict[str, str]:
        """
        Phase 1: Run AI Solver Evolution

        Args:
            datasets: Datasets to generate solvers for
            generations: Number of evolution generations

        Returns:
            Dict mapping dataset to best solver method
        """

        print("\n" + "="*70)
        print("PHASE 1: AI SOLVER EVOLUTION")
        print("="*70)
        print(f"\nGenerating specialized solvers for {len(datasets)} datasets")
        print(f"Requested generations: {generations}")
        print()

        # Run evolution workflow
        evolution = EvolutionWorkflow(self.api_key)

        # Check for existing generations
        existing_gens = evolution.detect_existing_generations(datasets)

        if existing_gens:
            # Existing generations found
            if self.continue_from_existing:
                # Auto-continue mode
                print(f"🔄 Continuing from existing generations (--continue flag detected)")
                for dataset_name, max_gen in existing_gens.items():
                    print(f"  📁 {dataset_name}: {max_gen} generation(s) found")
                print()

                should_continue = True
            else:
                # Ask user interactively
                should_continue = evolution.ask_user_continue_or_restart(existing_gens)

            if should_continue:
                # Load existing solvers into benchmark
                print("\n📊 Loading existing solvers into benchmark...")
                max_existing_gen = evolution.load_existing_solvers_into_benchmark(datasets)
                evolution.starting_generation = max_existing_gen + 1

                print(f"✅ Loaded {max_existing_gen} existing generation(s)")
                print(f"🚀 Will generate generations {evolution.starting_generation} to {evolution.starting_generation + generations - 1}")
                print()
            else:
                # Restart from generation 1
                evolution.starting_generation = 1
        else:
            # No existing generations
            print("No existing generations found. Starting from generation 1.")
            print()

        # Benchmark
        evolution.benchmark_all_solvers(datasets)

        # Run evolution cycles
        end_generation = evolution.starting_generation + generations - 1

        for gen in range(evolution.starting_generation, end_generation + 1):
            try:
                evolution.run_evolution_cycle(datasets, generation=gen)
            except KeyboardInterrupt:
                print("\n\nEvolution interrupted. Continuing with best available...")
                break
            except Exception as e:
                print(f"\n\nError in generation {gen}: {e}")
                print("Continuing with best available...")
                break

        # Store evolution results
        self.evolution_results = evolution.benchmark_results

        # Identify best solver for each dataset
        best_solvers = self._identify_best_solvers(evolution.benchmark_results)
        self.best_solvers = best_solvers

        print("\n" + "="*70)
        print("EVOLUTION PHASE COMPLETE")
        print("="*70)
        print("\n📊 Best Solvers Selected:")
        for dataset, solver_info in best_solvers.items():
            print(f"  {dataset:30s} → {solver_info['solver']:40s} (cost: {solver_info['cost']:,})")
        print()

        # Save evolution summary
        summary_path = self.results_dir / "evolution_summary.json"
        with open(summary_path, 'w') as f:
            json.dump({
                "datasets": datasets,
                "generations": generations,
                "best_solvers": best_solvers,
                "all_results": evolution.benchmark_results,
                "timestamp": time.time()
            }, f, indent=2)

        print(f"Evolution summary saved: {summary_path}\n")

        return best_solvers

    def _identify_best_solvers(
        self,
        benchmark_results: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict]:
        """
        Identify the best solver for each dataset.

        Args:
            benchmark_results: Results from benchmarking

        Returns:
            Dict with best solver info per dataset
        """

        best_solvers = {}

        for dataset_name, solvers in benchmark_results.items():
            if not solvers:
                continue

            # Find solver with minimum cost
            best_solver = min(solvers.items(), key=lambda x: x[1])
            solver_name, cost = best_solver

            # Map solver name to method path
            solver_method = self._solver_name_to_method(solver_name, dataset_name)

            best_solvers[dataset_name] = {
                "solver": solver_name,
                "method": solver_method,
                "cost": cost
            }

        return best_solvers

    def _solver_name_to_method(self, solver_name: str, dataset_name: str) -> str:
        """Convert solver name to method path"""

        # Check if it's a generated solver
        if solver_name.startswith("ai_"):
            return f"methods.generated.{solver_name}:solve"

        # Built-in solvers
        if solver_name == "optimized_solution":
            return "solver:optimized_solution"
        elif solver_name == "solve":
            # Could be from different modules, check which one
            # For now, default to baseline
            return "methods.baseline_place_on_buildings:solve"
        else:
            # Assume it's a method name from a module
            return f"methods.{solver_name}:solve"

    def run_optimization_phase(
        self,
        datasets: List[str],
        max_iterations: int
    ) -> Dict[str, Dict]:
        """
        Phase 2: Run optimization with best solvers + AI Reflection

        Args:
            datasets: Datasets to optimize
            max_iterations: Max iterations per dataset

        Returns:
            Optimization results per dataset
        """

        print("\n" + "="*70)
        print("PHASE 2: OPTIMIZATION WITH AI REFLECTION")
        print("="*70)
        print(f"\nOptimizing {len(datasets)} datasets with best solvers")
        print(f"Max iterations per dataset: {max_iterations}")
        print(f"AI Reflection: {'ENABLED' if self.base_config.get('enable_ai_reflection') else 'DISABLED'}")
        print()

        results = {}

        for dataset_name in datasets:
            print(f"\n{'='*70}")
            print(f"OPTIMIZING: {dataset_name}")
            print(f"{'='*70}")

            # Get best solver for this dataset
            if dataset_name in self.best_solvers:
                solver_method = self.best_solvers[dataset_name]["method"]
                baseline_cost = self.best_solvers[dataset_name]["cost"]
                print(f"Using solver: {solver_method}")
                print(f"Baseline cost: {baseline_cost:,}")
            else:
                # Fallback to default solver
                solver_method = self.base_config.get("solver_method", "solver:optimized_solution")
                baseline_cost = None
                print(f"Using default solver: {solver_method}")

            print()

            # Create temporary config for this dataset
            temp_config = self._create_dataset_config(
                dataset_name,
                solver_method,
                max_iterations
            )

            # Run optimization
            try:
                result = self._run_optimization_for_dataset(
                    dataset_name,
                    temp_config
                )
                results[dataset_name] = result

                # Compare to baseline
                if baseline_cost and result["best_cost"] < baseline_cost:
                    improvement = (baseline_cost - result["best_cost"]) / baseline_cost * 100
                    print(f"\n🎉 IMPROVED: {improvement:.1f}% better than evolution baseline!")

            except Exception as e:
                print(f"\n❌ Error optimizing {dataset_name}: {e}")
                import traceback
                traceback.print_exc()
                continue

        self.optimization_results = results

        print("\n" + "="*70)
        print("OPTIMIZATION PHASE COMPLETE")
        print("="*70)
        print()

        return results

    def _create_dataset_config(
        self,
        dataset_name: str,
        solver_method: str,
        max_iterations: int
    ) -> Path:
        """Create a temporary config file for a specific dataset"""

        # Copy base config
        config = self.base_config.copy()

        # Modify for this dataset
        config["active_datasets"] = [dataset_name]
        config["solver_method"] = solver_method
        config["max_iterations"] = max_iterations

        # Save temporary config
        temp_config_path = self.results_dir / f"config_{dataset_name}.yaml"
        with open(temp_config_path, 'w') as f:
            yaml.dump(config, f)

        return temp_config_path

    def _run_optimization_for_dataset(
        self,
        dataset_name: str,
        config_path: Path
    ) -> Dict:
        """Run optimization workflow for a single dataset"""

        # Create orchestrator
        orchestrator = WorkflowOrchestrator(config_path)
        orchestrator.config["__config_path__"] = str(config_path)

        # Process this dataset
        result = orchestrator._process_dataset(dataset_name)

        return result

    def generate_final_report(self):
        """Generate comprehensive final report"""

        print("\n" + "="*70)
        print("FINAL REPORT")
        print("="*70)
        print()

        print("📊 Results by Dataset:\n")

        # Combine evolution and optimization results
        all_datasets = set(self.evolution_results.keys()) | set(self.optimization_results.keys())

        for dataset_name in sorted(all_datasets):
            print(f"  {dataset_name}:")

            # Evolution baseline (best from generated solvers)
            if dataset_name in self.best_solvers:
                evolution_cost = self.best_solvers[dataset_name]["cost"]
                solver_name = self.best_solvers[dataset_name]["solver"]
                print(f"    Evolution Best: {evolution_cost:>15,} ({solver_name})")

            # Optimization final
            if dataset_name in self.optimization_results:
                opt_cost = self.optimization_results[dataset_name]["best_cost"]
                print(f"    Optimized:      {opt_cost:>15,}")

                # Calculate improvement
                if dataset_name in self.best_solvers:
                    evolution_cost = self.best_solvers[dataset_name]["cost"]
                    if opt_cost < evolution_cost:
                        improvement = (evolution_cost - opt_cost) / evolution_cost * 100
                        print(f"    Improvement:    {improvement:>14.1f}%")

            # Target (if available)
            if dataset_name in self.base_config.get("target_scores", {}):
                target = self.base_config["target_scores"][dataset_name]
                if target:
                    print(f"    Target:         {target:>15,}")

                    if dataset_name in self.optimization_results:
                        opt_cost = self.optimization_results[dataset_name]["best_cost"]
                        if opt_cost <= target:
                            print(f"    Status:         {'✅ TARGET REACHED':>15}")
                        else:
                            gap = opt_cost - target
                            gap_pct = gap / target * 100
                            print(f"    Gap:            {gap:>15,} (+{gap_pct:.1f}%)")

            print()

        # Save final report
        report = {
            "pipeline": "AUTO_PIPELINE",
            "timestamp": time.time(),
            "datasets_processed": list(all_datasets),
            "evolution_results": self.evolution_results,
            "best_solvers": self.best_solvers,
            "optimization_results": self.optimization_results,
            "config": self.base_config
        }

        report_path = self.results_dir / "final_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📁 Results saved to: {self.results_dir}")
        print(f"📄 Final report: {report_path}")
        print(f"💾 Best solutions: solutions/best/")
        print()

    def run(
        self,
        datasets: List[str],
        evolution_generations: int = 2,
        optimization_iterations: int = 50
    ):
        """
        Run the complete automated pipeline.

        Args:
            datasets: Datasets to process
            evolution_generations: Generations for solver evolution
            optimization_iterations: Max iterations for optimization
        """

        pipeline_start = time.time()

        print("\n" + "="*70)
        print("   🚀 AUTOMATED PIPELINE - FULL AI OPTIMIZATION")
        print("="*70)
        print()
        print(f"Datasets: {', '.join(datasets)}")
        print(f"Evolution generations: {evolution_generations}")
        print(f"Optimization iterations: {optimization_iterations}")
        print()
        print("This will:")
        print("  1. Generate specialized solvers for each dataset (AI Evolution)")
        print("  2. Automatically select the best solver per dataset")
        print("  3. Optimize using best solvers + AI Reflection")
        print("  4. Generate comprehensive report")
        print()
        print("Estimated time: 1-3 hours depending on datasets")
        print("="*70)
        print()

        input("Press ENTER to start (or Ctrl+C to cancel)...")

        try:
            # Phase 1: Evolution
            self.run_evolution_phase(datasets, evolution_generations)

            # Phase 2: Optimization
            self.run_optimization_phase(datasets, optimization_iterations)

            # Final report
            self.generate_final_report()

            # Success
            total_time = time.time() - pipeline_start
            print()
            print("="*70)
            print("   ✅ PIPELINE COMPLETE")
            print("="*70)
            print(f"\nTotal time: {total_time/60:.1f} minutes")
            print()
            print("🎉 Your datasets have been fully optimized with AI!")
            print()

        except KeyboardInterrupt:
            print("\n\n❌ Pipeline interrupted by user")
            print("Partial results may be available in workflow/auto_results/")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="Automated pipeline: AI Evolution + AI Reflection"
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["1_peaceful_village", "2_small_town", "3_suburbia"],
        help="Datasets to process (default: 1, 2, 3)"
    )
    parser.add_argument(
        "--evolution-generations",
        type=int,
        default=2,
        help="Generations for AI solver evolution (default: 2)"
    )
    parser.add_argument(
        "--optimization-iterations",
        type=int,
        default=50,
        help="Max iterations for optimization phase (default: 50)"
    )
    parser.add_argument(
        "--all-datasets",
        action="store_true",
        help="Process all 6 datasets (overrides --datasets)"
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
        print("❌ Error: ANTHROPIC_API_KEY not set in .env")
        print("AI features require API access.")
        sys.exit(1)

    # Determine datasets
    if args.all_datasets:
        datasets = [
            "1_peaceful_village",
            "2_small_town",
            "3_suburbia",
            "4_epitech",
            "5_isogrid",
            "6_manhattan"
        ]
    else:
        datasets = args.datasets

    # Run pipeline
    pipeline = AutoPipeline(api_key, continue_from_existing=args.continue_from_existing)
    pipeline.run(
        datasets=datasets,
        evolution_generations=args.evolution_generations,
        optimization_iterations=args.optimization_iterations
    )


if __name__ == "__main__":
    main()
