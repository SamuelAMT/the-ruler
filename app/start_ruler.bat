@echo off
if not "%1"=="am_admin" (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList 'am_admin'"
    exit /b
)
cd /d "%~dp0"
set PYTHONPATH=%~dp0
call "..\my_venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
pythonw the-ruler.py