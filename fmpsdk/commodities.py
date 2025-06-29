import typing

from pydantic import RootModel

from .models import FMPBulkEOD, FMPQuoteFull, FMPQuoteShort
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def commodities_quote(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get commodity quote for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Commodity symbol (e.g., 'GCUSD').
    Returns
    -------
    list
        List of commodity quote data.
    """
    path = f"/commodities-quote/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def commodities_quote_short(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Get short commodity quote for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Commodity symbol (e.g., 'GCUSD').
    Returns
    -------
    list
        List of short commodity quote data.
    """
    path = f"/commodities-quote-short/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def batch_commodity_quotes(
    apikey: str,
    symbols: typing.Optional[typing.List[str]] = None,
) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Get batch commodity quotes for a list of symbols.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list, optional
        List of commodity symbols (e.g., ['GCUSD', 'SIUSD']). If None, returns all.
    Returns
    -------
    list
        List of batch commodity quote data.
    """
    if symbols:
        path = f"/batch-commodity-quotes/{','.join(symbols)}"
    else:
        path = "/batch-commodity-quotes"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
