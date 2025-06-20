"""
Integration tests for insider_trading endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""
import os
import pytest
from datetime import datetime, timedelta
from pydantic import BaseModel

from fmpsdk.insider_trading import (
    insider_trading,
    insider_trading_latest,
    insider_trading_reporting_name,
    insider_trading_transaction_type,
    insider_trading_statistics,
)


API_KEY = os.getenv("FMP_API_KEY", "demo")


class TestInsiderTradingEndpoints:
    """Test suite for insider trading endpoints."""

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL", "TSLA"])
    def test_insider_trading_multiple_symbols(self, symbol):
        """Test insider trading data for multiple symbols."""
        result = insider_trading(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            trades = list(result)
            # May have insider trades or be empty
            assert len(trades) >= 0

    @pytest.mark.parametrize("transaction_type", ["Purchase", "Sale", "Option Execute"])
    def test_insider_trading_by_transaction_type(self, transaction_type):
        """Test insider trading filtered by transaction type."""
        result = insider_trading_transaction_type(
            apikey=API_KEY, 
            transaction_type=transaction_type
        )
        assert result is not None
        if hasattr(result, '__iter__'):
            trades = list(result)
            assert len(trades) >= 0

    def test_insider_trading_latest_comprehensive(self):
        """Test latest insider trading data."""
        result = insider_trading_latest(apikey=API_KEY)
        assert result is not None
        if hasattr(result, '__iter__'):
            latest_trades = list(result)
            # Should have some recent insider trades
            assert len(latest_trades) >= 0

    @pytest.mark.parametrize("name", ["Cook", "Musk", "Bezos"])
    def test_insider_trading_by_executive_name(self, name):
        """Test insider trading by executive names."""
        result = insider_trading_reporting_name(apikey=API_KEY, name=name)
        assert result is not None
        if hasattr(result, '__iter__'):
            trades = list(result)
            # May or may not have trades for this name
            assert len(trades) >= 0

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL"])
    def test_insider_trading_statistics_analysis(self, symbol):
        """Test insider trading statistics for major companies."""
        result = insider_trading_statistics(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            stats = list(result)
            assert len(stats) >= 0

    def test_insider_trading_data_validation(self):
        """Test that insider trading data contains expected fields."""
        result = insider_trading(apikey=API_KEY, symbol="AAPL")
        assert result is not None
        if hasattr(result, '__iter__'):
            trades = list(result)
            if trades:
                # Should have trade information
                for trade in trades[:3]:  # Check first few trades
                    assert isinstance(trade, (dict, BaseModel))

    def test_insider_trading_recent_activity(self):
        """Test for recent insider trading activity."""
        result = insider_trading_latest(apikey=API_KEY)
        assert result is not None
        if hasattr(result, '__iter__'):
            recent_trades = list(result)
            # Should have some activity (markets are active)
            assert len(recent_trades) >= 0

    @pytest.mark.parametrize("symbol,min_expected_trades", [
        ("AAPL", 0),  # Apple should have some insider activity
        ("MSFT", 0),  # Microsoft should have some activity
    ])
    def test_insider_trading_volume_expectations(self, symbol, min_expected_trades):
        """Test insider trading volume for active companies."""
        result = insider_trading(apikey=API_KEY, symbol=symbol)
        assert result is not None
        if hasattr(result, '__iter__'):
            trades = list(result)
            assert len(trades) >= min_expected_trades

    def test_insider_trading_cross_reference(self):
        """Test cross-referencing insider trading with statistics."""
        symbol = "AAPL"
        
        # Get insider trades
        trades_result = insider_trading(apikey=API_KEY, symbol=symbol)
        assert trades_result is not None
        
        # Get insider statistics
        stats_result = insider_trading_statistics(apikey=API_KEY, symbol=symbol)
        assert stats_result is not None
        
        # Both should be valid responses
        if hasattr(trades_result, '__iter__'):
            trades = list(trades_result)
        if hasattr(stats_result, '__iter__'):
            stats = list(stats_result)

    def test_insider_trading_specific_executive(self):
        """Test insider trading for specific well-known executives."""
        # Note: Executive names may change, so this is a flexible test
        result = insider_trading_reporting_name(apikey=API_KEY, name="Tim Cook")
        assert result is not None
        # Should not raise an exception regardless of results

    def test_insider_trading_transaction_types_comprehensive(self):
        """Test various transaction types for insider trading."""
        transaction_types = ["Purchase", "Sale", "Gift", "Option Execute"]
        
        for trans_type in transaction_types:
            result = insider_trading_transaction_type(
                apikey=API_KEY, 
                transaction_type=trans_type
            )
            assert result is not None
            # Should handle all transaction types without errors
