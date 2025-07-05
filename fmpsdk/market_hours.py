import typing

from pydantic import RootModel

from .models import FMPExchangeInfo
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def exchange_market_hours(
    apikey: str,
    exchange: str,
) -> RootModel[typing.List[FMPExchangeInfo]]:
    """
    Get exchange market hours.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    exchange : str
        The exchange name (e.g., "NASDAQ", "NYSE").
    Returns
    -------
    list
        List of all exchange market hours.
    """
    path = "exchange-market-hours"
    query_vars = {"apikey": apikey, "exchange": exchange}
    return __return_json(path, query_vars)


@parse_response
def holidays_by_exchange(
    apikey: str,
    exchange: str,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPExchangeInfo]]:
    """
    Get all exchange holidays.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    exchange : str
        The exchange name (e.g., "NASDAQ", "NYSE").
    from_date : str, optional
        The start date for the holiday search (YYYY-MM-DD).
    to_date : str, optional
        The end date for the holiday search (YYYY-MM-DD).
    Returns
    -------
    list
        List of all exchange holidays.
    """
    path = "holidays-by-exchange"
    query_vars = {"apikey": apikey, "exchange": exchange}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json(path, query_vars)


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
    path = "all-exchange-market-hours"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
