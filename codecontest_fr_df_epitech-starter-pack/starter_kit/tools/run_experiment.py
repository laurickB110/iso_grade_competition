#!/usr/bin/env python3
"""
Run experiments with different solvers, seeds, and parameters.

Usage:
    python tools/run_experiment.py --dataset 1_peaceful_village --method methods.baseline_place_on_buildings:solve --seeds 20
    python tools/run_experiment.py --dataset datasets/2_small_town.json --method methods.randomized_greedy:solve --seeds 10 --params '{"ordering":"random"}'
"""
import argparse
import json
import sys
import time
import importlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from score_function import getSolutionScore


def load_solver(method_spec: str):
    """
    Load solver function from module:function specification.

    Args:
        method_spec: String like "methods.baseline_place_on_buildings:solve"

    Returns:
        Callable solver function
    """
    try:
        module_name, function_name = method_spec.split(':')
        module = importlib.import_module(module_name)
        solver = getattr(module, function_name)
        return solver
    except Exception as e:
        raise ValueError(f'Failed to load solver {method_spec}: {e}')


def compute_solution_stats(solution: dict, dataset: dict) -> Dict[str, Any]:
    """
    Compute statistics about a solution.

    Returns:
        Dict with stats: nb_antennas, type_counts, percent_on_building, avg_buildings_per_antenna
    """
    antennas = solution.get('antennas', [])

    if not antennas:
        return {
            'nb_antennas': 0,
            'type_counts': {},
            'percent_on_building': 0.0,
            'avg_buildings_per_antenna': 0.0
        }

    # Count antenna types
    type_counts = {}
    for antenna in antennas:
        atype = antenna.get('type', 'Unknown')
        type_counts[atype] = type_counts.get(atype, 0) + 1

    # Check how many antennas are on building coordinates
    building_positions = {(b['x'], b['y']) for b in dataset['buildings']}
    on_building_count = sum(1 for a in antennas if (a['x'], a['y']) in building_positions)
    percent_on_building = (on_building_count / len(antennas) * 100) if antennas else 0.0

    # Average buildings per antenna
    total_assignments = sum(len(a.get('buildings', [])) for a in antennas)
    avg_buildings = total_assignments / len(antennas) if antennas else 0.0

    return {
        'nb_antennas': len(antennas),
        'type_counts': type_counts,
        'percent_on_building': round(percent_on_building, 1),
        'avg_buildings_per_antenna': round(avg_buildings, 1)
    }


def main():
    parser = argparse.ArgumentParser(description='Run experiments with different solvers')
    parser.add_argument('--dataset', required=True, help='Dataset path or name (e.g., "1_peaceful_village")')
    parser.add_argument('--method', required=True, help='Method specification (e.g., "methods.baseline:solve")')
    parser.add_argument('--seeds', type=int, default=20, help='Number of seeds to run (default: 20)')
    parser.add_argument('--time_limit', type=int, default=None, help='Time limit per run in seconds (optional)')
    parser.add_argument('--params', type=str, default='{}', help='JSON string of method parameters (default: "{}")')
    parser.add_argument('--outdir', type=str, default=None, help='Output directory (default: solutions/runs/<dataset>/<method>)')
    args = parser.parse_args()

    # Resolve dataset path
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        # Try as dataset name
        base_dir = Path(__file__).parent.parent
        dataset_path = base_dir / 'datasets' / f'{args.dataset}.json'
        if not dataset_path.exists():
            print(f'ERROR: Dataset not found: {args.dataset}', file=sys.stderr)
            return 1

    # Extract dataset name
    dataset_name = dataset_path.stem

    # Parse parameters
    try:
        params = json.loads(args.params)
    except Exception as e:
        print(f'ERROR: Invalid params JSON: {e}', file=sys.stderr)
        return 1

    # Load dataset
    try:
        with open(dataset_path, 'r') as f:
            dataset_txt = f.read()
            dataset = json.loads(dataset_txt)
    except Exception as e:
        print(f'ERROR: Failed to load dataset: {e}', file=sys.stderr)
        return 1

    # Load solver
    try:
        solver = load_solver(args.method)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 1

    # Setup output directories
    base_dir = Path(__file__).parent.parent
    if args.outdir:
        outdir = Path(args.outdir)
    else:
        method_name = args.method.replace(':', '_').replace('.', '_')
        outdir = base_dir / 'solutions' / 'runs' / dataset_name / method_name

    outdir.mkdir(parents=True, exist_ok=True)

    # Setup experiments log
    experiments_dir = base_dir / 'experiments'
    experiments_dir.mkdir(exist_ok=True)
    runs_log = experiments_dir / 'runs.jsonl'

    # Best solution tracking
    best_dir = base_dir / 'solutions' / 'best'
    best_dir.mkdir(parents=True, exist_ok=True)

    # Load current best cost for this dataset if it exists
    best_cost = float('inf')
    best_link = best_dir / f'{dataset_name}.json'
    if best_link.exists():
        try:
            with open(best_link, 'r') as f:
                best_solution = json.load(f)
            best_cost_result, _, _ = getSolutionScore(json.dumps(best_solution), dataset_txt)
            if best_cost_result > 0:
                best_cost = best_cost_result
        except:
            pass

    print(f'Dataset: {dataset_name} ({len(dataset["buildings"])} buildings)')
    print(f'Method: {args.method}')
    print(f'Seeds: {args.seeds}')
    print(f'Params: {json.dumps(params)}')
    print(f'Current best cost: {best_cost:,}' if best_cost != float('inf') else 'Current best cost: None')
    print('-' * 80)

    # Run experiments
    for seed in range(args.seeds):
        run_start = time.time()

        try:
            # Call solver
            solution = solver(dataset, seed=seed, params=params)

            # Validate it's a dict with antennas key
            if not isinstance(solution, dict) or 'antennas' not in solution:
                raise ValueError('Solver did not return dict with "antennas" key')

            solution_txt = json.dumps(solution)

            # Score the solution
            cost, valid, message = getSolutionScore(solution_txt, dataset_txt)

            runtime = time.time() - run_start

            # Compute stats
            stats = compute_solution_stats(solution, dataset)

            # Save solution
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            solution_filename = f'{timestamp}_seed{seed}.json'
            solution_path = outdir / solution_filename

            with open(solution_path, 'w') as f:
                json.dump(solution, f, indent=2)

            # Log to runs.jsonl
            log_entry = {
                'timestamp': timestamp,
                'dataset': dataset_name,
                'method': args.method,
                'seed': seed,
                'params': params,
                'valid': valid,
                'cost': cost,
                'message': message,
                'solution_path': str(solution_path.relative_to(base_dir)),
                'runtime_sec': round(runtime, 2),
                'stats': stats
            }

            with open(runs_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

            # Update best solution if this is better
            if valid and cost < best_cost:
                best_cost = cost
                best_filename = f'solution_{dataset_name}_{cost}.json'
                best_path = best_dir / best_filename

                with open(best_path, 'w') as f:
                    json.dump(solution, f, indent=2)

                # Update symlink/stable file
                if best_link.exists():
                    best_link.unlink()
                best_link.write_text(json.dumps(solution, indent=2))

                status = f'VALID (NEW BEST!)'
            elif valid:
                status = f'VALID'
            else:
                status = f'INVALID'

            # Print progress
            cost_str = f'{cost:,}' if valid else 'N/A'
            print(f'[{seed+1:3d}/{args.seeds}] {status:20s} | Cost: {cost_str:>12s} | Antennas: {stats["nb_antennas"]:4d} | Time: {runtime:5.2f}s')

        except Exception as e:
            runtime = time.time() - run_start

            # Log exception
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_entry = {
                'timestamp': timestamp,
                'dataset': dataset_name,
                'method': args.method,
                'seed': seed,
                'params': params,
                'valid': False,
                'cost': 0,
                'message': f'EXCEPTION: {str(e)}',
                'solution_path': None,
                'runtime_sec': round(runtime, 2),
                'stats': None
            }

            with open(runs_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

            print(f'[{seed+1:3d}/{args.seeds}] EXCEPTION            | {str(e)[:50]}')

    print('-' * 80)
    print(f'Experiments complete. Best cost: {best_cost:,}' if best_cost != float('inf') else 'No valid solutions found.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
