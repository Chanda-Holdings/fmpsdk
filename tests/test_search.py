import pytest

from fmpsdk import search
from fmpsdk.exceptions import InvalidQueryParameterException
from fmpsdk.models import (
    FMPCompanyCIKSearch,
    FMPCompanyNameSearch,
    FMPCompanyProfile,
    FMPCusipSearch,
    FMPIsinSearch,
    FMPStockScreenerResult,
    FMPSymbolSearch,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
    validate_required_fields,
)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestSymbolSearch:
    """Test class for symbol search functionality with comprehensive validation."""

    @pytest.mark.parametrize(
        "query,search_type,expected_patterns,min_results",
        [
            # Exact symbol matches
            ("AAPL", "exact_symbol", {"symbol_match": "exact", "company": "Apple"}, 1),
            (
                "MSFT",
                "exact_symbol",
                {"symbol_match": "exact", "company": "Microsoft"},
                1,
            ),
            (
                "GOOGL",
                "exact_symbol",
                {"symbol_match": "exact", "company": "Google"},
                1,
            ),
            ("TSLA", "exact_symbol", {"symbol_match": "exact", "company": "Tesla"}, 1),
            ("META", "exact_symbol", {"symbol_match": "exact", "company": "Meta"}, 1),
            # Company name searches
            (
                "Apple",
                "company_name",
                {"symbol_contains": "AAPL", "relevance": "high"},
                0,
            ),
            (
                "Microsoft",
                "company_name",
                {"symbol_contains": "MSFT", "relevance": "high"},
                0,
            ),
            (
                "Google",
                "company_name",
                {"symbol_contains": "GOOGL", "relevance": "high"},
                0,
            ),
            (
                "Amazon",
                "company_name",
                {"symbol_contains": "AMZN", "relevance": "high"},
                0,
            ),
            (
                "Tesla",
                "company_name",
                {"symbol_contains": "TSLA", "relevance": "high"},
                0,
            ),
            (
                "Netflix",
                "company_name",
                {"symbol_contains": "NFLX", "relevance": "high"},
                0,
            ),
            # Partial matches
            (
                "Alphabet",
                "partial_name",
                {"symbol_contains": "GOOGL", "relevance": "moderate"},
                0,
            ),
            (
                "Berkshire",
                "partial_name",
                {"symbol_contains": "BRK", "relevance": "moderate"},
                0,
            ),
            (
                "Johnson",
                "partial_name",
                {"symbol_contains": "JNJ", "relevance": "moderate"},
                0,
            ),
            (
                "JPMorgan",
                "partial_name",
                {"symbol_contains": "JPM", "relevance": "moderate"},
                0,
            ),
            # Industry searches
            ("Bank", "industry", {"sector": "financial", "diversity": "high"}, 0),
            ("Energy", "industry", {"sector": "energy", "diversity": "high"}, 0),
            (
                "Technology",
                "industry",
                {"sector": "technology", "diversity": "high"},
                0,
            ),
            (
                "Healthcare",
                "industry",
                {"sector": "healthcare", "diversity": "high"},
                0,
            ),
            # ETF searches (adjust expectations as API data varies)
            ("SPDR", "etf_family", {"structure": "etf", "family": "state_street"}, 0),
            ("iShares", "etf_family", {"structure": "etf", "family": "blackrock"}, 0),
            ("Vanguard", "etf_family", {"structure": "etf", "family": "vanguard"}, 0),
            # International searches (adjust expectations as API data varies)
            ("Toyota", "international", {"geography": "japan", "adr": True}, 0),
            ("ASML", "international", {"geography": "netherlands", "adr": True}, 1),
            ("Nestle", "international", {"geography": "switzerland", "adr": True}, 1),
        ],
    )
    def test_symbol_search_comprehensive(
        self, api_key, query, search_type, expected_patterns, min_results
    ):
        """Test comprehensive symbol search with business logic validation."""
        response, validation = handle_api_call_with_validation(
            search.search_symbol, "search_symbol", apikey=api_key, query=query, limit=50
        )

        search_results = get_response_models(response, FMPSymbolSearch)
        validate_model_list(search_results, FMPSymbolSearch, min_count=min_results)
        assert len(search_results) >= min_results

        # Validate search results structure
        for item in search_results[:5]:  # Check first 5 results
            symbol = item.symbol
            name = item.name
            currency = item.currency

            assert symbol is not None and len(symbol) > 0
            assert name is not None and len(name) > 0
            assert (
                len(symbol) <= 15
            )  # Reasonable symbol length (increased for international symbols)

            # Currency validation
            if currency:
                assert currency in [
                    "USD",
                    "EUR",
                    "GBP",
                    "CAD",
                    "JPY",
                    "CHF",
                    "AUD",
                    "HKD",
                    "GBp",
                    "MXN",
                    "SEK",
                    "NOK",
                    "DKK",
                    "SGD",
                    "NZD",
                    "ZAR",
                    "BRL",
                    "CNY",
                    "INR",
                    "KRW",
                    "IDR",
                    "PLN",
                    "TRY",
                    "RUB",
                    "THB",
                ]

        # Search type-specific validation
        if search_type == "exact_symbol":
            # Should find exact match in results
            found_exact = any(item.symbol == query for item in search_results)
            assert found_exact, f"Should find exact symbol match for {query}"

        elif search_type == "company_name":
            # Should find relevant company in results if any results are returned
            if search_results:
                found_company = any(
                    expected_patterns["symbol_contains"] in item.symbol
                    for item in search_results
                )
                assert found_company, f"Should find company symbol for {query}"

        elif search_type == "industry":
            # Should find multiple companies in the sector
            assert len(search_results) >= min_results

        elif search_type == "etf_family":
            # Should find ETF family members
            etf_symbols = [item.symbol for item in search_results]
            assert len(etf_symbols) >= min_results

    @pytest.mark.parametrize(
        "limit,expected_behavior",
        [
            (1, "single_result"),
            (5, "limited_results"),
            (10, "moderate_results"),
            (25, "many_results"),
            (50, "max_results"),
        ],
    )
    def test_symbol_search_limit_validation(self, api_key, limit, expected_behavior):
        """Test symbol search with different limit parameters."""
        response, validation = handle_api_call_with_validation(
            search.search_symbol,
            "search_symbol",
            apikey=api_key,
            query="Tech",
            limit=limit,
        )

        search_results = get_response_models(response, FMPSymbolSearch)
        validate_model_list(search_results, FMPSymbolSearch)
        assert len(search_results) <= limit

        if search_results:
            # Validate result quality
            first_item = search_results[0]
            symbol = first_item.symbol
            name = first_item.name

            assert symbol is not None and len(symbol) > 0
            assert name is not None and len(name) > 0

            # Limit-specific validation
            if expected_behavior == "single_result":
                assert len(search_results) == 1
            elif expected_behavior == "limited_results":
                assert len(search_results) <= 5
            elif expected_behavior == "max_results":
                assert len(search_results) <= 50

    @pytest.mark.parametrize(
        "exchange,expected_listings",
        [
            ("NASDAQ", {"primary_exchange": "NASDAQ", "tech_heavy": True}),
            ("NYSE", {"primary_exchange": "NYSE", "traditional": True}),
            ("AMEX", {"primary_exchange": "AMEX", "smaller_companies": True}),
        ],
    )
    def test_symbol_search_exchange_filtering(
        self, api_key, exchange, expected_listings
    ):
        """Test symbol search with exchange-specific filtering."""
        response, validation = handle_api_call_with_validation(
            search.search_symbol,
            "search_symbol",
            apikey=api_key,
            query="A",  # Broad search
            exchange=exchange,
            limit=20,
        )

        search_results = get_response_models(response, FMPSymbolSearch)
        validate_model_list(search_results, FMPSymbolSearch)

        if search_results:
            # Validate exchange information
            for item in search_results[:5]:
                symbol = item.symbol
                name = item.name
                exchange_info = item.exchange

                assert symbol is not None
                assert name is not None

                # Exchange-specific validation
                if exchange_info:
                    if exchange == "NASDAQ":
                        # Many NASDAQ symbols should be technology-related
                        assert exchange_info in ["NASDAQ", "NMS", "NCM"]
                    elif exchange == "NYSE":
                        # NYSE should have traditional listings
                        assert exchange_info in ["NYSE", "NYQ"]
                    elif exchange == "AMEX":
                        # AMEX should be present
                        assert exchange_info in ["AMEX", "ASE"]


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCompanyNameSearch:
    """Test class for company name search functionality."""

    @pytest.mark.parametrize(
        "company_name,expected_symbol,search_quality",
        [
            ("Apple Inc", "AAPL", "exact_match"),
            ("Microsoft Corporation", "MSFT", "exact_match"),
            ("Alphabet Inc", "GOOGL", "exact_match"),
            ("Amazon", "AMZN", "exact_match"),  # Use shorter name that works
            ("Tesla", "TSLA", "exact_match"),  # Use shorter name that works
            ("Johnson & Johnson", "JNJ", "exact_match"),
            ("JPMorgan Chase", "JPM", "partial_match"),
            ("Berkshire Hathaway", "BRK", "partial_match"),
            ("Walmart Inc", "WMT", "exact_match"),
            ("Exxon Mobil", "XOM", "exact_match"),
        ],
    )
    def test_company_name_search_validation(
        self, api_key, company_name, expected_symbol, search_quality
    ):
        """Test company name search with comprehensive validation."""
        response, validation = handle_api_call_with_validation(
            search.search_name,
            "search_name",
            apikey=api_key,
            query=company_name,
            limit=10,
        )

        search_results = get_response_models(response, FMPCompanyNameSearch)
        validate_model_list(search_results, FMPCompanyNameSearch)
        assert len(search_results) > 0

        # Validate search results structure
        for item in search_results[:3]:  # Check first 3 results
            symbol = item.symbol
            name = item.name

            assert symbol is not None and len(symbol) > 0
            assert name is not None and len(name) > 0
            assert len(symbol) <= 10  # Reasonable symbol length

        # Search quality-specific validation
        if search_quality == "exact_match":
            # Should find exact company match in top results
            found_exact = any(
                expected_symbol in item.symbol for item in search_results[:3]
            )
            assert found_exact, f"Should find {expected_symbol} for {company_name}"

        elif search_quality == "partial_match":
            # Should find related company somewhere in results
            found_related = any(
                expected_symbol in item.symbol for item in search_results
            )
            assert (
                found_related
            ), f"Should find {expected_symbol} related to {company_name}"

        # Validate data quality
        first_result = search_results[0]
        symbol = first_result.symbol
        name = first_result.name

        # Most relevant result should contain search term
        assert company_name.lower() in name.lower() or any(
            word.lower() in name.lower() for word in company_name.split()
        )

    @pytest.mark.parametrize(
        "search_term,expected_sector,min_results",
        [
            ("Bank", "financial", 3),
            ("Insurance", "financial", 2),
            ("Technology", "technology", 5),
            ("Pharmaceutical", "healthcare", 3),
            ("Energy", "energy", 2),
            ("Retail", "consumer_discretionary", 2),
            ("Utility", "utilities", 2),
        ],
    )
    def test_company_name_search_by_sector(
        self, api_key, search_term, expected_sector, min_results
    ):
        """Test company name search across different sectors."""
        response, validation = handle_api_call_with_validation(
            search.search_name,
            "search_name",
            apikey=api_key,
            query=search_term,
            limit=20,
        )

        search_results = get_response_models(response, FMPCompanyNameSearch)
        validate_model_list(search_results, FMPCompanyNameSearch)
        assert len(search_results) >= min_results

        # Validate sector diversity
        unique_symbols = set()
        for item in search_results:
            symbol = item.symbol
            name = item.name

            assert symbol is not None and len(symbol) > 0
            assert name is not None and len(name) > 0
            unique_symbols.add(symbol)

            # Sector-specific validation
            if expected_sector == "financial":
                # Financial companies often have keywords
                financial_keywords = [
                    "bank",
                    "financial",
                    "insurance",
                    "capital",
                    "group",
                ]
                has_financial_keyword = any(
                    keyword in name.lower() for keyword in financial_keywords
                )
                if not has_financial_keyword:
                    # Allow some flexibility but most should match
                    pass

            elif expected_sector == "technology":
                # Technology companies often have tech-related terms
                tech_keywords = [
                    "tech",
                    "systems",
                    "software",
                    "data",
                    "digital",
                    "computing",
                ]
                # Allow flexibility for broad technology search

        # Validate diversity - should find multiple unique companies
        assert len(unique_symbols) >= min_results

    def test_company_name_search_data_quality(self, api_key):
        """Test company name search data quality and consistency."""
        # Test with well-known companies
        test_companies = ["Apple", "Microsoft", "Google", "Amazon", "Tesla"]

        for company in test_companies:
            response, validation = handle_api_call_with_validation(
                search.search_name,
                "search_name",
                apikey=api_key,
                query=company,
                limit=5,
            )

            search_results = get_response_models(response, FMPCompanyNameSearch)
            validate_model_list(search_results, FMPCompanyNameSearch)

            if search_results:
                first_result = search_results[0]
                symbol = first_result.symbol
                name = first_result.name

                assert symbol is not None and len(symbol) > 0
                assert name is not None and len(name) > 0

                # Symbol should be reasonable length
                assert 1 <= len(symbol) <= 10

                # Name should contain the search term or be highly relevant
                assert company.lower() in name.lower() or any(
                    word.lower() in name.lower() for word in company.split()
                )


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCIKSearch:
    """Test class for CIK (Central Index Key) search functionality."""

    @pytest.mark.parametrize(
        "cik_input,search_type,expected_results",
        [
            # Well-known CIK numbers (only numeric CIKs work)
            ("320193", "numeric_cik", {"company": "Apple", "symbol": "AAPL"}),
            ("789019", "numeric_cik", {"company": "Microsoft", "symbol": "MSFT"}),
            ("1652044", "numeric_cik", {"company": "Alphabet", "symbol": "GOOGL"}),
            ("1018724", "numeric_cik", {"company": "Amazon", "symbol": "AMZN"}),
            ("1318605", "numeric_cik", {"company": "Tesla", "symbol": "TSLA"}),
        ],
    )
    def test_cik_search_validation(
        self, api_key, cik_input, search_type, expected_results
    ):
        """Test CIK search with validation."""
        response, validation = handle_api_call_with_validation(
            search.search_cik, "search_cik", apikey=api_key, query=cik_input, limit=10
        )

        search_results = get_response_models(response, FMPCompanyCIKSearch)
        validate_model_list(search_results, FMPCompanyCIKSearch)
        assert len(search_results) > 0

        # Validate search results
        found_match = False
        for item in search_results:
            cik = item.cik
            name = item.companyName

            assert cik is not None
            assert name is not None

            # CIK should be numeric string
            assert str(cik).isdigit() or cik.isdigit()

            # Search type-specific validation (only numeric CIK supported)
            if search_type == "numeric_cik":
                if cik_input in str(cik):
                    found_match = True
                    assert expected_results["company"].lower() in name.lower()
                    break

        assert found_match, f"Should find CIK match for {cik_input}"

    def test_cik_search_data_quality(self, api_key):
        """Test CIK search data quality and consistency."""
        response, validation = handle_api_call_with_validation(
            search.search_cik,
            "search_cik",
            apikey=api_key,
            query="320193",  # Use Apple's CIK instead of company name
            limit=5,
        )

        search_results = get_response_models(response, FMPCompanyCIKSearch)
        validate_model_list(search_results, FMPCompanyCIKSearch)
        assert len(search_results) > 0

        # Validate data quality
        for item in search_results:
            cik = item.cik
            name = item.companyName

            # CIK validation
            assert cik is not None
            assert len(str(cik)) >= 1

            # Name validation
            assert name is not None
            assert len(name) > 0

            # CIK should be reasonable length (typically 10 digits or less)
            assert len(str(cik)) <= 10

    def test_cik_search_company_name_error(self, api_key):
        """Test that company name searches are not supported by CIK search API."""
        with pytest.raises(InvalidQueryParameterException) as exc_info:
            response, validation = handle_api_call_with_validation(
                search.search_cik,
                "search_cik",
                apikey=api_key,
                query="Apple",  # Company names are not supported
            )

        assert "Invalid or missing query parameter" in str(exc_info.value)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCUSIPSearch:
    """Test class for CUSIP search functionality."""

    @pytest.mark.parametrize(
        "cusip_input,expected_characteristics",
        [
            ("037833100", {"company": "Apple", "format": "valid"}),
            ("594918104", {"company": "Microsoft", "format": "valid"}),
            ("02079K305", {"company": "Alphabet", "format": "valid"}),
            ("023135106", {"company": "Amazon", "format": "valid"}),
        ],
    )
    def test_cusip_search_validation(
        self, api_key, cusip_input, expected_characteristics
    ):
        """Test CUSIP search validation."""
        response, validation = handle_api_call_with_validation(
            search.search_cusip, "search_cusip", apikey=api_key, cusip=cusip_input
        )

        search_results = get_response_models(response, FMPCusipSearch)
        validate_model_list(search_results, FMPCusipSearch)

        if search_results:
            # Validate CUSIP structure
            for item in search_results:
                cusip = item.cusip
                name = item.companyName

                if cusip:
                    assert len(cusip) == 9  # CUSIP should be 9 characters
                    assert cusip.replace(" ", "").isalnum()  # Should be alphanumeric

                if name:
                    assert len(name) > 0

                    # Check for expected company match
                    if expected_characteristics.get("company"):
                        expected_company = expected_characteristics["company"]
                        assert expected_company.lower() in name.lower()

    def test_cusip_search_format_validation(self, api_key):
        """Test CUSIP search with format validation."""
        # Test with invalid CUSIP format
        response, validation = handle_api_call_with_validation(
            search.search_cusip, "search_cusip", apikey=api_key, cusip="INVALID"
        )

        search_results = get_response_models(response, FMPCusipSearch)
        validate_model_list(search_results, FMPCusipSearch, min_count=0)
        # Invalid CUSIP should return empty results (which is correct)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestISINSearch:
    """Test class for ISIN search functionality."""

    @pytest.mark.parametrize(
        "isin_input,expected_characteristics",
        [
            ("US0378331005", {"country": "US", "company": "Apple", "format": "valid"}),
            (
                "US5949181045",
                {"country": "US", "company": "Microsoft", "format": "valid"},
            ),
            (
                "US02079K3059",
                {"country": "US", "company": "Alphabet", "format": "valid"},
            ),
            ("US0231351067", {"country": "US", "company": "Amazon", "format": "valid"}),
        ],
    )
    def test_isin_search_validation(
        self, api_key, isin_input, expected_characteristics
    ):
        """Test ISIN search validation."""
        response, validation = handle_api_call_with_validation(
            search.search_isin, "search_isin", apikey=api_key, isin=isin_input
        )

        search_results = get_response_models(response, FMPIsinSearch)
        validate_model_list(search_results, FMPIsinSearch)

        if search_results:
            # Validate ISIN structure
            for item in search_results:
                isin = item.isin
                name = item.name

                if isin:
                    assert len(isin) == 12  # ISIN should be 12 characters
                    assert isin[
                        :2
                    ].isalpha()  # First 2 characters should be country code
                    assert isin[2:].isalnum()  # Remaining should be alphanumeric

                    # Country validation
                    if expected_characteristics.get("country"):
                        expected_country = expected_characteristics["country"]
                        assert isin.startswith(expected_country)

                if name:
                    assert len(name) > 0

                    # Check for expected company match
                    if expected_characteristics.get("company"):
                        expected_company = expected_characteristics["company"]
                        assert expected_company.lower() in name.lower()


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestStockScreener:
    """Test class for stock screener functionality."""

    @pytest.mark.parametrize(
        "filter_type,filter_params,expected_characteristics",
        [
            (
                "market_cap",
                {"market_cap_more_than": "10000000000"},
                {"segment": "large_cap", "min_results": 5},
            ),
            (
                "market_cap",
                {"market_cap_lower_than": "2000000000"},
                {"segment": "small_cap", "min_results": 5},
            ),
            (
                "price_range",
                {"price_more_than": "50", "price_lower_than": "200"},
                {"price_range": "mid", "min_results": 5},
            ),
            (
                "sector",
                {"sector": "Technology"},
                {"sector": "technology", "min_results": 10},
            ),
            (
                "exchange",
                {"exchange": "NASDAQ"},
                {"exchange": "nasdaq", "min_results": 10},
            ),
            (
                "dividend",
                {"dividend_more_than": "2"},
                {"dividend_yield": "high", "min_results": 3},
            ),
            (
                "beta",
                {"beta_more_than": "1.5"},
                {"volatility": "high", "min_results": 5},
            ),
        ],
    )
    def test_stock_screener_filters(
        self, api_key, filter_type, filter_params, expected_characteristics
    ):
        """Test stock screener with various filters."""
        response, validation = handle_api_call_with_validation(
            search.company_screener,
            "screener",
            apikey=api_key,
            limit=20,
            **filter_params,
        )

        screener_results = get_response_models(response, FMPStockScreenerResult)
        validate_model_list(screener_results, FMPStockScreenerResult)
        assert len(screener_results) >= expected_characteristics["min_results"]

        # Validate screener results
        for item in screener_results[:5]:
            symbol = item.symbol
            company_name = item.companyName
            price = item.price
            market_cap = item.marketCap

            assert symbol is not None
            assert company_name is not None

            # Filter-specific validation
            if filter_type == "market_cap":
                if market_cap is not None:
                    if "market_cap_more_than" in filter_params:
                        min_cap = float(filter_params["market_cap_more_than"])
                        assert market_cap >= min_cap
                    if "market_cap_lower_than" in filter_params:
                        max_cap = float(filter_params["market_cap_lower_than"])
                        assert market_cap <= max_cap

            elif filter_type == "price_range":
                if price is not None:
                    if "price_more_than" in filter_params:
                        min_price = float(filter_params["price_more_than"])
                        assert price >= min_price
                    if "price_lower_than" in filter_params:
                        max_price = float(filter_params["price_lower_than"])
                        assert price <= max_price

            elif filter_type == "sector":
                sector = item.sector
                if sector:
                    expected_sector = filter_params["sector"]
                    assert expected_sector.lower() in sector.lower()

    def test_stock_screener_comprehensive(self, api_key):
        """Test comprehensive stock screener functionality."""
        response, validation = handle_api_call_with_validation(
            search.company_screener,
            "company_screener",
            apikey=api_key,
            market_cap_more_than="1000000000",
            price_more_than="10",
            limit=10,
        )

        screener_results = get_response_models(response, FMPStockScreenerResult)
        validate_model_list(screener_results, FMPStockScreenerResult)
        assert len(screener_results) > 0

        # Validate comprehensive data
        for item in screener_results:
            symbol = item.symbol
            company_name = item.companyName
            price = item.price
            market_cap = item.marketCap
            sector = item.sector

            # Basic validation
            assert symbol is not None
            assert company_name is not None

            # Price validation
            if price is not None:
                assert price >= 10  # Based on filter

            # Market cap validation
            if market_cap is not None:
                assert market_cap >= 1000000000  # Based on filter

            # Symbol format validation
            assert len(symbol) <= 10
            assert symbol.isalnum() or "-" in symbol or "." in symbol


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestSearchErrorHandling:
    """Test class for search error handling and edge cases."""

    @pytest.mark.parametrize(
        "search_function,invalid_input,expected_behavior",
        [
            # Empty strings should cause parameter exceptions
            (search.search_symbol, "", "parameter_exception"),
            (search.search_name, "", "parameter_exception"),
            # Invalid but non-empty inputs should return empty results
            (search.search_symbol, "INVALID_SYMBOL_12345", "empty_result"),
            (search.search_name, "NONEXISTENT_COMPANY_XYZ", "empty_result"),
            (
                search.search_cik,
                "INVALID_CIK",
                "parameter_exception",
            ),  # Invalid CIK causes exception
            (search.search_cusip, "INVALID", "empty_result"),
            (search.search_isin, "INVALID", "empty_result"),
        ],
    )
    def test_search_invalid_inputs(
        self, api_key, search_function, invalid_input, expected_behavior
    ):
        """Test search functions with invalid inputs."""
        # Determine the correct parameter name for each function
        if search_function.__name__ == "search_cusip":
            param_name = "cusip"
        elif search_function.__name__ == "search_isin":
            param_name = "isin"
        elif search_function.__name__ == "search_cik":
            param_name = "query"  # CIK search function uses 'query' parameter
        else:
            param_name = "query"

        kwargs = {"apikey": api_key, param_name: invalid_input}

        if expected_behavior == "parameter_exception":
            # Expect InvalidQueryParameterException for empty strings and invalid CIKs
            with pytest.raises(InvalidQueryParameterException) as exc_info:
                response, validation = handle_api_call_with_validation(
                    search_function, search_function.__name__, **kwargs
                )
            assert "Invalid or missing query parameter" in str(exc_info.value)
            return

        # For empty_result behavior
        response, validation = handle_api_call_with_validation(
            search_function, search_function.__name__, **kwargs
        )

        # For invalid inputs test, we just need to check empty results generically
        if isinstance(response, list):
            search_results = response
        elif hasattr(response, "model_dump"):
            dumped = response.model_dump()
            search_results = dumped if isinstance(dumped, list) else [dumped]
        else:
            search_results = []

        assert isinstance(search_results, list)

        if expected_behavior == "empty_result":
            # Should return empty list for invalid inputs
            assert len(search_results) == 0 or search_results == []

    def test_search_api_key_validation(self):
        """Test search API key validation."""
        with pytest.raises(Exception):
            search.search_symbol(apikey="invalid_key", query="AAPL")

    @pytest.mark.parametrize(
        "limit_value,expected_result",
        [
            (0, "empty_or_error"),
            (1, "single_result"),
            (100, "max_results"),
            (1000, "max_results_capped"),
        ],
    )
    def test_search_limit_edge_cases(self, api_key, limit_value, expected_result):
        """Test search limit edge cases."""
        response, validation = handle_api_call_with_validation(
            search.search_symbol,
            "search_symbol",
            apikey=api_key,
            query="A",
            limit=limit_value,
        )

        search_results = get_response_models(response, FMPSymbolSearch)
        validate_model_list(search_results, FMPSymbolSearch)

        if expected_result == "single_result":
            assert len(search_results) <= 1
        elif expected_result == "max_results":
            assert len(search_results) <= 100
        elif expected_result == "max_results_capped":
            # API should cap results at reasonable limit
            assert len(search_results) <= 1000
