import csv
import io
import json
import logging
import typing

import requests

from .settings import BASE_URL_STABLE, BASE_URL_V4

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30

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
    path: str, query_vars: typing.Dict, version: str = "stable"
) -> typing.Optional[typing.List[typing.Any]]:
    """
    Query URL for JSON response for stable version of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """

    base_url = __get_base_url(version)
    url = f"{base_url}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )

        # Check for premium endpoint response (402 status code)
        if response.status_code == 402:
            return response  # Return the response object so premium detection can work

        # Check for other non-200 status codes and return error response
        if response.status_code != 200:
            error_msg = f"API request failed with status code {response.status_code}"
            if response.content:
                try:
                    error_content = response.content.decode("utf-8")
                    error_msg += f": {error_content}"
                    # Try to parse as JSON and return it
                    try:
                        error_json = json.loads(error_content)
                        logging.error(
                            f"{error_msg}\nURL: {url}\nQuery variables: {query_vars}"
                        )
                        return error_json  # type: ignore[no-any-return]
                    except json.JSONDecodeError:
                        pass
                except UnicodeDecodeError:
                    error_msg += f": {response.content!r}"

            logging.error(f"{error_msg}\nURL: {url}\nQuery variables: {query_vars}")

            # Return a generic error message dict
            return {  # type: ignore[no-any-return]
                "Error Message": f"API request failed with status code {response.status_code}"
            }

        if len(response.content) > 0:
            if query_vars.get("datatype") == "csv":
                content = response.content.decode("utf-8")
                try:
                    reader = csv.DictReader(io.StringIO(content))
                    return_var = [row for row in reader]
                except csv.Error as e:
                    logging.error(f"Failed to parse CSV response: {e}")
                    raise e
            else:
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
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related "
            f"issue."
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
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  "
            f"Error: {e}\n"
            f"URL: {url}\n"
            f"Query variables: {query_vars}\n"
            f"Response status code: {response.status_code if response else 'No response'}\n"
            f"Response content: {repr(response.content) if response else 'No response'}\n"
            f"Response text: {response.text if response else 'No response text'}"
        )
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
