"""
Test configuration and utilities for fmpsdk integration tests.
"""
import os
import pytest
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test configuration
API_KEY = os.getenv("FMP_API_KEY")
RATE_LIMIT_DELAY = 0.1  # Delay between API calls to respect rate limits

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
        "to": datetime.now().strftime("%Y-%m-%d")
    },
    "recent_quarter": {
        "from": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
        "to": datetime.now().strftime("%Y-%m-%d")
    },
    "year_2024": {
        "from": "2024-01-01",
        "to": "2024-12-31"
    },
    "jan_2024": {
        "from": "2024-01-01",
        "to": "2024-01-31"
    }
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
        assert hasattr(result, '__dict__'), f"{func_name} should return a Pydantic model"
    
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
            **extra_kwargs
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
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "rate_limited: mark test as potentially rate limited"
    )
