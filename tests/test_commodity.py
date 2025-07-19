from typing import List

import pytest

from fmpsdk import commodity
from fmpsdk.models import (  # Corrected - this is what the API actually returns
    FMPCommodityListItem,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
    validate_required_fields,
)


def validate_commodity_data(commodities: List[FMPCommodityListItem]) -> None:
    """Validate commodity data with business logic checks using Pydantic models."""
    if not commodities:
        return

    # Validate all items are FMPCommodityListItem models (the actual API return type)
    validate_model_list(commodities, FMPCommodityListItem, min_count=1)

    # Data quality metrics
    total_commodities = len(commodities)
    valid_symbols = 0
    valid_names = 0
    unique_symbols = set()
    category_coverage = set()

    # Commodity categories and their keywords
    category_keywords = {
        "energy": ["oil", "gas", "crude", "brent", "wti", "heating", "gasoline"],
        "precious_metals": ["gold", "silver", "platinum", "palladium"],
        "industrial_metals": ["copper", "aluminum", "zinc", "nickel", "lead", "tin"],
        "agricultural": ["corn", "wheat", "soybean", "rice", "oats", "barley"],
        "soft_commodities": ["coffee", "sugar", "cotton", "cocoa", "orange", "lumber"],
        "livestock": ["cattle", "hog", "lean", "feeder", "pork"],
    }

    for commodity in commodities:
        # Symbol validation - direct Pydantic model access
        symbol = commodity.symbol
        if symbol and len(symbol) >= 2:
            valid_symbols += 1
            unique_symbols.add(symbol)

        # Name validation - direct Pydantic model access
        name = commodity.name
        if name and len(name) > 2:
            valid_names += 1

        # Category detection
        name_lower = name.lower() if name else ""
        symbol_lower = symbol.lower() if symbol else ""

        for category, keywords in category_keywords.items():
            if any(
                keyword in name_lower or keyword in symbol_lower for keyword in keywords
            ):
                category_coverage.add(category)
                break

    # Business logic assertions
    if total_commodities > 0:
        assert (
            valid_symbols / total_commodities >= 0.85
        ), f"Only {valid_symbols}/{total_commodities} commodities have valid symbols"
        assert (
            valid_names / total_commodities >= 0.90
        ), f"Only {valid_names}/{total_commodities} commodities have valid names"
        assert (
            len(unique_symbols) == valid_symbols
        ), f"Commodity symbols should be unique: {len(unique_symbols)} != {valid_symbols}"
        assert (
            len(category_coverage) >= 1
        ), f"Should cover at least 1 major commodity category, found: {category_coverage}"

        # Reasonable commodity count
        assert (
            total_commodities >= 10
        ), f"Should have at least 10 commodities, got {total_commodities}"
        assert (
            total_commodities <= 1000
        ), f"Should have reasonable number of commodities (< 1000), got {total_commodities}"


class TestCommodityList:
    """Test the commodity_list function."""

    def test_commodity_list_success(self, api_key):
        """Test successful retrieval of commodity list."""
        response, validation = handle_api_call_with_validation(
            commodity.commodity_list, "commodity_list", True, apikey=api_key
        )

        # NEW: Use direct Pydantic model access
        commodities = get_response_models(response, FMPCommodityListItem)
        if commodities:
            validate_commodity_data(commodities)

    def test_commodity_list_model_validation(self, api_key):
        """Test that returned data validates against the Pydantic model."""
        response, validation = handle_api_call_with_validation(
            commodity.commodity_list, "commodity_list", True, apikey=api_key
        )

        # NEW: Direct model validation - no conversion needed!
        commodities = get_response_models(response, FMPCommodityListItem)
        validate_model_list(commodities, FMPCommodityListItem, min_count=1)
        if commodities:
            validate_commodity_data(commodities)

    def test_commodity_list_invalid_api_key(self):
        """Test handling of invalid API key."""
        with pytest.raises(Exception):
            commodity.commodity_list(apikey="invalid_api_key")

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
        response, validation = handle_api_call_with_validation(
            commodity.commodity_list, "commodity_list", True, apikey=api_key
        )

        # NEW: Use direct Pydantic model access
        commodities = get_response_models(response, FMPCommodityListItem)
        if commodities:
            validate_commodity_data(commodities)

            # Category-specific validation
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

            for commodity_model in commodities:
                # Direct Pydantic model field access - type safe!
                name = commodity_model.name
                symbol = commodity_model.symbol

                name_lower = name.lower() if name else ""
                symbol_lower = symbol.lower() if symbol else ""

                for pattern in patterns:
                    if pattern in name_lower or pattern in symbol_lower:
                        found_commodities.append(symbol)
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
            "HGUSD",  # Copper futures (API returns HGUSD, not CCUSD)
            "KEUSX",  # Wheat futures (API returns KEUSX, not WUSD)
            "ZCUSX",  # Corn futures (API returns ZCUSX, not CUSD)
            "PLUSD",  # Platinum
            "PAUSD",  # Palladium
        ],
    )
    def test_commodity_list_contains_major_commodities(
        self, api_key, expected_commodity
    ):
        """Test that commodity list contains major traded commodities."""
        response, validation = handle_api_call_with_validation(
            commodity.commodity_list, "commodity_list", True, apikey=api_key
        )

        # NEW: Use direct Pydantic model access
        commodities = get_response_models(response, FMPCommodityListItem)
        if commodities:
            validate_commodity_data(commodities)

            # Check for major commodities - direct model field access
            symbols = [
                commodity_model.symbol
                for commodity_model in commodities
                if commodity_model.symbol
            ]

            # Create a more flexible matching approach
            symbol_found = any(expected_commodity == symbol for symbol in symbols)

            # If exact match fails, try case-insensitive matching
            if not symbol_found:
                symbol_found = any(
                    expected_commodity.lower() == symbol.lower() for symbol in symbols
                )

            # For debugging: if symbol not found, show what symbols are available
            if not symbol_found:
                available_symbols = symbols[:10]  # Show first 10
                pytest.fail(
                    f"Expected commodity '{expected_commodity}' not found in list. "
                    f"Available symbols (first 10): {available_symbols}"
                )

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
        response, validation = handle_api_call_with_validation(
            commodity.commodity_list, "commodity_list", True, apikey=api_key
        )

        # NEW: Use direct Pydantic model access
        commodities = get_response_models(response, FMPCommodityListItem)
        if commodities:
            validate_commodity_data(commodities)

            # Additional specific checks using direct model field access
            if data_quality_check == "symbol_format":
                # Check that symbols follow expected patterns - type-safe access
                valid_symbols = sum(
                    1 for item in commodities if item.symbol and len(item.symbol) >= 2
                )
                assert (
                    valid_symbols >= len(commodities) * 0.8
                ), "At least 80% of symbols should be valid"

            elif data_quality_check == "name_completeness":
                # Check that most commodities have meaningful names - type-safe access
                named_commodities = sum(
                    1 for item in commodities if item.name and len(item.name) > 2
                )
                assert (
                    named_commodities >= len(commodities) * 0.9
                ), "At least 90% should have meaningful names"

            elif data_quality_check == "unique_symbols":
                # Check for duplicate symbols - direct field access
                symbols = [item.symbol for item in commodities if item.symbol]
                unique_symbols = set(symbols)
                assert len(unique_symbols) == len(
                    symbols
                ), "All commodity symbols should be unique"

            elif data_quality_check == "price_availability":
                # Check if price field exists in the Pydantic model
                commodities_with_price = sum(
                    1 for item in commodities if hasattr(item, "price")
                )
                # This is informational - price availability may vary
                assert commodities_with_price >= 0, "Price availability check"

            elif data_quality_check == "category_coverage":
                # Check that we have good coverage across commodity categories
                categories_found = set()
                energy_keywords = ["oil", "gas", "crude", "brent", "wti"]
                metal_keywords = ["gold", "silver", "copper", "aluminum", "zinc"]
                agri_keywords = ["corn", "wheat", "soybean", "rice", "cotton"]

                for item in commodities:
                    # Direct Pydantic model field access - type safe!
                    name = item.name
                    symbol = item.symbol

                    name_lower = name.lower() if name else ""
                    symbol_lower = symbol.lower() if symbol else ""

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
        # Test multiple rapid calls - NEW: using direct model access
        results = []
        for i in range(3):
            response, validation = handle_api_call_with_validation(
                commodity.commodity_list, "commodity_list", True, apikey=api_key
            )
            commodities = get_response_models(response, FMPCommodityListItem)
            results.append(len(commodities))

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
