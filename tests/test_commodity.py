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
