# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a competitive optimization framework for a 5G antenna placement contest. The goal is to place antennas to cover all buildings in various city datasets while minimizing total installation cost. Solutions are submitted as JSON files (not code), and the platform keeps the best score per dataset.

## Problem Domain

**Objective**: Minimize total cost of antenna installation while satisfying all constraints.

**Key Constraints**:
- Every building must be assigned to exactly one antenna
- Buildings can only be assigned to antennas within range (Euclidean distance ≤ antenna.range)
- Antenna capacity must handle the peak load: max(sum(peak), sum(off_peak), sum(night)) across all assigned buildings
- Antennas cost less when placed exactly on building coordinates
- Multiple antennas can share the same coordinates

**Antenna Types** (defined in score_function.py:31-36):
- Nano: range=50, capacity=200, cost=5k/6k (on/off building)
- Spot: range=100, capacity=800, cost=15k/20k
- Density: range=150, capacity=5000, cost=30k/50k
- MaxRange: range=400, capacity=3500, cost=40k/50k

**Solution Format**:
```json
{
  "antennas": [
    {
      "type": "Spot",
      "x": 150,
      "y": 200,
      "buildings": [0, 3, 7]
    }
  ]
}
```

## Repository Structure

```
starter_kit/
├── datasets/           # 6 city datasets (1-6)
│   ├── 1_peaceful_village.json
│   ├── 2_small_town.json
│   ├── 3_suburbia.json      (large: ~450KB)
│   ├── 4_epitech.json       (large: ~870KB)
│   ├── 5_isogrid.json       (very large: ~1.4MB)
│   └── 6_manhattan.json     (very large: ~1.7MB)
├── solutions/          # Generated solutions
├── score_function.py   # Official scoring logic (do not modify)
├── starter_kit.py      # Naive baseline example
└── question.md         # Problem statement (French)
```

## Core Commands

### Score a Solution
```bash
cd starter_kit
python3 -c "
import json
from score_function import getSolutionScore

dataset = json.load(open('datasets/1_peaceful_village.json'))
solution = json.load(open('solutions/solution_1_peaceful_village_150000.json'))
cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
print(f'Valid: {valid}, Cost: {cost}, Message: {msg}')
"
```

### Run Baseline Solution
```bash
cd starter_kit
python3 starter_kit.py
```
This generates a naive solution placing one Density antenna per building.

## Architecture Notes

### Scoring Function (score_function.py)
- `getSolutionScore(solution_txt, dataset_txt)` returns `(cost, is_valid, message)`
- This is the exact server-side validation logic
- Returns cost=0 and is_valid=False for any constraint violation
- Checks performed:
  1. JSON structure validation
  2. All buildings covered exactly once (no duplicates, no missing)
  3. Distance constraints (Euclidean distance ≤ range)
  4. Capacity constraints (max period load ≤ capacity)
  5. Valid antenna types and coordinates (non-negative integers)

### Dataset Format
Each dataset JSON contains:
```json
{
  "comment": "...",
  "buildings": [
    {
      "id": 0,
      "x": 100,
      "y": 250,
      "populationPeakHours": 500,
      "populationOffPeakHours": 150,
      "populationNight": 50
    }
  ]
}
```

## Development Workflow

When implementing new solvers or optimization algorithms:

1. **Precompute building demands**: For each building, calculate `max_demand = max(peak, off_peak, night)` upfront
2. **Use deterministic randomness**: Seed with `random.Random(seed)` or `np.random.default_rng(seed)` for reproducibility
3. **Validate solutions**: Always validate with score_function.py before considering a solution valid
4. **Handle edge cases**: Ensure all buildings are assigned; fall back to MaxRange antennas if needed
5. **Coordinate matching**: Check if `(antenna_x, antenna_y)` exactly matches any building coordinates for cost discount

## Important Invariants

- **Do not modify**: score_function.py (server validation logic), datasets/, question.md
- **Backward compatibility**: starter_kit.py must remain functional
- **Integer coordinates**: All x, y values must be non-negative integers
- **Distance calculation**: Use exact formula `distance = sqrt((x_a - x_b)² + (y_a - y_b)²)`
- **Capacity check**: Must satisfy `max(Σpeak, Σoff_peak, Σnight) ≤ antenna.capacity` for each antenna

## Performance Considerations

- Datasets 1-2: Small (~10-25 buildings), suitable for exhaustive search
- Datasets 3-4: Medium (~1k-3k buildings), require efficient heuristics
- Datasets 5-6: Large (~5k-7k buildings), require scalable algorithms
- Memory: Large datasets fit in memory; avoid redundant copies
- Precompute: Building coordinates, demand arrays, distance matrices for small instances

## Common Pitfalls

- Forgetting that capacity constraint checks the MAX across all three periods (not sum)
- Not checking for exact coordinate match when calculating antenna cost
- Allowing buildings to be assigned to multiple antennas
- Using floating-point coordinates instead of integers
- Exceeding antenna range due to floating-point precision errors
- Not seeding random generators, leading to non-reproducible results
