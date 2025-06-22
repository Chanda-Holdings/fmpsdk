"""
Integration tests for stock_time_series endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""
import os
import pytest
import fmpsdk.stock_time_series as sts

API_KEY = os.getenv("FMP_API_KEY")

@pytest.mark.parametrize("func,kwargs", [
    (sts.quote_short, {"symbol": "AAPL"}),
    (sts.exchange_realtime, {"exchange": "NASDAQ"}),
    (sts.historical_stock_dividend, {"symbol": "AAPL"}),
    (sts.historical_stock_split, {"symbol": "AAPL"}),
    (sts.historical_survivorship_bias_free_eod, {"symbol": "AAPL", "date": "2024-01-02"}),
    (sts.live_full_price, {"symbol": "AAPL"}),
    (sts.historical_price_eod_full, {"symbol": "AAPL"}),
    (sts.historical_chart, {"symbol": "AAPL", "interval": "1min"}),
    (sts.historical_price_eod_light, {"symbol": "AAPL"}),
    (sts.historical_price_eod_non_split_adjusted, {"symbol": "AAPL"}),
    (sts.historical_price_eod_dividend_adjusted, {"symbol": "AAPL"}),
    (sts.historical_chart_1min, {"symbol": "AAPL"}),
    (sts.historical_chart_5min, {"symbol": "AAPL"}),
    (sts.historical_chart_15min, {"symbol": "AAPL"}),
    (sts.historical_chart_30min, {"symbol": "AAPL"}),
    (sts.historical_chart_1hour, {"symbol": "AAPL"}),
    (sts.historical_chart_4hour, {"symbol": "AAPL"}),
])
def test_stock_time_series_endpoints(func, kwargs):
    kwargs["apikey"] = API_KEY
    result = func(**kwargs)
    assert result is not None, f"{func.__name__} returned None"

def test_historical_data_with_date_ranges():
    """Test historical data endpoints with specific date ranges."""
    from_date = "2024-01-01"
    to_date = "2024-01-31"
    
    # Test EOD data with date range
    result = sts.historical_price_eod_full(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None
    
    # Test light EOD data
    result = sts.historical_price_eod_light(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None

def test_intraday_data_with_date_ranges():
    """Test intraday data with date ranges."""
    from_date = "2024-01-02"
    to_date = "2024-01-03"
    
    # Test 1-minute data
    result = sts.historical_chart_1min(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None
    
    # Test 5-minute data
    result = sts.historical_chart_5min(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None
    
    # Test hourly data
    result = sts.historical_chart_1hour(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None

def test_dividend_and_split_data():
    """Test dividend and stock split historical data."""
    # Test dividend history
    result = sts.historical_stock_dividend(apikey=API_KEY, symbol="AAPL")
    assert result is not None
    
    # Test stock split history
    result = sts.historical_stock_split(apikey=API_KEY, symbol="AAPL")
    assert result is not None

def test_adjusted_price_data():
    """Test different types of price adjustments."""
    from_date = "2024-01-01"
    to_date = "2024-01-31"
    
    # Test non-split adjusted data
    result = sts.historical_price_eod_non_split_adjusted(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None
    
    # Test dividend adjusted data
    result = sts.historical_price_eod_dividend_adjusted(
        apikey=API_KEY, 
        symbol="AAPL", 
        from_date=from_date, 
        to_date=to_date
    )
    assert result is not None

def test_survivorship_bias_free_data():
    """Test survivorship bias free endpoint."""
    # Test with a specific date
    result = sts.historical_survivorship_bias_free_eod(
        apikey=API_KEY, 
        symbol="AAPL", 
        date="2024-01-02"
    )
    assert result is not None

def test_real_time_data():
    """Test real-time and current data endpoints."""
    # Test current quote
    result = sts.quote_short(apikey=API_KEY, symbol="AAPL")
    assert result is not None
    
    # Test live full price (if available)
    result = sts.live_full_price(apikey=API_KEY, symbol="AAPL")
    assert result is not None

def test_exchange_data():
    """Test exchange-specific data."""
    # Test NASDAQ real-time data
    result = sts.exchange_realtime(apikey=API_KEY, exchange="NASDAQ")
    assert result is not None
    
    # Test NYSE real-time data
    result = sts.exchange_realtime(apikey=API_KEY, exchange="NYSE")
    assert result is not None

def test_different_time_intervals():
    """Test all supported time intervals for historical charts."""
    interval_functions = [
        (sts.historical_chart_1min, "1min"),
        (sts.historical_chart_5min, "5min"),
        (sts.historical_chart_15min, "15min"),
        (sts.historical_chart_30min, "30min"),
        (sts.historical_chart_1hour, "1hour"),
        (sts.historical_chart_4hour, "4hour"),
    ]
    symbol = "AAPL"
    
    for func, interval_name in interval_functions:
        result = func(
            apikey=API_KEY, 
            symbol=symbol,
            from_date="2024-01-02",
            to_date="2024-01-02"
        )
        assert result is not None, f"Failed for interval {interval_name}"

def test_multiple_symbols():
    """Test time series data for different types of symbols."""
    symbols = [
        "AAPL",    # Large cap
        "TSLA",    # Volatile stock
        "BRK.A",   # High-priced stock
        "MSFT",    # Another large cap
        "NVDA",    # Tech stock
    ]
    
    for symbol in symbols:
        # Test basic quote
        result = sts.quote_short(apikey=API_KEY, symbol=symbol)
        assert result is not None, f"Quote failed for {symbol}"
        
        # Test historical data (using date range instead of limit)
        result = sts.historical_price_eod_light(
            apikey=API_KEY, 
            symbol=symbol, 
            from_date="2024-01-01",
            to_date="2024-01-05"
        )
        assert result is not None, f"Historical data failed for {symbol}"

def test_return_type_verification():
    """Verify that all endpoints return proper Pydantic models."""
    test_functions = [
        (sts.quote_short, {"symbol": "AAPL"}),
        (sts.historical_price_eod_full, {"symbol": "AAPL", "from_date": "2024-01-01", "to_date": "2024-01-05"}),
        (sts.historical_chart_1min, {"symbol": "AAPL", "from_date": "2024-01-02", "to_date": "2024-01-02"}),
        (sts.historical_stock_dividend, {"symbol": "AAPL"}),
    ]
    
    for func, kwargs in test_functions:
        kwargs["apikey"] = API_KEY
        result = func(**kwargs)
        assert result is not None, f"{func.__name__} returned None"
        assert hasattr(result, '__dict__'), f"{func.__name__} should return a Pydantic model"
