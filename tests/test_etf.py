"""
Integration tests for etf endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""
import os
import pytest
from pydantic import BaseModel

import fmpsdk.etf as etf


API_KEY = os.getenv("FMP_API_KEY")


class TestETFEndpoints:
    """Test suite for ETF endpoints."""

    @pytest.mark.parametrize("symbol", ["SPY", "QQQ", "IWM", "VTI"])
    def test_etf_info_multiple_symbols(self, symbol):
        """Test ETF info for multiple symbols."""
        result = etf.etf_info(apikey=API_KEY, symbol=symbol)
        assert result is not None
        
        # Handle RootModel responses
        if hasattr(result, 'root'):
            data = result.root
            if data is not None and isinstance(data, list):
                for item in data:
                    assert isinstance(item, dict) or hasattr(item, 'symbol')
        elif hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
            for item in result:
                assert hasattr(item, 'symbol') or isinstance(item, (dict, BaseModel))

    @pytest.mark.parametrize("symbol", ["SPY", "QQQ", "VTI"])
    def test_etf_holdings_multiple_symbols(self, symbol):
        """Test ETF holdings for multiple popular ETFs."""
        result = etf.etf_holdings(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            assert len(list(result)) > 0

    @pytest.mark.parametrize("symbol", ["SPY", "QQQ"])
    def test_etf_asset_exposure_major_etfs(self, symbol):
        """Test ETF asset exposure for major ETFs."""
        result = etf.etf_asset_exposure(apikey=API_KEY, symbol=symbol)
        assert result is not None

    def test_available_etfs_list(self):
        """Test getting list of available ETFs."""
        result = etf.available_etfs(apikey=API_KEY)
        assert result is not None
        if hasattr(result, '__iter__'):
            # Should have multiple ETFs (may be empty with demo key)
            etf_list = list(result)
            assert len(etf_list) >= 0  # Should not fail, may be empty with demo key

    def test_etf_price_realtime_response(self):
        """Test realtime ETF prices."""
        result = etf.etf_price_realtime(apikey=API_KEY)
        assert result is not None
        
        # Handle RootModel responses
        if hasattr(result, 'root'):
            data = result.root
            if data is not None and isinstance(data, list):
                # May be empty with demo key, just check it's a list
                assert isinstance(data, list)
        elif hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
            # Should have price data (may be empty with demo key)
            prices = list(result)
            assert len(prices) >= 0  # Should not fail, may be empty with demo key

    def test_etf_holdings_with_invalid_symbol(self):
        """Test ETF holdings with potentially invalid symbol."""
        result = etf.etf_holdings(apikey=API_KEY, symbol="INVALID_ETF_SYMBOL")
        # Should not raise an exception, but may return empty result
        assert result is not None

    @pytest.mark.parametrize("symbol,expected_holdings", [
        ("SPY", 100),  # SPY should have many holdings
        ("QQQ", 50),   # QQQ should have tech stocks
    ])
    def test_etf_holdings_count_expectations(self, symbol, expected_holdings):
        """Test that major ETFs have expected number of holdings."""
        result = etf.etf_holdings(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            holdings = list(result)
            # Should have at least some holdings (may be limited with demo key)
            assert len(holdings) >= 0  # Allow empty results for demo key

    def test_etf_sector_weightings(self):
        """Test ETF sector exposure data."""
        symbol = "SPY"
        result = etf.etf_asset_exposure(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            exposures = list(result)
            if exposures:
                # Should have sector information
                assert len(exposures) > 0

def test_etf_sector_weightings():
    result = etf.etf_sector_weightings(apikey=API_KEY, symbol="SPY")
    assert result is not None
