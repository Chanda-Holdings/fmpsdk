import typing

from pydantic import RootModel

from .models import (
    FMPFundDisclosure,
    FMPFundDisclosureDate,
    FMPFundHolder,
)
from .url_methods import __return_json
from .utils import parse_response


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
    path = "funds/disclosure-holders-latest"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)


@parse_response
def funds_disclosure(
    apikey: str, symbol: str, year: str, quarter: str, cik: str = None
) -> RootModel[typing.List[FMPFundDisclosure]]:
    """
    Get fund disclosure for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Fund ticker symbol.
    year : str
        The year for which to retrieve fund disclosure data (e.g., '2023').
    quarter : str
        The quarter for which to retrieve fund disclosure data (e.g., 'Q1').
    cik : str, optional
        The CIK number for the fund.

    Returns
    -------
    list
        List of fund disclosure data.
    """
    path = "funds/disclosure"
    query_vars = {"apikey": apikey, "symbol": symbol, "year": year, "quarter": quarter}
    if cik:
        query_vars["cik"] = cik
    return __return_json(path, query_vars)


@parse_response
def funds_disclosure_holders_search(
    apikey: str, name: str
) -> RootModel[typing.List[FMPFundHolder]]:
    """
    Search fund disclosure holders for a given name.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Fund or entity name.

    Returns
    -------
    list
        List of fund disclosure holders search results.
    """
    path = "funds/disclosure-holders-search"
    query_vars = {"apikey": apikey, "name": name}
    return __return_json(path, query_vars)


@parse_response
def funds_disclosure_dates(
    apikey: str, symbol: str, cik: str = None
) -> RootModel[typing.List[FMPFundDisclosureDate]]:
    """
    Get fund disclosure dates for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Fund ticker symbol.
    cik : str, optional
        The CIK number for the fund.

    Returns
    -------
    list
        List of fund disclosure dates.
    """
    path = "funds/disclosure-dates"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if cik:
        query_vars["cik"] = cik
    return __return_json(path, query_vars)
