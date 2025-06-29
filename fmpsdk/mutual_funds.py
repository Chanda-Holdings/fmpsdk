import typing

from pydantic import RootModel

from .general import __quotes
from .models import (
    FMPFundDisclosure,
    FMPFundDisclosureDate,
    FMPFundHolder,
    FMPSymbolAndNameList,
)
from .url_methods import __return_json
from .utils import parse_response


def mutual_fund_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /quotes/mutual_fund/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "mutual_fund"
    return __quotes(apikey=apikey, value=path)


@parse_response
def funds_disclosure_holders_latest(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundHolder]]:
    """
    Get latest fund disclosure holders for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Fund ticker symbol.

    Returns
    -------
    list
        List of latest fund disclosure holders.
    """
    path = f"/funds/disclosure-holders-latest/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def funds_disclosure(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundDisclosure]]:
    """
    Get fund disclosure for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Fund ticker symbol.

    Returns
    -------
    list
        List of fund disclosure data.
    """
    path = f"/funds/disclosure/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def funds_disclosure_holders_search(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundHolder]]:
    """
    Search fund disclosure holders for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Fund ticker symbol.

    Returns
    -------
    list
        List of fund disclosure holders search results.
    """
    path = f"/funds/disclosure-holders-search/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def funds_disclosure_dates(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundDisclosureDate]]:
    """
    Get fund disclosure dates for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Fund ticker symbol.

    Returns
    -------
    list
        List of fund disclosure dates.
    """
    path = f"/funds/disclosure-dates/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def mutual_fund_holdings(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFundHolder]]:
    """
    Get mutual fund holdings for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Mutual fund ticker symbol.

    Returns
    -------
    list
        List of mutual fund holdings.
    """
    path = f"/mutual-fund-holdings/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
