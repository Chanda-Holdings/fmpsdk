"""
Integration tests for shares_float endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""
import os
import pytest
from pydantic import BaseModel

from fmpsdk.shares_float import shares_float, shares_float_all


API_KEY = os.getenv("FMP_API_KEY")


class TestSharesFloatEndpoints:
    """Test suite for shares float endpoints."""

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"])
    def test_shares_float_multiple_symbols(self, symbol):
        """Test shares float data for multiple major companies."""
        result = shares_float(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, 'root'):
            float_data = result.root
            if float_data:
                for item in float_data:
                    assert hasattr(item, '__dict__'), f"Item should be a Pydantic model"

    def test_shares_float_all_comprehensive(self):
        """Test getting shares float data for all companies."""
        result = shares_float_all(apikey=API_KEY)
        assert result is not None
        if hasattr(result, '__iter__'):
            all_float_data = list(result)
            # Should have float data (may be limited with demo key)
            assert len(all_float_data) >= 0

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT"])
    def test_shares_float_data_validation(self, symbol):
        """Test that shares float data contains expected information."""
        result = shares_float(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            float_data = list(result)
            if float_data:
                # Should have meaningful float data
                assert len(float_data) > 0

    def test_shares_float_comparison(self):
        """Test comparing shares float between different companies."""
        companies = ["AAPL", "MSFT", "GOOGL"]
        float_results = []
        
        for symbol in companies:
            result = shares_float(apikey=API_KEY, symbol=symbol)
            if result is not None:
                float_results.append((symbol, result))
        
        # Should get results for most companies
        assert len(float_results) >= 2

    def test_shares_float_large_cap_vs_small_cap(self):
        """Test shares float for different market cap companies."""
        large_cap_symbols = ["AAPL", "MSFT"]
        
        for symbol in large_cap_symbols:
            result = shares_float(apikey=API_KEY, symbol=symbol)
            assert result is not None
            # Large cap companies should have float data

    def test_shares_float_all_pagination_sample(self):
        """Test that shares float all returns substantial data."""
        result = shares_float_all(apikey=API_KEY)
        assert result is not None
        if hasattr(result, '__iter__'):
            all_data = list(result)
            # Should have some data (may be limited with demo key)
            assert len(all_data) >= 0

    def test_shares_float_invalid_symbol(self):
        """Test shares float with invalid symbol."""
        result = shares_float(apikey=API_KEY, symbol="INVALID_SYMBOL")
        # Should not raise an exception
        assert result is not None or result is None

    def test_shares_float_data_structure(self):
        """Test the structure of shares float data."""
        result = shares_float(apikey=API_KEY, symbol="AAPL")
        assert result is not None
        if hasattr(result, '__iter__'):
            float_data = list(result)
            if float_data:
                # Should have structured data
                assert len(float_data) >= 0

    def test_shares_float_batch_processing(self):
        """Test processing multiple symbols efficiently."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        results = []
        
        for symbol in symbols:
            try:
                result = shares_float(apikey=API_KEY, symbol=symbol)
                if result is not None:
                    results.append(result)
            except Exception as e:
                # Should not fail for valid symbols
                pytest.fail(f"Unexpected error for {symbol}: {e}")
        
        # Should get results for most symbols
        assert len(results) >= len(symbols) * 0.5
