import typing

from pydantic import RootModel

from .general import __quotes
from .models import (
    FMPBulkEOD,
    FMPForexPair,
    FMPPressRelease,
    FMPQuoteFull,
    FMPQuoteShort,
)
from .settings import DEFAULT_LIMIT
from .url_methods import __return_json_stable
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
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def forex_news(
    apikey: str,
    symbol: str = None,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /stock_news/ API.

    :param apikey: Your API key.
    :param symbol: A forex symbol.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "forex_news"
    query_vars = {"apikey": apikey, "page": page, "limit": limit}
    if symbol:
        query_vars["symbol"] = symbol
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path, query_vars)


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
    return __return_json_stable(path, query_vars)


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
    return __return_json_stable(path, query_vars)


__all__ = [
    "forex",
    "forex_list",
    "available_forex",
    "forex_news",
    "forex_quote",
    "forex_quote_short",
    "batch_forex_quotes",
]

# All function return types should be updated to match ENDPOINT_MODEL_MAP
# from model_registry.py
