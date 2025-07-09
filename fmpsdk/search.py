import typing

from pydantic import RootModel

from .models import (
    FMPCompanyCIKSearch,
    FMPCompanyNameSearch,
    FMPCompanyProfile,
    FMPCusipSearch,
    FMPIsinSearch,
    FMPStockScreenerResult,
    FMPSymbolSearch,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def search_symbol(
    apikey: str,
    query: str,
    exchange: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPSymbolSearch]]:
    """
    Search for stock symbols using the /stable/search-symbol endpoint.

    Parameters:
        apikey (str): Your API key.
        query (str): The search query (company name, symbol, etc.).
        exchange (str, optional): Filter by exchange short name.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with symbol search results.
    """
    path = "search-symbol"
    query_vars = {"apikey": apikey, "query": query}
    if exchange:
        query_vars["exchange"] = exchange
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)


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
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)


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
    query_vars = {"apikey": apikey, "cik": query}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def search_cusip(
    apikey: str,
    cusip: str,
) -> RootModel[typing.List[FMPCusipSearch]]:
    """
    Search for companies by CUSIP using the /stable/search-cusip endpoint.

    Parameters:
        apikey (str): Your API key.
        cusip (str): The CUSIP to search for.
    Returns:
        List of dictionaries with CUSIP search results.
    """
    path = "search-cusip"
    query_vars = {"apikey": apikey, "cusip": cusip}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def search_isin(
    apikey: str,
    isin: str,
) -> RootModel[typing.List[FMPIsinSearch]]:
    """
    Search for companies by ISIN using the /stable/search-isin endpoint.

    Parameters:
        apikey (str): Your API key.
        isin (str): The search query (ISIN or company name).
    Returns:
        List of dictionaries with ISIN search results.
    """
    path = "search-isin"
    query_vars = {"apikey": apikey, "isin": isin}

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def company_screener(
    apikey: str,
    market_cap_more_than: int = None,
    market_cap_lower_than: int = None,
    price_more_than: float = None,
    price_lower_than: float = None,
    beta_more_than: float = None,
    beta_lower_than: float = None,
    volume_more_than: float = None,
    volume_lower_than: float = None,
    dividend_more_than: float = None,
    dividend_lower_than: float = None,
    is_etf: bool = None,
    is_fund: bool = None,
    is_actively_trading: bool = None,
    sector: str = None,
    industry: str = None,
    country: str = None,
    exchange: str = None,
    limit: int = None,
    include_all_share_classes: bool = None,
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
    if market_cap_more_than is not None:
        query_vars["marketCapMoreThan"] = str(market_cap_more_than)
    if market_cap_lower_than is not None:
        query_vars["marketCapLowerThan"] = str(market_cap_lower_than)
    if price_more_than is not None:
        query_vars["priceMoreThan"] = str(price_more_than)
    if price_lower_than is not None:
        query_vars["priceLowerThan"] = str(price_lower_than)
    if beta_more_than is not None:
        query_vars["betaMoreThan"] = str(beta_more_than)
    if beta_lower_than is not None:
        query_vars["betaLowerThan"] = str(beta_lower_than)
    if volume_more_than is not None:
        query_vars["volumeMoreThan"] = str(volume_more_than)
    if volume_lower_than is not None:
        query_vars["volumeLowerThan"] = str(volume_lower_than)
    if dividend_more_than is not None:
        query_vars["dividendMoreThan"] = str(dividend_more_than)
    if dividend_lower_than is not None:
        query_vars["dividendLowerThan"] = str(dividend_lower_than)
    if is_etf is not None:
        query_vars["isETF"] = str(is_etf).lower()
    if is_fund is not None:
        query_vars["isFund"] = str(is_fund).lower()
    if is_actively_trading is not None:
        query_vars["isActivelyTrading"] = str(is_actively_trading).lower()
    if sector is not None:
        query_vars["sector"] = sector
    if industry is not None:
        query_vars["industry"] = industry
    if country is not None:
        query_vars["country"] = country
    if exchange is not None:
        query_vars["exchange"] = exchange
    if limit is not None:
        query_vars["limit"] = str(limit)
    if include_all_share_classes is not None:
        query_vars["includeAllShareClasses"] = str(include_all_share_classes).lower()
    return __return_json(path=path, query_vars=query_vars)


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
    return __return_json(path=path, query_vars=query_vars)
