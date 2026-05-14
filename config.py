"""
Configuration management for CDK S3 deployment.
Handles environment-specific settings and S3 bucket configurations.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Environment(Enum):
    """Deployment environment constants."""
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


@dataclass
class S3BucketConfig:
    """S3 bucket configuration parameters."""
    
    bucket_name: str
    environment: Environment
    enable_versioning: bool = True
    enable_encryption: bool = True
    enable_public_access_block: bool = True
    enable_server_access_logs: bool = False
    logs_bucket_name: Optional[str] = None
    enable_lifecycle_rules: bool = False
    transition_days: int = 30
    expiration_days: Optional[int] = None
    block_public_acl: bool = True
    block_public_policy: bool = True
    ignore_public_acl: bool = True
    restrict_public_bucket: bool = True


# Environment-specific configurations
CONFIG_MAP = {
    Environment.DEV: S3BucketConfig(
        bucket_name="my-app-dev-bucket",
        environment=Environment.DEV,
        enable_versioning=False,
        enable_server_access_logs=False,
    ),
    Environment.STAGING: S3BucketConfig(
        bucket_name="my-app-staging-bucket",
        environment=Environment.STAGING,
        enable_versioning=True,
        enable_server_access_logs=True,
        logs_bucket_name="my-app-staging-logs",
    ),
    Environment.PROD: S3BucketConfig(
        bucket_name="my-app-prod-bucket",
        environment=Environment.PROD,
        enable_versioning=True,
        enable_server_access_logs=True,
        logs_bucket_name="my-app-prod-logs",
        enable_lifecycle_rules=True,
        transition_days=30,
        expiration_days=365,
    ),
}


def get_config(environment: str) -> S3BucketConfig:
    """
    Retrieve configuration for specified environment.
    
    Args:
        environment: Environment name (dev, staging, prod)
        
    Returns:
        S3BucketConfig: Configuration object for the environment
        
    Raises:
        ValueError: If environment is not supported
    """
    try:
        env = Environment(environment.lower())
        return CONFIG_MAP[env]
    except ValueError:
        raise ValueError(
            f"Unsupported environment: {environment}. "
            f"Supported values: {', '.join([e.value for e in Environment])}"
        )
