@echo off
title Adaptive Market Intelligence System

echo Starting Adaptive Neuro-Symbolic Market Intelligence System...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo Environment file not found. Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

echo Choose what to start:
echo 1. Backend API only
echo 2. Dashboard only
echo 3. Both Backend and Dashboard
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto backend_only
if "%choice%"=="2" goto dashboard_only
if "%choice%"=="3" goto both
if "%choice%"=="4" goto end
echo Invalid choice. Please try again.
goto start

:backend_only
echo.
echo Starting Backend API...
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
cd backend
python main.py
goto end

:dashboard_only
echo.
echo Starting Dashboard...
echo Dashboard will be available at: http://localhost:8501
echo.
cd dashboard
streamlit run app.py
goto end

:both
echo.
echo Starting Backend API and Dashboard...
echo.
echo Backend API will be available at: http://localhost:8000
echo Dashboard will be available at: http://localhost:8501
echo.
REM Start backend in background
start "Backend API" cmd /k "cd backend && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start dashboard
cd dashboard
streamlit run app.py
goto end

:end
echo.
echo System stopped.
pause
