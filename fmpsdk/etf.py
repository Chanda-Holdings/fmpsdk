import typing

from pydantic import RootModel

from .models import (
    FMPFundAssetExposure,
    FMPFundCountryAllocation,
    FMPFundHolding,
    FMPFundInfo,
    FMPFundSectorWeighting,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def etf_info(apikey: str, symbol: str) -> RootModel[typing.List[FMPFundInfo]]:
    """
    Query FMP /etf/info/ API

    All Real-time ETF Prices.

    :param apikey: Your API key.
    :param symbol: ETF ticker.
    :return: A list of dictionaries.
    """
    path = "etf/info"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


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
    path = "etf/holdings"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


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
    path = "etf/asset-exposure"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def etf_country_weightings(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundCountryAllocation]]:
    """
    Query FMP /etf/country-weightings endpoint.

    :param apikey: Your API key.
    :param symbol: ETF ticker symbol.
    :return: List of country weightings for the ETF.
    """
    path = "etf/country-weightings"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


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
    path = "etf/sector-weightings"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
