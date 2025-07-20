import csv
import io
import json
import logging
import time
import typing

import requests

from .exceptions import (
    HTTPS_READ_TIMEOUT_CODE,
    RATE_LIMIT_STATUS_CODE,
    PremiumEndpointException,
    RateLimitExceededException,
)
from .utils import raise_for_exception

BASE_URL_STABLE: str = "https://financialmodelingprep.com/stable/"
BASE_URL_V4: str = "https://financialmodelingprep.com/api/v4/"
BASE_URL_V3: str = "https://financialmodelingprep.com/api/v3/"

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30
RETRIES = 10
RETRY_DELAY = 10

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def __get_base_url(version: str) -> str:
    """
    Get the base URL for the API requests.
    """
    base_urls = {"stable": BASE_URL_STABLE, "v4": BASE_URL_V4, "v3": BASE_URL_V3}
    result: str = base_urls.get(version, BASE_URL_STABLE)
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
    :param retries: Number of retries for rate limiting
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

        if (
            response.status_code == RATE_LIMIT_STATUS_CODE
            or response.status_code == HTTPS_READ_TIMEOUT_CODE
        ):
            logging.warning(
                f"{'Rate limit' if response.status_code == RATE_LIMIT_STATUS_CODE else 'HTTPS read timeout'} occurred: {response.status_code}. "
                f"Query variables: {query_vars}"
            )
            # Once retries are exhausted, raise_for_exception will handle it
            if retries > 0:
                logging.info(
                    f"Retrying in {retry_delay} seconds... ({retries} retries left)"
                )
                time.sleep(retry_delay)
                return __return_json(
                    path, query_vars, version, retries - 1, retry_delay
                )

        raise_for_exception(response)

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
