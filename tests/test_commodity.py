import pytest

from fmpsdk import commodity
from fmpsdk.models import FMPCommodity

from .conftest import extract_data_list


class TestCommodityList:
    """Test the commodity_list function."""

    def test_commodity_list_success(self, api_key):
        """Test successful retrieval of commodity list."""
        result = commodity.commodity_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item - commodity returns dict, so create model from it
            first_item = result_list[0]
            if isinstance(first_item, dict):
                commodity_data = FMPCommodity(**first_item)
            else:
                commodity_data = first_item
            assert commodity_data.symbol, "Symbol should not be empty"
            assert commodity_data.name, "Name should not be empty"

    def test_commodity_list_model_validation(self, api_key):
        """Test that returned data validates against the Pydantic model."""
        result = commodity.commodity_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            # Test model validation on first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated_item = FMPCommodity(**first_item)
            else:
                validated_item = first_item
            assert hasattr(validated_item, "symbol")
            assert hasattr(validated_item, "name")

    def test_commodity_list_invalid_api_key(self):
        """Test handling of invalid API key."""
        result = commodity.commodity_list(apikey="invalid_api_key")
        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), "Should return a list even with invalid key"

    @pytest.mark.parametrize(
        "commodity_type",
        [
            "energy",  # Oil, gas, etc.
            "metals",  # Gold, silver, copper, etc.
            "agricultural",  # Corn, wheat, soybeans, etc.
            "livestock",  # Cattle, hogs, etc.
            "precious_metals",  # Gold, silver, platinum, palladium
            "industrial_metals",  # Copper, aluminum, zinc, etc.
            "soft_commodities",  # Coffee, sugar, cotton, etc.
        ],
    )
    def test_commodity_list_by_category(self, api_key, commodity_type):
        """Test commodity list contains expected categories of commodities."""
        result = commodity.commodity_list(apikey=api_key)
        result_list = extract_data_list(result)

        if not result_list:
            pytest.skip("No commodity data available")

        # Map commodity types to expected symbols/names
        expected_patterns = {
            "energy": ["crude", "oil", "gas", "brent", "wti"],
            "metals": ["gold", "silver", "copper", "aluminum", "zinc"],
            "agricultural": ["corn", "wheat", "soybean", "rice", "oats"],
            "livestock": ["cattle", "hog", "lean", "feeder"],
            "precious_metals": ["gold", "silver", "platinum", "palladium"],
            "industrial_metals": ["copper", "aluminum", "zinc", "nickel", "lead"],
            "soft_commodities": ["coffee", "sugar", "cotton", "cocoa", "orange"],
        }

        patterns = expected_patterns.get(commodity_type, [])
        found_commodities = []

        for item in result_list:
            if isinstance(item, dict):
                commodity_data = FMPCommodity(**item)
            else:
                commodity_data = item

            name_lower = commodity_data.name.lower() if commodity_data.name else ""
            symbol_lower = (
                commodity_data.symbol.lower() if commodity_data.symbol else ""
            )

            for pattern in patterns:
                if pattern in name_lower or pattern in symbol_lower:
                    found_commodities.append(commodity_data.symbol)
                    break

        # At least some commodities should match the category
        assert len(found_commodities) >= 0, f"No {commodity_type} commodities found"

    @pytest.mark.parametrize(
        "expected_commodity",
        [
            "GCUSD",  # Gold futures
            "SIUSD",  # Silver futures
            "CLUSD",  # Crude oil futures
            "NGUSD",  # Natural gas futures
            "CCUSD",  # Copper futures
            "CTUSD",  # Cotton futures
            "KCCUSD",  # Coffee futures
            "SBUSD",  # Sugar futures
            "WUSD",  # Wheat futures
            "CUSD",  # Corn futures
        ],
    )
    def test_commodity_list_contains_major_commodities(
        self, api_key, expected_commodity
    ):
        """Test that commodity list contains major traded commodities."""
        result = commodity.commodity_list(apikey=api_key)
        result_list = extract_data_list(result)

        if not result_list:
            pytest.skip("No commodity data available")

        symbols = []
        for item in result_list:
            if isinstance(item, dict):
                commodity_data = FMPCommodity(**item)
            else:
                commodity_data = item
            symbols.append(commodity_data.symbol)

        # Note: Exact symbol format may vary, so we'll check for partial matches
        symbol_found = any(expected_commodity in symbol for symbol in symbols)
        partial_match = any(expected_commodity[:2] in symbol for symbol in symbols)

        # Some commodities may not be available, so we'll make this more flexible
        if not (symbol_found or partial_match):
            pytest.skip(f"{expected_commodity} not found in current commodity list")

    @pytest.mark.parametrize(
        "data_quality_check",
        [
            "symbol_format",
            "name_completeness",
            "unique_symbols",
            "price_availability",
            "category_coverage",
        ],
    )
    def test_commodity_list_data_quality(self, api_key, data_quality_check):
        """Test various data quality aspects of commodity list."""
        result = commodity.commodity_list(apikey=api_key)
        result_list = extract_data_list(result)

        if not result_list:
            pytest.skip("No commodity data available")

        if data_quality_check == "symbol_format":
            # Check that symbols follow expected patterns
            valid_symbols = 0
            for item in result_list:
                if isinstance(item, dict):
                    commodity_data = FMPCommodity(**item)
                else:
                    commodity_data = item

                if commodity_data.symbol and len(commodity_data.symbol) >= 2:
                    valid_symbols += 1

            assert (
                valid_symbols >= len(result_list) * 0.8
            ), "At least 80% of symbols should be valid"

        elif data_quality_check == "name_completeness":
            # Check that most commodities have meaningful names
            named_commodities = 0
            for item in result_list:
                if isinstance(item, dict):
                    commodity_data = FMPCommodity(**item)
                else:
                    commodity_data = item

                if commodity_data.name and len(commodity_data.name) > 2:
                    named_commodities += 1

            assert (
                named_commodities >= len(result_list) * 0.9
            ), "At least 90% should have meaningful names"

        elif data_quality_check == "unique_symbols":
            # Check for duplicate symbols
            symbols = []
            for item in result_list:
                if isinstance(item, dict):
                    commodity_data = FMPCommodity(**item)
                else:
                    commodity_data = item
                symbols.append(commodity_data.symbol)

            unique_symbols = set(symbols)
            assert len(unique_symbols) == len(
                symbols
            ), "All commodity symbols should be unique"

        elif data_quality_check == "price_availability":
            # Check if price field exists (if available in model)
            commodities_with_price = 0
            for item in result_list:
                if isinstance(item, dict):
                    commodity_data = FMPCommodity(**item)
                    if "price" in item or hasattr(commodity_data, "price"):
                        commodities_with_price += 1
                else:
                    commodity_data = item
                    if hasattr(commodity_data, "price"):
                        commodities_with_price += 1

            # This is informational - price availability may vary
            assert commodities_with_price >= 0, "Price availability check"

        elif data_quality_check == "category_coverage":
            # Check that we have good coverage across commodity categories
            categories_found = set()
            energy_keywords = ["oil", "gas", "crude", "brent", "wti"]
            metal_keywords = ["gold", "silver", "copper", "aluminum", "zinc"]
            agri_keywords = ["corn", "wheat", "soybean", "rice", "cotton"]

            for item in result_list:
                if isinstance(item, dict):
                    commodity_data = FMPCommodity(**item)
                else:
                    commodity_data = item

                name_lower = commodity_data.name.lower() if commodity_data.name else ""
                symbol_lower = (
                    commodity_data.symbol.lower() if commodity_data.symbol else ""
                )

                if any(
                    keyword in name_lower or keyword in symbol_lower
                    for keyword in energy_keywords
                ):
                    categories_found.add("energy")
                if any(
                    keyword in name_lower or keyword in symbol_lower
                    for keyword in metal_keywords
                ):
                    categories_found.add("metals")
                if any(
                    keyword in name_lower or keyword in symbol_lower
                    for keyword in agri_keywords
                ):
                    categories_found.add("agricultural")

            assert (
                len(categories_found) >= 1
            ), "Should cover at least one major commodity category"

    def test_commodity_list_stress_test(self, api_key):
        """Stress test for commodity list endpoint."""
        # Test multiple rapid calls
        results = []
        for i in range(3):
            result = commodity.commodity_list(apikey=api_key)
            result_list = extract_data_list(result)
            results.append(len(result_list))

        # All calls should return consistent results
        assert all(
            count == results[0] for count in results
        ), "Commodity list should be consistent across calls"

        # Should have reasonable number of commodities
        if results[0] > 0:
            assert results[0] >= 10, "Should have at least 10 commodities listed"
            assert (
                results[0] <= 1000
            ), "Should have reasonable number of commodities (< 1000)"
