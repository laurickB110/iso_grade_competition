#!/bin/bash
#
# OVERNIGHT OPTIMIZATION - Maximum performance
#
# This script launches an intensive overnight optimization
# with maximum generations and iterations to reach target scores.
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    🌙 OVERNIGHT OPTIMIZATION MODE 🌙                              ║
║                                                                   ║
║    Maximum generations + iterations for best results             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${YELLOW}Configuration for tonight:${NC}"
echo "  Datasets: 3_suburbia, 4_epitech"
echo "  Generations: 6 (creates 6 specialized solvers per dataset)"
echo "  Iterations: 500 (extensive optimization with AI reflection)"
echo "  AI Reflection cycles: 10 (vs 3 default)"
echo "  Mode: 100% automatic (--auto-approve)"
echo ""
echo -e "${YELLOW}Targets:${NC}"
echo "  3_suburbia: 26,855,000 (current best: ~31,155,000)"
echo "  4_epitech:  30,315,000 (current best: ~36,500,000)"
echo ""
echo -e "${YELLOW}Estimated time: 8-10 hours${NC}"
echo -e "${YELLOW}Estimated cost: ~\$3-5 in API calls${NC}"
echo ""

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}⚠️  tmux not found. Installing...${NC}"
    sudo apt install -y tmux
fi

echo ""
echo "Starting in 5 seconds... (Ctrl+C to cancel)"
sleep 5

echo ""
echo -e "${GREEN}🚀 Launching overnight optimization in tmux session 'optim'...${NC}"
echo ""

# Kill existing session if any
tmux kill-session -t optim 2>/dev/null || true

# Create new session and run
tmux new-session -d -s optim "./AUTO.sh --datasets 3 4 --generations 6 --iterations 500 --auto-approve --continue"

echo -e "${GREEN}✅ Optimization launched in background!${NC}"
echo ""
echo "Commands to monitor:"
echo "  ${BLUE}tmux attach -t optim${NC}     # View progress in real-time"
echo "  ${BLUE}Ctrl+B then D${NC}            # Detach (process keeps running)"
echo "  ${BLUE}tmux ls${NC}                  # List sessions"
echo ""
echo "You can now:"
echo "  - Close this terminal (process continues)"
echo "  - Turn off your computer (if on server)"
echo "  - Go to sleep! 😴"
echo ""
echo "When you wake up:"
echo "  ${BLUE}tmux attach -t optim${NC}     # See results"
echo ""
echo -e "${YELLOW}Good night! 🌙${NC}"
echo ""
