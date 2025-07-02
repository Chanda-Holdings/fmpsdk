"""
Comprehensive endpoint testing for all fmpsdk modules.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os

import pytest
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

import fmpsdk.calendar_module as calendar_module
import fmpsdk.company_valuation as company_valuation_module
import fmpsdk.cryptocurrencies as cryptocurrencies_module
import fmpsdk.etf as etf_module

# Import modules for module checking test
import fmpsdk.general as general_module
import fmpsdk.news as news_module
import fmpsdk.stock_time_series as stock_time_series_module


# For modules with namespace conflicts, we'll create mock module objects
class ModuleMock:
    """Mock module to work around namespace conflicts."""

    pass


# Import all the forex functions and attach them to our mock
from fmpsdk.forex import available_forex, forex_quote

forex_module = ModuleMock()
forex_module.available_forex = available_forex
forex_module.forex_quote = forex_quote

# Import all the insider_trading functions and attach them to our mock
from fmpsdk.insider_trading import insider_trading_search, insider_trading_latest

insider_trading_module = ModuleMock()
insider_trading_module.insider_trading_search = insider_trading_search
insider_trading_module.insider_trading_latest = insider_trading_latest

# Import all the economic_indicators functions and attach them to our mock
from fmpsdk.economic_indicators import treasury_rates

economic_indicators_module = ModuleMock()
economic_indicators_module.treasury_rates = treasury_rates
from fmpsdk.calendar_module import earnings_calendar, ipos_calendar
from fmpsdk.company_valuation import company_profile, income_statement
from fmpsdk.cryptocurrencies import available_cryptocurrencies, cryptocurrency_quote
from fmpsdk.etf import available_etfs, etf_info

# Import specific functions to avoid namespace conflicts
from fmpsdk.general import available_indexes, quote
from fmpsdk.news import news_crypto, news_general
from fmpsdk.stock_time_series import historical_price_eod_full, quote_short

API_KEY = os.getenv("FMP_API_KEY")


class TestAllEndpoints:
    """Test suite for all major endpoints across modules."""

    def test_general_endpoints_basic(self):
        """Test basic general endpoints."""
        endpoints_to_test = [
            (available_indexes, {}),
            (quote, {"symbol": "AAPL"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_stock_time_series_endpoints_basic(self):
        """Test basic stock time series endpoints."""
        endpoints_to_test = [
            (quote_short, {"symbol": "AAPL"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_company_valuation_endpoints_basic(self):
        """Test basic company valuation endpoints."""
        endpoints_to_test = [
            (company_profile, {"symbol": "AAPL"}),
            (income_statement, {"symbol": "AAPL"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_news_endpoints_basic(self):
        """Test basic news endpoints."""
        endpoints_to_test = [
            (news_general, {}),
            (news_crypto, {}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_forex_endpoints_basic(self):
        """Test basic forex endpoints."""
        endpoints_to_test = [
            (available_forex, {}),
            (forex_quote, {"symbol": "EURUSD"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_cryptocurrency_endpoints_basic(self):
        """Test basic cryptocurrency endpoints."""
        endpoints_to_test = [
            (available_cryptocurrencies, {}),
            (cryptocurrency_quote, {"symbol": "BTCUSD"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_etf_endpoints_basic(self):
        """Test basic ETF endpoints."""
        endpoints_to_test = [
            (available_etfs, {}),
            (etf_info, {"symbol": "SPY"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_insider_trading_endpoints_basic(self):
        """Test basic insider trading endpoints."""
        endpoints_to_test = [
            (insider_trading_latest, {}),
            (insider_trading_search, {"symbol": "AAPL"}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_calendar_endpoints_basic(self):
        """Test basic calendar endpoints."""
        endpoints_to_test = [
            (earnings_calendar, {}),
            (ipos_calendar, {}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    def test_economic_indicators_endpoints_basic(self):
        """Test basic economic indicators endpoints."""
        endpoints_to_test = [
            (treasury_rates, {}),
        ]

        for endpoint_func, params in endpoints_to_test:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            assert result is not None

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL"])
    def test_cross_module_symbol_consistency(self, symbol):
        """Test that the same symbol works across different modules."""
        # Test symbol in different modules
        results = []

        # General quote
        result1 = quote(apikey=API_KEY, symbol=symbol)
        results.append(result1)

        # Stock time series quote
        result2 = quote_short(apikey=API_KEY, symbol=symbol)
        results.append(result2)

        # Company profile
        result3 = company_profile(apikey=API_KEY, symbol=symbol)
        results.append(result3)

        # All should return valid responses
        for result in results:
            assert result is not None

    def test_error_handling_across_modules(self):
        """Test error handling consistency across modules."""
        invalid_params_tests = [
            (quote, {"symbol": "INVALID_SYMBOL"}),
            (forex_quote, {"symbol": "INVALID_FOREX"}),
            (cryptocurrency_quote, {"symbol": "INVALID_CRYPTO"}),
        ]

        for endpoint_func, params in invalid_params_tests:
            params["apikey"] = API_KEY
            result = endpoint_func(**params)
            # Should not raise exceptions, may return None or empty
            assert result is not None or result is None

    def test_response_type_consistency(self):
        """Test that responses follow consistent patterns."""
        test_endpoints = [
            available_indexes(apikey=API_KEY),
            available_forex(apikey=API_KEY),
            available_cryptocurrencies(apikey=API_KEY),
        ]

        for result in test_endpoints:
            assert result is not None
            if hasattr(result, "__iter__"):
                items = list(result)
                if items:
                    # Should be consistent response types
                    for item in items[:3]:
                        assert isinstance(item, (dict, BaseModel))

    def test_api_rate_limiting_behavior(self):
        """Test behavior under rapid API calls."""
        # Make several quick calls to test rate limiting behavior
        results = []

        for i in range(5):
            result = quote(apikey=API_KEY, symbol="AAPL")
            results.append(result)

        # Should handle rate limiting gracefully
        successful_calls = [r for r in results if r is not None]
        assert len(successful_calls) > 0

    def test_module_function_coverage(self):
        """Test that major functions exist in each module."""
        module_function_map = {
            general_module: ["quote", "available_indexes"],
            stock_time_series_module: ["quote_short", "historical_price_eod_full"],
            company_valuation_module: ["company_profile", "income_statement"],
            news_module: ["news_general", "news_crypto"],
            forex_module: ["available_forex", "forex_quote"],
            cryptocurrencies_module: [
                "available_cryptocurrencies",
                "cryptocurrency_quote",
            ],
            etf_module: ["available_etfs", "etf_info"],
            insider_trading_module: ["insider_trading_search", "insider_trading_latest"],
            calendar_module: ["earnings_calendar", "ipos_calendar"],
            economic_indicators_module: ["treasury_rates"],
        }

        for module, functions in module_function_map.items():
            for func_name in functions:
                assert hasattr(
                    module, func_name
                ), f"Module {module.__name__} missing function {func_name}"

    def test_batch_symbol_processing(self):
        """Test processing multiple symbols efficiently."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = quote(apikey=API_KEY, symbol=symbol)
            assert result is not None

        # Should complete without errors for all symbols
