import pytest

from fmpsdk.utils import iterate_over_pages, parse_response


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
        with pytest.raises(ValueError, match="No model found for endpoint: mock_api_function"):
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
