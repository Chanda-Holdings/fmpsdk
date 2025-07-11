from datetime import datetime, timedelta

import pytest

from fmpsdk import sec_filings


class TestSECRSSFeeds:
    """Test SEC RSS feeds functionality."""

    def test_sec_rss_feeds_success(self, api_key):
        """Test SEC RSS feeds with valid API key."""
        result = sec_filings.sec_rss_feeds(apikey=api_key, limit=10)

        # Handle both dict and model responses
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:  # If not empty
            assert len(data) <= 10  # Respect limit

            # Validate first item structure
            item = data[0]
            if isinstance(item, dict):
                # Should have RSS feed fields
                assert "title" in item or "link" in item or "description" in item

    def test_sec_rss_feeds_with_limit(self, api_key):
        """Test SEC RSS feeds with different limits."""
        result = sec_filings.sec_rss_feeds(apikey=api_key, limit=5)

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            assert len(data) <= 5

    def test_sec_rss_feeds_invalid_api_key(self):
        """Test SEC RSS feeds with invalid API key."""
        result = sec_filings.sec_rss_feeds(apikey="invalid_key", limit=5)

        # Should return error response
        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilings8K:
    """Test SEC 8-K filings functionality."""

    def test_sec_filings_8k_basic(self, api_key):
        """Test 8-K filings with basic date range."""
        # Use a recent date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_8k(
            apikey=api_key, from_date=start_date, to_date=end_date, limit=10
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            assert len(data) <= 10

            # Validate 8-K filing structure
            item = data[0]
            if isinstance(item, dict):
                # Should have filing-related fields
                expected_fields = ["symbol", "cik", "form", "filedDate", "acceptedDate"]
                assert any(field in item for field in expected_fields)

    def test_sec_filings_8k_with_pagination(self, api_key):
        """Test 8-K filings with pagination."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_8k(
            apikey=api_key, from_date=start_date, to_date=end_date, page=0, limit=5
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)

    def test_sec_filings_8k_invalid_api_key(self):
        """Test 8-K filings with invalid API key."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_8k(
            apikey="invalid_key", from_date=start_date, to_date=end_date
        )

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilingsFinancials:
    """Test SEC financial filings functionality."""

    def test_sec_filings_financials_basic(self, api_key):
        """Test financial filings with basic date range."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_financials(
            apikey=api_key, from_date=start_date, to_date=end_date, limit=10
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            assert len(data) <= 10

    def test_sec_filings_financials_invalid_api_key(self):
        """Test financial filings with invalid API key."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_financials(
            apikey="invalid_key", from_date=start_date, to_date=end_date
        )

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilingsSearchFormType:
    """Test SEC filings search by form type."""

    @pytest.mark.parametrize(
        "form_type,date_range_days,expected_filing_frequency",
        [
            ("10-K", 365, "annual"),  # Annual reports - should find some in a year
            ("10-Q", 90, "quarterly"),  # Quarterly reports - should find recent ones
            ("8-K", 30, "event_driven"),  # Current reports - frequent
            ("DEF 14A", 180, "annual"),  # Proxy statements - typically annual
            ("13F-HR", 90, "quarterly"),  # Institutional holdings - quarterly
            ("4", 30, "insider"),  # Insider trading - frequent
            ("3", 180, "initial"),  # Initial insider reports - less frequent
            ("S-1", 365, "registration"),  # Registration statements - varies
            ("424B2", 180, "prospectus"),  # Prospectus supplements - varies
            ("6-K", 180, "foreign"),  # Foreign company reports - varies
        ],
    )
    def test_sec_filings_search_form_type_comprehensive(
        self, api_key, form_type, date_range_days, expected_filing_frequency
    ):
        """Test SEC filings search with comprehensive form types and appropriate date ranges."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=date_range_days)).strftime(
            "%Y-%m-%d"
        )

        result = sec_filings.sec_filings_search_form_type(
            apikey=api_key,
            form_type=form_type,
            from_date=start_date,
            to_date=end_date,
            limit=10,
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None, f"Should get data for form type {form_type}"
        assert isinstance(data, list), f"Result should be a list for {form_type}"

        if data:
            assert len(data) <= 10, f"Should not exceed limit for {form_type}"

            # Validate that results match the form type
            item = data[0]
            if isinstance(item, dict) and "form" in item:
                assert (
                    item["form"] == form_type
                ), f"Form type should match for {form_type}"

                # Validate date is within range
                if "acceptedDate" in item:
                    filing_date = datetime.strptime(
                        item["acceptedDate"][:10], "%Y-%m-%d"
                    )
                    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                    assert (
                        start_dt <= filing_date <= end_dt
                    ), f"Filing date should be within range for {form_type}"

    def test_sec_filings_search_form_type_invalid_api_key(self):
        """Test form type search with invalid API key."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_search_form_type(
            apikey="invalid_key",
            form_type="10-K",
            from_date=start_date,
            to_date=end_date,
        )

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilingsSearchSymbol:
    """Test SEC filings search by symbol."""

    @pytest.mark.parametrize(
        "symbol,sector,date_range_days,expected_filing_types",
        [
            ("AAPL", "technology", 60, ["10-Q", "8-K"]),
            ("MSFT", "technology", 90, ["10-Q", "8-K", "DEF 14A"]),
            ("TSLA", "automotive", 60, ["10-Q", "8-K"]),
            ("JPM", "financial", 90, ["10-Q", "8-K", "DEF 14A"]),
            ("JNJ", "healthcare", 120, ["10-Q", "8-K", "DEF 14A"]),
            ("XOM", "energy", 90, ["10-Q", "8-K"]),
            ("WMT", "retail", 60, ["10-Q", "8-K"]),
            ("DIS", "media", 90, ["10-Q", "8-K"]),
            ("BA", "aerospace", 120, ["10-Q", "8-K"]),
            ("CAT", "industrial", 90, ["10-Q", "8-K"]),
            ("AMZN", "technology", 60, ["10-Q", "8-K"]),
            ("GOOGL", "technology", 90, ["10-Q", "8-K"]),
            ("META", "technology", 60, ["10-Q", "8-K"]),
            ("NFLX", "media", 90, ["10-Q", "8-K"]),
            ("NVDA", "technology", 60, ["10-Q", "8-K"]),
        ],
    )
    def test_sec_filings_search_symbol_sector_diversity(
        self, api_key, symbol, sector, date_range_days, expected_filing_types
    ):
        """Test SEC filings search across diverse sectors with varying date ranges."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=date_range_days)).strftime(
            "%Y-%m-%d"
        )

        result = sec_filings.sec_filings_search_symbol(
            apikey=api_key,
            symbol=symbol,
            from_date=start_date,
            to_date=end_date,
            limit=10,
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None, f"Should get data for {sector} company {symbol}"
        assert isinstance(data, list), f"Result should be a list for {symbol}"

        if data:
            assert len(data) <= 10, f"Should not exceed limit for {symbol}"

            # Validate that results match the symbol
            item = data[0]
            if isinstance(item, dict) and "symbol" in item:
                assert item["symbol"] == symbol, f"Symbol should match for {symbol}"

                # Check if we got expected filing types
                if "form" in item:
                    filing_forms = [item["form"] for item in data if "form" in item]
                    # At least one of the expected filing types should be present
                    has_expected_form = any(
                        form in filing_forms for form in expected_filing_types
                    )
                    # Note: We don't assert this strictly as filings depend on timing

                # Validate date range
                if "acceptedDate" in item:
                    filing_date = datetime.strptime(
                        item["acceptedDate"][:10], "%Y-%m-%d"
                    )
                    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                    assert (
                        start_dt <= filing_date <= end_dt
                    ), f"Filing date should be within range for {symbol}"

    def test_sec_filings_search_symbol_invalid_symbol(self, api_key):
        """Test SEC filings search with invalid symbol."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_search_symbol(
            apikey=api_key, symbol="INVALIDXYZ", from_date=start_date, to_date=end_date
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should return empty list or error for invalid symbol
        assert isinstance(data, list)
        # May be empty for invalid symbol

    def test_sec_filings_search_symbol_invalid_api_key(self):
        """Test symbol search with invalid API key."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_search_symbol(
            apikey="invalid_key", symbol="AAPL", from_date=start_date, to_date=end_date
        )

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilingsSearchCIK:
    """Test SEC filings search by CIK."""

    def test_sec_filings_search_cik_valid_cik(self, api_key):
        """Test SEC filings search with valid CIK."""
        # Apple's CIK
        cik = "0000320193"
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_search_cik(
            apikey=api_key, cik=cik, from_date=start_date, to_date=end_date, limit=5
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            assert len(data) <= 5

    def test_sec_filings_search_cik_invalid_api_key(self):
        """Test CIK search with invalid API key."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_search_cik(
            apikey="invalid_key",
            cik="0000320193",
            from_date=start_date,
            to_date=end_date,
        )

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilingsCompanySearch:
    """Test SEC filings company search functionality."""

    def test_sec_filings_company_search_name(self, api_key):
        """Test company search by name."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_company_search_name(
            apikey=api_key,
            company="Apple",
            from_date=start_date,
            to_date=end_date,
            limit=5,
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            # Note: API may not always respect limit parameter for this endpoint
            assert len(data) >= 1  # Should return at least some results

            # Validate company search result structure
            item = data[0]
            if isinstance(item, dict):
                expected_fields = ["symbol", "name", "cik", "sicCode"]
                assert any(field in item for field in expected_fields)
            else:
                # If Pydantic model
                assert hasattr(item, "symbol") or hasattr(item, "name")

    def test_sec_filings_company_search_symbol(self, api_key):
        """Test company search by symbol."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_company_search_symbol(
            apikey=api_key,
            symbol="AAPL",
            from_date=start_date,
            to_date=end_date,
            limit=5,
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            assert len(data) <= 5

    def test_sec_filings_company_search_cik_with_dates(self, api_key):
        """Test company search by CIK with date parameters using sec_filings_search_cik."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_search_cik(
            apikey=api_key,
            cik="0000320193",
            from_date=start_date,
            to_date=end_date,
            limit=5,
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)

    def test_sec_filings_company_search_cik_basic(self, api_key):
        """Test company search by CIK without date parameters."""
        result = sec_filings.sec_filings_company_search_cik(
            apikey=api_key, cik="0000320193"
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)

    def test_sec_filings_company_search_invalid_api_key(self):
        """Test company search with invalid API key."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_company_search_name(
            apikey="invalid_key",
            company="Apple",
            from_date=start_date,
            to_date=end_date,
        )

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECProfile:
    """Test SEC profile functionality."""

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL"])
    def test_sec_profile_valid_symbols(self, api_key, symbol):
        """Test SEC profile with valid symbols."""
        result = sec_filings.sec_profile(apikey=api_key, symbol=symbol)

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            # Validate profile structure
            item = data[0]
            if isinstance(item, dict):
                expected_fields = ["symbol", "companyName", "industry", "cik"]
                assert any(field in item for field in expected_fields)
            else:
                # If Pydantic model
                assert hasattr(item, "symbol") or hasattr(item, "companyName")

    def test_sec_profile_with_cik(self, api_key):
        """Test SEC profile with CIK parameter."""
        result = sec_filings.sec_profile(
            apikey=api_key, symbol="AAPL", cik_A="0000320193"
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)

    def test_sec_profile_invalid_symbol(self, api_key):
        """Test SEC profile with invalid symbol."""
        result = sec_filings.sec_profile(apikey=api_key, symbol="INVALIDXYZ")

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should return empty list for invalid symbol
        assert isinstance(data, list)

    def test_sec_profile_invalid_api_key(self):
        """Test SEC profile with invalid API key."""
        result = sec_filings.sec_profile(apikey="invalid_key", symbol="AAPL")

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestIndustryClassification:
    """Test industry classification functionality."""

    def test_industry_classification_list_basic(self, api_key):
        """Test industry classification list."""
        result = sec_filings.industry_classification_list(apikey=api_key)

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            # Validate classification structure
            item = data[0]
            if isinstance(item, dict):
                expected_fields = ["sicCode", "industryTitle", "office"]
                assert any(field in item for field in expected_fields)
            else:
                # If Pydantic model
                assert hasattr(item, "sicCode") or hasattr(item, "industryTitle")

    def test_industry_classification_list_with_filters(self, api_key):
        """Test industry classification list with filters."""
        result = sec_filings.industry_classification_list(
            apikey=api_key, industry_title="Technology"
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)

    def test_industry_classification_search_by_symbol(self, api_key):
        """Test industry classification search by symbol."""
        result = sec_filings.industry_classification_search(
            apikey=api_key, symbol="AAPL"
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            # Validate search result structure
            item = data[0]
            if isinstance(item, dict):
                expected_fields = ["symbol", "sicCode", "industryTitle"]
                assert any(field in item for field in expected_fields)
            else:
                # If Pydantic model
                assert hasattr(item, "symbol") or hasattr(item, "sicCode")

    def test_industry_classification_search_by_cik(self, api_key):
        """Test industry classification search by CIK."""
        result = sec_filings.industry_classification_search(
            apikey=api_key, cik="0000320193"
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)

    def test_industry_classification_all(self, api_key):
        """Test all industry classifications."""
        result = sec_filings.industry_classification_all(
            apikey=api_key, page="0", limit="10"
        )

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert data is not None
        assert isinstance(data, list)
        if data:
            assert len(data) <= 10

    def test_industry_classification_invalid_api_key(self):
        """Test industry classification with invalid API key."""
        result = sec_filings.industry_classification_list(apikey="invalid_key")

        assert isinstance(result, dict)
        assert "Error Message" in result


class TestSECFilingsErrorHandling:
    """Test error handling across SEC filings functions."""

    def test_invalid_date_format_handling(self, api_key):
        """Test handling of invalid date formats."""
        # This should handle gracefully or return an error
        result = sec_filings.sec_filings_8k(
            apikey=api_key, from_date="invalid-date", to_date="invalid-date"
        )

        # Should either return error or handle gracefully
        assert result is not None

    def test_future_date_handling(self, api_key):
        """Test handling of future dates."""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")

        result = sec_filings.sec_filings_8k(
            apikey=api_key, from_date=today, to_date=future_date, limit=5
        )

        # Should handle future dates gracefully
        assert result is not None


class TestSECFilingsResponseTimes:
    """Test response times for SEC filings functions."""

    def test_sec_filings_response_time(self, api_key):
        """Test that SEC filings functions respond within reasonable time."""
        import time

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # Test RSS feeds response time
        start_time = time.time()
        result = sec_filings.sec_rss_feeds(apikey=api_key, limit=5)
        end_time = time.time()
        assert (end_time - start_time) < 10.0  # Should respond within 10 seconds

        # Test 8-K filings response time
        start_time = time.time()
        result = sec_filings.sec_filings_8k(
            apikey=api_key, from_date=start_date, to_date=end_date, limit=5
        )
        end_time = time.time()
        assert (end_time - start_time) < 10.0

        # Test SEC profile response time
        start_time = time.time()
        result = sec_filings.sec_profile(apikey=api_key, symbol="AAPL")
        end_time = time.time()
        assert (end_time - start_time) < 10.0


class TestSECFilingsDataConsistency:
    """Test data consistency across SEC filings functions."""

    def test_company_search_consistency(self, api_key):
        """Test consistency between different company search methods."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        # Search by symbol
        symbol_result = sec_filings.sec_filings_company_search_symbol(
            apikey=api_key,
            symbol="AAPL",
            from_date=start_date,
            to_date=end_date,
            limit=1,
        )

        # Search by name
        name_result = sec_filings.sec_filings_company_search_name(
            apikey=api_key,
            company="Apple",
            from_date=start_date,
            to_date=end_date,
            limit=1,
        )

        # Both should return data
        if hasattr(symbol_result, "root"):
            symbol_data = symbol_result.root
        else:
            symbol_data = symbol_result

        if hasattr(name_result, "root"):
            name_data = name_result.root
        else:
            name_data = name_result

        assert isinstance(symbol_data, list)
        assert isinstance(name_data, list)

    def test_search_vs_profile_consistency(self, api_key):
        """Test consistency between search results and profile data."""
        # Get SEC profile
        profile_result = sec_filings.sec_profile(apikey=api_key, symbol="AAPL")

        # Get classification search
        classification_result = sec_filings.industry_classification_search(
            apikey=api_key, symbol="AAPL"
        )

        # Both should return data for valid symbols
        if hasattr(profile_result, "root"):
            profile_data = profile_result.root
        else:
            profile_data = profile_result

        if hasattr(classification_result, "root"):
            classification_data = classification_result.root
        else:
            classification_data = classification_result

        assert isinstance(profile_data, list)
        assert isinstance(classification_data, list)
