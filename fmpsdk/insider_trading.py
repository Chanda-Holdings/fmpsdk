import typing

from pydantic import RootModel

from .models import (
    FMPAcquisitionOwnership,
    FMPInsiderTrade,
    FMPInsiderTradeStatistics,
    FMPInsiderTransactionType,
)
from .settings import DEFAULT_LIMIT
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def insider_trading(
    apikey: str,
    symbol: str = None,
    reportingCik: str = None,
    companyCik: str = None,
    transactionType: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
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
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if symbol:
        query_vars["symbol"] = symbol
    if reportingCik:
        query_vars["reportingCik"] = reportingCik
    if companyCik:
        query_vars["companyCik"] = companyCik
    if transactionType:
        query_vars["transactionType"] = transactionType

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def insider_trading_latest(
    apikey: str,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPInsiderTrade]]:
    """
    Get latest insider trading data.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int
        Page number for pagination.
    limit : int
        Number of records to return.
    Returns
    -------
    list
        List of latest insider trading data.
    """
    path = "/insider-trading/latest"
    query_vars = {"apikey": apikey, "page": page, "limit": limit}
    return __return_json(path, query_vars)


@parse_response
def insider_trading_reporting_name(
    apikey: str,
    name: str,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.Any]:
    """
    Get insider trading data by reporting name.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Reporting name.
    page : int
        Page number for pagination.
    limit : int
        Number of records to return.
    Returns
    -------
    list
        Insider trading data for the reporting name.
    """
    path = f"/insider-trading/reporting-name/{name}"
    query_vars = {"apikey": apikey, "page": page, "limit": limit}
    return __return_json(path, query_vars)


@parse_response
def insider_trading_transaction_type(
    apikey: str,
    transaction_type: str,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPInsiderTransactionType]]:
    """
    Get insider trading data by transaction type.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    transaction_type : str
        Transaction type.
    page : int
        Page number for pagination.
    limit : int
        Number of records to return.
    Returns
    -------
    list
        Insider trading data for the transaction type.
    """
    path = f"/insider-trading-transaction-type/{transaction_type}"
    query_vars = {"apikey": apikey, "page": page, "limit": limit}
    return __return_json(path, query_vars)


@parse_response
def insider_trading_statistics(
    apikey: str, symbol: str = None
) -> RootModel[typing.List[FMPInsiderTradeStatistics]]:
    """
    Query FMP /insider-trading/statistics endpoint.

    :param apikey: Your API key.
    :param symbol: Optional ticker symbol to filter statistics.
    :return: List of insider trading statistics.
    """
    path = "insider-trading/statistics"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def acquisition_ownership(
    apikey: str,
    symbol: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPAcquisitionOwnership]]:
    """
    Query FMP /acquisition-ownership/search API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "acquisition-ownership/search"
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if symbol:
        query_vars["symbol"] = symbol

    return __return_json(path=path, query_vars=query_vars)
