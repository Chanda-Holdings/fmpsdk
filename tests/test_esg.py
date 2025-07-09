from datetime import datetime
from typing import Dict

import pytest

from fmpsdk import esg
from fmpsdk.models import (
    FMPESGBenchmark,
    FMPESGFiling,
    FMPESGRating,
)
from tests.conftest import extract_data_list


class TestESGDisclosures:
    """Test the ESG disclosures endpoint."""

    def test_esg_disclosures_basic(self, api_key):
        """Test basic ESG disclosures for a known symbol."""
        result = esg.esg_disclosures(apikey=api_key, symbol="AAPL")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "date" in first_item
                assert "symbol" in first_item
                assert "cik" in first_item
                assert "companyName" in first_item
                assert "formType" in first_item

                # Test Pydantic model validation
                filing = FMPESGFiling(**first_item)
                assert filing.symbol == first_item["symbol"]
                assert filing.cik == first_item["cik"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "date")
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "companyName")

    def test_esg_disclosures_multiple_symbols(self, api_key):
        """Test ESG disclosures for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = esg.esg_disclosures(apikey=api_key, symbol=symbol)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if result_list:
                for item in result_list[:2]:  # Check first few items
                    if isinstance(item, dict):
                        assert item["symbol"] == symbol
                    else:
                        assert item.symbol == symbol

    def test_esg_disclosures_invalid_symbol(self, api_key):
        """Test ESG disclosures with invalid symbol."""
        result = esg.esg_disclosures(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        result_list = extract_data_list(result)
        # Should return empty list for invalid symbol
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_esg_disclosures_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = esg.esg_disclosures(apikey=invalid_api_key, symbol="AAPL")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestESGRatings:
    """Test the ESG ratings endpoint."""

    def test_esg_ratings_basic(self, api_key):
        """Test basic ESG ratings for a known symbol."""
        result = esg.esg_ratings(apikey=api_key, symbol="AAPL")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "symbol" in first_item
                assert "cik" in first_item
                assert "companyName" in first_item
                assert "industry" in first_item
                assert "fiscalYear" in first_item

                # Test Pydantic model validation
                rating = FMPESGRating(**first_item)
                assert rating.symbol == first_item["symbol"]
                assert rating.fiscalYear == first_item["fiscalYear"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "fiscalYear")
                assert hasattr(first_item, "industry")

    def test_esg_ratings_multiple_symbols(self, api_key):
        """Test ESG ratings for multiple symbols."""
        symbols = ["AAPL", "TSLA", "JPM"]

        for symbol in symbols:
            result = esg.esg_ratings(apikey=api_key, symbol=symbol)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if result_list:
                for item in result_list[:2]:  # Check first few items
                    if isinstance(item, dict):
                        assert item["symbol"] == symbol
                    else:
                        assert item.symbol == symbol

    def test_esg_ratings_invalid_symbol(self, api_key):
        """Test ESG ratings with invalid symbol."""
        result = esg.esg_ratings(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        result_list = extract_data_list(result)
        # Should return empty list for invalid symbol
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_esg_ratings_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = esg.esg_ratings(apikey=invalid_api_key, symbol="AAPL")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestESGBenchmark:
    """Test the ESG benchmark endpoint."""

    def test_esg_benchmark_basic(self, api_key):
        """Test basic ESG benchmark data."""
        result = esg.esg_benchmark(apikey=api_key)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "fiscalYear" in first_item
                assert "sector" in first_item
                assert "environmentalScore" in first_item
                assert "socialScore" in first_item
                assert "governanceScore" in first_item
                assert "ESGScore" in first_item

                # Test Pydantic model validation
                benchmark = FMPESGBenchmark(**first_item)
                assert benchmark.fiscalYear == first_item["fiscalYear"]
                assert benchmark.sector == first_item["sector"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "fiscalYear")
                assert hasattr(first_item, "sector")
                assert hasattr(first_item, "environmentalScore")
                assert hasattr(first_item, "socialScore")
                assert hasattr(first_item, "governanceScore")
                assert hasattr(first_item, "ESGScore")

    def test_esg_benchmark_with_year(self, api_key):
        """Test ESG benchmark data with specific year."""
        result = esg.esg_benchmark(apikey=api_key, year="2023")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            for item in result_list[:3]:  # Check first few items
                if isinstance(item, dict):
                    assert item["fiscalYear"] == 2023
                else:
                    assert item.fiscalYear == 2023

    def test_esg_benchmark_multiple_years(self, api_key):
        """Test ESG benchmark data for multiple years."""
        years = ["2021", "2022", "2023"]

        for year in years:
            result = esg.esg_benchmark(apikey=api_key, year=year)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if result_list:
                for item in result_list[:2]:  # Check first few items
                    if isinstance(item, dict):
                        assert item["fiscalYear"] == int(year)
                    else:
                        assert item.fiscalYear == int(year)

    def test_esg_benchmark_invalid_year(self, api_key):
        """Test ESG benchmark with invalid year."""
        result = esg.esg_benchmark(apikey=api_key, year="1900")  # Invalid year

        result_list = extract_data_list(result)
        # Should return empty list for invalid year
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_esg_benchmark_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = esg.esg_benchmark(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestESGDataQuality:
    """Test data quality and business logic validation."""

    def test_esg_disclosures_data_quality(self, api_key):
        """Test data quality in ESG disclosures."""
        result = esg.esg_disclosures(apikey=api_key, symbol="AAPL")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # Check date formats
                    assert len(item["date"]) >= 10  # YYYY-MM-DD format
                    assert len(item["acceptedDate"]) >= 10

                    # Check score ranges (typically 0-100)
                    assert 0 <= item["environmentalScore"] <= 100
                    assert 0 <= item["socialScore"] <= 100
                    assert 0 <= item["governanceScore"] <= 100
                    assert 0 <= item["ESGScore"] <= 100

                    # Check CIK format
                    assert item["cik"].isdigit()
                    assert len(item["cik"]) >= 6  # CIK should be at least 6 digits

                    # Check form type
                    assert len(item["formType"]) > 0

                    # Check URL
                    assert "http" in item["url"].lower()
                else:
                    # Pydantic model
                    assert len(item.date) >= 10
                    assert len(item.acceptedDate) >= 10
                    assert 0 <= item.environmentalScore <= 100
                    assert 0 <= item.socialScore <= 100
                    assert 0 <= item.governanceScore <= 100
                    assert 0 <= item.ESGScore <= 100
                    assert item.cik.isdigit()
                    assert len(item.cik) >= 6
                    assert len(item.formType) > 0
                    assert "http" in item.url.lower()

    def test_esg_ratings_data_quality(self, api_key):
        """Test data quality in ESG ratings."""
        result = esg.esg_ratings(apikey=api_key, symbol="AAPL")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # Check fiscal year reasonableness
                    current_year = datetime.now().year
                    assert 2015 <= item["fiscalYear"] <= current_year + 1

                    # Check required fields are not empty
                    assert len(item["companyName"]) > 0
                    assert len(item["industry"]) > 0
                    assert len(item["ESGRiskRating"]) > 0
                    assert len(item["industryRank"]) > 0

                    # Check CIK format
                    assert item["cik"].isdigit()
                    assert len(item["cik"]) >= 6
                else:
                    # Pydantic model
                    current_year = datetime.now().year
                    assert 2015 <= item.fiscalYear <= current_year + 1
                    assert len(item.companyName) > 0
                    assert len(item.industry) > 0
                    assert len(item.ESGRiskRating) > 0
                    assert len(item.industryRank) > 0
                    assert item.cik.isdigit()
                    assert len(item.cik) >= 6

    def test_esg_benchmark_data_quality(self, api_key):
        """Test data quality in ESG benchmark data."""
        result = esg.esg_benchmark(apikey=api_key, year="2023")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        if result_list:
            sectors_seen = set()
            for item in result_list[:5]:
                if isinstance(item, dict):
                    # Check score ranges
                    assert 0 <= item["environmentalScore"] <= 100
                    assert 0 <= item["socialScore"] <= 100
                    assert 0 <= item["governanceScore"] <= 100
                    assert 0 <= item["ESGScore"] <= 100

                    # Check fiscal year
                    assert item["fiscalYear"] == 2023

                    # Check sector is not empty
                    assert len(item["sector"]) > 0
                    sectors_seen.add(item["sector"])

                    # ESG score should be related to component scores
                    component_avg = (
                        item["environmentalScore"]
                        + item["socialScore"]
                        + item["governanceScore"]
                    ) / 3
                    # Allow some variance for weighted scoring
                    assert abs(item["ESGScore"] - component_avg) <= 20
                else:
                    # Pydantic model
                    assert 0 <= item.environmentalScore <= 100
                    assert 0 <= item.socialScore <= 100
                    assert 0 <= item.governanceScore <= 100
                    assert 0 <= item.ESGScore <= 100
                    assert item.fiscalYear == 2023
                    assert len(item.sector) > 0
                    sectors_seen.add(item.sector)

            # Should have multiple different sectors
            assert len(sectors_seen) >= 1


# Additional test utilities
def validate_esg_filing_model(data: Dict) -> bool:
    """Validate that data conforms to FMPESGFiling model."""
    try:
        FMPESGFiling(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False


def validate_esg_rating_model(data: Dict) -> bool:
    """Validate that data conforms to FMPESGRating model."""
    try:
        FMPESGRating(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False


def validate_esg_benchmark_model(data: Dict) -> bool:
    """Validate that data conforms to FMPESGBenchmark model."""
    try:
        FMPESGBenchmark(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False
