@echo off
:: Check if the script is running as administrator
net session >nul 2>&1
if '%errorlevel%' neq '0' (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

:: Run the Python script
python "%~dp0mainDev.py"

:: Pause to see errors
pause
