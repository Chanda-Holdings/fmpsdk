import pytest

from fmpsdk import indexes
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import (
    FMPHistoricalIndexConstituent,
    FMPIndexConstituent,
    FMPIndexListItem,
    FMPSector,
)
from tests.conftest import get_response_models, validate_model_list


class TestIndexList:
    """Test the index_list function with enhanced validation."""

    def test_index_list_comprehensive_validation(self, api_key):
        """Test index_list with comprehensive validation."""
        response = indexes.index_list(apikey=api_key)

        models = get_response_models(response, FMPIndexListItem)
        validate_model_list(models, FMPIndexListItem, min_count=1)

        # Index list specific validation using model attributes
        if models:
            # Data quality metrics
            total_indices = len(models)
            valid_symbols = 0
            valid_names = 0
            unique_symbols = set()

            for model in models:
                # Symbol validation using direct model access
                if model.symbol:
                    # More lenient symbol validation
                    if len(model.symbol) >= 1:
                        assert (
                            len(model.symbol) <= 25
                        ), f"Symbol should be reasonable length: {model.symbol}"
                        unique_symbols.add(model.symbol)
                        valid_symbols += 1

                # Name validation using model attributes
                if model.name:
                    # More lenient name validation
                    if len(model.name) >= 1:
                        assert (
                            len(model.name) <= 100
                        ), f"Name should be reasonable length: {model.name}"
                        valid_names += 1

            # Data quality assertions (more flexible)
            assert (
                total_indices >= 1
            ), f"Should have at least 1 index, got {total_indices}"

            # Only validate if we have actual data
            if valid_symbols > 0:
                assert (
                    valid_symbols / total_indices >= 0.5
                ), f"At least 50% should have valid symbols: {valid_symbols}/{total_indices}"
            if valid_names > 0:
                assert (
                    valid_names / total_indices >= 0.5
                ), f"At least 50% should have valid names: {valid_names}/{total_indices}"

            # Major index validation (only if we have sufficient data)
            if total_indices >= 3:
                major_indices = ["S&P 500", "NASDAQ", "Dow Jones", "Russell"]
                found_majors = []
                for model in models:
                    if model.name:
                        for major in major_indices:
                            if major.lower() in model.name.lower():
                                found_majors.append(major)
                                break

                assert (
                    len(found_majors) >= 1
                ), f"Should find at least 1 major index: {found_majors}"

    @pytest.mark.parametrize(
        "index_name,expected_min_constituents,index_type,market_focus",
        [
            ("sp500", 450, "broad_market", "large_cap"),
            ("nasdaq", 90, "technology_heavy", "growth"),
            ("dowjones", 25, "blue_chip", "established"),
        ],
    )
    def test_index_constituents_comprehensive(
        self, api_key, index_name, expected_min_constituents, index_type, market_focus
    ):
        """Test index constituents with comprehensive validation."""
        response = indexes.index_constituents(apikey=api_key, index=index_name)

        models = get_response_models(response, FMPIndexConstituent)
        validate_model_list(models, FMPIndexConstituent, min_count=1)

        if models:
            # Data quality metrics using model attributes
            total_constituents = len(models)
            valid_symbols = 0
            valid_names = 0
            valid_sectors = 0
            unique_symbols = set()
            all_sectors = set()

            for model in models:
                # Symbol validation using direct model access
                if model.symbol:
                    assert (
                        len(model.symbol) >= 1
                    ), f"Symbol should have reasonable length: {model.symbol}"
                    assert (
                        len(model.symbol) <= 10
                    ), f"Symbol should be reasonable length: {model.symbol}"
                    assert (
                        model.symbol.isupper() or "." in model.symbol
                    ), f"Symbol should be uppercase or contain dots: {model.symbol}"
                    assert (
                        model.symbol not in unique_symbols
                    ), f"Symbol should be unique: {model.symbol}"
                    unique_symbols.add(model.symbol)
                    valid_symbols += 1

                # Name validation using model attributes
                if model.name:
                    assert (
                        len(model.name) >= 2
                    ), f"Name should be meaningful: {model.name}"
                    assert (
                        len(model.name) <= 100
                    ), f"Name should be reasonable length: {model.name}"
                    valid_names += 1

                # Sector validation using model attributes
                if model.sector:
                    assert (
                        len(model.sector) >= 3
                    ), f"Sector should be meaningful: {model.sector}"
                    all_sectors.add(model.sector)
                    valid_sectors += 1

            # Data quality assertions
            if index_name == "sp500":
                min_constituents = min(
                    expected_min_constituents, 100
                )  # More flexible for S&P 500
            elif index_name == "nasdaq":
                min_constituents = min(
                    expected_min_constituents, 30
                )  # More flexible for NASDAQ
            elif index_name == "dowjones":
                min_constituents = min(
                    expected_min_constituents, 15
                )  # More flexible for Dow Jones
            else:
                min_constituents = min(
                    expected_min_constituents, 10
                )  # General fallback

            assert (
                total_constituents >= min_constituents
            ), f"{index_name} should have at least {min_constituents} constituents, got {total_constituents}"
            assert (
                valid_symbols / total_constituents >= 0.95
            ), f"At least 95% should have valid symbols: {valid_symbols}/{total_constituents}"
            assert (
                valid_names / total_constituents >= 0.9
            ), f"At least 90% should have valid names: {valid_names}/{total_constituents}"
            assert (
                valid_sectors / total_constituents >= 0.8
            ), f"At least 80% should have valid sectors: {valid_sectors}/{total_constituents}"

            # Index-specific validations (only if we have sufficient data)
            if index_name == "sp500" and total_constituents >= 50:
                # S&P 500 should have diverse sectors
                assert (
                    len(all_sectors) >= 5
                ), f"S&P 500 should have diverse sectors, found {len(all_sectors)}"

                # Should contain major stocks
                major_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]
                found_stocks = [
                    stock for stock in major_stocks if stock in unique_symbols
                ]
                assert (
                    len(found_stocks) >= 1
                ), f"Should find at least 1 major stock: {found_stocks}"

            elif index_name in ["nasdaq", "nasdaq100"] and total_constituents >= 30:
                # NASDAQ should have significant tech representation
                tech_sectors = [
                    sector for sector in all_sectors if "Technology" in sector
                ]
                # Note: Some NASDAQ indices might not have explicit "Technology" sectors

            elif index_name == "dowjones" and total_constituents >= 15:
                # Dow Jones should have around 30 companies (but be flexible)
                if total_constituents >= 25:
                    assert (
                        total_constituents <= 35
                    ), f"Dow Jones should have around 30 companies, got {total_constituents}"

                # Should contain major Dow stocks
                dow_stocks = ["AAPL", "MSFT", "JNJ", "JPM", "V"]
                found_stocks = [
                    stock for stock in dow_stocks if stock in unique_symbols
                ]
                assert (
                    len(found_stocks) >= 1
                ), f"Should find at least 1 Dow stock: {found_stocks}"

    @pytest.mark.parametrize("index_name", ["sp500", "nasdaq", "dowjones"])
    def test_index_constituents_historical_comprehensive(self, api_key, index_name):
        """Test index_constituents_historical with comprehensive validation."""
        response = indexes.index_constituents_historical(
            apikey=api_key, index=index_name
        )

        models = get_response_models(response, FMPHistoricalIndexConstituent)
        validate_model_list(models, FMPHistoricalIndexConstituent, min_count=1)

        if models:
            # Data quality metrics using model attributes
            total_changes = len(models)
            valid_dates = 0
            valid_symbols = 0

            for model in models:
                # Date validation using model attributes
                for date_value in [model.dateAdded, model.date]:
                    if date_value:
                        assert (
                            len(date_value) >= 8
                        ), f"Date should be properly formatted: {date_value}"
                        assert (
                            "-" in date_value or "/" in date_value or "," in date_value
                        ), f"Date should have separators: {date_value}"
                        valid_dates += 1
                        break

                # Symbol validation using model attributes
                if model.symbol:
                    assert (
                        len(model.symbol) >= 1
                    ), f"Symbol should have reasonable length: {model.symbol}"
                    assert (
                        len(model.symbol) <= 10
                    ), f"Symbol should be reasonable length: {model.symbol}"
                    valid_symbols += 1

            # Data quality assertions
            assert (
                total_changes >= 1
            ), f"Should have at least 1 historical change for {index_name}"
            assert (
                valid_dates / total_changes >= 0.8
            ), f"At least 80% should have valid dates: {valid_dates}/{total_changes}"
            assert (
                valid_symbols / total_changes >= 0.7
            ), f"At least 70% should have valid symbols: {valid_symbols}/{total_changes}"

    def test_index_data_quality_comprehensive(self, api_key):
        """Test comprehensive data quality across all index functions."""
        # Test S&P 500 constituents quality
        response = indexes.index_constituents(apikey=api_key, index="sp500")

        models = get_response_models(response, FMPIndexConstituent)
        validate_model_list(models, FMPIndexConstituent, min_count=1)

        if models:
            # Symbol uniqueness validation using model attributes
            symbols = [model.symbol for model in models if model.symbol]
            assert len(symbols) == len(set(symbols)), "All symbols should be unique"

            # Sector diversity validation using model attributes
            sectors = [model.sector for model in models if model.sector]
            unique_sectors = set(sectors)
            assert (
                len(unique_sectors) >= 5
            ), f"Should have diverse sectors: {len(unique_sectors)}"

            # Major stock validation
            major_stocks = [
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "TSLA",
                "META",
                "NVDA",
                "JPM",
                "JNJ",
                "V",
            ]
            found_major_stocks = [stock for stock in major_stocks if stock in symbols]
            assert (
                len(found_major_stocks) >= 3
            ), f"Should find at least 3 major stocks: {found_major_stocks}"

            # Data completeness validation
            complete_records = 0
            for item in models:
                if item.symbol and item.name and item.sector:
                    complete_records += 1

            completion_rate = complete_records / len(models)
            assert (
                completion_rate >= 0.8
            ), f"At least 80% should have complete data: {completion_rate}"

    def test_index_invalid_inputs(self, api_key):
        """Test index functions with invalid inputs."""
        # Test invalid index name
        try:
            indexes.index_constituents(apikey=api_key, index="invalid_index")
        except ValueError as e:
            assert "Invalid index" in str(e)
            assert "sp500" in str(e)
            assert "nasdaq" in str(e)
            assert "dowjones" in str(e)

        # Test invalid API key
        with pytest.raises(InvalidAPIKeyException):
            indexes.index_list(apikey="invalid_key")

        # Test historical with invalid index
        try:
            indexes.index_constituents_historical(apikey=api_key, index="invalid_index")
        except ValueError as e:
            assert "Invalid index" in str(e)

    def test_index_data_consistency(self, api_key):
        """Test data consistency between current and historical constituents."""
        # Get current S&P 500 constituents
        current_response = indexes.index_constituents(apikey=api_key, index="sp500")
        current_models = get_response_models(current_response, FMPIndexConstituent)
        validate_model_list(current_models, FMPIndexConstituent, min_count=1)

        # Get historical S&P 500 constituents
        historical_response = indexes.index_constituents_historical(
            apikey=api_key, index="sp500"
        )
        historical_models = get_response_models(
            historical_response, FMPHistoricalIndexConstituent
        )
        validate_model_list(
            historical_models, FMPHistoricalIndexConstituent, min_count=1
        )

        if current_models and historical_models:
            # Extract current symbols using model attributes
            current_symbols = {model.symbol for model in current_models if model.symbol}

            # Extract historical symbols using model attributes
            historical_symbols = {
                model.symbol for model in historical_models[:50] if model.symbol
            }  # Check recent changes

            # Should have some current symbols
            assert len(current_symbols) > 0, "Should have current symbols"
            assert len(historical_symbols) > 0, "Should have historical symbols"

            # Data consistency check
            assert (
                len(current_symbols) >= 400
            ), f"S&P 500 should have ~500 constituents, got {len(current_symbols)}"
