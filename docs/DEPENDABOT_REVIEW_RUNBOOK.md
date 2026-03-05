# Dependabot PR Review Runbook

This guide covers the process for reviewing and testing grouped Dependabot PRs before merging them into the `master` branch.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Weekly Review Schedule](#weekly-review-schedule)
- [Review Process](#review-process)
    - [1. Identify Open Dependabot PRs](#1-identify-open-dependabot-prs)
    - [2. Review PR Changes](#2-review-pr-changes)
    - [3. Create Local Test Branch](#3-create-local-test-branch)
    - [4. Run Automated Tests](#4-run-automated-tests)
    - [5. Manual Testing (if needed)](#5-manual-testing-if-needed)
    - [6. Approve and Merge](#6-approve-and-merge)
- [Handling Multiple Dependabot PRs](#handling-multiple-dependabot-prs)
- [Rollback Procedure](#rollback-procedure)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Best Practices](#best-practices)
- [Useful Commands Cheat Sheet](#useful-commands-cheat-sheet)

## Overview

Dependabot is configured to create grouped dependency update PRs weekly (Mondays at 09:00). You should expect to see up to 3 PRs:

1. **Python Dependencies** (`python-dependencies` group) - Major version updates for pip packages
2. **NPM Dependencies** (`npm-dependencies` group) - Major version updates for npm packages
3. **GitHub Actions** (`github-dependencies` group) - All updates to GitHub Actions

Minor and patch updates are ignored per the configuration in `.github/dependabot.yml`.

## Prerequisites

Ensure you have the following installed and configured:

- Git
- Access to the repository with write permissions
- All development dependencies installed via `make install`

See the [Development Guide](./DEVELOPMENT_GUIDE.md) for specific tool version requirements.

**Quick Setup:**

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd validated-relationships-service-api

# Install all dependencies
make install
```

## Weekly Review Schedule

**Recommended Review Time:** Monday afternoons or Tuesday mornings (after Dependabot creates PRs at 09:00 Monday)

**Estimated Time Required:**

- Simple review (no breaking changes): 15-30 minutes
- Complex review (with breaking changes): 1-2 hours

## Review Process

### 1. Identify Open Dependabot PRs

First, check what Dependabot PRs are currently open:

**Using GitHub Web UI:**

- Navigate to the repository on GitHub
- Click on "Pull requests" tab
- Filter by author: `author:app/dependabot[bot]`
- Or use the direct URL: `https://github.com/OWNER/REPO/pulls?q=is:pr+is:open+author:app/dependabot`

**Using Git Commands:**

```bash
# List remote branches containing "dependabot"
git fetch origin
git branch -r | grep dependabot
```

You should see PRs with titles like:

- "Bump the python-dependencies group with X updates" (for grouped Python updates)
- "Bump aiohttp from X.X.X to Y.Y.Y" (for individual Python package updates)
- "Bump cryptography from X.X.X to Y.Y.Y" (for individual Python package updates)
- "Bump the npm-dependencies group with X updates" (for grouped npm updates)
- "Bump basic-ftp from X.X.X to Y.Y.Y" (for individual npm package updates)
- "Bump the github-dependencies group with X updates" (for grouped GitHub Actions updates)

**Note:** You may see both grouped PRs (multiple packages) and individual PRs (single packages) depending on:

- Whether updates are available for multiple packages simultaneously
- Security updates (which may bypass grouping)
- Whether grouped updates failed and individual PRs were created instead

### 2. Review PR Changes

For each Dependabot PR, review the changes:

**Using GitHub Web UI:**

- Click on the PR title to view details
- Click "Files changed" tab to see the diff
- Click "Checks" tab to see CI/CD status

**Using Git Commands:**

```bash
# Fetch the PR branch
git fetch origin pull/<PR-NUMBER>/head:pr-<PR-NUMBER>

# View the diff
git diff main...pr-<PR-NUMBER>

# View changed files
git diff --name-only main...pr-<PR-NUMBER>
```

**What to look for:**

- ✅ Check if CI/CD checks are passing
- ✅ Review the changelog/release notes for each updated dependency
- ✅ Look for breaking changes in major version updates
- ⚠️ Pay special attention to dependencies that affect:
    - API schema validation (`openapi-schema-validator`, etc.)
    - Testing frameworks (`pytest`, `newman`, etc.)
    - Build tools (`webpack`, `poetry`, etc.)

**Check Release Notes:**

```bash
# For Python packages, check PyPI
# Example: https://pypi.org/project/package-name/#history

# For npm packages, check npm or GitHub
# Example: https://www.npmjs.com/package/package-name?activeTab=versions
```

### 3. Create Local Test Branch

Create a test branch to verify the changes locally:

**Using Git Commands:**

```bash
# Ensure you're on the latest master
git checkout master
git pull origin master

# Fetch all branches
git fetch origin

# Find the dependabot branch name
git branch -r | grep dependabot

# Checkout the dependabot branch directly
git checkout dependabot/npm_and_yarn/npm-dependencies-abc123

# Or fetch PR by number and checkout
git fetch origin pull/<PR-NUMBER>/head:dependabot-pr-<PR-NUMBER>
git checkout dependabot-pr-<PR-NUMBER>
```

> **Note:** Dependabot branches may be behind master if other PRs have been merged since the Dependabot PR was created. If you encounter issues or want to test against the latest master, you can ask Dependabot to rebase:
>
> **On GitHub Web UI:**
>
> 1. Navigate to the Dependabot PR on GitHub
> 2. Scroll to the bottom (comment section)
> 3. Add a comment: `@dependabot rebase`
> 4. Click "Comment"
>
> Dependabot will automatically rebase the PR branch against the current master branch.
>
> **Other useful Dependabot commands:**
>
> - `@dependabot recreate` - Recreate the PR from scratch
> - `@dependabot merge` - Merge the PR (if checks pass)
> - `@dependabot close` - Close the PR

**Alternative: Create a named test branch**

```bash
# Create a test branch from the dependabot branch
git checkout master
git pull origin master
git checkout -b test/dependabot-<ecosystem>-$(date +%Y%m%d)
git merge origin/dependabot/<ecosystem>/<group-name>
```

### 4. Run Automated Tests

Run the full test suite to verify nothing is broken:

#### Install Dependencies

```bash
# Install Node dependencies
make install-node

# Install Python dependencies (if updated)
make install-python

# Or install everything
make install
```

#### Run Linting

```bash
# Run Python linting
make lint

# Run Python formatting check
make format

# If formatting fails, you may need to apply formatting
make format-apply
```

#### Run Schema Validation

```bash
# Validate all schema examples
make schema-all

# Or validate specific schemas:
make schema-get-consent
make schema-post-consent
make schema-patch-consent
make schema-related-person
make schema-questionnaire
make schema-errors
```

#### Run Unit/Integration Tests

```bash
# Run Python tests (requires APIGEE_ACCESS_TOKEN)
make test

# Run smoke tests
make smoketest
```

#### Test OpenAPI Specification

```bash
# Publish the spec to check for errors
make publish

# Check the build output
ls -la build/

# Serve the spec locally to preview
make serve
# Open browser to http://localhost:8080
```

#### Test Postman Collection (if npm updated)

```bash
# Generate Postman collection
make generate-postman-collection

# Test against sandbox
make test-postman-collection SANDBOX_BASE_URL=https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4
```

### 5. Manual Testing (if needed)

For major version updates or if automated tests reveal issues:

#### Test Sandbox

```bash
# Start the sandbox locally (if sandbox dependencies were updated)
cd sandbox
poetry run python -m flask run --port 5000

# Test endpoints manually
curl http://localhost:5000/_ping
curl http://localhost:5000/_status
```

#### Review Breaking Changes

If tests fail or you notice breaking changes:

1. **Document the issue:**

    **Using GitHub Web UI:**
    - Navigate to the PR on GitHub
    - Scroll to the bottom and add a comment in the comment box
    - Include test output and description of the issue
    - Include relevant test output

2. **Check for migration guides:**
    - Look for UPGRADE.md, MIGRATION.md, or CHANGELOG.md in the dependency's repository
    - Check if there are code changes required

3. **Fix issues if possible:**

    ```bash
    # Make necessary code changes
    git add .
    git commit -m "fix: update code for dependency upgrade"

    # Push to a new branch (don't push to dependabot's branch)
    git push origin HEAD:fix/dependabot-<PR-NUMBER>
    ```

    **Create a new PR with GitHub Web UI:**
    - Navigate to the repository on GitHub
    - Click "Pull requests" → "New pull request"
    - Select your branch `fix/dependabot-<PR-NUMBER>`
    - Add title and description referencing the original Dependabot PR
    - Click "Create pull request"

### 6. Approve and Merge

Once all tests pass:

**Using GitHub Web UI:**

- Navigate to the PR on GitHub
- Click "Review changes" → "Approve" → "Submit review"
- Scroll down and click "Squash and merge" (or "Rebase and merge")
- Confirm the merge
- Check "Delete branch" option

**Clean up local branches:**

```bash
git checkout master
git pull origin master
git branch -d <dependabot-branch-name>
```

## Handling Multiple Dependabot PRs

If you have multiple ecosystem PRs open simultaneously, you can:

### Option A: Test Each Separately (Recommended)

Test and merge each PR individually following the process above. This makes it easier to identify which dependency causes issues if tests fail.

**Using Git Commands:**

```bash
# Test Python dependencies first
git fetch origin
git checkout dependabot/pip/python-dependencies-...
make install-python
make lint format
make schema-all
make test

# If tests pass, merge it via GitHub Web UI

# Then test npm dependencies
git checkout master
git pull origin master
git checkout dependabot/npm_and_yarn/npm-dependencies-...
make install-node
make publish
make generate-postman-collection

# If tests pass, merge it via GitHub Web UI
```

### Option B: Combine and Test Together

If you want to test all updates together before merging:

> ⚠️ **Warning:** Merging multiple Dependabot branches together may result in merge conflicts, especially if:
>
> - Multiple PRs update the same dependency to different versions
> - Both `poetry.lock` and `package-lock.json` are modified by different PRs
> - PRs modify overlapping sections of configuration files
>
> **If you encounter conflicts and want to undo the merge:**
>
> ```bash
> # Abort the merge and return to pre-merge state
> git merge --abort
>
> # Your branch will be back to the state before the merge command
> # You can then try a different approach or merge PRs individually
> ```
>
> **If you want to resolve conflicts:**
>
> - Resolve them manually by choosing the appropriate version
> - Regenerate lock files (`poetry lock`, `npm install`)
> - Test thoroughly after resolving conflicts
> - Complete the merge with `git commit`

**Using Git Commands:**

```bash
# Create a combined test branch
git checkout master
git pull origin master
git checkout -b test/all-dependabot-$(date +%Y%m%d)

# List and merge all dependabot branches
git fetch origin
git branch -r | grep dependabot | while read branch; do
  echo "Merging $branch"
  git merge --no-ff "$branch" -m "Merge $branch for testing"
done

# Run full test suite
make install
make lint format
make schema-all
make test
make publish

# If all tests pass, merge the original PRs individually via GitHub Web UI

# Clean up test branch
git checkout master
git branch -D test/all-dependabot-$(date +%Y%m%d)
```

## Rollback Procedure

If a merged Dependabot PR causes issues in production:

### Immediate Rollback

```bash
# Find the merge commit
git log --oneline --grep="dependabot"

# Revert the merge commit
git revert -m 1 <merge-commit-sha>

# Push the revert
git push origin master

# Create a PR for the revert
gh pr create --title "Revert: Dependabot updates" \
  --body "Reverting #<PR-NUMBER> due to [issue description]"
```

### Fix Forward (Preferred)

```bash
# Create a fix branch
git checkout -b fix/dependency-issue

# Make necessary fixes
# ... edit files ...

git add .
git commit -m "fix: resolve issue from dependency update"

git push origin fix/dependency-issue
```

**Create PR with GitHub Web UI:**

- Navigate to repository on GitHub
- Click "Pull requests" → "New pull request"
- Select your branch `fix/dependency-issue`
- Add title and description
- Click "Create pull request"

## Common Issues and Solutions

### Issue: Poetry lock file out of sync

**Symptom:** `poetry install` fails with lock file errors

**Solution:**

```bash
# Update the lock file
poetry lock --no-update

# Or regenerate it
poetry lock

# Commit the updated lock file
git add poetry.lock
git commit -m "chore: update poetry lock file"
```

### Issue: npm peer dependency conflicts

**Symptom:** `npm install` shows peer dependency warnings

**Solution:**

```bash
# Install with legacy peer deps (already in Makefile)
npm install --legacy-peer-deps

# If issues persist, check package.json for conflicting versions
```

### Issue: Schema validation fails after OpenAPI validator update

**Symptom:** `make schema-all` fails after updating `openapi-schema-validator`

**Solution:**

```bash
# Check if the schema needs updates
poetry run python scripts/validate_schema.py operationoutcome <failing-file>

# Common fix: Update schema to match new validator requirements
# Check the validator's changelog for breaking changes
```

### Issue: Flake8 or Black failures after dependency update

**Symptom:** `make lint` or `make format` fails

**Solution:**

```bash
# Apply black formatting
make format-apply

# Check flake8 config if needed
cat .flake8

# May need to update .flake8 config for new rules
```

### Issue: GitHub Actions fail after actions update

**Symptom:** CI/CD pipeline fails after updating `github-dependencies`

**Solution:**

```bash
# Check the action's changelog for breaking changes
# Common issues:
# - Changed input/output names
# - Deprecated features removed
# - Node version requirements changed

# Update workflow files in .github/workflows/
vim .github/workflows/<failing-workflow>.yml
```

### Issue: Tests pass locally but fail in CI

**Symptom:** Local tests pass but GitHub Actions or Azure DevOps fails

**Solution:**

```bash
# Check environment differences
# - Python version
# - Node version
# - Environment variables

# Try running tests in the same way CI does
poetry run pytest -v --color=yes

# Check CI logs for specific error messages
gh run list --workflow=<workflow-name>
gh run view <run-id>
```

## Best Practices

1. **Review Timing:** Review Dependabot PRs within 1-2 days of creation
2. **Batch Review:** Try to review all ecosystem PRs together for consistency
3. **Document Issues:** Always comment on PRs when you find issues
4. **Test Thoroughly:** Don't skip tests even for "simple" updates
5. **Monitor After Merge:** Check CI/CD pipelines after merging
6. **Keep Notes:** Document any issues encountered for future reference
7. **Stay Informed:** Subscribe to notifications for critical dependencies
8. **Security First:** Prioritize security updates even if they require more work
9. **Communicate:** Let the team know if you're blocking or delaying a merge
10. **Learn from Failures:** Document breaking changes for future reference

## Useful Commands Cheat Sheet

### Git Commands

```bash
# List remote dependabot branches
git fetch origin
git branch -r | grep dependabot

# Checkout a PR branch (find branch name first)
git checkout dependabot/npm_and_yarn/npm-dependencies-abc123

# Or fetch PR by number
git fetch origin pull/<PR-NUMBER>/head:pr-<PR-NUMBER>
git checkout pr-<PR-NUMBER>

# View diff from master
git diff master...HEAD

# List changed files
git diff --name-only master...HEAD

# View commit messages
git log master..HEAD

# Merge PR locally (then push to master)
git checkout master
git merge --squash pr-<PR-NUMBER>
git commit -m "Merge dependabot PR #<PR-NUMBER>"
git push origin master
```

### Testing Commands

```bash
# Run full test suite
make install && make lint && make format && make schema-all && make test

# Install dependencies
make install-node      # Install npm packages
make install-python    # Install Python packages
make install           # Install everything

# Run linting and formatting
make lint              # Check Python code style
make format            # Check Python formatting
make format-apply      # Apply Python formatting

# Run schema validation
make schema-all        # Validate all schemas
make schema-get-consent
make schema-post-consent
make schema-patch-consent

# Run tests
make test              # Run all tests
make smoketest         # Run smoke tests only

# Build and publish
make publish           # Generate OpenAPI spec
make serve             # Serve spec locally
```

## Additional Resources

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Project Development Guide](./DEVELOPMENT_GUIDE.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [NHS Digital API Producer Zone](https://nhsd-confluence.digital.nhs.uk/display/APM)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

**Last Updated:** March 2026
