# 📚 Documentation Index

Complete documentation for the AI-powered 5G antenna placement optimizer.

---

## 🚀 Getting Started

**New to the project?** Start here:

1. **[../README.md](../README.md)** - Project overview and context
2. **[guides/QUICK_START.md](guides/QUICK_START.md)** - Get running in 15 minutes
3. **[ai-systems/AUTO_PIPELINE.md](ai-systems/AUTO_PIPELINE.md)** - Complete automation guide

---

## 📖 Documentation Structure

### Guides (How-To)
Essential guides for using the system:

- **[QUICK_START.md](guides/QUICK_START.md)** - Fastest path to running the optimizer
- **[WORKFLOW.md](guides/WORKFLOW.md)** - Manual workflow and tools reference

### AI Systems (Deep Dive)
Understanding the AI automation:

- **[AUTO_PIPELINE.md](ai-systems/AUTO_PIPELINE.md)** - Complete AUTO.sh pipeline guide
- **[AI_EVOLUTION.md](ai-systems/AI_EVOLUTION.md)** - How AI generates solver code
- **[AI_REFLECTION.md](ai-systems/AI_REFLECTION.md)** - Automatic parameter tuning

### Reference (Technical)
Technical references for developers:

- **[SOLVER_DEVELOPMENT.md](reference/SOLVER_DEVELOPMENT.md)** - Creating custom solvers
- **[../question.md](../question.md)** - Original problem statement (French)
- **[../score_function.py](../score_function.py)** - Scoring logic reference

---

## 🎯 By Use Case

### "I want to run the optimizer now"
→ [guides/QUICK_START.md](guides/QUICK_START.md)

### "I want to understand the full automation"
→ [ai-systems/AUTO_PIPELINE.md](ai-systems/AUTO_PIPELINE.md)

### "I want to see how AI generates code"
→ [ai-systems/AI_EVOLUTION.md](ai-systems/AI_EVOLUTION.md)

### "I want to write my own solver"
→ [reference/SOLVER_DEVELOPMENT.md](reference/SOLVER_DEVELOPMENT.md)

### "I want to understand the competition problem"
→ [../question.md](../question.md) (French)

---

## 📊 By Tool

### AUTO.sh
- Overview: [../README.md](../README.md#-available-tools)
- Complete guide: [ai-systems/AUTO_PIPELINE.md](ai-systems/AUTO_PIPELINE.md)
- Quick start: [guides/QUICK_START.md](guides/QUICK_START.md#fastest-path-autosh)

### GO.sh
- Overview: [../README.md](../README.md#2-gosh)
- Workflow: [guides/WORKFLOW.md](guides/WORKFLOW.md)

### evolution.py
- Overview: [../README.md](../README.md#3-manual-evolution)
- Complete guide: [ai-systems/AI_EVOLUTION.md](ai-systems/AI_EVOLUTION.md)

---

## 🎓 Learning Path

### Beginner
1. Read [../README.md](../README.md) - Understand the problem
2. Run `./AUTO.sh --quick` - See it in action (15 min)
3. Read [guides/QUICK_START.md](guides/QUICK_START.md) - Understand what happened

### Intermediate
1. Read [ai-systems/AUTO_PIPELINE.md](ai-systems/AUTO_PIPELINE.md) - Full pipeline
2. Read [ai-systems/AI_EVOLUTION.md](ai-systems/AI_EVOLUTION.md) - Code generation
3. Examine generated code: `cat methods/generated/ai_*.py`

### Advanced
1. Read [reference/SOLVER_DEVELOPMENT.md](reference/SOLVER_DEVELOPMENT.md)
2. Study existing solvers in `methods/`
3. Create custom solver and test
4. Integrate with AUTO.sh workflow

---

## 🔍 Quick Reference

### Commands
```bash
./AUTO.sh            # Complete automation
./AUTO.sh --quick    # Quick test
./AUTO.sh --all      # All datasets
./GO.sh              # Optimization only
venv/bin/python3 workflow/evolution.py  # Generation only
```

### File Locations
```
methods/generated/      # AI-generated solvers
solutions/best/         # Best solutions
workflow/auto_results/  # AUTO.sh results
workflow/evolution_results/  # Evolution results
```

### Configuration
```
.env                           # API key (already configured)
workflow/config.yaml           # Workflow settings
```

---

## 🆘 Troubleshooting

### Setup Issues
→ [guides/QUICK_START.md](guides/QUICK_START.md) - Setup section

### AUTO.sh Problems
→ [ai-systems/AUTO_PIPELINE.md](ai-systems/AUTO_PIPELINE.md) - Troubleshooting section

### Evolution Issues
→ [ai-systems/AI_EVOLUTION.md](ai-systems/AI_EVOLUTION.md) - Troubleshooting section

### Solver Development
→ [reference/SOLVER_DEVELOPMENT.md](reference/SOLVER_DEVELOPMENT.md)

---

## 📝 Document Status

- ✅ Consolidated and organized
- ✅ Redundancy removed
- ✅ Clear navigation structure
- ✅ Cross-referenced

Last updated: 2025-12-29
