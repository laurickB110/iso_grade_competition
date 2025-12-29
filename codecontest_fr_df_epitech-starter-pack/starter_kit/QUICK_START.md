# Quick Start Guide

## Setup (One-time)

```bash
cd starter_kit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Essential Commands

### Score a Solution
```bash
python3 tools/score_one.py --dataset 1_peaceful_village --solution solutions/best/1_peaceful_village.json
```

### Run Single Experiment
```bash
python3 tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 20
```

### Run Multiple Datasets
```bash
for dataset in 1_peaceful_village 2_small_town 3_suburbia 4_epitech 5_isogrid 6_manhattan; do
  python3 tools/run_experiment.py \
    --dataset $dataset \
    --method methods.baseline_place_on_buildings:solve \
    --seeds 10
done
```

### Generate Summaries
```bash
python3 tools/summarize_runs.py
cat experiments/summary_1_peaceful_village.md
```

### Compare Methods
```bash
# Run baseline
python3 tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.baseline_place_on_buildings:solve \
  --seeds 20

# Run randomized greedy
python3 tools/run_experiment.py \
  --dataset 1_peaceful_village \
  --method methods.randomized_greedy:solve \
  --seeds 20 \
  --params '{"ordering":"random"}'

# Compare results
python3 tools/summarize_runs.py --dataset 1_peaceful_village
cat experiments/summary_1_peaceful_village.md
```

## Best Solutions Location

Best solutions are saved in:
- `solutions/best/<dataset>.json` - Latest best solution
- `solutions/best/solution_<dataset>_<cost>.json` - Timestamped best solutions

Submit these JSON files to the contest platform!
