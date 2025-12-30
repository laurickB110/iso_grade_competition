#!/bin/bash
#
# CHECK PROGRESS - Quick status without attaching to tmux
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     📊 OPTIMIZATION PROGRESS CHECK               ║${NC}"
echo -e "${BLUE}╔═══════════════════════════════════════════════════╝${NC}"
echo ""

# Check if tmux session exists
if tmux has-session -t optim 2>/dev/null; then
    echo -e "${GREEN}✅ Optimization is RUNNING in tmux session 'optim'${NC}"
    echo ""
else
    echo -e "${RED}❌ No tmux session 'optim' found${NC}"
    echo "The optimization is not running or has finished."
    echo ""
    exit 1
fi

# Check recent solutions
echo -e "${YELLOW}📁 Recent solutions:${NC}"
ls -lht solutions/solution_*_suburbia_*.json 2>/dev/null | head -3
ls -lht solutions/solution_*_epitech_*.json 2>/dev/null | head -3
echo ""

# Check best solutions
echo -e "${YELLOW}🏆 Current best solutions:${NC}"
if [ -f "solutions/best/3_suburbia.json" ]; then
    COST_3=$(python3 -c "
import json
from score_function import getSolutionScore
dataset = json.load(open('datasets/3_suburbia.json'))
solution = json.load(open('solutions/best/3_suburbia.json'))
cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
print(f'{cost:,}' if valid else 'INVALID')
" 2>/dev/null)
    TARGET_3="26,855,000"
    echo "  3_suburbia: ${COST_3} (target: ${TARGET_3})"
fi

if [ -f "solutions/best/4_epitech.json" ]; then
    COST_4=$(python3 -c "
import json
from score_function import getSolutionScore
dataset = json.load(open('datasets/4_epitech.json'))
solution = json.load(open('solutions/best/4_epitech.json'))
cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
print(f'{cost:,}' if valid else 'INVALID')
" 2>/dev/null)
    TARGET_4="30,315,000"
    echo "  4_epitech:  ${COST_4} (target: ${TARGET_4})"
fi

echo ""

# Check generated solvers
SOLVER_COUNT=$(ls methods/generated/ai_*.py 2>/dev/null | wc -l)
echo -e "${YELLOW}🧬 Generated solvers: ${SOLVER_COUNT}${NC}"

# Check auto results
if [ -f "workflow/auto_results/evolution_summary.json" ]; then
    echo ""
    echo -e "${YELLOW}📈 Evolution summary:${NC}"
    python3 -c "
import json
try:
    with open('workflow/auto_results/evolution_summary.json') as f:
        data = json.load(f)
        gens = data.get('generations', 'N/A')
        datasets = data.get('datasets', [])
        print(f'  Generations completed: {gens}')
        print(f'  Datasets: {len(datasets)}')
except:
    print('  Unable to read summary')
" 2>/dev/null
fi

echo ""
echo -e "${BLUE}Commands:${NC}"
echo "  tmux attach -t optim    # View live progress"
echo "  Ctrl+B then D           # Detach from tmux"
echo "  ./check_progress.sh     # Run this script again"
echo ""
