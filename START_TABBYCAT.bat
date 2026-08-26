@echo off
title Tabbycat Local Server
color 0A
echo ===================================================
echo           STARTING TABBYCAT ON LOCALHOST
echo ===================================================
echo.
cd /d "%~dp0"

echo [1/3] Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: Docker Desktop is not running!
    echo Please open Docker Desktop, wait for it to start, and try again.
    echo.
    pause
    exit /b 1
)

echo [2/3] Starting Tabbycat containers (PostgreSQL, Redis, Web, Worker)...
docker compose up -d

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: Failed to start containers.
    echo.
    pause
    exit /b 1
)

echo [3/3] Opening Tabbycat in your web browser...
timeout /t 3 /nobreak >nul
start http://localhost:8000/

echo.
echo ===================================================
echo   Tabbycat is RUNNING at http://localhost:8000/
echo   To STOP Tabbycat, double-click STOP_TABBYCAT.bat
echo ===================================================
echo.
pause
