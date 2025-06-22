"""
Integration tests for fmpsdk utility functions.
"""
import pytest
from typing import List, Dict, Any

from fmpsdk.utils import parse_response
from fmpsdk.models import RootModel


class TestParseResponse:
    """Test the parse_response decorator with real scenarios."""
    
    def test_parse_response_basic_functionality(self):
        """Test parse_response decorator works with basic functions."""
        
        @parse_response
        def test_function():
            return [{"test": "data"}]
        
        result = test_function()
        assert result is not None
        
    def test_parse_response_with_none_return(self):
        """Test parse_response handles None returns gracefully."""
        
        @parse_response  
        def test_function_none():
            return None
            
        result = test_function_none()
        # Since test_function_none is not in ENDPOINT_MODEL_MAP, 
        # parse_response returns the raw result (None)
        assert result is None
        
    def test_parse_response_with_empty_list(self):
        """Test parse_response handles empty list returns."""
        
        @parse_response
        def test_function_empty():
            return []
            
        result = test_function_empty()
        # Since test_function_empty is not in ENDPOINT_MODEL_MAP,
        # parse_response returns the raw result (empty list)
        assert result is not None
        assert result == []
        assert isinstance(result, list)


class TestUtilityFunctionality:
    """Test utility functions in real scenarios."""
    
    def test_root_model_basic_usage(self):
        """Test RootModel can be used with basic data."""
        data = [{"symbol": "AAPL", "name": "Apple Inc"}]
        model = RootModel(data)
        
        assert model.root == data
        assert len(model.root) == 1
        assert model.root[0]["symbol"] == "AAPL"
        
    def test_root_model_empty_data(self):
        """Test RootModel handles empty data."""
        model = RootModel([])
        
        assert model.root == []
        assert len(model.root) == 0
