#!/bin/bash
#
# GO - Single command to launch automated workflow
#
# Usage:
#   ./GO.sh              # Run with default config
#   ./GO.sh --test       # Run with test config (fast, 1 dataset)
#

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "======================================================================"
echo "   AUTOMATED OPTIMIZATION WORKFLOW - GO"
echo "======================================================================"
echo -e "${NC}"

# Check if test mode
if [[ "$1" == "--test" ]]; then
    echo "Running in TEST mode (quick validation)"
    CONFIG="workflow/config_test.yaml"
else
    echo "Running in PRODUCTION mode (full optimization)"
    CONFIG="workflow/config.yaml"
fi

# Check if config exists
if [ ! -f "$CONFIG" ]; then
    echo "Error: Configuration file not found: $CONFIG"
    echo "Please create it from the template or check the path."
    exit 1
fi

echo "Configuration: $CONFIG"
echo ""

# Run the workflow
python3 workflow/go.py --config "$CONFIG"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Workflow completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "  - Check results in solutions/best/"
    echo "  - Review report in workflow/workspace/final_report.json"
    echo "  - Adjust targets in $CONFIG if needed"
else
    echo ""
    echo "Workflow failed. Check errors above."
    exit 1
fi
