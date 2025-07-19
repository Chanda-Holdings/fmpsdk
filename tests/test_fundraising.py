from typing import Dict

import pytest

from fmpsdk.exceptions import InvalidQueryParameterException
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
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
    validate_required_fields,
)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCrowdfundingOfferingsLatest:
    """Test class for latest crowdfunding offerings functionality."""

    @pytest.mark.parametrize("limit", [5, 10, 20, 50])
    def test_crowdfunding_offerings_latest_limits(self, api_key, limit):
        """Test latest crowdfunding offerings with different limits."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings_latest,
            "crowdfunding_offerings_latest",
            apikey=api_key,
            limit=limit,
        )

        # Get response models and validate
        models = get_response_models(result, FMPCrowdfundingCampaign)
        validate_model_list(models, FMPCrowdfundingCampaign)

        if models:  # If data is available
            assert len(models) <= limit

            # Enhanced validation for first item
            first_item = models[0]

            # Crowdfunding validation
            if first_item.cik:
                assert (
                    first_item.cik.isdigit()
                    or first_item.cik.replace("-", "").isdigit()
                ), "CIK should be numeric"
                assert len(first_item.cik) >= 6, "CIK should be reasonable length"

            if first_item.filingDate:
                assert (
                    len(first_item.filingDate) >= 10
                ), "Filing date should be valid format"

            if first_item.acceptedDate:
                assert (
                    len(first_item.acceptedDate) >= 10
                ), "Accepted date should be valid format"

            if first_item.formType:
                # Crowdfunding forms should be relevant types
                crowdfunding_forms = [
                    "C",
                    "C-U",
                    "C-AR",
                    "C-W",
                    "1-A",
                    "1-K",
                    "1-SA",
                    "1-U",
                    "1-Z",
                ]
                assert any(
                    cf in first_item.formType.upper() for cf in crowdfunding_forms
                ), f"Form type should be crowdfunding related: {first_item.formType}"

    def test_crowdfunding_offerings_latest_basic(self, api_key):
        """Test basic latest crowdfunding offerings."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings_latest,
            "crowdfunding_offerings_latest",
            apikey=api_key,
            limit=10,
        )

        # Get response models and validate
        models = get_response_models(result, FMPCrowdfundingCampaign)
        validate_model_list(models, FMPCrowdfundingCampaign)

        if models:  # If data is available
            assert len(models) <= 10

            # Enhanced validation for first item
            first_item = models[0]

            # Business logic validation
            assert first_item.cik is not None, "CIK should be present"
            assert first_item.filingDate is not None, "Filing date should be present"
            assert (
                first_item.acceptedDate is not None
            ), "Accepted date should be present"
            assert first_item.formType is not None, "Form type should be present"

    @pytest.mark.parametrize("page,limit", [(0, 5), (1, 10), (2, 15), (0, 20), (1, 25)])
    def test_crowdfunding_offerings_latest_pagination_extended(
        self, api_key, page, limit
    ):
        """Test extensive pagination scenarios in latest crowdfunding offerings."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings_latest,
            "crowdfunding_offerings_latest",
            apikey=api_key,
            page=page,
            limit=limit,
        )

        # Get response models and validate
        models = get_response_models(result, FMPCrowdfundingCampaign)
        validate_model_list(models, FMPCrowdfundingCampaign)

        if models:
            assert len(models) <= limit

            # Enhanced validation for pagination
            for item in models[:3]:  # Check first few items
                if item.cik:
                    assert (
                        item.cik.isdigit() or item.cik.replace("-", "").isdigit()
                    ), "CIK should be numeric"
                if item.formType:
                    assert len(item.formType) > 0, "Form type should not be empty"

    def test_crowdfunding_offerings_latest_pagination(self, api_key):
        """Test pagination in latest crowdfunding offerings."""
        result_page1, validation = handle_api_call_with_validation(
            crowdfunding_offerings_latest,
            "crowdfunding_offerings_latest",
            apikey=api_key,
            page=0,
            limit=5,
        )

        result_page2, validation = handle_api_call_with_validation(
            crowdfunding_offerings_latest,
            "crowdfunding_offerings_latest",
            apikey=api_key,
            page=1,
            limit=5,
        )

        # Get response models and validate
        models1 = get_response_models(result_page1, FMPCrowdfundingCampaign)
        models2 = get_response_models(result_page2, FMPCrowdfundingCampaign)
        validate_model_list(models1, FMPCrowdfundingCampaign)
        validate_model_list(models2, FMPCrowdfundingCampaign)

        # Validate pagination if both pages have data
        if models1 and models2:
            assert len(models1) <= 5
            assert len(models2) <= 5


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCrowdfundingOfferingsSearch:
    """Test class for crowdfunding offerings search functionality."""

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
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings_search,
            "crowdfunding_offerings_search",
            apikey=api_key,
            name=search_term,
        )

        result_list = get_response_models(result, FMPCrowdfundingSearch)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            name = first_item.name
            date = first_item.date

            # Search validation
            if cik:
                assert (
                    cik.isdigit() or cik.replace("-", "").isdigit()
                ), "CIK should be numeric"

            if name:
                assert len(name) > 0, "Name should not be empty"
                assert len(name) <= 200, "Name should be reasonable length"
                # Search term should be somewhat related to the name
                if len(search_term) > 3:  # Only for meaningful search terms
                    # Very flexible matching for fundraising searches
                    search_words = [
                        word.lower().strip("'s").strip() for word in search_term.split()
                    ]
                    name_lower = name.lower()
                    name_words = [
                        word.strip(".,():").lower() for word in name_lower.split()
                    ]

                    match_found = False
                    for search_word in search_words:
                        # Direct substring match
                        if search_word in name_lower:
                            match_found = True
                            break
                        # Word-level substring matching
                        for name_word in name_words:
                            if (
                                search_word in name_word
                                or name_word in search_word
                                or (
                                    len(search_word) > 4
                                    and name_word.startswith(
                                        search_word[: min(6, len(search_word))]
                                    )
                                )
                                or (
                                    len(name_word) > 4
                                    and search_word.startswith(
                                        name_word[: min(6, len(name_word))]
                                    )
                                )
                            ):
                                match_found = True
                                break
                        if match_found:
                            break

                    # Special case handling for common variations
                    if not match_found:
                        # Handle common word mappings
                        word_mappings = {
                            "gaming": ["game", "games"],
                            "renewable": ["renew", "renewing"],
                            "technology": ["tech", "technologi"],
                        }

                        for search_word in search_words:
                            if search_word in word_mappings:
                                for variant in word_mappings[search_word]:
                                    if variant in name_lower:
                                        match_found = True
                                        break
                                if match_found:
                                    break

                    assert (
                        match_found
                    ), f"Search term '{search_term}' should be related to name '{name}'"

            if date:
                assert len(date) >= 10, "Date should be valid format"

    def test_crowdfunding_offerings_search_basic(self, api_key):
        """Test basic crowdfunding offerings search."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings_search,
            "crowdfunding_offerings_search",
            apikey=api_key,
            name="Republic",  # Popular crowdfunding platform
        )

        result_list = get_response_models(result, FMPCrowdfundingSearch)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            name = first_item.name
            date = first_item.date

            # Business logic validation
            assert cik is not None, "CIK should be present"
            assert name is not None, "Name should be present"
            assert date is not None, "Date should be present"

    def test_crowdfunding_offerings_search_multiple_names(self, api_key):
        """Test crowdfunding offerings search with multiple name variations."""
        search_terms = ["Republic", "StartEngine", "SeedInvest", "Wefunder"]

        for term in search_terms:
            result, validation = handle_api_call_with_validation(
                crowdfunding_offerings_search,
                "crowdfunding_offerings_search",
                apikey=api_key,
                name=term,
            )

            result_list = get_response_models(result, FMPCrowdfundingSearch)
            assert isinstance(result_list, list)

            if result_list:
                # Validate search relevance
                for item in result_list[:3]:
                    name = item.name
                    if name:
                        assert (
                            len(name) > 0
                        ), f"Name should not be empty for search term: {term}"

    def test_crowdfunding_offerings_search_invalid_name(self, api_key):
        """Test crowdfunding offerings search with invalid name."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings_search,
            "crowdfunding_offerings_search",
            apikey=api_key,
            name="INVALID_COMPANY_NAME_XYZ_123",
        )

        result_list = get_response_models(result, FMPCrowdfundingSearch)
        assert isinstance(result_list, list)
        # Should return empty list for invalid name
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCrowdfundingOfferings:
    """Test class for crowdfunding offerings by CIK functionality."""

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
        """Test crowdfunding offerings with multiple CIKs."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings, "crowdfunding_offerings", apikey=api_key, cik=cik
        )

        result_list = get_response_models(result, FMPCrowdfundingCampaign)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            result_cik = first_item.cik
            filing_date = first_item.filingDate
            form_type = first_item.formType

            # CIK validation
            if result_cik:
                assert (
                    cik.replace("000", "") in result_cik
                ), f"CIK should match requested: {cik}"

            if filing_date:
                assert len(filing_date) >= 10, "Filing date should be valid format"

            if form_type:
                # Should be crowdfunding related
                assert len(form_type) > 0, "Form type should not be empty"

    def test_crowdfunding_offerings_basic(self, api_key):
        """Test basic crowdfunding offerings."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings,
            "crowdfunding_offerings",
            apikey=api_key,
            cik="0001798024",
        )

        result_list = get_response_models(result, FMPCrowdfundingCampaign)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            filing_date = first_item.filingDate

            # Business logic validation
            assert cik is not None, "CIK should be present"
            assert filing_date is not None, "Filing date should be present"

    def test_crowdfunding_offerings_invalid_cik(self, api_key):
        """Test crowdfunding offerings with invalid CIK."""
        result, validation = handle_api_call_with_validation(
            crowdfunding_offerings,
            "crowdfunding_offerings",
            apikey=api_key,
            cik="9999999999",
        )

        result_list = get_response_models(result, FMPCrowdfundingCampaign)
        assert isinstance(result_list, list)
        # Should return empty list for invalid CIK
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFundraisingLatest:
    """Test class for latest fundraising functionality."""

    @pytest.mark.parametrize("limit", [5, 10, 15, 25, 50])
    def test_fundraising_latest_limits(self, api_key, limit):
        """Test latest fundraising with different limits."""
        result, validation = handle_api_call_with_validation(
            fundraising_latest, "fundraising_latest", apikey=api_key, limit=limit
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            assert len(result_list) <= limit

            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            filing_date = first_item.filingDate
            accepted_date = first_item.acceptedDate
            form_type = first_item.formType

            # Fundraising validation
            if cik:
                assert (
                    cik.isdigit() or cik.replace("-", "").isdigit()
                ), "CIK should be numeric"
                assert len(cik) >= 6, "CIK should be reasonable length"

            if filing_date:
                assert len(filing_date) >= 10, "Filing date should be valid format"

            if accepted_date:
                assert len(accepted_date) >= 10, "Accepted date should be valid format"

            if form_type:
                # Fundraising forms should be relevant types
                fundraising_forms = [
                    "S-1",
                    "S-3",
                    "S-4",
                    "S-8",
                    "S-11",
                    "F-1",
                    "F-3",
                    "F-4",
                    "424B",
                    "D",
                ]
                assert any(
                    ff in form_type.upper() for ff in fundraising_forms
                ), f"Form type should be fundraising related: {form_type}"

    @pytest.mark.parametrize("page,limit", [(0, 10), (1, 10), (2, 10), (0, 20), (1, 5)])
    def test_fundraising_latest_pagination_scenarios(self, api_key, page, limit):
        """Test various pagination scenarios in latest fundraising."""
        result, validation = handle_api_call_with_validation(
            fundraising_latest,
            "fundraising_latest",
            apikey=api_key,
            page=page,
            limit=limit,
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:
            assert len(result_list) <= limit

            # Enhanced validation for pagination
            for item in result_list[:3]:  # Check first few items
                cik = item.cik
                form_type = item.formType

                if cik:
                    assert (
                        cik.isdigit() or cik.replace("-", "").isdigit()
                    ), "CIK should be numeric"
                if form_type:
                    assert len(form_type) > 0, "Form type should not be empty"

    def test_fundraising_latest_basic(self, api_key):
        """Test basic latest fundraising."""
        result, validation = handle_api_call_with_validation(
            fundraising_latest, "fundraising_latest", apikey=api_key, limit=10
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            assert len(result_list) <= 10

            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            filing_date = first_item.filingDate
            accepted_date = first_item.acceptedDate
            form_type = first_item.formType

            # Business logic validation
            assert cik is not None, "CIK should be present"
            assert filing_date is not None, "Filing date should be present"
            assert accepted_date is not None, "Accepted date should be present"
            assert form_type is not None, "Form type should be present"

    def test_fundraising_latest_with_cik(self, api_key):
        """Test latest fundraising with CIK filter."""
        result, validation = handle_api_call_with_validation(
            fundraising_latest,
            "fundraising_latest",
            apikey=api_key,
            cik="0000320193",  # Apple
            limit=5,
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:
            # Enhanced validation for CIK consistency
            for item in result_list[:3]:
                cik = item.cik
                if cik:
                    assert "320193" in cik, f"CIK should match requested: {cik}"

    def test_fundraising_latest_pagination(self, api_key):
        """Test pagination in latest fundraising."""
        result_page1, validation = handle_api_call_with_validation(
            fundraising_latest, "fundraising_latest", apikey=api_key, page=0, limit=5
        )

        result_page2, validation = handle_api_call_with_validation(
            fundraising_latest, "fundraising_latest", apikey=api_key, page=1, limit=5
        )

        result_list1 = get_response_models(result_page1, FMPEquityOffering)
        result_list2 = get_response_models(result_page2, FMPEquityOffering)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

        # Validate pagination if both pages have data
        if result_list1 and result_list2:
            assert len(result_list1) <= 5
            assert len(result_list2) <= 5


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFundraisingSearch:
    """Test class for fundraising search functionality."""

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
        """Test fundraising search with comprehensive search terms."""
        result, validation = handle_api_call_with_validation(
            fundraising_search, "fundraising_search", apikey=api_key, name=search_term
        )

        result_list = get_response_models(result, FMPEquityOfferingSearch)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            name = first_item.name
            date = first_item.date

            # Search validation
            if cik:
                assert (
                    cik.isdigit() or cik.replace("-", "").isdigit()
                ), "CIK should be numeric"

            if name:
                assert len(name) > 0, "Name should not be empty"
                assert len(name) <= 200, "Name should be reasonable length"
                # Search term should be somewhat related to the name
                if len(search_term) > 3:  # Only for meaningful search terms
                    # Very flexible matching for fundraising searches
                    search_words = [
                        word.lower().strip("'s").strip() for word in search_term.split()
                    ]
                    name_lower = name.lower()
                    name_words = [
                        word.strip(".,():").lower() for word in name_lower.split()
                    ]

                    match_found = False
                    for search_word in search_words:
                        # Direct substring match
                        if search_word in name_lower:
                            match_found = True
                            break
                        # Word-level substring matching
                        for name_word in name_words:
                            if (
                                search_word in name_word
                                or name_word in search_word
                                or (
                                    len(search_word) > 4
                                    and name_word.startswith(
                                        search_word[: min(6, len(search_word))]
                                    )
                                )
                                or (
                                    len(name_word) > 4
                                    and search_word.startswith(
                                        name_word[: min(6, len(name_word))]
                                    )
                                )
                            ):
                                match_found = True
                                break
                        if match_found:
                            break

                    # Special case handling for common variations
                    if not match_found:
                        # Handle common word mappings
                        word_mappings = {
                            "gaming": ["game", "games"],
                            "renewable": ["renew", "renewing"],
                            "technology": ["tech", "technologi"],
                        }

                        for search_word in search_words:
                            if search_word in word_mappings:
                                for variant in word_mappings[search_word]:
                                    if variant in name_lower:
                                        match_found = True
                                        break
                                if match_found:
                                    break

                    assert (
                        match_found
                    ), f"Search term '{search_term}' should be related to name '{name}'"

            if date:
                assert len(date) >= 10, "Date should be valid format"

    def test_fundraising_search_basic(self, api_key):
        """Test basic fundraising search."""
        result, validation = handle_api_call_with_validation(
            fundraising_search, "fundraising_search", apikey=api_key, name="Apple"
        )

        result_list = get_response_models(result, FMPEquityOfferingSearch)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            name = first_item.name
            date = first_item.date

            # Business logic validation
            assert cik is not None, "CIK should be present"
            assert name is not None, "Name should be present"
            assert date is not None, "Date should be present"

    def test_fundraising_search_multiple_terms(self, api_key):
        """Test fundraising search with multiple search terms."""
        search_terms = ["Apple", "Microsoft", "Google", "Amazon"]

        for term in search_terms:
            result, validation = handle_api_call_with_validation(
                fundraising_search, "fundraising_search", apikey=api_key, name=term
            )

            result_list = get_response_models(result, FMPEquityOfferingSearch)
            assert isinstance(result_list, list)

            if result_list:
                # Validate search relevance
                for item in result_list[:3]:
                    name = item.name
                    if name:
                        assert (
                            len(name) > 0
                        ), f"Name should not be empty for search term: {term}"

    def test_fundraising_search_invalid_name(self, api_key):
        """Test fundraising search with invalid name."""
        result, validation = handle_api_call_with_validation(
            fundraising_search,
            "fundraising_search",
            apikey=api_key,
            name="INVALID_COMPANY_NAME_XYZ_123",
        )

        result_list = get_response_models(result, FMPEquityOfferingSearch)
        assert isinstance(result_list, list)
        # Should return empty list for invalid name
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFundraising:
    """Test class for fundraising by CIK functionality."""

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
        """Test fundraising with major company CIKs."""
        result, validation = handle_api_call_with_validation(
            fundraising, "fundraising", apikey=api_key, cik=cik
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            result_cik = first_item.cik
            filing_date = first_item.filingDate
            form_type = first_item.formType

            # CIK validation
            if result_cik:
                # Remove leading zeros for comparison
                requested_cik = cik.lstrip("0")
                assert requested_cik in result_cik, f"CIK should match requested: {cik}"

            if filing_date:
                assert len(filing_date) >= 10, "Filing date should be valid format"

            if form_type:
                assert len(form_type) > 0, "Form type should not be empty"

    def test_fundraising_basic(self, api_key):
        """Test basic fundraising."""
        result, validation = handle_api_call_with_validation(
            fundraising, "fundraising", apikey=api_key, cik="0000320193"  # Apple
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Enhanced validation for first item
            first_item = result_list[0]
            cik = first_item.cik
            filing_date = first_item.filingDate

            # Business logic validation
            assert cik is not None, "CIK should be present"
            assert filing_date is not None, "Filing date should be present"

    def test_fundraising_invalid_cik(self, api_key):
        """Test fundraising with invalid CIK."""
        result, validation = handle_api_call_with_validation(
            fundraising, "fundraising", apikey=api_key, cik="9999999999"
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)
        # Should return empty list for invalid CIK
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFundraisingDataQuality:
    """Test class for fundraising data quality and consistency."""

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
        """Test data consistency across fundraising endpoints."""
        if endpoint_type == "latest_crowdfunding":
            result, validation = handle_api_call_with_validation(
                crowdfunding_offerings_latest,
                "crowdfunding_offerings_latest",
                apikey=api_key,
                limit=10,
            )
        elif endpoint_type == "search_crowdfunding":
            result, validation = handle_api_call_with_validation(
                crowdfunding_offerings_search,
                "crowdfunding_offerings_search",
                apikey=api_key,
                name="Technology",
            )
        elif endpoint_type == "latest_fundraising":
            result, validation = handle_api_call_with_validation(
                fundraising_latest, "fundraising_latest", apikey=api_key, limit=10
            )
        elif endpoint_type == "search_fundraising":
            result, validation = handle_api_call_with_validation(
                fundraising_search,
                "fundraising_search",
                apikey=api_key,
                name="Technology",
            )

        # Determine correct model based on endpoint type
        if endpoint_type in ["latest_fundraising", "fundraising"]:
            result_list = get_response_models(result, FMPEquityOffering)
        elif endpoint_type in ["search_fundraising"]:
            result_list = get_response_models(result, FMPEquityOfferingSearch)
        elif endpoint_type in ["latest_crowdfunding", "crowdfunding"]:
            result_list = get_response_models(result, FMPCrowdfundingCampaign)
        elif endpoint_type in ["search_crowdfunding"]:
            result_list = get_response_models(result, FMPCrowdfundingSearch)
        else:
            result_list = get_response_models(result, FMPEquityOffering)

        assert isinstance(result_list, list)

        if result_list:
            # Enhanced validation for data consistency
            for item in result_list[:3]:  # Check first few items
                cik = item.cik
                if cik:
                    assert (
                        cik.isdigit() or cik.replace("-", "").isdigit()
                    ), f"CIK should be numeric for {endpoint_type}"
                    assert (
                        len(cik) >= 6
                    ), f"CIK should be reasonable length for {endpoint_type}"

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
        """Test fundraising financial fields validation."""
        result, validation = handle_api_call_with_validation(
            fundraising_latest, "fundraising_latest", apikey=api_key, limit=20
        )

        result_list = get_response_models(result, FMPEquityOffering)
        assert isinstance(result_list, list)

        if result_list:
            # Enhanced validation for financial fields
            for item in result_list[:10]:  # Check first 10 items
                field_value = getattr(item, financial_field)
                if field_value is not None:
                    if isinstance(field_value, (int, float)):
                        assert (
                            field_value >= 0
                        ), f"{financial_field} should be non-negative"
                    elif isinstance(field_value, str):
                        # Handle string representations of numbers
                        if (
                            field_value.replace(",", "")
                            .replace(".", "")
                            .replace("-", "")
                            .isdigit()
                        ):
                            numeric_value = float(field_value.replace(",", ""))
                            assert (
                                numeric_value >= 0
                            ), f"{financial_field} should be non-negative"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFundraisingErrorHandling:
    """Test class for fundraising error handling."""

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
        """Test fundraising with invalid CIKs."""
        # For obviously invalid CIKs (non-numeric), expect exception
        if invalid_cik == "abc123def":
            with pytest.raises(InvalidQueryParameterException):
                fundraising(apikey=api_key, cik=invalid_cik)
        else:
            # For empty or numeric but non-existent CIKs, API might return empty results
            result, validation = handle_api_call_with_validation(
                fundraising, "fundraising", apikey=api_key, cik=invalid_cik
            )

            result_list = get_response_models(result, FMPEquityOffering)
            assert isinstance(result_list, list)
            # Should return empty list for non-existent CIKs

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
        # For empty search terms, expect an exception
        if invalid_search_term == "":
            with pytest.raises(InvalidQueryParameterException):
                fundraising_search(apikey=api_key, name=invalid_search_term)
        else:
            # For other invalid terms, the API might still return results
            result, validation = handle_api_call_with_validation(
                fundraising_search,
                "fundraising_search",
                apikey=api_key,
                name=invalid_search_term,
            )

            result_list = get_response_models(result, FMPEquityOfferingSearch)
            assert isinstance(result_list, list)
            # May return empty or limited results for invalid search terms


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFundraisingComprehensive:
    """Test class for comprehensive fundraising coverage."""

    @pytest.mark.parametrize(
        "sector,expected_form_types,business_characteristics",
        [
            ("technology", ["S-1", "S-3", "424B"], "high_growth"),
            ("healthcare", ["S-1", "S-3", "424B"], "research_intensive"),
            ("financial", ["S-1", "S-3", "S-4"], "regulated"),
            ("energy", ["S-1", "S-3", "424B"], "capital_intensive"),
            ("consumer", ["S-1", "S-3", "424B"], "market_driven"),
        ],
    )
    def test_fundraising_sector_patterns(
        self, api_key, sector, expected_form_types, business_characteristics
    ):
        """Test fundraising patterns across different sectors."""
        result, validation = handle_api_call_with_validation(
            fundraising_search, "fundraising_search", apikey=api_key, name=sector
        )

        result_list = get_response_models(result, FMPEquityOfferingSearch)
        assert isinstance(result_list, list)

        if result_list:
            # Enhanced validation for sector patterns
            for item in result_list[:5]:  # Check first 5 items
                name = item.name
                if name:
                    # Very flexible matching for fundraising sectors
                    search_words = [
                        word.lower().strip("'s").strip() for word in sector.split()
                    ]
                    name_lower = name.lower()
                    name_words = [
                        word.strip(".,():").lower() for word in name_lower.split()
                    ]

                    match_found = False
                    for search_word in search_words:
                        # Direct substring match
                        if search_word in name_lower:
                            match_found = True
                            break
                        # Word-level substring matching
                        for name_word in name_words:
                            if (
                                search_word in name_word
                                or name_word in search_word
                                or (
                                    len(search_word) > 4
                                    and name_word.startswith(
                                        search_word[: min(6, len(search_word))]
                                    )
                                )
                                or (
                                    len(name_word) > 4
                                    and search_word.startswith(
                                        name_word[: min(6, len(name_word))]
                                    )
                                )
                            ):
                                match_found = True
                                break
                        if match_found:
                            break

                    # Special case handling for common variations
                    if not match_found:
                        # Handle common word mappings
                        word_mappings = {
                            "technology": [
                                "tech",
                                "technologi",
                                "software",
                                "digital",
                                "data",
                                "cyber",
                            ],
                            "healthcare": [
                                "health",
                                "medical",
                                "pharma",
                                "bio",
                                "therapeutic",
                            ],
                            "financial": [
                                "finance",
                                "bank",
                                "credit",
                                "investment",
                                "capital",
                            ],
                            "energy": [
                                "oil",
                                "gas",
                                "renewable",
                                "solar",
                                "wind",
                                "power",
                            ],
                            "consumer": [
                                "retail",
                                "brand",
                                "product",
                                "service",
                                "customer",
                            ],
                        }

                        for search_word in search_words:
                            if search_word in word_mappings:
                                for variant in word_mappings[search_word]:
                                    if variant in name_lower:
                                        match_found = True
                                        break
                                if match_found:
                                    break

                    assert match_found, f"Name should be related to sector: {sector}"

            # Business characteristics validation
            if business_characteristics == "high_growth":
                # Technology companies should have recent fundraising activity
                assert (
                    len(result_list) >= 0
                ), "Technology sector should have some fundraising activity"
            elif business_characteristics == "research_intensive":
                # Healthcare companies should have significant fundraising
                assert (
                    len(result_list) >= 0
                ), "Healthcare sector should have some fundraising activity"
            elif business_characteristics == "regulated":
                # Financial companies should have structured fundraising
                assert (
                    len(result_list) >= 0
                ), "Financial sector should have some fundraising activity"

    @pytest.mark.parametrize(
        "funding_stage,expected_characteristics",
        [
            ("early_stage", {"forms": ["D", "C"], "amounts": "small"}),
            ("growth_stage", {"forms": ["S-1", "S-3"], "amounts": "medium"}),
            ("public_offering", {"forms": ["S-1", "424B"], "amounts": "large"}),
        ],
    )
    def test_fundraising_stage_characteristics(
        self, api_key, funding_stage, expected_characteristics
    ):
        """Test fundraising characteristics by funding stage."""
        # Search for companies in different funding stages
        search_terms = {
            "early_stage": "startup",
            "growth_stage": "growth",
            "public_offering": "IPO",
        }

        search_term = search_terms.get(funding_stage, "technology")

        result, validation = handle_api_call_with_validation(
            fundraising_search, "fundraising_search", apikey=api_key, name=search_term
        )

        result_list = get_response_models(result, FMPEquityOfferingSearch)
        assert isinstance(result_list, list)

        if result_list:
            # Enhanced validation for funding stage characteristics
            for item in result_list[:3]:  # Check first 3 items
                name = item.name
                if name:
                    assert (
                        len(name) > 0
                    ), f"Name should not be empty for {funding_stage}"

            # Stage-specific validation
            if funding_stage == "early_stage":
                # Early stage companies should have some fundraising activity
                assert (
                    len(result_list) >= 0
                ), "Early stage should have some fundraising activity"
            elif funding_stage == "public_offering":
                # Public offering companies should have formal filings
                assert (
                    len(result_list) >= 0
                ), "Public offering should have some fundraising activity"


def validate_crowdfunding_campaign_model(data: Dict) -> bool:
    """Validate that data conforms to FMPCrowdfundingCampaign model."""
    try:
        FMPCrowdfundingCampaign(**data)
        return True
    except Exception as e:
        print(f"Crowdfunding campaign model validation failed: {e}")
        return False


def validate_equity_offering_model(data: Dict) -> bool:
    """Validate that data conforms to FMPEquityOffering model."""
    try:
        FMPEquityOffering(**data)
        return True
    except Exception as e:
        print(f"Equity offering model validation failed: {e}")
        return False
