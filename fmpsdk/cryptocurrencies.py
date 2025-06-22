import logging
import typing

from pydantic import RootModel

from .general import __quotes
from .models import *
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def available_cryptocurrencies(
    apikey: str,
) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /symbol/available-cryptocurrencies/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "symbol/available-cryptocurrencies"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def cryptocurrencies_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /quotes/crypto/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "crypto"
    return __quotes(apikey=apikey, value=path)


@parse_response
def last_crypto_price(apikey: str, symbol: str) -> typing.Optional[typing.Dict]:
    """
    Query FMP /crypto/last/ API.

    Get the latest price for a cryptocurrency.

    https://site.financialmodelingprep.com/developer/docs#crypto-last-price

    Endpoint:
        https://financialmodelingprep.com/api/v4/crypto/last/{symbol}

    :param apikey: Your API key.
    :param symbol: Cryptocurrency symbol (e.g., BTCUSD).
    :return: A dictionary containing the latest price data with fields:
             - symbol: The cryptocurrency symbol
             - price: The current price
             - volume: The trading volume
             - timestamp: The timestamp of the price
    """
    if not symbol:
        logging.warning("No symbol provided for last crypto price request.")
        return None

    path = "crypto/last/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def cryptocurrency_quote(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get cryptocurrency quote for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Cryptocurrency symbol (e.g., 'BTCUSD').

    Returns
    -------
    list
        List of cryptocurrency quote data.
    """
    path = "/cryptocurrency-quote/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def cryptocurrency_quote_short(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Get short cryptocurrency quote for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Cryptocurrency symbol (e.g., 'BTCUSD').

    Returns
    -------
    list
        List of short cryptocurrency quote data.
    """
    path = "/cryptocurrency-quote-short/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def batch_crypto_quotes(
    apikey: str, symbols: list = None
) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Get batch cryptocurrency quotes for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list, optional
        List of cryptocurrency symbols (e.g., ['BTCUSD', 'ETHUSD']).
        If None, returns all.

    Returns
    -------
    list
        List of batch cryptocurrency quote data.
    """
    if symbols:
        path = f"/batch-crypto-quotes/{','.join(symbols)}"
    else:
        path = "/batch-crypto-quotes"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def cryptocurrency_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /cryptocurrency-list endpoint.

    :param apikey: Your API key.
    :return: List of all cryptocurrencies.
    """
    path = "cryptocurrency-list"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


__all__ = [
    "available_cryptocurrencies",
    "cryptocurrencies_list",
    "last_crypto_price",
    "cryptocurrency_quote",
    "cryptocurrency_quote_short",
    "batch_crypto_quotes",
    "cryptocurrency_list",
]
