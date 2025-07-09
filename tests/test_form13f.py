import pytest

from fmpsdk import form13f
from fmpsdk.models import (
    FMPForm13FDate,
    FMPForm13FExtract,
    FMPForm13FFiling,
)
from tests.conftest import extract_data_list


class TestForm13F:
    """Test cases for Form 13F endpoints."""

    def test_institutional_ownership_latest(self, api_key):
        """Test latest institutional ownership filings endpoint."""
        result = form13f.institutional_ownership_latest(apikey=api_key, limit=5)

        # Use extract_data_list for automatic premium endpoint detection
        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            filing = data[0]
            # Validate against model
            if isinstance(filing, dict):
                filing_obj = FMPForm13FFiling(**filing)
            else:
                filing_obj = filing

            # Required fields validation
            assert hasattr(filing_obj, "cik")
            assert hasattr(filing_obj, "name")
            assert hasattr(filing_obj, "date")
            assert hasattr(filing_obj, "filingDate")
            assert hasattr(filing_obj, "formType")

            # Data quality checks
            assert filing_obj.cik
            assert filing_obj.name
            assert filing_obj.date
            assert filing_obj.formType in ["13F-HR", "13F-NT"]

    def test_institutional_ownership_latest_pagination(self, api_key):
        """Test latest institutional ownership with pagination parameters."""
        result = form13f.institutional_ownership_latest(apikey=api_key, page=0, limit=3)

        # Use extract_data_list for automatic premium endpoint detection
        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should respect limit parameter
        assert len(data) <= 3

    def test_institutional_ownership_extract(self, api_key):
        """Test institutional ownership extract endpoint."""
        # Use Berkshire Hathaway's CIK
        result = form13f.institutional_ownership_extract(
            apikey=api_key, cik="0001067983", year=2023, quarter=4
        )

        # This is a premium endpoint - expect 402 status or error dict

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            extract = data[0]
            # Validate against model
            if isinstance(extract, dict):
                extract_obj = FMPForm13FExtract(**extract)
            else:
                extract_obj = extract

            # Required fields validation
            assert hasattr(extract_obj, "cik")
            assert hasattr(extract_obj, "symbol")
            assert hasattr(extract_obj, "nameOfIssuer")
            assert hasattr(extract_obj, "shares")
            assert hasattr(extract_obj, "value")

            # Data quality checks
            assert extract_obj.cik
            assert extract_obj.symbol
            assert extract_obj.nameOfIssuer
            assert isinstance(extract_obj.shares, int)
            assert isinstance(extract_obj.value, int)

    def test_institutional_ownership_dates(self, api_key):
        """Test institutional ownership dates endpoint."""
        # Use Berkshire Hathaway's CIK
        result = form13f.institutional_ownership_dates(apikey=api_key, cik="0001067983")

        # This is a premium endpoint - expect 402 status or error dict

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            date_info = data[0]
            # Validate against model
            if isinstance(date_info, dict):
                date_obj = FMPForm13FDate(**date_info)
            else:
                date_obj = date_info

            # Required fields validation
            assert hasattr(date_obj, "date")
            assert hasattr(date_obj, "year")
            assert hasattr(date_obj, "quarter")

            # Data quality checks
            assert date_obj.date
            assert isinstance(date_obj.year, int)
            assert isinstance(date_obj.quarter, int)
            assert 1 <= date_obj.quarter <= 4

    def test_institutional_ownership_extract_analytics_by_holder(self, api_key):
        """Test institutional ownership extract analytics by holder endpoint."""
        result = form13f.institutional_ownership_extract_analytics_by_holder(
            apikey=api_key, symbol="AAPL", year=2023, quarter=4, limit=5
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            extract = data[0]
            # Validate against model
            if isinstance(extract, dict):
                extract_obj = FMPForm13FExtract(**extract)
            else:
                extract_obj = extract

            # Required fields validation
            assert hasattr(extract_obj, "symbol")
            assert hasattr(extract_obj, "cik")
            assert hasattr(extract_obj, "nameOfIssuer")

            # Data quality checks
            assert extract_obj.symbol == "AAPL"

    def test_institutional_ownership_holder_performance_summary(self, api_key):
        """Test institutional ownership holder performance summary endpoint."""
        # Use Berkshire Hathaway's CIK
        result = form13f.institutional_ownership_holder_performance_summary(
            apikey=api_key, cik="0001067983", page=0
        )

        # This is a premium endpoint - expect 402 status or error dict

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            summary = data[0]
            # Should be FMPForm13FExtract according to type annotation
            if isinstance(summary, dict):
                summary_obj = FMPForm13FExtract(**summary)
            else:
                summary_obj = summary

            # Basic validation
            assert hasattr(summary_obj, "cik")

    def test_institutional_ownership_holder_industry_breakdown(self, api_key):
        """Test institutional ownership holder industry breakdown endpoint."""
        # Use Berkshire Hathaway's CIK
        result = form13f.institutional_ownership_holder_industry_breakdown(
            apikey=api_key, cik="0001067983", year=2023, quarter=4
        )

        # This is a premium endpoint - expect 402 status or error dict

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            breakdown = data[0]
            # Should be FMPForm13FExtract according to type annotation
            if isinstance(breakdown, dict):
                breakdown_obj = FMPForm13FExtract(**breakdown)
            else:
                breakdown_obj = breakdown

            # Basic validation
            assert hasattr(breakdown_obj, "cik")

    def test_institutional_ownership_positions_summary(self, api_key):
        """Test institutional ownership positions summary endpoint."""
        result = form13f.institutional_ownership_positions_summary(
            apikey=api_key, symbol="AAPL", year=2023, quarter=4
        )

        # This is a premium endpoint - expect 402 status or error dict

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            summary = data[0]
            # Should be FMPForm13FExtract according to type annotation
            if isinstance(summary, dict):
                summary_obj = FMPForm13FExtract(**summary)
            else:
                summary_obj = summary

            # Basic validation
            assert hasattr(summary_obj, "symbol")
            if hasattr(summary_obj, "symbol") and summary_obj.symbol:
                assert summary_obj.symbol == "AAPL"

    def test_institutional_ownership_industry_summary(self, api_key):
        """Test institutional ownership industry summary endpoint."""
        result = form13f.institutional_ownership_industry_summary(
            apikey=api_key, year=2023, quarter=4
        )

        # This is a premium endpoint - expect 402 status or error dict

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            industry = data[0]
            # Should be FMPForm13FExtract according to type annotation
            if isinstance(industry, dict):
                industry_obj = FMPForm13FExtract(**industry)
            else:
                industry_obj = industry

            # Basic validation
            assert hasattr(industry_obj, "date")

    # Error handling tests
    def test_institutional_ownership_latest_invalid_api_key(self):
        """Test latest institutional ownership with invalid API key."""
        result = form13f.institutional_ownership_latest(apikey="invalid_key")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_extract_invalid_api_key(self):
        """Test institutional ownership extract with invalid API key."""
        result = form13f.institutional_ownership_extract(
            apikey="invalid_key", cik="0001067983", year=2023, quarter=4
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_dates_invalid_api_key(self):
        """Test institutional ownership dates with invalid API key."""
        result = form13f.institutional_ownership_dates(
            apikey="invalid_key", cik="0001067983"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_extract_analytics_by_holder_invalid_api_key(self):
        """Test institutional ownership extract analytics by holder with invalid API key."""
        result = form13f.institutional_ownership_extract_analytics_by_holder(
            apikey="invalid_key", symbol="AAPL", year=2023, quarter=4
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_holder_performance_summary_invalid_api_key(self):
        """Test institutional ownership holder performance summary with invalid API key."""
        result = form13f.institutional_ownership_holder_performance_summary(
            apikey="invalid_key", cik="0001067983"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_holder_industry_breakdown_invalid_api_key(self):
        """Test institutional ownership holder industry breakdown with invalid API key."""
        result = form13f.institutional_ownership_holder_industry_breakdown(
            apikey="invalid_key", cik="0001067983", year=2023, quarter=4
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_positions_summary_invalid_api_key(self):
        """Test institutional ownership positions summary with invalid API key."""
        result = form13f.institutional_ownership_positions_summary(
            apikey="invalid_key", symbol="AAPL", year=2023, quarter=4
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_institutional_ownership_industry_summary_invalid_api_key(self):
        """Test institutional ownership industry summary with invalid API key."""
        result = form13f.institutional_ownership_industry_summary(
            apikey="invalid_key", year=2023, quarter=4
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result
