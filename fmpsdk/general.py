import typing

from pydantic import RootModel

from .models import *
from .url_methods import __return_json_stable
from .utils import parse_response


def __quotes(apikey: str, value: str) -> typing.Optional[typing.List[typing.Dict]]:
    """
    Query FMP /quotes/ API.

    This API endpoint is a multifunction tool!
    :param apikey: Your API key
    :param value: The Ticker(s), Index(es), Commodity(ies), etc. symbol to query for.
    :return: A list of dictionaries.
    """
    path = "quote"
    query_vars = {"apikey": apikey, "symbol": value}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def quote(
    apikey: str, symbol: typing.Union[str, typing.List[str]]
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Query FMP Quote API.

    This API endpoint is a multifunction tool!

    :param apikey: Your API key
    :param symbol: The Ticker(s), Index(es), Commodity(ies), etc. symbol to query for.
    :return: A list of dictionaries.
    """
    if type(symbol) is list:
        symbol = ",".join(symbol)
    return __quotes(apikey=apikey, value=symbol)


@parse_response
def search_symbol(
    apikey: str,
    query: str = None,
    symbol: str = None,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPSymbolSearch]]:
    """
    Search for stock symbols using the /stable/search-symbol endpoint.

    Parameters:
        apikey (str): Your API key.
        query (str, optional): The search query (company name, symbol, etc.).
        symbol (str, optional): Alias for query.
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with symbol search results.
    """
    # Accept either query or symbol (query takes precedence)
    search_query = query or symbol
    if not search_query:
        raise ValueError("Either 'query' or 'symbol' must be provided.")
    path = "search-symbol"
    query_vars = {"apikey": apikey, "query": search_query}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def search_name(
    apikey: str,
    query: str,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPCompanyNameSearch]]:
    """
    Search for companies by name using the /stable/search-name endpoint.

    Parameters:
        apikey (str): Your API key.
        query (str): The search query (company name, etc.).
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with company name search results.
    """
    path = "search-name"
    query_vars = {"apikey": apikey, "query": query}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def search_cik(
    apikey: str,
    query: str,
    limit: int = None,
) -> RootModel[typing.List[FMPCompanyCIKSearch]]:
    """
    Search for companies by CIK using the /stable/search-cik endpoint.

    Parameters:
        apikey (str): Your API key.
        query (str): The search query (CIK or company name).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with CIK search results.
    """
    path = "search-cik"
    query_vars = {"apikey": apikey, "query": query}
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def search_cusip(
    apikey: str,
    query: str,
    limit: int = None,
) -> RootModel[typing.List[FMPCusipSearch]]:
    """
    Search for companies by CUSIP using the /stable/search-cusip endpoint.

    Parameters:
        apikey (str): Your API key.
        query (str): The search query (CUSIP or company name).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with CUSIP search results.
    """
    path = "search-cusip"
    query_vars = {"apikey": apikey, "query": query}
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def search_isin(
    apikey: str,
    query: str,
    limit: int = None,
) -> RootModel[typing.List[FMPIsinSearch]]:
    """
    Search for companies by ISIN using the /stable/search-isin endpoint.

    Parameters:
        apikey (str): Your API key.
        query (str): The search query (ISIN or company name).
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with ISIN search results.
    """
    path = "search-isin"
    query_vars = {"apikey": apikey, "query": query}
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def company_screener(
    apikey: str, **filters
) -> RootModel[typing.List[FMPStockScreenerResult]]:
    """
    Screen companies using the /stable/company-screener endpoint.

    Parameters:
        apikey (str): Your API key.
        filters: Arbitrary keyword arguments for screener filters (sector, industry, marketCapMoreThan, etc.).
    Returns:
        List of dictionaries with screener results.
    """
    path = "company-screener"
    query_vars = {"apikey": apikey}
    query_vars.update(filters)
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def search_exchange_variants(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Search for exchange variants of a symbol using the /stable/search-exchange-variants endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to search for exchange variants.
    Returns:
        List of dictionaries with exchange variant results.
    """
    path = "search-exchange-variants"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json_stable(path=path, query_vars=query_vars)


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
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


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
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


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
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)


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
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


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
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def earnings_transcript_list(
    apikey: str,
    symbol: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPEarningsTranscriptList]]:
    """
    Get a list of earnings transcripts using the /stable/earnings-transcript-list endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str, optional): Filter by symbol.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with earnings transcript list results.
    """
    path = "earnings-transcript-list"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)


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
    return __return_json_stable(path=path, query_vars=query_vars)
