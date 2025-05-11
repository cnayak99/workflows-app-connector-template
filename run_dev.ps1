# PowerShell version of run_dev.bat
# Parse command line arguments
param(
    [switch]$build
)

# Print Stacksync branding
Write-Host ""
Write-Host "  ____  _             _                           " -ForegroundColor Cyan
Write-Host " / ___|| |_ __ _  ___| | _____ _   _ _ __   ___  " -ForegroundColor Cyan
Write-Host " \___ \| __/ _` |/ __| |/ / __| | | | '_ \ / __| " -ForegroundColor Cyan
Write-Host "  ___) | || (_| | (__|   <\__ \ |_| | | | | (__  " -ForegroundColor Cyan
Write-Host " |____/ \__\__,_|\___|_|\_\___/\__, |_| |_|\___| " -ForegroundColor Cyan
Write-Host "                               |___/             " -ForegroundColor Cyan
Write-Host ""
Write-Host "App Connector Public Module" -ForegroundColor Green
Write-Host "Documentation: https://docs.stacksync.com/workflows/app-connector" -ForegroundColor Blue
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "Docker detected: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not installed or not in the PATH." -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    Write-Host "After installing, restart your computer and try again." -ForegroundColor Yellow
    exit 1
}

# Ensure config directory exists
if (-not (Test-Path "config")) {
    Write-Host "Creating config directory..." -ForegroundColor Yellow
    New-Item -Path "config" -ItemType Directory | Out-Null
}

# Check if Dockerfile.dev exists
$dockerfilePath = "config\Dockerfile.dev"
if (-not (Test-Path $dockerfilePath)) {
    if (Test-Path "Dockerfile.dev") {
        $dockerfilePath = "Dockerfile.dev"
        Write-Host "Using Dockerfile.dev from main directory" -ForegroundColor Yellow
    } else {
        Write-Host "Error: Dockerfile.dev not found in config directory or main directory." -ForegroundColor Red
        
        # Create minimal Dockerfile.dev if it doesn't exist
        Write-Host "Creating minimal Dockerfile.dev in config directory..." -ForegroundColor Yellow
        $dockerfileContent = @"
FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=2003
EXPOSE \${PORT}

CMD ["python", "main.py"]
"@
        Set-Content -Path "config\Dockerfile.dev" -Value $dockerfileContent
        $dockerfilePath = "config\Dockerfile.dev"
        Write-Host "Created minimal Dockerfile.dev in config directory" -ForegroundColor Green
    }
} else {
    Write-Host "Using Dockerfile.dev from config directory" -ForegroundColor Green
}

# Read port from app_config.yaml
$defaultPort = 2003
$port = $defaultPort

if (Test-Path "app_config.yaml") {
    $appConfig = Get-Content "app_config.yaml" -Raw
    if ($appConfig -match "port:\s*(\d+)") {
        $port = $matches[1]
        Write-Host "Using port from app_config.yaml: $port" -ForegroundColor Green
    } else {
        Write-Host "No port specified in app_config.yaml. Using default port: $port" -ForegroundColor Yellow
    }
} else {
    Write-Host "Could not read app_config.yaml. Using default port: $port" -ForegroundColor Yellow
}

# Get the repository name from the current directory
$dirName = Split-Path -Leaf (Get-Location)
$repoName = $dirName -replace "workflows-", ""
$appName = "workflows-app-$repoName"

Write-Host "Preparing $appName..." -ForegroundColor Cyan

# Check if the image exists
$imageExists = $false
try {
    $existingImage = docker images -q $appName 2>$null
    $imageExists = ![string]::IsNullOrWhiteSpace($existingImage)
} catch {
    $imageExists = $false
}

# Build if image doesn't exist or --build flag is set
if (-not $imageExists) {
    Write-Host "Docker image not found. Building: $appName" -ForegroundColor Yellow
    docker build -t $appName -f $dockerfilePath .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to build Docker image." -ForegroundColor Red
        exit 1
    }
} else {
    if ($build) {
        Write-Host "Forcing rebuild of Docker image: $appName" -ForegroundColor Yellow
        docker build --no-cache -t $appName -f $dockerfilePath .
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to rebuild Docker image." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Docker image $appName already exists. Skipping build." -ForegroundColor Green
        Write-Host "Use -build flag to force a rebuild." -ForegroundColor Yellow
    }
}

# Run the container
Write-Host "Starting container on port $port..." -ForegroundColor Cyan
docker run --rm -p ${port}:${port} -it -e ENVIRONMENT=dev -e REGION=besg --name=$appName -v ${PWD}:/usr/src/app/ $appName
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to run Docker container." -ForegroundColor Red
    exit 1
} 