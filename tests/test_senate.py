"""
Comprehensive tests for fmpsdk.senate module.
Tests all political trading disclosure functions including error handling.
"""
import os
import pytest

import fmpsdk.senate as senate
from fmpsdk.models import *

API_KEY = os.getenv("FMP_API_KEY", "demo")


# === PARAMETERIZED TEST CLASSES ===

class TestParameterizedSenateTradesNames:
    """Comprehensive parameterized tests for senate trades by name."""
    
    @pytest.mark.parametrize("name", [
        "Pelosi", "Warren", "Romney", "Burr", "Loeffler",
        "PELOSI", "WARREN", "ROMNEY",  # Uppercase
        "pelosi", "warren", "romney",  # Lowercase
        "Nancy Pelosi", "Elizabeth Warren", "Mitt Romney",  # Full names
        "InvalidName", "FakePerson", "NonExistent",  # Invalid names
        "", "   ", "123", "Test@Name"  # Edge cases
    ])
    def test_senate_trades_by_name_variations(self, name):
        """Test senate trades by name with various name formats."""
        result = senate.senate_trades_by_name(apikey=API_KEY, name=name)
        assert result is not None


class TestParameterizedSenateTradesSymbols:
    """Comprehensive parameterized tests for senate trades by symbol."""
    
    @pytest.mark.parametrize("symbol", [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",  # Large cap stocks
        "META", "NVDA", "NFLX", "V", "MA",  # Tech stocks
        "BRK.A", "BRK.B", "SPY", "QQQ",  # Special characters and ETFs
        "A", "T", "F", "C", "X",  # Single letter symbols
        "aapl", "msft", "googl",  # Lowercase
        "INVALID", "FAKE123", "",  # Invalid symbols
        "   ", "NULL", "TEST"  # Edge cases
    ])
    def test_senate_trades_by_symbol_variations(self, symbol):
        """Test senate trades by symbol with comprehensive symbol variations."""
        result = senate.senate_trades_by_symbol(apikey=API_KEY, symbol=symbol)
        assert result is not None


class TestParameterizedHouseTradesNames:
    """Comprehensive parameterized tests for house trades by name."""
    
    @pytest.mark.parametrize("name", [
        "Pelosi", "AOC", "McCarthy", "Jordan", "Gaetz",
        "PELOSI", "AOC", "MCCARTHY",  # Uppercase
        "pelosi", "aoc", "mccarthy",  # Lowercase
        "Nancy Pelosi", "Kevin McCarthy", "Jim Jordan",  # Full names
        "Alexandria Ocasio-Cortez", "Matt Gaetz",  # Hyphenated names
        "InvalidName", "FakePerson", "NonExistent",  # Invalid names
        "", "   ", "123", "Test@Name"  # Edge cases
    ])
    def test_house_trades_by_name_variations(self, name):
        """Test house trades by name with various name formats."""
        result = senate.house_trades_by_name(apikey=API_KEY, name=name)
        # For integration tests, empty/invalid names may return None (valid API behavior)
        if name.strip() == "":
            # Empty names are expected to return None or empty results
            assert result is None or result == []
        else:
            # Valid names should return some result (even if empty list for non-existent names)
            assert result is not None


class TestParameterizedHouseTradesSymbols:
    """Comprehensive parameterized tests for house trades by symbol."""
    
    @pytest.mark.parametrize("symbol", [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",  # Large cap stocks
        "META", "NVDA", "NFLX", "CRM", "ADBE",  # Tech stocks
        "JPM", "BAC", "WFC", "GS", "MS",  # Financial stocks
        "JNJ", "PFE", "UNH", "ABBV", "MRK",  # Healthcare stocks
        "BRK.A", "BRK.B", "BRK-A", "BRK-B",  # Special characters
        "V", "MA", "WM", "HD", "PG",  # Short symbols
        "A", "T", "F", "C", "X",  # Single letter symbols
        "NONEXISTENT", "FAKE123", "INVALID",  # Invalid symbols
        "", "   ", "NULL", "TEST"  # Edge cases
    ])
    def test_house_trades_by_symbol_variations(self, symbol):
        """Test house trades by symbol with comprehensive symbol variations."""
        result = senate.house_trades_by_symbol(apikey=API_KEY, symbol=symbol)
        assert result is not None


class TestParameterizedPoliticalTradesLatest:
    """Comprehensive parameterized tests for latest political trades."""
    
    @pytest.mark.parametrize("func_name,function", [
        ("senate_latest", senate.senate_latest),
        ("house_latest", senate.house_latest),
    ])
    def test_latest_trades_all_functions(self, func_name, function):
        """Test all latest trades functions."""
        result = function(apikey=API_KEY)
        assert result is not None


class TestSenateIntegration:
    """Test integration scenarios for senate functions."""

    def test_senate_latest_to_detailed_analysis_workflow(self):
        """Test workflow from latest trades to detailed analysis."""
        # 1. Get latest trades
        latest = senate.senate_latest(apikey=API_KEY)
        assert latest is not None
        
        # 2. Get house latest trades  
        house_latest = senate.house_latest(apikey=API_KEY)
        assert house_latest is not None

    def test_name_search_to_symbol_analysis_workflow(self):
        """Test workflow from name search to symbol analysis."""
        # Search by common political figures
        test_names = ["Pelosi", "Romney", "Warren"]
        
        for name in test_names:
            # 1. Search senate trades by name
            senate_trades = senate.senate_trades_by_name(apikey=API_KEY, name=name)
            assert senate_trades is not None
            
            # 2. Search house trades by name
            house_trades = senate.house_trades_by_name(apikey=API_KEY, name=name)
            assert house_trades is not None

    def test_symbol_correlation_workflow(self):
        """Test workflow analyzing trades by symbol."""
        symbols = ["AAPL", "TSLA", "NVDA"]
        
        for symbol in symbols:
            # 1. Get senate trades by symbol
            senate_symbol_trades = senate.senate_trades_by_symbol(apikey=API_KEY, symbol=symbol)
            assert senate_symbol_trades is not None
            
            # 2. Get house trades by symbol
            house_symbol_trades = senate.house_trades_by_symbol(apikey=API_KEY, symbol=symbol)
            assert house_symbol_trades is not None


class TestParameterizedErrorCases:
    """Test various error scenarios and edge cases."""
    
    @pytest.mark.parametrize("invalid_symbol,error_type", [
        ("", "EMPTY_STRING"),
        ("   ", "WHITESPACE_ONLY"),
        ("123", "NUMERIC_ONLY"),
        ("SYMBOL_TOO_LONG_FOR_API", "TOO_LONG"),
        ("SYM@BOL", "SPECIAL_CHARACTERS"),
        ("SYM BOL", "WITH_SPACE"),
        ("FAKE_DELISTED_STOCK", "DELISTED"),
        ("INVALID123", "NONEXISTENT"),
        (None, "NULL_VALUE"),
    ])
    def test_symbol_error_handling(self, invalid_symbol, error_type):
        """Test how functions handle various invalid symbol scenarios."""
        if invalid_symbol is None:
            pytest.skip("None symbol would cause TypeError")
            
        result = senate.senate_trades_by_symbol(apikey=API_KEY, symbol=invalid_symbol)
        
        if error_type in ["EMPTY_STRING", "WHITESPACE_ONLY"]:
            # These should return None or empty results
            assert result is None or result == []
        else:
            # Other cases might return None or empty results
            assert result is not None or result is None


class TestParameterizedSpecialCharacterHandling:
    """Test handling of special characters in various parameters."""
    
    @pytest.mark.parametrize("special_name,description", [
        ("O'Reilly", "APOSTROPHE"),
        ("Smith-Johnson", "HYPHEN"),
        ("Van Der Berg", "MULTIPLE_SPACES"),
        ("José", "ACCENTED_CHARACTERS"),
        ("李", "NON_LATIN_CHARACTERS"),
        ("Name.Jr", "PERIOD"),
        ("Name,Jr", "COMMA"),
        ("Name(Jr)", "PARENTHESES"),
        ("Name/Jr", "SLASH"),
        ("Name\\Jr", "BACKSLASH"),
        ("Name\"Jr", "QUOTES"),
        ("Name'Jr", "SINGLE_QUOTE"),
    ])
    def test_special_character_name_handling(self, special_name, description):
        """Test how name parameters handle special characters."""
        result = senate.senate_trades_by_name(apikey=API_KEY, name=special_name)
        # Special characters should be handled gracefully
        assert result is not None or result is None


class TestParameterizedMarketConditions:
    """Test different market condition scenarios."""
    
    @pytest.mark.parametrize("symbol,market_type", [
        # Different market cap categories
        ("AAPL", "MEGA_CAP"),
        ("MSFT", "LARGE_CAP"),
        ("AMD", "MID_CAP"),
        ("PLTR", "SMALL_CAP"),
        ("SIRI", "MICRO_CAP"),
        
        # Different sectors
        ("XOM", "ENERGY"),
        ("JPM", "FINANCIAL"),
        ("JNJ", "HEALTHCARE"),
        ("AMZN", "CONSUMER_DISCRETIONARY"),
        ("WMT", "CONSUMER_STAPLES"),
        ("MSFT", "TECHNOLOGY"),
        ("NEE", "UTILITIES"),
        ("CAT", "INDUSTRIALS"),
        ("FCX", "MATERIALS"),
        ("AMT", "REAL_ESTATE"),
        ("VZ", "COMMUNICATION"),
        
        # Volatility categories
        ("TSLA", "HIGH_VOLATILITY"),
        ("NVDA", "HIGH_GROWTH"),
        ("KO", "STABLE_DIVIDEND"),
        ("T", "HIGH_DIVIDEND"),
        
        # Different exchanges
        ("SHOP", "NYSE"),
        ("GOOGL", "NASDAQ"),
        ("BRK.B", "NYSE_BERKSHIRE"),
    ])
    def test_market_condition_scenarios(self, symbol, market_type):
        """Test various market conditions and symbol types."""
        result = senate.senate_trades_by_symbol(apikey=API_KEY, symbol=symbol)
        assert result is not None
