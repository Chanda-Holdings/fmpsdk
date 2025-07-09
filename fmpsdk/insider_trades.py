import typing

from pydantic import RootModel

from .models import (
    FMPAcquisitionOwnership,
    FMPInsiderTrade,
    FMPInsiderTradeStatistics,
    FMPInsiderTransactionType,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def insider_trading(
    apikey: str,
    symbol: str = None,
    reportingCik: str = None,
    companyCik: str = None,
    transactionType: str = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPInsiderTrade]]:
    """
    Query FMP /insider-trading/search/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param reporting_name: Name of reporting person.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "insider-trading/search"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if reportingCik:
        query_vars["reportingCik"] = reportingCik
    if companyCik:
        query_vars["companyCik"] = companyCik
    if transactionType:
        query_vars["transactionType"] = transactionType
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def insider_trading_latest(
    apikey: str,
    date: str = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPInsiderTrade]]:
    """
    Get latest insider trading data.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    date : str, optional
        Date in 'YYYY-MM-DD' format to filter results. If None, returns all latest
        insider trading data.
    page : int
        Page number for pagination.
    limit : int
        Number of records to return.
    Returns
    -------
    list
        List of latest insider trading data.
    """
    path = "insider-trading/latest"
    query_vars = {"apikey": apikey}
    if date is not None:
        query_vars["date"] = date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)


@parse_response
def insider_trading_reporting_name(apikey: str, name: str) -> RootModel[typing.Any]:
    """
    Get insider trading data by reporting name.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Reporting name.
    Returns
    -------
    list
        Insider trading data for the reporting name.
    """
    path = f"insider-trading/reporting-name"
    query_vars = {"apikey": apikey, "name": name}
    return __return_json(path, query_vars)


@parse_response
def insider_trading_transaction_type(
    apikey: str,
) -> RootModel[typing.List[FMPInsiderTransactionType]]:
    """
    Get insider trading data by transaction type.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    Returns
    -------
    list
        Insider trading data for the transaction type.
    """
    path = f"insider-trading-transaction-type"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def insider_trading_statistics(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPInsiderTradeStatistics]]:
    """
    Query FMP /insider-trading/statistics endpoint.

    :param apikey: Your API key.
    :param symbol: Ticker symbol to filter statistics.
    :return: List of insider trading statistics.
    """
    path = "insider-trading/statistics"
    query_vars = {"apikey": apikey, "symbol": symbol}

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def acquisition_ownership(
    apikey: str,
    symbol: str,
    page: int = None,
) -> RootModel[typing.List[FMPAcquisitionOwnership]]:
    """
    Query FMP /acquisition-ownership/search API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param page: Page number for pagination.
    :return: A list of dictionaries.
    """
    path = "acquisition-of-beneficial-ownership"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if page is not None:
        query_vars["page"] = str(page)

    return __return_json(path=path, query_vars=query_vars)
