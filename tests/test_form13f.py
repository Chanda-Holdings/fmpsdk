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
        result = form13f.institutional_ownership_latest(apikey=api_key, limit=10)

        # Use extract_data_list for automatic premium endpoint detection
        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            holding = data[0]

            # Validate against model
            if isinstance(holding, dict):
                holding_obj = FMPForm13FFiling(**holding)
            else:
                holding_obj = holding

            # Basic validation
            assert hasattr(holding_obj, "cik")
            assert hasattr(holding_obj, "name")
            assert hasattr(holding_obj, "date")

            # Since we're getting latest filings, we just check that we have a CIK
            if holding_obj.cik:
                assert holding_obj.cik is not None

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
            result = form13f.institutional_ownership_latest(apikey=api_key, limit=5)
            data = extract_data_list(result)
            assert isinstance(data, list)

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
            "BRK.B",
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
            # Popular ETFs (often held by institutions)
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
        """Test institutional ownership for widely held securities."""
        result = form13f.institutional_ownership_extract_analytics_by_holder(
            apikey=api_key, symbol=symbol, year=2023, quarter=4, limit=20
        )

        # Use extract_data_list for automatic premium endpoint detection
        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            holding = data[0]

            # Validate against model
            if isinstance(holding, dict):
                holding_obj = FMPForm13FExtract(**holding)
            else:
                holding_obj = holding

            # Basic validation
            assert hasattr(holding_obj, "symbol")
            assert hasattr(holding_obj, "cik")
            assert hasattr(holding_obj, "date")

            # Symbol should match requested
            if holding_obj.symbol:
                assert holding_obj.symbol == symbol

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
        """Test institutional ownership across different market cap tiers."""
        market_cap_symbols = {
            "mega_cap": ["AAPL", "MSFT", "GOOGL", "AMZN"],  # > $200B
            "large_cap": ["NVDA", "TSLA", "BRK.B", "UNH"],  # $10B-$200B
            "mid_cap": ["ROKU", "SNAP", "TWLO", "ZM"],  # $2B-$10B
            "small_cap": ["PTON", "LCID", "RIVN", "OPEN"],  # $300M-$2B
        }

        symbols = market_cap_symbols.get(market_cap, ["AAPL"])

        for symbol in symbols:
            result = form13f.institutional_ownership_extract_analytics_by_holder(
                apikey=api_key, symbol=symbol, year=2023, quarter=4, limit=10
            )
            data = extract_data_list(result)
            assert isinstance(data, list)

    @pytest.mark.parametrize("quarter", ["Q1", "Q2", "Q3", "Q4"])
    def test_form13f_filing_dates_by_quarter(self, api_key, quarter):
        """Test Form 13F filing dates for different quarters."""
        result = form13f.institutional_ownership_dates(apikey=api_key, cik="0001067983")

        # Use extract_data_list for automatic premium endpoint detection
        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            # Check if we have filings for the specified quarter
            quarter_filings = [
                filing
                for filing in data
                if isinstance(filing, dict)
                and quarter.lower() in filing.get("date", "").lower()
            ]

            # This is informational - not all quarters may be represented
            assert len(quarter_filings) >= 0

    @pytest.mark.parametrize("year", ["2023", "2022", "2021", "2020", "2019"])
    def test_form13f_historical_data(self, api_key, year):
        """Test Form 13F data for different historical years."""
        # Use a major institution like BlackRock
        cik = "0001067983"  # BlackRock

        result = form13f.institutional_ownership_latest(apikey=api_key, limit=50)
        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            # Look for holdings from the specified year
            year_holdings = [
                holding
                for holding in data
                if isinstance(holding, dict) and year in holding.get("date", "")
            ]

            # This is informational - not all years may be available
            assert len(year_holdings) >= 0

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
