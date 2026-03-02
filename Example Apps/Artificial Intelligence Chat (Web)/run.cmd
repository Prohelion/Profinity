@echo off
REM Artificial Intelligence Chat Startup Script (Windows)
REM This script sets up the Python environment, installs dependencies, and runs the web UI

setlocal enabledelayedexpansion

REM Script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo.
echo Artificial Intelligence Chat Startup Script
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: python is not installed or not in PATH
    echo Please install Python 3.12 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1 delims=." %%i in ("%PYTHON_VERSION%") do set PYTHON_MAJOR=%%i
for /f "tokens=2 delims=." %%i in ("%PYTHON_VERSION%") do set PYTHON_MINOR=%%i

if %PYTHON_MAJOR% LSS 3 (
    echo Error: Python 3.12 or higher is required. Found: Python %PYTHON_VERSION%
    pause
    exit /b 1
)

if %PYTHON_MAJOR% EQU 3 (
    if %PYTHON_MINOR% LSS 12 (
        echo Error: Python 3.12 or higher is required. Found: Python %PYTHON_VERSION%
        pause
        exit /b 1
    )
)

echo Python %PYTHON_VERSION% found
echo.

REM Virtual environment setup
set "VENV_DIR=%SCRIPT_DIR%venv"

if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
    echo.
) else (
    echo Virtual environment already exists
    echo.
)

REM Activate virtual environment (venv must be created on this OS; remove venv if switching OS)
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    echo Remove the "venv" folder and run run.cmd again to create a venv for this OS.
    pause
    exit /b 1
)

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo Warning: Failed to upgrade pip, continuing anyway...
)

REM Check and install MCP Python SDK
echo.
echo Checking MCP Python SDK...
python -c "import mcp" >nul 2>&1
if errorlevel 1 (
    echo Installing MCP Python SDK from GitHub...
    pip install git+https://github.com/modelcontextprotocol/python-sdk.git
    if errorlevel 1 (
        echo Error: Failed to install MCP Python SDK
        echo Make sure git is installed and accessible
        pause
        exit /b 1
    )
    echo MCP Python SDK installed
) else (
    echo MCP Python SDK already installed
)

REM Check and install other dependencies
echo.
echo Checking dependencies...
if exist "requirements.txt" (
    echo Installing/updating dependencies from requirements.txt...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo Warning: Some dependencies may have failed to install
    ) else (
        echo Dependencies installed
    )
) else (
    echo requirements.txt not found, installing core dependencies...
    pip install flask flask-cors langchain-ollama httpx markdown --quiet
    if errorlevel 1 (
        echo Warning: Some dependencies may have failed to install
    ) else (
        echo Core dependencies installed
    )
)

REM Verify critical packages
echo.
echo Verifying critical packages...
set MISSING_COUNT=0

python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Error: flask is not installed
    set /a MISSING_COUNT+=1
)

python -c "import flask_cors" >nul 2>&1
if errorlevel 1 (
    echo Error: flask-cors is not installed
    set /a MISSING_COUNT+=1
)

python -c "import langchain_ollama" >nul 2>&1
if errorlevel 1 (
    echo Error: langchain-ollama is not installed
    set /a MISSING_COUNT+=1
)

python -c "import httpx" >nul 2>&1
if errorlevel 1 (
    echo Error: httpx is not installed
    set /a MISSING_COUNT+=1
)

python -c "import markdown" >nul 2>&1
if errorlevel 1 (
    echo Error: markdown is not installed
    set /a MISSING_COUNT+=1
)

python -c "import mcp" >nul 2>&1
if errorlevel 1 (
    echo Error: mcp is not installed
    set /a MISSING_COUNT+=1
)

python -c "from langchain_mcp_adapters.tools import load_mcp_tools" >nul 2>&1
if errorlevel 1 (
    echo langchain-mcp-adapters import test failed, checking details...
    python -c "from langchain_mcp_adapters.tools import load_mcp_tools" 2>&1
    echo.
    
    REM Check if base package is installed
    python -c "import langchain_mcp_adapters" >nul 2>&1
    if not errorlevel 1 (
        echo Base package is installed but tools submodule is missing
        echo Attempting to upgrade MCP and langchain-mcp-adapters...
        pip install --upgrade "mcp>=1.20.0" langchain-mcp-adapters --quiet
        REM Test again after upgrade
        python -c "from langchain_mcp_adapters.tools import load_mcp_tools" >nul 2>&1
        if errorlevel 1 (
            echo Error: Upgrade did not fix the issue.
            echo Try: pip install --upgrade "mcp>=1.20.0" langchain-mcp-adapters
            set /a MISSING_COUNT+=1
        ) else (
            echo langchain-mcp-adapters and MCP SDK upgraded and verified
        )
    ) else (
        echo Error: langchain-mcp-adapters is not installed
        set /a MISSING_COUNT+=1
    )
)

if %MISSING_COUNT% GTR 0 (
    echo.
    echo Error: %MISSING_COUNT% required packages are missing
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo All required packages are installed
echo.

REM Check for Ollama (optional but recommended)
echo Checking for Ollama...
where ollama >nul 2>&1
if errorlevel 1 (
    echo Warning: Ollama is not installed
    echo Install from: https://ollama.ai/
) else (
    echo Ollama is installed
    ollama list >nul 2>&1
    if errorlevel 1 (
        echo Warning: Ollama is installed but may not be running
        echo Start Ollama with: ollama serve
    )
)
echo.

REM Environment variables (can be overridden by user's environment)
if not defined PROFINITY_MCP_URL set "PROFINITY_MCP_URL=http://localhost:18080/sse"
if not defined OLLAMA_MODEL set "OLLAMA_MODEL=qwen3:14b"

REM Check if token is provided as argument
set "TOKEN_ARG="
if not "%~1"=="" (
    set "TOKEN_ARG=--token %~1"
    echo Token provided via command line argument
    echo.
) else if defined PROFINITY_TOKEN (
    echo Token found in environment variable PROFINITY_TOKEN
    echo.
) else (
    echo No token provided - login form will be shown on startup
    echo.
)

REM Run the application
echo Starting Artificial Intelligence Chat...
echo ==================================
echo Open http://localhost:8090 in your browser
echo Press Ctrl+C to stop
echo ==================================
echo.

if not "%~1"=="" (
    python profinity_ollama_webui.py --token %~1
) else (
    python profinity_ollama_webui.py
)

if errorlevel 1 (
    echo.
    echo Error: Application failed to start
    pause
    exit /b 1
)
