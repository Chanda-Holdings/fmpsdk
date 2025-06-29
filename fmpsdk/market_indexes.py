import typing

from pydantic import RootModel

# from .general import __quotes
from .models import FMPExchangeInfo, FMPQuoteShort, FMPSector, FMPSymbolAndNameList

# from .settings import (
#     DEFAULT_LIMIT,
#     DOWJONES_CONSTITUENTS_FILENAME,
#     NASDAQ_CONSTITUENTS_FILENAME,
#     SP500_CONSTITUENTS_FILENAME,
# )
from .url_methods import __return_json
from .utils import parse_response


# All function return types should be updated to match ENDPOINT_MODEL_MAP
# from model_registry.py
@parse_response
def indexes(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /quotes/index/ API.

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "quotes/index"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


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
def all_exchange_market_hours(
    apikey: str,
) -> RootModel[typing.List[FMPExchangeInfo]]:
    """
    Get all exchange market hours.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    Returns
    -------
    list
        List of all exchange market hours.
    """
    path = "/all-exchange-market-hours"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


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
    path = "/index-list"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def index_quote_short(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Get short quote for an index symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The index symbol (e.g., 'SP500').
    Returns
    -------
    list
        Short quote data for the index.
    """
    path = f"/index-quote-short/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
