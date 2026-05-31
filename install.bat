@echo off
title Purple Storm v2.1 - Installer
echo [35m============================================
echo  Purple Storm v2.1 - Installation
echo [35m============================================
echo [97m

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m[!] Python not found. Please install Python 3.x
    pause
    exit /b 1
)

echo [35m[+][97m Python detected
echo [35m[+][97m All dependencies are built-in
echo [35m[+][97m Installation complete
echo.
echo [35m============================================
echo  Run start.bat to launch
echo [35m============================================
echo [97m
pause
