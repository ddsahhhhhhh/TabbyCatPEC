@echo off
title Stop Tabbycat Local Server
color 0E
echo ===================================================
echo           STOPPING TABBYCAT LOCALHOST
echo ===================================================
echo.
cd /d "%~dp0"

echo Stopping Docker containers...
docker compose stop

echo.
echo ===================================================
echo   Tabbycat has been successfully STOPPED.
echo ===================================================
echo.
pause
