#!/bin/bash
# Artificial Intelligence Chat Startup Script (Unix/Linux/macOS)
# This script sets up the Python environment, installs dependencies, and runs the web UI

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${GREEN}Artificial Intelligence Chat Startup Script${NC}"
echo "=================================="

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed or not in PATH${NC}"
    echo "Please install Python 3.12 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
    echo -e "${RED}Error: Python 3.12 or higher is required. Found: Python $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}Python $PYTHON_VERSION found${NC}"

# Virtual environment setup
VENV_DIR="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "\n${GREEN}Virtual environment already exists${NC}"
fi

# Use venv's Python directly (no need to activate when we call $VENV_PYTHON for everything)
VENV_PYTHON="$VENV_DIR/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}Error: Virtual environment Python not found at $VENV_PYTHON${NC}"
    exit 1
fi

# Verify we're using the venv Python (don't exit on failure; subprocess env can differ)
PYTHON_USED=$("$VENV_PYTHON" -c "import sys; print(sys.executable)" 2>/dev/null) || PYTHON_USED="$VENV_PYTHON"
echo -e "${GREEN}Using Python: $PYTHON_USED${NC}"

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
"$VENV_PYTHON" -m pip install --upgrade pip --quiet

# Check and install MCP Python SDK (now available on PyPI)
echo -e "\n${YELLOW}Checking MCP Python SDK...${NC}"
if ! "$VENV_PYTHON" -c "import mcp" 2>/dev/null; then
    echo -e "${YELLOW}Installing MCP Python SDK from PyPI...${NC}"
    "$VENV_PYTHON" -m pip install "mcp>=1.10.0" --quiet
    echo -e "${GREEN}MCP Python SDK installed${NC}"
else
    echo -e "${GREEN}MCP Python SDK already installed${NC}"
fi

# Check and install other dependencies
echo -e "\n${YELLOW}Installing dependencies from requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    "$VENV_PYTHON" -m pip install -r requirements.txt --quiet
    echo -e "${GREEN}Dependencies installed${NC}"
else
    echo -e "${RED}requirements.txt not found!${NC}"
    exit 1
fi

# Verify critical packages
echo -e "\n${YELLOW}Verifying critical packages...${NC}"
MISSING_PACKAGES=()

if ! "$VENV_PYTHON" -c "import flask" 2>/dev/null; then
    MISSING_PACKAGES+=("flask")
fi

if ! "$VENV_PYTHON" -c "import flask_cors" 2>/dev/null; then
    MISSING_PACKAGES+=("flask-cors")
fi

if ! "$VENV_PYTHON" -c "import langchain_ollama" 2>/dev/null; then
    MISSING_PACKAGES+=("langchain-ollama")
fi

if ! "$VENV_PYTHON" -c "import httpx" 2>/dev/null; then
    MISSING_PACKAGES+=("httpx")
fi

if ! "$VENV_PYTHON" -c "import markdown" 2>/dev/null; then
    MISSING_PACKAGES+=("markdown")
fi

if ! "$VENV_PYTHON" -c "import mcp" 2>/dev/null; then
    MISSING_PACKAGES+=("mcp")
fi

# Test langchain-mcp-adapters import
echo -e "${YELLOW}Testing langchain-mcp-adapters import...${NC}"
if ! "$VENV_PYTHON" -c "from langchain_mcp_adapters.tools import load_mcp_tools" 2>/dev/null; then
    echo -e "${RED}langchain-mcp-adapters import failed${NC}"
    echo -e "${YELLOW}Error details:${NC}"
    "$VENV_PYTHON" -c "from langchain_mcp_adapters.tools import load_mcp_tools" 2>&1 | head -20 || true
    MISSING_PACKAGES+=("langchain-mcp-adapters")
fi

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo -e "${RED}Error: Missing required packages: ${MISSING_PACKAGES[*]}${NC}"
    echo "Please run: pip install ${MISSING_PACKAGES[*]}"
    exit 1
fi

echo -e "${GREEN}All required packages are installed${NC}"

# Check for Ollama (optional but recommended)
echo -e "\n${YELLOW}Checking for Ollama...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}Ollama is installed${NC}"
    if ! ollama list &> /dev/null; then
        echo -e "${YELLOW}Warning: Ollama is installed but may not be running${NC}"
        echo "Start Ollama with: ollama serve"
    fi
else
    echo -e "${YELLOW}Warning: Ollama is not installed${NC}"
    echo "Install from: https://ollama.ai/"
fi

# Environment variables (can be overridden by user's environment)
export PROFINITY_MCP_URL="${PROFINITY_MCP_URL:-http://localhost:18080/sse}"
export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3:14b}"

# Check if token is provided as argument
TOKEN_ARG=""
if [ -n "$1" ]; then
    TOKEN_ARG="--token $1"
    echo -e "\n${GREEN}Token provided via command line argument${NC}"
elif [ -n "$PROFINITY_TOKEN" ]; then
    echo -e "\n${GREEN}Token found in environment variable PROFINITY_TOKEN${NC}"
else
    echo -e "\n${YELLOW}No token provided - login form will be shown on startup${NC}"
fi

# Run the application
echo -e "\n${GREEN}Starting Artificial Intelligence Chat...${NC}"
echo "=================================="
echo "Open http://localhost:8090 in your browser"
echo "Press Ctrl+C to stop"
echo "=================================="
echo ""

"$VENV_PYTHON" profinity_ollama_webui.py $TOKEN_ARG
