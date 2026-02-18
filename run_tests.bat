@echo off
echo Healthcare System - Running Tests
echo ====================================

echo Installing dependencies...
pip install -r requirements.txt -q
pip install -r requirements-dev.txt -q

echo.
echo Running unit tests...
python -m pytest test_crypto_utils.py -v
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pytest test_auth_system.py -v
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pytest test_patient_records.py -v
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pytest test_integration.py -v
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo Generating coverage report...
python -m pytest --cov=. --cov-report=term --cov-report=html
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo Running linting...
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo All tests passed!
echo Coverage report: htmlcov\index.html