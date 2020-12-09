import typing
import json
from urllib import parse
from urllib.request import urlopen
import logging
from .settings import INDUSTRY_VALUES, SECTOR_VALUES, PERIOD_VALUES, EXCHANGE_VALUES


def make_url(base: str, path: str, query_vars: typing.Dict):
    """
    Stitch component URL parts together.

    :param base: First part of the URL
    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """
    tmp = parse.urlsplit(base)
    url = parse.urlunsplit(
        (tmp.scheme, tmp.netloc, f"{tmp.path}{path}", parse.urlencode(query_vars), "",)
    )
    return url


def return_response(base: str, path: str, query_vars: typing.Dict):
    """
    Query URL for JSON response.

    :param base: First part of the URL
    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """
    response = urlopen(make_url(base=base, path=path, query_vars=query_vars))
    data = response.read().decode("utf-8")
    return json.loads(data)


def set_exchange(value: str) -> str:
    valid_values = EXCHANGE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid exchange value.  Valid options: {valid_values}")


def set_period(value: str) -> str:
    valid_values = PERIOD_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid period value.  Valid options: {valid_values}")


def set_sector(value: str) -> str:
    valid_values = SECTOR_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid sector value.  Valid options: {valid_values}")


def set_industry(value: str) -> str:
    valid_values = INDUSTRY_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid industry value.  Valid options: {valid_values}")
