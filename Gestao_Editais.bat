@echo off
title Gestao de Editais (Producao)
echo Iniciando Servidor Blindado...
cd /d "c:\Users\higosantos\Documents\gestao_editais\gestao_editais_novo"

:: Start waitress server without console window using pythonw
start "" ".\.venv\Scripts\pythonw.exe" serve.py

:: Wait for server to warm up
timeout /t 3 /nobreak >nul

:: Open Browser
start "" "http://127.0.0.1:5000"

:: Exit cleanly
exit
