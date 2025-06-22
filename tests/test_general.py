"""
Integration tests for general endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""
import os
import pytest
import fmpsdk.general as general

API_KEY = os.getenv("FMP_API_KEY")

@pytest.mark.parametrize("func,kwargs", [
    (general.search_symbol, {"query": "AAPL"}),
    (general.search_name, {"query": "Apple"}),
    (general.search_cik, {"query": "0000320193"}),
    (general.search_cusip, {"query": "037833100"}),
    (general.search_isin, {"query": "US0378331005"}),
    (general.company_screener, {}),
    (general.search_exchange_variants, {"symbol": "AAPL"}),
    (general.stock_list, {}),
    (general.cik_list, {}),
    (general.symbol_change, {}),
    (general.etf_list, {}),
    (general.actively_trading_list, {}),
    (general.earnings_transcript_list, {}),
    (general.available_exchanges, {}),
    (general.available_sectors, {}),
    (general.available_industries, {}),
    (general.available_countries, {}),
])
def test_general_endpoints(func, kwargs):
    """Test general API endpoints with real API calls."""
    kwargs["apikey"] = API_KEY
    result = func(**kwargs)
    assert result is not None, f"{func.__name__} returned None"
    
    # Verify return type is correct Pydantic model
    print(type(result))
    if type(result) == list:
        print(type(result[0]))
    assert hasattr(result, '__dict__'), f"{func.__name__} should return a Pydantic model"

def test_search_endpoints_with_limits():
    """Test search endpoints with various parameters."""
    # Test search with limit
    result = general.search_symbol(apikey=API_KEY, query="A", limit=5)
    assert result is not None
    
    # Test search with exchange filter
    result = general.search_symbol(apikey=API_KEY, query="AAPL", exchange="NASDAQ")
    assert result is not None

def test_company_screener_with_filters():
    """Test company screener with various filter parameters."""
    result = general.company_screener(
        apikey=API_KEY,
        market_cap_more_than=1000000000,  # $1B+
        limit=10
    )
    assert result is not None
    
    # Test with sector filter
    result = general.company_screener(
        apikey=API_KEY,
        sector="Technology",
        limit=5
    )
    assert result is not None

def test_error_handling():
    """Test error handling for invalid inputs."""
    # Test with invalid symbol (should still return a response, possibly empty)
    result = general.search_symbol(apikey=API_KEY, query="INVALIDXYZABC123")
    assert result is not None  # API might return empty results but not None
