@echo off
REM ============================================================
REM  Build do executavel BaseFeeder.exe
REM  Rode este arquivo (2 cliques) dentro da pasta base_feeder,
REM  com Python instalado no Windows.
REM ============================================================

echo Instalando dependencias...
pip install pandas openpyxl watchdog pyinstaller

echo.
echo Gerando executavel...
pyinstaller --onefile --console --name BaseFeeder feeder.py

echo.
echo ============================================================
echo Pronto! O executavel esta em: dist\BaseFeeder.exe
echo Copie o BaseFeeder.exe para a pasta do seu projeto HTML.
echo ============================================================
pause
