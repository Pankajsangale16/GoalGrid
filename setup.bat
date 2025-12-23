@echo off
echo ========================================
echo Task Management System - Setup Script
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Creating database migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

echo.
echo [3/4] Applying database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to apply migrations
    echo Please ensure MySQL is running and database 'taskmanager_db' exists
    pause
    exit /b 1
)

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo Next steps:
echo 1. Create MySQL database: CREATE DATABASE taskmanager_db;
echo 2. Update database credentials in taskmanager/settings.py
echo 3. Run: python manage.py runserver
echo 4. Open browser: http://127.0.0.1:8000
echo ========================================
echo.
pause


