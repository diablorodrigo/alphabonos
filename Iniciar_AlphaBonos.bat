@echo off
title AlphaBonos - Terminal de Renta Fija & Macro Local
cd /d "%~dp0"
echo ============================================================
echo   Iniciando AlphaBonos en http://localhost:8060 ...
echo ============================================================
start "" "http://localhost:8060"
"C:\Users\crist\AppData\Local\Programs\Python\Python312\python.exe" server.py
pause
