# GitHub Actions Workflows Guide

## 📋 Overview

This project includes two GitHub Actions workflows for CI/CD:

1. **`pipeline.yml`** - Testing & Validation Pipeline (5 stages)
2. **`deploy.yml`** - Deployment Pipeline (3 stages)

---

## 🚀 Workflow 1: Testing Pipeline (`pipeline.yml`)

### Purpose
Automatically test and validate code on every push and pull request.

### Triggers
- ✅ Push to `main`, `develop`, or `feature/**` branches
- ✅ Pull requests to `main` or `develop`
- ✅ Manual trigger (workflow_dispatch)

### 5 Stages

#### **Stage 1: Code Validation** 🔍
- Checks Python syntax
- Validates JSON files
- Verifies project structure
- **Status**: Must pass to proceed

```bash
python -m py_compile *.py
python -m json.tool cdk.json
```

#### **Stage 2: Dependency Check** 📦
- Installs Python packages
- Verifies all imports work
- Checks Node.js availability
- **Status**: Must pass to proceed

```bash
pip install -r requirements.txt
python -c "import aws_cdk; import constructs; import dotenv"
node --version
```

#### **Stage 3: Configuration Test** ⚙️
- Loads all environment configs (dev/staging/prod)
- Validates configuration parameters
- Tests configuration module
- **Status**: Must pass to proceed

```python
from config import get_config
dev_config = get_config('dev')      # ✓ Passes
staging_config = get_config('staging')  # ✓ Passes
prod_config = get_config('prod')    # ✓ Passes
```

#### **Stage 4: CDK Synthesis** 🏗️
- Tests CloudFormation generation for each environment
- Verifies CDK can synthesize templates
- Depends on: Stages 1 & 2
- **Status**: Must pass to proceed

```bash
export DEPLOYMENT_ENV=dev
cdk synth  # Generates CloudFormation template
```

#### **Stage 5: Test & Report** 🧪
- Runs final tests
- Generates pipeline report
- Checks deployment readiness
- Depends on: All previous stages
- **Status**: Final validation

```
✅ Stage 1: Code Validation - PASSED
✅ Stage 2: Dependency Check - PASSED
✅ Stage 3: Configuration Test - PASSED
✅ Stage 4: CDK Synthesis - PASSED
✅ Overall Status: ALL TESTS PASSED
```

### Example Output

```
╔════════════════════════════════════════╗
║   STAGE 1: CODE VALIDATION             ║
╚════════════════════════════════════════╝

✓ Checking Python files...
✓ Validating YAML syntax...
✓ Running linters...

🔎 Validating Python files...
✅ All Python files syntax is valid!

🔎 Validating JSON files...
✅ cdk.json is valid!

🔎 Checking project structure...
Files found:
-rw-r--r-- app.py
-rw-r--r-- config.py
-rw-r--r-- s3_stack.py
-rw-r--r-- requirements.txt

✅ Stage 1 PASSED: Code Validation Successful
```

---

## 🚀 Workflow 2: Deployment Pipeline (`deploy.yml`)

### Purpose
Deploy the CDK stack to AWS environments.

### Triggers
- Manual trigger only (workflow_dispatch)
- **Input**: Select environment (dev/staging/prod)

### Usage

1. Go to **GitHub** → Your Repository
2. Click **Actions** tab
3. Select **AWS CDK Deployment** workflow
4. Click **Run workflow**
5. Select environment:
   - `dev` - Development (auto-approve)
   - `staging` - Staging (auto-approve)
   - `prod` - Production (requires approval)
6. Click **Run workflow**

### 3 Stages

#### **Stage 1: Pre-deployment Checks** 🔐
- Validates environment selection
- Loads and validates configuration
- Checks AWS credentials
- **Status**: Must pass

```bash
Environment: dev/staging/prod
Configuration: Validated ✓
AWS Credentials: Validated ✓
```

#### **Stage 2: Deploy to AWS** 🚀
- Bootstraps CDK (first-time setup)
- Synthesizes CloudFormation template
- Deploys to AWS
- Depends on: Stage 1
- **Status**: Active deployment

```bash
cdk bootstrap
cdk synth
cdk deploy  # Auto-approve for dev/staging
           # Requires approval for prod
```

#### **Stage 3: Post-deployment Validation** ✅
- Validates deployed resources
- Generates deployment report
- Confirms success
- Depends on: Stage 2

```
📊 Deployment Report
═════════════════════════════════════════

Environment: dev
Deployment Date: 2024-01-15 10:30:00

Resources Deployed:
✓ S3 Bucket
✓ Encryption Configuration
✓ Versioning
✓ Public Access Block
✓ Deployment Successful
```

---

## 📁 Workflow Files Location

```
.github/
└── workflows/
    ├── pipeline.yml    # Testing & validation (5 stages)
    └── deploy.yml      # Deployment (3 stages)
```

---

## 🔐 Required Secrets for Deployment

For `deploy.yml` to work, add these secrets to your GitHub repository:

### GitHub Secrets Setup

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add:

```
Name: AWS_ROLE_TO_ASSUME
Value: arn:aws:iam::123456789012:role/GitHubActionsRole

Name: AWS_REGION
Value: us-east-1
```

### AWS IAM Role Setup

Create an IAM role with:
- Trust relationship for GitHub
- S3, CloudFormation, CDK permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "cloudformation:*",
        "iam:*",
        "cdk:*"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 📊 Workflow Status Badges

Add these to your README.md:

```markdown
[![Pipeline Tests](https://github.com/YOUR_USER/YOUR_REPO/actions/workflows/pipeline.yml/badge.svg)](https://github.com/YOUR_USER/YOUR_REPO/actions/workflows/pipeline.yml)

[![Deployment](https://github.com/YOUR_USER/YOUR_REPO/actions/workflows/deploy.yml/badge.svg)](https://github.com/YOUR_USER/YOUR_REPO/actions/workflows/deploy.yml)
```

---

## 🎯 Typical Workflow

```
Developer pushes code
        ↓
GitHub detects push
        ↓
pipeline.yml triggers automatically
        ↓
Runs 5 stages of testing
        ↓
All tests pass ✓
        ↓
Developer ready to deploy
        ↓
Manually trigger deploy.yml
        ↓
Select environment (dev/staging/prod)
        ↓
Deployment runs (3 stages)
        ↓
Stack deployed to AWS ✓
```

---

## 📝 Viewing Logs

1. Go to **Actions** tab
2. Click workflow name
3. Click specific run
4. Expand each stage to see detailed logs

### Example Log View
```
deploy.ps1
├─ Checkout code ✓
├─ Validate Python syntax ✓
├─ Validate JSON files ✓
├─ Check file structure ✓
├─ Stage 1 Complete ✓
├─ Install dependencies ✓
├─ Stage 2 Complete ✓
└─ Test & Report ✓
```

---

## 🚨 Troubleshooting

### Pipeline Fails: "Python not found"
- Verify Python version in workflow: `PYTHON_VERSION: '3.11'`
- Check dependencies in `requirements.txt`

### Deployment Fails: "AWS credentials invalid"
- Verify AWS_ROLE_TO_ASSUME secret is set correctly
- Check IAM role permissions
- Ensure role trust relationship includes GitHub

### CDK Synth Error
- Check `DEPLOYMENT_ENV` is set correctly
- Verify configuration exists in `config.py`
- Check AWS region is valid

### Bucket Name Already Exists
- S3 bucket names must be globally unique
- Update `bucket_name` in `config.py`
- Use timestamp or UUID suffix

---

## 💡 Best Practices

1. **Always test locally first**
   ```powershell
   .\deploy.ps1 -Environment dev
   ```

2. **Test in dev before staging**
   - Deploy to dev
   - Validate in AWS console
   - Deploy to staging

3. **Manual approval for production**
   - Production deployments require approval
   - Review CloudFormation diff before approving
   - Follow change control process

4. **Monitor deployment status**
   - Check Actions tab for real-time updates
   - Review logs for any warnings
   - Validate post-deployment

5. **Keep secrets secure**
   - Use IAM roles, not access keys
   - Rotate secrets regularly
   - Follow least-privilege principle

---

## 🔄 Continuous Improvement

### Monitor Pipeline Performance
- Check average execution time
- Identify slow stages
- Optimize dependencies

### Track Deployment Success
- Monitor failed deployments
- Review error patterns
- Update error handling

### Regular Maintenance
- Update action versions
- Update dependencies
- Review security best practices

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS CloudFormation Reference](https://docs.aws.amazon.com/cloudformation/)
- [YAML Syntax Reference](https://yaml.org/)

---

## ❓ FAQ

**Q: How do I skip a workflow?**
A: Add `[skip ci]` to commit message:
```bash
git commit -m "Update docs [skip ci]"
```

**Q: Can I manually trigger the pipeline?**
A: Yes! Add `workflow_dispatch` to trigger manually from Actions tab.

**Q: How long does deployment take?**
A: Typically 2-5 minutes depending on AWS API latency.

**Q: Can I deploy multiple environments?**
A: Yes, run deploy.yml multiple times with different environment selections.

**Q: What if deployment fails?**
A: Check logs, fix issues, commit, and redeploy. Failed deployments don't roll back automatically.
