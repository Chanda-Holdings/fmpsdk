"""
Test configuration and utilities for fmpsdk integration tests.
"""

import functools
import os
import time
from datetime import datetime, timedelta

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test configuration
API_KEY = os.getenv("FMP_API_KEY")
RATE_LIMIT_DELAY = 0.1  # Delay between API calls to respect rate limits
RETRY_DELAY = 30.0  # Delay before retrying after rate limit error (30 seconds)
MAX_RETRIES = 3  # Maximum number of retries for rate limit errors (only 3 retries)

# Common test symbols for different categories
TEST_SYMBOLS = {
    "large_cap": ["AAPL", "MSFT", "GOOGL", "AMZN"],
    "tech": ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"],
    "finance": ["JPM", "BAC", "WFC", "GS"],
    "healthcare": ["JNJ", "PFE", "UNH", "ABBV"],
    "energy": ["XOM", "CVX", "COP", "EOG"],
    "utilities": ["NEE", "DUK", "SO", "AEP"],
    "etfs": ["SPY", "QQQ", "IWM", "VTI"],
    "crypto": ["BTCUSD", "ETHUSD", "ADAUSD"],
    "forex": ["EURUSD", "GBPUSD", "USDJPY", "USDCAD"],
}

# Date ranges for testing
TEST_DATES = {
    "recent_month": {
        "from": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "to": datetime.now().strftime("%Y-%m-%d"),
    },
    "recent_quarter": {
        "from": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
        "to": datetime.now().strftime("%Y-%m-%d"),
    },
    "year_2024": {"from": "2024-01-01", "to": "2024-12-31"},
    "jan_2024": {"from": "2024-01-01", "to": "2024-01-31"},
}


def respect_rate_limit():
    """Add a small delay to respect API rate limits."""
    time.sleep(RATE_LIMIT_DELAY)


def skip_if_no_api_key():
    """Skip test if no valid API key is provided."""
    if API_KEY == "demo" or not API_KEY:
        pytest.skip("No valid API key provided")


class APITestHelper:
    """Helper class for API testing utilities."""

    @staticmethod
    def verify_pydantic_response(result, func_name):
        """Verify that the response is a proper Pydantic model."""
        assert result is not None, f"{func_name} returned None"
        assert hasattr(
            result, "__dict__"
        ), f"{func_name} should return a Pydantic model"

    @staticmethod
    def test_multiple_symbols(func, symbols, extra_kwargs=None):
        """Test a function with multiple symbols."""
        extra_kwargs = extra_kwargs or {}

        for symbol in symbols:
            kwargs = {"apikey": API_KEY, "symbol": symbol, **extra_kwargs}
            result = func(**kwargs)
            assert result is not None, f"{func.__name__} failed for symbol {symbol}"
            respect_rate_limit()

    @staticmethod
    def test_date_range(func, symbol, date_range, extra_kwargs=None):
        """Test a function with date range parameters."""
        extra_kwargs = extra_kwargs or {}

        kwargs = {
            "apikey": API_KEY,
            "symbol": symbol,
            "from_date": date_range["from"],
            "to_date": date_range["to"],
            **extra_kwargs,
        }

        result = func(**kwargs)
        assert result is not None, f"{func.__name__} failed with date range"
        return result

    @staticmethod
    def test_pagination(func, base_kwargs, max_pages=3):
        """Test pagination functionality."""
        results = []

        for page in range(max_pages):
            kwargs = {**base_kwargs, "page": page, "limit": 5}
            result = func(**kwargs)
            assert result is not None, f"{func.__name__} failed on page {page}"
            results.append(result)
            respect_rate_limit()

        return results


# Pytest fixtures
@pytest.fixture
def api_key():
    """Provide API key for tests."""
    skip_if_no_api_key()
    return API_KEY


@pytest.fixture
def test_symbols():
    """Provide test symbols categorized by type."""
    return TEST_SYMBOLS


@pytest.fixture
def test_dates():
    """Provide test date ranges."""
    return TEST_DATES


@pytest.fixture
def api_helper():
    """Provide API testing helper."""
    return APITestHelper()


# Custom pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring API key"
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line(
        "markers", "rate_limited: mark test as potentially rate limited"
    )


def pytest_runtest_makereport(item, call):
    """Custom hook to analyze test failures and provide information about rate limits."""
    if call.when == "call":
        if hasattr(call, "excinfo") and call.excinfo is not None:
            exception = call.excinfo.value

            # Check if this is a rate limit error - just log it, don't add retry markers
            if is_rate_limit_error(exception):
                print(f"\n🔄 Rate limit detected in {item.name}")
            else:
                print(f"\n❌ Non-rate-limit error in {item.name}")


def pytest_exception_interact(node, call, report):
    """Hook called when an exception occurs during test execution."""
    if hasattr(call, "excinfo") and call.excinfo is not None:
        exception = call.excinfo.value

        if is_rate_limit_error(exception):
            print(f"\n⚠️  Rate limit error detected in {node.name}")
            print(
                "💡 Use @retry_on_rate_limit decorator for automatic retry with 30 second delay"
            )
        else:
            print(f"\n❌ Non-rate-limit error in {node.name} - will not retry")


# Helper function to run tests with automatic retry on rate limits only
def run_tests_with_retry():
    """
    Run tests with automatic retry ONLY on rate limit errors.
    Usage: python -c "from tests.conftest import run_tests_with_retry; run_tests_with_retry()"
    """
    import subprocess
    import sys

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--reruns",
        "1",  # Only 1 retry
        "--reruns-delay",
        "30",  # 30 second delay
        "--only-rerun",
        "rate.limit|limit.reach|quota.exceeded|too.many.requests|upgrade.your.plan",  # Only rerun on rate limit patterns
        "--tb=short",
        "-v",
    ]

    print(
        "🚀 Running tests with automatic retry ONLY on rate limit errors (30s delay)..."
    )
    result = subprocess.run(cmd)
    return result.returncode


def is_rate_limit_error(exception):
    """Check if an exception is a rate limit error."""
    if isinstance(exception, AssertionError):
        error_msg = str(exception).lower()
        return any(
            phrase in error_msg
            for phrase in [
                "limit reach",
                "rate limit",
                "rate limited",
                "quota exceeded",
                "too many requests",
                "upgrade your plan",
                "api limit exceeded",
                "requests per minute exceeded",
            ]
        )
    # Also check for HTTP exceptions that might indicate rate limiting
    if hasattr(exception, "response"):
        if hasattr(exception.response, "status_code"):
            return exception.response.status_code == 429  # HTTP 429 Too Many Requests

    # Check for common rate limit error messages in the exception string
    error_str = str(exception).lower()
    return any(
        phrase in error_str
        for phrase in [
            "limit reach",
            "rate limit",
            "rate limited",
            "quota exceeded",
            "too many requests",
            "upgrade your plan",
            "api limit exceeded",
            "requests per minute exceeded",
        ]
    )


def retry_on_rate_limit(max_retries=1, delay=30.0):
    """
    Decorator to retry function calls ONLY when rate limit errors occur.

    Args:
        max_retries (int): Number of retries for rate limit errors only (default: 1)
        delay (float): Delay in seconds before retrying rate limit errors (default: 30.0)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    # Only retry if it's a rate limit error AND we haven't exhausted retries
                    if is_rate_limit_error(e) and attempt < max_retries:
                        print(
                            f"\n⚠️  Rate limit detected in {func.__name__}!"
                            f"\n💤 Sleeping for {delay} seconds before retry... (attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(delay)
                        continue
                    else:
                        # Re-raise immediately if it's not a rate limit error
                        # or if we've exhausted retries for rate limit errors
                        raise e

            # If we get here, we've exhausted all retries for rate limit errors
            raise last_exception

        return wrapper

    return decorator


@pytest.fixture
def add_retry_to_tests(request):
    """
    Manually add retry logic to tests that might hit rate limits.
    Only retries on rate limit errors with 30 second delay.
    Use this fixture explicitly in tests that need rate limit retry protection.
    """
    # Get the test function
    test_func = request.function

    # Wrap the test function with retry logic (1 retry, 30 second delay)
    wrapped_func = retry_on_rate_limit(max_retries=1, delay=30.0)(test_func)
    # Replace the original function
    request.function = wrapped_func
