# Competitive Optimization Workflow

This document describes the experimentation workflow for the 5G antenna placement optimization contest.

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Project Structure](#project-structure)
4. [Quick Start](#quick-start)
5. [Running Experiments](#running-experiments)
6. [Viewing Results](#viewing-results)
7. [Adding New Solvers](#adding-new-solvers)
8. [WSL2 Notes](#wsl2-notes)

---

## Overview

This workflow allows you to:
- Run multiple solver implementations with different seeds and parameters
- Automatically score solutions using the official `score_function.py`
- Track best solutions per dataset
- Log all experiment results for analysis
- Generate summaries comparing methods

**Important:** We submit JSON solution files (not code). The platform keeps the best score per dataset.

---

## Setup

### Prerequisites

- Python 3.8 or higher
- Ubuntu 24.04 or WSL2 Ubuntu
- No internet required after setup

### Installation

1. Create a virtual environment:
```bash
cd starter_kit
python3 -m venv venv
source venv/bin/activate  # On Windows WSL: same command
```

2. Install dependencies (currently none required for baseline):
```bash
pip install -r requirements.txt
```

3. Verify setup by running the original starter kit:
```bash
python starter_kit.py
```

This should generate a solution in `solutions/` and display the cost.

---

## Project Structure

```
starter_kit/
├── datasets/                    # Contest datasets (DO NOT MODIFY)
│   ├── 1_peaceful_village.json
│   ├── 2_small_town.json
│   ├── 3_suburbia.json
│   ├── 4_epitech.json
│   ├── 5_isogrid.json
│   └── 6_manhattan.json
├── methods/                     # Solver implementations
│   ├── __init__.py
│   ├── base.py                  # Base interface and utilities
│   ├── baseline_place_on_buildings.py
│   └── randomized_greedy.py
├── tools/                       # Orchestration tools
│   ├── __init__.py
│   ├── score_one.py             # Score a single solution
│   ├── run_experiment.py        # Run experiments with seeds
│   └── summarize_runs.py        # Generate summaries
├── experiments/                 # Experiment logs and summaries
│   ├── runs.jsonl               # All runs (append-only log)
│   └── summary_*.md             # Generated summaries per dataset
├── solutions/
│   ├── best/                    # Best solution per dataset
│   │   ├── solution_1_peaceful_village_*.json
│   │   └── 1_peaceful_village.json  # Symlink to current best
│   └── runs/                    # All runs organized by dataset/method
│       └── <dataset>/<method>/<timestamp>_seed*.json
├── score_function.py            # Official scoring (DO NOT MODIFY)
├── starter_kit.py               # Original naive solution (preserved)
├── question.md                  # Problem statement (DO NOT MODIFY)
├── requirements.txt             # Python dependencies
└── README_WORKFLOW.md           # This file
```

---

## Quick Start

### 1. Score an Existing Solution

```bash
python tools/score_one.py \
  --dataset 1_peaceful_village \
  --solution solutions/solution_1_peaceful_village_150000.json
```

**Output:**
```
VALID | 1_peaceful_village | Cost: 150,000 | Antennas: 10
```

### 2. Run a Single Experiment

Run the baseline method with 5 seeds:

```bash
python tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 5
```

**Output:**
```
Dataset: 1_peaceful_village (10 buildings)
Method: methods.baseline_place_on_buildings:solve
Seeds: 5
Params: {}
Current best cost: 150,000
--------------------------------------------------------------------------------
[  1/  5] VALID (NEW BEST!)  | Cost:      120,000 | Antennas:    8 | Time:  0.05s
[  2/  5] VALID              | Cost:      120,000 | Antennas:    8 | Time:  0.04s
[  3/  5] VALID              | Cost:      120,000 | Antennas:    8 | Time:  0.04s
[  4/  5] VALID              | Cost:      120,000 | Antennas:    8 | Time:  0.04s
[  5/  5] VALID              | Cost:      120,000 | Antennas:    8 | Time:  0.04s
--------------------------------------------------------------------------------
Experiments complete. Best cost: 120,000
```

### 3. Generate Summary

```bash
python tools/summarize_runs.py
```

This generates `experiments/summary_1_peaceful_village.md` with:
- Top 10 solutions
- Method comparison
- Invalid run analysis
- Antenna type usage

---

## Running Experiments

### Basic Usage

```bash
python tools/run_experiment.py \
  --dataset <dataset_name> \
  --method <module:function> \
  --seeds <number>
```

### Examples

**Run baseline on dataset 1:**
```bash
python tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 20
```

**Run randomized greedy with custom parameters:**
```bash
python tools/run_experiment.py \
  --dataset 2_small_town \
  --method methods.randomized_greedy:solve \
  --seeds 20 \
  --params '{"ordering":"random","radius_factor":1.2}'
```

**Run on large dataset:**
```bash
python tools/run_experiment.py \
  --dataset 6_manhattan \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 5
```

### Available Parameters for `randomized_greedy`

- `ordering`: `"max"` (default), `"peak"`, or `"random"` - How to sort buildings
- `radius_factor`: Float (default 1.0) - Multiplier for antenna range when searching candidates
- `attempt_rebalance`: Boolean (default false) - Enable local improvement pass

**Example:**
```bash
python tools/run_experiment.py \
  --dataset 3_suburbia \
  --method methods.randomized_greedy:solve \
  --seeds 50 \
  --params '{"ordering":"random","radius_factor":1.5,"attempt_rebalance":true}'
```

### Running Multiple Datasets

Use a bash loop:

```bash
for dataset in 1_peaceful_village 2_small_town 3_suburbia 4_epitech 5_isogrid 6_manhattan; do
  echo "=== Running $dataset ==="
  python tools/run_experiment.py \
    --dataset $dataset \
    --method methods.baseline_place_on_buildings:solve \
    --seeds 10
done
```

After all runs:
```bash
python tools/summarize_runs.py
```

---

## Viewing Results

### Best Solutions

Best solutions are stored in `solutions/best/`:

```bash
# View best solution for dataset 1
cat solutions/best/1_peaceful_village.json

# Score it
python tools/score_one.py \
  --dataset 1_peaceful_village \
  --solution solutions/best/1_peaceful_village.json
```

### Experiment Logs

All runs are logged to `experiments/runs.jsonl` (one JSON object per line).

**View last 10 runs:**
```bash
tail -n 10 experiments/runs.jsonl | python -m json.tool
```

**Filter valid runs for a dataset:**
```bash
grep '"dataset": "1_peaceful_village"' experiments/runs.jsonl | \
  grep '"valid": true' | \
  python -m json.tool
```

### Summaries

Generate and view summaries:

```bash
# Generate all summaries
python tools/summarize_runs.py

# View summary for dataset 1
cat experiments/summary_1_peaceful_village.md

# Generate summary for specific dataset only
python tools/summarize_runs.py --dataset 6_manhattan
```

Summaries include:
- Top 10 valid solutions ranked by cost
- Method comparison (best, average, median costs)
- Invalid run reasons
- Antenna type usage

---

## Adding New Solvers

### 1. Create Solver Module

Create a new file in `methods/`, e.g., `methods/my_solver.py`:

```python
"""
My custom solver description.
"""
from .base import SolverResult, ANTENNA_TYPES, get_building_demand, is_in_range


def solve(dataset: dict, *, seed: int, params: dict = None) -> SolverResult:
    """
    Solver implementation.

    Args:
        dataset: Dict with 'buildings' key
        seed: Random seed for reproducibility
        params: Optional parameters dict

    Returns:
        SolverResult dict with 'antennas' key
    """
    if params is None:
        params = {}

    buildings = dataset['buildings']
    antennas = []

    # Your algorithm here
    # ...

    return {'antennas': antennas}
```

### 2. Use Helper Functions

The `base.py` module provides:

- `ANTENNA_TYPES`: Dict of antenna specifications
- `ANTENNA_TYPES_BY_CAPACITY`: List of types sorted by capacity
- `ANTENNA_TYPES_BY_RANGE`: List of types sorted by range
- `get_building_demand(building)`: Get max demand across periods
- `distance(x1, y1, x2, y2)`: Euclidean distance
- `distance_squared(x1, y1, x2, y2)`: Squared distance (faster)
- `is_in_range(antenna_x, antenna_y, building_x, building_y, range)`: Check coverage

### 3. Test Your Solver

```bash
python tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.my_solver:solve \
  --seeds 5
```

### 4. Iterate and Compare

```bash
# Run multiple methods
python tools/run_experiment.py --dataset 1_peaceful_village --method methods.baseline_place_on_buildings:solve --seeds 20
python tools/run_experiment.py --dataset 1_peaceful_village --method methods.my_solver:solve --seeds 20

# Compare
python tools/summarize_runs.py --dataset 1_peaceful_village
cat experiments/summary_1_peaceful_village.md
```

---

## WSL2 Notes

### Running in WSL2

This workflow is fully compatible with WSL2 Ubuntu. Follow the same setup steps.

**Important:** Keep your repository in the Linux filesystem (not `/mnt/c/...`) for best performance:

```bash
# Good: Linux filesystem
/home/username/epitech/codecontest_fr_df_epitech-starter-pack/

# Avoid: Windows filesystem (slow)
/mnt/c/Users/username/Documents/epitech/...
```

### Accessing Files from Windows

Your Linux filesystem is accessible from Windows at:
```
\\wsl$\Ubuntu\home\username\epitech\codecontest_fr_df_epitech-starter-pack
```

You can open this in VS Code, Explorer, or any editor.

### Python Setup in WSL2

```bash
# Install Python if needed
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Verify version
python3 --version  # Should be 3.8+

# Continue with setup steps above
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'methods'"

Make sure you're running commands from the `starter_kit/` directory:

```bash
cd starter_kit
python tools/run_experiment.py ...
```

### "Dataset not found"

Use dataset name without `.json` extension:

```bash
# Correct
python tools/run_experiment.py --dataset 1_peaceful_village ...

# Also correct (full path)
python tools/run_experiment.py --dataset datasets/1_peaceful_village.json ...
```

### "INVALID: Building X is covered by multiple antennas"

Your solver assigned the same building to multiple antennas. Each building must be assigned exactly once.

### Large datasets run slowly

This is expected. Datasets 5-6 have 5,000-7,000 buildings. Reduce `--seeds` for testing:

```bash
python tools/run_experiment.py \
  --dataset 6_manhattan \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 3  # Instead of 20
```

---

## Best Practices

1. **Always use seeds:** Ensures reproducibility of results
2. **Start small:** Test on dataset 1 before running on large datasets
3. **Log everything:** The `runs.jsonl` log is append-only and preserves all history
4. **Compare methods:** Use summaries to identify which approaches work best
5. **Iterate quickly:** Run 5-10 seeds for testing, 20+ for final evaluation
6. **Check validity:** Invalid solutions have cost=0; fix errors before scaling up
7. **Track best solutions:** Best solutions are automatically saved in `solutions/best/`

---

## Example: Complete Workflow

```bash
# 1. Setup
cd starter_kit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Test original starter_kit still works
python starter_kit.py

# 3. Run baseline on dataset 1
python tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 20

# 4. Run randomized greedy
python tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.randomized_greedy:solve \
  --seeds 20 \
  --params '{"ordering":"random"}'

# 5. Compare methods
python tools/summarize_runs.py --dataset 1_peaceful_village
cat experiments/summary_1_peaceful_village.md

# 6. Run best method on all datasets
for dataset in 1_peaceful_village 2_small_town 3_suburbia 4_epitech 5_isogrid 6_manhattan; do
  python tools/run_experiment.py \
    --dataset $dataset \
    --method methods.baseline_place_on_buildings:solve \
    --seeds 10
done

# 7. Generate summaries for all datasets
python tools/summarize_runs.py

# 8. View best solutions
ls -lh solutions/best/
```

---

## Next Steps

1. Study the baseline solvers in `methods/`
2. Implement your own solver following the interface in `methods/base.py`
3. Experiment with different parameters using `--params`
4. Run experiments on all datasets
5. Submit best solutions (JSON files) to the contest platform
6. Iterate based on results

Good luck!
