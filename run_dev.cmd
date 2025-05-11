@echo off
echo Running Stacksync connector in PowerShell...
powershell -ExecutionPolicy Bypass -File .\run_dev.ps1 %*
if %ERRORLEVEL% NEQ 0 (
    echo Failed to run PowerShell script. Please check if PowerShell is installed.
    echo Trying to run with Docker directly...
    
    echo Checking for Docker installation...
    docker --version > nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Docker is not installed or not in your PATH.
        echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
        pause
        exit /b 1
    )
    
    echo Docker is installed. Running minimal setup...
    if not exist "config" mkdir config
    set PORT=2003
    set APP_NAME=workflows-app-connector-template
    
    docker run --rm -p %PORT%:%PORT% -it -e ENVIRONMENT=dev -e REGION=besg --name=%APP_NAME% -v %CD%:/usr/src/app/ %APP_NAME%
)
pause 