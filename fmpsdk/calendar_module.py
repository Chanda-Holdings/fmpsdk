import typing

from pydantic import RootModel

from .models import (
    FMPDisclosureFiling,
    FMPDividend,
    FMPDividendCalendarEvent,
    FMPDividendCalendarEventV3,
    FMPEarningsCalendarEvent,
    FMPEarningsReport,
    FMPProspectusFiling,
    FMPStockSplit,
    FMPUpcomingIPO,
)
from .url_methods import (  # Correct import for stable request function
    __return_json,
)
from .utils import parse_response


@parse_response
def dividends(
    apikey: str,
    symbol: str,
    limit: int = None,
) -> RootModel[typing.List[FMPDividend]]:
    """
    Get dividends using the /stable/dividends endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get dividends for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with dividends.
    """
    path = "dividends"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def dividends_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPDividendCalendarEventV3]]:
    """
    Get dividends calendar using the /stable/dividends-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
    Returns:
        List of dictionaries with dividends calendar.
    """
    path = "dividends-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def dividends_calendar_v3(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPDividendCalendarEvent]]:
    """
    Get dividends calendar using the /v3/stock_dividend_calendat endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
    Returns:
        List of dictionaries with dividends calendar.
    """
    path = "stock_dividend_calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars, version="v3")  # type: ignore[no-any-return]


@parse_response
def earnings(
    apikey: str,
    symbol: str,
    limit: str = None,
) -> RootModel[typing.List[FMPEarningsReport]]:
    """
    Get earnings using the /stable/earnings endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get earnings for.
        limit (str, optional): Limit the number of results.
    Returns:
        List of dictionaries with earnings.
    """
    path = "earnings"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = limit
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def earnings_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPEarningsCalendarEvent]]:
    """
    Get earnings calendar using the /stable/earnings-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
    Returns:
        List of dictionaries with earnings calendar.
    """
    path = "earnings-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def ipos_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPUpcomingIPO]]:
    """
    Get IPOs calendar using the /stable/ipos-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
    Returns:
        List of dictionaries with IPOs calendar.
    """
    path = "ipos-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def ipos_disclosure(
    apikey: str,
    symbol: str = None,
) -> RootModel[typing.List[FMPDisclosureFiling]]:
    """
    Get IPOs disclosure using the /stable/ipos-disclosure endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get IPO disclosure for.
    Returns:
        List of dictionaries with IPOs disclosure.
    """
    path = "ipos-disclosure"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def ipos_prospectus(
    apikey: str,
    symbol: str = None,
) -> RootModel[typing.List[FMPProspectusFiling]]:
    """
    Get IPOs prospectus using the /stable/ipos-prospectus endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get IPO prospectus for.
    Returns:
        List of dictionaries with IPOs prospectus.
    """
    path = "ipos-prospectus"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def splits(
    apikey: str,
    symbol: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPStockSplit]]:
    """
    Get stock splits using the /stable/splits endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): The symbol to get splits for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with splits.
    """
    path = "splits"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def splits_calendar(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPStockSplit]]:
    """
    Get splits calendar using the /stable/splits-calendar endpoint.

    Parameters:
        apikey (str): Your API key.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
    Returns:
        List of dictionaries with splits calendar.
    """
    path = "splits-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
