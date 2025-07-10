import typing

from pydantic import RootModel

from .models import (
    FMPCountry,
    FMPEarningsTranscriptList,
    FMPExchangeInfo,
    FMPFinancialStatementSymbolList,
    FMPIndustry,
    FMPSector,
    FMPSymbolAndCIKList,
    FMPSymbolAndCompanyNameList,
    FMPSymbolAndNameList,
    FMPSymbolChange,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def stock_list(
    apikey: str,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPSymbolAndCompanyNameList]]:
    """
    Get a list of all stocks using the /stable/stock-list endpoint.

    Parameters:
        apikey (str): Your API key.
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with stock list results.
    """
    path = "stock-list"
    query_vars = {"apikey": apikey}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_statement_symbol_list(
    apikey: str,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPFinancialStatementSymbolList]]:
    """
    Get a list of symbols with available financial statements using the /stable/financial-statement-symbol-list endpoint.

    Parameters:
        apikey (str): Your API key.
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with financial statement symbol list results.
    """
    path = "financial-statement-symbol-list"
    query_vars = {"apikey": apikey}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def cik_list(
    apikey: str,
    limit: int = None,
) -> RootModel[typing.List[FMPSymbolAndCIKList]]:
    """
    Get a list of all CIKs using the /stable/cik-list endpoint.

    Parameters:
        apikey (str): Your API key.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with CIK list results.
    """
    path = "cik-list"
    query_vars = {"apikey": apikey}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def symbol_change(
    apikey: str,
    date: str = None,
    symbol: str = None,
) -> RootModel[typing.List[FMPSymbolChange]]:
    """
    Get symbol change history using the /stable/symbol-change endpoint.

    Parameters:
        apikey (str): Your API key.
        date (str, optional): Filter by date (YYYY-MM-DD).
        symbol (str, optional): Filter by symbol.
    Returns:
        List of dictionaries with symbol change results.
    """
    path = "symbol-change"
    query_vars = {"apikey": apikey}
    if date:
        query_vars["date"] = date
    if symbol:
        query_vars["symbol"] = symbol
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def etf_list(
    apikey: str,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Get a list of all ETFs using the /stable/etf-list endpoint.

    Parameters:
        apikey (str): Your API key.
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with ETF list results.
    """
    path = "etf-list"
    query_vars = {"apikey": apikey}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def actively_trading_list(
    apikey: str,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Get a list of actively trading stocks using the /stable/actively-trading-list endpoint.

    Parameters:
        apikey (str): Your API key.
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with actively trading list results.
    """
    path = "actively-trading-list"
    query_vars = {"apikey": apikey}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def available_exchanges(
    apikey: str,
) -> RootModel[typing.List[FMPExchangeInfo]]:
    """
    Get a list of available exchanges using the /stable/available-exchanges endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of dictionaries with available exchanges.
    """
    path = "available-exchanges"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def available_sectors(
    apikey: str,
) -> RootModel[typing.List[FMPSector]]:
    """
    Get a list of available sectors using the /stable/available-sectors endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of dictionaries with available sectors.
    """
    path = "available-sectors"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def available_industries(
    apikey: str,
) -> RootModel[typing.List[FMPIndustry]]:
    """
    Get a list of available industries using the /stable/available-industries endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of dictionaries with available industries.
    """
    path = "available-industries"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def available_countries(
    apikey: str,
) -> RootModel[typing.List[FMPCountry]]:
    """
    Get a list of available countries using the /stable/available-countries endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of dictionaries with available countries.
    """
    path = "available-countries"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def available_indexes(
    apikey: str,
) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Get all available indexes from the /stable/index-list endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of dictionaries with available indexes.
    """
    path = "index-list"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
