"""
Integration tests for news endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""
import os
import pytest
import fmpsdk.news as news

API_KEY = os.getenv("FMP_API_KEY", "demo")

@pytest.mark.parametrize("func,kwargs", [
    (news.company_news, {"symbols": "AAPL"}),
    (news.company_news, {"symbols": ["AAPL", "MSFT"]}),  # Test with list
    (news.company_news_latest, {}),
    (news.company_press_releases, {"symbols": "AAPL"}),
    (news.company_press_releases, {"symbols": ["AAPL", "GOOGL"]}),  # Test with list
    (news.company_press_releases_latest, {}),
])
def test_news_endpoints(func, kwargs):
    """Test news API endpoints with real API calls."""
    kwargs["apikey"] = API_KEY
    result = func(**kwargs)
    assert result is not None, f"{func.__name__} returned None"
    
    # Verify return type is correct Pydantic model
    assert hasattr(result, '__dict__'), f"{func.__name__} should return a Pydantic model"

def test_company_news_with_date_range():
    """Test company news with date range filters."""
    result = news.company_news(
        apikey=API_KEY,
        symbols="AAPL",
        from_date="2024-01-01",
        to_date="2024-01-31",
        limit=10
    )
    assert result is not None

def test_company_news_with_pagination():
    """Test company news with pagination."""
    # Get first page
    result_page_0 = news.company_news(
        apikey=API_KEY,
        symbols="AAPL",
        page=0,
        limit=5
    )
    assert result_page_0 is not None
    
    # Get second page
    result_page_1 = news.company_news(
        apikey=API_KEY,
        symbols="AAPL",
        page=1,
        limit=5
    )
    assert result_page_1 is not None

def test_press_releases_with_date_range():
    """Test press releases with date range filters."""
    result = news.company_press_releases(
        apikey=API_KEY,
        symbols="AAPL",
        from_date="2024-01-01",
        to_date="2024-12-31",
        limit=5
    )
    assert result is not None

def test_news_multiple_symbols():
    """Test news endpoints with multiple symbols."""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    
    result = news.company_news(
        apikey=API_KEY,
        symbols=symbols,
        limit=10
    )
    assert result is not None
    
    # Test with comma-separated string
    result = news.company_news(
        apikey=API_KEY,
        symbols="AAPL,MSFT,GOOGL",
        limit=10
    )
    assert result is not None

def test_general_news_endpoints():
    """Test general news endpoints without specific symbols."""
    # Latest company news
    result = news.company_news_latest(apikey=API_KEY, limit=10)
    assert result is not None
    
    # Latest press releases
    result = news.company_press_releases_latest(apikey=API_KEY, limit=10)
    assert result is not None
