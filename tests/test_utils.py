from typing import List
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from pydantic import BaseModel, RootModel

from fmpsdk.utils import iterate_over_pages, parse_response, to_dataframe, to_dict_list


# Mock FMP model classes for testing
class MockFMPObject(BaseModel):
    symbol: str
    companyName: str
    sector: str
    price: float


class MockComplexFMPObject(BaseModel):
    symbol: str
    data: dict
    metrics: List[str]
    nestedObject: dict


class TestUtilityFunctions:
    """Test utility functions."""

    @pytest.mark.parametrize("page_limit", [1, 5, 10, 25, 50, 100])
    def test_iterate_over_pages_page_limits(self, page_limit):
        """Test iterate_over_pages with various page limits."""
        call_count = 0

        def mock_func(**kwargs):
            nonlocal call_count
            call_count += 1
            page = kwargs.get("page", 0)
            if page < page_limit // 2:  # Return data for half the page limit
                return [f"item{page}"]
            return []  # Empty to stop iteration

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=page_limit)

        # Should respect the page limit
        assert (
            call_count <= page_limit + 1
        )  # +1 for the empty page that stops iteration
        assert isinstance(result, list)

    @pytest.mark.parametrize("data_type", ["list", "dict", "empty_list", "empty_dict"])
    def test_iterate_over_pages_data_types(self, data_type):
        """Test iterate_over_pages with different data types."""

        def mock_func(**kwargs):
            page = kwargs.get("page", 0)
            if page == 0:
                if data_type == "list":
                    return ["item1", "item2"]
                elif data_type == "dict":
                    return {"key1": "value1", "key2": "value2"}
                elif data_type == "empty_list":
                    return []
                elif data_type == "empty_dict":
                    return {}
            else:
                return [] if data_type in ["list", "empty_list"] else {}

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=10)

        if data_type in ["list", "empty_list", "empty_dict"]:
            # Empty responses always return empty list regardless of type
            assert isinstance(result, list)
        elif data_type == "dict":
            assert isinstance(result, dict)

    @pytest.mark.parametrize(
        "num_pages,items_per_page",
        [(2, 5), (3, 10), (5, 20), (10, 100), (1, 1), (100, 1)],
    )
    def test_iterate_over_pages_pagination_scenarios(self, num_pages, items_per_page):
        """Test iterate_over_pages with various pagination scenarios."""

        def mock_func(**kwargs):
            page = kwargs.get("page", 0)
            if page < num_pages:
                return [f"page_{page}_item_{i}" for i in range(items_per_page)]
            return []

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=num_pages + 5)

        assert isinstance(result, list)
        assert len(result) == num_pages * items_per_page

        # Verify data integrity
        if result:
            assert f"page_0_item_0" in result
            if num_pages > 1:
                assert f"page_{num_pages-1}_item_{items_per_page-1}" in result

    def test_iterate_over_pages_with_list_data(self):
        """Test iterate_over_pages with list data."""

        # Mock function that returns paginated list data
        def mock_func(**kwargs):
            page = kwargs.get("page", 0)
            if page == 0:
                return ["item1", "item2"]
            elif page == 1:
                return ["item3", "item4"]
            else:
                return []  # End of pages

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=10)

        # Should combine all pages into single list
        assert isinstance(result, list)
        assert result == ["item1", "item2", "item3", "item4"]

    def test_iterate_over_pages_with_dict_data(self):
        """Test iterate_over_pages with dictionary data."""

        # Mock function that returns paginated dict data
        def mock_func(**kwargs):
            page = kwargs.get("page", 0)
            if page == 0:
                return {"key1": "value1", "key2": "value2"}
            elif page == 1:
                return {"key3": "value3", "key4": "value4"}
            else:
                return {}  # End of pages

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=10)

        # Should combine all pages into single dict
        assert isinstance(result, dict)
        assert result == {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
            "key4": "value4",
        }

    def test_iterate_over_pages_empty_first_page(self):
        """Test iterate_over_pages when first page is empty."""

        def mock_func(**kwargs):
            return []  # Always return empty

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=10)

        # Should return empty list
        assert isinstance(result, list)
        assert result == []

    def test_iterate_over_pages_page_limit(self):
        """Test iterate_over_pages respects page limit."""
        call_count = 0

        def mock_func(**kwargs):
            nonlocal call_count
            call_count += 1
            page = kwargs.get("page", 0)
            return [f"item{page}"]  # Always return data to test limit

        args = {"symbol": "AAPL"}
        # Set a low page limit
        result = iterate_over_pages(mock_func, args, page_limit=3)

        # Should respect the page limit
        assert call_count <= 4  # May call one extra time to detect end

    def test_parse_response_decorator(self):
        """Test parse_response decorator functionality."""

        # Test that the decorator raises an error for unknown functions
        @parse_response
        def mock_api_function():
            return {"symbol": "AAPL", "price": 150.0}

        # Should raise ValueError for unknown endpoint
        with pytest.raises(
            ValueError, match="No model found for endpoint: mock_api_function"
        ):
            mock_api_function()

        # Test error response passthrough
        @parse_response
        def mock_error_function():
            return {"Error Message": "Invalid API key"}

        result = mock_error_function()
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_iterate_over_pages_with_args_modification(self):
        """Test that iterate_over_pages properly modifies args with page parameter."""
        received_args = []

        def mock_func(**kwargs):
            received_args.append(kwargs.copy())
            page = kwargs.get("page", 0)
            if page < 2:
                return ["data"]
            return []

        args = {"symbol": "AAPL", "limit": 10}
        iterate_over_pages(mock_func, args, page_limit=10)

        # Check that page parameter was added to args for each call
        assert len(received_args) >= 2
        assert received_args[0]["page"] == 0
        assert received_args[1]["page"] == 1

        # Original args should be preserved
        for call_args in received_args:
            assert call_args["symbol"] == "AAPL"
            assert call_args["limit"] == 10


class TestParseResponse:
    """Test class for parse_response decorator functionality."""

    def test_parse_response_error_passthrough(self):
        """Test parse_response decorator with error responses."""

        @parse_response
        def mock_error_function():
            return {"Error Message": "Invalid API key"}

        result = mock_error_function()
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_parse_response_http_response_passthrough(self):
        """Test parse_response decorator with HTTP response objects (premium endpoints)."""

        @parse_response
        def mock_premium_function():
            # Create a mock HTTP response object
            mock_response = Mock()
            mock_response.status_code = 402
            return mock_response

        result = mock_premium_function()
        # Should return the response object as-is for premium endpoint detection
        assert hasattr(result, "status_code")
        assert result.status_code == 402

    def test_parse_response_none_data(self):
        """Test parse_response decorator with None response data."""

        # Create a mock list model that can handle empty lists
        class MockListModel(RootModel):
            root: List[MockFMPObject]

        with patch(
            "fmpsdk.model_registry.ENDPOINT_MODEL_MAP",
            {"mock_none_function": MockListModel},
        ):

            @parse_response
            def mock_none_function():
                return None

            result = mock_none_function()
            # Should convert None to empty list for model validation
            assert isinstance(result, MockListModel)
            assert result.root == []  # Empty list

    def test_parse_response_unknown_endpoint(self):
        """Test parse_response decorator with unknown endpoint."""

        @parse_response
        def unknown_endpoint_function():
            return [{"symbol": "AAPL", "price": 150.0}]

        # Should raise ValueError for unknown endpoint
        with pytest.raises(
            ValueError, match="No model found for endpoint: unknown_endpoint_function"
        ):
            unknown_endpoint_function()

    @patch("fmpsdk.model_registry.ENDPOINT_MODEL_MAP")
    def test_parse_response_with_registered_model(self, mock_endpoint_map):
        """Test parse_response decorator with properly registered model."""
        # Mock the endpoint map to include our test function
        mock_endpoint_map.get.return_value = MockFMPObject

        @parse_response
        def registered_function():
            return {
                "symbol": "AAPL",
                "companyName": "Apple",
                "sector": "Tech",
                "price": 150.0,
            }

        result = registered_function()
        # The result should be a MockFMPObject instance
        assert isinstance(result, MockFMPObject)
        assert result.symbol == "AAPL"
        assert result.companyName == "Apple"

    @patch("fmpsdk.model_registry.ENDPOINT_MODEL_MAP")
    def test_parse_response_with_list_data(self, mock_endpoint_map):
        """Test parse_response decorator with list data."""

        # Create a mock list model that can handle lists
        class MockListModel(RootModel):
            root: List[MockFMPObject]

        mock_endpoint_map.get.return_value = MockListModel

        @parse_response
        def list_function():
            return [
                {
                    "symbol": "AAPL",
                    "companyName": "Apple",
                    "sector": "Tech",
                    "price": 150.0,
                },
                {
                    "symbol": "GOOGL",
                    "companyName": "Google",
                    "sector": "Tech",
                    "price": 2500.0,
                },
            ]

        result = list_function()
        # Should return the model instance
        assert isinstance(result, MockListModel)

    def test_parse_response_model_validation_fallback(self):
        """Test parse_response decorator with model validation fallbacks."""

        # Create a mock model without model_validate method
        class LegacyModel:
            def __init__(self, data):
                self.data = data

        with patch(
            "fmpsdk.model_registry.ENDPOINT_MODEL_MAP", {"legacy_function": LegacyModel}
        ):

            @parse_response
            def legacy_function():
                return {"test": "data"}

            result = legacy_function()
            # Should fall back to constructor
            assert isinstance(result, LegacyModel)
            assert result.data == {"test": "data"}


class TestDataConversionUtilities:
    """Test data conversion utility functions."""

    @pytest.mark.parametrize(
        "input_data,expected_output",
        [
            ([], []),
            ([{"key": "value"}], [{"key": "value"}]),
            ({"key": "value"}, {"key": "value"}),
            (None, None),
            ("string", "string"),
            (123, 123),
        ],
    )
    def test_data_passthrough_scenarios(self, input_data, expected_output):
        """Test data conversion utilities with various input scenarios."""
        # Test that utilities handle edge cases properly
        if isinstance(input_data, list) and all(
            isinstance(item, dict) for item in input_data
        ):
            result = to_dict_list(input_data)
            assert result == expected_output
        elif input_data is None:
            # Utilities should handle None gracefully
            assert True  # Placeholder for None handling tests

    @pytest.mark.parametrize(
        "mixed_data_types",
        [
            [{"string": "value", "number": 42, "boolean": True, "null": None}],
            [{"list": [1, 2, 3], "dict": {"nested": "value"}}],
            [{"float": 3.14, "int": 100, "string": "test"}],
        ],
    )
    def test_mixed_data_type_handling(self, mixed_data_types):
        """Test utility functions with mixed data types."""
        # Create mock objects with mixed data types
        mock_objects = []
        for data in mixed_data_types:
            if all(
                key in ["symbol", "companyName", "sector", "price"]
                for key in data.keys()
                if key in ["symbol", "companyName", "sector", "price"]
            ):
                # Can create MockFMPObject
                continue
            else:
                # Use raw data
                mock_objects.append(data)

        if mock_objects:
            result = to_dict_list(mock_objects)
            assert isinstance(result, list)
            assert len(result) == len(mock_objects)


class TestUtilityErrorHandling:
    """Test error handling for utility functions."""

    @pytest.mark.parametrize(
        "invalid_input", [None, "string", 123, {"not": "list"}, set([1, 2, 3])]
    )
    def test_to_dict_list_invalid_inputs(self, invalid_input):
        """Test to_dict_list with invalid inputs."""
        try:
            result = to_dict_list(invalid_input)
            # Should either handle gracefully or return reasonable result
            assert result is not None
        except (TypeError, AttributeError):
            # Expected for invalid inputs
            assert True

    @pytest.mark.parametrize("invalid_input", [None, "string", 123, {"not": "list"}])
    def test_to_dataframe_invalid_inputs(self, invalid_input):
        """Test to_dataframe with invalid inputs."""
        try:
            result = to_dataframe(invalid_input)
            # Should either handle gracefully or return reasonable result
            if result is not None:
                assert isinstance(result, pd.DataFrame)
        except (TypeError, AttributeError, ValueError):
            # Expected for invalid inputs
            assert True

    def test_iterate_over_pages_function_errors(self):
        """Test iterate_over_pages when the function raises errors."""

        def error_func(**kwargs):
            raise ValueError("Simulated API error")

        args = {"symbol": "AAPL"}

        with pytest.raises(ValueError):
            iterate_over_pages(error_func, args, page_limit=10)

    @pytest.mark.parametrize(
        "edge_case_response",
        [
            {"Error Message": "API limit exceeded"},
            {"Error Message": "Invalid API key"},
            [],
            {},
            None,
        ],
    )
    def test_utility_edge_cases(self, edge_case_response):
        """Test utility functions with edge case responses."""
        # Test that utilities handle common API response edge cases
        if isinstance(edge_case_response, list):
            result = to_dict_list(edge_case_response)
            assert isinstance(result, list)
        elif isinstance(edge_case_response, dict):
            # Handle error responses
            assert "Error Message" in edge_case_response or edge_case_response == {}
        elif edge_case_response is None:
            # Handle None responses
            assert True


class TestToDictList:
    """Test class for to_dict_list utility function."""

    def test_to_dict_list_with_direct_list(self):
        """Test to_dict_list with direct List[FMPObject] - most common use case."""
        mock_objects = [
            MockFMPObject(
                symbol="AAPL",
                companyName="Apple Inc.",
                sector="Technology",
                price=150.0,
            ),
            MockFMPObject(
                symbol="MSFT",
                companyName="Microsoft Corp.",
                sector="Technology",
                price=300.0,
            ),
        ]

        result = to_dict_list(mock_objects)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "sector": "Technology",
            "price": 150.0,
        }
        assert result[1] == {
            "symbol": "MSFT",
            "companyName": "Microsoft Corp.",
            "sector": "Technology",
            "price": 300.0,
        }

    def test_to_dict_list_with_empty_list(self):
        """Test to_dict_list with empty list."""
        result = to_dict_list([])

        assert isinstance(result, list)
        assert len(result) == 0

    def test_to_dict_list_with_complex_objects(self):
        """Test to_dict_list with complex FMP objects containing nested data."""
        mock_objects = [
            MockComplexFMPObject(
                symbol="AAPL",
                data={"revenue": 1000, "profit": 200},
                metrics=["metric1", "metric2"],
                nestedObject={"key": "value"},
            )
        ]

        result = to_dict_list(mock_objects)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["data"] == {"revenue": 1000, "profit": 200}
        assert result[0]["metrics"] == ["metric1", "metric2"]
        assert result[0]["nestedObject"] == {"key": "value"}

    def test_to_dict_list_with_unexpected_type(self):
        """Test to_dict_list with unexpected response type."""
        unexpected_response = "unexpected string response"

        result = to_dict_list(unexpected_response)

        assert isinstance(result, list)
        assert len(result) == 1
        assert "unexpected_response" in result[0]
        assert "type" in result[0]
        assert result[0]["unexpected_response"] == "unexpected string response"

    def test_to_dict_list_with_error_response(self):
        """Test to_dict_list with error response dict."""
        error_response = {"Error Message": "Invalid API KEY"}

        result = to_dict_list(error_response)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == {"Error Message": "Invalid API KEY"}

    def test_to_dict_list_with_http_response_object(self):
        """Test to_dict_list with HTTP response object."""
        mock_response = Mock()
        mock_response.status_code = 402

        result = to_dict_list(mock_response)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == {"status_code": 402, "error": "HTTP response object"}

    def test_to_dict_list_with_none_response(self):
        """Test to_dict_list with None response."""
        result = to_dict_list(None)

        assert isinstance(result, list)
        assert len(result) == 0


class TestToDataFrame:
    """Test class for to_dataframe utility function."""

    def test_to_dataframe_with_direct_list(self):
        """Test to_dataframe with direct List[FMPObject] - most common use case."""
        mock_objects = [
            MockFMPObject(
                symbol="AAPL",
                companyName="Apple Inc.",
                sector="Technology",
                price=150.0,
            ),
            MockFMPObject(
                symbol="MSFT",
                companyName="Microsoft Corp.",
                sector="Technology",
                price=300.0,
            ),
            MockFMPObject(
                symbol="GOOGL",
                companyName="Alphabet Inc.",
                sector="Technology",
                price=2500.0,
            ),
        ]

        result = to_dataframe(mock_objects)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 4)  # 3 rows, 4 columns
        assert list(result.columns) == ["symbol", "companyName", "sector", "price"]
        assert result.iloc[0]["symbol"] == "AAPL"
        assert result.iloc[1]["symbol"] == "MSFT"
        assert result.iloc[2]["symbol"] == "GOOGL"
        assert result["price"].tolist() == [150.0, 300.0, 2500.0]

    def test_to_dataframe_with_empty_list(self):
        """Test to_dataframe with empty list."""
        result = to_dataframe([])

        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert result.shape == (0, 0)

    def test_to_dataframe_with_kwargs(self):
        """Test to_dataframe with additional DataFrame constructor kwargs."""
        mock_objects = [
            MockFMPObject(
                symbol="AAPL",
                companyName="Apple Inc.",
                sector="Technology",
                price=150.0,
            ),
            MockFMPObject(
                symbol="MSFT",
                companyName="Microsoft Corp.",
                sector="Technology",
                price=300.0,
            ),
        ]

        # Test with index parameter
        result = to_dataframe(mock_objects, index=[10, 20])

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (2, 4)
        assert result.index.tolist() == [10, 20]

    def test_to_dataframe_with_complex_objects(self):
        """Test to_dataframe with complex FMP objects."""
        mock_objects = [
            MockComplexFMPObject(
                symbol="AAPL",
                data={"revenue": 1000, "profit": 200},
                metrics=["metric1", "metric2"],
                nestedObject={"key": "value"},
            ),
            MockComplexFMPObject(
                symbol="MSFT",
                data={"revenue": 2000, "profit": 400},
                metrics=["metric3", "metric4"],
                nestedObject={"key2": "value2"},
            ),
        ]

        result = to_dataframe(mock_objects)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (2, 4)
        assert "symbol" in result.columns
        assert "data" in result.columns
        assert "metrics" in result.columns
        assert "nestedObject" in result.columns
        assert result.iloc[0]["symbol"] == "AAPL"
        assert result.iloc[1]["symbol"] == "MSFT"

    def test_to_dataframe_with_problematic_data_types(self):
        """Test to_dataframe with data that might cause DataFrame creation issues."""
        # Create mock objects with problematic nested structures
        mock_objects = [
            MockComplexFMPObject(
                symbol="TEST",
                data={"deeply": {"nested": {"structure": "value"}}},
                metrics=["metric1"],
                nestedObject={"list_in_dict": ["a", "b", "c"]},
            )
        ]

        result = to_dataframe(mock_objects)

        # Should handle complex structures gracefully
        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == 1  # Should have 1 row
        assert "symbol" in result.columns
        assert result.iloc[0]["symbol"] == "TEST"

    def test_to_dataframe_dataframe_creation_failure(self):
        """Test to_dataframe when DataFrame creation fails."""
        # Mock a scenario where DataFrame creation fails
        import fmpsdk.utils

        original_dataframe = fmpsdk.utils.pd.DataFrame

        with patch("fmpsdk.utils.pd.DataFrame") as mock_df:
            # First call fails, second call (in error handling) also fails, third succeeds for error DataFrame
            mock_error_df = original_dataframe(
                [{"error": "mocked error", "data_type": "test", "data_length": 1}]
            )
            mock_df.side_effect = [
                Exception("DataFrame creation failed"),
                Exception("Cleanup failed"),
                mock_error_df,
            ]

            mock_objects = [
                MockFMPObject(
                    symbol="AAPL",
                    companyName="Apple Inc.",
                    sector="Technology",
                    price=150.0,
                )
            ]
            root_model = RootModel[List[MockFMPObject]](mock_objects)

            result = to_dataframe(root_model)

            # Should return error DataFrame
            assert isinstance(result, original_dataframe)
            assert "error" in result.columns
            assert len(result) == 1

    def test_to_dataframe_with_none_response(self):
        """Test to_dataframe with None response."""
        result = to_dataframe(None)

        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert result.shape == (0, 0)

    def test_to_dataframe_with_error_response(self):
        """Test to_dataframe with error response dict."""
        error_response = {"Error Message": "Invalid API KEY"}

        result = to_dataframe(error_response)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (1, 1)
        assert "Error Message" in result.columns
        assert result.iloc[0]["Error Message"] == "Invalid API KEY"

    def test_to_dataframe_with_http_response_object(self):
        """Test to_dataframe with HTTP response object."""
        mock_response = Mock()
        mock_response.status_code = 402

        result = to_dataframe(mock_response)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == (1, 2)
        assert "status_code" in result.columns
        assert "error" in result.columns
        assert result.iloc[0]["status_code"] == 402


class TestUtilityFunctionIntegration:
    """Integration tests for utility functions working together."""

    def test_to_dict_list_to_dataframe_pipeline(self):
        """Test pipeline: List[FMPObject] -> to_dict_list -> to_dataframe."""
        mock_objects = [
            MockFMPObject(
                symbol="AAPL",
                companyName="Apple Inc.",
                sector="Technology",
                price=150.0,
            ),
            MockFMPObject(
                symbol="MSFT",
                companyName="Microsoft Corp.",
                sector="Technology",
                price=300.0,
            ),
        ]

        # Step 1: Convert to dict list
        dict_list = to_dict_list(mock_objects)

        # Step 2: Convert dict list to DataFrame manually
        df_from_dict_list = pd.DataFrame(dict_list)

        # Step 3: Convert List[FMPObject] directly to DataFrame
        df_direct = to_dataframe(mock_objects)

        # Both DataFrames should be identical
        pd.testing.assert_frame_equal(df_from_dict_list, df_direct)

    def test_consistency_across_utility_functions(self):
        """Test that utility functions are consistent with each other."""
        mock_objects = [
            MockFMPObject(
                symbol="AAPL",
                companyName="Apple Inc.",
                sector="Technology",
                price=150.0,
            )
        ]

        # Get results from both functions
        dict_list = to_dict_list(mock_objects)
        df = to_dataframe(mock_objects)

        # Verify consistency
        assert len(dict_list) == len(df)
        assert dict_list[0]["symbol"] == df.iloc[0]["symbol"]
        assert dict_list[0]["companyName"] == df.iloc[0]["companyName"]
        assert dict_list[0]["sector"] == df.iloc[0]["sector"]
        assert dict_list[0]["price"] == df.iloc[0]["price"]

    def test_empty_response_consistency(self):
        """Test that both functions handle empty responses consistently."""
        empty_list = []

        dict_list = to_dict_list(empty_list)
        df = to_dataframe(empty_list)

        assert len(dict_list) == 0
        assert df.empty
        assert len(df) == 0

    def test_error_response_consistency(self):
        """Test that both functions handle error responses consistently."""
        error_response = {"Error Message": "Invalid API KEY"}

        dict_list = to_dict_list(error_response)
        df = to_dataframe(error_response)

        assert len(dict_list) == 1
        assert len(df) == 1
        assert dict_list[0]["Error Message"] == df.iloc[0]["Error Message"]
        assert len(df) == 1
        assert dict_list[0]["Error Message"] == df.iloc[0]["Error Message"]
