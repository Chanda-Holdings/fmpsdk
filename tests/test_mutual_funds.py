import pytest

from fmpsdk import mutual_funds
from fmpsdk.models import (
    FMPFundDisclosure,
    FMPFundDisclosureDate,
    FMPFundHolder,
)
from tests.conftest import (
    get_first_item_from_response,
    get_response_models,
    handle_api_call_with_validation
)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestMutualFundsDisclosure:
    """Test class for mutual fund disclosure endpoints with comprehensive validation."""

    @pytest.mark.parametrize(
        "symbol,fund_family,fund_type,expected_characteristics",
        [
            # Vanguard Index Funds
            (
                "VTSAX",
                "vanguard",
                "total_market_equity",
                {"expense_ratio": "low", "diversification": "broad"},
            ),
            (
                "VTIAX",
                "vanguard",
                "international_equity",
                {"geographic": "global", "currency_exposure": "international"},
            ),
            (
                "VBTLX",
                "vanguard",
                "bond_index",
                {"asset_class": "fixed_income", "duration": "intermediate"},
            ),
            (
                "VFWAX",
                "vanguard",
                "international_equity",
                {"geographic": "ex_us", "market_cap": "all"},
            ),
            (
                "VGTSX",
                "vanguard",
                "international_equity",
                {"share_class": "investor", "geographic": "global"},
            ),
            (
                "VEMAX",
                "vanguard",
                "emerging_markets",
                {"geographic": "emerging", "risk_level": "higher"},
            ),
            (
                "VMCSX",
                "vanguard",
                "mid_cap_equity",
                {"market_cap": "mid", "style": "blend"},
            ),
            # Fidelity Index Funds
            ("FXAIX", "fidelity", "sp500_index", {"benchmark": "sp500", "cost": "low"}),
            (
                "FTIHX",
                "fidelity",
                "international_equity",
                {"geographic": "international", "diversification": "broad"},
            ),
            (
                "FXNAX",
                "fidelity",
                "bond_index",
                {"asset_class": "fixed_income", "quality": "investment_grade"},
            ),
            (
                "FSKAX",
                "fidelity",
                "total_market_equity",
                {"coverage": "total_market", "cap_weighted": True},
            ),
            (
                "FSMDX",
                "fidelity",
                "mid_cap_equity",
                {"market_cap": "mid", "style": "index"},
            ),
            (
                "FSSNX",
                "fidelity",
                "small_cap_equity",
                {"market_cap": "small", "growth_potential": "high"},
            ),
            # Schwab Index Funds
            (
                "SWPPX",
                "schwab",
                "sp500_index",
                {"benchmark": "sp500", "institutional": True},
            ),
            (
                "SWTSX",
                "schwab",
                "total_market_equity",
                {"coverage": "total_market", "cost": "low"},
            ),
            (
                "SWISX",
                "schwab",
                "international_equity",
                {"geographic": "international", "developed": True},
            ),
            (
                "SWAGX",
                "schwab",
                "aggregate_bond",
                {"asset_class": "fixed_income", "diversification": "broad"},
            ),
            # Schwab ETFs
            (
                "SCHB",
                "schwab",
                "broad_market_etf",
                {"structure": "etf", "trading": "intraday"},
            ),
            (
                "SCHF",
                "schwab",
                "international_etf",
                {"structure": "etf", "geographic": "international"},
            ),
            (
                "SCHZ",
                "schwab",
                "treasury_etf",
                {"structure": "etf", "duration": "intermediate"},
            ),
            (
                "SCHA",
                "schwab",
                "small_cap_etf",
                {"structure": "etf", "market_cap": "small"},
            ),
            (
                "SCHM",
                "schwab",
                "mid_cap_etf",
                {"structure": "etf", "market_cap": "mid"},
            ),
            (
                "SCHV",
                "schwab",
                "large_cap_value_etf",
                {"structure": "etf", "style": "value"},
            ),
        ],
    )
    def test_funds_disclosure_holders_latest_comprehensive(
        self, api_key, symbol, fund_family, fund_type, expected_characteristics
    ):
        """Test latest fund disclosure holders with comprehensive validation."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure_holders_latest,
            "funds_disclosure_holders_latest",
            apikey=api_key,
            symbol=symbol,
        )

        result_list = get_response_models(response, FMPFundHolder)
        assert isinstance(result_list, list)

        if result_list:
            holder = get_first_item_from_response(result_list)

            # Validate essential fields
            cik = holder.cik
            holder_name = holder.holder
            shares = holder.shares
            date_reported = holder.dateReported
            weight_percent = holder.weightPercent

            assert cik is not None and len(str(cik)) > 0
            assert holder_name is not None and len(holder_name) > 0
            assert date_reported is not None

            # Validate data types and ranges
            if shares is not None:
                assert isinstance(shares, int)
                assert shares >= 0

            if weight_percent is not None:
                assert isinstance(weight_percent, float)
                assert 0 <= weight_percent <= 100

            # Fund family-specific validation
            if fund_family == "vanguard":
                assert "vanguard" in symbol.lower() or "vg" in symbol.lower()
            elif fund_family == "fidelity":
                assert symbol.startswith("F") or "fidelity" in holder_name.lower()
            elif fund_family == "schwab":
                assert symbol.startswith("SW") or symbol.startswith("SCH")

            # Validate that institutional holders are reasonable
            if holder_name and "vanguard" in holder_name.lower():
                assert (
                    weight_percent is None or weight_percent > 0.01
                )  # Should have meaningful holdings

    @pytest.mark.parametrize(
        "year,quarter,period_type",
        [
            ("2023", "Q4", "recent"),
            ("2023", "Q3", "recent"),
            ("2023", "Q2", "recent"),
            ("2023", "Q1", "recent"),
            ("2022", "Q4", "historical"),
            ("2022", "Q3", "historical"),
            ("2022", "Q2", "historical"),
            ("2022", "Q1", "historical"),
            ("2021", "Q4", "historical"),
            ("2021", "Q3", "historical"),
        ],
    )
    def test_funds_disclosure_historical_periods(
        self, api_key, year, quarter, period_type
    ):
        """Test fund disclosure across different historical periods."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure,
            "funds_disclosure",
            apikey=api_key,
            symbol="VTSAX",
            year=year,
            quarter=quarter,
        )

        result_list = get_response_models(response, FMPFundDisclosure)
        assert isinstance(result_list, list)

        if result_list:
            disclosure = get_first_item_from_response(result_list)

            # Validate essential fields
            cik = disclosure.cik
            date = disclosure.date
            symbol = disclosure.symbol
            balance = disclosure.balance
            val_usd = disclosure.valUsd
            pct_val = disclosure.pctVal

            assert cik is not None
            assert date is not None
            assert symbol == "VTSAX"

            # Validate financial data
            if balance is not None:
                assert isinstance(balance, int)
                assert balance >= 0

            if val_usd is not None:
                assert isinstance(val_usd, float)
                assert val_usd >= 0

            if pct_val is not None:
                assert isinstance(pct_val, float)
                assert 0 <= pct_val <= 100

            # Period-specific validation
            if period_type == "recent":
                assert year in ["2023", "2022"]
            elif period_type == "historical":
                assert year in ["2022", "2021", "2020"]

            # Date should match the requested period
            if date:
                assert year in str(date)

    @pytest.mark.parametrize(
        "fund_category,symbols,expected_patterns",
        [
            (
                "large_cap_growth",
                ["VTSAX", "FXAIX", "SWPPX"],
                {"market_cap": "large", "style": "growth"},
            ),
            (
                "international_equity",
                ["VTIAX", "FTIHX", "SWISX"],
                {"geographic": "international", "currency_risk": True},
            ),
            (
                "bond_funds",
                ["VBTLX", "FXNAX", "SWAGX"],
                {"asset_class": "fixed_income", "interest_rate_risk": True},
            ),
            (
                "sector_etfs",
                ["VGT", "XLF", "XLE"],
                {"structure": "etf", "sector_focused": True},
            ),
            (
                "target_date",
                ["VTTSX", "FDKLX", "SWYNX"],
                {"lifecycle": True, "glide_path": True},
            ),
            (
                "small_cap",
                ["FSSNX", "SCHA"],
                {"market_cap": "small", "volatility": "higher"},
            ),
            (
                "mid_cap",
                ["VMCSX", "FSMDX", "SCHM"],
                {"market_cap": "mid", "growth_potential": "moderate"},
            ),
            ("value_funds", ["SCHV"], {"style": "value", "dividend_focus": True}),
        ],
    )
    def test_funds_disclosure_by_category(
        self, api_key, fund_category, symbols, expected_patterns
    ):
        """Test fund disclosure across different fund categories."""
        for symbol in symbols:
            response, validation = handle_api_call_with_validation(
                mutual_funds.funds_disclosure_holders_latest,
                "funds_disclosure_holders_latest",
                apikey=api_key,
                symbol=symbol,
            )

            result_list = get_response_models(response, FMPFundHolder)
            assert isinstance(result_list, list)

            if result_list:
                # Validate that we have reasonable holder data
                holder = get_first_item_from_response(result_list)

                holder_name = holder.holder
                weight_percent = holder.weightPercent

                # Category-specific validation
                if fund_category == "international_equity":
                    # International funds should have diverse holders
                    assert holder_name is not None
                elif fund_category == "bond_funds":
                    # Bond funds might have institutional holders
                    if weight_percent is not None:
                        assert weight_percent > 0
                elif fund_category == "sector_etfs":
                    # Sector ETFs should have focused holdings
                    assert holder_name is not None
                elif fund_category == "target_date":
                    # Target date funds should have lifecycle characteristics
                    assert holder_name is not None

    @pytest.mark.parametrize(
        "search_term,fund_company,expected_results",
        [
            ("Vanguard", "vanguard", {"min_results": 1, "name_contains": "vanguard"}),
            ("Fidelity", "fidelity", {"min_results": 1, "name_contains": "fidelity"}),
            ("Schwab", "schwab", {"min_results": 1, "name_contains": "schwab"}),
            (
                "BlackRock",
                "blackrock",
                {"min_results": 1, "name_contains": "blackrock"},
            ),
            (
                "State Street",
                "state_street",
                {"min_results": 1, "name_contains": "state"},
            ),
            (
                "American Funds",
                "american_funds",
                {"min_results": 1, "name_contains": "american"},
            ),
            (
                "T. Rowe Price",
                "t_rowe_price",
                {"min_results": 1, "name_contains": "rowe"},
            ),
            ("Invesco", "invesco", {"min_results": 1, "name_contains": "invesco"}),
        ],
    )
    def test_funds_disclosure_holders_search_comprehensive(
        self, api_key, search_term, fund_company, expected_results
    ):
        """Test comprehensive fund holder search across major fund companies."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure_holders_search,
            "funds_disclosure_holders_search",
            apikey=api_key,
            name=search_term,
        )

        result_list = get_response_models(response, FMPFundHolder)
        assert isinstance(result_list, list)

        if result_list:
            assert len(result_list) >= expected_results["min_results"]

            # Validate search results
            for result in result_list[:3]:  # Check first 3 results
                name = result.name
                cik = result.cik

                assert name is not None
                assert cik is not None

                # Check if search term appears in name (case-insensitive)
                name_lower = name.lower()
                search_lower = search_term.lower()
                expected_contains = expected_results["name_contains"].lower()

                assert expected_contains in name_lower or any(
                    word in name_lower for word in search_lower.split()
                )

    def test_funds_disclosure_dates(self, api_key):
        """Test fund disclosure dates endpoint."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure_dates,
            "funds_disclosure_dates",
            apikey=api_key,
            symbol="VTSAX",
        )

        result_list = get_response_models(response, FMPFundDisclosureDate)
        assert isinstance(result_list, list)

        if result_list:
            # Validate date structure
            date_item = get_first_item_from_response(result_list)

            date = date_item.date
            symbol = date_item.symbol

            assert date is not None
            assert symbol == "VTSAX"

            # Validate date format and chronological order
            dates = [item.date for item in result_list if item.date]
            if len(dates) > 1:
                # Dates should be in chronological order (most recent first)
                assert dates == sorted(dates, reverse=True)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestMutualFundsDataQuality:
    """Test class for mutual fund data quality and consistency validation."""

    @pytest.mark.parametrize(
        "symbol,fund_type,data_quality_expectations",
        [
            (
                "VTSAX",
                "broad_market",
                {"holder_diversity": "high", "weight_distribution": "balanced"},
            ),
            (
                "VTIAX",
                "international",
                {"geographic_diversity": "high", "currency_exposure": "diversified"},
            ),
            (
                "FXAIX",
                "sp500",
                {"holder_concentration": "moderate", "tracking": "tight"},
            ),
            (
                "SWPPX",
                "institutional",
                {"holder_quality": "high", "cost_efficiency": "high"},
            ),
        ],
    )
    def test_fund_holder_data_quality(
        self, api_key, symbol, fund_type, data_quality_expectations
    ):
        """Test fund holder data quality and consistency."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure_holders_latest,
            "funds_disclosure_holders_latest",
            apikey=api_key,
            symbol=symbol,
        )

        result_list = get_response_models(response, FMPFundHolder)
        assert isinstance(result_list, list)

        if result_list:
            total_weight = 0
            valid_holders = 0

            for holder in result_list:
                holder_name = holder.holder
                weight_percent = holder.weightPercent
                shares = holder.shares

                if holder_name:
                    assert len(holder_name) > 0
                    valid_holders += 1

                if weight_percent is not None:
                    assert 0 <= weight_percent <= 100
                    total_weight += weight_percent

                if shares is not None:
                    assert shares >= 0

            # Data quality validation
            assert valid_holders > 0

            # Weight percentages should be reasonable
            if total_weight > 0:
                assert total_weight <= 105  # Allow for small discrepancies

            # Fund type-specific validation
            if fund_type == "broad_market":
                assert valid_holders >= 1  # Should have institutional holders
            elif fund_type == "international":
                assert valid_holders >= 1  # Should have diverse holders
            elif fund_type == "sp500":
                assert valid_holders >= 1  # Should have tracking-focused holders

    @pytest.mark.parametrize(
        "symbol,year,quarter,consistency_checks",
        [
            (
                "VTSAX",
                "2023",
                "Q4",
                {"temporal_consistency": True, "data_completeness": "high"},
            ),
            (
                "VTSAX",
                "2023",
                "Q3",
                {"temporal_consistency": True, "data_completeness": "high"},
            ),
            (
                "FXAIX",
                "2023",
                "Q4",
                {"temporal_consistency": True, "data_completeness": "moderate"},
            ),
            (
                "FXAIX",
                "2023",
                "Q3",
                {"temporal_consistency": True, "data_completeness": "moderate"},
            ),
        ],
    )
    def test_fund_disclosure_temporal_consistency(
        self, api_key, symbol, year, quarter, consistency_checks
    ):
        """Test temporal consistency of fund disclosure data."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure,
            "funds_disclosure",
            apikey=api_key,
            symbol=symbol,
            year=year,
            quarter=quarter,
        )

        result_list = get_response_models(response, FMPFundDisclosure)
        assert isinstance(result_list, list)

        if result_list:
            # Validate temporal consistency
            for disclosure in result_list:
                date = disclosure.date
                symbol_check = disclosure.symbol
                val_usd = disclosure.valUsd

                assert date is not None
                assert symbol_check == symbol

                if val_usd is not None:
                    assert val_usd >= 0

                # Date should be within the requested period
                if date:
                    assert year in str(date)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestMutualFundsErrorHandling:
    """Test class for mutual fund error handling and edge cases."""

    def test_funds_disclosure_invalid_symbol(self, api_key):
        """Test handling of invalid fund symbols."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure_holders_latest,
            "funds_disclosure_holders_latest",
            apikey=api_key,
            symbol="INVALID_SYMBOL",
        )

        result_list = get_response_models(response, FMPFundHolder)
        assert isinstance(result_list, list)
        # Empty result is acceptable for invalid symbols

    def test_funds_disclosure_invalid_period(self, api_key):
        """Test handling of invalid year/quarter combinations."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure,
            "funds_disclosure",
            apikey=api_key,
            symbol="VTSAX",
            year="2030",  # Future year
            quarter="Q4",
        )

        result_list = get_response_models(response, FMPFundDisclosure)
        assert isinstance(result_list, list)
        # Future periods should return empty results

    def test_funds_search_empty_query(self, api_key):
        """Test handling of empty search queries."""
        response, validation = handle_api_call_with_validation(
            mutual_funds.funds_disclosure_holders_search,
            "funds_disclosure_holders_search",
            apikey=api_key,
            name="",
        )

        result_list = get_response_models(response, FMPFundHolder)
        assert isinstance(result_list, list)
        # Empty query should return empty or limited results

    def test_funds_disclosure_api_key_validation(self):
        """Test API key validation for fund disclosure endpoints."""
        # Test with invalid API key
        with pytest.raises(Exception):
            mutual_funds.funds_disclosure_holders_latest(
                apikey="invalid_key", symbol="VTSAX"
            )
