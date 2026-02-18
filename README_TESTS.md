# Healthcare System - Testing Documentation

## Overview

This project includes comprehensive unit tests, integration tests, and automated testing via GitHub Actions.

## Test Coverage

- **Crypto Utils Tests** (`test_crypto_utils.py`): 15+ tests for encryption/hashing
- **Auth System Tests** (`test_auth_system.py`): 14+ tests for authentication
- **Patient Records Tests** (`test_patient_records.py`): 18+ tests for data management
- **Integration Tests** (`test_integration.py`): 3+ end-to-end workflow tests

**Total: 50+ test cases**

## Running Tests Locally

### Prerequisites
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run All Tests
```bash
# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh

# Windows
run_tests.bat

# Manual
pytest -v
```

### Run Specific Test Files
```bash
pytest test_crypto_utils.py -v
pytest test_auth_system.py -v
pytest test_patient_records.py -v
pytest test_integration.py -v
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html --cov-report=term
# View coverage report: htmlcov/index.html
```

### Run Specific Tests
```bash
pytest test_auth_system.py::TestAuthSystem::test_register_user_success -v
```

## GitHub Actions

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Workflow Jobs

1. **Test Job**
   - Runs on: Ubuntu, Windows, macOS
   - Python versions: 3.8, 3.9, 3.10, 3.11
   - Generates coverage reports

2. **Lint Job**
   - Runs flake8, black, pylint
   - Checks code quality

3. **Security Job**
   - Runs bandit (security scanner)
   - Runs safety (dependency checker)

## Test Structure

### Unit Tests
Each module has dedicated unit tests:
- `crypto_utils.py` → `test_crypto_utils.py`
- `auth_system.py` → `test_auth_system.py`
- `patient_records.py` → `test_patient_records.py`

### Integration Tests
`test_integration.py` tests complete workflows:
- User registration → login → patient management
- Multiple users managing multiple patients
- Data persistence and security

## Writing New Tests

### Example Test
```python
import unittest
from module_name import ClassName

class TestFeature(unittest.TestCase):
    def setUp(self):
        # Setup before each test
        pass
    
    def test_something(self):
        # Your test code
        self.assertEqual(expected, actual)
    
    def tearDown(self):
        # Cleanup after each test
        pass
```

### Best Practices
1. Each test should be independent
2. Use descriptive test names
3. Test both success and failure cases
4. Clean up resources in `tearDown()`
5. Use temporary files for file operations

## Continuous Integration

### Badge Status
Add to your README.md:
```markdown
![Tests](https://github.com/yourusername/healthcare-system/workflows/Healthcare%20System%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/healthcare-system/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/healthcare-system)
```

## Security Testing

### Run Security Scan
```bash
# Bandit - Python security scanner
bandit -r . -ll

# Safety - dependency vulnerability checker
safety check
```

### Common Security Issues Checked
- Hardcoded passwords
- SQL injection vulnerabilities
- Weak cryptographic practices
- Insecure random number generation

## Code Quality

### Linting
```bash
# Flake8
flake8 . --max-line-length=127

# Black (formatting)
black . --check

# Pylint
pylint *.py
```

## Troubleshooting

### Tests Fail with Import Errors
```bash
# Ensure you're in the project directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Coverage Not Working
```bash
pip install --upgrade pytest-cov coverage
```

### GitHub Actions Failing
1. Check the Actions tab in your repository
2. Review the logs for specific errors
3. Ensure all dependencies are in requirements.txt

## Performance Testing

Future enhancement: Add performance tests for:
- Encryption/decryption speed
- Large dataset handling
- Concurrent user sessions

## Contact

For questions about testing, please open an issue on GitHub.
```

## Project Structure with Tests
```
healthcare_system/
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions config
├── crypto_utils.py
├── auth_system.py
├── patient_records.py
├── login_ui.py
├── main_ui.py
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── test_crypto_utils.py        # Unit tests
├── test_auth_system.py         # Unit tests
├── test_patient_records.py     # Unit tests
├── test_integration.py         # Integration tests
├── pytest.ini                  # Pytest config
├── .coveragerc                 # Coverage config
├── run_tests.sh               # Linux/Mac test runner
├── run_tests.bat              # Windows test runner
├── README.md
└── README_TESTS.md            # Testing documentation