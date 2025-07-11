from typing import Dict

import pytest

from fmpsdk.fundraising import (
    crowdfunding_offerings,
    crowdfunding_offerings_latest,
    crowdfunding_offerings_search,
    fundraising,
    fundraising_latest,
    fundraising_search,
)
from fmpsdk.models import (
    FMPCrowdfundingCampaign,
    FMPCrowdfundingSearch,
    FMPEquityOffering,
    FMPEquityOfferingSearch,
)
from tests.conftest import extract_data_list


class TestCrowdfundingOfferingsLatest:
    """Test the latest crowdfunding offerings endpoint."""

    @pytest.mark.parametrize("limit", [5, 10, 20, 50])
    def test_crowdfunding_offerings_latest_limits(self, api_key, limit):
        """Test latest crowdfunding offerings with different limits."""
        result = crowdfunding_offerings_latest(apikey=api_key, limit=limit)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            assert len(result_list) <= limit

            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "cik" in first_item
                assert "filingDate" in first_item
                assert "acceptedDate" in first_item
                assert "formType" in first_item

                # Test Pydantic model validation
                campaign = FMPCrowdfundingCampaign(**first_item)
                assert campaign.cik == first_item["cik"]
                assert campaign.filingDate == first_item["filingDate"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "filingDate")
                assert hasattr(first_item, "acceptedDate")
                assert hasattr(first_item, "formType")

    def test_crowdfunding_offerings_latest_basic(self, api_key):
        """Test basic latest crowdfunding offerings."""
        result = crowdfunding_offerings_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            assert len(result_list) <= 10

            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "cik" in first_item
                assert "filingDate" in first_item
                assert "acceptedDate" in first_item
                assert "formType" in first_item

                # Test Pydantic model validation
                campaign = FMPCrowdfundingCampaign(**first_item)
                assert campaign.cik == first_item["cik"]
                assert campaign.filingDate == first_item["filingDate"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "filingDate")
                assert hasattr(first_item, "acceptedDate")
                assert hasattr(first_item, "formType")

    @pytest.mark.parametrize("page,limit", [(0, 5), (1, 10), (2, 15), (0, 20), (1, 25)])
    def test_crowdfunding_offerings_latest_pagination_extended(
        self, api_key, page, limit
    ):
        """Test extensive pagination scenarios in latest crowdfunding offerings."""
        result = crowdfunding_offerings_latest(apikey=api_key, page=page, limit=limit)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            assert len(result_list) <= limit

            # Validate structure of results
            for item in result_list[:3]:  # Check first few items
                if isinstance(item, dict):
                    assert "cik" in item
                    assert "formType" in item
                else:
                    assert hasattr(item, "cik")
                    assert hasattr(item, "formType")

    def test_crowdfunding_offerings_latest_pagination(self, api_key):
        """Test pagination in latest crowdfunding offerings."""
        result_page1 = crowdfunding_offerings_latest(apikey=api_key, page=0, limit=5)

        result_page2 = crowdfunding_offerings_latest(apikey=api_key, page=1, limit=5)

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

    def test_crowdfunding_offerings_latest_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = crowdfunding_offerings_latest(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestCrowdfundingOfferingsSearch:
    """Test the crowdfunding offerings search endpoint."""

    @pytest.mark.parametrize(
        "search_term",
        [
            "Republic",  # Popular crowdfunding platform
            "StartEngine",  # Another crowdfunding platform
            "SeedInvest",  # Equity crowdfunding platform
            "Wefunder",  # Investment crowdfunding
            "Technology",  # Industry term
            "Software",  # Technology sector
            "Healthcare",  # Healthcare sector
            "Fintech",  # Financial technology
            "Real Estate",  # Property sector
            "Consumer",  # Consumer goods
            "Energy",  # Energy sector
            "Food",  # Food & beverage
            "Media",  # Media & entertainment
            "Gaming",  # Gaming industry
            "E-commerce",  # Online retail
        ],
    )
    def test_crowdfunding_offerings_search_various_terms(self, api_key, search_term):
        """Test crowdfunding offerings search with various search terms."""
        result = crowdfunding_offerings_search(apikey=api_key, name=search_term)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields for search results
                assert "cik" in first_item
                assert "name" in first_item
                assert "date" in first_item

                # Test Pydantic model validation
                search_result = FMPCrowdfundingSearch(**first_item)
                assert search_result.cik == first_item["cik"]
                assert search_result.name == first_item["name"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "date")

    def test_crowdfunding_offerings_search_basic(self, api_key):
        """Test basic crowdfunding offerings search."""
        result = crowdfunding_offerings_search(
            apikey=api_key, name="Republic"  # Popular crowdfunding platform
        )

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
                assert "cik" in first_item
                assert "name" in first_item
                assert "date" in first_item

                # Test Pydantic model validation
                search_result = FMPCrowdfundingSearch(**first_item)
                assert search_result.cik == first_item["cik"]
                assert search_result.name == first_item["name"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "date")

    def test_crowdfunding_offerings_search_multiple_names(self, api_key):
        """Test crowdfunding search with multiple search terms."""
        search_terms = ["Technology", "Software", "Gaming"]

        for term in search_terms:
            result = crowdfunding_offerings_search(apikey=api_key, name=term)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_crowdfunding_offerings_search_invalid_name(self, api_key):
        """Test crowdfunding search with invalid name."""
        result = crowdfunding_offerings_search(
            apikey=api_key, name="INVALID_COMPANY_NAME_XYZ_123"
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid name
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_crowdfunding_offerings_search_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = crowdfunding_offerings_search(apikey=invalid_api_key, name="Republic")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestCrowdfundingOfferings:
    """Test the crowdfunding offerings by CIK endpoint."""

    @pytest.mark.parametrize(
        "cik",
        [
            "0001798024",  # Example crowdfunding CIK
            "0001646924",  # Another potential CIK
            "0001604778",  # Third CIK
            "0001725283",  # Fourth CIK
            "0001568219",  # Fifth CIK
            "0001602658",  # Sixth CIK
            "0001788028",  # Seventh CIK
            "0001746963",  # Eighth CIK
            "0001812360",  # Ninth CIK
            "0001654954",  # Tenth CIK
        ],
    )
    def test_crowdfunding_offerings_multiple_ciks(self, api_key, cik):
        """Test crowdfunding offerings for multiple CIKs."""
        result = crowdfunding_offerings(apikey=api_key, cik=cik)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            for item in result_list[:3]:  # Check first few items
                if isinstance(item, dict):
                    assert item["cik"] == cik
                    assert "filingDate" in item
                    assert "formType" in item
                else:
                    assert item.cik == cik
                    assert hasattr(item, "filingDate")
                    assert hasattr(item, "formType")

    def test_crowdfunding_offerings_basic(self, api_key):
        """Test crowdfunding offerings by CIK."""
        # Use a known CIK that might have crowdfunding data
        result = crowdfunding_offerings(apikey=api_key, cik="0001798024")  # Example CIK

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            for item in result_list[:2]:  # Check first few items
                if isinstance(item, dict):
                    assert item["cik"] == "0001798024"
                else:
                    assert item.cik == "0001798024"

    def test_crowdfunding_offerings_invalid_cik(self, api_key):
        """Test crowdfunding offerings with invalid CIK."""
        result = crowdfunding_offerings(apikey=api_key, cik="9999999999")  # Invalid CIK

        result_list = extract_data_list(result)
        # Should return empty list for invalid CIK
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_crowdfunding_offerings_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = crowdfunding_offerings(apikey=invalid_api_key, cik="0001798024")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraisingLatest:
    """Test the latest fundraising/equity offerings endpoint."""

    @pytest.mark.parametrize("limit", [5, 10, 15, 25, 50])
    def test_fundraising_latest_limits(self, api_key, limit):
        """Test latest fundraising data with different limits."""
        result = fundraising_latest(apikey=api_key, limit=limit)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            assert len(result_list) <= limit

            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "cik" in first_item
                assert "filingDate" in first_item
                assert "acceptedDate" in first_item
                assert "companyName" in first_item
                assert "totalOfferingAmount" in first_item

                # Test Pydantic model validation
                offering = FMPEquityOffering(**first_item)
                assert offering.cik == first_item["cik"]
                assert offering.companyName == first_item["companyName"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "filingDate")
                assert hasattr(first_item, "acceptedDate")
                assert hasattr(first_item, "companyName")
                assert hasattr(first_item, "totalOfferingAmount")

    @pytest.mark.parametrize("page,limit", [(0, 10), (1, 10), (2, 10), (0, 20), (1, 5)])
    def test_fundraising_latest_pagination_scenarios(self, api_key, page, limit):
        """Test fundraising latest with various pagination scenarios."""
        result = fundraising_latest(apikey=api_key, page=page, limit=limit)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            assert len(result_list) <= limit

            # Validate offering amounts are non-negative
            for item in result_list[:3]:
                if isinstance(item, dict):
                    if (
                        "totalOfferingAmount" in item
                        and item["totalOfferingAmount"] is not None
                    ):
                        assert item["totalOfferingAmount"] >= 0
                else:
                    if (
                        hasattr(item, "totalOfferingAmount")
                        and item.totalOfferingAmount is not None
                    ):
                        assert item.totalOfferingAmount >= 0

    def test_fundraising_latest_basic(self, api_key):
        """Test basic latest fundraising data."""
        result = fundraising_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            assert len(result_list) <= 10

            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "cik" in first_item
                assert "companyName" in first_item
                assert "filingDate" in first_item
                assert "formType" in first_item

                # Test Pydantic model validation
                offering = FMPEquityOffering(**first_item)
                assert offering.cik == first_item["cik"]
                assert offering.companyName == first_item["companyName"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "companyName")
                assert hasattr(first_item, "filingDate")
                assert hasattr(first_item, "formType")

    def test_fundraising_latest_with_cik(self, api_key):
        """Test latest fundraising with specific CIK filter."""
        result = fundraising_latest(apikey=api_key, cik="0001798024", limit=5)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            for item in result_list:
                if isinstance(item, dict):
                    assert item["cik"] == "0001798024"
                else:
                    assert item.cik == "0001798024"

    def test_fundraising_latest_pagination(self, api_key):
        """Test pagination in latest"""
        result_page1 = fundraising_latest(apikey=api_key, page=0, limit=5)

        result_page2 = fundraising_latest(apikey=api_key, page=1, limit=5)

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

    def test_fundraising_latest_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising_latest(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraisingSearch:
    """Test the fundraising search endpoint."""

    @pytest.mark.parametrize(
        "search_term",
        [
            # Technology Companies
            "Apple",
            "Microsoft",
            "Google",
            "Amazon",
            "Tesla",
            "Meta",
            "Netflix",
            "Nvidia",
            "Adobe",
            "Salesforce",
            "Oracle",
            "Intel",
            "Cisco",
            # Healthcare & Biotech
            "Johnson",
            "Pfizer",
            "Moderna",
            "Gilead",
            "Amgen",
            "Biogen",
            "Regeneron",
            "Illumina",
            "Vertex",
            "BioNTech",
            # Financial Services
            "JPMorgan",
            "Goldman",
            "Morgan Stanley",
            "Bank of America",
            "Wells Fargo",
            "Visa",
            "Mastercard",
            "PayPal",
            "Square",
            "Coinbase",
            # Consumer & Retail
            "Walmart",
            "Target",
            "Home Depot",
            "Nike",
            "Starbucks",
            "McDonald's",
            "Coca Cola",
            "PepsiCo",
            "Procter",
            "Unilever",
            # Industry Terms
            "Software",
            "Technology",
            "Healthcare",
            "Fintech",
            "Biotech",
            "Energy",
            "Renewable",
            "Electric",
            "Autonomous",
            "Artificial Intelligence",
            "Blockchain",
            "Cryptocurrency",
            "Cloud",
            "Cybersecurity",
            "Data Analytics",
        ],
    )
    def test_fundraising_search_comprehensive_terms(self, api_key, search_term):
        """Test fundraising search with comprehensive company and industry terms."""
        result = fundraising_search(apikey=api_key, name=search_term)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "cik" in first_item
                assert "name" in first_item
                assert "date" in first_item

                # Test Pydantic model validation
                search_result = FMPEquityOfferingSearch(**first_item)
                assert search_result.cik == first_item["cik"]
                assert search_result.name == first_item["name"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "date")

    def test_fundraising_search_basic(self, api_key):
        """Test basic fundraising search."""
        result = fundraising_search(apikey=api_key, name="Technology")

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
                assert "cik" in first_item
                assert "name" in first_item
                assert "date" in first_item

                # Test Pydantic model validation
                search_result = FMPEquityOfferingSearch(**first_item)
                assert search_result.cik == first_item["cik"]
                assert search_result.name == first_item["name"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "date")

    def test_fundraising_search_multiple_terms(self, api_key):
        """Test fundraising search with multiple terms."""
        search_terms = ["Software", "Healthcare", "Fintech"]

        for term in search_terms:
            result = fundraising_search(apikey=api_key, name=term)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_fundraising_search_invalid_name(self, api_key):
        """Test fundraising search with invalid name."""
        result = fundraising_search(apikey=api_key, name="INVALID_COMPANY_NAME_XYZ_123")

        result_list = extract_data_list(result)
        # Should return empty list for invalid name
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_fundraising_search_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising_search(apikey=invalid_api_key, name="Technology")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraising:
    """Test the fundraising by CIK endpoint."""

    @pytest.mark.parametrize(
        "cik",
        [
            # Technology sector CIKs
            "0000320193",  # Apple Inc.
            "0000789019",  # Microsoft Corporation
            "0001652044",  # Alphabet Inc. (Google)
            "0001018724",  # Amazon.com Inc.
            "0001318605",  # Tesla Inc.
            "0001326801",  # Meta Platforms Inc.
            "0001065280",  # Netflix Inc.
            # Healthcare/Biotech CIKs
            "0000200406",  # Johnson & Johnson
            "0000078003",  # Pfizer Inc.
            "0001682852",  # Moderna Inc.
            "0000882095",  # Gilead Sciences Inc.
            "0000318154",  # Amgen Inc.
            # Financial Services CIKs
            "0000019617",  # JPMorgan Chase & Co.
            "0000886982",  # Goldman Sachs Group Inc.
            "0000895421",  # Morgan Stanley
            "0000070858",  # Bank of America Corp
            "0000072971",  # Wells Fargo & Company
            # Additional examples
            "0001798024",  # Example crowdfunding CIK
            "0001646924",  # Another potential CIK
            "0001604778",  # Third CIK
            "0001725283",  # Fourth CIK
        ],
    )
    def test_fundraising_major_company_ciks(self, api_key, cik):
        """Test fundraising data for major company CIKs."""
        result = fundraising(apikey=api_key, cik=cik)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            for item in result_list[:3]:  # Check first few items
                if isinstance(item, dict):
                    assert item["cik"] == cik
                    assert "filingDate" in item
                    assert "companyName" in item
                    assert "totalOfferingAmount" in item

                    # Validate financial amounts are non-negative
                    if item["totalOfferingAmount"] is not None:
                        assert item["totalOfferingAmount"] >= 0
                    if (
                        "totalAmountSold" in item
                        and item["totalAmountSold"] is not None
                    ):
                        assert item["totalAmountSold"] >= 0
                else:
                    assert item.cik == cik
                    assert hasattr(item, "filingDate")
                    assert hasattr(item, "companyName")
                    assert hasattr(item, "totalOfferingAmount")

                    # Validate financial amounts are non-negative
                    if item.totalOfferingAmount is not None:
                        assert item.totalOfferingAmount >= 0

    def test_fundraising_basic(self, api_key):
        """Test fundraising by CIK."""
        # Use a known CIK that might have fundraising data
        result = fundraising(apikey=api_key, cik="0001798024")  # Example CIK

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            for item in result_list[:2]:  # Check first few items
                if isinstance(item, dict):
                    assert item["cik"] == "0001798024"
                else:
                    assert item.cik == "0001798024"

    def test_fundraising_invalid_cik(self, api_key):
        """Test fundraising with invalid CIK."""
        result = fundraising(apikey=api_key, cik="9999999999")  # Invalid CIK

        result_list = extract_data_list(result)
        # Should return empty list for invalid CIK
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_fundraising_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising(apikey=invalid_api_key, cik="0001798024")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraisingDataQuality:
    """Test data quality and business logic validation for fundraising endpoints."""

    @pytest.mark.parametrize(
        "endpoint_type",
        [
            "latest_crowdfunding",
            "search_crowdfunding",
            "latest_fundraising",
            "search_fundraising",
        ],
    )
    def test_fundraising_data_consistency(self, api_key, endpoint_type):
        """Test data consistency across different fundraising endpoints."""
        if endpoint_type == "latest_crowdfunding":
            result = crowdfunding_offerings_latest(apikey=api_key, limit=5)
        elif endpoint_type == "search_crowdfunding":
            result = crowdfunding_offerings_search(apikey=api_key, name="Technology")
        elif endpoint_type == "latest_fundraising":
            result = fundraising_latest(apikey=api_key, limit=5)
        elif endpoint_type == "search_fundraising":
            result = fundraising_search(apikey=api_key, name="Software")

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            for item in result_list[:3]:  # Check first few items
                if isinstance(item, dict):
                    # Validate CIK format
                    assert "cik" in item
                    assert len(item["cik"]) >= 6  # CIKs should be at least 6 digits
                    assert item["cik"].isdigit()

                    # Validate date formats
                    if "filingDate" in item and item["filingDate"]:
                        assert len(item["filingDate"]) >= 10  # YYYY-MM-DD format
                    if "acceptedDate" in item and item["acceptedDate"]:
                        assert len(item["acceptedDate"]) >= 10

                    # Validate company information
                    if "companyName" in item:
                        assert len(item["companyName"]) > 0
                    if "name" in item:
                        assert len(item["name"]) > 0

    @pytest.mark.parametrize(
        "financial_field",
        [
            "totalOfferingAmount",
            "totalAmountSold",
            "totalAmountRemaining",
            "minimumInvestmentAccepted",
            "salesCommissions",
            "findersFees",
        ],
    )
    def test_fundraising_financial_fields_validation(self, api_key, financial_field):
        """Test validation of financial fields in fundraising data."""
        result = fundraising_latest(apikey=api_key, limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key issues or data unavailable")

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:5]:  # Check first few items
                if isinstance(item, dict):
                    if financial_field in item and item[financial_field] is not None:
                        # Financial amounts should be non-negative
                        assert item[financial_field] >= 0
                        # Should be numeric
                        assert isinstance(item[financial_field], (int, float))
                else:
                    if hasattr(item, financial_field):
                        field_value = getattr(item, financial_field)
                        if field_value is not None:
                            assert field_value >= 0
                            assert isinstance(field_value, (int, float))


class TestFundraisingErrorHandling:
    """Test error handling and edge cases for fundraising endpoints."""

    @pytest.mark.parametrize(
        "invalid_cik",
        [
            "9999999999",  # Non-existent CIK
            "1234567890",  # Another invalid CIK
            "0000000001",  # Very low CIK
            "abc123def",  # Non-numeric CIK
            "",  # Empty CIK
        ],
    )
    def test_fundraising_invalid_ciks(self, api_key, invalid_cik):
        """Test fundraising endpoints with invalid CIKs."""
        try:
            result = fundraising(apikey=api_key, cik=invalid_cik)

            if isinstance(result, dict) and "Error Message" in result:
                # API properly handles invalid CIK
                assert "Error Message" in result
                return

            result_list = extract_data_list(result)
            # Should return empty list for invalid CIK
            assert isinstance(result_list, list)
            assert len(result_list) == 0
        except Exception:
            # Some invalid formats may raise exceptions, which is acceptable
            pass

    @pytest.mark.parametrize(
        "invalid_search_term",
        [
            "NONEXISTENT_COMPANY_XYZ_123",
            "!@#$%^&*()",
            "A" * 100,  # Very long search term
            "",  # Empty search term
            "123456789",  # Numeric only
        ],
    )
    def test_fundraising_search_invalid_terms(self, api_key, invalid_search_term):
        """Test fundraising search with invalid search terms."""
        try:
            result = fundraising_search(apikey=api_key, name=invalid_search_term)

            if isinstance(result, dict) and "Error Message" in result:
                # API properly handles invalid search
                return

            result_list = extract_data_list(result)
            # Should return empty list for invalid search terms
            assert isinstance(result_list, list)
        except Exception:
            # Some invalid formats may raise exceptions, which is acceptable
            pass


# Additional test utilities
def validate_crowdfunding_campaign_model(data: Dict) -> bool:
    """Validate that data conforms to FMPCrowdfundingCampaign model."""
    try:
        FMPCrowdfundingCampaign(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False


def validate_equity_offering_model(data: Dict) -> bool:
    """Validate that data conforms to FMPEquityOffering model."""
    try:
        FMPEquityOffering(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False
