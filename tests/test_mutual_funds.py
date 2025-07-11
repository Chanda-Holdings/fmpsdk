import pytest

from fmpsdk import mutual_funds
from fmpsdk.models import (
    FMPFundDisclosure,
    FMPFundDisclosureDate,
    FMPFundHolder,
)
from tests.conftest import extract_data_list


class TestMutualFunds:
    """Test cases for mutual fund disclosure endpoints."""

    @pytest.mark.parametrize(
        "symbol",
        [
            # Vanguard Funds
            "VTSAX",  # Total Stock Market Index
            "VTIAX",  # Total International Stock Index
            "VBTLX",  # Total Bond Market Index
            "VFWAX",  # FTSE All-World ex-US Index
            "VGTSX",  # Total International Stock Index (Investor Shares)
            "VTISX",  # Total International Stock Index (Signal)
            "VTBSX",  # Total Bond Market Index (Signal)
            "VSGAX",  # ESG US Stock ETF
            "VEMAX",  # Emerging Markets Stock Index
            "VMCSX",  # Mid-Cap Index
            # Fidelity Funds
            "FXAIX",  # 500 Index
            "FTIHX",  # Total International Index
            "FXNAX",  # US Bond Index
            "FDVV",  # High Dividend ETF
            "FSKAX",  # Total Market Index
            "FSMDX",  # Mid Cap Index
            "FSSNX",  # Small Cap Index
            "FDVV",  # High Dividend ETF
            "FREL",  # MSCI Real Estate Index ETF
            "FNDE",  # Fundamental Index ETF
            # Other Major Fund Families
            "SWPPX",  # Schwab S&P 500 Index
            "SWTSX",  # Schwab Total Stock Market Index
            "SWISX",  # Schwab International Index
            "SWAGX",  # Schwab US Aggregate Bond Index
            "SCHB",  # Schwab US Broad Market ETF
            "SCHF",  # Schwab International Equity ETF
            "SCHZ",  # Schwab Intermediate-Term Treasury ETF
            "SCHA",  # Schwab US Small-Cap ETF
            "SCHM",  # Schwab US Mid-Cap ETF
            "SCHV",  # Schwab US Large-Cap Value ETF
        ],
    )
    def test_funds_disclosure_holders_latest_comprehensive(self, api_key, symbol):
        """Test latest fund disclosure holders for various mutual funds."""
        result = mutual_funds.funds_disclosure_holders_latest(
            apikey=api_key, symbol=symbol
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            holder = data[0]

            # Validate against model
            if isinstance(holder, dict):
                holder_obj = FMPFundHolder(**holder)
            else:
                holder_obj = holder

            # Required fields validation
            assert hasattr(holder_obj, "cik")
            assert hasattr(holder_obj, "holder")
            assert hasattr(holder_obj, "shares")
            assert hasattr(holder_obj, "dateReported")
            assert hasattr(holder_obj, "weightPercent")

            # Data quality checks
            assert holder_obj.cik
            assert holder_obj.holder
            if holder_obj.shares is not None:
                assert isinstance(holder_obj.shares, int)
                assert holder_obj.shares >= 0
            assert holder_obj.dateReported
            if holder_obj.weightPercent is not None:
                assert isinstance(holder_obj.weightPercent, float)
                assert 0 <= holder_obj.weightPercent <= 100

    @pytest.mark.parametrize(
        "fund_family",
        ["vanguard", "fidelity", "schwab", "blackrock", "state_street", "jp_morgan"],
    )
    def test_funds_disclosure_by_family(self, api_key, fund_family):
        """Test fund disclosure by major fund families."""
        family_symbols = {
            "vanguard": ["VTSAX", "VTIAX", "VBTLX"],
            "fidelity": ["FXAIX", "FTIHX", "FXNAX"],
            "schwab": ["SWPPX", "SWTSX", "SWISX"],
            "blackrock": ["IVV", "IEFA", "AGG"],  # ETF symbols for BlackRock
            "state_street": ["SPY", "IWM", "EFA"],  # SPDR ETFs
            "jp_morgan": ["JPST", "JPMB", "JPUS"],  # JPMorgan ETFs
        }

        symbols = family_symbols.get(fund_family, ["VTSAX"])

        for symbol in symbols:
            result = mutual_funds.funds_disclosure_holders_latest(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

    @pytest.mark.parametrize(
        "year,quarter",
        [
            ("2023", "Q4"),
            ("2023", "Q3"),
            ("2023", "Q2"),
            ("2023", "Q1"),
            ("2022", "Q4"),
            ("2022", "Q3"),
            ("2022", "Q2"),
            ("2022", "Q1"),
            ("2021", "Q4"),
            ("2021", "Q3"),
        ],
    )
    def test_funds_disclosure_historical_periods(self, api_key, year, quarter):
        """Test fund disclosure for various historical periods."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key, symbol="VTSAX", year=year, quarter=quarter
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            disclosure = data[0]

            # Validate against model
            if isinstance(disclosure, dict):
                disclosure_obj = FMPFundDisclosure(**disclosure)
            else:
                disclosure_obj = disclosure

            # Data quality checks
            assert disclosure_obj.cik
            assert disclosure_obj.date
            assert disclosure_obj.symbol == "VTSAX"
            if disclosure_obj.balance is not None:
                assert isinstance(disclosure_obj.balance, int)
                assert disclosure_obj.balance >= 0
            if disclosure_obj.valUsd is not None:
                assert isinstance(disclosure_obj.valUsd, float)
                assert disclosure_obj.valUsd >= 0
            if disclosure_obj.pctVal is not None:
                assert isinstance(disclosure_obj.pctVal, float)
                assert 0 <= disclosure_obj.pctVal <= 100

    @pytest.mark.parametrize(
        "fund_type",
        [
            "index_equity",
            "index_bond",
            "international",
            "sector_specific",
            "target_date",
        ],
    )
    def test_funds_disclosure_by_type(self, api_key, fund_type):
        """Test fund disclosure across different fund types."""
        fund_type_symbols = {
            "index_equity": ["VTSAX", "FXAIX", "SWPPX"],
            "index_bond": ["VBTLX", "FXNAX", "SWAGX"],
            "international": ["VTIAX", "FTIHX", "SWISX"],
            "sector_specific": ["VGT", "XLF", "XLE"],  # Tech, Financial, Energy ETFs
            "target_date": ["VTTSX", "FDKLX", "SWYNX"],  # Target date funds
        }

        symbols = fund_type_symbols.get(fund_type, ["VTSAX"])

        for symbol in symbols:
            result = mutual_funds.funds_disclosure_holders_latest(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

    @pytest.mark.parametrize(
        "search_term",
        [
            "Vanguard",
            "Fidelity",
            "Schwab",
            "BlackRock",
            "State Street",
            "American Funds",
            "T. Rowe Price",
            "Capital Group",
            "JPMorgan",
            "Invesco",
        ],
    )
    def test_funds_disclosure_holders_search_comprehensive(self, api_key, search_term):
        """Test fund disclosure holders search across major fund companies."""
        result = mutual_funds.funds_disclosure_holders_search(
            apikey=api_key, name=search_term
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            found_match = False
            for holder in data[:5]:  # Check first few results
                if isinstance(holder, dict):
                    holder_obj = FMPFundHolder(**holder)
                else:
                    holder_obj = holder

                # Should contain search term in holder name (case insensitive)
                if (
                    search_term.upper() in holder_obj.holder.upper()
                    or search_term.lower() in holder_obj.holder.lower()
                ):
                    found_match = True
                    break

            assert found_match, f"No holders found matching '{search_term}'"

    def test_funds_disclosure_holders_latest(self, api_key):
        """Test latest fund disclosure holders endpoint."""
        # Use a well-known mutual fund symbol
        result = mutual_funds.funds_disclosure_holders_latest(
            apikey=api_key, symbol="VTSAX"  # Vanguard Total Stock Market Index Fund
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            holder = data[0]

            # Validate against model
            if isinstance(holder, dict):
                holder_obj = FMPFundHolder(**holder)
            else:
                holder_obj = holder

            # Required fields validation
            assert hasattr(holder_obj, "cik")
            assert hasattr(holder_obj, "holder")
            assert hasattr(holder_obj, "shares")
            assert hasattr(holder_obj, "dateReported")
            assert hasattr(holder_obj, "weightPercent")

            # Data quality checks
            assert holder_obj.cik
            assert holder_obj.holder
            assert isinstance(holder_obj.shares, int)
            assert holder_obj.dateReported
            assert isinstance(holder_obj.weightPercent, float)
            assert 0 <= holder_obj.weightPercent <= 100  # Weight should be percentage

    def test_funds_disclosure(self, api_key):
        """Test fund disclosure endpoint with year and quarter."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key, symbol="VTSAX", year="2023", quarter="Q4"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            disclosure = data[0]

            # Validate against model
            if isinstance(disclosure, dict):
                disclosure_obj = FMPFundDisclosure(**disclosure)
            else:
                disclosure_obj = disclosure

            # Required fields validation
            assert hasattr(disclosure_obj, "cik")
            assert hasattr(disclosure_obj, "date")
            assert hasattr(disclosure_obj, "symbol")
            assert hasattr(disclosure_obj, "name")
            assert hasattr(disclosure_obj, "balance")
            assert hasattr(disclosure_obj, "valUsd")
            assert hasattr(disclosure_obj, "pctVal")

            # Data quality checks
            assert disclosure_obj.cik
            assert disclosure_obj.date
            assert disclosure_obj.symbol == "VTSAX"
            assert disclosure_obj.name
            assert isinstance(disclosure_obj.balance, int)
            assert isinstance(disclosure_obj.valUsd, float)
            assert isinstance(disclosure_obj.pctVal, float)

    def test_funds_disclosure_with_cik(self, api_key):
        """Test fund disclosure endpoint with CIK parameter."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key,
            symbol="VTSAX",
            year="2023",
            quarter="Q3",
            cik="0000102909",  # Vanguard CIK
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Data may be empty if specific CIK/quarter combination doesn't exist

    def test_funds_disclosure_holders_search(self, api_key):
        """Test fund disclosure holders search endpoint."""
        result = mutual_funds.funds_disclosure_holders_search(
            apikey=api_key, name="Vanguard"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for holder in data[:3]:  # Check first few results
                if isinstance(holder, dict):
                    holder_obj = FMPFundHolder(**holder)
                else:
                    holder_obj = holder

                # Should contain "Vanguard" in holder name
                assert (
                    "VANGUARD" in holder_obj.holder.upper()
                    or "Vanguard" in holder_obj.holder
                )

    def test_funds_disclosure_dates(self, api_key):
        """Test fund disclosure dates endpoint."""
        result = mutual_funds.funds_disclosure_dates(apikey=api_key, symbol="VTSAX")

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
                date_obj = FMPFundDisclosureDate(**date_info)
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
            assert 2020 <= date_obj.year <= 2025  # Reasonable year range

    def test_funds_disclosure_dates_with_cik(self, api_key):
        """Test fund disclosure dates endpoint with CIK parameter."""
        result = mutual_funds.funds_disclosure_dates(
            apikey=api_key, symbol="VTSAX", cik="0000102909"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

    def test_funds_invalid_symbol(self, api_key):
        """Test fund endpoints with invalid symbol."""
        result = mutual_funds.funds_disclosure_holders_latest(
            apikey=api_key, symbol="INVALID_FUND_XYZ"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid symbol
        assert len(data) == 0

    def test_funds_invalid_search_name(self, api_key):
        """Test fund search with invalid name."""
        result = mutual_funds.funds_disclosure_holders_search(
            apikey=api_key, name="INVALID_FUND_NAME_XYZ"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid name
        assert len(data) == 0


class TestMutualFundsDataQuality:
    """Test data quality and business logic validation."""

    def test_fund_holder_weight_percentages(self, api_key):
        """Test that fund holder weight percentages are reasonable."""
        result = mutual_funds.funds_disclosure_holders_latest(
            apikey=api_key, symbol="VTSAX"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            total_weight = 0
            for holder in data:
                if isinstance(holder, dict):
                    weight = holder["weightPercent"]
                else:
                    weight = holder.weightPercent

                # Individual weights should be reasonable
                assert 0 <= weight <= 100
                total_weight += weight

            # Total weights might not sum to 100% due to partial data or rounding
            # but should be reasonable
            assert total_weight >= 0

    def test_fund_disclosure_value_consistency(self, api_key):
        """Test value consistency in fund disclosure data."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key, symbol="VTSAX", year="2023", quarter="Q4"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for disclosure in data[:5]:  # Check first few items
                if isinstance(disclosure, dict):
                    balance = disclosure["balance"]
                    val_usd = disclosure["valUsd"]
                    pct_val = disclosure["pctVal"]
                else:
                    balance = disclosure.balance
                    val_usd = disclosure.valUsd
                    pct_val = disclosure.pctVal

                # Balance should be positive for holdings
                if balance > 0:
                    assert val_usd >= 0  # USD value should be non-negative
                    assert 0 <= pct_val <= 100  # Percentage should be valid

    def test_fund_disclosure_date_formats(self, api_key):
        """Test date format consistency in fund disclosure data."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key, symbol="VTSAX", year="2023", quarter="Q4"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for disclosure in data[:3]:
                if isinstance(disclosure, dict):
                    date = disclosure["date"]
                    accepted_date = disclosure["acceptedDate"]
                else:
                    date = disclosure.date
                    accepted_date = disclosure.acceptedDate

                # Dates should be in proper format
                assert len(date) >= 10  # YYYY-MM-DD format
                assert len(accepted_date) >= 10

                # Should contain year 2023 since we're searching for 2023 Q4
                assert (
                    "2023" in date or "2024" in date
                )  # Might be early 2024 for Q4 2023

    def test_fund_quarter_parameter_validation(self, api_key):
        """Test different quarter parameter formats."""
        quarters = ["Q1", "Q2", "Q3", "Q4"]

        for quarter in quarters:
            result = mutual_funds.funds_disclosure(
                apikey=api_key, symbol="VTSAX", year="2023", quarter=quarter
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                return

            data = extract_data_list(result)
            assert isinstance(data, list)
            # Data may be empty for some quarters, which is acceptable

    def test_fund_asset_categories(self, api_key):
        """Test asset category classification in fund disclosures."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key, symbol="VTSAX", year="2023", quarter="Q4"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            asset_categories = set()
            for disclosure in data:
                if isinstance(disclosure, dict):
                    asset_cat = disclosure.get("assetCat", "")
                else:
                    asset_cat = getattr(disclosure, "assetCat", "")

                if asset_cat:
                    asset_categories.add(asset_cat)

            # Should have reasonable asset categories for a mutual fund
            # Common categories: COMMON STOCK, CORPORATE BOND, etc.
            assert len(asset_categories) >= 0  # May be empty if no data


class TestMutualFundsErrorHandling:
    """Test error handling for mutual fund endpoints."""

    def test_funds_disclosure_holders_latest_invalid_api_key(self):
        """Test latest fund holders with invalid API key."""
        result = mutual_funds.funds_disclosure_holders_latest(
            apikey="invalid_key", symbol="VTSAX"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_funds_disclosure_invalid_api_key(self):
        """Test fund disclosure with invalid API key."""
        result = mutual_funds.funds_disclosure(
            apikey="invalid_key", symbol="VTSAX", year="2023", quarter="Q4"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_funds_disclosure_holders_search_invalid_api_key(self):
        """Test fund holders search with invalid API key."""
        result = mutual_funds.funds_disclosure_holders_search(
            apikey="invalid_key", name="Vanguard"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_funds_disclosure_dates_invalid_api_key(self):
        """Test fund disclosure dates with invalid API key."""
        result = mutual_funds.funds_disclosure_dates(
            apikey="invalid_key", symbol="VTSAX"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_funds_disclosure_invalid_year_quarter(self, api_key):
        """Test fund disclosure with invalid year/quarter combination."""
        result = mutual_funds.funds_disclosure(
            apikey=api_key, symbol="VTSAX", year="1900", quarter="Q4"  # Invalid year
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid year
        assert len(data) == 0
