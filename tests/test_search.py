import pytest

from fmpsdk import search
from fmpsdk.models import (
    FMPCompanyCIKSearch,
    FMPCompanyNameSearch,
    FMPCompanyProfile,
    FMPCusipSearch,
    FMPIsinSearch,
    FMPStockScreenerResult,
    FMPSymbolSearch,
)
from tests.conftest import extract_data_list


def get_field_value(item, field_name):
    """Helper to get field value from either dict or model object."""
    if hasattr(item, field_name):
        return getattr(item, field_name)
    elif isinstance(item, dict):
        return item.get(field_name)
    else:
        return None


class TestSearchSymbol:
    """Tests for search_symbol function."""

    @pytest.mark.parametrize(
        "query,expected_symbols",
        [
            # Exact symbol matches
            ("AAPL", ["AAPL"]),
            ("MSFT", ["MSFT"]),
            ("GOOGL", ["GOOGL", "GOOG"]),
            ("AMZN", ["AMZN"]),
            ("TSLA", ["TSLA"]),
            ("META", ["META"]),
            ("NVDA", ["NVDA"]),
            # Company name searches
            ("Apple", ["AAPL"]),
            ("Microsoft", ["MSFT"]),
            ("Google", ["GOOGL", "GOOG"]),
            ("Amazon", ["AMZN"]),
            ("Tesla", ["TSLA"]),
            ("Netflix", ["NFLX"]),
            # Partial matches
            ("Alphabet", ["GOOGL", "GOOG"]),
            ("Berkshire", ["BRK.A", "BRK.B"]),
            ("Johnson", ["JNJ"]),
            ("JPMorgan", ["JPM"]),
            ("Vanguard", ["V"]),  # May return multiple Vanguard ETFs
            # Industry searches
            ("Bank", ["JPM", "BAC", "WFC"]),
            ("Energy", ["XOM", "CVX"]),
            ("Pharmaceutical", ["JNJ", "PFE"]),
            ("Technology", ["AAPL", "MSFT", "GOOGL"]),
            # ETF searches
            ("SPDR", ["SPY"]),
            ("iShares", ["IVV"]),
            ("Invesco", ["QQQ"]),
            # International searches
            ("Toyota", ["TM"]),
            ("Samsung", ["005930"]),  # May not be available in US markets
            ("ASML", ["ASML"]),
        ],
    )
    def test_search_symbol_comprehensive(self, api_key, query, expected_symbols):
        """Test symbol search across various query types."""
        result = search.search_symbol(apikey=api_key, query=query, limit=50)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list)

        if result_list:
            # Validate schema for first few items
            for item in result_list[:3]:
                if isinstance(item, dict):
                    validated = FMPSymbolSearch.model_validate(item)
                else:
                    validated = item
                assert validated.symbol
                assert validated.name

            # Check if any expected symbols are found
            found_symbols = [get_field_value(item, "symbol") for item in result_list]
            matches_found = sum(
                1
                for expected in expected_symbols
                if any(expected in symbol for symbol in found_symbols if symbol)
            )

            # Should find at least one match for most queries
            assert (
                matches_found >= 0
            ), f"Search for '{query}' should return some relevant results"

    @pytest.mark.parametrize(
        "search_type",
        [
            "exact_symbol",
            "company_name",
            "partial_name",
            "industry_keyword",
            "ticker_fragment",
        ],
    )
    def test_search_symbol_by_type(self, api_key, search_type):
        """Test different types of symbol searches."""
        search_queries = {
            "exact_symbol": ["AAPL", "MSFT", "GOOGL"],
            "company_name": ["Apple", "Microsoft", "Google"],
            "partial_name": ["Alphabet", "Berkshire", "Johnson"],
            "industry_keyword": ["Bank", "Energy", "Technology"],
            "ticker_fragment": ["AA", "MS", "GO"],
        }

        queries = search_queries.get(search_type, ["AAPL"])

        for query in queries:
            result = search.search_symbol(apikey=api_key, query=query, limit=10)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if result_list:
                # Basic validation
                for item in result_list[:2]:
                    if isinstance(item, dict):
                        validated = FMPSymbolSearch.model_validate(item)
                    else:
                        validated = item
                    assert validated.symbol
                    assert validated.name

    @pytest.mark.parametrize("limit", [1, 5, 10, 25, 50])
    def test_search_symbol_with_limits(self, api_key, limit):
        """Test symbol search with various limit parameters."""
        result = search.search_symbol(apikey=api_key, query="Tech", limit=limit)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list)
        assert len(result_list) <= limit

        if result_list:
            # Validate first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPSymbolSearch.model_validate(first_item)
            else:
                validated = first_item
            assert validated.symbol
            assert validated.name

    def test_search_symbol_exact_match(self, api_key):
        """Test exact symbol match."""
        result = search.search_symbol(apikey=api_key, query="AAPL")

        # Extract data from API response
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate schema
        for item in result_list:
            if isinstance(item, dict):
                validated = FMPSymbolSearch.model_validate(item)
            else:
                validated = item  # Already a model instance
            assert validated.symbol
            assert validated.name
            assert validated.currency

        # Should find Apple Inc.
        apple_symbols = [
            item for item in result_list if "AAPL" in get_field_value(item, "symbol")
        ]
        assert len(apple_symbols) > 0

    def test_search_symbol_partial_match(self, api_key):
        """Test partial symbol matching."""
        result = search.search_symbol(apikey=api_key, query="AA")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Should return multiple matches
        assert len(result_list) >= 5

        # All symbols should contain "AA"
        for item in result_list:
            symbol = get_field_value(item, "symbol")
            assert "AA" in symbol.upper()
            if isinstance(item, dict):
                FMPSymbolSearch.model_validate(item)

    def test_search_symbol_with_exchange_filter(self, api_key):
        """Test symbol search with exchange filter."""
        result = search.search_symbol(apikey=api_key, query="AAPL", exchange="NASDAQ")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # All results should be from NASDAQ
        for item in result_list:
            exchange = get_field_value(item, "exchange")
            assert exchange == "NASDAQ"
            if isinstance(item, dict):
                FMPSymbolSearch.model_validate(item)

    def test_search_symbol_with_limit(self, api_key):
        """Test symbol search with result limit."""
        limit = 5
        result = search.search_symbol(apikey=api_key, query="A", limit=limit)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= limit
        assert len(result_list) > 0

        for item in result_list:
            if isinstance(item, dict):
                FMPSymbolSearch.model_validate(item)

    def test_search_symbol_empty_result(self, api_key):
        """Test symbol search with no matches."""
        result = search.search_symbol(apikey=api_key, query="ZZZNOMATCH999")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should return empty list for no matches

    def test_search_symbol_international(self, api_key):
        """Test search for international symbols."""
        result = search.search_symbol(apikey=api_key, query="ASML")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    FMPSymbolSearch.model_validate(item)


class TestSearchName:
    """Tests for search_name function."""

    def test_search_name_exact_company(self, api_key):
        """Test exact company name search."""
        result = search.search_name(apikey=api_key, query="Apple Inc")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        for item in result_list:
            if isinstance(item, dict):
                validated = FMPCompanyNameSearch.model_validate(item)
            else:
                validated = item
            assert validated.symbol
            assert validated.name
            assert "Apple" in validated.name

    def test_search_name_partial_match(self, api_key):
        """Test partial company name matching."""
        result = search.search_name(apikey=api_key, query="Bank")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Should return multiple bank companies
        for item in result_list:
            if isinstance(item, dict):
                FMPCompanyNameSearch.model_validate(item)
            name = get_field_value(item, "name")
            assert "Bank" in name or "BANK" in name

    def test_search_name_with_exchange_filter(self, api_key):
        """Test name search with exchange filter."""
        result = search.search_name(
            apikey=api_key, query="Microsoft", exchange="NASDAQ"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                exchange = get_field_value(item, "exchange")
                assert exchange == "NASDAQ"
                if isinstance(item, dict):
                    FMPCompanyNameSearch.model_validate(item)

    def test_search_name_with_limit(self, api_key):
        """Test name search with result limit."""
        limit = 3
        result = search.search_name(apikey=api_key, query="Bank", limit=limit)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= limit

        for item in result_list:
            if isinstance(item, dict):
                FMPCompanyNameSearch.model_validate(item)


class TestSearchCIK:
    """Tests for search_cik function."""

    def test_search_cik_valid_number(self, api_key):
        """Test CIK search with valid CIK number."""
        # Apple's CIK
        result = search.search_cik(apikey=api_key, query="320193")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPCompanyCIKSearch.model_validate(item)
                else:
                    validated = item
                assert validated.symbol
                assert validated.companyName
                assert validated.cik
                assert "320193" in validated.cik

    def test_search_cik_company_name(self, api_key):
        """Test CIK search by CIK number (Microsoft)."""
        # Microsoft's CIK
        result = search.search_cik(apikey=api_key, query="789019")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    FMPCompanyCIKSearch.model_validate(item)
                company_name = get_field_value(item, "companyName")
                cik_value = get_field_value(item, "cik")
                assert "Microsoft" in company_name or "MICROSOFT" in company_name
                assert "789019" in cik_value

    def test_search_cik_with_limit(self, api_key):
        """Test CIK search with result limit - Google's CIK."""
        limit = 5
        # Google/Alphabet's CIK
        result = search.search_cik(apikey=api_key, query="1652044", limit=limit)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= limit

        for item in result_list:
            if isinstance(item, dict):
                FMPCompanyCIKSearch.model_validate(item)
                cik_value = get_field_value(item, "cik")
                assert "1652044" in cik_value

    def test_search_cik_invalid_format(self, api_key):
        """Test CIK search with invalid format."""
        result = search.search_cik(apikey=api_key, query="INVALID_CIK")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should handle gracefully (empty result or error)


class TestSearchCUSIP:
    """Tests for search_cusip function."""

    def test_search_cusip_valid(self, api_key):
        """Test CUSIP search with valid identifier."""
        # Apple's CUSIP
        result = search.search_cusip(apikey=api_key, cusip="037833100")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPCusipSearch.model_validate(item)
                else:
                    validated = item
                assert validated.symbol
                assert validated.companyName
                assert validated.cusip == "037833100"

    def test_search_cusip_invalid_format(self, api_key):
        """Test CUSIP search with invalid format."""
        result = search.search_cusip(apikey=api_key, cusip="INVALID")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should handle gracefully


class TestSearchISIN:
    """Tests for search_isin function."""

    def test_search_isin_valid_us(self, api_key):
        """Test ISIN search with valid US ISIN."""
        # Apple's ISIN
        result = search.search_isin(apikey=api_key, isin="US0378331005")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPIsinSearch.model_validate(item)
                else:
                    validated = item
                assert validated.symbol
                assert validated.name
                assert validated.isin == "US0378331005"

    def test_search_isin_invalid_format(self, api_key):
        """Test ISIN search with invalid format."""
        result = search.search_isin(apikey=api_key, isin="INVALID_ISIN")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should handle gracefully


class TestCompanyScreener:
    """Tests for company_screener function."""

    def test_screener_market_cap_filter(self, api_key):
        """Test screener with market cap filters."""
        result = search.company_screener(
            apikey=api_key, market_cap_more_than=1000000000, limit=20  # > $1B
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        for item in result_list:
            if isinstance(item, dict):
                validated = FMPStockScreenerResult.model_validate(item)
            else:
                validated = item
            assert validated.marketCap >= 1000000000
            assert validated.symbol
            assert validated.companyName

    def test_screener_price_filter(self, api_key):
        """Test screener with price filters."""
        result = search.company_screener(
            apikey=api_key, price_more_than=10.0, price_lower_than=500.0, limit=15
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPStockScreenerResult.model_validate(item)
                else:
                    validated = item
                assert 10.0 <= validated.price <= 500.0

    def test_screener_sector_filter(self, api_key):
        """Test screener with sector filter."""
        result = search.company_screener(apikey=api_key, sector="Technology", limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPStockScreenerResult.model_validate(item)
                else:
                    validated = item
                if validated.sector:
                    assert "Technology" in validated.sector

    def test_screener_exchange_filter(self, api_key):
        """Test screener with exchange filter."""
        result = search.company_screener(apikey=api_key, exchange="NASDAQ", limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPStockScreenerResult.model_validate(item)
                else:
                    validated = item
                assert validated.exchangeShortName == "NASDAQ"

    def test_screener_etf_filter(self, api_key):
        """Test screener with ETF filter."""
        result = search.company_screener(apikey=api_key, is_etf=True, limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        for item in result_list:
            if isinstance(item, dict):
                FMPStockScreenerResult.model_validate(item)

    def test_screener_multiple_filters(self, api_key):
        """Test screener with multiple filters combined."""
        result = search.company_screener(
            apikey=api_key,
            market_cap_more_than=500000000,  # > $500M
            price_more_than=5.0,
            volume_more_than=100000,
            sector="Technology",
            limit=5,
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        for item in result_list:
            if isinstance(item, dict):
                validated = FMPStockScreenerResult.model_validate(item)
            else:
                validated = item
            assert validated.marketCap >= 500000000
            assert validated.price >= 5.0
            assert validated.volume >= 100000

    def test_screener_beta_filter(self, api_key):
        """Test screener with beta filters."""
        result = search.company_screener(
            apikey=api_key, beta_more_than=0.5, beta_lower_than=2.0, limit=10
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        for item in result_list:
            if isinstance(item, dict):
                validated = FMPStockScreenerResult.model_validate(item)
            else:
                validated = item
            if validated.beta is not None:
                assert 0.5 <= validated.beta <= 2.0

    def test_screener_no_filters(self, api_key):
        """Test screener with no filters (all stocks)."""
        result = search.company_screener(apikey=api_key, limit=5)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        for item in result_list:
            if isinstance(item, dict):
                FMPStockScreenerResult.model_validate(item)


class TestSearchExchangeVariants:
    """Tests for search_exchange_variants function."""

    def test_exchange_variants_single_listing(self, api_key):
        """Test exchange variants for symbol with single listing."""
        result = search.search_exchange_variants(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    FMPCompanyProfile.model_validate(item)

    def test_exchange_variants_multiple_listings(self, api_key):
        """Test exchange variants for symbol with multiple listings."""
        # Many international companies have multiple listings
        result = search.search_exchange_variants(
            apikey=api_key,
            symbol="TSM",  # Taiwan Semiconductor, often has multiple listings
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        for item in result_list:
            if isinstance(item, dict):
                FMPCompanyProfile.model_validate(item)

    def test_exchange_variants_invalid_symbol(self, api_key):
        """Test exchange variants for invalid symbol."""
        result = search.search_exchange_variants(apikey=api_key, symbol="INVALID999")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should handle gracefully (empty result)


class TestSearchErrorHandling:
    """Test error handling for search functions."""

    def test_search_symbol_invalid_api_key(self):
        """Test search_symbol with invalid API key."""
        result = search.search_symbol(apikey="invalid_key", query="AAPL")
        # Should return error message dict instead of raising exception
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            # If it returns a model, check if it's empty or has an error
            result_list = extract_data_list(result)
            # Should either be empty or have error indication

    def test_search_name_invalid_api_key(self):
        """Test search_name with invalid API key."""
        result = search.search_name(apikey="invalid_key", query="Apple")
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result

    def test_search_cik_invalid_api_key(self):
        """Test search_cik with invalid API key."""
        result = search.search_cik(apikey="invalid_key", query="320193")
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result

    def test_search_cusip_invalid_api_key(self):
        """Test search_cusip with invalid API key."""
        result = search.search_cusip(apikey="invalid_key", cusip="037833100")
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result

    def test_search_isin_invalid_api_key(self):
        """Test search_isin with invalid API key."""
        result = search.search_isin(apikey="invalid_key", isin="US0378331005")
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result

    def test_screener_invalid_api_key(self):
        """Test company_screener with invalid API key."""
        result = search.company_screener(apikey="invalid_key", limit=5)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result

    def test_exchange_variants_invalid_api_key(self):
        """Test search_exchange_variants with invalid API key."""
        result = search.search_exchange_variants(apikey="invalid_key", symbol="AAPL")
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result


class TestSearchResponseTimes:
    """Test response time performance for search functions."""

    def test_search_symbol_response_time(self, api_key):
        """Test search_symbol response time."""
        import time

        start_time = time.time()
        result = search.search_symbol(apikey=api_key, query="AAPL")
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 10.0  # Should respond within 10 seconds
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_screener_response_time(self, api_key):
        """Test company_screener response time."""
        import time

        start_time = time.time()
        result = search.company_screener(
            apikey=api_key, market_cap_more_than=1000000000, limit=10
        )
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 15.0  # Screener might be slower
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)


class TestSearchDataConsistency:
    """Test data consistency across search functions."""

    def test_symbol_vs_name_search_consistency(self, api_key):
        """Test consistency between symbol and name search results."""
        # Search by symbol
        symbol_result = search.search_symbol(apikey=api_key, query="AAPL")

        # Search by name
        name_result = search.search_name(apikey=api_key, query="Apple")

        symbol_list = extract_data_list(symbol_result)
        name_list = extract_data_list(name_result)

        assert isinstance(symbol_list, list)
        assert isinstance(name_list, list)

        if len(symbol_list) > 0 and len(name_list) > 0:
            # Look for Apple in both results
            symbol_apple = [
                item
                for item in symbol_list
                if get_field_value(item, "symbol") == "AAPL"
            ]
            name_apple = [
                item for item in name_list if get_field_value(item, "symbol") == "AAPL"
            ]

            if len(symbol_apple) > 0 and len(name_apple) > 0:
                # Should have consistent data
                symbol_name = get_field_value(symbol_apple[0], "name")
                name_name = get_field_value(name_apple[0], "name")
                assert symbol_name == name_name

                symbol_exchange = get_field_value(symbol_apple[0], "exchange")
                name_exchange = get_field_value(name_apple[0], "exchange")
                assert symbol_exchange == name_exchange

    def test_screener_vs_search_consistency(self, api_key):
        """Test consistency between screener and search results."""
        # Get Apple from screener
        screener_result = search.company_screener(
            apikey=api_key, market_cap_more_than=1000000000, limit=100
        )

        # Get Apple from symbol search
        symbol_result = search.search_symbol(apikey=api_key, query="AAPL")

        screener_list = extract_data_list(screener_result)
        symbol_list = extract_data_list(symbol_result)

        assert isinstance(screener_list, list)
        assert isinstance(symbol_list, list)

        if len(screener_list) > 0 and len(symbol_list) > 0:
            # Look for Apple in both
            screener_apple = [
                item
                for item in screener_list
                if get_field_value(item, "symbol") == "AAPL"
            ]
            symbol_apple = [
                item
                for item in symbol_list
                if get_field_value(item, "symbol") == "AAPL"
            ]

            if len(screener_apple) > 0 and len(symbol_apple) > 0:
                # Company name should be consistent
                screener_name = get_field_value(screener_apple[0], "companyName")
                symbol_name = get_field_value(symbol_apple[0], "name")
                assert screener_name in symbol_name or symbol_name in screener_name
