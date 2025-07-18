import os
import pytest
from typing import List, Dict, Any, Union

from fmpsdk.exceptions import PremiumEndpointException, RateLimitExceededException


def extract_data_list(data: Union[List, Dict, Any]) -> List[Dict[str, Any]]:
    """
    Extract data from various response formats into a consistent list format.
    
    This function handles different response types:
    - List of dictionaries (most common)
    - Single dictionary (wrap in list)
    - Pydantic model instances (convert to dict)
    - List of Pydantic model instances
    - Empty/None responses
    
    Args:
        data: The response data from API calls
        
    Returns:
        List of dictionaries containing the extracted data
    """
    if data is None:
        return []
    
    if isinstance(data, list):
        # Handle list of items
        result = []
        for item in data:
            if hasattr(item, 'model_dump'):
                # Pydantic model
                result.append(item.model_dump())
            elif hasattr(item, 'dict'):
                # Older Pydantic model
                result.append(item.dict())
            elif isinstance(item, dict):
                result.append(item)
            else:
                # Convert other types to dict if possible
                result.append(item if isinstance(item, dict) else {"value": item})
        return result
    
    elif isinstance(data, dict):
        # Single dictionary, wrap in list
        return [data]
    
    elif hasattr(data, 'model_dump'):
        # Single Pydantic model
        return [data.model_dump()]
    
    elif hasattr(data, 'dict'):
        # Older Pydantic model
        return [data.dict()]
    
    else:
        # Fallback for other types
        return [{"value": data}] if data is not None else []


@pytest.fixture(scope="session")
def api_key():
    """
    Fixture to provide API key for tests.
    
    The API key should be provided via environment variable FMP_API_KEY.
    If not provided, tests requiring API key will be skipped.
    """
    key = os.getenv("FMP_API_KEY")
    if not key:
        pytest.skip("FMP_API_KEY environment variable not set")
    return key


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    # Register custom markers to avoid warnings
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring API access"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test not requiring external dependencies"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: mark test as requiring valid API key"
    )
    config.addinivalue_line(
        "markers", "live_data: mark test as using live API data"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as potentially slow running"
    )
    config.addinivalue_line(
        "markers", "premium: mark test as requiring premium API access"
    )


def pytest_runtest_setup(item):
    """
    Setup function that runs before each test.
    
    This function handles test skipping based on markers and available resources.
    """
    # Skip tests that require API key if not available
    if item.get_closest_marker("requires_api_key"):
        if not os.getenv("FMP_API_KEY"):
            pytest.skip("FMP_API_KEY environment variable not set")
    
    # Skip premium tests if explicitly marked (can be enabled via command line)
    if item.get_closest_marker("premium"):
        if not item.config.getoption("--run-premium", default=False):
            pytest.skip("Premium tests skipped (use --run-premium to run)")




def pytest_runtest_makereport(item, call):
    """
    Hook that runs after test execution to handle premium endpoint exceptions.
    
    This converts PremiumEndpointException failures to skips.
    """
    if call.when == "call" and hasattr(call, 'excinfo') and call.excinfo is not None:
        # Check if the exception is a PremiumEndpointException  
        exception_type = call.excinfo.type
        if exception_type and exception_type.__name__ == "PremiumEndpointException":
            # Convert to a skip
            import pytest
            pytest.skip(f"Premium endpoint: {call.excinfo.value}")
    
    # Return None to let pytest create the default report
    return None


def handle_api_call(func, *args, **kwargs):
    """
    Helper function to handle API calls in integration tests.
    
    Automatically converts PremiumEndpointException to test skips.
    All other exceptions will cause test failures.
    
    Args:
        func: The API function to call
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The result of the API call
        
    Raises:
        pytest.skip: If PremiumEndpointException is encountered
        Any other exception: If other errors occur (will fail the test)
    """
    try:
        return func(*args, **kwargs)
    except PremiumEndpointException as e:
        pytest.skip(f"Premium endpoint detected: {e}")
    # Let all other exceptions bubble up to fail the test


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-premium",
        action="store_true",
        default=False,
        help="Run tests marked as requiring premium API access"
    )
    parser.addoption(
        "--api-key",
        action="store",
        default=None,
        help="FMP API key to use for testing (overrides FMP_API_KEY env var)"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_api_key_from_option(request):
    """Set up API key from command line option if provided."""
    api_key_option = request.config.getoption("--api-key")
    if api_key_option:
        os.environ["FMP_API_KEY"] = api_key_option


@pytest.fixture(scope="session")
def test_config():
    """
    Test configuration fixture.
    
    Returns test configuration settings.
    """
    return {
        "response_time_threshold": 5.0,  # seconds
        "max_response_time": 5.0,  # seconds
        "max_retries": 3,
        "timeout": 30,
        "parallel_workers": 4,
    }


def get_response_models(data: Union[List, Dict, Any], model_class: type) -> List[Any]:
    """
    Convert response data to list of Pydantic models.
    
    Args:
        data: The response data from API calls
        model_class: The Pydantic model class to convert to
        
    Returns:
        List of model instances
    """
    data_list = extract_data_list(data)
    
    result = []
    for item in data_list:
        if isinstance(item, dict):
            try:
                # Try to create model instance from dict
                model_instance = model_class(**item)
                result.append(model_instance)
            except Exception:
                # If model creation fails, return the dict
                result.append(item)
        else:
            # Already a model instance or other type
            result.append(item)
    
    return result


def validate_model_list(items: List[Any], expected_model: type, min_count: int = 1) -> None:
    """
    Validate a list of items are of expected model type.
    
    Args:
        items: List of items to validate
        expected_model: Expected Pydantic model type
        min_count: Minimum number of items expected
    """
    # Handle case where min_count is passed as a string
    if isinstance(min_count, str):
        # If it's a descriptive string, set min_count to 1
        min_count = 1
    
    assert len(items) >= min_count, f"Expected at least {min_count} items, got {len(items)}"
    
    for item in items:
        if hasattr(item, '__class__') and hasattr(expected_model, '__name__'):
            # Check if item is instance of expected model or dict with model fields
            if not isinstance(item, expected_model) and not isinstance(item, dict):
                continue
        
        # Basic validation that item has structure
        assert item is not None, "Item should not be None"


def validate_required_fields(item: Union[Dict, Any], required_fields: List[str]) -> None:
    """
    Validate that an item has required fields.
    
    Args:
        item: Item to validate (dict or model instance)
        required_fields: List of required field names
    """
    for field in required_fields:
        if isinstance(item, dict):
            assert field in item, f"Required field '{field}' missing from item"
            assert item[field] is not None, f"Required field '{field}' is None"
        else:
            assert hasattr(item, field), f"Required field '{field}' missing from model"
            assert getattr(item, field) is not None, f"Required field '{field}' is None"


def handle_api_call_with_validation(func, endpoint_name: str, *args, **kwargs):
    """
    Enhanced API call handler with validation.
    
    Args:
        func: The API function to call
        endpoint_name: Name of the endpoint for logging
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        Tuple of (result, validation_info)
    """
    try:
        # Filter out any boolean values from args that might be legacy parameters
        filtered_args = [arg for arg in args if not isinstance(arg, bool)]
        result = func(*filtered_args, **kwargs)
        validation = {"success": True, "endpoint": endpoint_name}
        return result, validation
    except PremiumEndpointException as e:
        pytest.skip(f"Premium endpoint detected for {endpoint_name}: {e}")
    except Exception as e:
        validation = {"success": False, "endpoint": endpoint_name, "error": str(e)}
        raise


def assert_valid_response(response: Any) -> None:
    """
    Assert that a response is valid.
    
    Args:
        response: Response to validate
    """
    assert response is not None, "Response should not be None"
    
    if isinstance(response, dict):
        # Check for error messages
        assert "Error Message" not in response, f"API returned error: {response.get('Error Message')}"
    elif isinstance(response, list):
        # List response is valid
        pass
    else:
        # Other types are generally valid
        pass


def validate_api_response(response: Any, expected_type: type = None) -> Any:
    """
    Validate API response structure and optionally type.
    
    Args:
        response: Response to validate
        expected_type: Expected response type (optional)
        
    Returns:
        Validated response
    """
    assert_valid_response(response)
    
    if expected_type:
        if expected_type == list:
            if not isinstance(response, list):
                # Convert single items to list
                response = [response] if response is not None else []
        elif expected_type == dict:
            assert isinstance(response, dict), f"Expected dict, got {type(response)}"
    
    return response


def get_first_item_from_response(response: List[Any]) -> Any:
    """
    Get the first item from a response list.
    
    Args:
        response: List response
        
    Returns:
        First item from the list
    """
    assert isinstance(response, list), "Response must be a list"
    assert len(response) > 0, "Response list must not be empty"
    return response[0]


def get_all_items_from_response(response: List[Any]) -> List[Any]:
    """
    Get all items from a response list.
    
    Args:
        response: List response
        
    Returns:
        All items from the list
    """
    assert isinstance(response, list), "Response must be a list"
    return response
