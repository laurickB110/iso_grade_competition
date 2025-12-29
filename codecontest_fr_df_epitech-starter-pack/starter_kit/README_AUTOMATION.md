# Automated Workflow - GO

Complete automation system for iterative solver optimization with AI-powered reflection.

## Overview

This workflow provides a **single "GO" command** that automatically:

1. ✅ Runs the solver iteratively on all datasets
2. 📊 Tracks and analyzes results in real-time
3. 🎯 Stops automatically when targets are reached
4. 🤖 Triggers AI reflection when progress stagnates (optional)
5. 📝 Generates detailed reports and saves best solutions

**Philosophy**: CPU does the heavy optimization work, LLM makes strategic decisions.

---

## Quick Start

### 1. Install Dependencies

```bash
# Core dependencies (if not already installed)
pip install pyyaml

# Optional: For AI reflection
pip install anthropic
```

### 2. Configure Targets

Edit `workflow/config.yaml` to set your target scores:

```yaml
target_scores:
  1_peaceful_village: 25000
  2_small_town: 100000
  3_suburbia: 5000000
  # ... etc
```

**This is the ONLY configuration you need to modify to get started.**

### 3. Launch the Workflow

```bash
python workflow/go.py
```

That's it! The workflow will run until targets are reached or limits exceeded.

---

## How It Works

### Execution Flow

```
┌─────────────────────────────────────────────────┐
│  START: Load config and initialize              │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  For each dataset:         │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  Run iteration             │
         │  (multiple seeds)          │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  Analyze results           │
         │  - Track best cost         │
         │  - Detect trends           │
         │  - Calculate improvement   │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  Make decision:            │
         │  - Target reached? → STOP  │
         │  - Max iterations? → STOP  │
         │  - Stagnant? → REFLECT     │
         │  - Improving? → CONTINUE   │
         └────────────┬───────────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
            ▼                   ▼
      [CONTINUE]           [REFLECT]
         │                     │
         │                     ▼
         │          ┌────────────────────┐
         │          │ AI analyzes data   │
         │          │ Suggests changes   │
         │          └─────────┬──────────┘
         │                    │
         └────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  Next dataset or STOP      │
         └────────────────────────────┘
```

### Stopping Conditions

The workflow stops for a dataset when ANY of these conditions are met:

1. **Target Reached**: Best cost ≤ target score
2. **Max Iterations**: Reached `max_iterations` (default: 50)
3. **Max Reflections**: Used all reflection cycles (default: 3)
4. **Timeout**: Exceeded `max_runtime_per_dataset` (if set)

---

## Configuration Guide

### Essential Configuration: `workflow/config.yaml`

#### 1. Target Scores (REQUIRED)

```yaml
target_scores:
  1_peaceful_village: 25000      # Set your goal for each dataset
  2_small_town: 100000
  3_suburbia: 5000000
  4_epitech: 10000000
  5_isogrid: 15000000
  6_manhattan: 20000000
```

**How to set targets:**
- Start conservative based on initial runs
- Adjust based on competition leaderboard
- Set `null` to disable target checking for a dataset
- Workflow stops when `best_cost <= target`

#### 2. Active Datasets

```yaml
active_datasets:
  - 1_peaceful_village
  - 2_small_town
  # Comment out datasets you don't want to process
```

Leave empty `[]` to process all datasets.

#### 3. Iteration Control

```yaml
max_iterations: 50              # Max iterations per dataset
seeds_per_iteration: 5          # Parallel runs per iteration
```

**Tuning tips:**
- More iterations = more exploration, longer runtime
- More seeds = better sampling, slower iterations
- Start with 50 iterations / 5 seeds

#### 4. Decision Thresholds

```yaml
analysis_window: 5                 # Iterations to analyze
min_improvement_threshold: 0.5     # Minimum % improvement
stagnation_limit: 10               # Iterations before reflecting
```

#### 5. Solver Configuration

```yaml
solver_method: "solver:optimized_solution"

solver_params:
  iterations: 1000    # Local optimization iterations
```

You can also use alternative solvers:
- `"methods.baseline_place_on_buildings:solve"`
- `"methods.randomized_greedy:solve"`

#### 6. AI Reflection (OPTIONAL)

```yaml
enable_ai_reflection: true
ai_model: "claude-sonnet-4-5-20250929"
auto_apply_suggestions: false
```

**To enable AI reflection:**
1. Set `enable_ai_reflection: true`
2. Install: `pip install anthropic`
3. Set API key: `cp .env.example .env` and edit `.env`
4. Add your key: `ANTHROPIC_API_KEY=sk-ant-...`

---

## Understanding Output

### Console Output

```
==================================================================
PROCESSING: 2_small_town
==================================================================
Target score: 100,000

  Iteration 1 (seeds: 5)... Best: 145,230 | Avg: 152,401
  Iteration 2 (seeds: 5)... Best: 138,920 | Avg: 143,105
  Iteration 3 (seeds: 5)... Best: 132,450 | Avg: 138,230
  ...

==================================================================
DECISION: TARGET_REACHED
Dataset: 2_small_town
Best cost: 98,340
Target: 100,000 (gap: -1,660 / -1.7%)
Reason: Target score 100,000 reached with 98,340
==================================================================
```

### Files Generated

```
workflow/
├── workspace/
│   ├── workflow_state.json      # Current state (resume from here)
│   ├── run_history.jsonl        # Detailed run logs
│   └── final_report.json        # Summary report
│
solutions/
└── best/
    ├── 1_peaceful_village.json  # Latest best solution
    ├── 2_small_town.json
    └── ...
```

### Progress Tracking

The workflow maintains state in `workflow/workspace/workflow_state.json`:

```json
{
  "datasets": {
    "2_small_town": {
      "iteration": 15,
      "best_cost": 98340,
      "best_iteration": 12,
      "reflection_count": 1,
      "history": [...]
    }
  }
}
```

---

## AI Reflection Phase

### What Happens During Reflection

When progress stagnates, the workflow can trigger AI analysis:

1. **Gathers Context**:
   - Current best cost and target
   - Recent iteration history (scores, trends)
   - Current solver parameters
   - Performance analysis

2. **Calls Claude API**:
   - Analyzes bottlenecks
   - Suggests parameter tuning
   - Recommends strategy changes

3. **Applies Suggestions**:
   - Auto-apply (if `auto_apply_suggestions: true`)
   - Or asks for user confirmation

4. **Continues Optimization**:
   - Resumes with updated parameters
   - Tracks improvement from changes

### Implementing AI Reflection

The template is provided in `workflow/reflection_template.py`.

To integrate into `go.py`:

```python
from workflow.reflection_template import reflect_with_claude, apply_suggestions

def _reflect_and_improve(self, dataset_name: str) -> bool:
    state = self.tracker.get_dataset_state(dataset_name)
    analysis = self.tracker.analyze_progress(dataset_name, window=10)

    suggestions = reflect_with_claude(
        dataset_name, state, analysis, self.config
    )

    if suggestions:
        return apply_suggestions(
            suggestions,
            self.config,
            auto_apply=self.config.get("auto_apply_suggestions", False)
        )

    return False
```

**Security Note**: Never commit API keys! Use `.env` (gitignored).

---

## Advanced Usage

### Run Specific Datasets

```bash
# Edit config.yaml
active_datasets:
  - 3_suburbia
  - 4_epitech

# Then run
python workflow/go.py
```

### Custom Configuration

```bash
python workflow/go.py --config my_custom_config.yaml
```

### Resume After Interruption

The workflow saves state continuously. Just run again:

```bash
python workflow/go.py
```

It will resume from the last completed iteration.

### Parallel Processing (Future Enhancement)

Currently, seeds within an iteration run sequentially. To parallelize:

```python
# In go.py, replace sequential loop with:
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(self._run_solver_iteration, ...)
        for seed in range(seeds_count)
    ]
    results = [f.result() for f in futures]
```

---

## Monitoring and Analysis

### Real-time Status

The workflow prints progress after each iteration:

```
Iteration 5 (seeds: 5)... Best: 142,330 | Avg: 148,205
```

### Final Report

After completion, check:

```bash
cat workflow/workspace/final_report.json
```

Contains:
- Best costs per dataset
- Iteration counts
- Improvement trends
- Reflection analysis

### Best Solutions

All best solutions are saved to:

```
solutions/best/<dataset>.json
```

These are automatically updated whenever a better solution is found.

---

## Troubleshooting

### Workflow Doesn't Stop

**Symptom**: Keeps running past target

**Check**:
1. Target score is set in `config.yaml`
2. Best cost is actually <= target
3. No typos in dataset name

### AI Reflection Not Working

**Symptom**: Skips reflection or errors

**Check**:
1. `enable_ai_reflection: true` in config
2. `ANTHROPIC_API_KEY` set in `.env`
3. `anthropic` package installed: `pip install anthropic`
4. API key is valid (starts with `sk-ant-`)

### Invalid Solutions

**Symptom**: "NO VALID SOLUTIONS!" message

**Possible causes**:
1. Solver bug (check `solver.py`)
2. Dataset corruption
3. Scoring function mismatch

**Debug**:
```bash
# Test solver directly
python starter_kit.py
```

### Slow Performance

**Symptom**: Each iteration takes too long

**Solutions**:
1. Reduce `seeds_per_iteration` (try 3 instead of 5)
2. Reduce `solver_params.iterations` (try 500 instead of 1000)
3. Start with smaller datasets
4. Implement parallel processing (see Advanced Usage)

---

## Architecture

### Component Overview

```
workflow/
├── config.yaml              # User configuration
├── go.py                    # Main orchestrator
├── tracker.py               # Run history & analysis
├── analyzer.py              # Decision logic
└── reflection_template.py   # AI reflection (optional)
```

### Design Principles

1. **Separation of Concerns**:
   - `go.py`: Orchestration only
   - `tracker.py`: Data management
   - `analyzer.py`: Decision logic
   - `solver.py`: Optimization (existing)

2. **CPU vs LLM**:
   - CPU: Heavy computation (solver iterations)
   - LLM: Strategic decisions (parameter tuning, bottleneck analysis)

3. **State Management**:
   - Persistent state in `workflow_state.json`
   - Resume-friendly design
   - No data loss on interrupt

4. **Extensibility**:
   - Easy to add new solvers
   - Pluggable reflection strategies
   - Configurable stopping conditions

---

## Performance Tips

### For Fast Iteration

```yaml
max_iterations: 20
seeds_per_iteration: 3
solver_params:
  iterations: 500
```

### For Best Quality

```yaml
max_iterations: 100
seeds_per_iteration: 10
solver_params:
  iterations: 2000
```

### For Overnight Runs

```yaml
max_iterations: 200
max_runtime_per_dataset: 3600  # 1 hour per dataset
enable_ai_reflection: true
```

---

## Integration with Claude Code

This workflow is designed to work seamlessly with Claude Code:

```bash
# Let Claude Code orchestrate everything
claude code "Run the automated workflow and optimize all datasets"

# Or run directly
python workflow/go.py
```

Claude Code acts as the **architect**, not a worker:
- Analyzes results
- Makes strategic decisions
- Suggests code improvements
- **Does not** run computationally expensive tasks

---

## Contributing

When adding features, maintain these principles:

1. **Keep `config.yaml` simple** - It's the user interface
2. **CPU for compute, LLM for strategy** - Don't use API calls in tight loops
3. **Save state frequently** - Support interruption/resume
4. **Clear stopping conditions** - Users should know when/why it stops
5. **Document configuration** - Every config option needs explanation

---

## FAQ

**Q: How long does it take to run?**
A: Depends on datasets and config. Small datasets: minutes. Large datasets: hours. Use `max_runtime_per_dataset` to limit.

**Q: Can I run multiple workflows in parallel?**
A: Not recommended (shared state). Run sequentially or use different directories.

**Q: Do I need AI reflection?**
A: No, it's optional. The workflow works fine without it. AI helps when stuck.

**Q: What if I don't have API key?**
A: Set `enable_ai_reflection: false`. Workflow runs normally without AI.

**Q: How do I know if my targets are realistic?**
A: Start with conservative estimates. The workflow will show you the best achievable costs. Adjust targets based on results.

**Q: Can I modify the solver during execution?**
A: No, changes require restart. Use AI reflection to adjust parameters without code changes.

**Q: What happens if I interrupt (Ctrl+C)?**
A: State is saved. Resume by running again. No progress lost.

---

## Summary

### The GO workflow provides:

✅ **Single command execution** - `python workflow/go.py`
✅ **Automatic target detection** - Stops when goals met
✅ **Progress tracking** - Real-time monitoring
✅ **AI-powered optimization** - Optional reflection phase
✅ **Resume capability** - Interrupt-safe design
✅ **Best solution tracking** - Always saves improvements
✅ **Detailed reporting** - JSON exports for analysis

### Configuration is simple:

📝 Edit `workflow/config.yaml` to set targets
🎯 Define your goals per dataset
🚀 Run and let it optimize automatically

---

**Ready to GO?**

```bash
python workflow/go.py
```

Good luck! 🚀
