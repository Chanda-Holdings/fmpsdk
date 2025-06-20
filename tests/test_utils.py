"""
Unit tests for fmpsdk utility functions.
"""
import pytest
from unittest.mock import Mock, patch
from typing import List, Dict, Any

from fmpsdk.utils import iterate_over_pages, parse_response
from fmpsdk.models import RootModel, FMPSymbolSearch


class TestIterateOverPages:
    """Test the iterate_over_pages utility function."""
    
    def test_iterate_over_pages_with_list_responses(self):
        """Test iterating over pages that return lists."""
        # Mock function that returns different data on each call
        mock_func = Mock()
        mock_func.side_effect = [
            [{"id": 1, "data": "page1"}, {"id": 2, "data": "page1"}],  # page 0
            [{"id": 3, "data": "page2"}],  # page 1
            []  # page 2 - empty, should stop iteration
        ]
        
        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=100)
        
        # Should have called function 3 times (pages 0, 1, 2)
        assert mock_func.call_count == 3
        
        # Should return combined list
        expected = [
            {"id": 1, "data": "page1"},
            {"id": 2, "data": "page1"},
            {"id": 3, "data": "page2"}
        ]
        assert result == expected
        
        # Check that page parameter was added correctly
        mock_func.assert_any_call(symbol="AAPL", page=0)
        mock_func.assert_any_call(symbol="AAPL", page=1)
        mock_func.assert_any_call(symbol="AAPL", page=2)
    
    def test_iterate_over_pages_with_dict_responses(self):
        """Test iterating over pages that return dictionaries."""
        mock_func = Mock()
        mock_func.side_effect = [
            {"key1": "value1", "key2": "value2"},  # page 0
            {"key3": "value3"},  # page 1
            {}  # page 2 - empty, should stop iteration
        ]
        
        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args, page_limit=100)
        
        # Should return combined dictionary
        expected = {"key1": "value1", "key2": "value2", "key3": "value3"}
        assert result == expected
    
    def test_iterate_over_pages_page_limit(self):
        """Test that page limit is respected."""
        mock_func = Mock()
        mock_func.return_value = [{"data": "test"}]  # Always return data
        
        args = {"symbol": "AAPL"}
        
        # Use a small page limit
        with patch('builtins.print') as mock_print:
            result = iterate_over_pages(mock_func, args, page_limit=2)
            
            # Should have called function 3 times (pages 0, 1, 2) and hit limit
            assert mock_func.call_count == 3
            
            # Should print error message
            mock_print.assert_called_with("ERROR: Reached FMP page limit: 2")
    
    def test_iterate_over_pages_invalid_response_type(self):
        """Test handling of invalid response types."""
        mock_func = Mock()
        mock_func.return_value = "invalid_string_response"
        
        args = {"symbol": "AAPL"}
        
        with pytest.raises(ValueError, match="Unexpected response type"):
            iterate_over_pages(mock_func, args)
    
    def test_iterate_over_pages_empty_list_first_call(self):
        """Test when first call returns empty list."""
        mock_func = Mock()
        mock_func.return_value = []
        
        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args)
        
        # Should call function once and return empty dict
        assert mock_func.call_count == 1
        assert result == {}
    
    def test_iterate_over_pages_empty_dict_first_call(self):
        """Test when first call returns empty dict."""
        mock_func = Mock()
        mock_func.return_value = {}
        
        args = {"symbol": "AAPL"}
        result = iterate_over_pages(mock_func, args)
        
        # Should call function once and return empty dict
        assert mock_func.call_count == 1
        assert result == {}


class TestParseResponse:
    """Test the parse_response decorator function."""
    
    def test_parse_response_with_mapped_model(self):
        """Test parse_response with a function that has a mapped model."""
        # Mock the ENDPOINT_MODEL_MAP
        with patch('fmpsdk.model_registry.ENDPOINT_MODEL_MAP', {'test_function': RootModel[List[FMPSymbolSearch]]}):
            
            @parse_response
            def test_function():
                return [{"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", 
                        "exchangeFullName": "NASDAQ", "exchange": "NASDAQ"}]
            
            result = test_function()
            
            # Should return parsed model
            assert isinstance(result, RootModel)
            assert len(result.root) == 1
            assert result.root[0].symbol == "AAPL"
    
    def test_parse_response_without_mapped_model(self):
        """Test parse_response with a function that has no mapped model."""
        with patch('fmpsdk.model_registry.ENDPOINT_MODEL_MAP', {}):
            
            @parse_response
            def test_function():
                return [{"symbol": "AAPL", "name": "Apple Inc."}]
            
            result = test_function()
            
            # Should return raw response
            assert result == [{"symbol": "AAPL", "name": "Apple Inc."}]
    
    def test_parse_response_with_none_response_list_model(self):
        """Test parse_response when API returns None for a list model."""
        # Create a mock list model
        mock_list_model = Mock()
        mock_list_model.__origin__ = list
        mock_list_model.model_validate.return_value = "validated_empty_list"
        
        with patch('fmpsdk.model_registry.ENDPOINT_MODEL_MAP', {'test_function': mock_list_model}):
            
            @parse_response
            def test_function():
                return None
            
            result = test_function()
            
            # Should call model_validate with empty list
            mock_list_model.model_validate.assert_called_once_with([])
            assert result == "validated_empty_list"
    
    def test_parse_response_with_none_response_dict_model(self):
        """Test parse_response when API returns None - all models expect lists."""
        # Since all our actual models are RootModel[List[...]], they should all get empty lists
        mock_list_model = Mock()
        mock_list_model.model_validate.return_value = "validated_empty_list"
        
        with patch('fmpsdk.model_registry.ENDPOINT_MODEL_MAP', {'test_function': mock_list_model}):
            
            @parse_response
            def test_function():
                return None
            
            result = test_function()
            
            # Should call model_validate with empty list (since all our models are list-based)
            mock_list_model.model_validate.assert_called_once_with([])
            assert result == "validated_empty_list"
    
    def test_parse_response_preserves_function_metadata(self):
        """Test that parse_response preserves function metadata."""
        with patch('fmpsdk.model_registry.ENDPOINT_MODEL_MAP', {}):
            
            @parse_response
            def test_function():
                """Test function docstring."""
                return {"test": "data"}
            
            # Should preserve function name and docstring
            assert test_function.__name__ == "test_function"
            assert test_function.__doc__ == "Test function docstring."
    
    def test_parse_response_with_args_and_kwargs(self):
        """Test that parse_response properly passes through arguments."""
        with patch('fmpsdk.model_registry.ENDPOINT_MODEL_MAP', {}):
            
            @parse_response
            def test_function(arg1, arg2, kwarg1=None):
                return {"arg1": arg1, "arg2": arg2, "kwarg1": kwarg1}
            
            result = test_function("value1", "value2", kwarg1="kwvalue")
            
            expected = {"arg1": "value1", "arg2": "value2", "kwarg1": "kwvalue"}
            assert result == expected