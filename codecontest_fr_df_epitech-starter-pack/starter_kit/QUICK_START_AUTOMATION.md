# Quick Start - Automated Workflow

## 🚀 Launch in 3 Steps

### 1. Configure Your Target Scores

Open `workflow/config.yaml` and set your target scores for each dataset:

```yaml
target_scores:
  1_peaceful_village: 25000      # ← Change these values
  2_small_town: 100000
  3_suburbia: 5000000
  4_epitech: 10000000
  5_isogrid: 15000000
  6_manhattan: 20000000
```

**This is the ONLY file you need to edit to get started.**

### 2. Run the Workflow

```bash
./GO.sh
```

Or for a quick test (1 small dataset, 3 iterations):

```bash
./GO.sh --test
```

Or directly with Python:

```bash
python3 workflow/go.py
```

### 3. Check Results

- **Best solutions**: `solutions/best/<dataset>.json`
- **Detailed report**: `workflow/workspace/final_report.json`
- **Console output**: Shows real-time progress

---

## 📋 What Happens Automatically

✅ Runs solver iteratively on all datasets
✅ Tracks best solutions and scores
✅ Analyzes progress trends
✅ Stops when targets are reached
✅ Stops when max iterations reached
✅ Saves all improvements
✅ Generates final report

---

## 🎯 How to Set Good Targets

### Strategy 1: Conservative (Recommended for First Run)

Run once without targets to see what's achievable:

```yaml
target_scores:
  1_peaceful_village: null  # No target = unlimited iterations
```

Then set targets based on results.

### Strategy 2: Competitive

Check competition leaderboard and set targets 10-20% better than current position.

### Strategy 3: Iterative

Start conservative, then progressively lower targets after each successful run.

---

## ⚙️ Configuration File Location

**File**: `workflow/config.yaml`

**What to configure**:

| Setting | Description | Default |
|---------|-------------|---------|
| `target_scores` | Goal cost per dataset | See file |
| `active_datasets` | Which datasets to process | All |
| `max_iterations` | Max iterations per dataset | 50 |
| `seeds_per_iteration` | Parallel runs per iteration | 5 |

**Example**: Only process 2 datasets with custom targets

```yaml
target_scores:
  3_suburbia: 5000000
  4_epitech: 10000000

active_datasets:
  - 3_suburbia
  - 4_epitech

max_iterations: 100
seeds_per_iteration: 10
```

---

## 🛑 When the Workflow Stops

The workflow automatically stops for each dataset when:

1. **Target reached**: Best cost ≤ target score (✓ shown in output)
2. **Max iterations**: Hit the iteration limit
3. **Timeout**: Exceeded time limit (if configured)
4. **User interrupt**: Ctrl+C (can resume later)

---

## 📊 Understanding Output

```
Iteration 1 (seeds: 5)... Best: 145,230 | Avg: 152,401
```

- **Iteration**: Current optimization cycle
- **seeds**: Number of parallel runs
- **Best**: Best cost found this iteration
- **Avg**: Average cost across all seeds

```
1_peaceful_village    21,000 ✓       5      0.2s
```

- ✓ = Target reached
- 5 = Iterations completed
- 0.2s = Time spent

---

## 🔧 Optional: AI Reflection

To enable AI-powered analysis when progress stagnates:

1. Install Anthropic SDK:
```bash
pip install anthropic
```

2. Configure API key:
```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-...
```

3. Enable in config:
```yaml
enable_ai_reflection: true
```

AI will analyze performance and suggest improvements when progress slows.

---

## 📁 Output Files

```
solutions/
└── best/
    ├── 1_peaceful_village.json  ← Latest best solutions
    ├── 2_small_town.json
    └── ...

workflow/
└── workspace/
    ├── workflow_state.json      ← Current state (for resume)
    ├── run_history.jsonl        ← Detailed logs
    └── final_report.json        ← Summary report
```

---

## 💡 Tips

### Speed Up Exploration
```yaml
max_iterations: 20
seeds_per_iteration: 3
solver_params:
  iterations: 500
```

### Maximize Quality
```yaml
max_iterations: 100
seeds_per_iteration: 10
solver_params:
  iterations: 2000
```

### Focus on One Dataset
```yaml
active_datasets:
  - 5_isogrid
```

---

## 🆘 Troubleshooting

**Problem**: Workflow doesn't stop at target

**Solution**: Check dataset name spelling in `target_scores` matches exactly (including file extension).

---

**Problem**: Slow performance

**Solution**:
- Reduce `seeds_per_iteration` from 5 to 3
- Reduce `solver_params.iterations` from 1000 to 500
- Process fewer datasets at once

---

**Problem**: Want to resume after interrupt

**Solution**: Just run `./GO.sh` again. State is preserved in `workflow/workspace/`.

---

## 📚 Full Documentation

For complete details, see:
- **README_AUTOMATION.md**: Complete workflow documentation
- **workflow/config.yaml**: All configuration options with comments

---

## 🎯 Example Session

```bash
# 1. Set targets
vim workflow/config.yaml  # Edit target_scores

# 2. Launch
./GO.sh

# 3. Watch progress
# Iteration 1 (seeds: 5)... Best: 145,230 | Avg: 152,401
# Iteration 2 (seeds: 5)... Best: 138,920 | Avg: 143,105
# ...
# ✓ Target reached!

# 4. Check results
cat workflow/workspace/final_report.json
ls -l solutions/best/
```

---

**Ready? Just run:**

```bash
./GO.sh
```

Good luck! 🚀
