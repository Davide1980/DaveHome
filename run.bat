@echo off
echo ============================================================
echo SCRAPER IMMOBILIARE - MONSELICE
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERRORE: Ambiente virtuale non trovato!
    echo Esegui prima setup_and_run.bat
    pause
    exit /b 1
)

REM Activate virtual environment and run scraper
call venv\Scripts\activate.bat

echo Avvio scraper...
echo.
python main.py

echo.
echo ============================================================
echo COMPLETATO!
echo ============================================================
echo.
pause
