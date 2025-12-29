#!/usr/bin/env python3
"""
Score a single solution against a dataset using the official score_function.

Usage:
    python tools/score_one.py --dataset <path> --solution <path>
    python tools/score_one.py --dataset 1_peaceful_village --solution solutions/best/1_peaceful_village.json
"""
import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import score_function
sys.path.insert(0, str(Path(__file__).parent.parent))
from score_function import getSolutionScore


def main():
    parser = argparse.ArgumentParser(description='Score a solution against a dataset')
    parser.add_argument('--dataset', required=True, help='Dataset path or name (e.g., "1_peaceful_village" or full path)')
    parser.add_argument('--solution', required=True, help='Solution JSON path')
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

    # Resolve solution path
    solution_path = Path(args.solution)
    if not solution_path.is_absolute():
        solution_path = Path(__file__).parent.parent / solution_path

    if not solution_path.exists():
        print(f'ERROR: Solution not found: {args.solution}', file=sys.stderr)
        return 1

    # Load files
    try:
        with open(dataset_path, 'r') as f:
            dataset_txt = f.read()
            dataset = json.loads(dataset_txt)
    except Exception as e:
        print(f'ERROR: Failed to load dataset: {e}', file=sys.stderr)
        return 1

    try:
        with open(solution_path, 'r') as f:
            solution_txt = f.read()
            solution = json.loads(solution_txt)
    except Exception as e:
        print(f'ERROR: Failed to load solution: {e}', file=sys.stderr)
        return 1

    # Score the solution
    cost, valid, message = getSolutionScore(solution_txt, dataset_txt)

    # Print concise result
    dataset_name = dataset_path.stem
    status = 'VALID' if valid else 'INVALID'
    if valid:
        print(f'{status} | {dataset_name} | Cost: {cost:,} | Antennas: {len(solution.get("antennas", []))}')
    else:
        print(f'{status} | {dataset_name} | {message}')

    return 0 if valid else 1


if __name__ == '__main__':
    sys.exit(main())
