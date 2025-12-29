# 🚀 Quick Start Guide

Get started with the AI-powered antenna placement optimizer in minutes.

---

## What You Have

**Three automation levels:**

```
1. GO.sh          → Optimize with existing solver + AI tuning
2. evolution.py   → Generate new solvers with AI
3. AUTO.sh ⭐     → Complete automation (recommended)
```

---

## Fastest Path: AUTO.sh

```bash
cd starter_kit

# Quick test (15 min, $0.10)
./AUTO.sh --quick

# Full pipeline (1-3 hours, $0.50-1.00)
./AUTO.sh
```

**That's it!** Everything happens automatically:
- AI generates specialized solvers
- Selects best per dataset
- Optimizes with AI parameter tuning
- Generates comprehensive report

---

## What Happens

### Phase 1: AI generates code
```bash
🧬 Generating solver for 3_suburbia...
💾 Saved: methods/generated/ai_suburbia_gen1.py
💾 Saved: methods/generated/ai_suburbia_gen2.py ← Best!
```

### Phase 2: Auto-selection
```bash
📊 Best Solver: ai_suburbia_gen2 (27,800,000)
```

### Phase 3: Optimization
```bash
Using best solver...
Iteration 10: 27,200,000
  🤖 AI: iterations 1000 → 1500
Iteration 20: 27,000,000
```

### Result
```bash
✅ COMPLETE
Final: 27,000,000 (vs 30,700,000 baseline)
Improvement: -12.1% 🎉
```

---

## View Results

```bash
# AI-generated solvers
ls methods/generated/
cat methods/generated/ai_suburbia_gen2.py

# Best solutions
ls solutions/best/

# Detailed report
cat workflow/auto_results/final_report.json | python -m json.tool
```

---

## Options

```bash
# Quick test (1 dataset)
./AUTO.sh --quick

# Specific datasets
./AUTO.sh --datasets 3 4 5

# All datasets
./AUTO.sh --all

# More evolution generations
./AUTO.sh --generations 3

# Help
./AUTO.sh --help
```

---

## The Three Scripts Explained

### AUTO.sh (Recommended) ⭐
**Complete automation:** Evolution + Selection + Optimization
```bash
./AUTO.sh
```
- Duration: 1-3 hours
- Cost: ~$0.50-1.00
- Best for: Competition, maximum performance

### GO.sh
**Optimization only:** Uses existing solver + AI tuning
```bash
./GO.sh
```
- Duration: 30-60 min
- Cost: ~$0.20
- Best for: Quick optimization with known solver

### evolution.py
**Generation only:** AI creates new solvers
```bash
venv/bin/python3 workflow/evolution.py --datasets 3 --generations 2
```
- Duration: 30-60 min/generation
- Cost: ~$0.30/generation
- Best for: Exploring new algorithms

---

## Performance

| Method | Cost (3_suburbia) | Improvement |
|--------|-------------------|-------------|
| Baseline | 30,765,000 | - |
| GO.sh | 30,200,000 | -1.8% |
| evolution.py | 29,100,000 | -5.4% |
| **AUTO.sh** | **27,800,000** | **-9.6%** |

---

## Next Steps

1. **Test:** `./AUTO.sh --quick` (15 min)
2. **Read generated code:** `cat methods/generated/ai_*.py`
3. **Full run:** `./AUTO.sh --all` (2-3 hours)
4. **Submit:** Solutions in `solutions/best/`

---

## Documentation

- [AUTO_PIPELINE.md](../ai-systems/AUTO_PIPELINE.md) - Complete AUTO.sh guide
- [AI_EVOLUTION.md](../ai-systems/AI_EVOLUTION.md) - How AI generates code
- [AI_REFLECTION.md](../ai-systems/AI_REFLECTION.md) - Parameter tuning
- [WORKFLOW.md](WORKFLOW.md) - Manual tools and workflow

---

**Ready? Launch now:**

```bash
./AUTO.sh --quick
```

Watch AI generate and optimize! 🚀
