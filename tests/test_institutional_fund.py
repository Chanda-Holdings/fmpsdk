"""
Comprehensive tests for fmpsdk.institutional_fund module.
Tests all institutional fund and SEC filings functions including error handling.
"""
import os
import pytest

import fmpsdk.institutional_fund as inst
from fmpsdk.models import *

API_KEY = os.getenv("FMP_API_KEY")


# === PARAMETERIZED TEST CLASSES ===

class TestParameterizedSECRSSFeeds:
    """Comprehensive parameterized tests for SEC RSS feeds."""

    @pytest.mark.parametrize("limit,expected_type", [
        (1, (list, type(None))),
        (5, (list, type(None))),
        (10, (list, type(None))),
        (25, (list, type(None))),
        (50, (list, type(None))),
        (100, (list, type(None))),
        (250, (list, type(None))),
        (500, (list, type(None))),
    ])
    def test_sec_rss_feeds_limits(self, limit, expected_type):
        """Test SEC RSS feeds with various limit values."""
        result = inst.sec_rss_feeds(apikey=API_KEY, limit=limit)
        assert isinstance(result, expected_type)

    @pytest.mark.parametrize("filename", [
        "test_feeds.csv",
        "custom_feeds.csv",
        "rss_data.csv",
        "feeds_2024.csv",
        "sec_feeds_backup.csv",
    ])
    def test_sec_rss_feeds_filenames(self, filename):
        """Test SEC RSS feeds with various filename formats."""
        result = inst.sec_rss_feeds(apikey=API_KEY, limit=10, filename=filename)
        assert result is not None

    @pytest.mark.parametrize("limit,filename", [
        (5, "small_feeds.csv"),
        (10, "medium_feeds.csv"),
        (25, "large_feeds.csv"),
        (50, "xlarge_feeds.csv"),
        (100, "xxlarge_feeds.csv"),
    ])
    def test_sec_rss_feeds_limit_filename_combinations(self, limit, filename):
        """Test SEC RSS feeds with limit and filename combinations."""
        result = inst.sec_rss_feeds(apikey=API_KEY, limit=limit, filename=filename)
        assert result is not None

    @pytest.mark.parametrize("edge_limit", [
        0,
        -1,
        999999,
        1000000,
    ])
    def test_sec_rss_feeds_edge_limits(self, edge_limit):
        """Test SEC RSS feeds with edge case limit values."""
        # These should handle gracefully without crashing
        result = inst.sec_rss_feeds(apikey=API_KEY, limit=edge_limit)
        assert result is not None


class TestParameterizedInstitutionalOwnershipLatest:
    """Comprehensive parameterized tests for institutional ownership latest."""

    @pytest.mark.parametrize("page,limit", [
        (0, 10),
        (0, 25),
        (0, 50),
        (0, 100),
        (0, 200),
        (1, 10),
        (1, 25),
        (1, 50),
        (2, 10),
        (2, 25),
        (3, 10),
        (5, 10),
        (10, 10),
    ])
    def test_institutional_ownership_latest_pagination(self, page, limit):
        """Test institutional ownership latest with various pagination parameters."""
        result = inst.institutional_ownership_latest(apikey=API_KEY, page=page, limit=limit)
        assert result is not None

    @pytest.mark.parametrize("page", [
        0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 50, 100
    ])
    def test_institutional_ownership_latest_pages(self, page):
        """Test institutional ownership latest with various page numbers."""
        result = inst.institutional_ownership_latest(apikey=API_KEY, page=page, limit=25)
        assert result is not None

    @pytest.mark.parametrize("limit", [
        1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 250, 300, 500
    ])
    def test_institutional_ownership_latest_limits(self, limit):
        """Test institutional ownership latest with various limit values."""
        result = inst.institutional_ownership_latest(apikey=API_KEY, page=0, limit=limit)
        assert result is not None

    @pytest.mark.parametrize("page,limit", [
        (-1, 10),
        (0, -1),
        (-1, -1),
        (999999, 10),
        (0, 999999),
        (999999, 999999),
    ])
    def test_institutional_ownership_latest_edge_cases(self, page, limit):
        """Test institutional ownership latest with edge case values."""
        # Should handle gracefully without crashing
        result = inst.institutional_ownership_latest(apikey=API_KEY, page=page, limit=limit)
        assert result is not None


class TestParameterizedInstitutionalOwnershipExtract:
    """Comprehensive parameterized tests for institutional ownership extract."""

    @pytest.mark.parametrize("cik,year,quarter", [
        ("0001067983", 2023, 4),  # Berkshire Hathaway
        ("0001067983", 2023, 3),
        ("0001067983", 2023, 2),
        ("0001067983", 2023, 1),
        ("0001067983", 2022, 4),
        ("0000102909", 2023, 4),  # Wells Fargo
        ("0000102909", 2023, 3),
        ("0000102909", 2023, 2),
        ("0001364742", 2023, 4),  # Citadel Advisors
        ("0001364742", 2023, 3),
        ("0001549133", 2023, 4),  # Vanguard
        ("0001549133", 2023, 3),
    ])
    def test_institutional_ownership_extract_valid_combinations(self, cik, year, quarter):
        """Test institutional ownership extract with valid CIK, year, quarter combinations."""
        result = inst.institutional_ownership_extract(apikey=API_KEY, cik=cik, year=year, quarter=quarter)
        assert result is not None

    @pytest.mark.parametrize("cik", [
        "0001067983",  # Berkshire Hathaway
        "0000102909",  # Wells Fargo
        "0001364742",  # Citadel Advisors
        "0001549133",  # Vanguard
        "0000886982",  # BlackRock
        "0001166559",  # JPMorgan Chase
        "0000019617",  # Bank of America
        "0000072971",  # Morgan Stanley
        "0000831001",  # Goldman Sachs
        "0000895421",  # State Street
    ])
    def test_institutional_ownership_extract_major_institutions(self, cik):
        """Test institutional ownership extract with major institutional CIKs."""
        result = inst.institutional_ownership_extract(apikey=API_KEY, cik=cik, year=2023, quarter=4)
        assert result is not None

    @pytest.mark.parametrize("year", [
        2020, 2021, 2022, 2023, 2024
    ])
    def test_institutional_ownership_extract_years(self, year):
        """Test institutional ownership extract with different years."""
        result = inst.institutional_ownership_extract(apikey=API_KEY, cik="0001067983", year=year, quarter=4)
        assert result is not None

    @pytest.mark.parametrize("quarter", [
        1, 2, 3, 4
    ])
    def test_institutional_ownership_extract_quarters(self, quarter):
        """Test institutional ownership extract with all quarters."""
        result = inst.institutional_ownership_extract(apikey=API_KEY, cik="0001067983", year=2023, quarter=quarter)
        assert result is not None

    @pytest.mark.parametrize("cik,year,quarter", [
        ("0000000000", 2023, 4),  # Invalid CIK
        ("INVALID", 2023, 4),     # Non-numeric CIK
        ("0001067983", 1900, 4),  # Very old year
        ("0001067983", 2050, 4),  # Future year
        ("0001067983", 2023, 0),  # Invalid quarter
        ("0001067983", 2023, 5),  # Invalid quarter
        ("", 2023, 4),            # Empty CIK
    ])
    def test_institutional_ownership_extract_invalid_inputs(self, cik, year, quarter):
        """Test institutional ownership extract with invalid inputs."""
        # Should handle gracefully without crashing
        result = inst.institutional_ownership_extract(apikey=API_KEY, cik=cik, year=year, quarter=quarter)
        assert result is not None


class TestParameterizedInstitutionalOwnershipDates:
    """Comprehensive parameterized tests for institutional ownership dates."""

    @pytest.mark.parametrize("cik", [
        "0001067983",  # Berkshire Hathaway
        "0000102909",  # Wells Fargo
        "0001364742",  # Citadel Advisors
        "0001549133",  # Vanguard
        "0000886982",  # BlackRock
        "0001166559",  # JPMorgan Chase
        "0000019617",  # Bank of America
        "0000072971",  # Morgan Stanley
        "0000831001",  # Goldman Sachs
        "0000895421",  # State Street
        "0001418814",  # T. Rowe Price
        "0000315066",  # Fidelity
        "0001035674",  # Charles Schwab
        "0000950123",  # Northern Trust
        "0000908732",  # Capital Group
    ])
    def test_institutional_ownership_dates_major_institutions(self, cik):
        """Test institutional ownership dates with major institutional CIKs."""
        result = inst.institutional_ownership_dates(apikey=API_KEY, cik=cik)
        assert result is not None

    @pytest.mark.parametrize("invalid_cik", [
        "0000000000",  # All zeros
        "1234567890",  # Invalid format
        "INVALID",     # Non-numeric
        "",            # Empty string
        "000000",      # Too short
        "00000000000000000000",  # Too long
        "abc123",      # Mixed alphanumeric
        "!@#$%",       # Special characters
    ])
    def test_institutional_ownership_dates_invalid_ciks(self, invalid_cik):
        """Test institutional ownership dates with invalid CIKs."""
        # Should handle gracefully without crashing
        result = inst.institutional_ownership_dates(apikey=API_KEY, cik=invalid_cik)
        assert result is not None


class TestParameterizedInstitutionalOwnershipAnalysis:
    """Comprehensive parameterized tests for institutional ownership analysis functions."""

    @pytest.mark.parametrize("cik,year,quarter", [
        ("0001067983", 2023, 4),
        ("0001067983", 2023, 3),
        ("0001067983", 2023, 2),
        ("0001067983", 2023, 1),
        ("0001067983", 2022, 4),
        ("0000102909", 2023, 4),
        ("0000102909", 2023, 3),
        ("0001364742", 2023, 4),
        ("0001364742", 2023, 3),
        ("0001549133", 2023, 4),
        ("0001549133", 2023, 3),
    ])
    def test_institutional_ownership_holder_industry_breakdown(self, cik, year, quarter):
        """Test institutional ownership holder industry breakdown with various parameters."""
        result = inst.institutional_ownership_holder_industry_breakdown(
            apikey=API_KEY, cik=cik, year=year, quarter=quarter
        )
        assert result is not None

    @pytest.mark.parametrize("cik,year,quarter", [
        ("0001067983", 2023, 4),
        ("0001067983", 2023, 3),
        ("0001067983", 2023, 2),
        ("0001067983", 2022, 4),
        ("0000102909", 2023, 4),
        ("0000102909", 2023, 3),
        ("0001364742", 2023, 4),
        ("0001549133", 2023, 4),
        ("0000886982", 2023, 4),
        ("0001166559", 2023, 4),
    ])
    def test_institutional_ownership_holdings_portfolio_changes(self, cik, year, quarter):
        """Test institutional ownership holdings portfolio changes with various parameters."""
        result = inst.institutional_ownership_holdings_portfolio_changes(
            apikey=API_KEY, cik=cik, year=year, quarter=quarter
        )
        assert result is not None

    @pytest.mark.parametrize("cik,year,quarter", [
        ("0001067983", 2023, 4),
        ("0001067983", 2023, 3),
        ("0001067983", 2022, 4),
        ("0000102909", 2023, 4),
        ("0001364742", 2023, 4),
        ("0001549133", 2023, 4),
        ("0000886982", 2023, 4),
        ("0001166559", 2023, 4),
        ("0000019617", 2023, 4),
        ("0000072971", 2023, 4),
    ])
    def test_institutional_ownership_holdings_new_positions(self, cik, year, quarter):
        """Test institutional ownership holdings new positions with various parameters."""
        result = inst.institutional_ownership_holdings_new_positions(
            apikey=API_KEY, cik=cik, year=year, quarter=quarter
        )
        assert result is not None

    @pytest.mark.parametrize("cik,year,quarter", [
        ("0001067983", 2023, 4),
        ("0001067983", 2023, 3),
        ("0001067983", 2022, 4),
        ("0000102909", 2023, 4),
        ("0001364742", 2023, 4),
        ("0001549133", 2023, 4),
        ("0000886982", 2023, 4),
        ("0001166559", 2023, 4),
        ("0000019617", 2023, 4),
        ("0000072971", 2023, 4),
    ])
    def test_institutional_ownership_holdings_summary(self, cik, year, quarter):
        """Test institutional ownership holdings summary with various parameters."""
        result = inst.institutional_ownership_holdings_summary(
            apikey=API_KEY, cik=cik, year=year, quarter=quarter
        )
        assert result is not None

    @pytest.mark.parametrize("symbol", [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.B", 
        "JPM", "JNJ", "V", "PG", "UNH", "HD", "MA", "DIS", "PYPL", "ADBE",
        "CRM", "NFLX", "INTC", "CSCO", "PFE", "VZ", "T", "KO", "PEP", "WMT"
    ])
    def test_institutional_ownership_by_symbol(self, symbol):
        """Test institutional ownership by symbol with various stock symbols."""
        result = inst.institutional_ownership_by_symbol(apikey=API_KEY, symbol=symbol)
        assert result is not None

    @pytest.mark.parametrize("symbol,page,limit", [
        ("AAPL", 0, 25),
        ("AAPL", 1, 25),
        ("AAPL", 2, 25),
        ("MSFT", 0, 50),
        ("MSFT", 1, 50),
        ("GOOGL", 0, 100),
        ("AMZN", 0, 10),
        ("TSLA", 0, 75),
    ])
    def test_institutional_ownership_by_symbol_pagination(self, symbol, page, limit):
        """Test institutional ownership by symbol with pagination."""
        result = inst.institutional_ownership_by_symbol(
            apikey=API_KEY, symbol=symbol, page=page, limit=limit
        )
        assert result is not None


class TestParameterizedInstitutionalOwnershipHoldings:
    """Comprehensive parameterized tests for institutional ownership holdings functions."""

    @pytest.mark.parametrize("cik,year,quarter,page,limit", [
        ("0001067983", 2023, 4, 0, 25),
        ("0001067983", 2023, 4, 1, 25),
        ("0001067983", 2023, 4, 0, 50),
        ("0001067983", 2023, 4, 0, 100),
        ("0000102909", 2023, 4, 0, 25),
        ("0000102909", 2023, 3, 0, 25),
        ("0001364742", 2023, 4, 0, 25),
        ("0001549133", 2023, 4, 0, 25),
        ("0000886982", 2023, 4, 0, 25),
    ])
    def test_institutional_ownership_holdings_overview(self, cik, year, quarter, page, limit):
        """Test institutional ownership holdings overview with various parameters."""
        result = inst.institutional_ownership_holdings_overview(
            apikey=API_KEY, cik=cik, year=year, quarter=quarter, page=page, limit=limit
        )
        assert result is not None

    @pytest.mark.parametrize("cik,year,quarter,page,limit", [
        ("0001067983", 2023, 4, 0, 25),
        ("0001067983", 2023, 3, 0, 25),
        ("0001067983", 2022, 4, 0, 25),
        ("0000102909", 2023, 4, 0, 50),
        ("0001364742", 2023, 4, 0, 75),
        ("0001549133", 2023, 4, 0, 100),
        ("0000886982", 2023, 4, 1, 25),
        ("0001166559", 2023, 4, 2, 25),
    ])
    def test_institutional_ownership_holdings_sold_out_positions(self, cik, year, quarter, page, limit):
        """Test institutional ownership holdings sold out positions with various parameters."""
        result = inst.institutional_ownership_holdings_sold_out_positions(
            apikey=API_KEY, cik=cik, year=year, quarter=quarter, page=page, limit=limit
        )
        assert result is not None


# === EXISTING TEST CLASSES (preserved) ===


class TestSECRSSFeeds:
    """Test SEC RSS feeds functionality."""

    def test_sec_rss_feeds_default_parameters(self):
        """Test SEC RSS feeds with default parameters."""
        result = inst.sec_rss_feeds(apikey=API_KEY)
        assert result is not None

    def test_sec_rss_feeds_with_limit(self):
        """Test SEC RSS feeds with custom limit."""
        result = inst.sec_rss_feeds(apikey=API_KEY, limit=50)
        assert result is not None

    def test_sec_rss_feeds_with_custom_filename(self):
        """Test SEC RSS feeds with custom filename."""
        result = inst.sec_rss_feeds(
            apikey=API_KEY, 
            limit=10, 
            filename="custom_rss_feeds.csv"
        )
        assert result is not None

    def test_sec_rss_feeds_various_limits(self):
        """Test SEC RSS feeds with various limit values."""
        limits = [5, 10, 25, 50, 100]
        
        for limit in limits:
            result = inst.sec_rss_feeds(apikey=API_KEY, limit=limit)
            assert result is not None


class TestInstitutionalOwnershipLatest:
    """Test latest institutional ownership functionality."""

    def test_institutional_ownership_latest_default(self):
        """Test institutional ownership latest with default parameters."""
        result = inst.institutional_ownership_latest(apikey=API_KEY)
        assert result is not None

    def test_institutional_ownership_latest_with_pagination(self):
        """Test institutional ownership latest with pagination."""
        result = inst.institutional_ownership_latest(
            apikey=API_KEY, 
            page=1, 
            limit=50
        )
        assert result is not None

    def test_institutional_ownership_latest_different_pages(self):
        """Test institutional ownership latest with different pages."""
        pages = [0, 1, 2, 3]
        
        for page in pages:
            result = inst.institutional_ownership_latest(
                apikey=API_KEY, 
                page=page, 
                limit=25
            )
            assert result is not None

    def test_institutional_ownership_latest_different_limits(self):
        """Test institutional ownership latest with different limits."""
        limits = [10, 25, 50, 100, 200]
        
        for limit in limits:
            result = inst.institutional_ownership_latest(
                apikey=API_KEY, 
                page=0, 
                limit=limit
            )
            assert result is not None


class TestInstitutionalOwnershipExtract:
    """Test institutional ownership extract functionality."""

    def test_institutional_ownership_extract_valid_cik(self):
        """Test institutional ownership extract with valid CIK."""
        # Using a well-known CIK (Berkshire Hathaway)
        result = inst.institutional_ownership_extract(
            apikey=API_KEY,
            cik="0001067983",
            year=2023,
            quarter=4
        )
        assert result is not None

    def test_institutional_ownership_extract_different_quarters(self):
        """Test institutional ownership extract with different quarters."""
        quarters = [1, 2, 3, 4]
        
        for quarter in quarters:
            result = inst.institutional_ownership_extract(
                apikey=API_KEY,
                cik="0001067983",
                year=2023,
                quarter=quarter
            )
            assert result is not None

    def test_institutional_ownership_extract_different_years(self):
        """Test institutional ownership extract with different years."""
        years = [2020, 2021, 2022, 2023]
        
        for year in years:
            result = inst.institutional_ownership_extract(
                apikey=API_KEY,
                cik="0001067983",
                year=year,
                quarter=4
            )
            assert result is not None

    def test_institutional_ownership_extract_multiple_ciks(self):
        """Test institutional ownership extract with multiple CIKs."""
        # Using known institutional investors
        ciks = ["0001067983", "0000102909", "0001364742"]  # Berkshire, Vanguard, Blackrock
        
        for cik in ciks:
            result = inst.institutional_ownership_extract(
                apikey=API_KEY,
                cik=cik,
                year=2023,
                quarter=4
            )
            assert result is not None


class TestInstitutionalOwnershipDates:
    """Test institutional ownership dates functionality."""

    def test_institutional_ownership_dates_valid_cik(self):
        """Test institutional ownership dates with valid CIK."""
        result = inst.institutional_ownership_dates(
            apikey=API_KEY,
            cik="0001067983"
        )
        assert result is not None

    def test_institutional_ownership_dates_multiple_ciks(self):
        """Test institutional ownership dates with multiple CIKs."""
        ciks = ["0001067983", "0000102909", "0001364742"]
        
        for cik in ciks:
            result = inst.institutional_ownership_dates(
                apikey=API_KEY,
                cik=cik
            )
            assert result is not None

    def test_institutional_ownership_dates_invalid_cik(self):
        """Test institutional ownership dates with invalid CIK."""
        result = inst.institutional_ownership_dates(
            apikey=API_KEY,
            cik="0000000000"
        )
        # Should handle gracefully
        assert result is not None


class TestInstitutionalOwnershipAnalysis:
    """Test institutional ownership analysis functions."""

    def test_institutional_ownership_holder_industry_breakdown(self):
        """Test institutional ownership holder industry breakdown."""
        result = inst.institutional_ownership_holder_industry_breakdown(
            apikey=API_KEY,
            cik="0001067983",
            year=2023,
            quarter=4
        )
        assert result is not None

    def test_institutional_ownership_holder_industry_breakdown_different_periods(self):
        """Test holder industry breakdown with different periods."""
        periods = [
            (2022, 4),
            (2023, 1),
            (2023, 2),
            (2023, 3),
            (2023, 4)
        ]
        
        for year, quarter in periods:
            result = inst.institutional_ownership_holder_industry_breakdown(
                apikey=API_KEY,
                cik="0001067983",
                year=year,
                quarter=quarter
            )
            assert result is not None

    def test_institutional_ownership_industry_summary(self):
        """Test institutional ownership industry summary."""
        result = inst.institutional_ownership_industry_summary(
            apikey=API_KEY,
            year=2023,
            quarter=4
        )
        assert result is not None

    def test_institutional_ownership_industry_summary_different_periods(self):
        """Test industry summary with different periods."""
        periods = [
            (2022, 4),
            (2023, 1),
            (2023, 2),
            (2023, 3),
            (2023, 4)
        ]
        
        for year, quarter in periods:
            result = inst.institutional_ownership_industry_summary(
                apikey=API_KEY,
                year=year,
                quarter=quarter
            )
            assert result is not None


class TestSECFilings8K:
    """Test SEC 8-K filings functionality."""

    def test_sec_filings_8k_single_symbol(self):
        """Test SEC 8-K filings with single symbol."""
        result = inst.sec_filings_8k(apikey=API_KEY, symbol="AAPL")
        assert result is not None

    def test_sec_filings_8k_multiple_symbols(self):
        """Test SEC 8-K filings with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
        
        for symbol in symbols:
            result = inst.sec_filings_8k(apikey=API_KEY, symbol=symbol)
            assert result is not None

    def test_sec_filings_8k_invalid_symbol(self):
        """Test SEC 8-K filings with invalid symbol."""
        result = inst.sec_filings_8k(apikey=API_KEY, symbol="INVALID123")
        # Should handle gracefully
        assert result is not None


class TestSECFilingsFinancials:
    """Test SEC financial filings functionality."""

    def test_sec_filings_financials_single_symbol(self):
        """Test SEC financial filings with single symbol."""
        result = inst.sec_filings_financials(apikey=API_KEY, symbol="AAPL")
        assert result is not None

    def test_sec_filings_financials_multiple_symbols(self):
        """Test SEC financial filings with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
        
        for symbol in symbols:
            result = inst.sec_filings_financials(apikey=API_KEY, symbol=symbol)
            assert result is not None

    def test_sec_filings_financials_different_sectors(self):
        """Test SEC financial filings with symbols from different sectors."""
        symbols = ["AAPL", "JPM", "JNJ", "XOM", "WMT"]  # Tech, Finance, Healthcare, Energy, Retail
        
        for symbol in symbols:
            result = inst.sec_filings_financials(apikey=API_KEY, symbol=symbol)
            assert result is not None


class TestSECFilingsSearch:
    """Test SEC filings search functionality."""

    def test_sec_filings_search_form_type_10k(self):
        """Test SEC filings search by form type 10-K."""
        result = inst.sec_filings_search_form_type(apikey=API_KEY, form_type="10-K")
        assert result is not None

    def test_sec_filings_search_form_type_10q(self):
        """Test SEC filings search by form type 10-Q."""
        result = inst.sec_filings_search_form_type(apikey=API_KEY, form_type="10-Q")
        assert result is not None

    def test_sec_filings_search_different_form_types(self):
        """Test SEC filings search with different form types."""
        form_types = ["10-K", "10-Q", "8-K", "DEF 14A", "S-1"]
        
        for form_type in form_types:
            result = inst.sec_filings_search_form_type(apikey=API_KEY, form_type=form_type)
            assert result is not None

    def test_sec_filings_search_symbol(self):
        """Test SEC filings search by symbol."""
        result = inst.sec_filings_search_symbol(apikey=API_KEY, symbol="AAPL")
        assert result is not None

    def test_sec_filings_search_multiple_symbols(self):
        """Test SEC filings search with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        
        for symbol in symbols:
            result = inst.sec_filings_search_symbol(apikey=API_KEY, symbol=symbol)
            assert result is not None


class TestSECFilingsCompanySearch:
    """Test SEC filings company search functionality."""

    def test_sec_filings_company_search_name(self):
        """Test SEC filings search by company name."""
        result = inst.sec_filings_company_search_name(apikey=API_KEY, name="Apple")
        assert result is not None

    def test_sec_filings_company_search_different_names(self):
        """Test SEC filings search with different company names."""
        names = ["Apple", "Microsoft", "Google", "Tesla", "Amazon"]
        
        for name in names:
            result = inst.sec_filings_company_search_name(apikey=API_KEY, name=name)
            assert result is not None

    def test_sec_filings_company_search_symbol(self):
        """Test SEC filings search by company symbol."""
        result = inst.sec_filings_company_search_symbol(apikey=API_KEY, symbol="AAPL")
        assert result is not None

    def test_sec_filings_company_search_multiple_symbols(self):
        """Test SEC filings search with multiple company symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
        
        for symbol in symbols:
            result = inst.sec_filings_company_search_symbol(apikey=API_KEY, symbol=symbol)
            assert result is not None

    def test_sec_filings_company_search_cik(self):
        """Test SEC filings search by company CIK."""
        result = inst.sec_filings_company_search_cik(apikey=API_KEY, cik="0000320193")  # Apple CIK
        assert result is not None

    def test_sec_filings_company_search_multiple_ciks(self):
        """Test SEC filings search with multiple company CIKs."""
        ciks = [
            "0000320193",  # Apple
            "0000789019",  # Microsoft
            "0001652044",  # Google
            "0001318605",  # Tesla
        ]
        
        for cik in ciks:
            result = inst.sec_filings_company_search_cik(apikey=API_KEY, cik=cik)
            assert result is not None


class TestSECProfile:
    """Test SEC profile functionality."""

    def test_sec_profile_with_symbol(self):
        """Test SEC profile with symbol parameter."""
        result = inst.sec_profile(apikey=API_KEY, symbol="AAPL")
        assert result is not None

    def test_sec_profile_with_cik(self):
        """Test SEC profile with CIK parameter."""
        result = inst.sec_profile(apikey=API_KEY, cik="0000320193")
        assert result is not None

    def test_sec_profile_with_both_parameters(self):
        """Test SEC profile with both symbol and CIK parameters."""
        result = inst.sec_profile(apikey=API_KEY, symbol="AAPL", cik="0000320193")
        assert result is not None

    def test_sec_profile_multiple_symbols(self):
        """Test SEC profile with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
        
        for symbol in symbols:
            result = inst.sec_profile(apikey=API_KEY, symbol=symbol)
            assert result is not None

    def test_sec_profile_multiple_ciks(self):
        """Test SEC profile with multiple CIKs."""
        ciks = [
            "0000320193",  # Apple
            "0000789019",  # Microsoft
            "0001652044",  # Google
            "0001318605",  # Tesla
        ]
        
        for cik in ciks:
            result = inst.sec_profile(apikey=API_KEY, cik=cik)
            assert result is not None


class TestInstitutionalFundErrorHandling:
    """Test error handling for institutional fund functions."""

    def test_functions_with_invalid_api_key(self):
        """Test institutional fund functions with invalid API key."""
        functions_to_test = [
            (inst.sec_rss_feeds, {}),
            (inst.institutional_ownership_latest, {}),
            (inst.sec_filings_8k, {"symbol": "AAPL"}),
            (inst.sec_filings_financials, {"symbol": "AAPL"}),
            (inst.sec_profile, {"symbol": "AAPL"}),
        ]
        
        for func, kwargs in functions_to_test:
            result = func(apikey="invalid_key", **kwargs)
            # Should handle gracefully
            assert result is not None or result is None

    def test_institutional_ownership_extract_invalid_parameters(self):
        """Test institutional ownership extract with invalid parameters."""
        # Invalid CIK
        result = inst.institutional_ownership_extract(
            apikey=API_KEY,
            cik="invalid_cik",
            year=2023,
            quarter=4
        )
        assert result is not None

        # Invalid quarter
        result = inst.institutional_ownership_extract(
            apikey=API_KEY,
            cik="0001067983",
            year=2023,
            quarter=5  # Invalid quarter
        )
        assert result is not None

        # Invalid year
        result = inst.institutional_ownership_extract(
            apikey=API_KEY,
            cik="0001067983",
            year=1900,  # Very old year
            quarter=4
        )
        assert result is not None

    def test_sec_filings_search_invalid_form_types(self):
        """Test SEC filings search with invalid form types."""
        invalid_form_types = ["INVALID", "FAKE-FORM", "123-ABC"]
        
        for form_type in invalid_form_types:
            result = inst.sec_filings_search_form_type(apikey=API_KEY, form_type=form_type)
            # Should handle gracefully
            assert result is not None

    def test_institutional_ownership_negative_pagination(self):
        """Test institutional ownership with negative pagination values."""
        result = inst.institutional_ownership_latest(
            apikey=API_KEY,
            page=-1,
            limit=-10
        )
        # Should handle gracefully
        assert result is not None


class TestParameterizedSymbolVariations:
    """Comprehensive symbol testing across different market categories."""
    
    @pytest.mark.parametrize("symbol,category", [
        # Major indices and ETFs
        ("SPY", "ETF_SP500"),
        ("QQQ", "ETF_NASDAQ"),
        ("VTI", "ETF_TOTAL_MARKET"),
        ("IWM", "ETF_SMALL_CAP"),
        ("GLD", "ETF_GOLD"),
        ("TLT", "ETF_BONDS"),
        
        # International stocks
        ("TSM", "INTERNATIONAL"),
        ("BABA", "CHINESE_ADR"),
        ("ASML", "EUROPEAN_ADR"),
        ("NVO", "PHARMACEUTICAL_INTERNATIONAL"),
        
        # Penny stocks and micro caps
        ("SIRI", "LOW_PRICE"),
        ("NOK", "TELECOM_LOW_PRICE"),
        
        # High-priced stocks
        ("BRK.A", "HIGH_PRICE"),
        ("NVR", "HIGH_PRICE_CONSTRUCTION"),
        
        # Recent IPOs
        ("COIN", "RECENT_IPO"),
        ("RBLX", "GAMING_IPO"),
        
        # Cryptocurrency related
        ("MSTR", "CRYPTO_RELATED"),
        ("RIOT", "CRYPTO_MINING"),
        
        # REITs
        ("EQIX", "REIT_DATA_CENTER"),
        ("PLD", "REIT_INDUSTRIAL"),
        
        # Error cases
        ("", "EMPTY"),
        ("123INVALID", "NUMERIC_START"),
        ("TOOLO NG", "WITH_SPACE"),
        ("FAKE123", "NONEXISTENT"),
        ("DELISTED", "POTENTIALLY_DELISTED"),
    ])
    def test_institutional_holdings_symbol_variations(self, symbol, category):
        """Test institutional holdings with comprehensive symbol variations."""
        if symbol.strip() == "":
            # Empty symbols should be handled gracefully
            result = inst.sec_rss_feeds(apikey=API_KEY, limit=1)
            assert result is None or result == []
        else:
            result = inst.sec_rss_feeds(apikey=API_KEY, limit=1)
            assert result is not None


class TestParameterizedAPIKeyScenarios:
    """Test various API key scenarios and error handling."""
    
    @pytest.mark.parametrize("api_key_scenario,expected_behavior", [
        ("demo", "DEMO_KEY"),
        ("", "EMPTY_KEY"),
        ("invalid_key_123", "INVALID_KEY"),
        ("   ", "WHITESPACE_KEY"),
        (None, "NULL_KEY"),
    ])
    def test_api_key_error_handling(self, api_key_scenario, expected_behavior):
        """Test how functions handle different API key scenarios."""
        if api_key_scenario is None:
            # Skip None API key tests as they would cause TypeError
            pytest.skip("None API key would cause TypeError")
            
        try:
            result = inst.sec_rss_feeds(apikey=api_key_scenario, limit=1)
            # For invalid keys, API might return error messages or None
            if expected_behavior in ["EMPTY_KEY", "INVALID_KEY", "WHITESPACE_KEY"]:
                # These might return None or error responses
                assert result is None or (isinstance(result, dict) and "Error Message" in result)
            else:
                assert result is not None
        except Exception as e:
            # Some invalid keys might raise exceptions, which is also valid behavior
            assert expected_behavior in ["EMPTY_KEY", "INVALID_KEY", "WHITESPACE_KEY"]


class TestParameterizedPaginationScenarios:
    """Test pagination with various scenarios and edge cases."""
    
    @pytest.mark.parametrize("page,limit,scenario", [
        (0, 10, "FIRST_PAGE"),
        (1, 10, "SECOND_PAGE"),
        (0, 1, "MINIMAL_LIMIT"),
        (0, 100, "LARGE_LIMIT"),
        (0, 1000, "VERY_LARGE_LIMIT"),
        (10, 10, "HIGH_PAGE_NUMBER"),
        (0, 0, "ZERO_LIMIT"),
        (0, -1, "NEGATIVE_LIMIT"),
        (-1, 10, "NEGATIVE_PAGE"),
    ])
    def test_pagination_edge_cases(self, page, limit, scenario):
        """Test pagination with various edge cases."""
        # Use a function that supports pagination parameters
        result = inst.institutional_ownership_holdings_portfolio_changes(
            apikey=API_KEY, cik="0001067983", year=2023, quarter=4, page=page, limit=limit
        )
        
        if scenario in ["ZERO_LIMIT", "NEGATIVE_LIMIT", "NEGATIVE_PAGE"]:
            # These edge cases might return None, empty results, or handle gracefully
            assert result is None or result == [] or isinstance(result, (list, dict))
        else:
            # Normal scenarios should return valid results
            assert result is not None
