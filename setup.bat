@echo off
REM Setup script for DocuCollab on Windows

echo =============================================
echo DocuCollab - Django Setup Script
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 4: Running database migrations...
python manage.py migrate

echo.
echo Step 5: Creating admin account...
echo Please create a superuser account for admin access:
python manage.py createsuperuser

echo.
echo =============================================
echo Setup Complete!
echo =============================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat (if not already active)
echo   python manage.py runserver
echo.
echo Then open your browser to:
echo   http://localhost:8000
echo.
echo Admin panel:
echo   http://localhost:8000/admin
echo.
pause
