from fmpsdk import crypto
from fmpsdk.models import FMPCryptocurrencyListItem, FMPSymbolAndNameList

from .conftest import extract_data_list


class TestCryptocurrencyList:
    """Test the cryptocurrency_list function."""

    def test_cryptocurrency_list_success(self, api_key):
        """Test successful retrieval of cryptocurrency list."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item - might be dict or model depending on SDK implementation
            first_item = result_list[0]
            if isinstance(first_item, dict):
                crypto_data = FMPCryptocurrencyListItem(**first_item)
            else:
                crypto_data = first_item
            assert crypto_data.symbol, "Symbol should not be empty"
            assert crypto_data.name, "Name should not be empty"

    def test_cryptocurrency_list_model_validation(self, api_key):
        """Test that returned data validates against the Pydantic model."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            # Test model validation on first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated_item = FMPSymbolAndNameList(**first_item)
            else:
                validated_item = first_item
            assert hasattr(validated_item, "symbol")
            assert hasattr(validated_item, "name")

    def test_cryptocurrency_list_invalid_api_key(self):
        """Test handling of invalid API key."""
        result = crypto.cryptocurrency_list(apikey="invalid_api_key")
        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), "Should return a list even with invalid key"
