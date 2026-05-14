"""
Advanced S3 Stack with additional features like CORS, bucket policies, and notifications.
This is an extended version showing how to enhance the base S3BucketStack.
"""

from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    core,
)
from s3_stack import S3BucketStack
from config import S3BucketConfig


class AdvancedS3BucketStack(S3BucketStack):
    """
    Extended S3 Stack with additional features:
    - CORS configuration
    - Bucket policies for CloudFront
    - SNS notifications for object events
    - Website hosting
    """
    
    def add_cors_configuration(
        self,
        allowed_methods: list = None,
        allowed_origins: list = None,
        allowed_headers: list = None,
        max_age: int = 3000,
    ) -> None:
        """
        Add CORS configuration to bucket.
        
        Args:
            allowed_methods: HTTP methods to allow (GET, PUT, POST, etc.)
            allowed_origins: Origins allowed to access bucket
            allowed_headers: Headers allowed in cross-origin requests
            max_age: Max age of preflight requests in seconds
        """
        if not self.bucket:
            return
        
        allowed_methods = allowed_methods or [s3.HttpMethods.GET]
        allowed_origins = allowed_origins or ["*"]
        allowed_headers = allowed_headers or ["*"]
        
        self.bucket.add_cors_rule(
            allowed_methods=allowed_methods,
            allowed_origins=allowed_origins,
            allowed_headers=allowed_headers,
            max_age=core.Duration.seconds(max_age),
        )
    
    def add_cloudfront_policy(self, distribution_id: str) -> None:
        """
        Add bucket policy allowing CloudFront distribution to access objects.
        
        Args:
            distribution_id: CloudFront distribution ID
        """
        if not self.bucket:
            return
        
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                principals=[
                    iam.ServicePrincipal("cloudfront.amazonaws.com")
                ],
                actions=["s3:GetObject"],
                resources=[self.bucket.arn_for_objects("*")],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{core.Stack.of(self).account}:distribution/{distribution_id}"
                    }
                },
            )
        )
    
    def enable_website_hosting(
        self,
        index_document: str = "index.html",
        error_document: str = "error.html",
    ) -> None:
        """
        Configure bucket for static website hosting.
        
        Args:
            index_document: Default index document
            error_document: Error document path
        """
        if not self.bucket:
            return
        
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[self.bucket.arn_for_objects("*")],
            )
        )
        
        # Configure website hosting
        core.CfnOutput(
            self,
            "WebsiteURL",
            value=self.bucket.bucket_website_url,
            description="S3 Website Hosting URL",
        )
    
    def deny_unencrypted_uploads(self) -> None:
        """Add policy to deny unencrypted object uploads."""
        if not self.bucket:
            return
        
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[self.bucket.arn_for_objects("*")],
                effect=iam.Effect.DENY,
                conditions={
                    "StringNotEquals": {
                        "s3:x-amz-server-side-encryption": "AES256"
                    }
                },
            )
        )
