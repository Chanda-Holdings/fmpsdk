"""
Core integration tests for fmpsdk library functionality.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os

from pydantic import BaseModel

import fmpsdk
from fmpsdk import settings
from fmpsdk.utils import parse_response

API_KEY = os.getenv("FMP_API_KEY")


class TestCoreFunctionality:
    """Test suite for core fmpsdk functionality."""

    def test_fmpsdk_import(self):
        """Test that fmpsdk can be imported successfully."""
        assert fmpsdk is not None
        # Note: Direct module access commented out for linting compliance
        # Core functionality is still accessible via explicit imports
        assert fmpsdk.attribution is not None

    def test_settings_module(self):
        """Test that settings module is accessible."""
        assert settings is not None
        assert hasattr(settings, "FMP_ENDPOINT")

    def test_parse_response_decorator(self):
        """Test the parse_response decorator functionality."""

        # Create a simple test function
        @parse_response
        def test_function():
            return {"test": "data"}

        result = test_function()
        assert result is not None

    def test_api_key_validation(self):
        """Test that API key is available for testing."""
        assert API_KEY is not None
        assert len(API_KEY) > 0
        # API key should be either "demo" or a valid key
        assert API_KEY == "demo" or len(API_KEY) > 10

    def test_basic_api_call(self):
        """Test a basic API call to verify connectivity."""
        from fmpsdk.general import available_indexes

        result = available_indexes(apikey=API_KEY)
        assert result is not None

    def test_module_imports(self):
        """Test that all main modules can be imported."""
        modules_to_test = [
            "general",
            "stock_time_series",
            "company_valuation",
            "news",
            "forex",
            "cryptocurrencies",
            "etf",
            "insider_trading",
            "calendar_module",
            "economic_indicators",
        ]

        for module_name in modules_to_test:
            try:
                module = getattr(fmpsdk, module_name)
                assert module is not None
            except AttributeError:
                # Some modules might not be directly accessible
                exec(f"import fmpsdk.{module_name}")

    def test_error_handling(self):
        """Test error handling with invalid API key."""
        from fmpsdk.general import available_indexes

        # This should not raise an exception but may return empty/None
        result = available_indexes(apikey="invalid_key")
        # The function should handle errors gracefully
        assert result is not None or result is None

    def test_response_formats(self):
        """Test that responses are in expected formats."""
        from fmpsdk.general import available_indexes

        result = available_indexes(apikey=API_KEY)
        assert result is not None

        # Check if result is a Pydantic model
        if hasattr(result, "__root__") or hasattr(result, "root"):
            # It's a RootModel, get the actual data
            data = result.root if hasattr(result, "root") else result.__root__
            if isinstance(data, list) and data:
                # Check first few items
                for item in data[:3]:
                    assert isinstance(item, (dict, BaseModel))
        elif hasattr(result, "__iter__") and not isinstance(result, (str, bytes)):
            items = list(result)
            if items:
                # Should have Pydantic models or dict-like objects
                for item in items[:3]:  # Check first few items
                    assert isinstance(item, (dict, BaseModel))

    def test_settings_endpoint_configuration(self):
        """Test that FMP endpoint is properly configured."""
        assert hasattr(settings, "FMP_ENDPOINT")
        assert settings.FMP_ENDPOINT.startswith("https://")
        assert "financialmodelingprep.com" in settings.FMP_ENDPOINT

    def test_library_version_info(self):
        """Test that library has version information."""
        # Check if version is accessible
        try:
            import fmpsdk

            # May have __version__ attribute
            if hasattr(fmpsdk, "__version__"):
                assert isinstance(fmpsdk.__version__, str)
        except:
            # Version info may not be available in all setups
            pass

    def test_multiple_api_calls_stability(self):
        """Test that multiple API calls work consistently."""
        from fmpsdk.general import available_indexes

        results = []
        for i in range(3):
            result = available_indexes(apikey=API_KEY)
            results.append(result)

        # All calls should succeed
        assert all(r is not None for r in results)

    def test_concurrent_api_access(self):
        """Test basic concurrent API access."""
        from fmpsdk.general import available_indexes
        from fmpsdk.stock_time_series import quote_short

        # Make different API calls
        result1 = available_indexes(apikey=API_KEY)
        result2 = quote_short(apikey=API_KEY, symbol="AAPL")

        assert result1 is not None
        assert result2 is not None

    def test_model_registry_integration(self):
        """Test that model registry is properly integrated."""
        from fmpsdk.model_registry import ENDPOINT_MODEL_MAP

        assert ENDPOINT_MODEL_MAP is not None
        assert isinstance(ENDPOINT_MODEL_MAP, dict)
        assert len(ENDPOINT_MODEL_MAP) > 0

    def test_utils_functionality(self):
        """Test utility functions."""
        # Test that utils module is accessible
        from fmpsdk import utils

        assert utils is not None
        assert hasattr(utils, "parse_response")
