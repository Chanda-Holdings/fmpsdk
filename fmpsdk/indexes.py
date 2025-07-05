import typing

from pydantic import RootModel

from .models import (
    FMPHistoricalIndexConstituent,
    FMPIndexConstituent,
    FMPSector,
    FMPSymbolAndNameList,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def index_list(
    apikey: str,
) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Get a list of available indexes.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    Returns
    -------
    list
        List of available indexes.
    """
    path = "index-list"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def available_sectors(apikey: str) -> RootModel[typing.List[FMPSector]]:
    """
    Query FMP /sectors-list API to get all available sectors.

    :param apikey: Your API key
    :return: A list of sector names.
    """
    path = "sectors-list"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def index_constituents(
    apikey: str,
    index: str,
) -> RootModel[typing.List[FMPIndexConstituent]]:
    """
    Query FMP index constituents API.

    :param apikey: Your API key.
    :param index: The index to query (e.g., "sp500", "nasdaq", "dowjones").

    :return: A list of index constituents.
    """
    valid_indexes = ["sp500", "nasdaq", "dowjones"]
    if index not in valid_indexes:
        raise ValueError(f"Invalid index: {index}. Valid indexes are: {valid_indexes}")

    path = f"{index}-constituent"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def index_constituents_historical(
    apikey: str,
    index: str,
) -> RootModel[typing.List[FMPHistoricalIndexConstituent]]:
    """
    Query FMP historical constituent API.

    :param apikey: Your API key.
    :param index: The index to query (e.g., "sp500", "nasdaq", "dowjones").
    :return: A list of historical index constituents.
    """
    valid_indexes = ["sp500", "nasdaq", "dowjones"]
    if index not in valid_indexes:
        raise ValueError(f"Invalid index: {index}. Valid indexes are: {valid_indexes}")

    path = f"historical-{index}-constituent"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)
