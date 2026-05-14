# AWS CDK S3 Bucket Deployment

Professional-grade Python AWS CDK project for S3 bucket provisioning with enterprise best practices.

## Features

- **Security-First Design**: Server-side encryption, public access blocking, and SSL enforcement
- **Multi-Environment Support**: Dev, Staging, and Production configurations
- **Logging & Monitoring**: Server access logging to dedicated bucket
- **Cost Optimization**: Lifecycle policies with automatic transitions to Glacier
- **Versioning**: Optional object versioning for data protection
- **Production-Ready**: Type hints, error handling, and comprehensive documentation

## Project Structure

```
.
├── app.py                 # CDK application entry point
├── s3_stack.py           # S3 Stack construct definition
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Prerequisites

- Python 3.9+
- AWS CLI configured with credentials
- AWS CDK CLI installed: `npm install -g aws-cdk`

## Installation

1. Clone/navigate to the project directory:
```bash
cd c:\Users\z004fh4f\Desktop\git
```

2. Create and activate virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize bucket names and settings for each environment:

```python
CONFIG_MAP = {
    Environment.DEV: S3BucketConfig(
        bucket_name="my-app-dev-bucket",
        environment=Environment.DEV,
        enable_versioning=False,
        ...
    ),
    ...
}
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bucket_name` | str | Required | Unique S3 bucket name |
| `environment` | Environment | Required | Deployment environment (dev/staging/prod) |
| `enable_versioning` | bool | True | Enable object versioning |
| `enable_encryption` | bool | True | Enable server-side encryption (AES-256) |
| `enable_public_access_block` | bool | True | Block all public access |
| `enable_server_access_logs` | bool | False | Enable access logging |
| `logs_bucket_name` | str | None | Dedicated bucket for logs |
| `enable_lifecycle_rules` | bool | False | Enable lifecycle policies |
| `transition_days` | int | 30 | Days before transitioning to Glacier |
| `expiration_days` | int | None | Days before object expiration |

## Usage

### Deploy to Development Environment

```bash
export DEPLOYMENT_ENV=dev
export CDK_DEFAULT_ACCOUNT=123456789012
export CDK_DEFAULT_REGION=us-east-1

cdk deploy
```

### Deploy to Production Environment

```bash
export DEPLOYMENT_ENV=prod
cdk deploy --require-approval=any-change
```

### Synthesize CloudFormation Template

```bash
export DEPLOYMENT_ENV=staging
cdk synth
```

### View Stack Differences

```bash
cdk diff
```

## Best Practices Implemented

### Security
- ✅ Public access blocking enabled by default
- ✅ Server-side encryption (AES-256) on all objects
- ✅ SSL/TLS enforcement for all connections
- ✅ Bucket policy to prevent unencrypted uploads
- ✅ Versioning for data recovery

### Compliance
- ✅ Server access logging for audit trails
- ✅ Separate logging bucket with proper permissions
- ✅ Resource tagging for governance
- ✅ RETAIN policy to prevent accidental deletion

### Cost Optimization
- ✅ Lifecycle policies for Glacier transitions
- ✅ Automatic object expiration
- ✅ Environment-specific configurations

### Operations
- ✅ Type hints for IDE support
- ✅ Comprehensive error handling
- ✅ CloudFormation outputs for easy reference
- ✅ Extensible design for additional features

## Extending the Stack

### Add KMS Encryption

Replace in `s3_stack.py`:
```python
encryption=s3.BucketEncryption.AES_256,
```

With:
```python
encryption=s3.BucketEncryption.KMS,
encryption_key=kms.Key(self, "S3Key", ...),
```

### Add Bucket Policy

```python
self.bucket.add_to_resource_policy(
    iam.PolicyStatement(
        principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
        actions=["s3:GetObject"],
        resources=[self.bucket.arn_for_objects("*")],
    )
)
```

### Add CORS Configuration

```python
self.bucket.add_cors_rule(
    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.POST],
    allowed_origins=["https://example.com"],
    allowed_headers=["*"],
)
```

## Troubleshooting

### Bucket Already Exists
If the bucket name is already taken, modify the `bucket_name` in `config.py`. S3 bucket names must be globally unique.

### Permission Denied
Ensure your AWS credentials have permissions:
- `s3:CreateBucket`
- `s3:PutBucketVersioning`
- `s3:PutBucketLogging`
- `s3:PutBucketEncryption`
- `s3:PutBucketPublicAccessBlock`

### CloudFormation Stack Exists
To update an existing stack:
```bash
cdk deploy --force
```

## Cleanup

To delete the stack and all resources:

```bash
cdk destroy
```

**Note**: S3 bucket is retained by default to prevent data loss. To delete the bucket, update `removal_policy` to `RemovalPolicy.DESTROY` in the stack.

## AWS CLI Commands Reference

```bash
# List buckets created by this stack
aws s3 ls

# Check bucket versioning
aws s3api get-bucket-versioning --bucket my-app-dev-bucket

# Check bucket encryption
aws s3api get-bucket-encryption --bucket my-app-dev-bucket

# Check public access block
aws s3api get-public-access-block --bucket my-app-dev-bucket

# Monitor bucket metrics
aws cloudwatch get-metric-statistics --namespace AWS/S3 \
  --metric-name NumberOfObjects --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z --period 86400 \
  --statistics Sum --dimensions Name=BucketName,Value=my-app-dev-bucket \
  Name=StorageType,Value=AllStorageTypes
```

## Support & Maintenance

For issues or enhancements:
1. Review AWS CDK documentation: https://docs.aws.amazon.com/cdk/latest/guide/
2. Check S3 best practices: https://docs.aws.amazon.com/AmazonS3/latest/userguide/BestPractices.html
3. Validate configurations before deployment

## License

Internal use. All rights reserved.
