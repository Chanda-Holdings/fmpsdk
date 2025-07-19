import csv
import io
import json
import logging
import time
import typing

import requests

from .exceptions import (
    RETRYABLE_STATUS_CODE,
    SUCCESS_STATUS_CODE,
    InvalidQueryParameterException,
    PremiumEndpointException,
    RateLimitExceededException,
)
from .utils import raise_for_exception

BASE_URL_STABLE: str = "https://financialmodelingprep.com/stable/"
BASE_URL_V4: str = "https://financialmodelingprep.com/api/v4/"

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30
RETRIES = 10
RETRY_DELAY = 10
# if "pytest" in sys.modules:
#     RETRIES = 2
#     RETRY_DELAY = 2

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def __get_base_url(version: str) -> str:
    """
    Get the base URL for the API requests.
    """
    result: str = BASE_URL_V4 if version == "v4" else BASE_URL_STABLE
    return result


def __return_json(
    path: str,
    query_vars: typing.Dict,
    version: str = "stable",
    retries: int = RETRIES,
    retry_delay: int = RETRY_DELAY,
) -> typing.Optional[typing.List[typing.Any]]:
    """
    Query URL for JSON response for stable version of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :param version: API version to use ("stable" or "v4")
    :param retries: Number of retries for rate limiting or retryable errors
    :param retry_delay: Delay in seconds between retries
    :return: JSON response
    """

    base_url = __get_base_url(version)
    url = f"{base_url}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )

        if response.status_code == RETRYABLE_STATUS_CODE:
            logging.warning(
                f"Rate limit or retryable error occurred: {response.status_code}. "
                f"Query variables: {query_vars}"
            )
            if retries > 0:
                logging.info(
                    f"Retrying in {retry_delay} seconds... ({retries} retries left)"
                )
                time.sleep(retry_delay)
                return __return_json(
                    path, query_vars, version, retries - 1, retry_delay
                )
            else:
                logging.error(f"Max retries exceeded for {url}")
                raise RateLimitExceededException(
                    f"Rate limit exceeded or retryable error for {url}. "
                    f"Query variables: {query_vars}"
                    f"Response: {response.text}"
                )

        raise_for_exception(response)

        # Check for other non-200 status codes and return error response
        if response.status_code != SUCCESS_STATUS_CODE:
            error_msg = response.reason
            if response.content:
                try:
                    error_content = response.content.decode("utf-8")
                    try:
                        # Try to parse as JSON and return it
                        error_json = json.loads(error_content)
                        logging.error(
                            f"{error_msg}: {error_content}\nURL: {url}\nQuery variables: {query_vars}"
                        )
                        # Handle both dict and list error responses
                        if isinstance(error_json, dict):
                            error_message = error_json.get(
                                "Error Message", "Unknown error"
                            )
                        else:
                            error_message = str(error_json)
                        raise Exception(
                            f"API request failed with error: {error_message}",
                            error_json,
                        )
                    except json.JSONDecodeError:
                        # Not valid JSON, continue with regular error handling
                        error_msg += f": {error_content}"
                except UnicodeDecodeError:
                    error_msg += f": {response.content!r}"

            logging.error(f"{error_msg}\nURL: {url}\nQuery variables: {query_vars}")

            if "Invalid or missing query parameter" in error_msg:
                raise InvalidQueryParameterException(error_msg)

            raise Exception(
                f"API request failed with status code {response.status_code}: {error_msg}"
            )

        if len(response.content) > 0:
            if query_vars.get("datatype") == "csv":
                # Handle CSV response
                content = response.content.decode("utf-8")
                try:
                    reader = csv.DictReader(io.StringIO(content))
                    return_var = [row for row in reader]
                except csv.Error as e:
                    logging.error(f"Failed to parse CSV response: {e}")
                    raise e
            else:
                # Handle JSON response
                return_var = response.json()

        if len(response.content) == 0 or (
            isinstance(return_var, dict) and len(return_var.keys()) == 0
        ):
            logging.warning("Response appears to have no data.  Returning empty List.")
            return_var = []

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
        raise
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related issues."
        )
        raise
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
        raise
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except (PremiumEndpointException, RateLimitExceededException):
        # Allow our custom exceptions to bubble up
        raise
    except json.JSONDecodeError:
        # Allow JSON decode errors to be handled by the caller
        raise
    except (UnicodeDecodeError, csv.Error) as e:
        # Handle specific parsing errors
        logging.error(f"Data parsing error: {e}")
        raise
    return return_var


def __return_binary_stable(
    path: str, query_vars: typing.Dict
) -> typing.Optional[bytes]:
    """
    Query URL for binary response for stable version of FMP API.
    Used for downloading files like XLSX, PDF, etc.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: Binary response content
    """
    url = f"{BASE_URL_STABLE}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        if len(response.content) > 0:
            return_var = response.content
        else:
            logging.warning("Response appears to have no data.")
            return_var = b""

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed: DNS failure, refused connection or some other connection related "
            f"issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for. "
            f"Error: {e}"
        )
    return return_var
