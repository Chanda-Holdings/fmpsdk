import typing

from pydantic import RootModel

from .general import __quotes
from .models import *
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def available_etfs(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /symbol/available-etfs/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "symbol/available-etfs"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def etf_price_realtime(apikey: str) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Query FMP /quotes/etf/ API

    All Real-time ETF Prices.

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "etf"
    return __quotes(apikey=apikey, value=path)


@parse_response
def etf_info(apikey: str, symbol: str) -> RootModel[typing.List[FMPFundInfo]]:
    """
    Query FMP /etf-info/ API

    All Real-time ETF Prices.

    :param apikey: Your API key.
    :param symbol: ETF ticker.
    :return: A list of dictionaries.
    """
    path = "etf-info"
    query_vars = {"symbol": symbol, "apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def etf_holdings(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPFundHolding]]:
    """
    Get ETF holdings for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        ETF ticker symbol (e.g., 'SPY').

    Returns
    -------
    list
        List of ETF holdings.
    """
    path = "/etf/holdings/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def etf_asset_exposure(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPFundAssetExposure]]:
    """
    Get ETF asset exposure for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        ETF ticker symbol (e.g., 'SPY').

    Returns
    -------
    list
        List of ETF asset exposure data.
    """
    path = "/etf/asset-exposure/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def etf_sector_weightings(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundSectorWeighting]]:
    """
    Query FMP /etf/sector-weightings endpoint.

    :param apikey: Your API key.
    :param symbol: ETF ticker symbol.
    :return: List of sector weightings for the ETF.
    """
    path = "etf/sector-weightings/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)
