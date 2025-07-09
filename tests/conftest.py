import functools
import json
import os
import threading
import time
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file at test session start
# Use explicit path and override=True to ensure .envdef with_rate_limit_retry(max_retries=2, cooldown_seconds=30):takes precedence
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path, override=True)


class RateLimitError(Exception):
    """Exception raised when rate limiting is detected."""

    pass


class GlobalRateLimitManager:
    """
    Global rate limit manager that coordinates rate limiting across pytest workers.

    Uses file-based coordination to ensure all workers respect rate limits.
    """

    def __init__(self, cooldown_duration=20):
        self.cooldown_duration = cooldown_duration
        self.lock_file = Path("/tmp/fmpsdk_rate_limit_lock")
        self.cooldown_file = Path("/tmp/fmpsdk_rate_limit_cooldown")
        self._local_lock = threading.Lock()

    def is_in_cooldown(self):
        """Check if we're currently in a rate limit cooldown period."""
        if not self.cooldown_file.exists():
            return False

        try:
            with open(self.cooldown_file, "r") as f:
                cooldown_data = json.load(f)
                cooldown_until = cooldown_data.get("cooldown_until", 0)
                return time.time() < cooldown_until
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return False

    def wait_for_cooldown(self):
        """Wait for any active cooldown period to complete."""
        if not self.is_in_cooldown():
            return  # No cooldown active

        print("Rate limit cooldown active. Waiting for completion...")
        start_time = time.time()

        while self.is_in_cooldown():
            try:
                with open(self.cooldown_file, "r") as f:
                    cooldown_data = json.load(f)
                    remaining = cooldown_data.get("cooldown_until", 0) - time.time()
                    if remaining > 0:
                        time.sleep(min(2, remaining + 0.5))
                    else:
                        break
            except (json.JSONDecodeError, FileNotFoundError):
                break

        elapsed = time.time() - start_time
        print(f"Cooldown completed after {elapsed:.1f}s")

    def trigger_cooldown(self):
        """Trigger a global cooldown period."""
        with self._local_lock:
            try:
                # Always set cooldown period, regardless of lock file existence
                cooldown_until = time.time() + self.cooldown_duration
                cooldown_data = {
                    "cooldown_until": cooldown_until,
                    "triggered_by_pid": os.getpid(),
                    "triggered_at": time.time(),
                }

                with open(self.cooldown_file, "w") as f:
                    json.dump(cooldown_data, f)

                print(
                    f"Rate limit detected! Triggered {self.cooldown_duration}s global cooldown."
                )

            except Exception as e:
                print(f"Error managing rate limit cooldown: {e}")
                # Fallback - don't sleep, just continue and let retry handle it


# Global instance
rate_limit_manager = GlobalRateLimitManager()


def is_premium_endpoint_response(result):
    """
    Check if the response indicates a premium endpoint (not just premium parameters).

    This function distinguishes between:
    - Premium endpoint errors (entire endpoint requires premium) - should skip
    - Premium parameter errors (specific parameter values require premium) - should fail

    Args:
        result: The API response object

    Returns:
        bool: True if this is a premium endpoint error, False otherwise
    """
    # Check for 402 status code responses
    if hasattr(result, "status_code") and result.status_code == 402:
        # Check the content to distinguish between endpoint vs parameter premium errors
        if hasattr(result, "content"):
            try:
                content = (
                    result.content.decode("utf-8")
                    if isinstance(result.content, bytes)
                    else str(result.content)
                )

                # First, check for explicit "Premium Endpoint:" messages
                if content.strip().startswith("Premium Endpoint:"):
                    return True  # This is definitely an endpoint error

                # Premium PARAMETER errors - should fail the test, not skip
                # Be specific to avoid conflicts with endpoint errors
                premium_parameter_indicators = [
                    "premium query parameter",
                    "this value set for",
                ]
                if any(
                    indicator.lower() in content.lower()
                    for indicator in premium_parameter_indicators
                ):
                    return False  # This is a parameter issue, not an endpoint issue

                # Premium ENDPOINT errors - should skip the test
                premium_endpoint_indicators = [
                    "premium endpoint",
                    "this endpoint requires",
                    "upgrade your plan to access this endpoint",
                    "this endpoint is not available under your",
                    "endpoint is not available under your",
                ]
                if any(
                    indicator.lower() in content.lower()
                    for indicator in premium_endpoint_indicators
                ):
                    return True

                # Default for 402 without specific indicators - treat as endpoint issue to be safe
                return True
            except (UnicodeDecodeError, AttributeError):
                # If we can't decode the content, assume it's an endpoint issue to be safe
                return True

    # Check for text responses containing premium endpoint messages
    if hasattr(result, "content"):
        try:
            content = (
                result.content.decode("utf-8")
                if isinstance(result.content, bytes)
                else str(result.content)
            )
            # Only skip for premium ENDPOINT messages, not premium PARAMETER messages
            premium_endpoint_keywords = [
                "premium endpoint",
                "higher plan",
                "this endpoint is not available under your",
                "endpoint is not available under your",
            ]
            if any(
                keyword.lower() in content.lower()
                for keyword in premium_endpoint_keywords
            ):
                return True
        except (UnicodeDecodeError, AttributeError):
            pass

    # Check for specific error messages related to premium ENDPOINTS (not parameters)
    if isinstance(result, dict) and "Error Message" in result:
        error_msg = result["Error Message"].lower()
        # Skip only for premium endpoint access, not premium parameter values
        premium_endpoint_indicators = [
            "premium endpoint",
            "higher tier",
            "advanced features",
        ]
        if any(indicator in error_msg for indicator in premium_endpoint_indicators):
            return True

    return False


def is_rate_limit_error(result):
    """
    Check if the response indicates a rate limiting error.

    Args:
        result: The API response object

    Returns:
        bool: True if this is a rate limiting error, False otherwise
    """
    # Check for dictionary responses with Error Message (FMP API specific)
    if isinstance(result, dict) and "Error Message" in result:
        error_msg = result["Error Message"].lower()
        # FMP specific rate limiting message
        if "limit reach" in error_msg:
            return True
        # Check for other common rate limiting keywords
        rate_limit_keywords = [
            "rate limit",
            "too many requests",
            "quota exceeded",
            "api limit",
            "requests per",
            "upgrade your plan",  # FMP often says this for rate limits
        ]
        return any(keyword in error_msg for keyword in rate_limit_keywords)

    # Check for HTTP status responses
    if hasattr(result, "status_code"):
        # 429 is the standard rate limiting status code
        if result.status_code == 429:
            return True
        # Some APIs use other status codes for rate limiting
        if result.status_code in [
            503,
            509,
        ]:  # Service Unavailable, Bandwidth Limit Exceeded
            if hasattr(result, "content"):
                try:
                    content = (
                        result.content.decode("utf-8")
                        if isinstance(result.content, bytes)
                        else str(result.content)
                    )
                    return any(
                        keyword in content.lower()
                        for keyword in ["rate", "limit", "quota"]
                    )
                except (UnicodeDecodeError, AttributeError):
                    pass

    return False


def is_assertion_error_rate_limit(exception):
    """
    Check if an AssertionError is actually caused by rate limiting.

    This is for cases where the test fails an assertion because the API
    returned a rate limit error instead of expected data.

    Args:
        exception: The exception to check

    Returns:
        bool: True if this assertion error is due to rate limiting
    """
    if not isinstance(exception, AssertionError):
        return False

    error_str = str(exception).lower()

    # Be VERY specific - only detect the exact FMP rate limit message
    # "Limit Reach . Please upgrade your plan or visit our documentation for more details at https://site.financialmodelingprep.com/"
    if "limit reach" in error_str and "upgrade your plan" in error_str:
        return True

    # Also check for the specific assertion pattern with the exact error message
    if (
        "isinstance" in error_str
        and "error message" in error_str
        and "limit reach" in error_str
        and "upgrade your plan" in error_str
    ):
        return True

    return False


def extract_data_list(result):
    """
    Helper function to extract data list from various response formats.

    This function automatically detects premium endpoint responses and skips
    tests gracefully when premium access is required. It also detects premium
    parameter errors and fails tests with appropriate error messages.

    For rate limiting errors, this function raises a RateLimitError to trigger
    the retry mechanism.

    Args:
        result: The API response object

    Returns:
        list: The extracted data list

    Raises:
        pytest.skip: If the response indicates premium endpoint without access
        AssertionError: If the response indicates premium parameter restrictions
        RateLimitError: If the response indicates rate limiting
    """
    # Check if this is a premium endpoint response (should skip) - check this FIRST
    if is_premium_endpoint_response(result):
        pytest.skip("Premium endpoint detected - requires higher API plan")

    # Check for rate limiting errors - RAISE EXCEPTION instead of skipping
    if is_rate_limit_error(result):
        raise RateLimitError("Rate limiting detected in API response")

    # Check for premium parameter errors (should fail, not skip)
    if hasattr(result, "status_code") and result.status_code == 402:
        if hasattr(result, "content"):
            try:
                content = (
                    result.content.decode("utf-8")
                    if isinstance(result.content, bytes)
                    else str(result.content)
                )

                # Premium PARAMETER errors - should fail the test
                premium_parameter_indicators = [
                    "premium query parameter",
                    "this value set for",
                ]
                if any(
                    indicator.lower() in content.lower()
                    for indicator in premium_parameter_indicators
                ):
                    pytest.fail(f"Premium parameter restriction detected: {content}")
            except (UnicodeDecodeError, AttributeError):
                pass

    # Extract the data list from valid responses
    if hasattr(result, "root") and isinstance(result.root, list):
        data_list = result.root
    elif isinstance(result, list):
        data_list = result
    elif hasattr(result, "__iter__") and not isinstance(result, (str, dict)):
        data_list = list(result)
    else:
        data_list = [result] if result else []

    return data_list


@pytest.fixture(scope="session")
def api_key():
    """
    Provide API key for all tests in the session.

    This fixture loads the API key from environment variables and
    skips all tests if no valid API key is found.

    Returns:
        str: The FMP API key

    Raises:
        pytest.skip: If no API key is found in environment variables
    """
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        pytest.skip("FMP_API_KEY environment variable not set")

    # Check if this looks like a placeholder API key
    if api_key in ["your_api_key_here"]:
        pytest.skip(
            "Please set a valid FMP API key in .env file (current key appears to be a placeholder)"
        )

    return api_key


@pytest.fixture(scope="session")
def test_symbols():
    """
    Provide a set of reliable test symbols for various test scenarios.

    Returns:
        dict: Dictionary containing different categories of test symbols
    """
    return {
        "large_cap": ["AAPL", "MSFT", "GOOGL"],  # High volume, reliable data
        "mid_cap": ["ROKU", "TDOC", "ZM"],  # Medium volume stocks
        "etf": ["SPY", "QQQ", "VTI"],  # Popular ETFs
        "crypto": ["BTCUSD", "ETHUSD"],  # Crypto pairs
        "forex": ["EURUSD", "GBPUSD"],  # Forex pairs
        "commodity": ["GCUSD", "CLUSD"],  # Gold and Oil
        "invalid": ["INVALID", "NOTREAL"],  # Invalid symbols for error testing
    }


@pytest.fixture
def test_config():
    """
    Provide test configuration settings.

    Returns:
        dict: Configuration settings for tests
    """
    return {
        "timeout": 30,  # API timeout in seconds
        "retry_count": 3,  # Number of retries for flaky tests
        "min_market_cap": 1_000_000_000,  # Minimum market cap for validation
        "max_response_time": 5.0,  # Maximum acceptable response time in seconds
    }


# Test markers for categorizing tests
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line(
        "markers", "requires_api_key: mark test as requiring API key"
    )
    config.addinivalue_line("markers", "live_data: mark test as using live market data")
    config.addinivalue_line(
        "markers", "premium: mark test as potentially requiring premium API plan"
    )


# Custom assertions and utilities
class TestHelpers:
    """Helper methods for common test operations."""

    @staticmethod
    def validate_price_data(price_data, symbol):
        """
        Validate common price data fields.

        Args:
            price_data: The price data object to validate
            symbol: The expected symbol
        """
        assert price_data.symbol == symbol, f"Symbol should match: {symbol}"
        assert price_data.price is not None, "Price should be present"
        assert price_data.price > 0, "Price should be positive"

    @staticmethod
    def validate_market_data_consistency(data):
        """
        Validate that market data is internally consistent.

        Args:
            data: Market data object with price fields
        """
        if all(
            hasattr(data, field) and getattr(data, field) is not None
            for field in ["dayLow", "dayHigh", "price"]
        ):
            assert (
                data.dayLow <= data.price <= data.dayHigh
            ), "Price should be between day low and high"

        if all(
            hasattr(data, field) and getattr(data, field) is not None
            for field in ["yearLow", "yearHigh", "price"]
        ):
            assert (
                data.yearLow <= data.price <= data.yearHigh
            ), "Price should be between year low and high"


@pytest.fixture
def test_helpers():
    """Provide test helper utilities."""
    return TestHelpers


def with_rate_limit_retry(max_retries=4, cooldown_seconds=20):
    """
    Decorator to add rate limiting retry functionality to test functions.

    This decorator can be used on individual test functions that need
    automatic retry on rate limiting errors.

    Args:
        max_retries: Maximum number of retry attempts (default: 2)
        cooldown_seconds: Seconds to wait between retries (default: 20)

    Example:
        @with_rate_limit_retry(max_retries=2, cooldown_seconds=20)
        def test_my_api_function(self, api_key):
            result = some_api_call(apikey=api_key)
            data = extract_data_list(result)
            assert len(data) > 0
    """

    def decorator(test_func):
        @functools.wraps(test_func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    # Check if we're in a cooldown period before starting
                    if attempt > 0:  # Only wait on retries
                        rate_limit_manager.wait_for_cooldown()

                    return test_func(*args, **kwargs)

                except RateLimitError as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(
                            f"Rate limiting detected on attempt {attempt + 1}/{max_retries + 1}. "
                            f"Triggering global cooldown..."
                        )
                        rate_limit_manager.trigger_cooldown()
                        continue
                    else:
                        # Max retries exceeded, skip the test
                        pytest.skip(
                            f"Rate limiting persisted after {max_retries} retries"
                        )

                except Exception as e:
                    # Check if it's a pytest.skip with rate limiting message
                    if hasattr(e, "msg") and isinstance(e.msg, str):
                        if (
                            "rate limiting" in e.msg.lower()
                            or "rate limit" in e.msg.lower()
                        ):
                            last_exception = RateLimitError(
                                "Rate limit detected in skip message"
                            )
                            if attempt < max_retries:
                                print(
                                    f"Rate limiting detected on attempt {attempt + 1}/{max_retries + 1}. "
                                    f"Triggering global cooldown..."
                                )
                                rate_limit_manager.trigger_cooldown()
                                continue

                    # Not a rate limit error, re-raise immediately
                    raise e

            # This should not be reached, but just in case
            if last_exception:
                pytest.skip(f"Rate limiting persisted after {max_retries} retries")

        return wrapper

    return decorator


def pytest_runtest_setup(item):
    """
    Called before each test runs. Check for global rate limit cooldown.
    """
    # Wait for any active cooldown before starting test
    rate_limit_manager.wait_for_cooldown()


def rate_limit_test_wrapper(test_func):
    """
    Wrapper function that adds rate limit retry logic to any test function.
    """

    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        max_retries = 4
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                # Wait for cooldown before each attempt (except first)
                if attempt > 0:
                    rate_limit_manager.wait_for_cooldown()

                # Run the test
                return test_func(*args, **kwargs)

            except RateLimitError as e:
                last_exception = e
                if attempt < max_retries:
                    print(
                        f"Rate limiting detected on attempt {attempt + 1}/{max_retries + 1}. "
                        f"Triggering global cooldown..."
                    )
                    rate_limit_manager.trigger_cooldown()
                    continue
                else:
                    pytest.skip(f"Rate limiting persisted after {max_retries} retries")

            except AssertionError as e:
                # Check if this assertion error is due to rate limiting
                if is_assertion_error_rate_limit(e):
                    last_exception = RateLimitError(
                        f"Rate limit detected in assertion: {e}"
                    )
                    if attempt < max_retries:
                        print(
                            f"Rate limiting detected in assertion on attempt {attempt + 1}/{max_retries + 1}. "
                            f"Triggering global cooldown..."
                        )
                        rate_limit_manager.trigger_cooldown()
                        continue
                    else:
                        pytest.skip(
                            f"Rate limiting persisted after {max_retries} retries"
                        )
                else:
                    # Regular assertion error, re-raise immediately
                    raise e

            except Exception as e:
                # Be more specific about rate limit detection to avoid false positives
                error_str = str(e).lower()

                # Only check for very specific FMP rate limit indicators
                specific_rate_limit_indicators = [
                    "limit reach . please upgrade your plan",  # Full FMP message
                    "limit reach",  # FMP specific, but only if also contains upgrade
                ]

                # For "limit reach", require additional confirmation it's rate limiting
                is_rate_limit = False
                if "limit reach . please upgrade your plan" in error_str:
                    is_rate_limit = True
                elif "limit reach" in error_str and "upgrade your plan" in error_str:
                    is_rate_limit = True

                if is_rate_limit:
                    last_exception = RateLimitError(
                        f"Rate limit detected in error: {e}"
                    )
                    if attempt < max_retries:
                        print(
                            f"Rate limiting detected in error on attempt {attempt + 1}/{max_retries + 1}. "
                            f"Triggering global cooldown..."
                        )
                        rate_limit_manager.trigger_cooldown()
                        continue
                    else:
                        pytest.skip(
                            f"Rate limiting persisted after {max_retries} retries"
                        )

                # Not a rate limit error, re-raise immediately
                raise e

        # Should not reach here, but just in case
        if last_exception:
            pytest.skip(f"Rate limiting persisted after {max_retries} retries")

    return wrapper


def pytest_collection_modifyitems(config, items):
    """
    Modify collected test items to add rate limiting retry wrapper to ALL tests.
    This ensures every test gets rate limit protection without requiring decorators.
    """
    for item in items:
        # Wrap the runtest method instead of the function
        if hasattr(item, "runtest"):
            original_runtest = item.runtest

            def make_wrapped_runtest(original_func, test_item):
                def wrapped_runtest():
                    max_retries = 4
                    last_exception = None

                    for attempt in range(max_retries + 1):
                        try:
                            # Wait for cooldown before each attempt (including first, in case another test triggered cooldown)
                            if attempt > 0:
                                print(
                                    f"Attempt {attempt + 1} for {test_item.name} - checking cooldown..."
                                )
                            rate_limit_manager.wait_for_cooldown()
                            if attempt > 0:
                                print(
                                    f"Cooldown complete for {test_item.name}, retrying..."
                                )

                            # Run the original test
                            result = original_func()
                            if attempt > 0:
                                print(f"Retry successful for {test_item.name}!")
                            return result

                        except RateLimitError as e:
                            last_exception = e
                            if attempt < max_retries:
                                print(
                                    f"Rate limiting detected on attempt {attempt + 1}/{max_retries + 1} "
                                    f"for {test_item.name}. Triggering global cooldown..."
                                )
                                rate_limit_manager.trigger_cooldown()
                                continue  # This will trigger the next attempt
                            else:
                                print(
                                    f"Rate limiting persisted after {max_retries} retries for {test_item.name}. Skipping."
                                )
                                pytest.skip(
                                    f"Rate limiting persisted after {max_retries} retries"
                                )

                        except AssertionError as e:
                            # Check if this assertion error is due to rate limiting
                            if is_assertion_error_rate_limit(e):
                                print(
                                    f"Assertion error detected as rate limit for {test_item.name}: {str(e)[:100]}..."
                                )
                                last_exception = RateLimitError(
                                    f"Rate limit detected in assertion: {e}"
                                )
                                if attempt < max_retries:
                                    print(
                                        f"Rate limiting detected in assertion on attempt {attempt + 1}/{max_retries + 1} "
                                        f"for {test_item.name}. Triggering global cooldown..."
                                    )
                                    rate_limit_manager.trigger_cooldown()
                                    continue  # This will trigger the next attempt
                                else:
                                    print(
                                        f"Rate limiting persisted after {max_retries} retries for {test_item.name}. Skipping."
                                    )
                                    pytest.skip(
                                        f"Rate limiting persisted after {max_retries} retries"
                                    )
                            else:
                                # Regular assertion error, re-raise immediately
                                raise e

                        except Exception as e:
                            # Be more specific about rate limit detection to avoid false positives
                            error_str = str(e).lower()

                            # Only check for very specific FMP rate limit indicators
                            specific_rate_limit_indicators = [
                                "limit reach . please upgrade your plan",  # Full FMP message
                                "limit reach",  # FMP specific, but only if also contains upgrade
                            ]

                            # For "limit reach", require additional confirmation it's rate limiting
                            is_rate_limit = False
                            if "limit reach . please upgrade your plan" in error_str:
                                is_rate_limit = True
                            elif (
                                "limit reach" in error_str
                                and "upgrade your plan" in error_str
                            ):
                                is_rate_limit = True

                            if is_rate_limit:
                                last_exception = RateLimitError(
                                    f"Rate limit detected in error: {e}"
                                )
                                if attempt < max_retries:
                                    print(
                                        f"Rate limiting detected in error on attempt {attempt + 1}/{max_retries + 1} "
                                        f"for {test_item.name}. Triggering global cooldown..."
                                    )
                                    rate_limit_manager.trigger_cooldown()
                                    continue
                                else:
                                    pytest.skip(
                                        f"Rate limiting persisted after {max_retries} retries"
                                    )

                            # Not a rate limit error, re-raise immediately
                            raise e

                    # Should not reach here, but just in case
                    if last_exception:
                        pytest.skip(
                            f"Rate limiting persisted after {max_retries} retries"
                        )

                return wrapped_runtest

            # Check if it's already wrapped (avoid double-wrapping)
            if not hasattr(original_runtest, "_rate_limit_wrapped"):
                wrapped_runtest = make_wrapped_runtest(original_runtest, item)
                wrapped_runtest._rate_limit_wrapped = True
                item.runtest = wrapped_runtest


def pytest_runtest_makereport(item, call):
    """
    Make test reports, especially to customize skip reason display.
    """
    if call.when == "call":
        if call.excinfo is not None:
            if call.excinfo.type.__name__ == "Skipped":
                # Extract skip reason and make it more visible
                skip_reason = str(call.excinfo.value)
                if skip_reason:
                    # Print the skip reason so it's visible in output
                    print(f"\nSKIPPED: {item.name} - {skip_reason}")


def pytest_report_teststatus(report, config):
    """
    Customize how test statuses are reported.
    """
    if report.when == "call":
        if hasattr(report, "wasxfail"):
            return

        if report.skipped:
            # Extract skip reason from the report
            skip_reason = getattr(report.longrepr, "reprcrash", None)
            if skip_reason:
                reason_text = (
                    str(skip_reason).split("\n")[-1]
                    if skip_reason
                    else "Unknown reason"
                )
            else:
                reason_text = (
                    str(report.longrepr) if report.longrepr else "Unknown reason"
                )

            # Return custom skip status with reason
            return ("SKIPPED", "s", f"SKIPPED: {reason_text}")


# Export key utilities for use by test files
__all__ = [
    "RateLimitError",
    "with_rate_limit_retry",
    "extract_data_list",
    "is_rate_limit_error",
    "is_assertion_error_rate_limit",
    "rate_limit_manager",
]
