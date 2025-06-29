import csv
import io
import logging
import typing

import requests

from .settings import (
    BASE_URL_STABLE,
    BASE_URL_V4,
    ECONOMIC_INDICATOR_VALUES,
    INDUSTRY_VALUES,
    PERIOD_VALUES,
    SECTOR_VALUES,
    SERIES_TYPE_VALUES,
    STATISTICS_TYPE_VALUES,
    TECHNICAL_INDICATORS_TIME_DELTA_VALUES,
    TIME_DELTA_VALUES,
)

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def __get_base_url(version: str) -> str:
    """
    Get the base URL for the API requests.
    """
    return BASE_URL_V4 if version == "v4" else BASE_URL_STABLE


def __return_json(
    path: str, query_vars: typing.Dict, version: str = "stable"
) -> typing.Optional[typing.List]:
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
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related "
            f"issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  "
            f"Error: {e}"
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


def __validate_period(value: str) -> str:
    """
    Check to see if passed string is in the list of possible time periods.
    :param value: Period name.
    :return: Passed value or No Return
    """
    valid_values = PERIOD_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid period value: {value}.  Valid options: {valid_values}")
        return value  # Return the value anyway to avoid breaking


def __validate_sector(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Sectors.
    :param value: Sector name.
    :return: Passed value or No Return
    """
    valid_values = SECTOR_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid sector value: {value}.  Valid options: {valid_values}")
        return value  # Return the value anyway to avoid breaking


def __validate_industry(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Industries.
    :param value: Industry name.
    :return: Passed value or No Return
    """
    valid_values = INDUSTRY_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid industry value: {value}.  Valid options: {valid_values}"
        )
        return value  # Return the value anyway to avoid breaking


def __validate_time_delta(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Time Deltas.
    :param value: Time Delta name.
    :return: Passed value or No Return
    """
    valid_values = TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid time_delta value: {value}.  Valid options: {valid_values}"
        )
        return value  # Return the value anyway to avoid breaking


def __validate_series_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Series Type.
    :param value: Series Type name.
    :return: Passed value or No Return
    """
    valid_values = SERIES_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid series_type value: {value}.  Valid options: {valid_values}"
        )
        return value  # Return the value anyway to avoid breaking


def __validate_statistics_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Statistics Type.
    :param value: Statistics Type name.
    :return: Passed value or No Return
    """
    valid_values = STATISTICS_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid statistics_type value: {value}.  Valid options: {valid_values}"
        )
        return value  # Return the value anyway to avoid breaking


def __validate_technical_indicators_time_delta(value: str) -> str:
    """Exactly like set_time_delta() method but adds 'daily' as an option.
    :param value: Indicators Time Delta name.
    :return: Passed value or No Return
    """
    valid_values = TECHNICAL_INDICATORS_TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid time_delta value: {value}.  Valid options: {valid_values}"
        )
        return value  # Return the value anyway to avoid breaking


def __validate_economic_indicator(value: str) -> str:
    """
    Validate economic indicator value.

    :param value: Value to validate
    :return: Validated value
    """
    if value not in ECONOMIC_INDICATOR_VALUES:
        raise ValueError(f"'{value}' not in {ECONOMIC_INDICATOR_VALUES}")
    return value
