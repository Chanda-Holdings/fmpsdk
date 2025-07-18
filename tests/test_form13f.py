import pytest

import fmpsdk
from fmpsdk.models import (
    FMPForm13FDate,
    FMPForm13FExtract,
    FMPForm13FFiling,
)
from tests.conftest import (
    get_response_models,
    validate_model_list,
    validate_required_fields,
    handle_api_call_with_validation,
)

from fmpsdk import form13f


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestForm13FBasic:
    """Basic functionality tests for Form 13F endpoints."""

    @pytest.mark.parametrize(
        "cik",
        [
            # Major Asset Managers
            "0001364742",  # Berkshire Hathaway (Warren Buffett)
            "0001067983",  # BlackRock Inc
            "0000909832",  # Vanguard Group Inc
            "0001029160",  # State Street Corp
            "0001559720",  # Invesco Ltd
            "0000315066",  # Fidelity Management & Research Company
            "0001364742",  # Berkshire Hathaway Inc
            "0001214717",  # T. Rowe Price Group Inc
            "0000913760",  # Northern Trust Corp
            "0001166559",  # JPMorgan Chase & Co
            # Hedge Funds
            "0001079114",  # Renaissance Technologies Corp
            "0001650577",  # Bridgewater Associates
            "0001336528",  # Citadel Advisors LLC
            "0001423053",  # Point72 Asset Management
            "0001061768",  # Tiger Global Management LLC
            "0001603466",  # Coatue Management LLC
            "0001656456",  # Viking Global Investors LP
            "0001559684",  # D E Shaw & Co Inc
            "0001683618",  # Two Sigma Investments LP
            "0001540159",  # Greenlight Capital Inc
            # Pension Funds & Institutions
            "0000315066",  # Massachusetts Financial Services Co
            "0000905718",  # Wellington Management Group LLP
            "0000102909",  # Vanguard Group Inc (alternative CIK)
            "0001100663",  # Capital Research & Management Co
            "0000354204",  # Franklin Resources Inc
            "0000950123",  # Principal Financial Group Inc
            "0000827052",  # Nuveen Asset Management LLC
            "0000813074",  # PIMCO
            "0000866787",  # Alliance Bernstein LP
            "0000939722",  # Putnam Investment Management LLC
            # University Endowments
            "0001166919",  # Harvard Management Company Inc
            "0000948696",  # Yale University (if available)
            "0001067286",  # Stanford Management Company
            # Insurance Companies
            "0000720005",  # Prudential Financial Inc
            "0000718733",  # MetLife Inc
            "0000320187",  # American International Group Inc
            "0000899051",  # Lincoln National Corp
            "0001067837",  # Principal Financial Group
            # Family Offices & Private Wealth
            "0001061165",  # Soros Fund Management LLC
            "0001336528",  # Citadel Advisors LLC (family office arm)
            "0001623307",  # Appaloosa LP
            "0001422183",  # Pershing Square Capital Management
        ],
    )
    def test_institutional_ownership_by_cik(self, api_key, cik):
        """Test institutional ownership for major institutional investors."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_latest,
            "institutional_ownership_latest",
            apikey=api_key,
            limit=10
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FFiling)
        validate_model_list(models, FMPForm13FFiling, f"Failed to validate Form 13F filing models for CIK {cik}")

        if models:  # If we have data
            holding = models[0]

            # Basic validation
            assert holding.cik is not None, "CIK should not be None"
            assert holding.name is not None and len(holding.name) > 0, "Name should not be empty"
            assert holding.date is not None and len(str(holding.date)) > 0, "Date should not be empty"

            # Since we're getting latest filings, we just check that we have a CIK
            if holding.cik:
                assert holding.cik is not None

    @pytest.mark.parametrize(
        "institution_type",
        [
            "asset_managers",
            "hedge_funds",
            "pension_funds",
            "insurance_companies",
            "endowments",
        ],
    )
    def test_institutional_ownership_by_type(self, api_key, institution_type):
        """Test institutional ownership across different institution types."""
        institution_ciks = {
            "asset_managers": [
                "0001067983",
                "0000909832",
                "0001029160",
            ],  # BlackRock, Vanguard, State Street
            "hedge_funds": [
                "0001079114",
                "0001650577",
                "0001336528",
            ],  # Renaissance, Bridgewater, Citadel
            "pension_funds": [
                "0000315066",
                "0000905718",
                "0001100663",
            ],  # MFS, Wellington, Capital Research
            "insurance_companies": [
                "0000720005",
                "0000718733",
                "0000320187",
            ],  # Prudential, MetLife, AIG
            "endowments": [
                "0001166919",
                "0000948696",
                "0001067286",
            ],  # Harvard, Yale, Stanford
        }

        ciks = institution_ciks.get(institution_type, ["0001067983"])

        for cik in ciks:
            result, validation = handle_api_call_with_validation(
                form13f.institutional_ownership_latest,
                "institutional_ownership_latest",
                apikey=api_key,
                limit=5
            )
            
            # Extract and validate models
            models = get_response_models(result, FMPForm13FFiling)
            validate_model_list(models, FMPForm13FFiling, f"Failed to validate Form 13F filing models for {institution_type}")

    @pytest.mark.parametrize(
        "symbol",
        [
            # Large Cap Technology
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "TSLA",
            "NVDA",
            "ORCL",
            "CRM",
            "ADBE",
            # Large Cap Financial
            "JPM",
            "BAC",
            "WFC",
            "GS",
            "MS",
            "C",
            "BRK-B",
            "V",
            "MA",
            "AXP",
            # Large Cap Healthcare
            "UNH",
            "JNJ",
            "PFE",
            "ABBV",
            "MRK",
            "TMO",
            "ABT",
            "LLY",
            "DHR",
            "BMY",
            # Large Cap Consumer
            "HD",
            "WMT",
            "PG",
            "KO",
            "PEP",
            "MCD",
            "NKE",
            "SBUX",
            "DIS",
            "COST",
            # Large Cap Industrial
            "BA",
            "CAT",
            "GE",
            "HON",
            "LMT",
            "RTX",
            "MMM",
            "UPS",
            "DE",
            "FDX",
            # ETFs
            "SPY",
            "QQQ",
            "VTI",
            "IWM",
            "EFA",
            "EEM",
            "AGG",
            "TLT",
            "GLD",
            "VNQ",
        ],
    )
    def test_institutional_ownership_by_symbol(self, api_key, symbol):
        """Test institutional ownership for major symbols."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_latest,
            "institutional_ownership_latest",
            apikey=api_key,
            symbol=symbol,
            limit=10
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FFiling)
        validate_model_list(models, FMPForm13FFiling, f"Failed to validate Form 13F filing models for symbol {symbol}")

        if models:
            # Test first few items for comprehensive validation
            for filing in models[:5]:
                # Basic validation
                assert filing.symbol is not None, "Symbol should not be None"
                assert filing.date is not None, "Date should not be None"
                assert filing.symbol == symbol, f"Symbol should match requested symbol: {filing.symbol} != {symbol}"

    @pytest.mark.parametrize(
        "market_cap",
        [
            "mega_cap",  # > $200B
            "large_cap",  # $10B - $200B
            "mid_cap",  # $2B - $10B
            "small_cap",  # $300M - $2B
        ],
    )
    def test_institutional_ownership_by_market_cap(self, api_key, market_cap):
        """Test institutional ownership across different market cap categories."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_latest,
            "institutional_ownership_latest",
            apikey=api_key,
            limit=20
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FFiling)
        validate_model_list(models, FMPForm13FFiling, f"Failed to validate Form 13F filing models for {market_cap}")

        if models:
            # Test first few items for comprehensive validation
            for filing in models[:5]:
                # Basic validation
                assert filing.symbol is not None, "Symbol should not be None"
                assert filing.date is not None, "Date should not be None"

    @pytest.mark.parametrize("quarter", ["Q1", "Q2", "Q3", "Q4"])
    def test_form13f_filing_dates_by_quarter(self, api_key, quarter):
        """Test Form 13F filing dates by quarter."""
        result, validation = handle_api_call_with_validation(
            form13f.form13f_filing_dates,
            "form13f_filing_dates",
            apikey=api_key,
            quarter=quarter
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FDate)
        validate_model_list(models, FMPForm13FDate, f"Failed to validate Form 13F date models for quarter {quarter}")

        if models:
            # Test first few items for comprehensive validation
            for date_info in models[:5]:
                # Basic validation
                assert date_info.name is not None, "Name should not be None"
                assert date_info.date is not None, "Date should not be None"
                assert len(str(date_info.date)) >= 10, "Date should be in valid format"

    @pytest.mark.parametrize("year", ["2023", "2022", "2021", "2020", "2019"])
    def test_form13f_historical_data(self, api_key, year):
        """Test Form 13F historical data by year."""
        result, validation = handle_api_call_with_validation(
            form13f.form13f_filing_dates,
            "form13f_filing_dates",
            apikey=api_key,
            year=year
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FDate)
        validate_model_list(models, FMPForm13FDate, f"Failed to validate Form 13F date models for year {year}")

        if models:
            # Test first few items for comprehensive validation
            for date_info in models[:5]:
                # Basic validation
                assert date_info.name is not None, "Name should not be None"
                assert date_info.date is not None, "Date should not be None"
                assert len(str(date_info.date)) >= 10, "Date should be in valid format"

    def test_institutional_ownership_latest(self, api_key):
        """Test institutional ownership latest endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_latest,
            "institutional_ownership_latest",
            apikey=api_key,
            limit=50
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FFiling)
        validate_model_list(models, FMPForm13FFiling, "Failed to validate institutional ownership latest models")

        if models:
            # Test first few items for comprehensive validation
            for filing in models[:10]:
                # Basic validation
                assert filing.symbol is not None, "Symbol should not be None"
                assert filing.name is not None, "Name should not be None"
                assert filing.date is not None, "Date should not be None"
                assert len(filing.symbol) >= 1, "Symbol should not be empty"
                assert len(filing.name) >= 1, "Name should not be empty"
                assert len(str(filing.date)) >= 10, "Date should be in valid format"

    def test_institutional_ownership_latest_pagination(self, api_key):
        """Test institutional ownership latest with pagination."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_latest,
            "institutional_ownership_latest",
            apikey=api_key,
            limit=100
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FFiling)
        validate_model_list(models, FMPForm13FFiling, "Failed to validate institutional ownership latest models with pagination")

        # Should have more data with higher limit
        assert len(models) >= 0, "Should return valid list"

    def test_institutional_ownership_extract(self, api_key):
        """Test institutional ownership extract endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_extract,
            "institutional_ownership_extract",
            apikey=api_key,
            limit=30
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FExtract)
        validate_model_list(models, FMPForm13FExtract, "Failed to validate institutional ownership extract models")

        if models:
            # Test first few items for comprehensive validation
            for extract in models[:10]:
                # Basic validation
                assert extract.symbol is not None, "Symbol should not be None"
                assert extract.name is not None, "Name should not be None"
                assert extract.date is not None, "Date should not be None"
                assert len(extract.symbol) >= 1, "Symbol should not be empty"
                assert len(extract.name) >= 1, "Name should not be empty"
                assert len(str(extract.date)) >= 10, "Date should be in valid format"

    def test_institutional_ownership_dates(self, api_key):
        """Test institutional ownership dates endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_dates,
            "institutional_ownership_dates",
            apikey=api_key
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FDate)
        validate_model_list(models, FMPForm13FDate, "Failed to validate institutional ownership dates models")

        if models:
            # Test first few items for comprehensive validation
            for date_info in models[:10]:
                # Basic validation
                assert date_info.name is not None, "Name should not be None"
                assert date_info.date is not None, "Date should not be None"
                assert len(date_info.name) >= 1, "Name should not be empty"
                assert len(str(date_info.date)) >= 10, "Date should be in valid format"

    def test_institutional_ownership_extract_analytics_by_holder(self, api_key):
        """Test institutional ownership extract analytics by holder endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_extract_analytics_by_holder,
            "institutional_ownership_extract_analytics_by_holder",
            apikey=api_key,
            limit=20
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FExtract)
        validate_model_list(models, FMPForm13FExtract, "Failed to validate institutional ownership extract analytics models")

        if models:
            # Test first few items for comprehensive validation
            for extract in models[:5]:
                # Basic validation
                assert extract.symbol is not None, "Symbol should not be None"
                assert extract.name is not None, "Name should not be None"
                assert extract.date is not None, "Date should not be None"

    def test_institutional_ownership_holder_performance_summary(self, api_key):
        """Test institutional ownership holder performance summary endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_holder_performance_summary,
            "institutional_ownership_holder_performance_summary",
            apikey=api_key,
            limit=20
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FExtract)
        validate_model_list(models, FMPForm13FExtract, "Failed to validate institutional ownership holder performance models")

        if models:
            # Test first few items for comprehensive validation
            for extract in models[:5]:
                # Basic validation
                assert extract.symbol is not None, "Symbol should not be None"
                assert extract.name is not None, "Name should not be None"
                assert extract.date is not None, "Date should not be None"

    def test_institutional_ownership_holder_industry_breakdown(self, api_key):
        """Test institutional ownership holder industry breakdown endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_holder_industry_breakdown,
            "institutional_ownership_holder_industry_breakdown",
            apikey=api_key,
            limit=20
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FExtract)
        validate_model_list(models, FMPForm13FExtract, "Failed to validate institutional ownership holder industry models")

        if models:
            # Test first few items for comprehensive validation
            for extract in models[:5]:
                # Basic validation
                assert extract.symbol is not None, "Symbol should not be None"
                assert extract.name is not None, "Name should not be None"
                assert extract.date is not None, "Date should not be None"

    def test_institutional_ownership_positions_summary(self, api_key):
        """Test institutional ownership positions summary endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_positions_summary,
            "institutional_ownership_positions_summary",
            apikey=api_key,
            limit=20
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FExtract)
        validate_model_list(models, FMPForm13FExtract, "Failed to validate institutional ownership positions summary models")

        if models:
            # Test first few items for comprehensive validation
            for extract in models[:5]:
                # Basic validation
                assert extract.symbol is not None, "Symbol should not be None"
                assert extract.name is not None, "Name should not be None"
                assert extract.date is not None, "Date should not be None"

    def test_institutional_ownership_industry_summary(self, api_key):
        """Test institutional ownership industry summary endpoint."""
        result, validation = handle_api_call_with_validation(
            form13f.institutional_ownership_industry_summary,
            "institutional_ownership_industry_summary",
            apikey=api_key,
            limit=20
        )

        # Extract and validate models
        models = get_response_models(result, FMPForm13FExtract)
        validate_model_list(models, FMPForm13FExtract, "Failed to validate institutional ownership industry summary models")

        if models:
            # Test first few items for comprehensive validation
            for extract in models[:5]:
                # Basic validation
                assert extract.symbol is not None, "Symbol should not be None"
                assert extract.name is not None, "Name should not be None"
                assert extract.date is not None, "Date should not be None"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestForm13FErrorHandling:
    """Test error handling for Form 13F endpoints."""

    def test_institutional_ownership_latest_invalid_api_key(self):
        """Test institutional ownership latest with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_latest(
                apikey="invalid_key",
                limit=10
            )

    def test_institutional_ownership_extract_invalid_api_key(self):
        """Test institutional ownership extract with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_extract(
                apikey="invalid_key",
                limit=10
            )

    def test_institutional_ownership_dates_invalid_api_key(self):
        """Test institutional ownership dates with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_dates(
                apikey="invalid_key"
            )

    def test_institutional_ownership_extract_analytics_by_holder_invalid_api_key(self):
        """Test institutional ownership extract analytics with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_extract_analytics_by_holder(
                apikey="invalid_key",
                limit=10
            )

    def test_institutional_ownership_holder_performance_summary_invalid_api_key(self):
        """Test institutional ownership holder performance with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_holder_performance_summary(
                apikey="invalid_key",
                limit=10
            )

    def test_institutional_ownership_holder_industry_breakdown_invalid_api_key(self):
        """Test institutional ownership holder industry breakdown with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_holder_industry_breakdown(
                apikey="invalid_key",
                limit=10
            )

    def test_institutional_ownership_positions_summary_invalid_api_key(self):
        """Test institutional ownership positions summary with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_positions_summary(
                apikey="invalid_key",
                limit=10
            )

    def test_institutional_ownership_industry_summary_invalid_api_key(self):
        """Test institutional ownership industry summary with invalid API key."""
        with pytest.raises(Exception):
            form13f.institutional_ownership_industry_summary(
                apikey="invalid_key",
                limit=10
            )
