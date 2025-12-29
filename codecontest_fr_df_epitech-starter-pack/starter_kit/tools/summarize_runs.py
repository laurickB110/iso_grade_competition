#!/usr/bin/env python3
"""
Summarize experiment runs and generate reports per dataset.

Usage:
    python tools/summarize_runs.py
    python tools/summarize_runs.py --dataset 1_peaceful_village
"""
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict


def load_runs(runs_log_path: Path) -> List[Dict]:
    """Load all runs from runs.jsonl"""
    runs = []
    if not runs_log_path.exists():
        return runs

    with open(runs_log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    runs.append(json.loads(line))
                except:
                    pass
    return runs


def summarize_dataset(dataset_name: str, runs: List[Dict], output_path: Path):
    """Generate summary markdown for a dataset"""

    # Filter runs for this dataset
    dataset_runs = [r for r in runs if r['dataset'] == dataset_name]

    if not dataset_runs:
        return

    # Separate valid and invalid runs
    valid_runs = [r for r in dataset_runs if r['valid']]
    invalid_runs = [r for r in dataset_runs if not r['valid']]

    # Sort valid runs by cost (ascending)
    valid_runs.sort(key=lambda r: r['cost'])

    # Collect invalid reasons
    invalid_reasons = Counter()
    for r in invalid_runs:
        msg = r.get('message', 'Unknown error')
        # Truncate long messages
        if len(msg) > 100:
            msg = msg[:100] + '...'
        invalid_reasons[msg] += 1

    # Generate markdown
    lines = []
    lines.append(f'# Experiment Summary: {dataset_name}')
    lines.append('')
    lines.append(f'**Total runs:** {len(dataset_runs)}')
    lines.append(f'**Valid solutions:** {len(valid_runs)}')
    lines.append(f'**Invalid solutions:** {len(invalid_runs)}')
    lines.append('')

    if valid_runs:
        best = valid_runs[0]
        lines.append(f'**Best cost:** {best["cost"]:,}')
        lines.append(f'**Best method:** {best["method"]}')
        lines.append(f'**Best seed:** {best["seed"]}')
        if best.get('stats'):
            lines.append(f'**Best antennas:** {best["stats"]["nb_antennas"]}')
        lines.append('')

    # Top 10 valid runs
    if valid_runs:
        lines.append('## Top 10 Valid Solutions')
        lines.append('')
        lines.append('| Rank | Cost | Method | Seed | Antennas | On Building % | Avg Buildings/Antenna | Runtime (s) |')
        lines.append('|------|------|--------|------|----------|---------------|-----------------------|-------------|')

        for i, run in enumerate(valid_runs[:10], 1):
            method = run['method'].split('.')[-1].replace(':solve', '')
            stats = run.get('stats', {})
            nb_antennas = stats.get('nb_antennas', 'N/A')
            on_building = stats.get('percent_on_building', 'N/A')
            avg_buildings = stats.get('avg_buildings_per_antenna', 'N/A')
            runtime = run.get('runtime_sec', 'N/A')

            lines.append(f'| {i} | {run["cost"]:,} | {method} | {run["seed"]} | {nb_antennas} | {on_building} | {avg_buildings} | {runtime} |')

        lines.append('')

    # Method comparison
    if valid_runs:
        lines.append('## Method Comparison')
        lines.append('')

        method_stats = defaultdict(lambda: {'costs': [], 'runtimes': []})
        for run in valid_runs:
            method = run['method']
            method_stats[method]['costs'].append(run['cost'])
            method_stats[method]['runtimes'].append(run.get('runtime_sec', 0))

        lines.append('| Method | Runs | Best Cost | Avg Cost | Median Cost | Avg Runtime (s) |')
        lines.append('|--------|------|-----------|----------|-------------|-----------------|')

        for method in sorted(method_stats.keys()):
            stats = method_stats[method]
            costs = sorted(stats['costs'])
            runtimes = stats['runtimes']

            method_short = method.split('.')[-1].replace(':solve', '')
            num_runs = len(costs)
            best_cost = costs[0]
            avg_cost = sum(costs) / len(costs)
            median_cost = costs[len(costs) // 2]
            avg_runtime = sum(runtimes) / len(runtimes) if runtimes else 0

            lines.append(f'| {method_short} | {num_runs} | {best_cost:,} | {avg_cost:,.0f} | {median_cost:,} | {avg_runtime:.2f} |')

        lines.append('')

    # Invalid reasons
    if invalid_reasons:
        lines.append('## Top Invalid Reasons')
        lines.append('')
        lines.append('| Count | Reason |')
        lines.append('|-------|--------|')

        for reason, count in invalid_reasons.most_common(5):
            lines.append(f'| {count} | {reason} |')

        lines.append('')

    # Antenna type usage (from best solution)
    if valid_runs:
        best = valid_runs[0]
        stats = best.get('stats')
        if stats and stats.get('type_counts'):
            lines.append('## Antenna Type Usage (Best Solution)')
            lines.append('')
            lines.append('| Type | Count |')
            lines.append('|------|-------|')

            for atype, count in sorted(stats['type_counts'].items()):
                lines.append(f'| {atype} | {count} |')

            lines.append('')

    # Write to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description='Summarize experiment runs')
    parser.add_argument('--dataset', type=str, default=None, help='Summarize specific dataset only (default: all)')
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    runs_log = base_dir / 'experiments' / 'runs.jsonl'

    if not runs_log.exists():
        print('No runs found. Run experiments first with tools/run_experiment.py')
        return 1

    # Load all runs
    print('Loading runs...')
    runs = load_runs(runs_log)
    print(f'Loaded {len(runs)} runs')

    if not runs:
        print('No valid runs found in log')
        return 1

    # Get unique datasets
    datasets = sorted(set(r['dataset'] for r in runs))
    print(f'Found {len(datasets)} datasets: {", ".join(datasets)}')

    # Generate summaries
    experiments_dir = base_dir / 'experiments'
    experiments_dir.mkdir(exist_ok=True)

    if args.dataset:
        # Single dataset
        if args.dataset in datasets:
            output_path = experiments_dir / f'summary_{args.dataset}.md'
            print(f'Generating summary for {args.dataset}...')
            summarize_dataset(args.dataset, runs, output_path)
            print(f'Summary written to: {output_path}')
        else:
            print(f'Dataset {args.dataset} not found in runs')
            return 1
    else:
        # All datasets
        for dataset in datasets:
            output_path = experiments_dir / f'summary_{dataset}.md'
            print(f'Generating summary for {dataset}...')
            summarize_dataset(dataset, runs, output_path)
            print(f'  -> {output_path}')

    print('Done!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
