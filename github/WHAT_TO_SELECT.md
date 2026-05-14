# GitHub Actions: What to Select - Complete Guide

## 🎯 Quick Navigation

Choose your scenario:
1. [**I want to test my code**](#scenario-1-test-pipeline) → Use `pipeline.yml`
2. [**I want to deploy to Dev**](#scenario-2-deploy-to-dev) → Use `deploy.yml`
3. [**I want to preview Production deployment**](#scenario-3-preview-prod-deployment) → Use `deploy.yml`
4. [**I want to deploy to Production**](#scenario-4-deploy-to-production) → Use `deploy.yml`
5. [**I want debug output**](#scenario-5-debug-mode) → Use `pipeline.yml`

---

## 📍 How to Access Inputs

```
1. GitHub.com → Your Repository
2. Click "Actions" (top tab)
3. Left sidebar: Select workflow
4. Click "Run workflow" button
5. Inputs dropdown appears
6. Make selections
7. Click "Run workflow"
```

---

## ✅ SCENARIO 1: Test Pipeline

**When:** You pushed code and want to verify it works  
**Workflow:** `AWS CDK S3 Deployment Pipeline`  
**Time:** ~2-3 minutes

### What to Select

```
┌────────────────────────────────────────────────┐
│ Workflow inputs                                │
│                                                │
│ verbose_output                                 │
│ ┌──────────────────────────────────┐          │
│ │ ◉ false (default)  ✓ SELECT THIS│          │
│ │ ○ true             (for debugging)          │
│ └──────────────────────────────────┘          │
│                                                │
│ skip_tests                                     │
│ ┌──────────────────────────────────┐          │
│ │ ◉ false (default)  ✓ SELECT THIS│          │
│ │ ○ true             (not recommended)        │
│ └──────────────────────────────────┘          │
│                                                │
│ notification_level                             │
│ ┌──────────────────────────────────┐          │
│ │ ◉ all (default)    ✓ SELECT THIS│          │
│ │ ○ errors-only      (alternate)   │          │
│ │ ○ none             (silent mode) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ [Run workflow]  [Cancel]                      │
└────────────────────────────────────────────────┘
```

### What Happens
```
✅ Stage 1: Code Validation
✅ Stage 2: Dependency Check
✅ Stage 3: Configuration Test
✅ Stage 4: CDK Synthesis
✅ Stage 5: Test & Report

Result: Your code is validated ✓
```

---

## ✅ SCENARIO 2: Deploy to Dev

**When:** You want to test deployment to development environment  
**Workflow:** `AWS CDK Deployment`  
**Time:** ~5-10 minutes  
**Cost Impact:** Minimal (only dev bucket created)

### What to Select

```
┌────────────────────────────────────────────────┐
│ Workflow inputs                                │
│                                                │
│ environment * (required)                       │
│ ┌──────────────────────────────────┐          │
│ │ ○ dev              ✓ SELECT THIS │          │
│ │ ○ staging                        │          │
│ │ ○ prod                           │          │
│ └──────────────────────────────────┘          │
│                                                │
│ dry_run                                        │
│ ┌──────────────────────────────────┐          │
│ │ ◉ false (default)  ✓ SELECT THIS │          │
│ │ ○ true             (preview only) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_logging                                 │
│ ┌──────────────────────────────────┐          │
│ │ ○ true                           │          │
│ │ ◉ false            ✓ SELECT THIS │          │
│ │                    (saves money)  │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_versioning                              │
│ ┌──────────────────────────────────┐          │
│ │ ○ true                           │          │
│ │ ◉ false            ✓ SELECT THIS │          │
│ │                    (saves money)  │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_lifecycle                               │
│ ┌──────────────────────────────────┐          │
│ │ ◉ false (default)  ✓ SELECT THIS │          │
│ │ ○ true             (for archives) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ deployment_tags                                │
│ ┌──────────────────────────────────┐          │
│ │ Team=Dev,Environment=Testing  ✓ │          │
│ │ (default is fine)                │          │
│ └──────────────────────────────────┘          │
│                                                │
│ notifications                                  │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false            (silent mode)  │          │
│ └──────────────────────────────────┘          │
│                                                │
│ [Run workflow]  [Cancel]                      │
└────────────────────────────────────────────────┘
```

### Summary Card

| Input | Select | Reason |
|-------|--------|--------|
| **environment** | `dev` | Development environment |
| **dry_run** | `false` | Actually create resources |
| **enable_logging** | `false` | Save cost in dev |
| **enable_versioning** | `false` | Save cost in dev |
| **enable_lifecycle** | `false` | No archiving needed |
| **deployment_tags** | (keep default) | Optional |
| **notifications** | `true` | Get alerts |

### What Happens
```
1. Pre-deployment checks ✓
2. Deploys to AWS Dev environment
3. Creates S3 bucket: my-app-dev-bucket
4. Sends you notification ✓

Result: Dev S3 bucket is live!
```

---

## ✅ SCENARIO 3: Preview Prod Deployment

**When:** Before deploying to production, see what will change  
**Workflow:** `AWS CDK Deployment`  
**Time:** ~3-5 minutes  
**Cost Impact:** None (dry run only)

### What to Select

```
┌────────────────────────────────────────────────┐
│ Workflow inputs                                │
│                                                │
│ environment * (required)                       │
│ ┌──────────────────────────────────┐          │
│ │ ○ dev                            │          │
│ │ ○ staging                        │          │
│ │ ○ prod             ✓ SELECT THIS │          │
│ └──────────────────────────────────┘          │
│                                                │
│ dry_run                                        │
│ ┌──────────────────────────────────┐          │
│ │ ○ false            (actually deploy)        │
│ │ ◉ true             ✓ SELECT THIS │          │
│ │                    (preview only) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_logging                                 │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false            (not for prod) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_versioning                              │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false            (not for prod) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_lifecycle                               │
│ ┌──────────────────────────────────┐          │
│ │ ○ false                          │          │
│ │ ◉ true             ✓ SELECT THIS │          │
│ │                    (cost saving)  │          │
│ └──────────────────────────────────┘          │
│                                                │
│ deployment_tags                                │
│ ┌──────────────────────────────────┐          │
│ │ Owner=DevOps,Compliance=PCI  ✓  │          │
│ │ (add your team info)              │          │
│ └──────────────────────────────────┘          │
│                                                │
│ notifications                                  │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false            (not for prod) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ [Run workflow]  [Cancel]                      │
└────────────────────────────────────────────────┘
```

### Summary Card

| Input | Select | Reason |
|-------|--------|--------|
| **environment** | `prod` | Production environment |
| **dry_run** | `true` | PREVIEW ONLY - don't deploy yet |
| **enable_logging** | `true` | Required for production |
| **enable_versioning** | `true` | Data protection |
| **enable_lifecycle** | `true` | Cost optimization |
| **deployment_tags** | Custom tags | Your team/compliance info |
| **notifications** | `true` | Alert team for review |

### What to Do Next

```
1. Workflow runs (no resources created)
2. Check the logs carefully
3. Review CloudFormation diff:
   - What new resources?
   - What changes to existing?
4. If OK → Run again with dry_run: false
5. If NOT OK → Fix code → Commit → Re-run
```

---

## ✅ SCENARIO 4: Deploy to Production

**When:** Ready to deploy after preview looks good  
**Workflow:** `AWS CDK Deployment`  
**Time:** ~5-10 minutes  
**Cost Impact:** Production bucket created  
**⚠️ ATTENTION:** This is REAL deployment!

### What to Select

```
┌────────────────────────────────────────────────┐
│ Workflow inputs                                │
│                                                │
│ environment * (required)                       │
│ ┌──────────────────────────────────┐          │
│ │ ○ dev                            │          │
│ │ ○ staging                        │          │
│ │ ○ prod             ✓ SELECT THIS │          │
│ │                    ⚠️ PRODUCTION! │          │
│ └──────────────────────────────────┘          │
│                                                │
│ dry_run                                        │
│ ┌──────────────────────────────────┐          │
│ │ ◉ false (default)  ✓ SELECT THIS │          │
│ │ ○ true             (would preview) │         │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_logging                                 │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false                          │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_versioning                              │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false                          │          │
│ └──────────────────────────────────┘          │
│                                                │
│ enable_lifecycle                               │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true             ✓ SELECT THIS │          │
│ │ ○ false            (auto-archive) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ deployment_tags                                │
│ ┌──────────────────────────────────┐          │
│ │ Owner=DevOps,Compliance=PCI  ✓  │          │
│ │ CostCenter=001,Team=Platform     │          │
│ └──────────────────────────────────┘          │
│                                                │
│ notifications                                  │
│ ┌──────────────────────────────────┐          │
│ │ ◉ true (default)   ✓ SELECT THIS │          │
│ │ ○ false                          │          │
│ └──────────────────────────────────┘          │
│                                                │
│ ⚠️  DOUBLE CHECK BEFORE CLICKING!              │
│ [Run workflow]  [Cancel]                      │
└────────────────────────────────────────────────┘
```

### Summary Card

| Input | Select | Reason |
|-------|--------|--------|
| **environment** | `prod` | Production environment |
| **dry_run** | `false` | **ACTUALLY DEPLOY** |
| **enable_logging** | `true` | Required for production |
| **enable_versioning** | `true` | Data protection |
| **enable_lifecycle** | `true` | Cost optimization + archiving |
| **deployment_tags** | Custom tags | Your team/compliance info |
| **notifications** | `true` | Alert team that prod is live |

### ⚠️ Before You Deploy

- [ ] Already ran dry_run and reviewed changes
- [ ] Got approval from team lead
- [ ] Reviewed CloudFormation diff
- [ ] Notified stakeholders
- [ ] Have rollback plan ready
- [ ] Verified all settings above

### What Happens
```
1. Pre-deployment checks ✓
2. Requires approval for production
3. Deploy to AWS Production
4. Create S3 bucket: my-app-prod-bucket
5. Enable all security features ✓
6. Send team notification ✓

Result: Production S3 bucket is LIVE! 🚀
```

---

## ✅ SCENARIO 5: Debug Mode

**When:** Something failed and you need to see detailed output  
**Workflow:** `AWS CDK S3 Deployment Pipeline`  
**Time:** ~3-5 minutes  
**Use Case:** Troubleshooting test failures

### What to Select

```
┌────────────────────────────────────────────────┐
│ Workflow inputs                                │
│                                                │
│ verbose_output                                 │
│ ┌──────────────────────────────────┐          │
│ │ ○ false                          │          │
│ │ ◉ true             ✓ SELECT THIS │          │
│ │                    (debug output) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ skip_tests                                     │
│ ┌──────────────────────────────────┐          │
│ │ ◉ false (default)  ✓ SELECT THIS │          │
│ │ ○ true             (don't skip)   │          │
│ └──────────────────────────────────┘          │
│                                                │
│ notification_level                             │
│ ┌──────────────────────────────────┐          │
│ │ ○ all                            │          │
│ │ ◉ errors-only      ✓ SELECT THIS │          │
│ │ ○ none                           │          │
│ │                    (only on fail) │          │
│ └──────────────────────────────────┘          │
│                                                │
│ [Run workflow]  [Cancel]                      │
└────────────────────────────────────────────────┘
```

### Summary Card

| Input | Select | Reason |
|-------|--------|--------|
| **verbose_output** | `true` | See detailed debug logs |
| **skip_tests** | `false` | Run all tests to find issue |
| **notification_level** | `errors-only` | Only notify if it fails |

### What to Check in Logs
```
Expand each stage and look for:
1. ❌ Which stage failed?
2. 🔴 What error message?
3. 📋 What's the full stack trace?
4. 💡 Fix the issue
5. 🔄 Commit and re-run
```

---

## 🎯 Quick Reference Table

### Pipeline Testing Inputs

| Scenario | verbose_output | skip_tests | notification_level |
|----------|---|---|---|
| Normal test | `false` | `false` | `all` |
| **Debug mode** | **`true`** | **`false`** | **`errors-only`** |
| Fast test | `false` | `true` | `none` |
| Important test | `false` | `false` | `all` |

### Deployment Inputs

| Scenario | environment | dry_run | logging | versioning | lifecycle | notifications |
|----------|---|---|---|---|---|---|
| **Test Dev** | **`dev`** | **`false`** | **`false`** | **`false`** | **`false`** | **`true`** |
| **Preview Prod** | **`prod`** | **`true`** | **`true`** | **`true`** | **`true`** | **`true`** |
| **Deploy Prod** | **`prod`** | **`false`** | **`true`** | **`true`** | **`true`** | **`true`** |
| Test Staging | `staging` | `false` | `true` | `true` | `false` | `true` |

---

## 🚀 Step-by-Step: Deploy to Production (Safe Way)

### Day 1: Code & Test
```
1. Write code locally
2. Commit to feature branch
3. Pipeline auto-runs (validation) ✓

4. Merge to main branch
5. Pipeline auto-runs again (validation) ✓

6. Code is ready!
```

### Day 2: Preview Deployment
```
1. Go to Actions → AWS CDK Deployment
2. Click "Run workflow"
3. Select inputs (see Scenario 3 above)
4. Click "Run workflow"

5. Wait for dry_run to complete
6. Check logs carefully
7. Review CloudFormation diff
8. Share with team for approval

9. If everything OK → Proceed to deployment
10. If issues → Fix code → Go to Day 1
```

### Day 3: Production Deployment
```
1. Go to Actions → AWS CDK Deployment
2. Click "Run workflow"
3. Select inputs (see Scenario 4 above)

⚠️  CHECKLIST:
   [ ] Pre-deployment verified OK
   [ ] Team approved changes
   [ ] Backup plan ready
   [ ] Stakeholders notified

4. Click "Run workflow"
5. APPROVE when prompted (for prod)
6. Monitor deployment
7. Get success notification ✓

8. Verify in AWS console
9. Production is LIVE! 🎉
```

---

## ✅ Verification Checklist

After deployment, verify:

### For Dev Deployment
- [ ] S3 bucket exists in AWS
- [ ] Bucket name is `my-app-dev-bucket`
- [ ] No versioning (to save cost)
- [ ] No logging configured
- [ ] Public access is blocked

### For Production Deployment
- [ ] S3 bucket exists in AWS
- [ ] Bucket name is `my-app-prod-bucket`
- [ ] Versioning is ENABLED
- [ ] Logging is ENABLED (to logs bucket)
- [ ] Public access is BLOCKED
- [ ] Lifecycle rules configured
- [ ] Encryption enabled
- [ ] Tags applied correctly

---

## 🎓 Learning Path

**Start here if new:**
1. ✅ Run Scenario 1 (Test Pipeline) - Get familiar with Actions
2. ✅ Run Scenario 2 (Deploy Dev) - See live deployment
3. ✅ Run Scenario 5 (Debug Mode) - Learn troubleshooting
4. ✅ Run Scenario 3 (Preview Prod) - Understand dry-run
5. ✅ Run Scenario 4 (Deploy Prod) - Real deployment

**Each one takes 5 minutes and you'll be an expert!**

---

## 💡 Pro Tips

### ✅ DO These
```
✓ Always use dry_run: true for production first
✓ Review logs before making selections
✓ Keep verbose_output: true during debugging
✓ Add meaningful deployment_tags
✓ Enable notifications for important deployments
✓ Test in dev before staging before prod
```

### ❌ DON'T Do These
```
✗ Don't skip_tests: true for production
✗ Don't disable logging in production
✗ Don't disable versioning in production
✗ Don't deploy during business hours without notice
✗ Don't run multiple deployments at same time
```

---

## ❓ FAQ

**Q: I selected wrong inputs, what do I do?**
A: It's OK! You can stop the workflow and run again with correct inputs.

**Q: Can I see what inputs I used last time?**
A: Yes! Go to Actions → Click previous run → See inputs under "Summary"

**Q: What if dry_run shows errors?**
A: Perfect! That's what it's for. Fix the code, commit, and run dry_run again.

**Q: Can I change inputs while workflow is running?**
A: No, inputs are locked. Stop and create new run with different inputs.

**Q: How long should each scenario take?**
A: Pipeline test: 2-3 min, Dev deploy: 5 min, Prod deploy: 5-10 min

---

## 🎉 You're Ready!

Pick your scenario above, make the selections, and click "Run workflow"!

**Good luck! 🚀**
