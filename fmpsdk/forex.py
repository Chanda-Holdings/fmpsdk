import typing

from pydantic import RootModel

from .general import __quotes
from .models import (
    FMPBulkEOD,
    FMPForexPair,
    FMPQuoteFull,
    FMPQuoteShort,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def forex(apikey: str) -> RootModel[typing.List[FMPForexPair]]:
    """
    Query FMP /fx/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "fx"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def forex_list(apikey: str) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Query FMP /quotes/forex/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "forex"
    return __quotes(apikey=apikey, value=path)


@parse_response
def available_forex(apikey: str) -> RootModel[typing.List[FMPForexPair]]:
    """
    Query FMP /symbol/available-forex-currency-pairs/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "symbol/available-forex-currency-pairs"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def forex_quote(apikey: str, symbol: str) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get forex quote for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Forex symbol (e.g., 'EURUSD').

    Returns
    -------
    list
        List of forex quote data.
    """
    path = f"/forex-quote/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def forex_quote_short(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Get short forex quote for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Forex symbol (e.g., 'EURUSD').

    Returns
    -------
    list
        List of short forex quote data.
    """
    path = f"/forex-quote-short/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def batch_forex_quotes(
    apikey: str, symbols: list = None
) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Get batch forex quotes for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list, optional
        List of forex symbols (e.g., ['EURUSD', 'GBPUSD']). If None, returns all.

    Returns
    -------
    list
        List of batch forex quote data.
    """
    if symbols:
        path = f"/batch-forex-quotes/{','.join(symbols)}"
    else:
        path = "/batch-forex-quotes"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


__all__ = [
    "forex",
    "forex_list",
    "available_forex",
    "forex_quote",
    "forex_quote_short",
    "batch_forex_quotes",
]
