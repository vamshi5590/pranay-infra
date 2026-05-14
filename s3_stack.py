"""
AWS CDK Stack for S3 bucket creation with production-ready configurations.
Implements best practices for security, logging, and lifecycle management.
"""

from typing import Optional
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    core,
    Duration,
)
from constructs import Construct
from config import S3BucketConfig


class S3BucketStack(Stack):
    """
    CDK Stack that provisions an S3 bucket with enterprise-grade configurations.
    
    Features:
    - Server-side encryption (AES-256 or KMS)
    - Versioning support
    - Public access blocking
    - Server access logging
    - Lifecycle policies (transition to Glacier, expiration)
    - Block all public access by default
    """
    
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: S3BucketConfig,
        **kwargs
    ) -> None:
        """
        Initialize S3BucketStack.
        
        Args:
            scope: CDK Construct scope
            construct_id: Unique identifier for this stack
            config: S3BucketConfig object with bucket settings
            **kwargs: Additional arguments passed to Stack
        """
        super().__init__(scope, construct_id, **kwargs)
        
        self.config = config
        self.bucket: Optional[s3.Bucket] = None
        self.logs_bucket: Optional[s3.Bucket] = None
        
        # Create logging bucket if needed
        if config.enable_server_access_logs:
            self._create_logs_bucket()
        
        # Create main S3 bucket
        self._create_s3_bucket()
        
        # Apply configurations
        self._configure_versioning()
        self._configure_encryption()
        self._configure_public_access_block()
        self._configure_logging()
        self._configure_lifecycle_rules()
    
    def _create_logs_bucket(self) -> None:
        """Create dedicated S3 bucket for access logs."""
        if not self.config.logs_bucket_name:
            raise ValueError("logs_bucket_name must be specified when enable_server_access_logs is True")
        
        self.logs_bucket = s3.Bucket(
            self,
            "LogsBucket",
            bucket_name=self.config.logs_bucket_name,
            encryption=s3.BucketEncryption.AES_256,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True,
            ),
            enforce_ssl=True,
            versioning_enabled=False,
            removal_policy=core.RemovalPolicy.RETAIN,
        )
    
    def _create_s3_bucket(self) -> None:
        """Create main S3 bucket with baseline configurations."""
        self.bucket = s3.Bucket(
            self,
            "S3Bucket",
            bucket_name=self.config.bucket_name,
            encryption=s3.BucketEncryption.AES_256,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=self.config.block_public_acl,
                block_public_policy=self.config.block_public_policy,
                ignore_public_acls=self.config.ignore_public_acl,
                restrict_public_buckets=self.config.restrict_public_bucket,
            ),
            enforce_ssl=True,
            removal_policy=core.RemovalPolicy.RETAIN,
        )
        
        # Output bucket name
        core.CfnOutput(
            self,
            "BucketName",
            value=self.bucket.bucket_name,
            description=f"S3 Bucket Name for {self.config.environment.value}",
            export_name=f"{self.config.environment.value}-bucket-name",
        )
        
        core.CfnOutput(
            self,
            "BucketArn",
            value=self.bucket.bucket_arn,
            description=f"S3 Bucket ARN for {self.config.environment.value}",
            export_name=f"{self.config.environment.value}-bucket-arn",
        )
    
    def _configure_versioning(self) -> None:
        """Configure bucket versioning if enabled."""
        if not self.bucket:
            return
        
        if self.config.enable_versioning:
            self.bucket.versioning_enabled = True
    
    def _configure_encryption(self) -> None:
        """Configure server-side encryption (already set in _create_s3_bucket)."""
        # Encryption is configured during bucket creation using AES-256
        # For KMS encryption, replace s3.BucketEncryption.AES_256 with:
        # s3.BucketEncryption.KMS or s3.BucketEncryption.KMS_MANAGED
        pass
    
    def _configure_public_access_block(self) -> None:
        """Apply public access blocking (already configured in _create_s3_bucket)."""
        # Public access blocking is configured during bucket creation
        pass
    
    def _configure_logging(self) -> None:
        """Configure server access logging if enabled and logs bucket exists."""
        if not self.bucket or not self.config.enable_server_access_logs or not self.logs_bucket:
            return
        
        self.bucket.log_file_prefix = "access-logs/"
        self.bucket.add_to_resource_policy(
            core.PolicyStatement(
                principals=[
                    core.ServicePrincipal("logging.s3.amazonaws.com")
                ],
                actions=["s3:PutObject"],
                resources=[self.logs_bucket.arn_for_objects("*")],
            )
        )
    
    def _configure_lifecycle_rules(self) -> None:
        """Configure S3 lifecycle policies for cost optimization."""
        if not self.bucket or not self.config.enable_lifecycle_rules:
            return
        
        # Transition to Glacier after specified days
        self.bucket.add_lifecycle_rule(
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=Duration.days(self.config.transition_days),
                )
            ],
            expiration=Duration.days(self.config.expiration_days) if self.config.expiration_days else None,
        )
    
    def get_bucket(self) -> s3.Bucket:
        """
        Get reference to the created S3 bucket.
        
        Returns:
            s3.Bucket: The S3 bucket construct
        """
        if not self.bucket:
            raise RuntimeError("Bucket not initialized")
        return self.bucket
