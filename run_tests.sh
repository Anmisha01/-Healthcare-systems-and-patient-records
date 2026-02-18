#!/bin/bash

# Healthcare System Test Runner
# Runs all tests with coverage reporting
# Updated for final implementation

set -e  # Exit on error

echo "🏥 Healthcare System - Comprehensive Test Suite"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    print_error "Please run this script from the healthcare_system directory"
fi

print_info "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" = "3.8" ]; then 
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3.8+ required, found $PYTHON_VERSION"
fi

echo ""
print_info "Installing test dependencies..."
pip install pytest pytest-cov coverage --break-system-packages -q 2>/dev/null || pip install pytest pytest-cov coverage -q
print_success "Test dependencies installed"

echo ""
echo "================================================"
echo "Running Unit Tests"
echo "================================================"

# Test 1: Crypto Utils
echo ""
print_info "Testing crypto_utils.py..."
python3 -m pytest test_crypto_utils.py -v --tb=short
if [ $? -eq 0 ]; then
    print_success "Crypto utils tests passed"
else
    print_error "Crypto utils tests failed"
fi

# Test 2: Auth System
echo ""
print_info "Testing auth_system.py..."
python3 -m pytest test_auth_system.py -v --tb=short
if [ $? -eq 0 ]; then
    print_success "Auth system tests passed"
else
    print_error "Auth system tests failed"
fi

# Test 3: Patient Records
echo ""
print_info "Testing patient_records.py..."
python3 -m pytest test_patient_records.py -v --tb=short
if [ $? -eq 0 ]; then
    print_success "Patient records tests passed"
else
    print_error "Patient records tests failed"
fi

# Test 4: Integration Tests
echo ""
print_info "Testing integration workflows..."
python3 -m pytest test_integration.py -v --tb=short
if [ $? -eq 0 ]; then
    print_success "Integration tests passed"
else
    print_error "Integration tests failed"
fi

echo ""
echo "================================================"
echo "Generating Coverage Report"
echo "================================================"
echo ""

print_info "Running coverage analysis..."
python3 -m pytest --cov=. --cov-report=term --cov-report=html \
    test_crypto_utils.py test_auth_system.py test_patient_records.py test_integration.py \
    --ignore=test_gui.py --ignore=diagnose.py --ignore=verify.py

if [ $? -eq 0 ]; then
    print_success "Coverage report generated"
    echo ""
    print_info "HTML coverage report saved to: htmlcov/index.html"
else
    print_warning "Coverage generation had some issues"
fi

echo ""
echo "================================================"
echo "Test Summary"
echo "================================================"
echo ""

# Count total tests
TOTAL_TESTS=$(python3 -m pytest --collect-only -q test_*.py 2>/dev/null | grep "test session" | grep -oP '\d+' | head -1)

print_success "All test suites passed!"
echo ""
echo "Test Statistics:"
echo "  • Total test cases: ~$TOTAL_TESTS+"
echo "  • Test files: 4"
echo "  • Modules tested: crypto_utils, auth_system, patient_records"
echo "  • Integration tests: Complete workflows"
echo ""
echo "Coverage report: htmlcov/index.html"
echo ""
print_success "Testing complete! Your healthcare system is working perfectly."