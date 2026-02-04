# GitHub Actions Workflow Setup & Usage Guide
##  Overview
Your project now has a complete GitHub Actions CI/CD pipeline configured with automated testing, linting, and security scanning. This guide explains how to use and maintain it.
##  What the Workflow Does
### Automatic Triggers
The workflow runs automatically when you:
- Push code to `main` or `develop` branches
- Open/update pull requests to `main` or `develop` branches
### Three Parallel Jobs
#### 1. **Test Job** (Runs first)
Tests your code on 4 Python versions in parallel:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
Each version:
- Installs dependencies (PyQt5, pycryptodome, pytest, pytest-cov)
- Runs your test suite with coverage
- Reports coverage to Codecov
**Expected Duration:** 2-5 minutes per version
#### 2. **Lint Job** (Runs in parallel)
Checks code quality with three tools:
- **Black**: Enforces consistent code formatting
- **isort**: Ensures consistent import ordering
- **flake8**: Checks for style violations and errors
**Expected Duration:** 1-2 minutes
#### 3. **Security Job** (Runs in parallel)
Scans code for security issues:
- **Bandit**: Finds common security problems
- Runs non-blocking (doesn't fail the workflow)
**Expected Duration:** 1-2 minutes
##  Getting Started
### Step 1: Commit the Workflow File
```bash
git add .github/workflows/main.yml
git commit -m "Add GitHub Actions CI/CD workflow"
git push origin main
```
### Step 2: Check GitHub Actions
1. Go to your repository on GitHub
2. Click "Actions" tab
3. You'll see your workflow run
### Step 3: Monitor the Run
- Watch the workflow execute
- Check each job's status
- Click on failed jobs to see errors
### Step 4: View Results
- **Tests**: See pytest output and coverage
- **Linting**: See any formatting issues
- **Security**: See security findings
- **Coverage**: Reports appear on Codecov (if configured)
##  Understanding the Workflow Status
###  All Green (Success)
```
 test (Python 3.8)
 test (Python 3.9)
 test (Python 3.10)
 test (Python 3.11)
 lint
 security
```
All checks passed! Your code is ready to merge.
###  Red (Failed)
Check the failed job:
- **test**: Fix failing tests
- **lint**: Run formatter/linter locally
- **security**: Address security findings
###  Yellow (In Progress)
The workflow is still running. Wait for it to complete.
##  Local Testing Before Pushing
### Test Locally First
```bash
# Run all tests
pytest tests/ -v
# Run with coverage
pytest tests/ -v --cov=.
# Run specific test
pytest tests/test_auth.py -v
```
### Lint Locally
```bash
# Check formatting with black
black --check .
# Fix formatting with black
black .
# Check imports with isort
isort --check-only .
# Fix imports with isort
isort .
# Check style with flake8
flake8 .
```
### Security Check Locally
```bash
# Run bandit
bandit -r . -ll
```
##  Troubleshooting
### Test Failure in Workflow but Passes Locally
- Ensure you're using the same Python version
- Check if environment variables are different
- Verify all dependencies are installed
### Linting Failure
- Run formatters locally: `black .` and `isort .`
- Commit the formatted code
- Push again
### Security Warnings
- Review findings carefully
- Fix critical issues
- Document or suppress non-critical issues
### Workflow Won't Run
1. Check `.github/workflows/main.yml` exists
2. Verify syntax: `pip install pyyaml && python -c "import yaml; yaml.safe_load(open('.github/workflows/main.yml'))"`
3. Check branch names match (main, develop)
##  Monitoring & Maintenance
### Weekly Check
- Review failed workflows
- Monitor test coverage trends
- Address security findings
### Monthly Update
- Check for updates to GitHub Actions versions
- Review Python version support
- Update dependencies if needed
### Before Major Release
- Ensure all tests pass on all Python versions
- Run security scan and address issues
- Review code coverage (aim for >80%)
##  Security Considerations
### Secrets Management
If you need API keys or credentials:
1. Never commit them to the repository
2. Use GitHub Secrets:
   - Go to Settings > Secrets and variables > Actions
   - Add your secret
   - Reference in workflow: `${{ secrets.SECRET_NAME }}`
### Coverage Service Integration
To enable Codecov:
1. Visit https://codecov.io
2. Connect your GitHub account
3. Add your repository
4. Coverage will automatically upload
##  Customization
### Add More Python Versions
Edit `.github/workflows/main.yml`:
```yaml
matrix:
  python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]  # Added 3.12
```
### Add New Dependencies
Edit the install step:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install PyQt5 pycryptodome pytest pytest-cov NEW_PACKAGE
```
### Change Trigger Branches
Edit the `on` section:
```yaml
on:
  push:
    branches: [ main, staging, develop ]  # Added staging
  pull_request:
    branches: [ main, staging, develop ]
```
### Disable a Job
Comment out or remove the job section:
```yaml
# security:  # Temporarily disabled
#   runs-on: ubuntu-latest
```
##  Testing the Workflow Locally
### Validate Workflow File
```bash
# Using act (local GitHub Actions runner)
# Install: https://github.com/nektos/act
act -l  # List workflows
act     # Run workflow locally
```
### Run Workflow Tests
```bash
# Test the workflow configuration
pytest tests/test_workflow.py tests/test_workflow_integration.py -v
# Run specific test class
pytest tests/test_workflow.py::TestWorkflowConfiguration -v
```
##  Support & Resources
### GitHub Actions Documentation
- https://docs.github.com/en/actions
- Workflow syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
### Tool Documentation
- pytest: https://docs.pytest.org
- black: https://black.readthedocs.io
- flake8: https://flake8.pycqa.org
- bandit: https://bandit.readthedocs.io
### Related Files
- Workflow: `.github/workflows/main.yml`
- Tests: `tests/test_workflow.py`, `tests/test_workflow_integration.py`
- Documentation: `GITHUB_ACTIONS_TESTS.md`, `WORKFLOW_TESTS_SUMMARY.md`
##  Best Practices
1. **Always test locally first**
   - Run `pytest` before pushing
   - Fix linting issues with `black` and `isort`
2. **Keep workflows simple**
   - Don't add unnecessary steps
   - Use separate jobs for different concerns
3. **Monitor workflow metrics**
   - Watch build times
   - Track test coverage
   - Review security findings
4. **Update regularly**
   - Check for tool updates
   - Update Python versions as needed
   - Review GitHub Actions best practices
5. **Document changes**
   - Commit messages explain workflow changes
   - Update this guide when modifying workflows
   - Keep README updated with any new requirements
##  You're All Set!
Your GitHub Actions workflow is ready to use. Your code will now be automatically tested, linted, and scanned for security issues on every push and pull request!
Happy coding!
