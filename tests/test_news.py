"""
Integration tests for news endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os

import pytest

import fmpsdk.news as news

API_KEY = os.getenv("FMP_API_KEY")


@pytest.mark.parametrize(
    "func,kwargs",
    [
        (news.company_news, {}),
        (news.company_press_releases, {"symbols": "AAPL"}),
        (news.news_general, {}),  # Updated function name
        (news.news_crypto, {}),  # Updated function name
        (news.news_forex, {}),  # Updated function name
    ],
)
def test_news_endpoints(func, kwargs):
    """Test news API endpoints with real API calls."""
    from pydantic import RootModel

    kwargs["apikey"] = API_KEY
    result = func(**kwargs)
    assert result is not None, f"{func.__name__} returned None"

    # Verify return type - should be a list, dict, or Pydantic model
    assert isinstance(result, (list, dict, RootModel)) or hasattr(
        result, "__dict__"
    ), f"{func.__name__} should return a valid response"


def test_company_news_with_date_range():
    """Test company news with date range filters."""
    result = news.company_news(
        apikey=API_KEY,
        from_date="2024-01-01",
        to_date="2024-01-31",
        limit=10,
    )
    assert result is not None


def test_company_news_with_pagination():
    """Test company news with pagination."""
    # Get first page
    result_page_0 = news.company_news(apikey=API_KEY, page=0, limit=5)
    assert result_page_0 is not None

    # Get second page
    result_page_1 = news.company_news(apikey=API_KEY, page=1, limit=5)
    assert result_page_1 is not None


def test_press_releases_with_date_range():
    """Test press releases with date range filters."""
    result = news.company_press_releases(
        apikey=API_KEY,
        symbols="AAPL",
        from_date="2024-01-01",
        to_date="2024-12-31",
        limit=5,
    )
    assert result is not None


def test_news_multiple_symbols():
    """Test news endpoints with multiple symbols."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

    result = news.company_press_releases(apikey=API_KEY, symbols=symbols, limit=10)
    assert result is not None

    # Test with comma-separated string
    result = news.company_press_releases(
        apikey=API_KEY, symbols="AAPL,MSFT,GOOGL", limit=10
    )
    assert result is not None


def test_general_news_endpoints():
    """Test general news endpoints."""
    # General news
    result = news.news_general(apikey=API_KEY, limit=10)
    assert result is not None


def test_new_news_endpoints():
    """Test the new news endpoints with enhanced parameters."""
    # Test general news
    result = news.news_general(apikey=API_KEY, limit=5)
    assert result is not None

    # Test crypto news
    result = news.news_crypto(apikey=API_KEY, limit=5)
    assert result is not None

    # Test forex news
    result = news.news_forex(apikey=API_KEY, limit=5)
    assert result is not None


def test_new_news_endpoints_with_dates():
    """Test new news endpoints with date parameters."""
    from_date = "2024-01-01"
    to_date = "2024-01-31"

    # Test general news with dates
    result = news.news_general(
        apikey=API_KEY, from_date=from_date, to_date=to_date, limit=5
    )
    assert result is not None

    # Test crypto news with dates
    result = news.news_crypto(
        apikey=API_KEY, from_date=from_date, to_date=to_date, limit=5
    )
    assert result is not None

    # Test forex news with dates
    result = news.news_forex(
        apikey=API_KEY, from_date=from_date, to_date=to_date, limit=5
    )
    assert result is not None


def test_new_news_endpoints_with_pagination():
    """Test new news endpoints with pagination."""
    # Test general news pagination
    result_page_0 = news.news_general(apikey=API_KEY, page=0, limit=5)
    result_page_1 = news.news_general(apikey=API_KEY, page=1, limit=5)

    assert result_page_0 is not None
    assert result_page_1 is not None


def test_return_type_consistency():
    """Test that all news endpoints return valid responses."""
    from pydantic import RootModel

    # Test a few endpoints to ensure they return valid data
    result = news.company_news(apikey=API_KEY, limit=1)
    assert result is not None
    assert isinstance(
        result, (list, dict, RootModel)
    ), "Should return valid response data"

    result = news.news_general(apikey=API_KEY, limit=1)
    assert result is not None
    assert isinstance(
        result, (list, dict, RootModel)
    ), "Should return valid response data"
