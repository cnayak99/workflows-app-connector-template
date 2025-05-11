@echo on
setlocal enabledelayedexpansion

REM Parse command line arguments
set "REBUILD=false"
for %%a in (%*) do (
    if "%%a"=="--build" set "REBUILD=true"
)

REM Print Stacksync branding
echo.
echo [96m  ____  _             _                           [0m
echo [96m / ___^|^| ^|_ __ _  ___^| ^| _____ _   _ _ __   ___  [0m
echo [96m \___ \^| __/ _` ^|/ __^| ^|/ / __^| ^| ^| ^| '_ \ / __^| [0m
echo [96m  ___) ^| ^|^| (_^| ^| (__|   <\__ \ ^|_^| ^| ^| ^| ^| (__  [0m
echo [96m ^|____/ \__\__,_^|\___|_^|\_\___/\__, ^|_^| ^|_^|\___^| [0m
echo [96m                               ^|___/             [0m
echo.
echo [92mApp Connector Public Module[0m
echo [94mDocumentation: https://docs.stacksync.com/workflows/app-connector[0m
echo.

REM Check if Docker is installed
docker --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker is not installed or not in the PATH. Please install Docker.
    goto :error
)

REM Ensure config directory exists
if not exist "config" (
    echo Creating config directory...
    mkdir config
)

REM Check if Dockerfile.dev exists
set "DOCKERFILE_PATH=config\Dockerfile.dev"
if not exist "%DOCKERFILE_PATH%" (
    if exist "Dockerfile.dev" (
        set "DOCKERFILE_PATH=Dockerfile.dev"
        echo Using Dockerfile.dev from main directory
    ) else (
        echo Error: Dockerfile.dev not found in config directory or main directory.
        goto :error
    )
) else (
    echo Using Dockerfile.dev from config directory
)

REM Read port from app_config.yaml
set "DEFAULT_PORT=2003"
set "PORT=%DEFAULT_PORT%"

if exist "app_config.yaml" (
    for /f "tokens=2 delims=: " %%p in ('findstr /r "^\s*port:" app_config.yaml') do (
        set "PORT=%%p"
        echo Using port from app_config.yaml: !PORT!
        goto :port_found
    )
    echo No port specified in app_config.yaml. Using default port: %PORT%
) else (
    echo Could not read app_config.yaml. Using default port: %PORT%
)

:port_found

REM Get the repository name from the current directory
for %%I in ("%CD%") do set "DIRNAME=%%~nxI"
set "REPO_NAME=%DIRNAME%"
set "REPO_NAME=%REPO_NAME:workflows-=%"
set "APP_NAME=workflows-app-%REPO_NAME%"

echo Preparing %APP_NAME%...

REM Check if the image exists
for /f %%i in ('docker images -q %APP_NAME% 2^>nul') do set "IMAGE_EXISTS=%%i"

REM Build if image doesn't exist or --rebuild flag is set
if "%IMAGE_EXISTS%"=="" (
    echo Docker image not found. Building: %APP_NAME%
    docker build -t %APP_NAME% -f %DOCKERFILE_PATH% . || goto :error
) else (
    if "%REBUILD%"=="true" (
        echo Forcing rebuild of Docker image: %APP_NAME%
        docker build --no-cache -t %APP_NAME% -f %DOCKERFILE_PATH% . || goto :error
    ) else (
        echo Docker image %APP_NAME% already exists. Skipping build.
        echo Use --build flag to force a rebuild.
    )
)

REM Run the container
echo Starting container on port %PORT%...
docker run --rm -p %PORT%:%PORT% -it -e ENVIRONMENT=dev -e REGION=besg --name=%APP_NAME% -v %CD%:/usr/src/app/ %APP_NAME% || goto :error

goto :end

:error
echo.
echo Error encountered. Please check the output above for details.
exit /b 1

:end
endlocal 