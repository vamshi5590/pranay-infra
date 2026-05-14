#!/usr/bin/env python3
"""
AWS CDK application entry point for S3 bucket deployment.
Handles stack instantiation and synthesizes CloudFormation templates.
"""

import os
import sys
from aws_cdk import App, Environment as CDKEnvironment
from s3_stack import S3BucketStack
from config import get_config, Environment


def main() -> None:
    """
    Main entry point for CDK application.
    Retrieves configuration from environment variables and creates the stack.
    """
    
    # Get environment from command line or environment variable
    deployment_env = os.getenv("DEPLOYMENT_ENV", "dev").lower()
    
    # Validate environment
    try:
        config = get_config(deployment_env)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize CDK App
    app = App()
    
    # Get AWS account and region from context or environment
    aws_account = os.getenv("CDK_DEFAULT_ACCOUNT", "123456789012")
    aws_region = os.getenv("CDK_DEFAULT_REGION", "us-east-1")
    
    # Create CDK environment
    cdk_env = CDKEnvironment(
        account=aws_account,
        region=aws_region,
    )
    
    # Instantiate the stack
    stack = S3BucketStack(
        app,
        f"S3BucketStack-{config.environment.value}",
        config=config,
        env=cdk_env,
        description=f"S3 Bucket Stack for {config.environment.value} environment",
    )
    
    # Add tags for resource organization
    app.node.apply_aspect(
        core.Tag("Environment", config.environment.value)
    )
    app.node.apply_aspect(
        core.Tag("ManagedBy", "CDK")
    )
    
    # Synthesize the app
    app.synth()


if __name__ == "__main__":
    # Import after ensuring path is set
    from aws_cdk import core
    main()
