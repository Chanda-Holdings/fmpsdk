from fmpsdk import forex
from fmpsdk.models import FMPForexPair

from .conftest import extract_data_list


class TestForexList:
    """Test the forex_list function."""

    def test_forex_list_success(self, api_key):
        """Test successful retrieval of forex pairs list."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item - might be dict or model depending on SDK implementation
            first_item = result_list[0]
            if isinstance(first_item, dict):
                forex_data = FMPForexPair(**first_item)
            else:
                forex_data = first_item
            assert forex_data.symbol, "Symbol should not be empty"
            assert forex_data.fromCurrency, "From currency should not be empty"
            assert forex_data.toCurrency, "To currency should not be empty"

    def test_forex_list_model_validation(self, api_key):
        """Test that returned data validates against the Pydantic model."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            # Test model validation on first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated_item = FMPForexPair(**first_item)
            else:
                validated_item = first_item
            assert hasattr(validated_item, "symbol")
            assert hasattr(validated_item, "fromCurrency")

    def test_forex_list_invalid_api_key(self):
        """Test handling of invalid API key."""
        result = forex.forex_list(apikey="invalid_api_key")
        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), "Should return a list even with invalid key"
