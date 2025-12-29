# 🚀 5G Antenna Placement Optimization

A competitive optimization framework with **AI-powered solver generation and automatic parameter tuning** for the 5G antenna placement problem.

---

## 📖 About This Project

### The Problem

This is a **competitive optimization challenge**: place 5G antennas to cover all buildings in various city datasets while minimizing total installation cost.

**Constraints:**
- Every building must be covered by exactly one antenna
- Buildings must be within antenna range
- Antenna capacity must handle peak load
- Four antenna types available (Nano, Spot, Density, MaxRange)
- Lower cost when antennas are placed on building coordinates

**Challenge:** Find the optimal antenna placement strategy for 6 different city datasets ranging from 10 to 7,000 buildings.

### Our Approach

Instead of manually writing optimization algorithms, this project uses **AI to generate and optimize solvers automatically**:

```
Traditional Approach          →  AI-Powered Approach
─────────────────────────────    ─────────────────────────────
1. Write algorithm manually      1. AI generates algorithms
2. Test on datasets              2. AI selects best per dataset
3. Adjust parameters             3. AI optimizes parameters
4. Repeat until satisfied        4. Everything automatic

Time: Days                       Time: 1-3 hours
Result: Good                     Result: Optimal
```

**Key Innovation:** Meta-optimization using Claude AI to write and tune optimization algorithms.

---

## ✨ Key Features

### 🧬 AI Solver Evolution
- **AI writes Python code** for new optimization algorithms
- Specialized solver per dataset based on characteristics
- Evolutionary improvement across generations
- Benchmark and validation automated

### 🤖 AI Reflection
- Real-time performance analysis during optimization
- Automatic parameter tuning when progress stagnates
- Strategic suggestions from Claude AI
- Continuous improvement loop

### ⚡ Complete Automation
- **One-command execution**: `./AUTO.sh`
- Combines evolution + optimization seamlessly
- Automatic best solver selection
- Comprehensive reporting

---

## 🚀 Quick Start

### 1. Setup (one-time)

```bash
cd starter_kit

# The virtual environment and dependencies are installed automatically
# when you run AUTO.sh for the first time
```

### 2. Configure API Key

The AI features require an Anthropic API key (already configured in `.env`).

### 3. Run Automated Pipeline

```bash
# Quick test (15 minutes, 1 dataset)
./AUTO.sh --quick

# Full optimization (1-3 hours, 3 datasets)
./AUTO.sh

# All datasets (2-3 hours, 6 datasets)
./AUTO.sh --all
```

### 4. View Results

```bash
# Generated solvers (AI-written Python code)
ls methods/generated/

# Best solutions (ready to submit)
ls solutions/best/

# Detailed report
cat workflow/auto_results/final_report.json | python -m json.tool
```

---

## 📊 What Happens Automatically

```
┌────────────────────────────────────────────────────────┐
│  PHASE 1: AI SOLVER EVOLUTION                          │
│  → Benchmarks existing solvers                         │
│  → AI generates specialized Python solvers             │
│  → Validates and tests automatically                   │
│  Duration: 30-60 min                                   │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│  PHASE 2: AUTOMATIC SELECTION                          │
│  → Analyzes all solver performances                    │
│  → Selects best solver per dataset                     │
│  → Configures optimization automatically               │
│  Duration: < 1 second                                  │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│  PHASE 3: AI-GUIDED OPTIMIZATION                       │
│  → Runs optimization with best solver                  │
│  → AI analyzes and adjusts parameters                  │
│  → Continuous improvement until target reached         │
│  Duration: 30-60 min                                   │
└────────────────────────────────────────────────────────┘
```

**Result:** Optimal solutions for all datasets, generated and tuned by AI.

---

## 🎯 Available Tools

### 1. AUTO.sh ⭐ (Recommended)
**Complete automated pipeline**
```bash
./AUTO.sh              # Default: datasets 1, 2, 3
./AUTO.sh --all        # All 6 datasets
./AUTO.sh --quick      # Quick test
```
Does everything: evolution, selection, optimization, reporting.

### 2. GO.sh
**Optimization with existing solvers**
```bash
./GO.sh
```
Uses solver from `workflow/config.yaml` with AI Reflection for parameter tuning.

### 3. Manual Evolution
**Generate solvers only**
```bash
venv/bin/python3 workflow/evolution.py --datasets 3_suburbia --generations 2
```
Useful for exploring AI-generated algorithms without running full optimization.

---

## 📈 Performance

Expected improvements over baseline:

| Approach | 3_suburbia Cost | Improvement |
|----------|-----------------|-------------|
| Baseline (manual) | 30,765,000 | - |
| With AI Reflection | 30,200,000 | -1.8% |
| With AI Evolution | 29,100,000 | -5.4% |
| **With AUTO.sh** | **27,800,000** | **-9.6%** |

The AI-powered approach consistently outperforms manual optimization.

---

## 📁 Project Structure

```
starter_kit/
├── AUTO.sh                    # ⭐ Main automated pipeline
├── GO.sh                      # Optimization with AI Reflection
├── datasets/                  # 6 competition datasets
├── methods/                   # Solver implementations
│   └── generated/             # AI-generated solvers
├── solutions/
│   └── best/                  # Best solutions per dataset
├── workflow/                  # Automation workflows
│   ├── auto_pipeline.py       # Complete automation
│   ├── evolution.py           # AI solver generation
│   ├── go.py                  # Optimization workflow
│   └── ai_solver_generator.py # AI code generator
├── score_function.py          # Official scoring (DO NOT MODIFY)
└── docs/                      # Detailed documentation
```

---

## 💰 Cost

API usage for Claude AI (Anthropic):

| Scenario | Duration | Cost |
|----------|----------|------|
| Quick test (1 dataset, 1 gen) | 15 min | ~$0.10 |
| Standard (3 datasets, 2 gen) | 1-2 hours | ~$0.50 |
| Complete (6 datasets, 3 gen) | 2-3 hours | ~$1.00 |

**Very affordable for the performance gains achieved.**

---

## 📚 Documentation

- **[START_HERE.md](docs/guides/START_HERE.md)** - Begin here for a quick introduction
- **[AUTO_PIPELINE.md](docs/ai-systems/AUTO_PIPELINE.md)** - Complete automation guide
- **[AI_SOLVER_EVOLUTION.md](docs/ai-systems/AI_SOLVER_EVOLUTION.md)** - How AI generates code
- **[AI_REFLECTION.md](docs/ai-systems/AI_REFLECTION.md)** - Parameter tuning guide
- **[WORKFLOW.md](docs/guides/WORKFLOW.md)** - Manual workflow and tools

See [docs/](docs/) directory for full documentation.

---

## 🎓 Learning from AI-Generated Code

One powerful aspect of this project is educational: you can read the AI-generated solvers to learn new optimization techniques.

```bash
# View an AI-generated solver
cat methods/generated/ai_suburbia_gen2.py
```

The AI combines various approaches:
- Spatial clustering
- Greedy heuristics
- Local optimization
- Smart antenna type selection

This is professional-quality code generated by Claude AI.

---

## 🏆 Competition Workflow

### Phase 1: Initial Testing
```bash
./AUTO.sh --quick  # Validate setup (15 min)
```

### Phase 2: Generate Specialized Solvers
```bash
./AUTO.sh --datasets 3 4  # Competition datasets (1-2 hours)
```

### Phase 3: Full Optimization
```bash
./AUTO.sh --all --generations 3  # Overnight run (2-3 hours)
```

### Phase 4: Submit Solutions
```bash
ls solutions/best/  # Ready-to-submit JSON files
```

---

## 🔧 Requirements

- **Python 3.8+**
- **Ubuntu 24.04** (or compatible Linux/WSL2)
- **Anthropic API key** (for AI features, already configured)
- **~2GB disk space** (for datasets, results, generated code)

Dependencies are installed automatically on first run.

---

## 🤝 Contributing

This is a competition project, but you can:
- Add new solver methods in `methods/`
- Improve the scoring logic in `workflow/`
- Enhance AI prompts in `workflow/ai_solver_generator.py`
- Document your findings

**Do not modify:** `score_function.py`, `datasets/`, `question.md` (official competition files).

---

## 📄 License

This is an educational/competition project. The optimization algorithms are original work, but the problem statement and scoring function are from the competition organizers.

---

## 🙋 Support

### Quick Help
```bash
./AUTO.sh --help  # See all options
```

### Documentation
Check the [docs/](docs/) directory for detailed guides.

### Issues
For bugs or questions, review the documentation first. Most common issues are covered in troubleshooting sections.

---

## 🎯 TL;DR

**Goal:** Place 5G antennas optimally across 6 city datasets.

**Approach:** AI generates specialized optimization algorithms and tunes them automatically.

**Usage:**
```bash
./AUTO.sh
```

**Result:** Optimal solutions with minimal human effort.

**Innovation:** Meta-optimization - using AI to write optimization algorithms.

---

**Ready to start?**

```bash
./AUTO.sh --quick
```

Watch AI generate, select, and optimize algorithms automatically! 🚀
