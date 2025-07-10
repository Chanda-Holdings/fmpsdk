import pytest
from unittest.mock import Mock, patch
import pandas as pd
from pydantic import BaseModel, RootModel
from typing import List

from fmpsdk.utils import iterate_over_pages, parse_response, to_dict_list, to_dataframe


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


class TestUtilsErrorHandling:
    """Test error handling in utility functions."""

    def test_iterate_over_pages_with_exception(self):
        """Test iterate_over_pages handles exceptions gracefully."""

        def mock_func_with_exception(**kwargs):
            page = kwargs.get("page", 0)
            if page == 0:
                return ["item1"]
            else:
                raise Exception("API Error")

        args = {"symbol": "AAPL"}

        # Should raise the exception
        with pytest.raises(Exception, match="API Error"):
            iterate_over_pages(mock_func_with_exception, args, page_limit=10)

    def test_iterate_over_pages_with_none_response(self):
        """Test iterate_over_pages handles None response."""

        def mock_func_with_none(**kwargs):
            return None

        args = {"symbol": "AAPL"}

        # Should handle None gracefully
        # This might raise an exception depending on implementation
        try:
            result = iterate_over_pages(mock_func_with_none, args, page_limit=10)
            # If no exception, result should be empty
            assert result == [] or result == {}
        except (TypeError, AttributeError):
            # This is also acceptable behavior for None input
            pass


class TestUtilsPerformance:
    """Test performance aspects of utility functions."""

    def test_iterate_over_pages_stops_on_empty_response(self):
        """Test that iteration stops when empty response is received."""
        call_count = 0

        def mock_func(**kwargs):
            nonlocal call_count
            call_count += 1
            page = kwargs.get("page", 0)
            if page < 2:
                return ["data"]
            return []  # Empty response should stop iteration

        args = {"symbol": "AAPL"}
        iterate_over_pages(mock_func, args, page_limit=100)

        # Should stop after receiving empty response
        assert call_count == 3  # 2 pages with data + 1 empty page

    def test_iterate_over_pages_large_dataset_simulation(self):
        """Test iterate_over_pages with simulated large dataset."""

        def mock_func(**kwargs):
            page = kwargs.get("page", 0)
            if page < 5:  # 5 pages of data
                return [f"item_{page}_{i}" for i in range(10)]  # 10 items per page
            return []

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=10)

        # Should collect all data from all pages
        assert isinstance(result, list)
        assert len(result) == 50  # 5 pages * 10 items per page

        # Verify data integrity
        assert "item_0_0" in result
        assert "item_4_9" in result

    def test_to_dict_list(self):
        """Test to_dict_list function."""

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
                price=250.0,
            ),
        ]
        # Create a proper RootModel instance as expected by the function
        data = RootModel[List[MockFMPObject]](mock_objects)

        result = to_dict_list(data)

        # Should convert list of Pydantic objects to list of dicts
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "sector": "Technology",
            "price": 150.0,
        }

    def test_to_dataframe(self):
        """Test to_dataframe function."""

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
                price=250.0,
            ),
        ]
        # Create a proper RootModel instance as expected by the function
        data = RootModel[List[MockFMPObject]](mock_objects)

        result = to_dataframe(data)

        # Should convert list of Pydantic objects to pandas DataFrame
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (2, 4) # 2 rows, 4 columns
        assert result.iloc[0]["symbol"] == "AAPL"
        assert result.iloc[1]["price"] == 250.0

    def test_iterate_over_pages_with_complex_objects(self):
        """Test iterate_over_pages with complex Pydantic objects."""

        def mock_func(**kwargs):
            page = kwargs.get("page", 0)
            if page < 3:  # 3 pages of data
                return [
                    MockComplexFMPObject(
                        symbol="AAPL",
                        data={"key": "value"},
                        metrics=["metric1", "metric2"],
                        nestedObject={"nestedKey": "nestedValue"},
                    )
                ]
            return []

        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=10)

        # Should collect all data from all pages
        assert isinstance(result, list)
        assert len(result) == 3  # 3 pages

        # Verify data integrity
        assert result[0].symbol == "AAPL"
        assert result[0].data == {"key": "value"}
        assert result[0].metrics == ["metric1", "metric2"]
        assert result[0].nestedObject == {"nestedKey": "nestedValue"}


class TestToDictList:
    """Test class for to_dict_list utility function."""

    def test_to_dict_list_with_rootmodel_list(self):
        """Test to_dict_list with RootModel[List[FMP_OBJECT]]."""
        # Create mock data
        mock_objects = [
            MockFMPObject(symbol="AAPL", companyName="Apple Inc.", sector="Technology", price=150.0),
            MockFMPObject(symbol="MSFT", companyName="Microsoft Corp.", sector="Technology", price=300.0)
        ]
        root_model = RootModel[List[MockFMPObject]](mock_objects)
        
        result = to_dict_list(root_model)
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "sector": "Technology", 
            "price": 150.0
        }
        assert result[1] == {
            "symbol": "MSFT",
            "companyName": "Microsoft Corp.",
            "sector": "Technology",
            "price": 300.0
        }

    def test_to_dict_list_with_empty_rootmodel(self):
        """Test to_dict_list with empty RootModel."""
        root_model = RootModel[List[MockFMPObject]]([])
        
        result = to_dict_list(root_model)
        
        assert isinstance(result, list)
        assert len(result) == 0

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

    def test_to_dict_list_with_none_root(self):
        """Test to_dict_list with RootModel that has None root."""
        mock_response = Mock()
        mock_response.root = None
        # Explicitly set that this mock doesn't have status_code
        del mock_response.status_code
        
        result = to_dict_list(mock_response)
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_to_dict_list_with_complex_objects(self):
        """Test to_dict_list with complex FMP objects containing nested data."""
        mock_objects = [
            MockComplexFMPObject(
                symbol="AAPL",
                data={"revenue": 1000, "profit": 200},
                metrics=["metric1", "metric2"],
                nestedObject={"key": "value"}
            )
        ]
        root_model = RootModel[List[MockComplexFMPObject]](mock_objects)
        
        result = to_dict_list(root_model)
        
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


class TestToDataFrame:
    """Test class for to_dataframe utility function."""

    def test_to_dataframe_with_rootmodel_list(self):
        """Test to_dataframe with RootModel[List[FMP_OBJECT]]."""
        mock_objects = [
            MockFMPObject(symbol="AAPL", companyName="Apple Inc.", sector="Technology", price=150.0),
            MockFMPObject(symbol="MSFT", companyName="Microsoft Corp.", sector="Technology", price=300.0),
            MockFMPObject(symbol="GOOGL", companyName="Alphabet Inc.", sector="Technology", price=2500.0)
        ]
        root_model = RootModel[List[MockFMPObject]](mock_objects)
        
        result = to_dataframe(root_model)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 4)  # 3 rows, 4 columns
        assert list(result.columns) == ["symbol", "companyName", "sector", "price"]
        assert result.iloc[0]["symbol"] == "AAPL"
        assert result.iloc[1]["symbol"] == "MSFT"
        assert result.iloc[2]["symbol"] == "GOOGL"
        assert result["price"].tolist() == [150.0, 300.0, 2500.0]

    def test_to_dataframe_with_empty_rootmodel(self):
        """Test to_dataframe with empty RootModel."""
        root_model = RootModel[List[MockFMPObject]]([])
        
        result = to_dataframe(root_model)
        
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

    def test_to_dataframe_with_kwargs(self):
        """Test to_dataframe with additional DataFrame constructor kwargs."""
        mock_objects = [
            MockFMPObject(symbol="AAPL", companyName="Apple Inc.", sector="Technology", price=150.0),
            MockFMPObject(symbol="MSFT", companyName="Microsoft Corp.", sector="Technology", price=300.0)
        ]
        root_model = RootModel[List[MockFMPObject]](mock_objects)
        
        # Test with index parameter
        result = to_dataframe(root_model, index=[10, 20])
        
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
                nestedObject={"key": "value"}
            ),
            MockComplexFMPObject(
                symbol="MSFT",
                data={"revenue": 2000, "profit": 400}, 
                metrics=["metric3", "metric4"],
                nestedObject={"key2": "value2"}
            )
        ]
        root_model = RootModel[List[MockComplexFMPObject]](mock_objects)
        
        result = to_dataframe(root_model)
        
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
                nestedObject={"list_in_dict": ["a", "b", "c"]}
            )
        ]
        root_model = RootModel[List[MockComplexFMPObject]](mock_objects)
        
        result = to_dataframe(root_model)
        
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
        
        with patch('fmpsdk.utils.pd.DataFrame') as mock_df:
            # First call fails, second call (in error handling) also fails, third succeeds for error DataFrame
            mock_error_df = original_dataframe([{"error": "mocked error", "data_type": "test", "data_length": 1}])
            mock_df.side_effect = [
                Exception("DataFrame creation failed"), 
                Exception("Cleanup failed"), 
                mock_error_df
            ]
            
            mock_objects = [MockFMPObject(symbol="AAPL", companyName="Apple Inc.", sector="Technology", price=150.0)]
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


class TestUtilityFunctionIntegration:
    """Integration tests for utility functions working together."""

    def test_to_dict_list_to_dataframe_pipeline(self):
        """Test pipeline: RootModel -> to_dict_list -> to_dataframe."""
        mock_objects = [
            MockFMPObject(symbol="AAPL", companyName="Apple Inc.", sector="Technology", price=150.0),
            MockFMPObject(symbol="MSFT", companyName="Microsoft Corp.", sector="Technology", price=300.0)
        ]
        root_model = RootModel[List[MockFMPObject]](mock_objects)
        
        # Step 1: Convert to dict list
        dict_list = to_dict_list(root_model)
        
        # Step 2: Convert dict list to DataFrame manually
        df_from_dict_list = pd.DataFrame(dict_list)
        
        # Step 3: Convert RootModel directly to DataFrame
        df_direct = to_dataframe(root_model)
        
        # Both DataFrames should be identical
        pd.testing.assert_frame_equal(df_from_dict_list, df_direct)

    def test_consistency_across_utility_functions(self):
        """Test that utility functions are consistent with each other."""
        mock_objects = [
            MockFMPObject(symbol="AAPL", companyName="Apple Inc.", sector="Technology", price=150.0)
        ]
        root_model = RootModel[List[MockFMPObject]](mock_objects)
        
        # Get results from both functions
        dict_list = to_dict_list(root_model)
        df = to_dataframe(root_model)
        
        # Verify consistency
        assert len(dict_list) == len(df)
        assert dict_list[0]["symbol"] == df.iloc[0]["symbol"]
        assert dict_list[0]["companyName"] == df.iloc[0]["companyName"]
        assert dict_list[0]["sector"] == df.iloc[0]["sector"]
        assert dict_list[0]["price"] == df.iloc[0]["price"]

    def test_empty_response_consistency(self):
        """Test that both functions handle empty responses consistently."""
        root_model = RootModel[List[MockFMPObject]]([])
        
        dict_list = to_dict_list(root_model)
        df = to_dataframe(root_model)
        
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
