import typing

from pydantic import RootModel

from .models import (
    FMPDisclosureFiling,
    FMPDividend,
    FMPDividendCalendarEvent,
    FMPEarningsCalendarEvent,
    FMPProspectusFiling,
    FMPStockSplit,
    FMPStockSplitCalendarEvent,
    FMPUpcomingIPO,
)
from .url_methods import (  # Correct import for stable request function
    __return_json_stable,
)
from .utils import parse_response


@parse_response
def dividends(
    apikey: str,
    symbol: str = None,
    from_date: str = None,
    to_date: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPDividend]]:
    """
    Get dividends using the /stable/dividends endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get dividends for.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with dividends.
    """
    path = "dividends"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def dividends_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPDividendCalendarEvent]]:
    """
    Get dividends calendar using the /stable/dividends-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with dividends calendar.
    """
    path = "dividends-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def earnings_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPEarningsCalendarEvent]]:
    """
    Get earnings calendar using the /stable/earnings-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with earnings calendar.
    """
    path = "earnings-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def ipos_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPUpcomingIPO]]:
    """
    Get IPOs calendar using the /stable/ipos-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with IPOs calendar.
    """
    path = "ipos-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def ipos_disclosure(
    apikey: str,
    symbol: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPDisclosureFiling]]:
    """
    Get IPOs disclosure using the /stable/ipos-disclosure endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get IPO disclosure for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with IPOs disclosure.
    """
    path = "ipos-disclosure"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def ipos_prospectus(
    apikey: str,
    symbol: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPProspectusFiling]]:
    """
    Get IPOs prospectus using the /stable/ipos-prospectus endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get IPO prospectus for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with IPOs prospectus.
    """
    path = "ipos-prospectus"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def splits(
    apikey: str,
    symbol: str = None,
    from_date: str = None,
    to_date: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPStockSplit]]:
    """
    Get stock splits using the /stable/splits endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get splits for.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with splits.
    """
    path = "splits"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def splits_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPStockSplitCalendarEvent]]:
    """
    Get splits calendar using the /stable/splits-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with splits calendar.
    """
    path = "splits-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json_stable(path=path, query_vars=query_vars)
