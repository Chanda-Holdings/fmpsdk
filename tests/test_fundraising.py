from typing import Dict

import pytest

from fmpsdk import fundraising
from fmpsdk.models import (
    FMPCrowdfundingCampaign,
    FMPCrowdfundingSearch,
    FMPEquityOffering,
    FMPEquityOfferingSearch,
)
from tests.conftest import extract_data_list


class TestCrowdfundingOfferingsLatest:
    """Test the latest crowdfunding offerings endpoint."""

    def test_crowdfunding_offerings_latest_basic(self, api_key):
        """Test basic latest crowdfunding offerings."""
        result = fundraising.crowdfunding_offerings_latest(apikey=api_key, limit=10)

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

    def test_crowdfunding_offerings_latest_pagination(self, api_key):
        """Test pagination in latest crowdfunding offerings."""
        result_page1 = fundraising.crowdfunding_offerings_latest(
            apikey=api_key, page=0, limit=5
        )

        result_page2 = fundraising.crowdfunding_offerings_latest(
            apikey=api_key, page=1, limit=5
        )

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

    def test_crowdfunding_offerings_latest_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising.crowdfunding_offerings_latest(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestCrowdfundingOfferingsSearch:
    """Test the crowdfunding offerings search endpoint."""

    def test_crowdfunding_offerings_search_basic(self, api_key):
        """Test basic crowdfunding offerings search."""
        result = fundraising.crowdfunding_offerings_search(
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
            result = fundraising.crowdfunding_offerings_search(
                apikey=api_key, name=term
            )

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_crowdfunding_offerings_search_invalid_name(self, api_key):
        """Test crowdfunding search with invalid name."""
        result = fundraising.crowdfunding_offerings_search(
            apikey=api_key, name="INVALID_COMPANY_NAME_XYZ_123"
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid name
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_crowdfunding_offerings_search_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising.crowdfunding_offerings_search(
            apikey=invalid_api_key, name="Republic"
        )

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestCrowdfundingOfferings:
    """Test the crowdfunding offerings by CIK endpoint."""

    def test_crowdfunding_offerings_basic(self, api_key):
        """Test crowdfunding offerings by CIK."""
        # Use a known CIK that might have crowdfunding data
        result = fundraising.crowdfunding_offerings(
            apikey=api_key, cik="0001798024"  # Example CIK
        )

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
        result = fundraising.crowdfunding_offerings(
            apikey=api_key, cik="9999999999"  # Invalid CIK
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid CIK
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_crowdfunding_offerings_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising.crowdfunding_offerings(
            apikey=invalid_api_key, cik="0001798024"
        )

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraisingLatest:
    """Test the latest fundraising/equity offerings endpoint."""

    def test_fundraising_latest_basic(self, api_key):
        """Test basic latest fundraising data."""
        result = fundraising.fundraising_latest(apikey=api_key, limit=10)

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
        result = fundraising.fundraising_latest(
            apikey=api_key, cik="0001798024", limit=5
        )

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
        """Test pagination in latest fundraising."""
        result_page1 = fundraising.fundraising_latest(apikey=api_key, page=0, limit=5)

        result_page2 = fundraising.fundraising_latest(apikey=api_key, page=1, limit=5)

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

    def test_fundraising_latest_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising.fundraising_latest(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraisingSearch:
    """Test the fundraising search endpoint."""

    def test_fundraising_search_basic(self, api_key):
        """Test basic fundraising search."""
        result = fundraising.fundraising_search(apikey=api_key, name="Technology")

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
            result = fundraising.fundraising_search(apikey=api_key, name=term)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_fundraising_search_invalid_name(self, api_key):
        """Test fundraising search with invalid name."""
        result = fundraising.fundraising_search(
            apikey=api_key, name="INVALID_COMPANY_NAME_XYZ_123"
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid name
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_fundraising_search_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising.fundraising_search(
            apikey=invalid_api_key, name="Technology"
        )

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraising:
    """Test the fundraising by CIK endpoint."""

    def test_fundraising_basic(self, api_key):
        """Test fundraising by CIK."""
        # Use a known CIK that might have fundraising data
        result = fundraising.fundraising(
            apikey=api_key, cik="0001798024"  # Example CIK
        )

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

    def test_fundraising_multiple_ciks(self, api_key):
        """Test fundraising with multiple CIKs."""
        ciks = ["0001798024", "0001559720", "0001652044"]

        for cik in ciks:
            result = fundraising.fundraising(apikey=api_key, cik=cik)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if result_list:
                for item in result_list[:2]:
                    if isinstance(item, dict):
                        assert item["cik"] == cik
                    else:
                        assert item.cik == cik

    def test_fundraising_invalid_cik(self, api_key):
        """Test fundraising with invalid CIK."""
        result = fundraising.fundraising(
            apikey=api_key, cik="9999999999"  # Invalid CIK
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid CIK
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_fundraising_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = fundraising.fundraising(apikey=invalid_api_key, cik="0001798024")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestFundraisingDataQuality:
    """Test data quality and business logic validation."""

    def test_crowdfunding_campaign_data_quality(self, api_key):
        """Test data quality in crowdfunding campaigns."""
        result = fundraising.crowdfunding_offerings_latest(apikey=api_key, limit=5)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # Check date formats
                    assert len(item["filingDate"]) >= 10  # YYYY-MM-DD format
                    assert len(item["acceptedDate"]) >= 10

                    # Check numeric fields are reasonable
                    assert item["numberOfSecurityOffered"] >= 0
                    assert item["offeringPrice"] >= 0
                    assert item["offeringAmount"] >= 0
                    assert item["currentNumberOfEmployees"] >= 0

                    # Check financial fields
                    assert item["totalAssetMostRecentFiscalYear"] >= 0
                    assert item["revenueMostRecentFiscalYear"] >= 0

                    # Check CIK format
                    assert item["cik"].isdigit() or item["cik"] == ""
                    if item["cik"]:
                        assert len(item["cik"]) >= 6

                    # Check form type
                    assert len(item["formType"]) > 0
                else:
                    # Pydantic model
                    assert len(item.filingDate) >= 10
                    assert len(item.acceptedDate) >= 10
                    assert item.numberOfSecurityOffered >= 0
                    assert item.offeringPrice >= 0
                    assert item.offeringAmount >= 0
                    assert item.currentNumberOfEmployees >= 0
                    assert item.totalAssetMostRecentFiscalYear >= 0
                    assert item.revenueMostRecentFiscalYear >= 0
                    assert item.cik.isdigit() or item.cik == ""
                    if item.cik:
                        assert len(item.cik) >= 6
                    assert len(item.formType) > 0

    def test_equity_offering_data_quality(self, api_key):
        """Test data quality in equity offerings."""
        result = fundraising.fundraising_latest(apikey=api_key, limit=5)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # Check date formats (some dates may be empty)
                    assert len(item["filingDate"]) >= 10
                    assert len(item["acceptedDate"]) >= 10
                    if item["dateOfFirstSale"]:  # Only check if not empty
                        assert len(item["dateOfFirstSale"]) >= 10

                    # Check offering amounts are reasonable
                    assert item["totalOfferingAmount"] >= 0
                    assert item["totalAmountSold"] >= 0
                    assert item["totalAmountRemaining"] >= 0
                    assert item["minimumInvestmentAccepted"] >= 0

                    # Check investor counts are reasonable
                    assert item["totalNumberAlreadyInvested"] >= 0

                    # Check fees and costs
                    assert item["salesCommissions"] >= 0
                    assert item["findersFees"] >= 0
                    assert item["grossProceedsUsed"] >= 0

                    # Check company information
                    assert len(item["companyName"]) > 0
                    assert len(item["entityName"]) > 0
                    assert len(item["industryGroupType"]) > 0

                    # Check CIK format
                    assert item["cik"].isdigit()
                    assert len(item["cik"]) >= 6

                    # Check boolean fields
                    assert isinstance(item["isAmendment"], bool)
                    assert isinstance(item["durationOfOfferingIsMoreThanYear"], bool)
                    assert isinstance(item["isBusinessCombinationTransaction"], bool)
                    assert isinstance(item["hasNonAccreditedInvestors"], bool)
                else:
                    # Pydantic model
                    assert len(item.filingDate) >= 10
                    assert len(item.acceptedDate) >= 10
                    if item.dateOfFirstSale:  # Only check if not empty
                        assert len(item.dateOfFirstSale) >= 10
                    assert item.totalOfferingAmount >= 0
                    assert item.totalAmountSold >= 0
                    assert item.totalAmountRemaining >= 0
                    assert item.minimumInvestmentAccepted >= 0
                    assert item.totalNumberAlreadyInvested >= 0
                    assert item.salesCommissions >= 0
                    assert item.findersFees >= 0
                    assert item.grossProceedsUsed >= 0
                    assert len(item.companyName) > 0
                    assert len(item.entityName) > 0
                    assert len(item.industryGroupType) > 0
                    assert item.cik.isdigit()
                    assert len(item.cik) >= 6
                    assert isinstance(item.isAmendment, bool)
                    assert isinstance(item.durationOfOfferingIsMoreThanYear, bool)
                    assert isinstance(item.isBusinessCombinationTransaction, bool)
                    assert isinstance(item.hasNonAccreditedInvestors, bool)


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
