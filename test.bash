set -e

# Code formatting and linting
black .
black --check --diff fmpsdk/ tests/
isort .
isort --check-only --diff fmpsdk/ tests/

# Static analysis
# stop the build if there are Python syntax errors or undefined names
flake8 fmpsdk/ --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 fmpsdk/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
mypy fmpsdk/ --ignore-missing-imports --no-strict-optional

# Multithreaded test execution
echo "Running tests with multithreading for faster execution..."

# Check if we're in a CI environment or local development
if [ "${CI:-false}" = "true" ]; then
    echo "CI environment detected - using auto worker detection"
    pytest -n auto --tb=short --junitxml=test-results.xml
else
    echo "Local development - using 4 workers for optimal performance"
    pytest -n 50 --tb=short
fi

echo "Test execution completed!"
echo "Performance tip: Use 'pytest -n 8' for maximum local speed or 'pytest' for debugging"