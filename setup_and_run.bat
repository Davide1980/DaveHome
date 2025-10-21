@echo off
echo ============================================================
echo SETUP SCRAPER IMMOBILIARE - MONSELICE
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non e' installato!
    echo Installa Python da: https://www.python.org/downloads/
    echo RICORDA: Spunta "Add Python to PATH" durante l'installazione
    pause
    exit /b 1
)

echo [1/3] Python trovato!
echo.

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo [2/3] Creazione ambiente virtuale...
    python -m venv venv
    echo Ambiente virtuale creato!
) else (
    echo [2/3] Ambiente virtuale gia' esistente
)
echo.

REM Activate virtual environment and install dependencies
echo [3/3] Installazione dipendenze...
call venv\Scripts\activate.bat
pip install -q --upgrade pip
pip install -q -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRORE durante l'installazione delle dipendenze!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SETUP COMPLETATO CON SUCCESSO!
echo ============================================================
echo.
echo Premi un tasto per avviare lo scraper...
pause >nul

REM Run the scraper
echo.
echo ============================================================
echo AVVIO SCRAPER...
echo ============================================================
echo.
python main.py

echo.
echo ============================================================
echo SCRAPING COMPLETATO!
echo ============================================================
echo.
echo Controlla il file CSV generato nella cartella corrente.
echo.
pause
