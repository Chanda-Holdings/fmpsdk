import typing
from typing import Any, Callable, TypeVar
import time

import pandas as pd

from .exceptions import RateLimitExceededException

T = TypeVar("T")

def is_rate_limit_error(result):
    """
    Check if the response indicates a rate limiting error.

    Args:
        result: The API response object

    Returns:
        bool: True if this is a rate limiting error, False otherwise
    """
    # Check for dictionary responses with Error Message (FMP API specific)
    if isinstance(result, dict) and "Error Message" in result:
        error_msg = result["Error Message"].lower()
        # FMP specific rate limiting message
        if "limit reach" in error_msg:
            return True
        # Check for other common rate limiting keywords
        rate_limit_keywords = [
            "rate limit",
            "too many requests",
            "quota exceeded",
            "api limit",
            "requests per",
            "upgrade your plan",  # FMP often says this for rate limits
        ]
        return any(keyword in error_msg for keyword in rate_limit_keywords)

    # Check for HTTP status responses
    if hasattr(result, "status_code"):
        # 429 is the standard rate limiting status code
        if result.status_code == 429:
            return True
        # Some APIs use other status codes for rate limiting
        if result.status_code in [
            503,
            509,
        ]:  # Service Unavailable, Bandwidth Limit Exceeded
            if hasattr(result, "content"):
                try:
                    content = (
                        result.content.decode("utf-8")
                        if isinstance(result.content, bytes)
                        else str(result.content)
                    )
                    return any(
                        keyword in content.lower()
                        for keyword in ["rate", "limit", "quota"]
                    )
                except (UnicodeDecodeError, AttributeError):
                    pass

    return False


def iterate_over_pages(
    func, args, page_limit=100, max_retries=3, retry_delay=10
) -> typing.Union[typing.List, typing.Dict]:
    """
    Iterate over paginated API responses with rate limiting retry logic.
    
    Args:
        func: The function to call for each page
        args: Arguments to pass to the function
        page_limit: Maximum number of pages to fetch (default: 100)
        max_retries: Maximum number of retries for rate limiting (default: 3)
        retry_delay: Delay in seconds between retries (default: 10)
    
    Returns:
        Union[List, Dict]: Combined data from all pages
        
    Raises:
        RateLimitExceededException: If rate limiting persists after max_retries
        ValueError: If response type is unexpected
        StopIteration: If page limit is reached
    """
    page = 0
    data_list = []
    data_dict = {}
    
    while True:
        args["page"] = page
        
        # Retry logic for rate limiting
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                response = func(**args)
                
                # Check if response indicates rate limiting
                if is_rate_limit_error(response):
                    if attempt < max_retries:
                        print(f"Rate limiting detected on page {page}, attempt {attempt + 1}/{max_retries + 1}. "
                              f"Waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise RateLimitExceededException(f"Rate limiting persisted after {max_retries} retries on page {page}")
                
                # Successful response, break out of retry loop
                break
                
            except Exception as e:
                last_exception = e
                # Check if this is a network-related error that we might want to retry
                if hasattr(e, '__class__') and 'requests' in str(type(e)):
                    if attempt < max_retries:
                        print(f"Network error on page {page}, attempt {attempt + 1}/{max_retries + 1}: {str(e)[:100]}... "
                              f"Waiting {retry_delay // 2} seconds before retry...")
                        time.sleep(retry_delay // 2)  # Shorter delay for network errors
                        continue
                # For other exceptions, re-raise immediately
                raise e
        
        # If we get here and have an exception, something went wrong
        if last_exception and not hasattr(last_exception, '__class__'):
            raise last_exception
        
        # Check for empty response (end of pagination)
        if len(response) == 0:
            break

        # Process the response
        if isinstance(response, list):
            data_list.extend(response)
        elif isinstance(response, dict):
            # Check if it's an error response
            if "Error Message" in response:
                if is_rate_limit_error(response):
                    raise RateLimitExceededException(f"Rate limiting detected in response: {response['Error Message']}")
                else:
                    # Other API errors should be handled by the calling code
                    return response
            data_dict.update(response)
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")

        if page >= page_limit:
            raise StopIteration("Reached FMP page limit")

        page += 1

    if len(data_list) == 0 and len(data_dict) > 0:
        return data_dict
    else:
        return data_list


def parse_response(func: Callable[..., Any]) -> Callable[..., Any]:
    from functools import wraps

    from .model_registry import ENDPOINT_MODEL_MAP

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        raw = func(*args, **kwargs)

        # Check for HTTP Response objects (e.g., 402 for premium endpoints)
        if hasattr(raw, "status_code"):
            return raw  # Return response object as-is for premium endpoint detection

        # Check for API error responses and return them as-is
        if isinstance(raw, dict) and "Error Message" in raw:
            return raw

        model = ENDPOINT_MODEL_MAP.get(func.__name__)
        if model:
            # Defensive: If API returns None, convert to empty list for list models
            if raw is None:
                raw = []

            try:
                # Try BaseModel.model_validate first
                if hasattr(model, "model_validate"):
                    result = model.model_validate(raw)
                else:
                    # Fallback to constructor for RootModel
                    result = model(raw)
            except (AttributeError, TypeError):
                # Final fallback to constructor
                result = model(raw)
            # Do NOT unwrap __root__ or root; always return the model instance
            return result
        else:
            raise ValueError(
                f"No model found for endpoint: {func.__name__}. "
                "Ensure the endpoint is registered in ENDPOINT_MODEL_MAP."
            )

    return wrapper


def to_dict_list(response: Any) -> typing.List[typing.Dict[str, Any]]:
    """
    Convert FMP data to a list of dictionaries.

    This function is designed for the primary use case: converting a List[FMPObject]
    (list of Pydantic model instances) to a list of dictionaries.

    Args:
        response: The data to convert - typically List[FMPObject] from FMP API calls

    Returns:
        List of dictionaries representing the FMP data objects

    Examples:
        >>> objects = [CompanyProfile(...), CompanyProfile(...)]
        >>> data = to_dict_list(objects)
        >>> print(data[0]['symbol'])  # 'AAPL'
    """
    # Handle None or empty responses
    if response is None:
        return []

    # Handle direct List[FMPObject] - primary use case
    if isinstance(response, list):
        if not response:  # Empty list
            return []
        return [
            item.model_dump() if hasattr(item, "model_dump") else item
            for item in response
        ]

    # Handle error responses (dict with "Error Message") - for compatibility
    if isinstance(response, dict) and "Error Message" in response:
        return [response]

    # Handle HTTP Response objects (premium endpoint errors) - for compatibility
    if hasattr(response, "status_code"):
        return [{"status_code": response.status_code, "error": "HTTP response object"}]

    # Fallback for unexpected types
    return [{"unexpected_response": str(response), "type": str(type(response))}]


def to_dataframe(response: Any, **kwargs) -> Any:
    """
    Convert FMP data to a pandas DataFrame.

    This function is designed for the primary use case: converting a List[FMPObject]
    (list of Pydantic model instances) to a pandas DataFrame.

    Args:
        response: The data to convert - typically List[FMPObject] from FMP API calls
        **kwargs: Additional arguments to pass to pandas.DataFrame constructor

    Returns:
        pandas.DataFrame containing the FMP data objects as rows

    Raises:
        ImportError: If pandas is not installed

    Examples:
        >>> objects = [CompanyProfile(...), CompanyProfile(...)]
        >>> df = to_dataframe(objects)
        >>> print(df[['symbol', 'companyName', 'sector']])
    """

    # Convert response to list of dictionaries
    dict_list = to_dict_list(response)

    # Handle empty responses
    if not dict_list:
        return pd.DataFrame()

    # Create DataFrame from list of dictionaries
    try:
        df = pd.DataFrame(dict_list, **kwargs)
        return df
    except Exception as e:
        # If DataFrame creation fails, it's likely due to inconsistent data types
        # or nested structures in the FMP objects. Handle gracefully.
        try:
            # Convert problematic columns to strings
            cleaned_list = []
            for item in dict_list:
                cleaned_item = {}
                for key, value in item.items():
                    # Convert complex types to strings
                    if isinstance(value, (dict, list)):
                        cleaned_item[key] = str(value)
                    else:
                        cleaned_item[key] = value
                cleaned_list.append(cleaned_item)

            df = pd.DataFrame(cleaned_list, **kwargs)
            return df
        except Exception:
            # Final fallback: return error info in DataFrame
            return pd.DataFrame(
                [
                    {
                        "error": f"Failed to create DataFrame: {str(e)}",
                        "data_type": str(type(response)),
                        "data_length": len(dict_list),
                    }
                ]
            )
