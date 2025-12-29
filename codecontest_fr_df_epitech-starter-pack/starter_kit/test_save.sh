#!/bin/bash
#
# TEST SCRIPT - Verify solutions are saved correctly
#
# This script tests that the fix works by running a quick optimization
# and verifying that solutions are saved properly.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================================"
echo "🧪 TESTING SOLUTION SAVE FIX"
echo "========================================================================"
echo ""
echo "This will:"
echo "  1. Run a quick optimization on dataset 1 (15-30 seconds)"
echo "  2. Verify that solutions are saved correctly"
echo "  3. Report success or failure"
echo ""

# Clean up previous test solutions
echo "📁 Cleaning up previous test solutions..."
rm -f solutions/best/1_peaceful_village.json
rm -f solutions/solution_1_peaceful_village_*.json

# Run quick optimization
echo ""
echo "🚀 Running quick test optimization..."
echo ""

# Use GO.sh directly with dataset 1, just 3 iterations
if [ ! -d "venv" ]; then
    echo "⚙️  Setting up virtual environment..."
    python3 -m venv venv
    venv/bin/pip install -q --upgrade pip
    venv/bin/pip install -q -r requirements.txt
fi

# Create test config
cat > workflow/test_config.yaml << 'EOF'
target_scores:
  1_peaceful_village: 21000

active_datasets:
  - 1_peaceful_village

max_iterations: 3
seeds_per_iteration: 2

analysis_window: 2
min_improvement_threshold: 0.5
stagnation_limit: 2
max_reflection_cycles: 1

max_runtime_seconds: 0
max_runtime_per_dataset: 0

solver_method: "solver:optimized_solution"

solver_params:
  iterations: 100

save_run_logs: true
save_all_solutions: false
generate_reports: true
verbosity: 1

enable_ai_reflection: false
auto_apply_suggestions: false
EOF

echo "Running optimization (3 iterations)..."
venv/bin/python3 workflow/go.py workflow/test_config.yaml

# Check results
echo ""
echo "========================================================================"
echo "📊 VERIFICATION RESULTS"
echo "========================================================================"
echo ""

SUCCESS=true

# Check if best solution was saved
if [ -f "solutions/best/1_peaceful_village.json" ]; then
    echo "✅ solutions/best/1_peaceful_village.json created"
else
    echo "❌ solutions/best/1_peaceful_village.json NOT FOUND"
    SUCCESS=false
fi

# Check if timestamped backup was saved
BACKUP_COUNT=$(ls solutions/solution_1_peaceful_village_*.json 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 0 ]; then
    echo "✅ Timestamped backup created (found $BACKUP_COUNT file(s))"
    ls -lh solutions/solution_1_peaceful_village_*.json | tail -1
else
    echo "❌ No timestamped backup found"
    SUCCESS=false
fi

# Verify solution is valid
if [ -f "solutions/best/1_peaceful_village.json" ]; then
    COST=$(python3 -c "
import json
from score_function import getSolutionScore

dataset = json.load(open('datasets/1_peaceful_village.json'))
solution = json.load(open('solutions/best/1_peaceful_village.json'))
cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))

if valid:
    print(f'{cost}')
    exit(0)
else:
    print('INVALID')
    exit(1)
" 2>&1)

    if [ "$COST" != "INVALID" ]; then
        echo "✅ Solution is valid with cost: $COST"
    else
        echo "❌ Solution is INVALID"
        SUCCESS=false
    fi
fi

echo ""
echo "========================================================================"
if [ "$SUCCESS" = true ]; then
    echo "✅ TEST PASSED - Solution save fix is working correctly!"
    echo ""
    echo "🎉 You can now safely run long optimizations:"
    echo "   ./AUTO.sh --datasets 3 4 --generations 3 --iterations 100 --auto-approve"
else
    echo "❌ TEST FAILED - Something is wrong with solution saving"
    echo ""
    echo "⚠️  DO NOT run long optimizations until this is fixed!"
fi
echo "========================================================================"
echo ""

# Cleanup
rm -f workflow/test_config.yaml

exit 0
