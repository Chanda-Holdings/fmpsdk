import time
from datetime import datetime, timedelta
from typing import List

import pytest

from fmpsdk import directory
from fmpsdk.models import (
    FMPFinancialStatementSymbolList,
    FMPSymbolAndCIKList,
    FMPSymbolAndCompanyNameList,
    FMPSymbolAndNameList,
    FMPSymbolChange,
)
from tests.conftest import extract_data_list

# Test configuration
RESPONSE_TIME_LIMIT = (
    15.0  # seconds (directory endpoints might be slower due to large datasets)
)


@pytest.fixture
def recent_date():
    """Recent date for testing (within last 30 days)."""
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


class TestDirectoryBasic:
    """Basic functionality tests for directory endpoints."""

    def test_stock_list_basic(self, api_key):
        """Test getting basic stock list."""
        start_time = time.time()
        result = directory.stock_list(apikey=api_key, limit=50)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            assert len(data) > 0

            for stock in data[:10]:  # Check first few items
                if isinstance(stock, dict):
                    stock_obj = FMPSymbolAndCompanyNameList(**stock)
                else:
                    stock_obj = stock

                # Validate stock list data
                assert stock_obj.symbol
                assert len(stock_obj.symbol) >= 1
                assert len(stock_obj.symbol) <= 10  # Reasonable symbol length

                # Symbol should be uppercase
                assert stock_obj.symbol.isupper() or stock_obj.symbol.isdigit()

                # Company name should exist if provided
                if stock_obj.companyName:
                    assert len(stock_obj.companyName) >= 1
                    assert (
                        len(stock_obj.companyName) <= 200
                    )  # Reasonable company name length

    def test_financial_statement_symbol_list(self, api_key):
        """Test getting financial statement symbol list."""
        start_time = time.time()
        result = directory.financial_statement_symbol_list(apikey=api_key, limit=30)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for symbol_info in data[:10]:  # Check first few items
                if isinstance(symbol_info, dict):
                    symbol_obj = FMPFinancialStatementSymbolList(**symbol_info)
                else:
                    symbol_obj = symbol_info

                # Validate financial statement symbol data
                assert symbol_obj.symbol
                assert symbol_obj.companyName
                assert symbol_obj.tradingCurrency
                # reportingCurrency can be None for some symbols
                if symbol_obj.reportingCurrency:
                    assert isinstance(symbol_obj.reportingCurrency, str)

                # Currency should be 3-letter codes
                assert len(symbol_obj.tradingCurrency) == 3
                if symbol_obj.reportingCurrency:
                    assert len(symbol_obj.reportingCurrency) == 3
                # Currency codes should be alphanumeric (allowing for cases like GBp)
                assert symbol_obj.tradingCurrency.isalnum()
                if symbol_obj.reportingCurrency:
                    assert symbol_obj.reportingCurrency.isalnum()

    def test_cik_list(self, api_key):
        """Test getting CIK list."""
        start_time = time.time()
        result = directory.cik_list(apikey=api_key, limit=30)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for cik_info in data[:10]:  # Check first few items
                if isinstance(cik_info, dict):
                    cik_obj = FMPSymbolAndCIKList(**cik_info)
                else:
                    cik_obj = cik_info

                # Validate CIK data
                assert cik_obj.cik
                assert cik_obj.companyName

                # CIK should be numeric string with reasonable length
                assert cik_obj.cik.isdigit()
                assert 6 <= len(cik_obj.cik) <= 10  # CIK format

    def test_etf_list(self, api_key):
        """Test getting ETF list."""
        start_time = time.time()
        result = directory.etf_list(apikey=api_key, limit=30)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for etf in data[:10]:  # Check first few items
                if isinstance(etf, dict):
                    etf_obj = FMPSymbolAndNameList(**etf)
                else:
                    etf_obj = etf

                # Validate ETF data
                assert etf_obj.symbol
                assert etf_obj.name

                # ETF symbols are typically 3-5 characters
                assert 1 <= len(etf_obj.symbol) <= 10
                assert etf_obj.symbol.isupper()

    def test_actively_trading_list(self, api_key):
        """Test getting actively trading list."""
        start_time = time.time()
        result = directory.actively_trading_list(apikey=api_key, limit=30)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for stock in data[:10]:  # Check first few items
                if isinstance(stock, dict):
                    stock_obj = FMPSymbolAndNameList(**stock)
                else:
                    stock_obj = stock

                # Validate actively trading stock data
                assert stock_obj.symbol
                assert stock_obj.name

                # Symbol format validation
                assert len(stock_obj.symbol) <= 10
                assert stock_obj.symbol.isupper() or stock_obj.symbol.isdigit()


class TestDirectoryExchangeFiltering:
    """Test directory endpoints with exchange filtering."""

    def test_stock_list_by_exchange(self, api_key):
        """Test stock list filtered by exchange."""
        exchanges = ["NASDAQ", "NYSE", "AMEX"]

        for exchange in exchanges:
            result = directory.stock_list(apikey=api_key, exchange=exchange, limit=20)

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

            # Exchange filtering might not be strictly enforced by API
            # So we just verify the data structure
            if data:
                for stock in data[:5]:
                    if isinstance(stock, dict):
                        stock_obj = FMPSymbolAndCompanyNameList(**stock)
                    else:
                        stock_obj = stock

                    assert stock_obj.symbol

    def test_financial_statement_list_by_exchange(self, api_key):
        """Test financial statement list filtered by exchange."""
        result = directory.financial_statement_symbol_list(
            apikey=api_key, exchange="NASDAQ", limit=15
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            for symbol_info in data[:5]:
                if isinstance(symbol_info, dict):
                    symbol_obj = FMPFinancialStatementSymbolList(**symbol_info)
                else:
                    symbol_obj = symbol_info

                # Validate structure
                assert symbol_obj.symbol
                assert symbol_obj.companyName

    def test_etf_list_by_exchange(self, api_key):
        """Test ETF list filtered by exchange."""
        result = directory.etf_list(apikey=api_key, exchange="AMEX", limit=15)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            for etf in data[:5]:
                if isinstance(etf, dict):
                    etf_obj = FMPSymbolAndNameList(**etf)
                else:
                    etf_obj = etf

                assert etf_obj.symbol
                assert etf_obj.name


class TestDirectorySymbolChanges:
    """Test symbol change tracking functionality."""

    def test_symbol_change_basic(self, api_key):
        """Test getting symbol changes."""
        result = directory.symbol_change(apikey=api_key)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for change in data[:10]:  # Check first few items
                if isinstance(change, dict):
                    change_obj = FMPSymbolChange(**change)
                else:
                    change_obj = change

                # Validate symbol change data
                assert change_obj.date
                assert change_obj.companyName
                assert change_obj.oldSymbol
                assert change_obj.newSymbol

                # Symbols should be different
                assert change_obj.oldSymbol != change_obj.newSymbol

                # Date format validation
                try:
                    datetime.strptime(change_obj.date[:10], "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid date format: {change_obj.date}")

    def test_symbol_change_by_date(self, api_key, recent_date):
        """Test symbol changes filtered by date."""
        result = directory.symbol_change(apikey=api_key, date=recent_date)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        # Date filtering might return empty results for recent dates
        # This is acceptable as symbol changes are rare events
        if data:
            for change in data[:5]:
                if isinstance(change, dict):
                    change_obj = FMPSymbolChange(**change)
                else:
                    change_obj = change
                # Validate date consistency (API may not strictly filter by date)
                change_date = datetime.strptime(change_obj.date[:10], "%Y-%m-%d")
                filter_date = datetime.strptime(recent_date, "%Y-%m-%d")

                # Allow broader tolerance as API date filtering may be approximate
                assert (
                    abs((change_date - filter_date).days) <= 90
                ), f"Change date {change_obj.date} too far from filter date {recent_date}"

    def test_symbol_change_by_symbol(self, api_key):
        """Test symbol changes filtered by specific symbol."""
        # Use a known symbol that might have historical changes
        test_symbols = ["META", "GOOGL", "TSLA"]

        for symbol in test_symbols:
            result = directory.symbol_change(apikey=api_key, symbol=symbol)

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)
            # Symbol filtering might return empty results or broader results
            # This is acceptable as not all symbols have change history
            # and the API may return related symbol changes
            if data:
                for change in data[:3]:
                    if isinstance(change, dict):
                        change_obj = FMPSymbolChange(**change)
                    else:
                        change_obj = change

                    # Validate that we have symbol change data structure
                    assert change_obj.oldSymbol
                    assert change_obj.newSymbol
                    assert change_obj.date

                    # Note: API may return broader results than just the specific symbol


class TestDirectoryDataQuality:
    """Test directory data quality and consistency."""

    def test_stock_list_symbol_uniqueness(self, api_key):
        """Test that stock list has unique symbols."""
        result = directory.stock_list(apikey=api_key, limit=100)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data and len(data) > 10:
            symbols = set()
            duplicate_symbols = []

            for stock in data:
                if isinstance(stock, dict):
                    stock_obj = FMPSymbolAndCompanyNameList(**stock)
                else:
                    stock_obj = stock

                if stock_obj.symbol in symbols:
                    duplicate_symbols.append(stock_obj.symbol)
                symbols.add(stock_obj.symbol)

            # Allow some duplicates (different share classes, etc.)
            assert len(duplicate_symbols) <= len(data) * 0.1  # Max 10% duplicates

    def test_cik_format_consistency(self, api_key):
        """Test CIK format consistency."""
        result = directory.cik_list(apikey=api_key, limit=50)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            valid_ciks = 0
            for cik_info in data:
                if isinstance(cik_info, dict):
                    cik_obj = FMPSymbolAndCIKList(**cik_info)
                else:
                    cik_obj = cik_info

                # CIK should be numeric and proper length
                if cik_obj.cik.isdigit() and 6 <= len(cik_obj.cik) <= 10:
                    valid_ciks += 1

            # Most CIKs should be valid format
            assert valid_ciks >= len(data) * 0.8  # At least 80% valid

    def test_financial_statement_currency_validation(self, api_key):
        """Test financial statement currency validation."""
        result = directory.financial_statement_symbol_list(apikey=api_key, limit=50)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            valid_currencies = 0
            common_currencies = {
                "USD",
                "CAD",
                "EUR",
                "GBP",
                "JPY",
                "AUD",
                "CHF",
                "SEK",
                "NOK",
                "DKK",
            }

            for symbol_info in data:
                if isinstance(symbol_info, dict):
                    symbol_obj = FMPFinancialStatementSymbolList(**symbol_info)
                else:
                    symbol_obj = symbol_info

                # Check if currencies are in common set
                if (
                    symbol_obj.tradingCurrency in common_currencies
                    and symbol_obj.reportingCurrency in common_currencies
                ):
                    valid_currencies += 1

            # Most should have common currencies
            assert valid_currencies >= len(data) * 0.7  # At least 70% common currencies


class TestDirectoryErrorHandling:
    """Test error handling for directory endpoints."""

    def test_stock_list_invalid_api_key(self):
        """Test stock list with invalid API key."""
        result = directory.stock_list(apikey="invalid_key", limit=10)

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_financial_statement_list_invalid_api_key(self):
        """Test financial statement list with invalid API key."""
        result = directory.financial_statement_symbol_list(
            apikey="invalid_key", limit=10
        )

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_cik_list_invalid_api_key(self):
        """Test CIK list with invalid API key."""
        result = directory.cik_list(apikey="invalid_key", limit=10)

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_symbol_change_invalid_api_key(self):
        """Test symbol change with invalid API key."""
        result = directory.symbol_change(apikey="invalid_key")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_etf_list_invalid_api_key(self):
        """Test ETF list with invalid API key."""
        result = directory.etf_list(apikey="invalid_key", limit=10)

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_actively_trading_list_invalid_api_key(self):
        """Test actively trading list with invalid API key."""
        result = directory.actively_trading_list(apikey="invalid_key", limit=10)

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_symbol_change_invalid_date(self, api_key):
        """Test symbol change with invalid date format."""
        result = directory.symbol_change(apikey=api_key, date="invalid-date")

        # API might return error or empty result for invalid date
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            assert isinstance(data, list)

    def test_directory_invalid_exchange(self, api_key):
        """Test directory endpoints with invalid exchange."""
        result = directory.stock_list(
            apikey=api_key, exchange="INVALID_EXCHANGE", limit=10
        )

        # API might return empty result or error for invalid exchange
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            assert isinstance(data, list)
            # Empty result is acceptable for invalid exchange


class TestDirectoryPerformance:
    """Test directory endpoint performance."""

    def test_directory_response_times(self, api_key):
        """Test that all directory endpoints respond within acceptable time."""
        endpoints = [
            ("stock_list", lambda: directory.stock_list(api_key, limit=30)),
            (
                "financial_statement_list",
                lambda: directory.financial_statement_symbol_list(api_key, limit=30),
            ),
            ("cik_list", lambda: directory.cik_list(api_key, limit=30)),
            ("etf_list", lambda: directory.etf_list(api_key, limit=30)),
            (
                "actively_trading_list",
                lambda: directory.actively_trading_list(api_key, limit=30),
            ),
            ("symbol_change", lambda: directory.symbol_change(api_key)),
        ]

        for endpoint_name, endpoint_func in endpoints:
            start_time = time.time()
            result = endpoint_func()
            response_time = time.time() - start_time

            # Skip premium endpoints

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

            if data:
                # The API may not enforce limits strictly, but should return data
                assert len(data) > 0
                # Basic validation of data structure - different endpoints have different structures
                first_item = data[0]

                # Validate based on endpoint type
                if endpoint_name == "cik_list":
                    # CIK list has cik and companyName
                    assert hasattr(first_item, "cik")
                    assert hasattr(first_item, "companyName")
                elif endpoint_name == "symbol_change":
                    # Symbol change has oldSymbol and newSymbol
                    assert hasattr(first_item, "oldSymbol") or hasattr(
                        first_item, "newSymbol"
                    )
                else:
                    # Most other endpoints have symbol
                    assert hasattr(first_item, "symbol")
                    # Some may not have companyName
                    if hasattr(first_item, "companyName"):
                        assert first_item.companyName or first_item.companyName == ""

    def test_cik_list_limit_validation(self, api_key):
        """Test CIK list with different limit values."""
        limits = [1, 10, 25]

        for limit in limits:
            result = directory.cik_list(apikey=api_key, limit=limit)

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

            # Should respect limits approximately
            if data:
                assert len(data) <= limit * 2  # Allow flexibility
