# GitHub Actions Workflow Inputs Guide

## 📋 Overview

Both workflows now have **input parameters** you can select when running them manually. These inputs allow you to customize behavior without editing code.

---

## 🎯 Workflow 1: Pipeline Testing (`pipeline.yml`)

### Available Inputs

#### **1. Verbose Output** 🔍
```
Label: Enable verbose output
Options:
  ◉ false (default) - Normal output
  ○ true           - Detailed logging
```

**What it does:**
- `false` - Shows standard output
- `true` - Shows detailed debug information

**When to use:**
- Use `true` when debugging test failures
- Use `false` for normal runs

---

#### **2. Skip Tests** ⏭️
```
Label: Skip testing stages
Options:
  ◉ false (default) - Run all tests
  ○ true           - Skip tests
```

**What it does:**
- `false` - Run all 5 stages (validation, dependencies, config, synthesis, report)
- `true` - Skip expensive test stages (use with caution!)

**When to use:**
- Use `false` for normal deployments
- Use `true` only if you're sure code is safe
- NOT recommended for production

---

#### **3. Notification Level** 📢
```
Label: Notification level
Options:
  ◉ all (default)    - All notifications
  ○ errors-only      - Only error notifications
  ○ none             - No notifications
```

**What it does:**
- `all` - Notify on all events (start, pass, fail)
- `errors-only` - Notify only on failures
- `none` - No notifications (silent mode)

**When to use:**
- Use `all` during active development
- Use `errors-only` for scheduled runs
- Use `none` for debugging without alerts

---

## 🚀 Workflow 2: Deployment (`deploy.yml`)

### Available Inputs

#### **1. Environment** 🌍 (Required)
```
Label: Environment to deploy
Options:
  ◉ dev (default)    - Development (auto-approve, fast)
  ○ staging          - Staging (standard checks)
  ○ prod             - Production (requires approval)
```

**What it does:**
- `dev` - Deploys to development bucket (no approval needed)
- `staging` - Deploys to staging bucket (standard checks)
- `prod` - Deploys to production (manual approval required)

**When to use:**
- Start with `dev` to test
- Move to `staging` before production
- Use `prod` only after testing

---

#### **2. Dry Run** 🔬
```
Label: Dry run (preview changes only)
Options:
  ◉ false (default) - Actually deploy
  ○ true           - Preview only (no deployment)
```

**What it does:**
- `false` - Creates actual AWS resources
- `true` - Shows what WOULD be deployed (no changes made)

**When to use:**
- Use `false` for actual deployments
- Use `true` to preview changes before deploying
- Use `true` to review CloudFormation diff

---

#### **3. Enable Logging** 📊
```
Label: Enable server access logging
Options:
  ◉ true (default)  - Logging ON
  ○ false           - Logging OFF
```

**What it does:**
- `true` - Logs all S3 access to separate bucket
- `false` - No access logging (saves cost)

**When to use:**
- Use `true` for production (required for compliance)
- Use `true` for staging (good practice)
- Use `false` for development (saves money)

---

#### **4. Enable Versioning** 📝
```
Label: Enable bucket versioning
Options:
  ◉ true (default)  - Versioning ON
  ○ false           - Versioning OFF
```

**What it does:**
- `true` - Keep versions of all objects (recovery enabled)
- `false` - Only keep current version

**When to use:**
- Use `true` for production (data protection)
- Use `true` for staging (good practice)
- Use `false` for development (saves storage)

---

#### **5. Enable Lifecycle** ♻️
```
Label: Enable lifecycle rules
Options:
  ◉ false (default) - Lifecycle OFF
  ○ true           - Lifecycle ON
```

**What it does:**
- `false` - Objects stay indefinitely
- `true` - Auto-transition to Glacier after 30 days, delete after 365 days

**When to use:**
- Use `false` for active data
- Use `true` for archive/long-term storage
- Use `true` for cost optimization

---

#### **6. Deployment Tags** 🏷️
```
Label: Custom tags (comma-separated key=value)
Default: Team=Platform,CostCenter=Engineering

Examples:
  Team=Platform,CostCenter=Engineering
  Owner=DevOps,Project=Infrastructure,Environment=Dev
  Compliance=HIPAA,DataClass=Confidential
```

**What it does:**
- Adds custom tags to deployed resources
- Used for billing, compliance, organization

**When to use:**
- Add team ownership tags
- Add cost center for billing
- Add compliance/classification tags

---

#### **7. Notifications** 📧
```
Label: Send notifications
Options:
  ◉ true (default)  - Send notifications
  ○ false           - No notifications
```

**What it does:**
- `true` - Send Slack/email notifications on completion
- `false` - Silent deployment (check manually)

**When to use:**
- Use `true` for production deployments (notify team)
- Use `true` for important staging
- Use `false` for development/testing

---

## 📸 Visual Walkthrough

### **Step 1: Go to Actions**
```
GitHub Repository
│
└─ Actions (Tab)
```

### **Step 2: Select Workflow**
```
Left Sidebar:
├─ All workflows
├─ AWS CDK S3 Deployment Pipeline ← For testing
└─ AWS CDK Deployment ← For deployment
```

### **Step 3: Click "Run workflow"**
```
┌───────────────────────────────────┐
│ AWS CDK S3 Deployment Pipeline   │
│                                  │
│ [Run workflow ▼] ← CLICK HERE   │
│ Latest: passed 2 hours ago       │
└───────────────────────────────────┘
```

### **Step 4: Select Inputs** (Appears automatically)

**For pipeline.yml:**
```
┌─────────────────────────────────────┐
│ Workflow inputs                     │
│                                     │
│ verbose_output                      │
│ [ false (default) ▼ ]               │
│ ├─ false                            │
│ └─ true                             │
│                                     │
│ skip_tests                          │
│ [ false (default) ▼ ]               │
│ ├─ false                            │
│ └─ true                             │
│                                     │
│ notification_level                  │
│ [ all (default) ▼ ]                 │
│ ├─ all                              │
│ ├─ errors-only                      │
│ └─ none                             │
│                                     │
│ [Run workflow]  [Cancel]            │
└─────────────────────────────────────┘
```

**For deploy.yml:**
```
┌─────────────────────────────────────┐
│ Workflow inputs                     │
│                                     │
│ environment * (required)            │
│ [ dev (default) ▼ ]                 │
│ ├─ dev                              │
│ ├─ staging                          │
│ └─ prod                             │
│                                     │
│ dry_run                             │
│ [ false (default) ▼ ]               │
│ ├─ false                            │
│ └─ true                             │
│                                     │
│ enable_logging                      │
│ [ true (default) ▼ ]                │
│ ├─ true                             │
│ └─ false                            │
│                                     │
│ enable_versioning                   │
│ [ true (default) ▼ ]                │
│ ├─ true                             │
│ └─ false                            │
│                                     │
│ enable_lifecycle                    │
│ [ false (default) ▼ ]               │
│ ├─ false                            │
│ └─ true                             │
│                                     │
│ deployment_tags                     │
│ [Team=Platform,CostCenter=...]  ✎   │
│                                     │
│ notifications                       │
│ [ true (default) ▼ ]                │
│ ├─ true                             │
│ └─ false                            │
│                                     │
│ [Run workflow]  [Cancel]            │
└─────────────────────────────────────┘
```

### **Step 5: Make Selections**
- Select values from dropdowns
- Enter custom values in text fields
- Click "Run workflow"

---

## 🎯 Common Scenarios

### **Scenario 1: Test Pipeline with Debug Output**
```
workflow_dispatch with inputs:
├─ verbose_output: true ← See detailed logs
├─ skip_tests: false ← Run all tests
└─ notification_level: all ← Get all notifications
```

### **Scenario 2: Quick Dev Deployment**
```
workflow_dispatch with inputs:
├─ environment: dev
├─ dry_run: false ← Actually deploy
├─ enable_logging: false ← Save cost
├─ enable_versioning: false ← Save cost
├─ enable_lifecycle: false ← No archiving
└─ notifications: false ← Silent
```

### **Scenario 3: Production Safe Deployment**
```
workflow_dispatch with inputs:
├─ environment: prod
├─ dry_run: true ← Preview first
├─ enable_logging: true ← Required
├─ enable_versioning: true ← Data protection
├─ enable_lifecycle: true ← Cost optimization
├─ deployment_tags: Owner=DevOps,Compliance=PCI
└─ notifications: true ← Alert team
```

### **Scenario 4: Preview Before Deploy**
```
First run:
├─ environment: prod
├─ dry_run: true ← See what changes
└─ (Review the logs)

After approval, run again:
├─ environment: prod
├─ dry_run: false ← Actually deploy
└─ (All other settings same)
```

---

## 📊 Input Types

GitHub Actions supports different input types:

```yaml
type: choice           # Dropdown menu
  options:
    - option1
    - option2

type: string          # Text input field
  default: 'value'

type: boolean         # True/False toggle (in newer versions)
```

All our inputs use `choice` (dropdowns) and `string` (text fields) for clarity.

---

## 💡 Tips & Tricks

### **✅ Good Practices**
1. Always use `dry_run: true` before production deployments
2. Review CloudFormation diff from dry run
3. Add meaningful deployment_tags for tracking
4. Use verbose output when debugging
5. Keep notifications ON for prod

### **⚠️ Avoid These**
1. Don't skip tests in production (`skip_tests: true`)
2. Don't disable logging in production
3. Don't disable versioning in production
4. Don't manually edit values after running
5. Don't run multiple deployments simultaneously

### **🔒 Security**
1. Sensitive values use GitHub Secrets (not input parameters)
2. AWS credentials in Secrets, not in inputs
3. Tokens never exposed in workflow inputs
4. Deployment_tags can be public (no secrets!)

---

## 🔍 Viewing Input Values

After workflow runs, you can see what inputs were used:

```
Actions → Specific Run
├─ Run name: "AWS CDK Deployment - prod"
├─ Triggered by: Manual (workflow_dispatch)
├─ Inputs used:
│  ├─ environment: prod
│  ├─ dry_run: true
│  ├─ enable_logging: true
│  ├─ enable_versioning: true
│  └─ enable_lifecycle: false
└─ Show logs →
```

---

## 📚 Reference Table

| Workflow | Input | Type | Options | Default |
|----------|-------|------|---------|---------|
| **pipeline.yml** | verbose_output | choice | true/false | false |
| **pipeline.yml** | skip_tests | choice | true/false | false |
| **pipeline.yml** | notification_level | choice | all/errors-only/none | all |
| **deploy.yml** | environment | choice | dev/staging/prod | dev |
| **deploy.yml** | dry_run | choice | true/false | false |
| **deploy.yml** | enable_logging | choice | true/false | true |
| **deploy.yml** | enable_versioning | choice | true/false | true |
| **deploy.yml** | enable_lifecycle | choice | true/false | false |
| **deploy.yml** | deployment_tags | string | any | Team=Platform,... |
| **deploy.yml** | notifications | choice | true/false | true |

---

## 🚀 Quick Start Examples

### **Example 1: Run Pipeline with All Bells and Whistles**
```
1. Go to Actions → AWS CDK S3 Deployment Pipeline
2. Click Run workflow
3. Select:
   - verbose_output: true (see details)
   - skip_tests: false (run all)
   - notification_level: all (get alerts)
4. Click Run workflow
```

### **Example 2: Deploy to Dev Quickly**
```
1. Go to Actions → AWS CDK Deployment
2. Click Run workflow
3. Select:
   - environment: dev
   - dry_run: false (actually deploy)
   - enable_logging: false (save cost)
   - enable_versioning: false (save cost)
   - notifications: false (silent)
4. Click Run workflow
```

### **Example 3: Safe Production Deploy**
```
1. Go to Actions → AWS CDK Deployment
2. Click Run workflow
3. Select:
   - environment: prod
   - dry_run: true (PREVIEW FIRST)
   - enable_logging: true (required)
   - enable_versioning: true (required)
   - enable_lifecycle: true (optional)
   - deployment_tags: Owner=DevOps,Compliance=PCI
   - notifications: true (alert team)
4. Review logs carefully
5. If OK, run again with dry_run: false
```

---

## ❓ FAQ

**Q: Can I change inputs after starting a run?**
A: No, inputs are locked once the run starts. Create a new run with different inputs.

**Q: Are inputs case-sensitive?**
A: Yes, "true" and "True" are different. Use exact values from options.

**Q: Can I add new inputs?**
A: Yes, edit the workflow YAML file and add new inputs under `workflow_dispatch.inputs`.

**Q: Do inputs show in logs?**
A: Yes, input values are visible in run summary for auditing.

**Q: Can I set inputs programmatically?**
A: Yes, via GitHub CLI: `gh workflow run deploy.yml -f environment=prod`

---

## 🎉 You're Ready!

Now you can:
✅ Run pipeline with custom settings  
✅ Deploy with flexible configurations  
✅ Preview changes before deploying  
✅ Add custom tags to resources  
✅ Control notifications and verbosity  

**Go to Actions tab and start using these inputs!**
