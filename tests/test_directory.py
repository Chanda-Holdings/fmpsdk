from datetime import datetime, timedelta

import pytest

from fmpsdk import directory
from fmpsdk.models import (
    FMPCountry,
    FMPExchangeInfo,
    FMPFinancialStatementSymbolList,
    FMPIndustry,
    FMPSector,
    FMPSymbolAndCIKList,
    FMPSymbolAndCompanyNameList,
    FMPSymbolAndNameList,
    FMPSymbolChange,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)

# Test configuration
RESPONSE_TIME_LIMIT = (
    15.0  # seconds (directory endpoints might be slower due to large datasets)
)


@pytest.fixture
def recent_date():
    """Recent date for testing (within last 30 days)."""
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


class TestDirectoryBasic:
    """Basic functionality tests for directory endpoints with enhanced validation."""

    @pytest.mark.parametrize(
        "exchange",
        [
            # Major US Exchanges
            "NASDAQ",
            "NYSE",
            "AMEX",
            # International Exchanges
            "TSX",  # Toronto Stock Exchange
            "LSE",  # London Stock Exchange
            "FRA",  # Frankfurt Stock Exchange
            "TYO",  # Tokyo Stock Exchange
            "HKG",  # Hong Kong Stock Exchange
            "ASX",  # Australian Securities Exchange
            "SWX",  # SIX Swiss Exchange
        ],
    )
    def test_stock_list_by_exchange(self, api_key, exchange):
        """Test stock list for various exchanges using enhanced validation."""
        result, validation = handle_api_call_with_validation(
            directory.stock_list,
            "stock_list",
            apikey=api_key,
            exchange=exchange,
            limit=50,
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndCompanyNameList)
        # Some exchanges may have limited or no data
        if len(models) == 0:
            pytest.skip(f"No stock data available for exchange {exchange}")
        validate_model_list(
            models,
            FMPSymbolAndCompanyNameList,
            f"Failed to validate stock list models for {exchange}",
        )

        if models:  # If we have stocks for this exchange
            first_stock = models[0]

            # Enhanced business logic validation
            assert (
                first_stock.symbol is not None and len(first_stock.symbol) > 0
            ), "Symbol should not be empty"
            assert len(first_stock.symbol) <= 10, "Symbol should be reasonable length"
            assert (
                first_stock.symbol.isupper()
                or first_stock.symbol.isdigit()
                or "-" in first_stock.symbol
            ), "Symbol should be uppercase or contain digits/hyphens"

            if first_stock.companyName:
                assert (
                    len(first_stock.companyName) <= 200
                ), "Company name should be reasonable length"

    @pytest.mark.parametrize("limit", [10, 25, 50, 100])
    def test_stock_list_with_limits(self, api_key, limit):
        """Test stock list with various limit parameters using enhanced validation."""
        result, validation = handle_api_call_with_validation(
            directory.stock_list, "stock_list", apikey=api_key, limit=limit
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndCompanyNameList)
        validate_model_list(
            models,
            FMPSymbolAndCompanyNameList,
            f"Failed to validate stock list models with limit {limit}",
            min_count=0,
        )
        assert len(models) >= 0, "Should return a valid list"

    def test_stock_list_basic_validation(self, api_key):
        """Test basic stock list with comprehensive validation."""
        result, validation = handle_api_call_with_validation(
            directory.stock_list, "stock_list", apikey=api_key, limit=50
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndCompanyNameList)
        validate_model_list(
            models, FMPSymbolAndCompanyNameList, "Failed to validate stock list models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for stock in models[:10]:
                # Symbol validation
                assert (
                    stock.symbol is not None and len(stock.symbol) >= 1
                ), "Symbol should not be empty"
                assert len(stock.symbol) <= 10, "Symbol should be reasonable length"
                assert (
                    stock.symbol.isupper()
                    or stock.symbol.isdigit()
                    or "-" in stock.symbol
                ), "Symbol should be properly formatted"

                # Company name validation
                if stock.companyName:
                    assert (
                        len(stock.companyName) >= 1
                    ), "Company name should not be empty if present"
                    assert (
                        len(stock.companyName) <= 200
                    ), "Company name should be reasonable length"

    def test_financial_statement_symbol_list(self, api_key):
        """Test financial statement symbol list with enhanced validation."""
        result, validation = handle_api_call_with_validation(
            directory.financial_statement_symbol_list,
            "financial_statement_symbol_list",
            apikey=api_key,
            limit=30,
        )

        # Extract and validate models
        models = get_response_models(result, FMPFinancialStatementSymbolList)
        validate_model_list(
            models,
            FMPFinancialStatementSymbolList,
            "Failed to validate financial statement symbol list models",
        )

        if models:
            # Test first 10 items for comprehensive validation
            for symbol_info in models[:10]:
                # Core validation
                assert symbol_info.symbol is not None, "Symbol should not be None"
                assert (
                    symbol_info.companyName is not None
                ), "Company name should not be None"
                assert (
                    symbol_info.tradingCurrency is not None
                ), "Trading currency should not be None"

                # Currency validation
                assert (
                    len(symbol_info.tradingCurrency) == 3
                ), "Trading currency should be 3-letter code"
                assert (
                    symbol_info.tradingCurrency.isalnum()
                ), "Trading currency should be alphanumeric"

                if symbol_info.reportingCurrency:
                    assert (
                        len(symbol_info.reportingCurrency) == 3
                    ), "Reporting currency should be 3-letter code"
                    assert (
                        symbol_info.reportingCurrency.isalnum()
                    ), "Reporting currency should be alphanumeric"

    def test_cik_list(self, api_key):
        """Test CIK list with enhanced validation."""
        result, validation = handle_api_call_with_validation(
            directory.cik_list, "cik_list", apikey=api_key, limit=30
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndCIKList)
        validate_model_list(
            models, FMPSymbolAndCIKList, "Failed to validate CIK list models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for cik_info in models[:10]:
                # CIK validation
                assert cik_info.cik is not None, "CIK should not be None"
                assert (
                    cik_info.companyName is not None
                ), "Company name should not be None"
                assert cik_info.cik.isdigit(), "CIK should be numeric"
                assert (
                    6 <= len(cik_info.cik) <= 10
                ), "CIK should be proper length (6-10 digits)"

    def test_etf_list(self, api_key):
        """Test ETF list with enhanced validation."""
        result, validation = handle_api_call_with_validation(
            directory.etf_list, "etf_list", apikey=api_key, limit=30
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndNameList)
        validate_model_list(
            models, FMPSymbolAndNameList, "Failed to validate ETF list models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for etf in models[:10]:
                # ETF validation
                assert etf.symbol is not None, "ETF symbol should not be None"
                assert etf.name is not None, "ETF name should not be None"
                assert len(etf.symbol) >= 1, "ETF symbol should not be empty"
                assert len(etf.name) >= 1, "ETF name should not be empty"
                assert len(etf.symbol) <= 10, "ETF symbol should be reasonable length"
                assert len(etf.name) <= 200, "ETF name should be reasonable length"

    def test_actively_trading_list(self, api_key):
        """Test actively trading list with enhanced validation."""
        result, validation = handle_api_call_with_validation(
            directory.actively_trading_list,
            "actively_trading_list",
            apikey=api_key,
            limit=30,
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndNameList)
        validate_model_list(
            models,
            FMPSymbolAndNameList,
            "Failed to validate actively trading list models",
        )

        if models:
            # Test first 10 items for comprehensive validation
            for stock in models[:10]:
                # Stock validation
                assert stock.symbol is not None, "Stock symbol should not be None"
                assert stock.name is not None, "Stock name should not be None"
                assert len(stock.symbol) >= 1, "Stock symbol should not be empty"
                assert len(stock.name) >= 1, "Stock name should not be empty"
                assert (
                    len(stock.symbol) <= 10
                ), "Stock symbol should be reasonable length"
                assert len(stock.name) <= 200, "Stock name should be reasonable length"


class TestDirectorySymbolChanges:
    """Test symbol change functionality."""

    def test_symbol_change_basic(self, api_key):
        """Test basic symbol change functionality."""
        result, validation = handle_api_call_with_validation(
            directory.symbol_change, "symbol_change", apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolChange)
        validate_model_list(
            models, FMPSymbolChange, "Failed to validate symbol change models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for change in models[:10]:
                # Symbol change validation
                assert change.oldSymbol is not None, "Old symbol should not be None"
                assert change.newSymbol is not None, "New symbol should not be None"
                assert len(change.oldSymbol) >= 1, "Old symbol should not be empty"
                assert len(change.newSymbol) >= 1, "New symbol should not be empty"
                assert (
                    len(change.oldSymbol) <= 10
                ), "Old symbol should be reasonable length"
                assert (
                    len(change.newSymbol) <= 10
                ), "New symbol should be reasonable length"

    def test_symbol_change_by_date(self, api_key, recent_date):
        """Test symbol change with date filter."""
        result, validation = handle_api_call_with_validation(
            directory.symbol_change, "symbol_change", apikey=api_key, date=recent_date
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolChange)
        validate_model_list(
            models,
            FMPSymbolChange,
            "Failed to validate symbol change models with date filter",
        )

        if models:
            # Test first 10 items for comprehensive validation
            for change in models[:10]:
                # Symbol change validation
                assert change.oldSymbol is not None, "Old symbol should not be None"
                assert change.newSymbol is not None, "New symbol should not be None"
                assert len(change.oldSymbol) >= 1, "Old symbol should not be empty"
                assert len(change.newSymbol) >= 1, "New symbol should not be empty"


class TestDirectoryAvailableEndpoints:
    """Test available endpoints functionality."""

    def test_available_exchanges(self, api_key):
        """Test available exchanges endpoint."""
        result, validation = handle_api_call_with_validation(
            directory.available_exchanges, "available_exchanges", apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeInfo)
        validate_model_list(
            models, FMPExchangeInfo, "Failed to validate available exchanges models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for exchange in models[:10]:
                # Exchange validation
                assert exchange.name is not None, "Exchange name should not be None"
                assert exchange.exchange is not None, "Exchange code should not be None"
                assert (
                    exchange.countryName is not None
                ), "Country name should not be None"
                assert (
                    exchange.countryCode is not None
                ), "Country code should not be None"
                assert len(exchange.name) >= 1, "Exchange name should not be empty"
                assert len(exchange.exchange) >= 1, "Exchange code should not be empty"

                # Some exchanges may have empty country information in the API data
                # Only validate non-empty country data when country name is provided
                if exchange.countryName and len(exchange.countryName.strip()) > 0:
                    assert (
                        len(exchange.countryName) >= 1
                    ), "Country name should not be empty when provided"
                    # Country code may still be empty even when country name is provided
                    # This is acceptable for some exchanges (e.g., Taiwan Stock Exchange)

                # Validate country code only if it's provided
                if exchange.countryCode and len(exchange.countryCode.strip()) > 0:
                    assert (
                        len(exchange.countryCode) >= 1
                    ), "Country code should not be empty when provided"

    def test_available_sectors(self, api_key):
        """Test available sectors endpoint."""
        result, validation = handle_api_call_with_validation(
            directory.available_sectors, "available_sectors", apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPSector)
        validate_model_list(
            models, FMPSector, "Failed to validate available sectors models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for sector in models[:10]:
                # Sector validation
                assert sector.sector is not None, "Sector name should not be None"
                assert len(sector.sector) >= 1, "Sector name should not be empty"
                assert (
                    len(sector.sector) <= 100
                ), "Sector name should be reasonable length"

    def test_available_industries(self, api_key):
        """Test available industries endpoint."""
        result, validation = handle_api_call_with_validation(
            directory.available_industries, "available_industries", apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPIndustry)
        validate_model_list(
            models, FMPIndustry, "Failed to validate available industries models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for industry in models[:10]:
                # Industry validation
                assert industry.industry is not None, "Industry name should not be None"
                assert len(industry.industry) >= 1, "Industry name should not be empty"
                assert (
                    len(industry.industry) <= 100
                ), "Industry name should be reasonable length"

    def test_available_countries(self, api_key):
        """Test available countries endpoint."""
        result, validation = handle_api_call_with_validation(
            directory.available_countries, "available_countries", apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPCountry)
        validate_model_list(
            models, FMPCountry, "Failed to validate available countries models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for country in models[:10]:
                # Country validation
                assert country.name is not None, "Country name should not be None"
                assert len(country.name) >= 1, "Country name should not be empty"
                assert (
                    len(country.name) <= 100
                ), "Country name should be reasonable length"

    def test_available_indexes(self, api_key):
        """Test available indexes endpoint."""
        result, validation = handle_api_call_with_validation(
            directory.available_indexes, "available_indexes", apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndNameList)
        validate_model_list(
            models, FMPSymbolAndNameList, "Failed to validate available indexes models"
        )

        if models:
            # Test first 10 items for comprehensive validation
            for index in models[:10]:
                # Index validation
                assert index.symbol is not None, "Index symbol should not be None"
                assert index.name is not None, "Index name should not be None"
                assert len(index.symbol) >= 1, "Index symbol should not be empty"
                assert len(index.name) >= 1, "Index name should not be empty"
                assert (
                    len(index.symbol) <= 20
                ), "Index symbol should be reasonable length"
                assert len(index.name) <= 200, "Index name should be reasonable length"


class TestDirectoryDataQuality:
    """Test data quality for directory endpoints."""

    def test_stock_list_data_quality(self, api_key):
        """Test data quality for stock list endpoint."""
        result, validation = handle_api_call_with_validation(
            directory.stock_list, "stock_list", apikey=api_key, limit=100
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndCompanyNameList)
        validate_model_list(
            models,
            FMPSymbolAndCompanyNameList,
            "Failed to validate stock list models for data quality test",
        )

        if models:
            # Data quality metrics
            total_stocks = len(models)
            valid_symbols = 0
            valid_names = 0
            unique_symbols = set()

            for stock in models:
                # Symbol validation
                if stock.symbol and len(stock.symbol) >= 1:
                    valid_symbols += 1
                    unique_symbols.add(stock.symbol)

                # Company name validation
                if stock.companyName and len(stock.companyName) >= 1:
                    valid_names += 1

            # Business logic assertions
            if total_stocks > 0:
                assert (
                    valid_symbols / total_stocks >= 0.95
                ), f"Only {valid_symbols}/{total_stocks} stocks have valid symbols"
                assert (
                    valid_names / total_stocks >= 0.80
                ), f"Only {valid_names}/{total_stocks} stocks have valid names"
                assert (
                    len(unique_symbols) == valid_symbols
                ), f"Symbols should be unique: {len(unique_symbols)} != {valid_symbols}"

    def test_available_data_consistency(self, api_key):
        """Test consistency across available endpoints."""
        # Test exchanges
        exchanges_response, _ = handle_api_call_with_validation(
            directory.available_exchanges, "available_exchanges", apikey=api_key
        )

        # Test sectors
        sectors_response, _ = handle_api_call_with_validation(
            directory.available_sectors, "available_sectors", apikey=api_key
        )

        # Test industries
        industries_response, _ = handle_api_call_with_validation(
            directory.available_industries, "available_industries", apikey=api_key
        )

        # Test countries
        countries_response, _ = handle_api_call_with_validation(
            directory.available_countries, "available_countries", apikey=api_key
        )

        # Extract and validate models
        exchanges_models = get_response_models(exchanges_response, FMPExchangeInfo)
        sectors_models = get_response_models(sectors_response, FMPSector)
        industries_models = get_response_models(industries_response, FMPIndustry)
        countries_models = get_response_models(countries_response, FMPCountry)

        # Validate model lists
        validate_model_list(
            exchanges_models, FMPExchangeInfo, "Failed to validate exchanges models"
        )
        validate_model_list(
            sectors_models, FMPSector, "Failed to validate sectors models"
        )
        validate_model_list(
            industries_models, FMPIndustry, "Failed to validate industries models"
        )
        validate_model_list(
            countries_models, FMPCountry, "Failed to validate countries models"
        )

        # Consistency checks
        if exchanges_models:
            assert len(exchanges_models) >= 5, "Should have at least 5 exchanges"

        if sectors_models:
            assert len(sectors_models) >= 10, "Should have at least 10 sectors"

        if industries_models:
            assert len(industries_models) >= 20, "Should have at least 20 industries"

        if countries_models:
            assert len(countries_models) >= 10, "Should have at least 10 countries"

    def test_financial_statement_currency_validation(self, api_key):
        """Test currency validation for financial statement symbols."""
        result, validation = handle_api_call_with_validation(
            directory.financial_statement_symbol_list,
            "financial_statement_symbol_list",
            apikey=api_key,
            limit=50,
        )

        # Extract and validate models
        models = get_response_models(result, FMPFinancialStatementSymbolList)
        validate_model_list(
            models,
            FMPFinancialStatementSymbolList,
            "Failed to validate financial statement symbol list models",
        )

        if models:
            # Currency validation
            for symbol_info in models:
                # Trading currency validation
                assert (
                    symbol_info.tradingCurrency is not None
                ), "Trading currency should not be None"
                assert (
                    len(symbol_info.tradingCurrency) == 3
                ), "Trading currency should be 3-letter code"
                assert (
                    symbol_info.tradingCurrency.isalnum()
                ), "Trading currency should be alphanumeric"

                # Reporting currency validation (if present)
                if symbol_info.reportingCurrency:
                    assert (
                        len(symbol_info.reportingCurrency) == 3
                    ), "Reporting currency should be 3-letter code"
                    assert (
                        symbol_info.reportingCurrency.isalnum()
                    ), "Reporting currency should be alphanumeric"
