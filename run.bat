@echo off
echo ====================================
echo Django Real-time Chat App Startup
echo ====================================
echo.

echo Checking if Redis is running...
netstat -an | find "6379" > nul
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Redis is not running on port 6379!
    echo.
    echo To start Redis:
    echo 1. Download Redis from: https://github.com/microsoftarchive/redis/releases
    echo 2. Extract and run redis-server.exe
    echo 3. Or use WSL: wsl then run: redis-server
    echo 4. Or use Docker: docker run -d -p 6379:6379 redis:latest
    echo.
    echo Waiting 5 seconds... (you can start Redis manually)
    timeout /t 5
)

echo.
echo Setting up initial data...
python manage.py migrate --noinput
python manage.py setup_test_data

echo.
echo ====================================
echo Starting Django Daphne Server...
echo ====================================
echo.
echo Server running at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Test user credentials (created by setup_test_data):
echo   alice / alice123
echo   bob / bob123
echo   charlie / charlie123
echo.

daphne -b 0.0.0.0 -p 8000 config.asgi:application
