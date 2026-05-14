#!/usr/bin/env python3
"""
Testing utilities for S3 CDK stack.
Provides validation and testing functions for stack configurations.
"""

import boto3
from typing import Dict, List, Optional
from config import S3BucketConfig, Environment, get_config


class S3BucketValidator:
    """Validates S3 bucket configuration and deployment."""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize S3 validator.
        
        Args:
            region: AWS region
        """
        self.s3_client = boto3.client("s3", region_name=region)
        self.cloudformation_client = boto3.client("cloudformation", region_name=region)
    
    def validate_bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if S3 bucket exists.
        
        Args:
            bucket_name: Name of the bucket
            
        Returns:
            True if bucket exists, False otherwise
        """
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except Exception:
            return False
    
    def validate_versioning(self, bucket_name: str) -> bool:
        """Check if versioning is enabled."""
        try:
            response = self.s3_client.get_bucket_versioning(Bucket=bucket_name)
            return response.get("Status") == "Enabled"
        except Exception:
            return False
    
    def validate_encryption(self, bucket_name: str) -> bool:
        """Check if encryption is enabled."""
        try:
            self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            return True
        except self.s3_client.exceptions.ServerSideEncryptionConfigurationNotFoundError:
            return False
        except Exception:
            return False
    
    def validate_public_access_block(self, bucket_name: str) -> bool:
        """Check if public access is blocked."""
        try:
            response = self.s3_client.get_public_access_block(Bucket=bucket_name)
            config = response["PublicAccessBlockConfiguration"]
            return all([
                config.get("BlockPublicAcls"),
                config.get("BlockPublicPolicy"),
                config.get("IgnorePublicAcls"),
                config.get("RestrictPublicBuckets"),
            ])
        except Exception:
            return False
    
    def validate_logging(self, bucket_name: str) -> Optional[str]:
        """
        Check if logging is configured.
        
        Returns:
            Target bucket name if logging is enabled, None otherwise
        """
        try:
            response = self.s3_client.get_bucket_logging(Bucket=bucket_name)
            if "LoggingEnabled" in response:
                return response["LoggingEnabled"]["TargetBucket"]
            return None
        except Exception:
            return None
    
    def validate_stack(self, stack_name: str, config: S3BucketConfig) -> Dict[str, bool]:
        """
        Validate entire stack against configuration.
        
        Args:
            stack_name: CloudFormation stack name
            config: Expected configuration
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "bucket_exists": self.validate_bucket_exists(config.bucket_name),
            "versioning": (
                self.validate_versioning(config.bucket_name)
                if config.enable_versioning else True
            ),
            "encryption": self.validate_encryption(config.bucket_name),
            "public_access_block": self.validate_public_access_block(config.bucket_name),
            "logging": (
                bool(self.validate_logging(config.bucket_name))
                if config.enable_server_access_logs else True
            ),
        }
        return results
    
    def print_validation_report(self, stack_name: str, config: S3BucketConfig) -> None:
        """Print detailed validation report."""
        results = self.validate_stack(stack_name, config)
        
        print(f"\n{'='*50}")
        print(f"Validation Report: {stack_name}")
        print(f"{'='*50}\n")
        
        for check, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{check:<30} {status}")
        
        all_passed = all(results.values())
        print(f"\n{'='*50}")
        print(f"Overall: {'✓ ALL CHECKS PASSED' if all_passed else '✗ SOME CHECKS FAILED'}")
        print(f"{'='*50}\n")


def run_validation(environment: str = "dev", region: str = "us-east-1") -> None:
    """
    Run validation for specified environment.
    
    Args:
        environment: Environment to validate (dev/staging/prod)
        region: AWS region
    """
    try:
        config = get_config(environment)
        validator = S3BucketValidator(region=region)
        stack_name = f"S3BucketStack-{environment}"
        
        validator.print_validation_report(stack_name, config)
        
    except Exception as e:
        print(f"Validation error: {e}")
        exit(1)


if __name__ == "__main__":
    import sys
    
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    region = sys.argv[2] if len(sys.argv) > 2 else "us-east-1"
    
    run_validation(env, region)
