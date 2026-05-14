# AWS CDK S3 Bucket Deployment Script (PowerShell)
# Usage: .\deploy.ps1 -Environment dev

param(
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev",
    
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Color output functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error-Custom { Write-Host $args -ForegroundColor Red }
function Write-Warning-Custom { Write-Host $args -ForegroundColor Yellow }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Success "========================================"
Write-Success "AWS CDK S3 Bucket Deployment"
Write-Success "========================================"
Write-Info "Environment: $Environment"
Write-Info ""

# Check prerequisites
Write-Warning-Custom "Checking prerequisites..."

# Check AWS CLI
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Error-Custom "Error: AWS CLI is not installed"
    exit 1
}
Write-Success "✓ AWS CLI found"

# Check CDK CLI
if (-not (Get-Command cdk -ErrorAction SilentlyContinue)) {
    Write-Error-Custom "Error: AWS CDK CLI is not installed"
    Write-Info "Install with: npm install -g aws-cdk"
    exit 1
}
Write-Success "✓ AWS CDK found"

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error-Custom "Error: Python is not installed or not in PATH"
    exit 1
}
Write-Success "✓ Python found"

# Load environment variables from .env file if it exists
if (Test-Path ".env") {
    Write-Info "Loading environment from .env file..."
    Get-Content .env | Where-Object { $_ -notmatch '^#' -and $_ -notmatch '^$' } | ForEach-Object {
        $key, $value = $_ -split '=', 2
        if ($key -and $value) {
            [Environment]::SetEnvironmentVariable($key, $value)
        }
    }
}

# Set deployment environment
$env:DEPLOYMENT_ENV = $Environment

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Info "Activating Python virtual environment..."
    & "venv\Scripts\activate.ps1"
}

# Install dependencies
Write-Warning-Custom "Installing Python dependencies..."
pip install -r requirements.txt | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Failed to install dependencies"
    exit 1
}
Write-Success "✓ Dependencies installed"

# Bootstrap CDK
Write-Warning-Custom "Bootstrapping AWS CDK..."
cdk bootstrap 2>&1 | Out-Null

# Synthesize stack
Write-Warning-Custom "Synthesizing CloudFormation template..."
cdk synth
if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Failed to synthesize stack"
    exit 1
}
Write-Success "✓ Stack synthesized"

# Deploy stack
Write-Warning-Custom "Deploying stack..."

$requireApproval = if ($Environment -eq "prod") { "any-change" } else { "never" }

cdk deploy --require-approval $requireApproval

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Deployment failed"
    exit 1
}

Write-Success "✓ Deployment completed successfully!"
Write-Success ""
Write-Success "Stack: S3BucketStack-$Environment"
Write-Info "To view stack outputs, run:"
Write-Info "aws cloudformation describe-stacks --stack-name S3BucketStack-$Environment"
