# GitHub Actions Workflow Tests
This directory contains comprehensive automated tests for the GitHub Actions CI/CD pipeline configuration and execution.
## Overview
Two test files validate the GitHub Actions workflow:
### 1. [tests/test_workflow.py](tests/test_workflow.py)
Tests for the GitHub Actions workflow configuration (YAML structure, jobs, steps, and best practices).
**Test Classes:**
- `TestWorkflowConfiguration` (25 tests): Validates workflow YAML structure, jobs, and configuration
- `TestWorkflowExecution` (4 tests): Verifies environment and tool availability
- `TestWorkflowSecurityAndBestPractices` (6 tests): Ensures security best practices
**Key Validations:**
- Workflow file exists and is valid YAML
- Required triggers (push, pull_request) on main and develop branches
- Test job runs on Ubuntu with Python 3.8, 3.9, 3.10, 3.11 matrix
- Dependencies are properly installed (PyQt5, pycryptodome, pytest, pytest-cov)
- Code coverage reporting with pytest-cov
- Lint job with black, isort, and flake8
- Security job with bandit scanning
- Actions are pinned to specific versions
- Codecov integration configured
### 2. [tests/test_workflow_integration.py](tests/test_workflow_integration.py)
Integration tests that simulate actual CI/CD pipeline job execution.
**Test Classes:**
- `TestWorkflowJobExecution` (5 tests): Simulates test job steps
- `TestLintingTools` (2 tests): Validates linting tool availability
- `TestSecurityScanning` (2 tests): Validates security scanning tools
- `TestCoverageReporting` (2 tests): Validates coverage configuration
- `TestMatrixStrategy` (2 tests): Validates Python version matrix
**Key Validations:**
- Dependencies can be installed via pip
- Pytest can collect all tests
- Pytest runs successfully and reports results properly
- Core Python modules are importable
- Linting tools are available
- Security scanning tools are available
- Code coverage reporting is configurable
- Python versions are tested across the matrix
## Running the Tests
### Run all workflow tests:
```bash
pytest tests/test_workflow.py tests/test_workflow_integration.py -v
```
### Run specific test class:
```bash
pytest tests/test_workflow.py::TestWorkflowConfiguration -v
```
### Run with coverage:
```bash
pytest tests/test_workflow.py tests/test_workflow_integration.py -v --cov=tests
```
### Run specific test:
```bash
pytest tests/test_workflow.py::TestWorkflowConfiguration::test_workflow_file_exists -v
```
## Workflow Jobs
The GitHub Actions workflow (`.github/workflows/main.yml`) contains three jobs:
### 1. Test Job
- **Runs on:** Ubuntu latest
- **Matrix:** Python 3.8, 3.9, 3.10, 3.11
- **Steps:**
  - Checkout code
  - Set up Python with pip caching
  - Install dependencies (PyQt5, pycryptodome, pytest, pytest-cov)
  - Run pytest with coverage reporting
  - Upload coverage to Codecov
### 2. Lint Job
- **Runs on:** Ubuntu latest with Python 3.10
- **Tools:**
  - Black: Code formatting checker
  - isort: Import ordering checker
  - flake8: Style guide enforcement
- **Steps:**
  - Checkout code
  - Set up Python
  - Install linting tools
  - Run each linter in check mode
### 3. Security Job
- **Runs on:** Ubuntu latest with Python 3.10
- **Tools:**
  - Bandit: Security issue scanner
- **Steps:**
  - Checkout code
  - Set up Python
  - Install bandit
  - Run security scan (non-blocking with || true)
## Triggers
The workflow runs on:
- **Push** to `main` and `develop` branches
- **Pull Requests** to `main` and `develop` branches
## Test Statistics
- **Total Tests:** 48
- **Passing:** 48 (100%)
- **Configuration Tests:** 25
- **Execution Tests:** 4
- **Security & Best Practice Tests:** 6
- **Integration Tests:** 13
## Coverage
Tests validate:
-  Workflow file structure and validity
-  All required jobs are present and configured
-  Python version matrix is correctly specified
-  Dependencies are properly declared
-  Code coverage reporting is enabled
-  Linting and security tools are configured
-  Actions use pinned versions
-  Tools run in correct environments
-  Exit codes and status reporting
## Dependencies
The tests require:
- Python 3.8+
- pytest
- PyYAML (for YAML parsing)
- Standard library modules (subprocess, os, sys, yaml)
Install test dependencies:
```bash
pip install pytest pyyaml
```
## CI/CD Integration
These tests can be run locally to validate workflow configuration before pushing to GitHub:
```bash
# Local validation
pytest tests/test_workflow.py tests/test_workflow_integration.py -v
# From project root
cd /home/samriddha8/Documents/GitHub/-Healthcare-systems-and-patient-records
pytest tests/test_workflow*.py -v
```
## Troubleshooting
### ModuleNotFoundError for PyQt5 or Crypto
- The workflow tests are designed to run independently of other project dependencies
- Integration tests only test core imports that don't require PyQt5
- The actual workflow in GitHub will have all dependencies available
### YAML parsing warnings
- YAML `on` keyword is parsed as `True` in Python - tests handle this automatically
- No action needed
### Bandit security scan warnings
- Security job intentionally doesn't fail on warnings (`|| true`)
- This allows the workflow to complete even with low-severity findings
- Review findings but don't block the pipeline
## Best Practices Validated
1. **Security:** Actions pinned to specific versions to prevent supply chain attacks
2. **Reproducibility:** Consistent Python versions tested across matrix
3. **Efficiency:** pip caching for faster builds
4. **Coverage:** Automated coverage reporting to Codecov
5. **Code Quality:** Automated linting with multiple tools
6. **Non-blocking Security:** Security scanning that alerts but doesn't block
7. **Pip Upgrades:** Always upgrade pip before installing packages
8. **Clear Configuration:** Well-documented workflow with descriptive step names
## Related Files
- [.github/workflows/main.yml](.github/workflows/main.yml) - The GitHub Actions workflow configuration
- [tests/test_auth.py](tests/test_auth.py) - Authentication logic tests
- [tests/test_crypto_utils.py](tests/test_crypto_utils.py) - Crypto utilities tests
- [tests/test_data_store.py](tests/test_data_store.py) - Data store tests
- [tests/test_gui_login.py](tests/test_gui_login.py) - GUI login tests
- [tests/test_main.py](tests/test_main.py) - Main module tests
## Notes
- Tests validate configuration and execution without running the actual GitHub Actions environment
- Some integration tests are resilient to missing dependencies to allow testing in various environments
- The workflow ensures code quality and security through multiple automated checks
- All tests pass in the current environment (Python 3.14.2)
