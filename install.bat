@echo off
echo Installing Adaptive Neuro-Symbolic Market Intelligence System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating environment file...
if not exist .env (
    copy .env.example .env
    echo Environment file created from template. Please edit .env with your configuration.
) else (
    echo Environment file already exists.
)

echo.
echo Installation completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your database and API credentials
echo 2. Set up MySQL database and run: mysql -u root -p < database/market.sql
echo 3. Run the system:
echo    - Backend: cd backend && python main.py
echo    - Dashboard: cd dashboard && streamlit run app.py
echo.
pause
