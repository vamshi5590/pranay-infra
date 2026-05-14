#!/bin/bash
# Deployment script for AWS CDK S3 bucket stack
# Usage: ./deploy.sh [dev|staging|prod]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validate environment argument
if [ $# -eq 0 ]; then
    ENVIRONMENT="dev"
    echo -e "${YELLOW}No environment specified, using 'dev' as default${NC}"
else
    ENVIRONMENT=$1
fi

# Validate environment value
if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
    echo -e "${RED}Error: Invalid environment '$ENVIRONMENT'${NC}"
    echo "Supported environments: dev, staging, prod"
    exit 1
fi

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    exit 1
fi

# Check if CDK CLI is installed
if ! command -v cdk &> /dev/null; then
    echo -e "${RED}Error: AWS CDK CLI is not installed${NC}"
    echo "Install with: npm install -g aws-cdk"
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Override with deployment environment
export DEPLOYMENT_ENV=$ENVIRONMENT

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}AWS CDK S3 Bucket Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Environment: $ENVIRONMENT"
echo "AWS Account: ${CDK_DEFAULT_ACCOUNT:-Using default}"
echo "AWS Region: ${CDK_DEFAULT_REGION:-Using default}"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Bootstrap CDK if needed
echo -e "${YELLOW}Bootstrapping AWS CDK...${NC}"
cdk bootstrap || true

# Synthesize the stack
echo -e "${YELLOW}Synthesizing CloudFormation template...${NC}"
cdk synth

# Deploy the stack
echo -e "${YELLOW}Deploying stack...${NC}"
if [ "$ENVIRONMENT" == "prod" ]; then
    cdk deploy --require-approval=any-change
else
    cdk deploy --require-approval=never
fi

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo ""
echo "Stack outputs:"
cdk describe-stack-resources --stack-name "S3BucketStack-$ENVIRONMENT" 2>/dev/null || true
