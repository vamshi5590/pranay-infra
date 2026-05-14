# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Prerequisites
```powershell
# Install Node.js (if not already installed)
# Download from https://nodejs.org/

# Install AWS CDK
npm install -g aws-cdk

# Verify installations
cdk --version
aws --version
python --version
```

### Step 2: Configure AWS Credentials
```powershell
# Configure AWS credentials
aws configure

# Enter your:
# AWS Access Key ID
# AWS Secret Access Key
# Default region (e.g., us-east-1)
# Default output format (json)
```

### Step 3: Setup Python Environment
```powershell
cd c:\Users\z004fh4f\Desktop\git

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Deployment
Edit `config.py` and update bucket names:
```python
CONFIG_MAP = {
    Environment.DEV: S3BucketConfig(
        bucket_name="my-company-dev-bucket-$(date +%s)",  # Must be globally unique
        environment=Environment.DEV,
        ...
    ),
}
```

### Step 5: Deploy
```powershell
# Deploy to dev environment
.\deploy.ps1 -Environment dev

# Deploy to production (requires approval)
.\deploy.ps1 -Environment prod
```

---

## Key Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Entry point - orchestrates stack creation |
| `s3_stack.py` | Core S3 bucket stack definition |
| `config.py` | Environment-specific configurations |
| `test_stack.py` | Validation utilities |
| `advanced_s3_stack.py` | Extended features (CORS, CloudFront, etc.) |
| `deploy.ps1` | PowerShell deployment script |
| `requirements.txt` | Python dependencies |

---

## Common Commands

```powershell
# View CloudFormation template (without deploying)
cdk synth

# See differences between current stack and code
cdk diff

# Deploy with user approval prompts
cdk deploy --require-approval=any-change

# Delete the stack
cdk destroy

# List all stacks
cdk list

# Get stack outputs
aws cloudformation describe-stacks --stack-name S3BucketStack-dev --query 'Stacks[0].Outputs'
```

---

## Validation & Testing

```powershell
# Validate deployed stack
python test_stack.py dev us-east-1

# Check bucket properties with AWS CLI
aws s3api head-bucket --bucket my-app-dev-bucket
aws s3api get-bucket-versioning --bucket my-app-dev-bucket
aws s3api get-bucket-encryption --bucket my-app-dev-bucket
```

---

## Production Checklist

Before deploying to production:

- [ ] Update bucket name to production naming convention
- [ ] Enable versioning: `enable_versioning=True`
- [ ] Enable logging: `enable_server_access_logs=True`
- [ ] Set logs bucket: `logs_bucket_name="my-app-prod-logs"`
- [ ] Enable lifecycle rules: `enable_lifecycle_rules=True`
- [ ] Set retention: `expiration_days=365`
- [ ] Review and approve IAM permissions
- [ ] Test in staging first
- [ ] Document bucket purpose and ownership

---

## Troubleshooting

### Error: "Bucket already exists"
S3 bucket names must be globally unique. Update `bucket_name` in `config.py`:
```python
bucket_name=f"my-app-dev-bucket-{unique_identifier}"
```

### Error: "Access Denied"
Ensure AWS credentials have S3 permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "cloudformation:*",
        "iam:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### CDK won't find Python
Make sure virtual environment is activated:
```powershell
venv\Scripts\activate
```

---

## Next Steps

1. **Add Bucket Policy**: Restrict access to specific IAM roles
2. **Enable CloudFront**: Use `advanced_s3_stack.py` for CDN integration
3. **Enable Website Hosting**: Serve static content from S3
4. **Add Monitoring**: CloudWatch metrics and alarms
5. **Implement Backup**: Cross-region replication

See `advanced_s3_stack.py` for examples of advanced configurations.
