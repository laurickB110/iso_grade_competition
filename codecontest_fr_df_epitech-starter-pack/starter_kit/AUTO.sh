#!/bin/bash
#
# AUTO.sh - Complete Automated Pipeline
#
# This script combines:
# 1. AI Solver Evolution (generates specialized solvers)
# 2. Automatic best solver selection
# 3. AI Reflection optimization
#
# Everything is automatic. Just run and wait.
#
# Usage:
#   ./AUTO.sh                      # Default: datasets 1,2,3 with 2 generations
#   ./AUTO.sh --all                # All 6 datasets
#   ./AUTO.sh --datasets 3 4 5     # Custom datasets
#   ./AUTO.sh --quick              # Quick test (1 generation, fewer iterations)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     █████╗ ██╗   ██╗████████╗ ██████╗                            ║
║    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗                           ║
║    ███████║██║   ██║   ██║   ██║   ██║                           ║
║    ██╔══██║██║   ██║   ██║   ██║   ██║                           ║
║    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝                           ║
║    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝                            ║
║                                                                   ║
║    AUTOMATED AI OPTIMIZATION PIPELINE                            ║
║    Evolution + Reflection = Maximum Performance                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Setup virtual environment if needed
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚙️  Setting up virtual environment...${NC}"
    python3 -m venv venv
    venv/bin/pip install -q --upgrade pip
    venv/bin/pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Environment ready${NC}"
    echo ""
fi

# Check API key
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo "Please create .env with your ANTHROPIC_API_KEY"
    exit 1
fi

# Parse arguments
DATASETS=""
EVOLUTION_GENS=2
OPT_ITERS=50
QUICK_MODE=false
CONTINUE_FLAG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            DATASETS="--all-datasets"
            shift
            ;;
        --quick)
            QUICK_MODE=true
            EVOLUTION_GENS=1
            OPT_ITERS=20
            DATASETS="--datasets 1_peaceful_village"
            shift
            ;;
        --continue)
            CONTINUE_FLAG="--continue"
            shift
            ;;
        --datasets)
            shift
            DS_LIST=""
            while [[ $# -gt 0 ]] && [[ ! $1 =~ ^-- ]]; do
                # Convert number to dataset name
                case $1 in
                    1) DS_LIST="$DS_LIST 1_peaceful_village" ;;
                    2) DS_LIST="$DS_LIST 2_small_town" ;;
                    3) DS_LIST="$DS_LIST 3_suburbia" ;;
                    4) DS_LIST="$DS_LIST 4_epitech" ;;
                    5) DS_LIST="$DS_LIST 5_isogrid" ;;
                    6) DS_LIST="$DS_LIST 6_manhattan" ;;
                    *) DS_LIST="$DS_LIST $1" ;;
                esac
                shift
            done
            DATASETS="--datasets$DS_LIST"
            ;;
        --generations)
            EVOLUTION_GENS="$2"
            shift 2
            ;;
        --iterations)
            OPT_ITERS="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./AUTO.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --all                    Process all 6 datasets"
            echo "  --quick                  Quick test (1 dataset, 1 gen, 20 iter)"
            echo "  --datasets <list>        Process specific datasets (numbers or names)"
            echo "                           Example: --datasets 1 2 3"
            echo "                           Example: --datasets 3_suburbia 4_epitech"
            echo "  --generations <N>        Evolution generations (default: 2)"
            echo "  --iterations <N>         Optimization iterations (default: 50)"
            echo "  --continue               Continue from existing generations without prompt"
            echo "  --help                   Show this help"
            echo ""
            echo "Examples:"
            echo "  ./AUTO.sh                                # Default: datasets 1,2,3"
            echo "  ./AUTO.sh --all                          # All 6 datasets"
            echo "  ./AUTO.sh --quick                        # Quick test"
            echo "  ./AUTO.sh --datasets 3 4 5               # Datasets 3, 4, 5"
            echo "  ./AUTO.sh --datasets 3 --generations 3   # Custom"
            echo "  ./AUTO.sh --datasets 3 4 --continue      # Continue evolution"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Display configuration
echo ""
echo -e "${BLUE}Configuration:${NC}"
if [ "$QUICK_MODE" = true ]; then
    echo -e "  Mode: ${YELLOW}QUICK TEST${NC}"
else
    echo "  Mode: FULL PIPELINE"
fi
echo "  Evolution generations: $EVOLUTION_GENS"
echo "  Optimization iterations: $OPT_ITERS"
if [ -n "$DATASETS" ]; then
    echo "  Datasets: $DATASETS"
else
    echo "  Datasets: 1_peaceful_village, 2_small_town, 3_suburbia (default)"
fi
echo ""

echo -e "${BLUE}What will happen:${NC}"
echo "  1️⃣  Generate specialized solvers (AI Evolution)"
echo "  2️⃣  Automatically select best solver per dataset"
echo "  3️⃣  Optimize with AI Reflection"
echo "  4️⃣  Generate comprehensive report"
echo ""

if [ "$QUICK_MODE" = false ]; then
    echo -e "${YELLOW}⏱️  Estimated time: 1-3 hours${NC}"
    echo -e "${YELLOW}💰 Estimated cost: ~\$1-2 in API calls${NC}"
else
    echo -e "${YELLOW}⏱️  Estimated time: 10-15 minutes${NC}"
    echo -e "${YELLOW}💰 Estimated cost: ~\$0.10 in API calls${NC}"
fi
echo ""

# Launch pipeline
echo -e "${GREEN}🚀 Launching automated pipeline...${NC}"
echo ""

venv/bin/python3 workflow/auto_pipeline.py \
    $DATASETS \
    --evolution-generations $EVOLUTION_GENS \
    --optimization-iterations $OPT_ITERS \
    $CONTINUE_FLAG

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║   ✅  PIPELINE COMPLETE!                           ║
    ║                                                    ║
    ║   Your datasets have been fully optimized         ║
    ║   using AI-generated algorithms + AI tuning       ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo ""
    echo "📁 Results:"
    echo "   Auto pipeline: workflow/auto_results/"
    echo "   Best solutions: solutions/best/"
    echo "   Generated solvers: methods/generated/"
    echo ""
    echo "📊 View final report:"
    echo "   cat workflow/auto_results/final_report.json | python -m json.tool"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Pipeline failed or was interrupted${NC}"
    echo "Check workflow/auto_results/ for partial results"
    exit 1
fi
