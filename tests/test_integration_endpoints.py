"""
Comprehensive integration tests across all fmpsdk endpoints.
This file tests end-to-end functionality and cross-module interactions.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os
import time

import fmpsdk.calendar_module as calendar
import fmpsdk.commodities as commodities
import fmpsdk.company_valuation as cv
import fmpsdk.cryptocurrencies as crypto
import fmpsdk.etf as etf
import fmpsdk.tsx as tsx


# For modules that have function name conflicts, create mock modules
class ModuleMock:
    """Mock module to work around namespace conflicts."""

    pass


# Import and setup economic indicators
from fmpsdk.economic_indicators import economic_indicators, treasury_rates

economic = ModuleMock()
economic.treasury_rates = treasury_rates
economic.economic_indicators = economic_indicators

# Import and setup forex
from fmpsdk.forex import available_forex, forex

forex_mod = ModuleMock()
forex_mod.forex = forex
forex_mod.available_forex = available_forex

# Import and setup insider trading
from fmpsdk.insider_trading import insider_trading, insider_trading_statistics

insider_mod = ModuleMock()
insider_mod.insider_trading = insider_trading
insider_mod.insider_trading_statistics = insider_trading_statistics

# Import all modules
import fmpsdk.general as general
import fmpsdk.institutional_fund as institutional
import fmpsdk.market_indexes as market_idx
import fmpsdk.mutual_funds as mutual_funds
import fmpsdk.news as news
import fmpsdk.senate as senate
import fmpsdk.shares_float as shares
import fmpsdk.stock_time_series as sts
import fmpsdk.technical_indicators as technical
import fmpsdk.tsx as tsx

API_KEY = os.getenv("FMP_API_KEY")


class TestCrossModuleIntegration:
    """Test interactions between different modules."""

    def test_symbol_search_to_company_data_flow(self):
        """Test flow from symbol search to detailed company data."""
        # 1. Search for a company
        search_result = general.search_symbol(apikey=API_KEY, symbol="AAPL", limit=1)
        assert search_result is not None

        # 2. Get company profile
        profile = cv.company_profile(apikey=API_KEY, symbol="AAPL")
        assert profile is not None

        # 3. Get financial data
        income = cv.income_statement(apikey=API_KEY, symbol="AAPL", limit=1)
        assert income is not None

        # 4. Get stock price data
        quote = sts.quote_short(apikey=API_KEY, symbol="AAPL")
        assert quote is not None

        # 5. Get news for the company
        company_news = news.company_news(apikey=API_KEY, limit=5)
        assert company_news is not None

    def test_market_data_consistency(self):
        """Test consistency across different market data endpoints."""
        symbol = "AAPL"

        # Get data from different endpoints
        quote = sts.quote_short(apikey=API_KEY, symbol=symbol)
        market_cap = cv.market_capitalization(apikey=API_KEY, symbol=symbol)
        profile = cv.company_profile(apikey=API_KEY, symbol=symbol)

        assert quote is not None
        assert market_cap is not None
        assert profile is not None

    def test_calendar_events_integration(self):
        """Test integration between calendar events and company data."""
        # Get earnings calendar
        earnings_cal = calendar.earnings_calendar(apikey=API_KEY, limit=10)
        assert earnings_cal is not None

        # Get dividends calendar
        div_cal = calendar.dividends_calendar(apikey=API_KEY, limit=10)
        assert div_cal is not None

        # Get company dividends for a specific stock
        company_div = calendar.dividends(apikey=API_KEY, symbol="AAPL")
        assert company_div is not None


class TestDataTypesAndFormats:
    """Test that API responses have correct data types and formats."""

    def test_response_model_types(self):
        """Test that all endpoints return proper Pydantic models."""
        test_cases = [
            (general.search_symbol, {"symbol": "AAPL"}),
            (cv.company_profile, {"symbol": "AAPL"}),
            (sts.quote_short, {"symbol": "AAPL"}),
            (news.company_news, {"limit": 1}),
            (calendar.earnings_calendar, {"limit": 5}),
        ]

        for func, kwargs in test_cases:
            kwargs["apikey"] = API_KEY
            result = func(**kwargs)
            assert result is not None, f"{func.__name__} returned None"
            assert hasattr(
                result, "__dict__"
            ), f"{func.__name__} should return a Pydantic model"

    def test_date_parameters(self):
        """Test endpoints that accept date parameters."""
        from_date = "2024-01-01"
        to_date = "2024-01-31"

        # Test historical market cap
        result = cv.historical_market_capitalization(
            apikey=API_KEY, symbol="AAPL", from_date=from_date, to_date=to_date
        )
        assert result is not None

        # Test news with date range
        result = news.company_news(apikey=API_KEY, from_date=from_date, to_date=to_date)
        assert result is not None


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_symbols(self):
        """Test behavior with invalid symbols."""
        # Most endpoints should return empty results or handle gracefully
        invalid_symbols = ["INVALIDXYZ123", "NOTREAL", "FAKESYMBOL"]

        for symbol in invalid_symbols:
            # These should not crash, might return empty results
            result = cv.company_profile(apikey=API_KEY, symbol=symbol)
            # Result might be None or empty, but shouldn't crash

            result = sts.quote_short(apikey=API_KEY, symbol=symbol)
            # Same here - graceful handling expected

    def test_rate_limiting_awareness(self):
        """Test that we can handle potential rate limiting."""
        # Make several quick requests to test rate limiting behavior
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        for symbol in symbols:
            result = sts.quote_short(apikey=API_KEY, symbol=symbol)
            assert result is not None
            # Small delay to be respectful to API
            time.sleep(0.1)


class TestSpecializedEndpoints:
    """Test specialized and less common endpoints."""

    def test_crypto_endpoints(self):
        """Test cryptocurrency-related endpoints."""
        # Get crypto list
        crypto_list = crypto.cryptocurrencies_list(apikey=API_KEY)
        assert crypto_list is not None

        # Get available cryptocurrencies
        available = crypto.available_cryptocurrencies(apikey=API_KEY)
        assert available is not None

    def test_forex_endpoints(self):
        """Test forex-related endpoints."""
        # Get forex list
        forex_list = forex_mod.forex(apikey=API_KEY)
        assert forex_list is not None

        # Get available forex pairs
        available = forex_mod.available_forex(apikey=API_KEY)
        assert available is not None

    def test_commodity_endpoints(self):
        """Test commodity-related endpoints."""
        # Get commodity quotes
        commodity_quotes = commodities.commodities_quote(apikey=API_KEY, symbol="GCUSD")
        assert commodity_quotes is not None

        # Get short commodity quotes
        commodity_short = commodities.commodities_quote_short(
            apikey=API_KEY, symbol="GCUSD"
        )
        assert commodity_short is not None

    def test_etf_endpoints(self):
        """Test ETF-related endpoints."""
        # Get ETF holdings for a popular ETF
        holdings = etf.etf_holdings(apikey=API_KEY, symbol="SPY")
        assert holdings is not None

        # Get ETF info
        info = etf.etf_info(apikey=API_KEY, symbol="SPY")
        assert info is not None

        # Get ETF sector weightings
        sectors = etf.etf_sector_weightings(apikey=API_KEY, symbol="SPY")
        assert sectors is not None

    def test_insider_trading_endpoints(self):
        """Test insider trading endpoints."""
        # Get latest insider trading
        trading = insider_mod.insider_trading(apikey=API_KEY, symbol="AAPL", limit=10)
        assert trading is not None

        # Get insider trading statistics
        stats = insider_mod.insider_trading_statistics(apikey=API_KEY, symbol="AAPL")
        assert stats is not None

    def test_economic_indicators(self):
        """Test economic indicator endpoints."""
        # Get treasury rates
        treasury = economic.treasury_rates(apikey=API_KEY)
        assert treasury is not None

        # Get economic indicators
        indicators = economic.economic_indicators(apikey=API_KEY, name="GDP")
        assert indicators is not None

    def test_international_exchanges(self):
        """Test international exchange endpoints."""
        # Test TSX (Toronto Stock Exchange)
        tsx_list = tsx.tsx_list(apikey=API_KEY)
        assert tsx_list is not None


class TestBulkOperations:
    """Test bulk operations and list endpoints."""

    def test_list_endpoints(self):
        """Test various list endpoints."""
        # Stock lists
        stock_list = general.stock_list(apikey=API_KEY)
        assert stock_list is not None

        # ETF list
        etf_list = general.etf_list(apikey=API_KEY)
        assert etf_list is not None

        # Exchange list
        exchanges = general.available_exchanges(apikey=API_KEY)
        assert exchanges is not None

    def test_sector_and_industry_data(self):
        """Test sector and industry related endpoints."""
        # Available sectors
        sectors = general.available_sectors(apikey=API_KEY)
        assert sectors is not None

        # Available industries
        industries = general.available_industries(apikey=API_KEY)
        assert industries is not None

        # Available countries
        countries = general.available_countries(apikey=API_KEY)
        assert countries is not None


class TestAdvancedFeatures:
    """Test advanced features and complex scenarios."""

    def test_pagination_across_endpoints(self):
        """Test pagination functionality across different endpoints."""
        # Test news pagination
        page_0 = news.company_news(apikey=API_KEY, page=0, limit=5)
        page_1 = news.company_news(apikey=API_KEY, page=1, limit=5)

        assert page_0 is not None
        assert page_1 is not None

    def test_limit_parameters(self):
        """Test limit parameters across endpoints."""
        limits_to_test = [1, 5, 10, 20, 50]

        for limit in limits_to_test:
            result = calendar.earnings_calendar(apikey=API_KEY, limit=limit)
            assert result is not None

            result = news.company_news(apikey=API_KEY, limit=limit)
            assert result is not None

    def test_multiple_symbols_processing(self):
        """Test endpoints that can handle multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

        # Test press releases with multiple symbols (company_news doesn't accept symbols parameter)
        result = news.company_press_releases(apikey=API_KEY, symbols=symbols, limit=10)
        assert result is not None

        # Test with comma-separated string
        result = news.company_press_releases(
            apikey=API_KEY, symbols="AAPL,MSFT,GOOGL", limit=10
        )
        assert result is not None

    def test_news_endpoints_with_dates(self):
        """Test new news endpoints with date parameters."""
        from_date = "2024-01-01"
        to_date = "2024-01-31"  # Test general news
        result = news.news_general(
            apikey=API_KEY, from_date=from_date, to_date=to_date, limit=5
        )
        assert result is not None

        # Test crypto news
        result = news.news_crypto(
            apikey=API_KEY, from_date=from_date, to_date=to_date, limit=5
        )
        assert result is not None

        # Test forex news
        result = news.news_forex(
            apikey=API_KEY, from_date=from_date, to_date=to_date, limit=5
        )
        assert result is not None

    def test_news_pagination_new_functions(self):
        """Test pagination with new news functions."""
        # Test general news pagination
        page_0 = news.news_general(apikey=API_KEY, page=0, limit=5)
        page_1 = news.news_general(apikey=API_KEY, page=1, limit=5)

        assert page_0 is not None
        assert page_1 is not None
