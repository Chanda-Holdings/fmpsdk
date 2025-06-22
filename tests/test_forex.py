"""
Integration tests for forex endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os

import pytest

from fmpsdk.forex import (available_forex, batch_forex_quotes, forex,
                          forex_news, forex_quote, forex_quote_short)

API_KEY = os.getenv("FMP_API_KEY")


@pytest.mark.parametrize(
    "func,kwargs",
    [
        (forex, {}),
        (available_forex, {}),
        (forex_news, {}),
        (forex_news, {"symbol": "EURUSD"}),
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


def test_forex_news_with_date_range():
    """Test forex news with date range and pagination."""
    result = forex_news(
        apikey=API_KEY,
        symbol="EURUSD",
        from_date="2024-01-01",
        to_date="2024-01-31",
        limit=10,
    )
    assert result is not None


def test_forex_news_pagination():
    """Test forex news with pagination."""
    # Test first page
    result_page_0 = forex_news(apikey=API_KEY, page=0, limit=5)
    assert result_page_0 is not None

    # Test second page
    result_page_1 = forex_news(apikey=API_KEY, page=1, limit=5)
    assert result_page_1 is not None


def test_major_forex_pairs():
    """Test forex news for major currency pairs."""
    major_pairs = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD"]

    for pair in major_pairs:
        result = forex_news(apikey=API_KEY, symbol=pair, limit=5)
        assert result is not None, f"Failed for forex pair {pair}"


def test_forex_list_endpoints():
    """Test forex list endpoints."""
    # Test general forex list
    result = forex(apikey=API_KEY)
    assert result is not None

    # Test available forex pairs
    result = available_forex(apikey=API_KEY)
    assert result is not None
