#!/bin/bash

# ============================================================
# Hostel Hub - Cloudflare Quick Tunnel Launcher
# ============================================================
# This script starts your Flask app AND the Cloudflare tunnel.
# Anyone on any network can access your site via the tunnel URL.
# ============================================================

# Configuration
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"  # Current script directory
FLASK_PORT=5000
CLOUDFLARED="cloudflared"  # Assumes cloudflared is in PATH
LOG_FILE="$PROJECT_DIR/tunnel.log"

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'  # No Color

echo ""
echo -e "${CYAN}========================================"
echo -e "   HOSTEL HUB - PUBLIC TUNNEL LAUNCHER  "
echo -e "========================================${NC}"
echo ""

# Step 1: Check cloudflared is available
if ! command -v $CLOUDFLARED &> /dev/null; then
    echo -e "${RED}[ERROR] cloudflared not found in PATH${NC}"
    echo -e "${YELLOW}Install cloudflared with: curl -L https://pkg.cloudflare.com/cloudflared-release.key | gpg --import - && sudo apt install cloudflared${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] cloudflared found.${NC}"

# Step 2: Check if Flask app exists
if [ ! -f "$PROJECT_DIR/app.py" ]; then
    echo -e "${RED}[ERROR] app.py not found in: $PROJECT_DIR${NC}"
    exit 1
fi

# Step 3: Launch Flask app in background
echo ""
echo -e "${YELLOW}[1/2] Starting Flask app on port $FLASK_PORT ...${NC}"
cd "$PROJECT_DIR"
python3 app.py > "$PROJECT_DIR/flask.log" 2>&1 &
FLASK_PID=$!
sleep 3

# Check if Flask started successfully
if ! kill -0 $FLASK_PID 2>/dev/null; then
    echo -e "${RED}[ERROR] Failed to start Flask app. Check flask.log${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Flask app started (PID: $FLASK_PID)${NC}"

# Step 4: Start the Cloudflare Quick Tunnel
echo -e "${YELLOW}[2/2] Starting Cloudflare Quick Tunnel...${NC}"
echo ""
echo -e "${GRAY}--------------------------------------------------------${NC}"
echo -e "${GRAY} Watch for the tunnel URL that looks like:${NC}"
echo -e "${GREEN} https://some-random-words-1234.trycloudflare.com${NC}"
echo -e "${GRAY}--------------------------------------------------------${NC}"
echo ""
echo -e "${CYAN} Share that URL with anyone - they can access your site!${NC}"
echo -e "${GRAY} Press Ctrl+C in this window to stop the tunnel.${NC}"
echo ""

# Trap Ctrl+C to clean up
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    kill $FLASK_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT

# Run tunnel and capture output to log file
$CLOUDFLARED tunnel --url "http://localhost:$FLASK_PORT" 2>&1 | tee "$LOG_FILE"
