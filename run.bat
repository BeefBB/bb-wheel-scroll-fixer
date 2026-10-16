@echo off

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...

    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

echo Running "bb-wheel-scroll-fixer.py"...

if not exist ".venv" (
    echo .venv not found. Creating virtual environment...

    py -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    .venv\Scripts\pip.exe install -r requirements.txt
)

.venv\Scripts\python.exe "bb-wheel-scroll-fixer.py"

echo.
echo Application exited.
pause
