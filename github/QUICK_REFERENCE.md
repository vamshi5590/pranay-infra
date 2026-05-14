# 🎯 GitHub Actions Quick Reference Card

Print this or bookmark it!

---

## 🚀 SCENARIO SELECTOR

### I want to...

**Test my code?**
```
Go to: Actions → AWS CDK S3 Deployment Pipeline
Select: verbose_output=false, skip_tests=false, notifications=all
Click: Run workflow ✓
```

**Deploy to Dev?**
```
Go to: Actions → AWS CDK Deployment
Select: environment=dev, dry_run=false, logging=false, versioning=false
Click: Run workflow ✓
```

**Preview Production?**
```
Go to: Actions → AWS CDK Deployment
Select: environment=prod, dry_run=true, logging=true, versioning=true
Click: Run workflow ✓
Review logs carefully!
```

**Deploy to Production?**
```
Go to: Actions → AWS CDK Deployment
Select: environment=prod, dry_run=false, logging=true, versioning=true
Click: Run workflow ✓
⚠️  Requires approval!
```

**Debug a failure?**
```
Go to: Actions → AWS CDK S3 Deployment Pipeline
Select: verbose_output=true, skip_tests=false, notifications=errors-only
Click: Run workflow ✓
Check detailed logs!
```

---

## 📋 COPY-PASTE CHECKLISTS

### Testing Pipeline
```
☐ verbose_output = false
☐ skip_tests = false
☐ notification_level = all
☐ Click Run workflow
```

### Dev Deployment
```
☐ environment = dev
☐ dry_run = false
☐ enable_logging = false
☐ enable_versioning = false
☐ enable_lifecycle = false
☐ deployment_tags = (optional)
☐ notifications = true
☐ Click Run workflow
```

### Production Preview
```
☐ environment = prod
☐ dry_run = true
☐ enable_logging = true
☐ enable_versioning = true
☐ enable_lifecycle = true
☐ deployment_tags = (add yours)
☐ notifications = true
☐ Click Run workflow
☐ Review logs!
```

### Production Deployment
```
☐ environment = prod
☐ dry_run = false
☐ enable_logging = true
☐ enable_versioning = true
☐ enable_lifecycle = true
☐ deployment_tags = (add yours)
☐ notifications = true
☐ Click Run workflow
☐ Approve when prompted
```

---

## 🎨 VISUAL GUIDE

```
GitHub Repository
│
├─ Code tab (for coding)
├─ Issues tab (for tracking)
│
└─ ⭐ Actions tab (YOU ARE HERE!)
    │
    ├─ Left Sidebar:
    │  ├─ All workflows
    │  ├─ AWS CDK S3 Deployment Pipeline (testing)
    │  └─ AWS CDK Deployment (deployment)
    │
    ├─ Main Area:
    │  ├─ Recent runs (see past results)
    │  └─ [Run workflow ▼] ← Click here!
    │
    └─ After clicking:
       ├─ Inputs dropdown appears
       ├─ Make your selections
       └─ Click "Run workflow"
```

---

## 🔑 INPUT OPTIONS AT A GLANCE

### Pipeline Workflow Inputs

| Input | Options | Pick |
|-------|---------|------|
| **verbose_output** | `false`, `true` | `false` normally, `true` for debugging |
| **skip_tests** | `false`, `true` | `false` (always) |
| **notification_level** | `all`, `errors-only`, `none` | `all` for dev, `errors-only` for debug |

### Deployment Workflow Inputs

| Input | Options | Pick |
|-------|---------|------|
| **environment** | `dev`, `staging`, `prod` | Depends on target |
| **dry_run** | `false`, `true` | `true` before prod, `false` to deploy |
| **enable_logging** | `true`, `false` | `false` for dev, `true` for prod |
| **enable_versioning** | `true`, `false` | `false` for dev, `true` for prod |
| **enable_lifecycle** | `false`, `true` | `false` for dev, `true` for prod/archive |
| **deployment_tags** | Any text | Add your team info |
| **notifications** | `true`, `false` | `true` (recommended) |

---

## ⏱️ TIME ESTIMATES

| Action | Time | Frequency |
|--------|------|-----------|
| Run tests | 2-3 min | Every commit |
| Deploy Dev | 5 min | Multiple times daily |
| Preview Prod | 3-5 min | Before prod deployment |
| Deploy Prod | 5-10 min | Rarely (careful!) |

---

## ✅ BEFORE/AFTER CHECKLIST

### Before Running Test
- [ ] Code committed
- [ ] No uncommitted changes
- [ ] Ready to wait 2-3 minutes

### Before Dev Deployment
- [ ] Pipeline tests passed
- [ ] Code merged to main
- [ ] Casual testing OK

### Before Prod Preview
- [ ] Pipeline tests passed
- [ ] Code reviewed
- [ ] Team notified
- [ ] Ready to review changes

### Before Prod Deployment
- [ ] Dry run successful
- [ ] Team approved
- [ ] Backup plan ready
- [ ] Change window approved
- [ ] Stakeholders notified

---

## 🔍 WHERE TO FIND RESULTS

```
After clicking "Run workflow"...

Go to: Actions tab → Specific workflow
Look for:
├─ Status: ✅ Passed or ❌ Failed
├─ Duration: How long it took
├─ Click to expand:
│  ├─ Stage name
│  ├─ Logs (detailed output)
│  └─ Errors (if any)
└─ Share link: Copy and send to team
```

---

## 🚨 COMMON MISTAKES

| Mistake | Fix |
|---------|-----|
| Deployed with dry_run=true | No worries, no resources created. Deploy again with dry_run=false |
| Selected prod instead of dev | Stop workflow, run new one with dev |
| Didn't read dry_run logs | Can't undo! But good learning for next time |
| Enabled logging in dev | Extra costs, can disable later in AWS |
| Deployed at wrong time | Check AWS console, can delete bucket if needed |

---

## 💬 WHAT EACH INPUT DOES

### verbose_output
- `false` = Normal output ← Pick this usually
- `true` = Show every detail (for debugging)

### skip_tests
- `false` = Run all tests ← Pick this always
- `true` = Skip tests (risky!)

### notification_level
- `all` = Notify on everything ← Pick for important
- `errors-only` = Notify only on failures ← Pick for debugging
- `none` = No notifications (silent)

### environment
- `dev` = Development bucket ← Pick for testing
- `staging` = Staging bucket ← Pick for pre-prod testing
- `prod` = Production bucket ← Pick carefully!

### dry_run
- `false` = Actually create resources ← Pick to deploy
- `true` = Preview only, no changes ← Pick before prod

### enable_logging
- `true` = Track all bucket access ← Required for prod
- `false` = No access logs ← OK for dev (saves cost)

### enable_versioning
- `true` = Keep object history ← Required for prod
- `false` = Only current version ← OK for dev

### enable_lifecycle
- `false` = Keep forever ← Pick normally
- `true` = Auto-archive old objects ← Pick for cost savings

### deployment_tags
- Any text = Add metadata to resources
- Example: `Owner=John,Team=DevOps,Project=S3`

### notifications
- `true` = Send alerts ← Recommended
- `false` = Silent mode

---

## 🎓 FIRST-TIME USER PATH

```
Step 1: Go to GitHub Actions tab
        ↓
Step 2: Select "AWS CDK S3 Deployment Pipeline"
        ↓
Step 3: Click "Run workflow"
        ↓
Step 4: Keep all defaults, click "Run workflow"
        ↓
Step 5: Watch it run (2-3 minutes)
        ↓
Step 6: See green checkmarks ✓
        ↓
Step 7: Repeat with different options
        ↓
Step 8: Now you're an expert! 🎉
```

---

## 📞 QUICK HELP

**Q: Where do I click?**
A: Actions tab → Select workflow → Run workflow button

**Q: What if something goes wrong?**
A: Check logs! Click the failed step → Expand → Read error message

**Q: Can I stop a running workflow?**
A: Yes! Click "Cancel" on the workflow page

**Q: How do I see past runs?**
A: Actions tab → Scroll down → See "Recent runs"

**Q: Where is my bucket after deployment?**
A: AWS Console → S3 → Look for "my-app-dev-bucket" or similar

---

## 🎯 DECISION TREE

```
Are you testing code?
├─ YES → Use pipeline.yml (testing)
└─ NO → Are you deploying?
        ├─ YES → Use deploy.yml (deployment)
        │       ├─ To dev?
        │       │  └─ environment=dev, dry_run=false
        │       ├─ To prod?
        │       │  ├─ First time?
        │       │  │  └─ environment=prod, dry_run=true
        │       │  └─ After reviewing?
        │       │     └─ environment=prod, dry_run=false
        │       └─ Need to debug?
        │          └─ Check verbose_output=true
        └─ NO → What are you doing?
```

---

## 📱 Mobile Guide

Even on your phone:

1. GitHub app → Your repo
2. Tap "Actions" 
3. Tap workflow name
4. Tap "Run workflow" button
5. Fill in inputs (dropdown + text)
6. Tap "Run workflow"
7. Wait for ✅ or ❌

---

## 🏁 FINAL CHECKLIST

Before you start, you have:
- [ ] GitHub account with repo
- [ ] Read this guide
- [ ] Opened GitHub Actions tab
- [ ] Picked your scenario
- [ ] Ready to click "Run workflow"

You're ready! 🚀

---

## 📖 FULL GUIDES

For more details, see:
- **INPUTS_GUIDE.md** - Detailed input documentation
- **WORKFLOWS_GUIDE.md** - Complete workflow guide
- **WHAT_TO_SELECT.md** - Scenario-based guide
- **README.md** - Project overview

---

**Last Updated:** May 14, 2026  
**Version:** 1.0  
**For Questions:** See WORKFLOWS_GUIDE.md FAQ section
