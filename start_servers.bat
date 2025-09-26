@echo off
setlocal enabledelayedexpansion

title Portfolio Development Servers

echo ========================================
echo  Starting Development Environment
echo ========================================
echo.

:: Check if backend directory exists
if not exist "%~dp0backend" (
    echo [ERROR] Backend directory not found at %~dp0backend
    pause
    exit /b 1
)

:: Check if frontend directory exists
if not exist "%~dp0frontend" (
    echo [ERROR] Frontend directory not found at %~dp0frontend
    pause
    exit /b 1
)

:: Start Backend server
echo [1/2] Starting Backend server...
start "Backend Server" cmd /k "@echo off & title Backend Server & cd /d "%~dp0backend" & if exist "%CD%\venv\Scripts\activate.bat" (call "%CD%\venv\Scripts\activate.bat" & python manage.py runserver) else (echo [ERROR] Virtual environment not found. Please create one in the project root. & pause)"

:: Start Frontend server
echo [2/2] Starting Frontend server...
start "Frontend Server" cmd /k "@echo off & title Frontend Server & cd /d "%~dp0frontend" & if exist "%CD%\node_modules" (npm start) else (echo [ERROR] Node modules not found. Please run 'npm install' in the frontend directory. & pause)"

echo.
echo ========================================
echo  Both servers are starting in separate windows...
echo  - Backend:  http://127.0.0.1:8000/
echo  - Frontend: http://localhost:3000/
echo ========================================
echo.
pause
