#!/bin/bash
set -e

echo "Running essential tests for fmpsdk..."

# Code formatting (auto-fix)
echo "Auto-formatting code with black..."
black . > /dev/null 2>&1

echo "Auto-organizing imports with isort..."
isort . > /dev/null 2>&1

# Critical syntax errors only 
echo "Checking for critical Python syntax errors..."
flake8 fmpsdk/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Test execution
echo "Running tests with multithreading..."
if [ "${CI:-false}" = "true" ]; then
    echo "CI environment detected - using auto worker detection"
    pytest -n auto --tb=short --junitxml=test-results.xml
else
    echo "Local development - using 4 workers for optimal performance" 
    pytest -n 4 --tb=short -q
fi

echo "✅ All essential tests passed!"
echo "Note: Some cosmetic linting warnings may exist but don't affect functionality"
echo "Run 'black .' and 'isort .' to auto-fix formatting if needed"
