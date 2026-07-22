@echo off
REM ===========================================================
REM Hostel Hub Quick Tunnel Launcher (Double-click this file)
REM ===========================================================

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start_tunnel.ps1"
pause
