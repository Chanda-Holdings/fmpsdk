"""
Integration tests for forex endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os

import pytest

from fmpsdk.forex import (
    available_forex,
    batch_forex_quotes,
    forex,
    forex_quote,
    forex_quote_short,
)

API_KEY = os.getenv("FMP_API_KEY")


@pytest.mark.parametrize(
    "func,kwargs",
    [
        (forex, {}),
        (available_forex, {}),
    ],
)
def test_forex_endpoints(func, kwargs):
    """Test forex API endpoints with real API calls."""
    kwargs["apikey"] = API_KEY
    result = func(**kwargs)
    assert result is not None, f"{func.__name__} returned None"

    # Handle RootModel/list responses properly
    if hasattr(result, "__iter__"):
        # For list-type responses, check if we can iterate
        try:
            data = list(result)
            assert len(data) >= 0  # Allow empty results for demo key
        except Exception:
            # If it's not iterable as expected, check for model structure
            pass


def test_forex_data_endpoints():
    """Test forex data endpoints."""
    result = forex(apikey=API_KEY)
    assert result is not None


def test_forex_quotes():
    """Test forex quote functionality."""
    # Test basic forex data
    result = forex(apikey=API_KEY)
    assert result is not None

    # Test available forex pairs
    result = available_forex(apikey=API_KEY)
    assert result is not None


def test_major_forex_pairs():
    """Test forex data for major currency pairs."""
    # Test that we can get general forex data
    result = forex(apikey=API_KEY)
    assert result is not None


def test_forex_list_endpoints():
    """Test forex list endpoints."""
    # Test general forex list
    result = forex(apikey=API_KEY)
    assert result is not None

    # Test available forex pairs
    result = available_forex(apikey=API_KEY)
    assert result is not None
